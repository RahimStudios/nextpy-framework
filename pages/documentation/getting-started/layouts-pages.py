import json
from nextpy.psx import component, Link, register_component, interactive_component, useState, useEffect
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock, CodeTabs, FileTree

# Register components
register_component("EnhancedCodeBlock", EnhancedCodeBlock)
register_component("CodeTabs", CodeTabs)
register_component("FileTree", FileTree)

@component
def LayoutsAndPages():
    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-12 w-full max-w-6xl mx-auto">
                <DocsScrollSpy />

            
            <!-- MAIN CONTENT AREA -->
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-16 pb-24 pt-6">

                <!-- Top Breadcrumb & Actions -->
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-6">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>Getting Started</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Layouts and Pages</span>
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
                        Layouts and Pages
                    </h1>
                    <p class="text-lg leading-relaxed text-zinc-400">
                        NextPy uses file-system based routing, meaning you can use folders and files to define routes. This page will guide you through how to create layouts and pages, and link between them.
                    </p>
                </header>

                <!-- Section: Creating a page -->
                <div id="creating-a-page" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Creating a page</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        A page is UI that is rendered on a specific route. To create a page, add an <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">index.py</code> file inside the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages</code> directory and default export a React component. For example, to create an index page <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/</code>:
                    </p>

                    <!-- Visual Diagram -->
                    <div class="p-8 rounded-xl border border-zinc-800/60 bg-zinc-950 bg-[radial-gradient(#27272a_1px,transparent_1px)] [background-size:24px_24px] flex items-center justify-center gap-8 mt-6">
                        <div class="w-56 bg-zinc-900 border border-zinc-800 rounded-lg p-3 shadow-xl">
                            <div class="flex items-center gap-2 text-sm font-mono text-zinc-300 mb-2"><svg class="w-4 h-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>pages</div>
                            <div class="space-y-1 text-sm font-mono text-zinc-400 pl-4">
                                <div class="flex items-center gap-2 text-blue-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                            </div>
                        </div>
                        <svg class="w-8 h-8 text-zinc-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                        <div class="flex items-center gap-2 bg-zinc-800/50 border border-zinc-700/50 rounded-md px-4 py-2 font-mono text-sm text-zinc-300 shrink-0">
                            <svg class="w-4 h-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/></svg>
                            /
                        </div>
                    </div>

                    <EnhancedCodeBlock
                        lang="python"
                        filename="pages/index.py"
                        snippet="from nextpy.psx import component, psx&#10;&#10;@component&#10;def Page():&#10;    return psx(&#34;&lt;h1&gt;Hello NextPy!&lt;/h1&gt;&#34;)"
                    />
                </div>

                <!-- Section: Creating a layout -->
                <div id="creating-a-layout" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Creating a layout</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        A layout is UI that is <strong>shared</strong> between multiple pages. On navigation, layouts preserve state, remain interactive, and do not rerender.
                    </p>
                    <p class="text-base leading-7 text-zinc-400 mt-4">
                        You can define a layout by creating a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">layout.psx</code> file. The component should accept a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">children</code> prop which can be a page or another layout.
                    </p>
                    <p class="text-base leading-7 text-zinc-400 mt-4">
                        For example, to create a layout that accepts your index page as child, add a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">layout.psx</code> file inside the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages</code> directory:
                    </p>

                    <!-- Visual Diagram -->
                    <div class="p-8 rounded-xl border border-zinc-800/60 bg-zinc-950 bg-[radial-gradient(#27272a_1px,transparent_1px)] [background-size:24px_24px] flex items-center justify-center gap-8 mt-6">
                        <div class="w-56 bg-zinc-900 border border-zinc-800 rounded-lg p-3 shadow-xl">
                            <div class="flex items-center gap-2 text-sm font-mono text-zinc-300 mb-2"><svg class="w-4 h-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>pages</div>
                            <div class="space-y-1 text-sm font-mono text-zinc-400 pl-4">
                                <div class="flex items-center gap-2 text-blue-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>layout.psx</div>
                                <div class="flex items-center gap-2"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                            </div>
                        </div>
                        <svg class="w-8 h-8 text-zinc-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                        <div class="flex items-center gap-2 bg-zinc-800/50 border border-zinc-700/50 rounded-md px-4 py-2 font-mono text-sm text-zinc-300 shrink-0">
                            <svg class="w-4 h-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/></svg>
                            /
                        </div>
                    </div>

                    <EnhancedCodeBlock
                        lang="python"
                        filename="pages/layout.psx"
                        snippet="from nextpy.psx import component, psx&#10;&#10;@component&#10;def DashboardLayout(children):&#10;    return psx(&#34;&#34;&#34;&#10;        &lt;html lang=&#34;en&#34;&gt;&#10;            &lt;body&gt;&#10;                &lt;!-- Layout UI --&gt;&#10;                &lt;!-- Place children where you want to render a page or nested layout --&gt;&#10;                &lt;main&gt;{children}&lt;/main&gt;&#10;            &lt;/body&gt;&#10;        &lt;/html&gt;&#10;    &#34;&#34;&#34;)"
                    />

                    <p class="text-base leading-7 text-zinc-400 mt-4">
                        The layout above is called a <strong>root layout</strong> because it's defined at the root of the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages</code> directory. The root layout is required and must contain <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">html</code> and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">body</code> tags.
                    </p>
                </div>

                <!-- Section: Creating a nested route -->
                <div id="creating-a-nested-route" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Creating a nested route</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        A nested route is a route composed of multiple URL segments. For example, the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/blog/&#91;slug&#93;</code> route is composed of three segments:
                    </p>
                    <ul class="list-disc pl-6 space-y-3 text-base leading-7 text-zinc-400 mt-2">
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/</code> (Root Segment)</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">blog</code> (Segment)</li>
                        <li><code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">&#91;slug&#93;</code> (Leaf Segment)</li>
                    </ul>
                    
                    <p class="text-base leading-7 text-zinc-400 mt-4">
                        In NextPy:
                    </p>
                    <ul class="list-disc pl-6 space-y-3 text-base leading-7 text-zinc-400">
                        <li><strong>Folders</strong> are used to define the route segments that map to URL segments.</li>
                        <li><strong>Files</strong> like <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">index.py</code> and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">layout.psx</code> are used to create UI that is shown for a segment.</li>
                    </ul>
                    
                    <p class="text-base leading-7 text-zinc-400 mt-4">
                        To create nested routes, you can nest folders inside each other. For example, to add a route for <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/blog</code>, create a folder called <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">blog</code> in the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages</code> directory. Then, to make <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/blog</code> publicly accessible, add a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">index.py</code> file:
                    </p>

                    <!-- Visual Diagram -->
                    <div class="p-8 rounded-xl border border-zinc-800/60 bg-zinc-950 bg-[radial-gradient(#27272a_1px,transparent_1px)] [background-size:24px_24px] flex items-center justify-center gap-8 mt-6">
                        <div class="w-56 bg-zinc-900 border border-zinc-800 rounded-lg p-3 shadow-xl">
                            <div class="flex items-center gap-2 text-sm font-mono text-zinc-300 mb-2"><svg class="w-4 h-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>pages</div>
                            <div class="space-y-1 text-sm font-mono text-zinc-400 pl-4">
                                <div class="flex items-center gap-2"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>layout.psx</div>
                                <div class="flex items-center gap-2"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                                <div class="flex items-center gap-2 text-blue-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>blog</div>
                                <div class="flex items-center gap-2 pl-4 text-blue-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                            </div>
                        </div>
                        <svg class="w-8 h-8 text-zinc-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                        <div class="space-y-2 shrink-0">
                            <div class="flex items-center gap-3">
                                <div class="w-40 bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-zinc-400">/</div>
                            </div>
                            <div class="flex items-center gap-3">
                                <div class="w-40 bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-zinc-400">/blog</div>
                            </div>
                        </div>
                    </div>

                    <EnhancedCodeBlock
                        lang="python"
                        filename="pages/blog/index.py"
                        snippet="from nextpy.psx import component, psx&#10;&#10;# Dummy imports&#10;from lib.posts import get_posts&#10;from components.post import Post&#10;&#10;@component&#10;def Page():&#10;    posts = get_posts()&#10;&#10;    return psx(f&#34;&#34;&#34;&#10;        &lt;ul&gt;&#10;            {{''.join([f'&lt;li&gt;&lt;Post id=&#34;{{p.id}}&#34; post=&#34;{{p.title}}&#34; /&gt;&lt;/li&gt;' for p in posts])}}&#10;        &lt;/ul&gt;&#10;    &#34;&#34;&#34;)"
                    />

                    <p class="text-base leading-7 text-zinc-400 mt-4">
                        You can continue nesting folders to create nested routes. For example, to create a route for a specific blog post, create a new <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">&#91;slug&#93;</code> folder inside <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">blog</code> and add a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">index.py</code> file:
                    </p>

                    <!-- Visual Diagram 2 -->
                    <div class="p-8 rounded-xl border border-zinc-800/60 bg-zinc-950 bg-[radial-gradient(#27272a_1px,transparent_1px)] [background-size:24px_24px] flex items-center justify-center gap-8 mt-6">
                        <div class="w-56 bg-zinc-900 border border-zinc-800 rounded-lg p-3 shadow-xl">
                            <div class="flex items-center gap-2 text-sm font-mono text-zinc-300 mb-2"><svg class="w-4 h-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>pages</div>
                            <div class="space-y-1 text-sm font-mono text-zinc-400 pl-4">
                                <div class="flex items-center gap-2"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>layout.psx</div>
                                <div class="flex items-center gap-2"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                                <div class="flex items-center gap-2"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>blog</div>
                                <div class="flex items-center gap-2 pl-4"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                                <div class="flex items-center gap-2 pl-4 text-blue-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>&#91;slug&#93;</div>
                                <div class="flex items-center gap-2 pl-8 text-blue-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                            </div>
                        </div>
                        <svg class="w-8 h-8 text-zinc-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                        <div class="space-y-2 shrink-0">
                            <div class="flex items-center gap-3">
                                <div class="w-40 bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-zinc-400">/</div>
                            </div>
                            <div class="flex items-center gap-3">
                                <div class="w-40 bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-zinc-400">/blog</div>
                            </div>
                            <div class="flex items-center gap-3">
                                <div class="w-40 bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-zinc-400">/blog/&#91;slug&#93;</div>
                            </div>
                        </div>
                    </div>

                    <EnhancedCodeBlock
                        lang="python"
                        filename="pages/blog/[slug]/index.py"
                        snippet="from nextpy.psx import component, psx&#10;&#10;@component&#10;def Page(params):&#10;    return psx(&#34;&lt;h1&gt;Hello, Blog Post Page!&lt;/h1&gt;&#34;)"
                    />

                    <p class="text-base leading-7 text-zinc-400 mt-4">
                        Wrapping a folder name in square brackets <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">&#91;slug&#93;</code> creates a dynamic route segment which is used to generate multiple pages from data. e.g. blog posts, product pages, etc.
                    </p>
                </div>

                <!-- Section: Nesting layouts -->
                <div id="nesting-layouts" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Nesting layouts</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        By default, layouts in the folder hierarchy are also nested, which means they wrap child layouts via their <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">children</code> prop. You can nest layouts by adding <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">layout.psx</code> inside specific route segments folders.
                    </p>
                    <p class="text-base leading-7 text-zinc-400 mt-4">
                        For example, to create a layout for the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">/blog</code> route, add a new <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">layout.psx</code> file inside the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">blog</code> folder.
                    </p>

                    <!-- Visual Diagram -->
                    <div class="p-8 rounded-xl border border-zinc-800/60 bg-zinc-950 bg-[radial-gradient(#27272a_1px,transparent_1px)] [background-size:24px_24px] flex items-center justify-center gap-8 mt-6">
                        <div class="w-56 bg-zinc-900 border border-zinc-800 rounded-lg p-3 shadow-xl">
                            <div class="flex items-center gap-2 text-sm font-mono text-zinc-300 mb-2"><svg class="w-4 h-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>pages</div>
                            <div class="space-y-1 text-sm font-mono text-zinc-400 pl-4">
                                <div class="flex items-center gap-2"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>layout.psx</div>
                                <div class="flex items-center gap-2"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                                <div class="flex items-center gap-2"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>blog</div>
                                <div class="flex items-center gap-2 pl-4 text-blue-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>layout.psx</div>
                                <div class="flex items-center gap-2 pl-4"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                                <div class="flex items-center gap-2 pl-4 text-blue-400"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>&#91;slug&#93;</div>
                                <div class="flex items-center gap-2 pl-8"><svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>index.py</div>
                            </div>
                        </div>
                        <svg class="w-8 h-8 text-zinc-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                        <div class="space-y-2 shrink-0">
                            <div class="flex items-center gap-3">
                                <div class="w-40 bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-zinc-400">/</div>
                            </div>
                            <div class="flex items-center gap-3">
                                <div class="w-40 bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-zinc-400">/blog</div>
                            </div>
                            <div class="flex items-center gap-3">
                                <div class="w-40 bg-zinc-800/50 border border-zinc-700/50 rounded px-3 py-1.5 text-sm font-mono text-zinc-400">/blog/&#91;slug&#93;</div>
                            </div>
                        </div>
                    </div>

                    <EnhancedCodeBlock
                        lang="python"
                        filename="pages/blog/layout.psx"
                        snippet="from nextpy.psx import component, psx&#10;&#10;@component&#10;def BlogLayout(children):&#10;    return psx(f&#34;&lt;section&gt;{children}&lt;/section&gt;&#34;)"
                    />

                    <p class="text-base leading-7 text-zinc-400 mt-4">
                        If you were to combine the two layouts above, the root layout (<code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/layout.psx</code> would wrap the blog layout (<code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/blog/layout.psx</code>, which would wrap the blog (<code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/blog/index.py</code> and blog post page (<code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/blog/&#91;slug&#93;/index.py</code>.
                    </p>
                </div>

                <!-- Section: Creating a dynamic segment -->
                <div id="creating-a-dynamic-segment" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Creating a dynamic segment</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        Dynamic segments allow you to create routes that are generated from data. For example, instead of manually creating a route for each individual blog post, you can create a dynamic segment to generate the routes based on blog post data.
                    </p>
                    <p class="text-base leading-7 text-zinc-400 mt-4">
                        To create a dynamic segment, wrap the segment (folder) name in square brackets: <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">&#91;segmentName&#93;</code>. For example, in the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pages/blog/&#91;slug&#93;/index.py</code> route, the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">&#91;slug&#93;</code> is the dynamic segment.
                    </p>

                    <EnhancedCodeBlock
                        lang="python"
                        filename="pages/blog/[slug]/index.py"
                        snippet="from nextpy.psx import component, psx&#10;&#10;@component&#10;def BlogPostPage(params):&#10;    slug = params.get(&#34;slug&#34;)&#10;    post = get_post(slug)&#10;&#10;    return psx(f&#34;&#34;&#34;&#10;        &lt;div&gt;&#10;            &lt;h1&gt;{post.title}&lt;/h1&gt;&#10;            &lt;p&gt;{post.content}&lt;/p&gt;&#10;        &lt;/div&gt;&#10;    &#34;&#34;&#34;)"
                    />

                    <p class="text-base leading-7 text-zinc-400 mt-4">
                        Learn more about <a href="#" class="text-blue-400 hover:underline">Dynamic Segments</a> and the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">params</code> props.
                    </p>
                    <p class="text-base leading-7 text-zinc-400 mt-2">
                        Nested <a href="#" class="text-blue-400 hover:underline">layouts within Dynamic Segments</a> can also access the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">params</code> props.
                    </p>
                </div>

                <!-- Section: Rendering with search params -->
                <div id="rendering-with-search-params" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Rendering with search params</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        In a Server Component page, you can access search parameters using the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">searchParams</code> prop:
                    </p>

                    <EnhancedCodeBlock
                        lang="python"
                        filename="pages/index.py"
                        snippet="from nextpy.psx import component, psx&#10;&#10;@component&#10;def Page(searchParams):&#10;    filters = searchParams.get(&#34;filters&#34;)&#10;    return psx(&#34;&lt;div&gt;Filtered Results&lt;/div&gt;&#34;)"
                    />

                    <p class="text-base leading-7 text-zinc-400 mt-4">
                        Using <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">searchParams</code> opts your page into <a href="#" class="text-blue-400 hover:underline">dynamic rendering</a> because it requires an incoming request to read the search parameters from.
                    </p>
                    <p class="text-base leading-7 text-zinc-400 mt-4">
                        Client Components can read search params using the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useSearchParams</code> hook.
                    </p>
                    <p class="text-base leading-7 text-zinc-400 mt-2">
                        Learn more about <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useSearchParams</code> in <a href="#" class="text-blue-400 hover:underline">prerendered</a> and <a href="#" class="text-blue-400 hover:underline">dynamically rendered</a> routes.
                    </p>
                </div>

                <!-- Section: What to use and when -->
                <div id="what-to-use-and-when" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">What to use and when</h2>
                    <ul class="list-disc pl-6 space-y-3 text-base leading-7 text-zinc-400">
                        <li>Use the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">searchParams</code> prop when you need search parameters to load data for the page pagination, filtering from a database.</li>
                        <li>Use <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useSearchParams</code> when search parameters are used only on the client filtering a list already loaded via props.</li>
                        <li>As a small optimization, you can use <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">new URLSearchParams(window.location.search)</code> in callbacks or event handlers to read search params without triggering re-renders.</li>
                    </ul>
                </div>

                <!-- Section: Linking between pages -->
                <div id="linking-between-pages" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Linking between pages</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        You can use the <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">&lt;Link&gt;</code> component to navigate between routes. <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">&lt;Link&gt;</code> is a built-in NextPy component that extends the HTML <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">&lt;a&gt;</code> tag to provide <a href="#" class="text-blue-400 hover:underline">prefetching</a> and <a href="#" class="text-blue-400 hover:underline">client-side navigation</a>.
                    </p>
                    <p class="text-base leading-7 text-zinc-400 mt-4">
                        For example, to generate a list of blog posts, import <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">&lt;Link&gt;</code> from <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy.psx</code> and pass a <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">href</code> prop to the component:
                    </p>

                    <EnhancedCodeBlock
                        lang="python"
                        filename="pages/api/post.py"
                        snippet="from nextpy.psx import component, psx, Link&#10;from lib.posts import get_posts&#10;&#10;@component&#10;def Posts():&#10;    posts = get_posts()&#10;&#10;    return psx(f&#34;&#34;&#34;&#10;        &lt;ul&gt;&#10;            {{''.join([f'''&#10;                &lt;li key=&#34;{{p.slug}}&#34;&gt;&#10;                    &lt;Link href=&#34;/blog/{{p.slug}}&#34;&gt;{{p.title}}&lt;/Link&gt;&#10;                &lt;/li&gt;&#10;            ''' for p in posts])}}&#10;        &lt;/ul&gt;&#10;    &#34;&#34;&#34;)"
                    />

                    <div class="p-4 rounded-xl border border-zinc-800/60 bg-zinc-900/30 flex gap-3 text-sm text-zinc-400 mt-6 leading-6">
                        <svg class="w-5 h-5 text-zinc-500 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                        <div class="space-y-2">
                            <strong class="text-white font-medium">Good to know:</strong>
                            <ul class="list-disc pl-4 space-y-1">
                                <li><code class="text-zinc-200 font-mono text-xs px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">&lt;Link&gt;</code> is the primary way to navigate between routes in NextPy. You can also use the <code class="text-zinc-200 font-mono text-xs px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">useRouter</code> hook for more advanced navigation.</li>
                            </ul>
                        </div>
                    </div>
                </div>

                <!-- Section: Route Props Helpers -->
                <div id="route-props-helpers" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Route Props Helpers</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        NextPy exposes utility types that infer <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">params</code> and named slots from your route structure:
                    </p>
                    <ul class="list-disc pl-6 space-y-3 text-base leading-7 text-zinc-400">
                        <li><strong>PageProps:</strong> Props for <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">index.py</code> components, including <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">params</code> and <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">searchParams</code>.</li>
                        <li><strong>LayoutProps:</strong> Props for <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">layout.psx</code> components, including <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">children</code> and any named slots folders like <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">@analytics</code></li>
                    </ul>
                    <p class="text-base leading-7 text-zinc-400 mt-4">
                        These are globally available helpers, generated when running either <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy dev</code>, <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy build</code> or <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy typegen</code>.
                    </p>

                    <EnhancedCodeBlock
                        lang="python"
                        filename="pages/blog/[slug]/index.py"
                        snippet="from nextpy.psx import component, psx&#10;&#10;@component&#10;def Page(props):&#10;    slug = props.params.get(&#34;slug&#34;)&#10;    return psx(f&#34;&lt;h1&gt;Blog post: {slug}&lt;/h1&gt;&#34;)"
                    />

                    <EnhancedCodeBlock
                        lang="python"
                        filename="pages/dashboard/layout.psx"
                        snippet="from nextpy.psx import component, psx&#10;&#10;@component&#10;def Layout(props):&#10;    return psx(f&#34;&#34;&#34;&#10;        &lt;section&gt;&#10;            {props.children}&#10;            &lt;!-- If you have app/dashboard/@analytics, it appears as a typed slot: --&gt;&#10;            &lt;!-- {props.analytics} --&gt;&#10;        &lt;/section&gt;&#10;    &#34;&#34;&#34;)"
                    />
                </div>

                <!-- Section: API Reference -->
                <div id="api-reference" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">API Reference</h2>
                    <p class="text-base leading-7 text-zinc-400">
                        For a complete reference of NextPy routing APIs, see the <a href="#" class="text-blue-400 hover:underline">Routing API Reference</a>.
                    </p>
                </div>

                <div class="text-sm text-zinc-500 mt-8">
                    Last updated October 2, 2026
                </div>

                <!-- Footer Pagination -->
                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/getting-started/project-structure" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Project Structure
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/getting-started/linking-and-navigating" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Linking and Navigating
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                            </span>
                        </Link>
                    </div>
                </footer>
            </article>

            <!-- RIGHT SIDEBAR (ON THIS PAGE) -->
            <aside class="hidden xl:block w-64 shrink-0 sticky top-24 pt-6 pb-24 h-[calc(100vh-6rem)] overflow-y-auto">
                <div class="text-sm">
                    <h4 class="font-semibold text-white mb-4 tracking-wide">On this page</h4>
                    
                    <ul class="space-y-3 font-medium text-zinc-400 border-l border-zinc-800/50">
                        <li>
                            <a href="#creating-a-page" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Creating a page</a>
                        </li>
                        <li>
                            <a href="#creating-a-layout" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Creating a layout</a>
                        </li>
                        <li>
                            <a href="#creating-a-nested-route" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Creating a nested route</a>
                        </li>
                        <li>
                            <a href="#nesting-layouts" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Nesting layouts</a>
                        </li>
                        <li>
                            <a href="#creating-a-dynamic-segment" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Creating a dynamic segment</a>
                        </li>
                        <li>
                            <a href="#rendering-with-search-params" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Rendering with search params</a>
                        </li>
                        <li>
                            <a href="#what-to-use-and-when" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">What to use and when</a>
                        </li>
                        <li>
                            <a href="#linking-between-pages" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Linking between pages</a>
                        </li>
                        <li>
                            <a href="#route-props-helpers" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Route Props Helpers</a>
                        </li>
                        <li>
                            <a href="#api-reference" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">API Reference</a>
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
            "title": "Layouts and Pages",
        }
    }

default = LayoutsAndPages

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
