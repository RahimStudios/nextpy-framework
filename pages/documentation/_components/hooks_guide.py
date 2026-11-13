from nextpy.psx import psx, component, register_component, useState, useEffect, useReducer, useMemo, useCallback, create_onclick, interactive_component


@interactive_component
def HooksDemo(props):
    [count, setCount] = useState(0)
    [doubled, setDoubled] = useState(0)
    
    handle_increment = create_onclick(lambda e: setCount(count + 1))
    handle_double = create_onclick(lambda e: setDoubled(count * 2))

    return psx(f"""
        <div class="p-5 border border-purple-200 rounded-2xl bg-purple-50">
            <div class="flex items-center justify-between gap-4">
                <div>
                    <h3 class="font-semibold text-purple-900">Hooks Demo</h3>
                    <p class="mt-1 text-sm text-purple-700">Multiple hooks working together.</p>
                </div>
                <div class="flex gap-2">
                    <button create_onclick={handle_increment} class="px-3 py-2 text-sm font-semibold text-white rounded-lg bg-purple-600">
                        +1
                    </button>
                    <button create_onclick={handle_double} class="px-3 py-2 text-sm font-semibold rounded-lg text-purple-700 bg-purple-100">
                        Double
                    </button>
                </div>
            </div>
            <div class="mt-4 text-sm text-purple-800">
                <p>Count: {count}</p>
                <p>Doubled: {doubled}</p>
            </div>
        </div>
    """)

register_component("HooksDemo", HooksDemo)


@component
def HooksGuide(props):
    return psx("""
        <section id="hooks-guide" class="space-y-6">
            <div class="pb-3 border-b border-gray-800">
                <h2 class="text-2xl font-bold text-gray-100">Hooks Guide</h2>
                <p class="mt-2 text-gray-400">
                    Manage component state and side effects with React-style hooks in Python.
                </p>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-indigo-400">What are Hooks?</h3>
                <p class="mt-2 text-sm text-indigo-300">
                    Hooks are functions that let you use state and other React features in functional components. They follow the same mental model as React hooks but are implemented in Python.
                </p>
            </div>

            <div class="grid gap-6 lg:grid-cols-2">
                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">useState</h3>
                    <p class="mt-2 text-sm text-gray-400">Manage local component state.</p>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">from nextpy.psx import useState

[count, setCount] = useState(0)
# count: current state value
# setCount: function to update state

setCount(count + 1)  # Update state</pre>
                </div>

                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">useEffect</h3>
                    <p class="mt-2 text-sm text-gray-400">Handle side effects like data fetching.</p>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">from nextpy.psx import useEffect

useEffect(lambda: print("Mounted"), [])
useEffect(
    lambda: print(f"Count changed: {count}"),
    [count]
)</pre>
                </div>
            </div>

            <div class="grid gap-6 lg:grid-cols-2">
                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">useReducer</h3>
                    <p class="mt-2 text-sm text-gray-400">Manage complex state with reducers.</p>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">from nextpy.psx import useReducer

def reducer(state, action):
    if action["type"] == "increment":
        return state + 1
    return state

[state, dispatch] = useReducer(reducer, 0)
dispatch({"type": "increment"})</pre>
                </div>

                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">useMemo & useCallback</h3>
                    <p class="mt-2 text-sm text-gray-400">Optimize performance with memoization.</p>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">from nextpy.psx import useMemo, useCallback

expensive_value = useMemo(
    lambda: compute_expensive(data),
    [data]
)

memoized_callback = useCallback(
    lambda e: handle_click(e),
    [dependency]
)</pre>
                </div>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-gray-100">Hook Rules</h3>
                <ul class="pl-5 mt-3 space-y-2 text-sm text-gray-400 list-disc">
                    <li>Only call hooks at the top level of components</li>
                    <li>Don't call hooks inside loops, conditions, or nested functions</li>
                    <li>Only call hooks from functional components or custom hooks</li>
                    <li>Custom hooks should start with "use" prefix</li>
                </ul>
            </div>

            <HooksDemo />
        </section>
    """)
