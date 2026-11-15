"""Server Actions - NextPy Documentation"""

from nextpy.psx import component, Link, register_component, interactive_component, useState, useEffect
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)


@component
def ServerActionsAPI():
    action_example = """# pages/actions/todo_actions.py
from nextpy.server_actions import server_action, ValidationError
from nextpy.db import get_session, Todo

@server_action(name="create_todo")
async def create_todo(title: str):
    if not title:
        raise ValidationError("title", "Title cannot be empty")
    db = next(get_session())
    todo = Todo(title=title, completed=False)
    db.add(todo)
    db.commit()
    db.close()
    return {"id": todo.id}"""

    client_example = """from nextpy.psx import interactive_component, useState, useEffect, callServerAction

@interactive_component
def TodoForm():
    [title, setTitle] = useState("")
    [_server_result, _setServerResult] = useState(None)
    [_server_loading, _setServerLoading] = useState(False)

    def submit(e):
        e.preventDefault()
        callServerAction("create_todo", {"title": title})

    def handle_result():
        if _server_result and _server_result.get("success"):
            setTitle("")
            window.location.reload()

    useEffect(handle_result, [_server_result])

    return (
        <form onsubmit={submit}>
            <input value={title} oninput={lambda e: setTitle(e.target.value)} />
            <button type="submit" disabled={_server_loading}>
                {"Saving..." if _server_loading else "Add"}
            </button>
        </form>
    )"""

    options_example = """@server_action(
    name="update_profile",
    schema=ProfileSchema,      # Pydantic model or ActionSchema
    auth=True,                 # require authenticated user
    roles=("admin",),          # optional role restriction
)"""

    formvalidator_example = """from nextpy.server_actions import FormValidator

# Static helpers — each returns a bool or (bool, message) tuple.
FormValidator.validate_email("user@example.com")        # -> True
FormValidator.validate_password("Abc12345")            # -> (True, "")
FormValidator.validate_password("weak")                # -> (False, "Password must contain uppercase letters")

FormValidator.validate_required_fields(
    {"email": "a@b.com", "name": ""},
    ["email", "name"],
)
# -> (False, "Field 'name' is required")"""

    actionschema_example = """from nextpy.server_actions import ActionSchema, FormValidator, server_action

profile_schema = ActionSchema(
    email={"type": str, "required": True,
           "validator": lambda v: (True, "") if FormValidator.validate_email(v) else (False, "Invalid email")},
    age={"type": int},
    bio={"type": str},
)

@server_action(name="update_profile", schema=profile_schema)
async def update_profile(email: str, age: int = 0, bio: str = ""):
    ..."""

    builtin_example = """from nextpy.server_actions import get_health_status, get_current_user

# Registered automatically — call them like any other action:
#   callServerAction("get_health_status")
#   callServerAction("get_current_user")

# get_health_status() ->
#   {"status": "healthy", "version": "5.0.0", "timestamp": "..."}

# get_current_user(request) ->
#   {"id": 1, "email": "...", "username": "...", "role": "..."} or None"""

    register_example = """from nextpy.server_actions import ServerAction

# register() is a classmethod returning a decorator — same as @server_action
login_action = ServerAction.register(name="login", validate=check_credentials)

@login_action
async def login(email: str, password: str):
    ...

# Inspect the registry
ServerAction.list_actions()      # {"login": "<docstring>", ...}
ServerAction.get_action("login") # the registered wrapper

# Or execute an action directly inside server code:
#   await ServerAction.execute("login", request, params={"email": ..., "password": ...})"""

    context_example = """from nextpy.server_actions import server_action

@server_action(name="my_action", auth=True, roles=("admin",))
async def my_action(user, request, session, db, response, title: str):
    # execute() injects context params by name:
    #   user     - authenticated User (requires auth=True)
    #   request  - FastAPI Request
    #   response - FastAPI Response (set cookies/headers)
    #   session / db - a DB session, closed after the call
    ..."""

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Reference API</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Server Actions</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">Server Actions</h1>
                    <p class="leading-relaxed text-zinc-300">
                        Call Python functions from the browser without writing an API route. Actions are registered with <code class="font-mono text-sm">@server_action</code> and invoked via <code class="font-mono text-sm">callServerAction</code>.
                    </p>
                </header>

                <div id="defining" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Defining an action</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Put actions in <code class="font-mono text-xs">pages/actions/</code> (or any imported module). The decorator registers the function under a name; params are filtered to the function signature and validated.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/actions/todo_actions.py" snippet={action_example} />
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">ValidationError(field, message)</code> &mdash; returned to the client as a structured error.</li>
                        <li><code class="font-mono text-xs">ServerActionError(message, code)</code> &mdash; for domain failures like "not found".</li>
                        <li>Every result is wrapped as <code class="font-mono text-xs">{"{success, data, timestamp}"}</code> or <code class="font-mono text-xs">{"{success: false, error}"}</code>.</li>
                    </ul>
                </div>

                <div id="options" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Options</h2>
                    <EnhancedCodeBlock lang="python" filename="pages/actions/profile.py" snippet={options_example} />
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">schema</code> &mdash; a Pydantic model or <code class="font-mono text-xs">ActionSchema</code> for input validation.</li>
                        <li><code class="font-mono text-xs">auth=True</code> &mdash; rejects unauthenticated calls.</li>
                        <li><code class="font-mono text-xs">roles</code> &mdash; tuple of allowed roles.</li>
                    </ul>
                </div>

                <div id="calling" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Calling from a component</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">callServerAction(name, params)</code> POSTs to <code class="font-mono text-xs">/__nextpy/actions/execute</code> and writes the result into reserved state keys: <code class="font-mono text-xs">_server_result</code> and <code class="font-mono text-xs">_server_loading</code>. React to results with <code class="font-mono text-xs">useEffect(..., [_server_result])</code>.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/jobs/create.py" snippet={client_example} />
                </div>

                <div id="form-validator" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">FormValidator</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">FormValidator</code> is a collection of static helpers you can call inside actions (or validators) for common checks. Each returns a boolean, or a <code class="font-mono text-xs">(is_valid, message)</code> tuple where a message is provided.
                    </p>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Method</th>
                                    <th class="text-left px-4 py-3 font-semibold">Signature</th>
                                    <th class="text-left px-4 py-3 font-semibold">Returns</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">validate_email</td><td class="px-4 py-3 font-mono text-xs">(email: str) -&gt; bool</td><td class="px-4 py-3">True when the address matches a standard email pattern.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">validate_password</td><td class="px-4 py-3 font-mono text-xs">(password: str) -&gt; (bool, str)</td><td class="px-4 py-3">Enforces &ge;8 chars plus uppercase, lowercase, and a digit; returns a failure reason.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">validate_required_fields</td><td class="px-4 py-3 font-mono text-xs">(data: dict, required_fields: list) -&gt; (bool, str)</td><td class="px-4 py-3">True when every listed key exists and is non-empty.</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <EnhancedCodeBlock lang="python" filename="pages/actions/validators.py" snippet={formvalidator_example} />
                    <p class="text-base leading-7 text-zinc-300">
                        To turn a failed check into a client-visible error, raise <code class="font-mono text-xs">ValidationError(field, message)</code> inside the action, or return a non-<code class="font-mono text-xs">True</code> value (or a <code class="font-mono text-xs">&#123;"field": ..., "message": ...&#125;</code> dict) from a registered validator.
                    </p>
                </div>

                <div id="action-schema" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">ActionSchema</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">ActionSchema</code> declares field rules declaratively and is passed via <code class="font-mono text-xs">schema=</code> on the decorator. Each field config supports:
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">type</code> &mdash; a Python type checked with <code class="font-mono text-xs">isinstance</code> (e.g. <code class="font-mono text-xs">str</code>, <code class="font-mono text-xs">int</code>).</li>
                        <li><code class="font-mono text-xs">required</code> &mdash; when true, a missing key produces a field error.</li>
                        <li><code class="font-mono text-xs">validator</code> &mdash; a callable <code class="font-mono text-xs">value -&gt; (is_valid, message)</code> run after the type check.</li>
                    </ul>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">schema.validate(data)</code> returns <code class="font-mono text-xs">(is_valid, errors_dict)</code>. On success the action receives the validated kwargs; on failure the client gets <code class="font-mono text-xs">&#123;"success": false, "error": &#123;"type": "validation", "fields": &#123;...&#125;&#125;&#125;</code>. Pydantic models (v1 <code class="font-mono text-xs">parse_obj</code> / v2 <code class="font-mono text-xs">model_validate</code>) are also accepted as schemas.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/actions/profile.py" snippet={actionschema_example} />
                </div>

                <div id="built-in-actions" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Built-in actions</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Two actions are registered automatically when <code class="font-mono text-xs">nextpy.server_actions</code> is imported:
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="font-mono text-xs">get_health_status</code> &mdash; returns <code class="font-mono text-xs">&#123;"status": "healthy", "version": "5.0.0", "timestamp": ...&#125;</code>. Useful for uptime checks and load-balancer probes.</li>
                        <li><code class="font-mono text-xs">get_current_user</code> &mdash; resolves the authenticated user from the request and returns <code class="font-mono text-xs">&#123;"id", "email", "username", "role"&#125;</code>, or <code class="font-mono text-xs">None</code> when unauthenticated.</li>
                    </ul>
                    <EnhancedCodeBlock lang="python" filename="pages/actions/builtin.py" snippet={builtin_example} />
                </div>

                <div id="server-action-class" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">ServerAction class API</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        <code class="font-mono text-xs">server_action</code> is an alias for <code class="font-mono text-xs">ServerAction.register</code>. The class keeps class-level registries (<code class="font-mono text-xs">_actions</code>, <code class="font-mono text-xs">_validators</code>, <code class="font-mono text-xs">_schemas</code>, <code class="font-mono text-xs">_auth</code>, <code class="font-mono text-xs">_roles</code>) and exposes:
                    </p>
                    <div class="overflow-x-auto rounded-xl border border-zinc-800/60">
                        <table class="w-full text-sm">
                            <thead class="bg-zinc-900/60 text-zinc-300">
                                <tr>
                                    <th class="text-left px-4 py-3 font-semibold">Member</th>
                                    <th class="text-left px-4 py-3 font-semibold">Description</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-zinc-800/60 text-zinc-400">
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">register(name=None, validate=None, *, schema=None, auth=False, roles=None)</td><td class="px-4 py-3">Decorator registering an action. Supports bare <code class="font-mono text-xs">@server_action</code> (no parentheses).</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">get_action(name)</td><td class="px-4 py-3">Returns the registered wrapper for <code class="font-mono text-xs">name</code>, or <code class="font-mono text-xs">None</code>.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">list_actions()</td><td class="px-4 py-3">Dict of action name → first line of its docstring.</td></tr>
                                <tr><td class="px-4 py-3 font-mono text-xs text-zinc-200">execute(name, request, response=None, params=None)</td><td class="px-4 py-3">Async executor used by the HTTP endpoint; returns the <code class="font-mono text-xs">&#123;"success", "data"/"error", "timestamp"&#125;</code> envelope.</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <p class="text-base leading-7 text-zinc-300">
                        During <code class="font-mono text-xs">execute</code>, params are filtered to the function signature (unknown keys and the reserved names <code class="font-mono text-xs">request</code>, <code class="font-mono text-xs">response</code>, <code class="font-mono text-xs">session</code>, <code class="font-mono text-xs">db</code>, <code class="font-mono text-xs">user</code> are dropped from client input, then re-injected server-side by name). With <code class="font-mono text-xs">auth=True</code>, a missing user yields HTTP 401 and a role mismatch yields 403; <code class="font-mono text-xs">request.state.user</code>/<code class="font-mono text-xs">user_id</code> are set.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="pages/actions/login.py" snippet={register_example} />
                    <EnhancedCodeBlock lang="python" filename="pages/actions/context.py" snippet={context_example} />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/reference/events" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Event System
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/reference/metadata" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Metadata &amp; SEO
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
                        <li><a href="#defining" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Defining an action</a></li>
                        <li><a href="#options" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Options</a></li>
                        <li><a href="#calling" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Calling from a component</a></li>
                        <li><a href="#form-validator" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">FormValidator</a></li>
                        <li><a href="#action-schema" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">ActionSchema</a></li>
                        <li><a href="#built-in-actions" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Built-in actions</a></li>
                        <li><a href="#server-action-class" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">ServerAction class API</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Server Actions - NextPy Docs"}}


default = ServerActionsAPI

