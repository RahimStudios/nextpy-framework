import json
from nextpy.psx import component, Link, register_component, interactive_component, useState, useEffect
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock, CodeTabs, FileTree

# Register components
register_component("EnhancedCodeBlock", EnhancedCodeBlock)
register_component("CodeTabs", CodeTabs)
register_component("FileTree", FileTree)

@component
def Installation():
    # --- DATA PREPARATION ---
    quickstart_tabs = json.dumps({
        "pip": "pip install nextpy-framework\\nnextpy create my-app\\ncd my-app\\nnextpy dev",
        "poetry": "poetry add nextpy-framework\\npoetry run nextpy create my-app\\ncd my-app\\npoetry run nextpy dev",
        "uv": "uv add nextpy-framework\\nuv run nextpy create my-app\\ncd my-app\\nuv run nextpy dev"
    })

    cli_tabs = json.dumps({
        "pip": "pip install nextpy-framework",
        "poetry": "poetry add nextpy-framework",
        "uv": "uv add nextpy-framework"
    })

    upgrade_tabs = json.dumps({
        "pip": "pip install --upgrade nextpy-framework",
        "poetry": "poetry update nextpy-framework",
        "uv": "uv lock --upgrade-package nextpy-framework"
    })

    pages_tree = json.dumps([
        {"name": "pages/", "type": "folder"},
        {"name": "  ├── layout.psx", "type": "file"},
        {"name": "  └── index.py", "type": "file"}
    ])

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-12 w-full max-w-6xl mx-auto">
                <DocsScrollSpy />

            
            <!-- MAIN CONTENT AREA -->
            <!-- Strict max-w-4xl for optimal line length (approx 75-85 chars) -->
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-16 pb-24 pt-6">

                <!-- Top Breadcrumb & Actions -->
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-6">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Getting Started</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Installation</span>
                    </div>
                    
                    <!-- Copy Page Button -->
                    <div class="relative flex items-center rounded-md border border-zinc-800 bg-zinc-950 overflow-hidden">
                        <button class="flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-zinc-300 hover:bg-zinc-900 transition-colors border-r border-zinc-800"
                            onclick="navigator.clipboard.writeText(document.querySelector('article').innerText);var l=this.querySelector('.cp-label');l.textContent='Copied';setTimeout(()=>l.textContent='Copy page',1500)">
                            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
                            <span class="cp-label">Copy page</span>
                        </button>
                        <button class="px-2 py-1.5 text-zinc-500 hover:bg-zinc-900 hover:text-zinc-300 transition-colors"
                            onclick="var m=this.parentElement.querySelector('.copy-menu');m.style.display=m.style.display==='none'?'block':'none'">
                            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/></svg>
                        </button>
                        <div class="copy-menu absolute right-0 top-full mt-1 w-44 rounded-lg border border-zinc-800 bg-zinc-900 shadow-xl z-50 py-1" style="display:none">
                            <button class="w-full text-left px-3 py-2 text-sm text-zinc-300 hover:bg-zinc-800" onclick="navigator.clipboard.writeText(document.querySelector('article').innerText);this.closest('.copy-menu').style.display='none'">Copy page</button>
                            <button class="w-full text-left px-3 py-2 text-sm text-zinc-300 hover:bg-zinc-800" onclick="navigator.clipboard.writeText(window.location.href);this.closest('.copy-menu').style.display='none'">Copy link</button>
                        </div>
                    </div>
                </div>

                <!-- Page Header -->
                <header id="header" class="mb-12">
                    <h1 class="text-4xl sm:text-5xl font-bold tracking-tight text-white mb-6">
                        Installation
                    </h1>
                    <p class="text-lg leading-relaxed text-zinc-400">
                        Create a new NextPy app and run it locally.
                    </p>
                </header>

                <!-- Section: Quick Start -->
                <div id="quick-start" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Quick start</h2>
                    
                    <ol class="list-decimal pl-6 space-y-3 text-base leading-7 text-zinc-400">
                        <li>Create a new NextPy app named <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">my-app</code></li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">cd my-app</code> and start the dev server.</li>
                        <li>Visit <code class="text-blue-400 font-mono text-sm">http://localhost:8000</code>.</li>
                    </ol>

                    <CodeTabs tabs='{quickstart_tabs}' default_tab="pip" />

                    <ul class="list-disc pl-6 space-y-3 text-base leading-7 text-zinc-400">
                        <li>
                            <code class="text-zinc-200 font-mono text-xs px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">--yes</code> skips prompts using saved preferences or defaults. The default setup enables Python 3.11+, Tailwind CSS, and the NextPy App Router, with standard import aliases.
                        </li>
                    </ul>
                </div>

                <!-- Section: System requirements -->
                <div id="system-requirements" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">System requirements</h2>
                    <p class="text-base leading-7 text-zinc-400">Before you begin, make sure your development environment meets the following requirements:</p>
                    <ul class="list-disc pl-6 space-y-3 text-base leading-7 text-zinc-400">
                        <li>Minimum Python version: <a href="#" class="text-blue-400 hover:underline">3.11</a></li>
                        <li>Operating systems: macOS, Windows (including WSL), and Linux.</li>
                    </ul>
                </div>

                <!-- Section: Supported browsers -->
                <div id="supported-browsers" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Supported browsers</h2>
                    <p class="text-base leading-7 text-zinc-400">NextPy supports modern browsers with zero configuration.</p>
                    <ul class="list-disc pl-6 space-y-3 text-base leading-7 text-zinc-400">
                        <li>Chrome 111+</li>
                        <li>Edge 111+</li>
                        <li>Firefox 111+</li>
                        <li>Safari 16.4+</li>
                    </ul>
                    <p class="text-base leading-7 text-zinc-400">Learn more about <a href="#" class="text-blue-400 hover:underline">browser support</a>, including how to configure polyfills and target specific browsers.</p>
                </div>

                <!-- Section: Create with the CLI -->
                <div id="create-with-cli" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Create with the CLI</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        The quickest way to create a new NextPy app is using <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy create</code>, which sets up everything automatically for you. To create a project, run:
                    </p>

                    <CodeTabs tabs='{cli_tabs}' default_tab="pip" />

                    <p class="text-base leading-7 text-zinc-400 mt-6">On installation, you'll see the following prompts:</p>

                    <EnhancedCodeBlock
                        lang="txt"
                        filename="Terminal"
                        snippet="What is your project named? my-app&#10;Would you like to use the recommended NextPy defaults?&#10;    Yes, use recommended defaults - Python, Tailwind CSS, No src/ directory, App Router&#10;    No, reuse previous settings&#10;    No, customize settings - Choose your own preferences"
                    />
                </div>

                <!-- Section: Manual installation -->
                <div id="manual-installation" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Manual installation</h2>
                    <p class="text-base leading-7 text-zinc-400">To manually create a new NextPy app, install the required packages:</p>

                    <CodeTabs tabs='{cli_tabs}' default_tab="pip" />

                    <div class="p-4 rounded-xl border border-zinc-800/60 bg-zinc-900/30 flex gap-3 text-sm text-zinc-400 mt-6 leading-6">
                        <svg class="w-5 h-5 text-zinc-500 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                        <div class="space-y-2">
                            <strong class="text-white font-medium">Good to know:</strong>
                            <ul class="list-disc pl-4 space-y-1">
                                <li>The App Router uses React canary releases built-in, which include all the stable React 19 changes.</li>
                                <li>The Pages Router uses the React version from your package.json.</li>
                            </ul>
                        </div>
                    </div>

                    <p class="text-base leading-7 text-zinc-400 mt-6">Then, add the following scripts to your <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy.config.py</code> file:</p>

                    <EnhancedCodeBlock
                        lang="python"
                        filename="nextpy.config.py"
                        snippet="from nextpy import Config&#10;&#10;config = Config(&#10;    app_name=&#34;my-app&#34;,&#10;    debug=True,&#10;    port=8000,&#10;    tailwind=True&#10;)"
                    />

                    <p class="text-base leading-7 text-zinc-400 mt-6">These scripts refer to the different stages of developing an application:</p>
                    <ul class="list-disc pl-6 space-y-3 text-base leading-7 text-zinc-400">
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy dev</code>: Starts the development server using Turbopack (default bundler).</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy build</code>: Builds the application for production.</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy start</code>: Starts the production server.</li>
                    </ul>
                </div>

                <!-- Section: Create the pages directory -->
                <div id="create-pages-directory" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h3 class="text-xl font-semibold text-white tracking-tight">Create the <code class="text-zinc-200 font-mono text-lg px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages</code> directory</h3>
                    <p class="text-base leading-7 text-zinc-400">NextPy uses file-system routing, which means the routes in your application are determined by how you structure your files.</p>
                    
                    <p class="text-base leading-7 text-zinc-400 mt-6">
                        Create an <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages</code> folder. Then, inside <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages</code>, create a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">layout.psx</code> file. This file is the <a href="#" class="text-blue-400 hover:underline">root layout</a>. It's required and must contain the HTML structure.
                    </p>

                    <EnhancedCodeBlock
                        lang="python"
                        filename="pages/layout.psx"
                        snippet="from nextpy.psx import component, psx&#10;&#10;@component&#10;def RootLayout(children):&#10;    return psx(&#34;&#34;&#34;&#10;        &lt;html lang=&#34;en&#34;&gt;&#10;            &lt;body&gt;{children}&lt;/body&gt;&#10;        &lt;/html&gt;&#10;    &#34;&#34;&#34;)"
                    />

                    <p class="text-base leading-7 text-zinc-400 mt-6">Create a home page <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/index.py</code> with some initial content:</p>

                    <EnhancedCodeBlock
                        lang="python"
                        filename="pages/index.py"
                        snippet="from nextpy.psx import component, psx&#10;&#10;@component&#10;def Page():&#10;    return psx(&#34;&lt;h1&gt;Hello, NextPy!&lt;/h1&gt;&#34;)"
                    />

                    <p class="text-base leading-7 text-zinc-400 mt-6">
                        Both <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">layout.psx</code> and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">index.py</code> will be rendered when the user visits the root of your application <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/</code>.
                    </p>

                    <!-- Visual Diagram -->
                    <div class="p-8 rounded-xl border border-zinc-800/60 bg-zinc-950 bg-[radial-gradient(#27272a_1px,transparent_1px)] [background-size:24px_24px] flex items-center justify-center gap-8 mt-6">
                        <div class="w-64">
                            <FileTree files='{pages_tree}' />
                        </div>
                        <svg class="w-8 h-8 text-zinc-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                        <div class="flex items-center gap-2 bg-zinc-800/50 border border-zinc-700/50 rounded-md px-4 py-2 font-mono text-sm text-zinc-300 shrink-0">
                            <svg class="w-4 h-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/></svg>
                            /
                        </div>
                    </div>
                </div>

                <!-- Section: Create the public folder -->
                <div id="create-public-folder" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h3 class="text-xl font-semibold text-white tracking-tight">Create the <code class="text-zinc-200 font-mono text-lg px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">public</code> folder <span class="text-zinc-500 font-normal text-base">(optional)</span></h3>
                    <p class="text-base leading-7 text-zinc-400">
                        Create a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">public</code> folder at the root of your project to store static assets such as images, fonts, etc. Files inside <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">public</code> can then be referenced by your code starting from the base URL <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/</code>.
                    </p>
                    
                    <p class="text-base leading-7 text-zinc-400 mt-6">
                        You can then reference these assets using the root path <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/</code>. For example, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">public/profile.png</code> can be referenced as <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/profile.png</code>:
                    </p>

                    <EnhancedCodeBlock
                        lang="python"
                        filename="pages/index.py"
                        snippet="from nextpy.psx import component, psx&#10;&#10;@component&#10;def Page():&#10;    return psx(&#34;&#34;&#34;&#10;        &lt;img src=&#34;/profile.png&#34; alt=&#34;Profile&#34; width=&#34;100&#34; height=&#34;100&#34; /&gt;&#10;    &#34;&#34;&#34;)"
                    />
                </div>

                <!-- Section: Run the development server -->
                <div id="run-dev-server" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Run the development server</h2>
                    <ol class="list-decimal pl-6 space-y-3 text-base leading-7 text-zinc-400">
                        <li>Run <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy dev</code> to start the development server.</li>
                        <li>Visit <code class="text-blue-400 font-mono text-sm">http://localhost:8000</code> to view your application.</li>
                        <li>Edit the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/index.py</code> file and save it to see the updated result in your browser.</li>
                    </ol>
                </div>

                <!-- Section: Set up Python Type Checking -->
                <div id="setup-types" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Set up Python Type Checking</h2>
                    <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-md border border-zinc-800 bg-zinc-900/50 text-sm text-zinc-300">
                        <span class="font-semibold text-white">Minimum mypy version:</span> <span class="font-mono text-xs bg-zinc-800 px-1.5 py-0.5 rounded border border-zinc-700">v1.8.0</span>
                    </div>
                    <p class="text-base leading-7 text-zinc-400 mt-4">
                        NextPy comes with built-in support for Python type hints. To add strict type checking to your project, install <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">mypy</code> and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">ruff</code>. NextPy will automatically respect the type checking rules during the build process.
                    </p>
                </div>

                <!-- Section: Set up your editor -->
                <div id="setup-editor" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Set up your editor</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        The App Router names files by convention, like <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">index.py</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">layout.psx</code>, and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">api.py</code>, so your editor quickly fills with same-named tabs. Label each tab with its enclosing folders, like <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">blog/&#91;id&#93;</code>, so you can tell them apart.
                    </p>
                    
                    <p class="text-base leading-7 text-zinc-400 mt-6">
                        In VS Code 1.88+ or Cursor, add <a href="#" class="text-blue-400 hover:underline">custom editor labels</a> to <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">.vscode/settings.json</code>. Labeling two folders deep keeps dynamic routes like <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">blog/&#91;id&#93;/index.py</code> from all collapsing to the same <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">&#91;id&#93;</code> label:
                    </p>

                    <EnhancedCodeBlock
                        lang="json"
                        filename=".vscode/settings.json"
                        snippet="&#123;&#10;  &#34;workbench.editor.customLabels.patterns&#34;: &#123;&#10;    &#34;**/pages/**/index.py&#34;: &#34;${dirname(1)}/${dirname} - index.py&#34;,&#10;    &#34;**/pages/**/layout.psx&#34;: &#34;${dirname(1)}/${dirname} - layout.psx&#34;,&#10;    &#34;**/pages/**/loading.py&#34;: &#34;${dirname(1)}/${dirname} - loading.py&#34;,&#10;    &#34;**/pages/**/error.py&#34;: &#34;${dirname(1)}/${dirname} - error.py&#34;,&#10;    &#34;**/pages/**/api.py&#34;: &#34;${dirname(1)}/${dirname} - api.py&#34;&#10;  &#125;&#10;&#125;"
                    />

                    <div class="p-4 rounded-xl border border-zinc-800/60 bg-zinc-900/30 flex gap-3 text-sm text-zinc-400 mt-6 leading-6">
                        <svg class="w-5 h-5 text-zinc-500 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                        <div>
                            <strong class="text-white font-medium">Good to know:</strong> JetBrains IDEs (WebStorm, IntelliJ) show the folder for same-named files automatically, so no setup is needed.
                        </div>
                    </div>
                </div>

                <!-- Section: Set up linting -->
                <div id="setup-linting" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Set up linting</h2>
                    <p class="text-base leading-7 text-zinc-400">NextPy supports linting with <strong>Ruff</strong> (fast Python linter + formatter). Choose a linter and run it directly via <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">ruff.toml</code> scripts.</p>
                    
                    <ul class="list-disc pl-6 space-y-3 text-base leading-7 text-zinc-400">
                        <li>Use <strong>Ruff</strong> (comprehensive rules):</li>
                    </ul>

                    <EnhancedCodeBlock
                        lang="toml"
                        filename="ruff.toml"
                        snippet="[lint]&#10;select = [&#34;E&#34;, &#34;F&#34;, &#34;I&#34;]&#10;&#10;[format]&#10;quote-style = &#34;double&#34;"
                    />

                    <div class="p-4 rounded-xl border border-zinc-800/60 bg-zinc-900/30 flex gap-3 text-sm text-zinc-400 mt-6 leading-6">
                        <svg class="w-5 h-5 text-zinc-500 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                        <div>
                            <strong class="text-white font-medium">Good to know:</strong> Starting with NextPy 1.0, <code class="text-zinc-200 font-mono text-xs px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy build</code> no longer runs the linter automatically. Instead, you can run your linter through NPM scripts.
                        </div>
                    </div>
                </div>

                <!-- Section: Set up Absolute Imports -->
                <div id="setup-imports" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Set up Absolute Imports and Module Path Aliases</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        NextPy has in-built support for absolute imports via your <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy.config.py</code> file.
                    </p>
                    
                    <p class="text-base leading-7 text-zinc-400 mt-6">These options allow you to alias project directories to absolute paths, making it easier and cleaner to import modules. For example:</p>

                    <EnhancedCodeBlock
                        lang="python"
                        filename="Example"
                        snippet="# Before&#10;from ...components.button import Button&#10;&#10;# After&#10;from components.button import Button"
                    />

                    <p class="text-base leading-7 text-zinc-400 mt-6">To configure absolute imports, add the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">baseUrl</code> configuration option to your <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy.config.py</code> file. For example:</p>

                    <EnhancedCodeBlock
                        lang="python"
                        filename="nextpy.config.py"
                        snippet="from nextpy import Config&#10;&#10;config = Config(&#10;    app_name=&#34;my-app&#34;,&#10;    base_dir=&#34;src/&#34;&#10;)&#10;&#10;# Each of the paths are relative to the base_dir location."
                    />
                </div>

                <!-- Section: Upgrade your NextPy app -->
                <div id="upgrade" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Upgrade your NextPy app</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Keep your NextPy version up to date. Each release ships security patches, bug fixes, and performance optimizations alongside new features, and staying current keeps every individual upgrade small. Run the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">upgrade</code> command:
                    </p>

                    <CodeTabs tabs='{upgrade_tabs}' default_tab="pip" />

                    <p class="text-base leading-7 text-zinc-400 mt-6">
                        Upgrading also updates the documentation bundled inside the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy</code> package at <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">node_modules/nextpy/dist/docs/</code>. New features arrive with their docs, and existing pages pick up new guidance and pitfalls discovered along the way.
                    </p>

                    <p class="text-base leading-7 text-zinc-400 mt-6">
                        See <a href="#" class="text-blue-400 hover:underline">Upgrading</a> for version guides and manual upgrade steps, or the <a href="#" class="text-blue-400 hover:underline">preview docs</a> to explore features before they ship in a stable version.
                    </p>
                    
                    <div class="text-sm text-zinc-500 mt-8">
                        Last updated October 2, 2026
                    </div>
                </div>

                <!-- Footer Pagination -->
                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Getting Started
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/getting-started/project-structure" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Project Structure
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                            </span>
                        </Link>
                    </div>
                </footer>
            </article>

            <!-- RIGHT SIDEBAR (ON THIS PAGE) -->
            <aside class="hidden xl:block w-64 shrink-0 sticky top-24 pt-6 pb-24 h-[calc(100vh-6rem)] overflow-y-auto scrollbar-none">
                <div class="text-sm">
                    <h4 class="font-semibold text-white mb-4 tracking-wide">On this page</h4>
                    
                    <ul class="space-y-3 font-medium text-zinc-400 border-l border-zinc-800">
                        <li>
                            <a href="#quick-start" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Quick start</a>
                        </li>
                        <li>
                            <a href="#system-requirements" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">System requirements</a>
                        </li>
                        <li>
                            <a href="#supported-browsers" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Supported browsers</a>
                        </li>
                        <li>
                            <a href="#create-with-cli" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Create with the CLI</a>
                        </li>
                        <li>
                            <a href="#manual-installation" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Manual installation</a>
                        </li>
                        
                        <!-- Sub items -->
                        <li>
                            <a href="#create-pages-directory" class="block pl-8 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors text-[13px]">Create the pages directory</a>
                        </li>
                        <li>
                            <a href="#create-public-folder" class="block pl-8 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors text-[13px]">Create the public folder (optional)</a>
                        </li>
                        
                        <li>
                            <a href="#run-dev-server" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Run the development server</a>
                        </li>
                        <li>
                            <a href="#setup-types" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Set up Python Type Checking</a>
                        </li>
                        <li>
                            <a href="#setup-editor" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Set up your editor</a>
                        </li>
                        <li>
                            <a href="#setup-linting" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Set up linting</a>
                        </li>
                        <li>
                            <a href="#setup-imports" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors leading-snug">Set up Absolute Imports and Module Path Aliases</a>
                        </li>
                        <li>
                            <a href="#upgrade" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Upgrade your NextPy app</a>
                        </li>
                    </ul>
                </div>

                <!-- Feedback Links -->
                <div class="pt-8 mt-8 border-t border-zinc-800/50 text-sm font-medium space-y-4">
                    <a href="#" class="flex items-center gap-2 text-zinc-400 hover:text-white transition-colors">
                        <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"/></svg>
                        Give feedback
                    </a>
                    <a href="#" class="flex items-center gap-2 text-zinc-400 hover:text-white transition-colors">
                        <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
                        Edit this page on GitHub
                    </a>
                </div>
            </aside>

        </div>
    )




def getServerSideProps(context):
    return {
        "props": {
            "title": "Installation",
        }
    }

default = Installation

@interactive_component
def DocsScrollSpy():
    [scroll_progress, set_scroll_progress] = useState(0)

    def SetupScroll():
        def OnScroll():
            doc_height = document.documentElement.scrollHeight - window.innerHeight
            if doc_height > 0:
                set_scroll_progress((window.scrollY / doc_height) * 100)

            current = ""
            sections = document.querySelectorAll("article div[id], article header[id], section[id]")
            for sec in sections:
                rect = sec.getBoundingClientRect()
                if rect.top <= 160:
                    current = sec.id
                in_view = rect.top < window.innerHeight * 0.92 and rect.bottom > 0
                if in_view:
                    sec.setAttribute("data-docs-revealed", "")
                else:
                    sec.removeAttribute("data-docs-revealed")

            links = document.querySelectorAll("aside a[href^='#'], nav a[href^='#']")
            for a in links:
                if a.getAttribute("href") == "#" + current:
                    a.setAttribute("data-docs-toc-active", "")
                else:
                    a.removeAttribute("data-docs-toc-active")

            path = window.location.pathname
            nav_links = document.querySelectorAll("aside a[href^='/']")
            for a in nav_links:
                if a.getAttribute("href") == path:
                    a.setAttribute("data-docs-nav-active", "")
                    parent = a.closest("details")
                    if parent:
                        parent.setAttribute("open", "")
                else:
                    a.removeAttribute("data-docs-nav-active")

        sections = document.querySelectorAll("article div[id], article header[id], section[id]")
        for sec in sections:
            sec.setAttribute("data-docs-reveal", "")

        window.addEventListener("scroll", OnScroll)
        document.addEventListener("nextpy:navigate", OnScroll)
        OnScroll()
        return lambda: window.removeEventListener("scroll", OnScroll)

    useEffect(SetupScroll, [])

    progress_style = f"width: {scroll_progress}%"

    return (
        <div class="fixed top-0 left-0 right-0 z-[70] h-[3px] pointer-events-none">
            <div style={progress_style} class="h-full bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 transition-[width] duration-100"></div>
        </div>
    )

register_component("DocsScrollSpy", DocsScrollSpy)
