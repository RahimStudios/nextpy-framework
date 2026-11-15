"""Streaming SSR - NextPy Documentation"""

from nextpy.psx import component, Link, register_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)

@component
def StreamingSSRGuide():
    enabling_example = '''"""pages/dashboard.py — opt into chunked streaming"""

from nextpy.psx import component


@component
def Dashboard():
    return (
        <div class="p-8">
            <h1>Dashboard</h1>
            {/* ... */}
        </div>
    )


def getServerSideProps(context):
    return {"props": {"stats": fetch_stats()}}


# Flush the rendered HTML to the client in ~4KB chunks instead of
# waiting for the full document:
streaming = True'''

    custom_stream_example = '''"""pages/feed.py — yield HTML chunks progressively"""

from nextpy.psx import component


@component
def Feed():
    return <div id="feed-root" />


async def stream(context):
    """Yield HTML fragments as data becomes available."""
    yield '<!DOCTYPE html><html><head><title>Feed</title></head><body>'
    yield '<div id="nextpy-page"><h1>Live feed</h1>'

    for item in await fetch_items():
        yield f'<section class="item">{item["title"]}</section>'
        await asyncio.sleep(0)  # let the event loop breathe

    yield "</div></body></html>"'''

    chunking_example = '''"""nextpy/core/streaming.py — how output is chunked"""

DEFAULT_CHUNK_SIZE = 4096

# chunk_html(html, chunk_size=4096) splits rendered HTML into
# ~4KB pieces, preferring to break right after a newline so tags
# are less likely to be split mid-flush. The minimum chunk size
# is clamped to 256 bytes.
#
# stream_route(module, context, fallback_html) is the dispatcher:
#   1. If the page module defines stream(context), its result is
#      iterated — async generators, sync generators, awaitables,
#      and plain iterables are all supported; anything else is
#      chunked via chunk_html.
#   2. Otherwise the fully rendered HTML is chunked and yielded.'''

    headers_example = '''"""Streaming response headers (nextpy/server/app.py)"""

# A streaming page responds with Starlette's StreamingResponse:
#
#   Content-Type: text/html
#   X-NextPy-Streaming: true
#   X-NextPy-Layout-Sig: <layout signature>
#   Cache-Control: no-cache            # default
#
# When the page is cacheable (no cookies / Authorization header in
# the request, no getServerSideProps), the headers instead become:
#
#   Cache-Control: public, max-age=0, s-maxage=<ttl>,
#                  stale-while-revalidate=<ttl>
#   X-NextPy-ISR: true
#
# where <ttl> is the page's `revalidate` value or the router's
# global page-cache TTL (NEXTPY_PAGE_CACHE_TTL, default 30s).'''

    example_page = '''"""pages/report.py — progressive SSR with data sections"""

import asyncio
from nextpy.psx import component


@component
def Report():
    return <div id="report-root" />


async def stream(context):
    """Shell first, then each slow section as it finishes."""
    yield ''' + '"""' + '''<!DOCTYPE html><html><head><title>Report</title></head><body>
<div id="nextpy-page"><h1>Annual report</h1>''' + '"""' + '''

    # Fast section — send immediately.
    yield await render_summary_section()

    # Slow sections stream in independently.
    for coro in (
        fetch_revenue_block(),
        fetch_users_block(),
        fetch_churn_block(),
    ):
        block = await coro
        yield block
        await asyncio.sleep(0)

    yield "</div></body></html>"'''

    limitations_example = '''"""Streaming SSR — limitations & best practices"""

# - stream(context) owns the ENTIRE HTML document when defined —
#   you must yield a complete <!DOCTYPE html>... page yourself.
# - It bypasses the router's rendered-HTML page cache, so every
#   request re-runs your generator (unless a CDN honours the ISR
#   Cache-Control headers on cacheable pages).
# - Yield strings only — each chunk is coerced with str(chunk).
# - Keep chunks small and meaningful; chunk_html aligns automatic
#   chunking to newlines, but custom streams control their own
#   boundaries.
# - Personalised responses (cookies / Authorization) are never
#   cached and always stream fresh.'''

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>How-to Guides</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Streaming SSR</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">
                        Streaming SSR
                    </h1>
                    <p class="leading-relaxed text-zinc-300">
                        Flush server-rendered HTML to the browser progressively — send the page shell immediately and stream data-heavy sections as they become ready.
                    </p>
                </header>

                <div id="overview" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Overview</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        By default NextPy renders a page fully, then sends one HTML response. Two opt-in mechanisms in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy/core/streaming.py</code> change that: set a module-level <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">streaming = True</code> flag to flush the finished document in chunks, or define <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">async def stream(context)</code> to yield HTML yourself as data arrives. Both are detected per-page by the server (<code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy/server/app.py</code>) and served through a Starlette <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">StreamingResponse</code>.
                    </p>
                </div>

                <div id="when-to-stream" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">When to stream</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Streaming pays off when part of the page is slow but the shell is fast: dashboards aggregating several APIs, feeds or reports backed by long-running queries, or pages where you want the browser to start parsing HTML (and firing sub-resource requests) before all data is ready. For ordinary pages, the default buffered response plus the router's page cache is faster and simpler — streaming also opts the response out of ETag/304 handling.
                    </p>
                </div>

                <div id="enabling" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Enabling: <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">streaming = True</code></h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Add a module-level flag to any page file. The page renders normally — layouts, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">getServerSideProps</code> / <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">getStaticProps</code>, and hydration scripts are all still applied — but the finished HTML is flushed in chunks:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/dashboard.py" snippet={enabling_example} />
                    <p class="text-base leading-7 text-zinc-300">
                        This is used in the framework's own job-board pages (<code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/jobs/index.py</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/jobs/browse.py</code>), often alongside <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">revalidate</code> for incremental regeneration.
                    </p>
                </div>

                <div id="custom-stream" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Custom <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">stream(context)</code></h2>
                    <p class="text-base leading-7 text-zinc-300">
                        For true progressive rendering, define <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">stream</code> on the page module. It receives the route <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">context</code> dict (with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">params</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">query</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">request</code>, and any props fetched by data-fetching functions) and may be an async generator, a sync generator, or return an awaitable/iterable. Each yielded value is coerced with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">str()</code> and sent immediately:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/feed.py" snippet={custom_stream_example} />
                    <p class="text-base leading-7 text-zinc-300">
                        When <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">stream</code> is present it takes precedence — the router does not render the page component for the response body, so you are responsible for emitting the full HTML document.
                    </p>
                </div>

                <div id="chunking" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">How chunking works</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The heavy lifting is in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy/core/streaming.py</code>:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="nextpy/core/streaming.py" snippet={chunking_example} />
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">chunk_html</code> prefers breaking right after a newline once past half a chunk, which keeps most tags intact per flush. With a custom <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">stream()</code> you control the boundaries yourself — yield at meaningful points (after a section closes) rather than arbitrary sizes.
                    </p>
                </div>

                <div id="headers" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Headers &amp; behaviour</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Streaming responses are marked so clients and proxies can tell them apart from buffered pages:
                    </p>
                    <EnhancedCodeBlock lang="http" filename="response headers" snippet={headers_example} />
                    <p class="text-base leading-7 text-zinc-300">
                        Because the body is a stream, there is no ETag and no <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">304 Not Modified</code> path — every navigation re-streams. The <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">X-NextPy-Layout-Sig</code> header still lets the client router detect layout changes.
                    </p>
                </div>

                <div id="caching" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Interaction with caching &amp; ISR</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Streaming and caching interact in two different ways depending on which mechanism you use:
                    </p>
                    <ul class="space-y-3 text-base leading-7 text-zinc-300 list-disc list-inside marker:text-zinc-600">
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">streaming = True</code> pages still render through <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">router.render_route()</code>, so the in-process page cache and stale-while-revalidate refresh apply exactly as for buffered pages — a cache hit is simply chunked on the way out.</li>
                        <li>A custom <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">stream(context)</code> bypasses that rendered-HTML cache entirely: your generator runs on every request. Cacheable pages still receive ISR-style <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Cache-Control</code> headers so a CDN can cache the streamed response, but the server itself does not store it.</li>
                        <li>Requests carrying cookies or an <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Authorization</code> header, and pages defining <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">getServerSideProps</code>, are never cacheable — they always stream fresh with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Cache-Control: no-cache</code>.</li>
                    </ul>
                </div>

                <div id="example" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Example: progressive page</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        A report page that sends its shell and fast sections immediately, then streams each slow data block as it resolves:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/report.py" snippet={example_page} />
                </div>

                <div id="limitations" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Limitations &amp; best practices</h2>
                    <EnhancedCodeBlock lang="python" filename="notes" snippet={limitations_example} />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/howto/plugins" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Plugin System
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/howto/testing" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Testing
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                            </span>
                        </Link>
                    </div>
                </footer>
            </article>

            <aside class="hidden xl:block w-64 shrink-0 sticky top-24 pt-4 pl-8 pb-24 h-[calc(100vh-6rem)] overflow-y-auto">
                <div class="text-sm">
                    <h4 class="font-semibold text-white mb-4 tracking-wide">On this page</h4>
                    <ul class="space-y-3 font-medium text-zinc-400 border-l border-zinc-800/50">
                        <li><a href="#overview" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Overview</a></li>
                        <li><a href="#when-to-stream" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">When to stream</a></li>
                        <li><a href="#enabling" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Enabling: streaming = True</a></li>
                        <li><a href="#custom-stream" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Custom stream(context)</a></li>
                        <li><a href="#chunking" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">How chunking works</a></li>
                        <li><a href="#headers" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Headers &amp; behaviour</a></li>
                        <li><a href="#caching" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Interaction with caching &amp; ISR</a></li>
                        <li><a href="#example" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Example: progressive page</a></li>
                        <li><a href="#limitations" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Limitations &amp; best practices</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Streaming SSR - NextPy Docs"}}


default = StreamingSSRGuide
