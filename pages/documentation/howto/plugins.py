"""Plugin System - NextPy Documentation"""

from nextpy.psx import component, Link, register_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)

@component
def PluginsGuide():
    plugin_example = '''"""my_plugin.py — a custom JSX transform plugin"""

from pathlib import Path
from nextpy.plugins import JSXPlugin, PluginContext, PluginResult


class Plugin(JSXPlugin):
    """The loader looks for a class named 'Plugin'."""

    def __init__(self):
        super().__init__("my-plugin", "1.0.0")

    def transform(self, context: PluginContext) -> PluginResult:
        content = context.file_content
        # Transform the file content here, e.g. inject a banner:
        if "<!-- nextpy-plugin -->" not in content:
            content = "<!-- nextpy-plugin -->\\n" + content
        return PluginResult(
            success=True,
            content=content,
            metadata={"processed": str(context.file_path)},
            errors=[],
            warnings=[],
        )'''

    register_example = '''"""Register plugins programmatically"""

from pathlib import Path
from nextpy.plugins import plugin_manager

# Load a plugin file (must define a 'Plugin' class subclassing JSXPlugin)
plugin = plugin_manager.load_plugin_from_file(Path("plugins/my_plugin.py"))
plugin_manager.register_plugin(plugin)

# Or load every .py file in a directory
plugin_manager.load_plugins_from_directory(Path("plugins"))

# Inspect what's registered
info = plugin_manager.get_plugin_info()
# {"total_plugins": ..., "enabled_plugins": ..., "plugins": [...]}'''

    lifecycle_example = '''"""Hooks fired around the transform pipeline"""

from nextpy.plugins import plugin_manager

# Valid events: before_transform, after_transform, on_error, on_success
def log_before(context):
    print(f"Transforming {context.file_path}")

def log_after(context, result):
    print(f"Done. Errors: {result.errors}")

plugin_manager.add_hook("before_transform", log_before)
plugin_manager.add_hook("after_transform", log_after)'''

    cli_example = '''$ nextpy plugin list
$ nextpy plugin enable tailwind
$ nextpy plugin disable typescript
$ nextpy plugin configure tailwind --config '{"optimize_classes": true}'
$ nextpy plugin load plugins/my_plugin.py'''

    config_example = '''{
  "plugins": {
    "tailwind": {
      "enabled": true,
      "config": {
        "optimize_classes": true,
        "remove_duplicates": true,
        "purge_unused": true
      },
      "priority": 10
    },
    "typescript": {
      "enabled": true,
      "config": {
        "strict": true,
        "generate_types": true
      },
      "priority": 5
    }
  }
}'''

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>How-to Guides</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Plugin System</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">
                        Plugin System
                    </h1>
                    <p class="leading-relaxed text-zinc-300">
                        Extend NextPy's JSX processing pipeline with custom transform plugins — written in plain Python and managed through code or the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy plugin</code> CLI.
                    </p>
                </header>

                <div id="overview" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Overview</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        NextPy's plugin system lives in the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy.plugins</code> package. Plugins subclass <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">JSXPlugin</code> and implement a single <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">transform()</code> method that receives a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">PluginContext</code> (file path, content, config) and returns a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">PluginResult</code>. A global <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">plugin_manager</code> collects plugins, runs them in priority order during JSX preprocessing, and exposes hooks for observing each transform.
                    </p>
                </div>

                <div id="writing-a-plugin" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Writing a plugin</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Create a Python file that defines a class named <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">Plugin</code> subclassing <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">JSXPlugin</code>. The constructor takes a name and version; <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">transform()</code> must return a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">PluginResult</code> with the (possibly modified) content. Optional overrides: <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">can_handle()</code> to skip files, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">validate_config()</code> to check configuration, and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">get_dependencies()</code> to declare requirements.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="plugins/my_plugin.py" snippet={plugin_example} />
                </div>

                <div id="plugin-lifecycle" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Plugin lifecycle</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        When content is transformed, the manager fires <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">before_transform</code> hooks, then runs each enabled plugin in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">PluginPriority</code> order (HIGHEST → LOWEST). Each plugin's <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">can_handle()</code> gate is checked, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">transform()</code> runs on the accumulated content, and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">on_success</code> or <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">on_error</code> hooks fire per plugin. <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">after_transform</code> hooks run last with the final result.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="hooks.py" snippet={lifecycle_example} />
                </div>

                <div id="registering-plugins" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Registering and loading plugins</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The global <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">plugin_manager</code> (an instance of <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">PluginManager</code>) handles discovery and registration. Plugin names must be unique — re-registering raises <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">PluginError</code>. Use <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">enable_plugin()</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">disable_plugin()</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">configure_plugin()</code>, and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">unregister_plugin()</code> to manage the registry at runtime.
                    </p>
                    <EnhancedCodeBlock lang="python" filename="register_plugins.py" snippet={register_example} />
                </div>

                <div id="cli-management" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Managing plugins via the CLI</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy plugin</code> command group wraps the same manager. <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">list</code> shows every plugin with its enabled state, version, priority, and dependencies; <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">enable</code> / <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">disable</code> toggle a plugin by name; <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">configure</code> merges a JSON config object into the plugin's config; and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">load</code> imports a plugin file and registers it.
                    </p>
                    <EnhancedCodeBlock lang="bash" filename="terminal" snippet={cli_example} />
                </div>

                <div id="builtin-plugins" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Built-in plugins</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        NextPy ships five built-in JSX plugins, exported from <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy.plugins</code>:
                    </p>
                    <ul class="list-disc pl-6 space-y-2 text-base leading-7 text-zinc-300">
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">ValidationPlugin</code> ("validation") — validates JSX content during preprocessing.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">TailwindPlugin</code> ("tailwind") — deduplicates and optimizes Tailwind CSS classes in <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">class</code>/<code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">className</code> attributes.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">TypeScriptPlugin</code> ("typescript") — adds type annotations and reports type issues as warnings.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">StylePlugin</code> ("style") — converts Python-style <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">style={...}</code> objects into CSS strings.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">ComponentPlugin</code> ("component") — validates and enhances component usage.</li>
                    </ul>
                    <p class="text-base leading-7 text-zinc-300">
                        Plugin failures are non-fatal: errors are collected into the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">PluginResult</code> and logged while preprocessing continues.
                    </p>
                </div>

                <div id="configuration" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Configuration</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Plugin settings are stored in a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy-plugins.json</code> file at the project root. Each entry controls whether the plugin is <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">enabled</code>, its <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">config</code> dictionary, and its execution <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">priority</code>:
                    </p>
                    <EnhancedCodeBlock lang="json" filename="nextpy-plugins.json" snippet={config_example} />
                </div>

                <div id="example-plugins" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Example plugins</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Because plugins only see file content, typical use cases are source transformations: stripping debug markup, injecting license headers, rewriting deprecated component names, or logging every file that passes through the pipeline via hooks. For request/response-style concerns, prefer NextPy middleware or API route handlers — the plugin pipeline operates on source files during compilation, not on live HTTP traffic.
                    </p>
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/howto/middleware-guide" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Middleware
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/howto/streaming" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Streaming SSR
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
                        <li><a href="#writing-a-plugin" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Writing a plugin</a></li>
                        <li><a href="#plugin-lifecycle" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Plugin lifecycle</a></li>
                        <li><a href="#registering-plugins" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Registering and loading plugins</a></li>
                        <li><a href="#cli-management" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Managing plugins via the CLI</a></li>
                        <li><a href="#builtin-plugins" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Built-in plugins</a></li>
                        <li><a href="#configuration" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Configuration</a></li>
                        <li><a href="#example-plugins" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Example plugins</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Plugin System - NextPy Docs"}}

default = PluginsGuide
