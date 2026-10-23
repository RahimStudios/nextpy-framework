"""Streaming SSR helpers.

Pages can opt into streaming in two ways:

1. Set ``streaming = True`` to flush the rendered HTML in chunks.
2. Define ``async def stream(context)`` (or a sync generator) to yield chunks
   directly.  This is useful for long-running data sources.

The router and server use these helpers; application code normally only needs
to declare one of the two options in a page module.
"""

from __future__ import annotations

import inspect
from typing import Any, AsyncIterator, Dict, Iterable, Optional


DEFAULT_CHUNK_SIZE = 4096


def chunk_html(html: str, chunk_size: int = DEFAULT_CHUNK_SIZE) -> Iterable[str]:
    """Split rendered HTML into chunks at safe boundaries.

    Chunks are aligned to line breaks when possible so partial tags are less
    likely to be flushed to the client.
    """
    if not html:
        return
    size = max(256, int(chunk_size or DEFAULT_CHUNK_SIZE))
    start = 0
    length = len(html)
    while start < length:
        end = min(start + size, length)
        if end < length:
            newline = html.rfind("\n", start, end)
            if newline > start + (size // 2):
                end = newline + 1
        yield html[start:end]
        start = end


async def stream_route(module: Any, context: Dict[str, Any], fallback_html: str) -> AsyncIterator[str]:
    """Yield page output from a module stream function or rendered HTML."""
    stream_fn = getattr(module, "stream", None) if module is not None else None
    if callable(stream_fn):
        result = stream_fn(context)
        if inspect.isawaitable(result):
            result = await result
        if hasattr(result, "__aiter__"):
            async for chunk in result:
                if chunk:
                    yield str(chunk)
            return
        if hasattr(result, "__iter__") and not isinstance(result, (str, bytes, dict)):
            for chunk in result:
                if chunk:
                    yield str(chunk)
            return
        if result:
            for chunk in chunk_html(str(result)):
                yield chunk
            return

    for chunk in chunk_html(fallback_html):
        yield chunk
