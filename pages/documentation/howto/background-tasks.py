"""Background Tasks & Job Queue - NextPy Documentation"""

from nextpy.psx import component, Link, register_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)

@component
def BackgroundTasksGuide():
    task_example = '''"""Background tasks for NextPy — emails, cleanup, cache warming."""

from nextpy import background_task, enqueue


@background_task
async def send_welcome_email(user_id: int):
    """Runs on a worker thread — never blocks the HTTP request."""
    user = fetch_user(user_id)
    await mailer.send(user.email, "Welcome!")


def post(request, params):
    """POST /api/signup — enqueue the email and return instantly."""
    data = request.json()
    user_id = create_user(data["email"])
    enqueue(send_welcome_email, user_id)   # fire-and-forget
    return {"user_id": user_id, "queued": True}'''

    queue_example = '''"""Custom named queues with retries and error hooks."""

from nextpy import get_queue, BackgroundQueue


# Named queues are created lazily; each gets its own thread pool.
email_queue = BackgroundQueue(
    name="email",
    workers=4,
    max_retries=3,
    retry_delay=5.0,                     # seconds between attempts
    on_error=lambda exc: log.error("email task failed: %s", exc),
)


@email_queue.task
async def send_receipt(order_id: str):
    await send_receipt_email(order_id)


def handle_order(order_id: str):
    send_receipt(order_id)               # returns a Future immediately
    stats = email_queue.stats            # QueueStats snapshot
    print(stats.to_dict())'''

    action_example = '''"""Enqueue work from a server action."""

import time

from nextpy.server_actions import server_action
from nextpy import enqueue

_task_log = []


def _resize_image(path: str) -> str:
    """CPU-bound work — runs on a queue worker, not the event loop."""
    time.sleep(1)
    result = f"resized:{path}"
    _task_log.append({"path": path, "result": result})
    return result


@server_action()
def queue_image_resize(path: str):
    future = enqueue(_resize_image, path)
    return {"queued": True, "path": path}


@server_action()
def get_task_log():
    return {"completed": list(_task_log)}'''

    monitoring_example = '''"""Inspect queue health and task futures."""

from concurrent.futures import as_completed
from nextpy import get_queue

queue = get_queue()          # the shared default queue

# QueueStats fields: submitted, completed, failed, retried, running
print(queue.stats.to_dict())

# submit() returns a concurrent.futures.Future
future = queue.submit(expensive_report, "weekly")
if future.done():
    print(future.result())
elif future.exception():
    print("task raised:", future.exception())'''

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>How-to Guides</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Background Tasks &amp; Job Queue</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">
                        Background Tasks &amp; Job Queue
                    </h1>
                    <p class="leading-relaxed text-zinc-300">
                        Run slow work — emails, image processing, cleanup jobs, webhook fan-out — off the request path with NextPy's built-in retrying thread-pool queue. No broker, no extra dependencies.
                    </p>
                </header>

                <div id="overview" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Overview</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        NextPy ships a small, dependency-free background queue in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy.tasks</code>. It is a process-local <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">ThreadPoolExecutor</code> with optional retries — ideal for work that should not block an HTTP request or server action. Both sync functions and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">async def</code> callables are supported; coroutine functions are executed via <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">asyncio.run</code> on the worker thread.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        Everything is exposed at the top level: <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">from nextpy import enqueue, background_task, get_queue, BackgroundQueue</code>. A shared default queue (2 workers) is created automatically; named queues give you isolated pools.
                    </p>
                </div>

                <div id="quick-start" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Quick start</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Decorate a function with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">background_task</code> (exported as <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">task</code> inside <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy.tasks</code>) and every call is enqueued instead of running inline. The decorated function returns a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">concurrent.futures.Future</code>, so you can still inspect the result later.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/api/signup.py" snippet={task_example} />
                </div>

                <div id="queue-internals" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Queue internals</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">BackgroundQueue</code> wraps a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">ThreadPoolExecutor</code>. Its core methods are <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">submit(func, *args, **kwargs)</code> (aliased as <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">enqueue</code>), the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">.task</code> decorator, a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">stats</code> property returning <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">QueueStats</code>, and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">stop(wait=True)</code> for shutdown.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="app/queues.py" snippet={queue_example} />
                </div>

                <div id="retries" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Retries &amp; error handling</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Pass <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">max_retries</code> and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">retry_delay</code> (seconds, slept on the worker thread) to re-run a failing task. After retries are exhausted the exception propagates to the returned <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Future</code> and the optional <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">on_error</code> callback fires. Retries are counted in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">QueueStats.retried</code>.
                    </p>
                </div>

                <div id="server-actions" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Using with server actions</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The most common pattern: a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">@server_action</code> validates input, enqueues the heavy work, and returns immediately so the client never waits. Because the worker runs in a separate thread, CPU-bound or blocking calls (synchronous DB drivers, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">time.sleep</code>, file I/O) are safe there.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/actions/jobs.py" snippet={action_example} />
                </div>

                <div id="monitoring" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Monitoring &amp; inspection</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">QueueStats</code> tracks <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">submitted</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">completed</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">failed</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">retried</code>, and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">running</code> counts. <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">to_dict()</code> gives you a JSON-safe snapshot for an admin endpoint, and every <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">submit</code> returns a standard <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Future</code> you can poll, cancel, or wait on.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/api/admin/queue.py" snippet={monitoring_example} />
                </div>

                <div id="production-notes" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Production notes</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The queue is <strong class="text-white">process-local and in-memory</strong>: queued work is lost on restart, jobs are not shared across worker processes, and there is no persistence or dead-letter store. It is perfect for single-process deployments and dev/staging. For multi-process or durable workloads, swap in an external broker (Celery, RQ, or Redis-backed queues) behind the same submit/fire-and-forget pattern — the framework keeps the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">submit</code> API stable so call sites do not change.
                    </p>
                    <p class="text-base leading-7 text-zinc-300">
                        Submitting to a stopped queue raises <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">RuntimeError</code>. Use <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">get_queue("name")</code> for named pools — they are created lazily with default settings, so prefer constructing <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">BackgroundQueue</code> directly when you need custom workers or retries.
                    </p>
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/howto/testing" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Testing
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/howto/realtime" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Real-Time: WebSockets, State Sync &amp; Multi-User
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
                        <li><a href="#quick-start" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Quick start</a></li>
                        <li><a href="#queue-internals" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Queue internals</a></li>
                        <li><a href="#retries" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Retries &amp; error handling</a></li>
                        <li><a href="#server-actions" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Using with server actions</a></li>
                        <li><a href="#monitoring" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Monitoring &amp; inspection</a></li>
                        <li><a href="#production-notes" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Production notes</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Background Tasks & Job Queue - NextPy Docs"}}

default = BackgroundTasksGuide
