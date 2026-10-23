"""Framework-level caching helpers.

Provides a thread-safe in-memory TTL cache plus a ``@cached`` decorator that
works with both sync and async functions.  The cache is intentionally small and
dependency-free so it can be used from pages, server actions, data loaders and
background jobs.
"""

from __future__ import annotations

import functools
import hashlib
import inspect
import json
import threading
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional


def make_cache_key(*parts: Any) -> str:
    """Build a stable, bounded cache key from arbitrary values."""
    raw = "|".join(_stable(value) for value in parts)
    digest = hashlib.sha256(raw.encode("utf-8", "replace")).hexdigest()[:32]
    return digest


def _stable(value: Any) -> str:
    if isinstance(value, (str, int, float, bool, type(None))):
        return repr(value)
    try:
        return json.dumps(value, sort_keys=True, default=str, separators=(",", ":"))
    except Exception:
        return repr(value)


@dataclass
class CacheStats:
    hits: int = 0
    misses: int = 0
    sets: int = 0
    evictions: int = 0
    expirations: int = 0

    def to_dict(self) -> Dict[str, int]:
        return {
            "hits": self.hits,
            "misses": self.misses,
            "sets": self.sets,
            "evictions": self.evictions,
            "expirations": self.expirations,
        }


class MemoryCache:
    """Thread-safe TTL cache with a bounded number of entries."""

    def __init__(self, maxsize: int = 2048):
        self.maxsize = max(1, int(maxsize))
        self._store: Dict[str, tuple[Any, float, float]] = {}
        self._lock = threading.RLock()
        self._stats = CacheStats()

    def get(self, key: str, default: Any = None) -> Any:
        entry = self.get_entry(key)
        return default if entry is None else entry[0]

    def get_entry(self, key: str) -> Optional[tuple[Any, float, float]]:
        """Return ``(value, expires_at, created_at)`` or ``None``."""
        with self._lock:
            item = self._store.get(key)
            if item is None:
                self._stats.misses += 1
                return None
            value, expires_at, created_at = item
            if time.time() >= expires_at:
                self._store.pop(key, None)
                self._stats.misses += 1
                self._stats.expirations += 1
                return None
            self._stats.hits += 1
            return value, expires_at, created_at

    def set(self, key: str, value: Any, ttl: float = 60) -> None:
        ttl = max(0.0, float(ttl))
        now = time.time()
        with self._lock:
            if len(self._store) >= self.maxsize and key not in self._store:
                self._evict_one()
            self._store[key] = (value, now + ttl, now)
            self._stats.sets += 1

    def delete(self, key: str) -> bool:
        with self._lock:
            return self._store.pop(key, None) is not None

    def clear(self, prefix: Optional[str] = None) -> int:
        with self._lock:
            if prefix is None:
                count = len(self._store)
                self._store.clear()
                return count
            keys = [key for key in self._store if key.startswith(prefix)]
            for key in keys:
                self._store.pop(key, None)
            return len(keys)

    def cleanup(self) -> int:
        now = time.time()
        with self._lock:
            expired = [key for key, (_, expiry, _) in self._store.items() if now >= expiry]
            for key in expired:
                self._store.pop(key, None)
            self._stats.expirations += len(expired)
            return len(expired)

    def _evict_one(self) -> None:
        if not self._store:
            return
        oldest = min(self._store.items(), key=lambda item: item[1][2])[0]
        self._store.pop(oldest, None)
        self._stats.evictions += 1

    @property
    def stats(self) -> CacheStats:
        return self._stats

    def __len__(self) -> int:
        return len(self._store)


_cache = MemoryCache()


def get_cache() -> MemoryCache:
    return _cache


def cached(
    ttl: float = 60,
    *,
    key: Optional[Callable[..., str]] = None,
    namespace: str = "default",
    cache: Optional[MemoryCache] = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Cache a sync or async function result.

    The default key includes the function's module, qualified name, args and
    kwargs, so identical calls share a cache entry.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        target_cache = cache or _cache
        base = f"{namespace}:{func.__module__}.{func.__qualname__}"

        def build_key(args: tuple[Any, ...], kwargs: Dict[str, Any]) -> str:
            if key is not None:
                return f"{base}:{key(*args, **kwargs)}"
            return f"{base}:{make_cache_key(args, kwargs)}"

        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                cache_key = build_key(args, kwargs)
                value = target_cache.get(cache_key)
                if value is not None:
                    return value
                result = await func(*args, **kwargs)
                if result is not None:
                    target_cache.set(cache_key, result, ttl)
                return result

            async_wrapper.cache_clear = lambda: target_cache.clear(base)  # type: ignore[attr-defined]
            return async_wrapper

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            cache_key = build_key(args, kwargs)
            value = target_cache.get(cache_key)
            if value is not None:
                return value
            result = func(*args, **kwargs)
            if result is not None:
                target_cache.set(cache_key, result, ttl)
            return result

        sync_wrapper.cache_clear = lambda: target_cache.clear(base)  # type: ignore[attr-defined]
        return sync_wrapper

    return decorator


def invalidate(prefix: str = "", cache: Optional[MemoryCache] = None) -> int:
    """Delete all entries, or entries whose keys start with ``prefix``."""
    return (cache or _cache).clear(prefix or None)
