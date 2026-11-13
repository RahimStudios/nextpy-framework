from nextpy.psx import component, register_component, psx


@component
def ReusableComponents(props):
    props=props or {}
    title = props.get("title", "Reusable Components")
    
    return psx(f"""
        <section id="components" class="space-y-6">
            <div class="pb-3 border-b border-gray-800">
                <h2 class="text-2xl font-bold text-gray-100">Reusable Components</h2>
                <p class="mt-2 text-gray-400">
                    Build small, composable pieces of UI and combine them into complete pages with props and shared logic.
                </p>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                <h3 class="font-semibold text-gray-100">Component pattern</h3>
                <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">from nextpy.psx import component

        @component
        def Card(props):
            title = props.get("title", "Untitled")
            return(
                <div class="card">{title}</div></pre>
                    </div>

                    <div class="grid gap-6 md:grid-cols-2">
                        <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                            <h3 class="font-semibold text-gray-100">Why components help</h3>
                            <p class="mt-2 text-sm text-gray-400">They keep your code organized, make your interfaces easier to scale, and simplify maintenance.</p>
                        </div>

                        <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                            <h3 class="font-semibold text-gray-100">Composition tips</h3>
                            <p class="mt-2 text-sm text-gray-400">Split UI into layout, feature, and data-display components so each file stays focused.</p>
                        </div>
                    </div>
                </section>
            )
            """)
