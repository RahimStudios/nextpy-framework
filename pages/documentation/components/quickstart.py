from nextpy.psx import component, interactive_component, useState, create_onclick, psx, register_component
from pages.components.codeblock import CodeBlock

register_component('CodeBlock', CodeBlock)


@interactive_component
def QuickStartDemo(props):

    [count, setCount] = useState(0)

    handle_click = create_onclick(lambda e: setCount(count + 1))

    return psx(f"""
        <div class="p-5 border border-emerald-800 rounded-2xl bg-gray-900">

            <div class="flex items-center justify-between gap-4">

                <div>
                    <h3 class="font-semibold text-emerald-400 flex items-center gap-2">

                        <svg class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" stroke-width="2"
                            viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>

                        Live demo
                    </h3>

                    <p class="mt-1 text-sm text-gray-400">
                        This counter uses real NextPy state system.
                    </p>
                </div>

                <button create_onclick={handle_click}
                    class="px-4 py-2 text-sm font-semibold text-white rounded-lg bg-emerald-600 hover:bg-emerald-500 transition">
                    Increment
                </button>

            </div>

            <p class="mt-4 text-sm text-gray-300">
                Current count: {count}
            </p>

        </div>
    """)


register_component("QuickStartDemo", QuickStartDemo)


@component
def QuickStart():
    return psx("""
        <section id="quickstart" class="space-y-10 py-8">

            <!-- Header -->
            <div class="pb-4 border-b border-gray-800">

                <h2 class="text-3xl font-bold text-white">
                    Quick Start
                </h2>

                <p class="mt-3 text-gray-400">
                    Build your first page, add state, and run your app instantly.
                </p>

            </div>

            <!-- Grid 1 -->
            <div class="grid gap-6 lg:grid-cols-2">

                <div class="p-6 border border-gray-800 rounded-2xl bg-gray-900">

                    <h3 class="font-semibold text-white">1. Create a page</h3>

                    <CodeBlock
                        lang="python"
                        code="
from nextpy.psx import component

@component
def Home():
    return <h1>Hello from NextPy</h1>

default = Home
                        "
                    />

                </div>

                <div class="p-6 border border-gray-800 rounded-2xl bg-gray-900">

                    <h3 class="font-semibold text-white">2. Add interactivity</h3>

                    <CodeBlock
                        lang="python"
                        code="
from nextpy.psx import component, useState, create_onclick

@component
def Counter():
    count, setCount = useState(0)
    handle_click = create_onclick(lambda e: setCount(count + 1))

    return (
        <div>
            <p>Count: {count}</p>
            <button create_onclick='handle_click'>Increment</button>
        </div>
    )
                        "
                    />

                </div>

            </div>

            <!-- Grid 2 -->
            <div class="grid gap-6 lg:grid-cols-2">

                <div class="p-6 border border-gray-800 rounded-2xl bg-gray-900">

                    <h3 class="font-semibold text-white">3. Create components</h3>

                    <CodeBlock
                        lang="python"
                        code="
@component
def Card(props):
    title = props.get('title', 'Default')
    children = props.get('children')

    return (
        <div class='card'>
            <h2>{title}</h2>
            {children}
        </div>
    )
                        "
                    />

                </div>

                <div class="p-6 border border-gray-800 rounded-2xl bg-gray-900">

                    <h3 class="font-semibold text-white">4. Styling</h3>

                    <CodeBlock
                        lang="python"
                        code="
@component
def StyledButton(props):
    return (
        <button class='px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700'>
            {props.get('children')}
        </button>
    )
                        "
                    />

                </div>

            </div>

            <!-- Run -->
            <div class="p-6 border border-gray-800 rounded-2xl bg-gray-800">

                <h3 class="font-semibold text-emerald-400 flex items-center gap-2">

                    <svg class="w-5 h-5 text-emerald-400" fill="none" stroke="currentColor" stroke-width="2"
                        viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M5 13l4 4L19 7" />
                    </svg>

                    Run your app
                </h3>

                <CodeBlock
                    lang="bash"
                    code="nextpy dev"
                />

                <p class="mt-3 text-sm text-gray-300">
                    Visit localhost:8000 — hot reload enabled.
                </p>

            </div>

            <!-- Live Demo -->
            <QuickStartDemo />

        </section>
    """)