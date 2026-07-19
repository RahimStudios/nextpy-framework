from nextpy.psx import component, interactive_component, useState, create_onclick, register_component, psx


@interactive_component
def StateAndHooksDemo(props):
    [counter, setCounter] = useState(0)
    handle_incrementer = create_onclick(lambda e: setCounter(counter + 1))
    handle_reseter = create_onclick(lambda e: setCounter(0))

    return psx(f"""
        <div class="p-5 border border-violet-200 rounded-2xl bg-violet-50">
            <div class="flex items-center justify-between gap-4">
                <div>
                    <h3 class="font-semibold text-violet-900">Interactive state example</h3>
                    <p class="mt-1 text-sm text-violet-700">Use hooks to manage UI state without leaving Python.</p>
                </div>
                <div class="flex gap-2">
                    <button create_onclick={handle_incrementer} class="px-3 py-2 text-sm font-semibold text-white rounded-lg bg-violet-600">
                        +1
                    </button>
                    <button create_onclick={handle_reseter} class="px-3 py-2 text-sm font-semibold rounded-lg text-violet-700 bg-violet-100">
                        Reset
                    </button>
                </div>
            </div>
            <p class="mt-4 text-sm text-violet-800">Current count: {counter}</p>
        </div>
    """)
register_component("StateAndHooksDemo", StateAndHooksDemo)


@component
def StateAndHooks():
    return psx("""
        <section id="state-and-hooks" class="space-y-6">
            <div class="pb-3 border-b border-gray-800">
                <h2 class="text-2xl font-bold text-gray-100">State and Hooks</h2>
                <p class="mt-2 text-gray-400">
                    Manage component state with the same mental model as modern frontend frameworks, but in Python.
                </p>
            </div>

            <div class="grid gap-6 lg:grid-cols-2">
                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Hook example</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">from nextpy.psx import useState, create_onclick

[count, setCount] = useState(0)
handle_click = create_onclick(lambda e: setCount(count + 1))</pre>
                </div>

                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">When to use state</h3>
                    <ul class="pl-5 mt-3 space-y-2 text-sm text-gray-400 list-disc">
                        <li>Toggle menus and dialogs</li>
                        <li>Store form input and submission status</li>
                        <li>Drive dynamic lists and conditional rendering</li>
                    </ul>
                </div>
            </div>

            <StateAndHooksDemo />
        </section>
    """)
