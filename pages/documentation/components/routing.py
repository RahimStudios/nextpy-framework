from nextpy.psx import psx



def RoutingGuide():
    return psx("""
        <section id="file-routing" class="space-y-6">
            <div class="pb-3 border-b border-gray-800">
                <h2 class="text-2xl font-bold text-gray-100">File-based Routing</h2>
                <p class="mt-2 text-gray-400">
                    NextPy maps files in the pages folder directly to URLs, so your app structure stays simple and intuitive.
                </p>
            </div>

            <div class="grid gap-6 md:grid-cols-2">
                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Basic routes</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">pages/index.py      -> /
pages/about.py     -> /about
pages/contact.py   -> /contact</pre>
                </div>

                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Dynamic and nested routes</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">pages/blog/[slug].py   -> /blog/hello
pages/app/dashboard/settings/index.py -> /app/dashboard/settings</pre>
                </div>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-gray-100">Layout support</h3>
                <p class="mt-2 text-sm text-gray-400">
                    Place layout files inside folders to share headers, sidebars, and navigation across related pages.
                </p>
            </div>
        </section>
   """ )
