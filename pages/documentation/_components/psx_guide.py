from nextpy.psx import psx, component, register_component, useState, create_onclick, interactive_component


@interactive_component
def PSXDemo(props):
    [greeting, setGreeting] = useState("Hello")
    handle_change = create_onclick(lambda e: setGreeting("Welcome" if greeting == "Hello" else "Hello"))

    return psx(f"""
        <div class="p-5 border border-amber-200 rounded-2xl bg-amber-50">
            <div class="flex items-center justify-between gap-4">
                <div>
                    <h3 class="font-semibold text-amber-900">Live PSX Demo</h3>
                    <p class="mt-1 text-sm text-amber-700">See PSX syntax in action with interactive state.</p>
                </div>
                <button create_onclick={handle_change} class="px-4 py-2 text-sm font-semibold text-white rounded-lg bg-amber-600">
                    Change Greeting
                </button>
            </div>
            <p class="mt-4 text-sm text-amber-800">{greeting} from NextPy PSX!</p>
        </div>
    """)

register_component("PSXDemo", PSXDemo)


@component
def PSXGuide(props):
    return psx("""
        <section id="psx-guide" class="space-y-6">
            <div class="pb-3 border-b border-gray-800">
                <h2 class="text-2xl font-bold text-gray-100">PSX (Python Syntax Extension)</h2>
                <p class="mt-2 text-gray-400">
                    Write component-based user interfaces using NextPy's Python Syntax Extension - a powerful way to build UI with Python.
                </p>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-blue-400">What is PSX?</h3>
                <p class="mt-2 text-sm text-blue-300">
                    <strong class="text-white">PSX is NextPy's component syntax.</strong> It can be written directly inside Python files or as standalone .psx files, which NextPy parses into Python components. PSX combines the power of React-style components with Python's simplicity, supporting component composition, props, children, and state management.
                </p>
                <p class="mt-2 text-sm text-blue-300">
                    When you write PSX in Python files, you use standard Python syntax with JSX-like template literals. When you use .psx files, NextPy compiles them to Python components automatically.
                </p>
            </div>

            <div class="grid gap-6 lg:grid-cols-2">
                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Basic PSX syntax</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">from nextpy.psx import component

@component
def Greeting(props):
    name = props.get("name", "World")
    return <h1>Hello, {name}!</h1>

# Usage
return <Greeting name="NextPy" /></pre>
                </div>

                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Component composition</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">@component
def Card(props):
    children = props.get("children")
    return (
        <div class="card">
            <h2>{props.get("title")}</h2>
            {children}
        </div>
    )

return (
    <Card title="Welcome">
        <p>This is content</p>
    </Card>
)</pre>
                </div>
            </div>

            <div class="grid gap-6 lg:grid-cols-2">
                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Conditional rendering</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">@component
def UserStatus(props):
    is_logged_in = props.get("logged_in", False)
    
    if is_logged_in:
        return <button>Logout</button>
    else:
        return <button>Login</button></pre>
                </div>

                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">List rendering</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">@component
def TodoList(props):
    items = props.get("items", [])
    
    return (
        <ul>
            {[
                <li key={item}>{item}</li>
                for item in items
            ]}
        </ul>
    )</pre>
                </div>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-gray-100">PSX file format</h3>
                <p class="mt-2 text-sm text-gray-400">
                    <strong class="text-white">You can write PSX in two ways:</strong>
                </p>
                <ul class="pl-5 mt-2 space-y-2 text-sm text-gray-400 list-disc">
                    <li><strong class="text-white">Python files (.py):</strong> Use the psx() function with template strings to write JSX-like syntax directly in Python</li>
                    <li><strong class="text-white">PSX files (.psx):</strong> Write pure JSX-style syntax that NextPy automatically compiles to Python components</li>
                </ul>
                <p class="mt-3 text-sm text-gray-400">
                    Both approaches result in the same Python components at runtime. The choice depends on your preference for pure Python vs. JSX-style syntax.
                </p>
                <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">// components/Button.psx (Optional JSX-style syntax)
export function Button(props) {
    const { children, onClick } = props
    return (
        <button onClick={onClick} class="btn">
            {children}
        </button>
    )
}</pre>
            </div>

            <PSXDemo />
        </section>
    """)
