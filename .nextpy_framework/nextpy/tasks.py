"""Lightweight background task queue for NextPy applications.

The queue is process-local and dependency-free.  Use it for work that should
not block an HTTP request: emails, webhook fan-out, cache warming, cleanup,
thumbnail generation, etc.  For multi-process deployments a durable queue
(Celery/RQ/Redis) can be swapped in behind the same ``submit`` API.
"""

from __future__ import annotations

import asyncio
import functools
import inspect
import threading
import time
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional


@dataclass
class QueueStats:
    submitted: int = 0
    completed: int = 0
    failed: int = 0
    retried: int = 0
    running: int = 0

    def to_dict(self) -> Dict[str, int]:
        return {
            "submitted": self.submitted,
            "completed": self.completed,
            "failed": self.failed,
            "retried": self.retried,
            "running": self.running,
        }


class BackgroundQueue:
    """A small retrying thread-pool task queue."""

    def __init__(
        self,
        name: str = "default",
        *,
        workers: int = 2,
        max_retries: int = 0,
        retry_delay: float = 0.0,
        on_error: Optional[Callable[[BaseException], None]] = None,
    ):
        self.name = name
        self.max_retries = max(0, int(max_retries))
        self.retry_delay = max(0.0, float(retry_delay))
        self.on_error = on_error
        self._executor = ThreadPoolExecutor(
            max_workers=max(1, int(workers)), thread_name_prefix=f"nextpy-{name}"
        )
        self._stats = QueueStats()
        self._lock = threading.Lock()
        self._stopped = False

    def submit(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Future:
        """Schedule ``func`` and return its future."""
        if self._stopped:
            raise RuntimeError(f"Queue '{self.name}' has been stopped")
        with self._lock:
            self._stats.submitted += 1
        return self._executor.submit(self._run, func, args, kwargs)

    enqueue = submit

    def task(self, func: Callable[..., Any]) -> Callable[..., Future]:
        """Decorator that enqueues calls instead of running them inline."""
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Future:
            return self.submit(func, *args, **kwargs)

        wrapper.submit = lambda *args, **kwargs: self.submit(func, *args, **kwargs)  # type: ignore[attr-defined]
        return wrapper

    def _run(self, func: Callable[..., Any], args: tuple[Any, ...], kwargs: Dict[str, Any]) -> Any:
        attempt = 0
        with self._lock:
            self._stats.running += 1
        try:
            while True:
                try:
                    result = self._invoke(func, args, kwargs)
                    with self._lock:
                        self._stats.completed += 1
                    return result
                except BaseException as exc:
                    if attempt < self.max_retries:
                        attempt += 1
                        with self._lock:
                            self._stats.retried += 1
                        if self.retry_delay:
                            time.sleep(self.retry_delay)
                        continue
                    with self._lock:
                        self._stats.failed += 1
                    if self.on_error:
                        try:
                            self.on_error(exc)
                        except Exception:
                            pass
                    raise
        finally:
            with self._lock:
                self._stats.running = max(0, self._stats.running - 1)

    @staticmethod
    def _invoke(func: Callable[..., Any], args: tuple[Any, ...], kwargs: Dict[str, Any]) -> Any:
        if inspect.iscoroutinefunction(func):
            return asyncio.run(func(*args, **kwargs))
        result = func(*args, **kwargs)
        if inspect.isawaitable(result):
            return asyncio.run(result)
        return result

    @property
    def stats(self) -> QueueStats:
        return self._stats

    def stop(self, wait: bool = True) -> None:
        self._stopped = True
        self._executor.shutdown(wait=wait, cancel_futures=False)


_queues: Dict[str, BackgroundQueue] = {}
_queues_lock = threading.Lock()
_default_queue = BackgroundQueue("default", workers=2)


def get_queue(name: str = "default") -> BackgroundQueue:
    if name == "default":
        return _default_queue
    with _queues_lock:
        if name not in _queues:
            _queues[name] = BackgroundQueue(name)
        return _queues[name]


def enqueue(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Future:
    """Enqueue a task on the default queue."""
    return _default_queue.submit(func, *args, **kwargs)


def task(func: Callable[..., Any]) -> Callable[..., Future]:
    """Decorator for default-queue tasks."""
    return _default_queue.task(func)
