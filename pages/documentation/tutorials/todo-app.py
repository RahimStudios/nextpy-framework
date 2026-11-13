from nextpy.psx import register_component, component, psx, interactive_component, useState, useEffect


@component
def TodoAppTutorial():
    return psx("""
        <div class="mx-auto max-w-6xl">
        <div class="grid gap-12 lg:grid-cols-[1fr_260px]">
        <article class="min-w-0">
        <DocsScrollSpy />
            <div class="mb-8 pb-6 border-b border-gray-800">
                <div class="flex items-center gap-3 mb-4">
                    <span class="px-2 py-1 text-xs font-medium border rounded bg-blue-500/20 text-blue-400 border-blue-500">
                        Tutorial
                    </span>
                    <span class="px-2 py-1 text-xs font-medium border rounded bg-yellow-500/20 text-yellow-400 border-yellow-500">
                        Intermediate
                    </span>
                    <span class="px-2 py-1 text-xs font-medium border rounded bg-gray-700 text-gray-300 border-gray-600">
                        NextPy 5.0.0
                    </span>
                    <span class="ml-auto text-sm text-gray-400">
                        ⏱ 30 minutes
                    </span>
                </div>
                
                <h1 class="text-4xl font-bold text-white">
                    Build a Todo App
                </h1>
                
                <p class="mt-4 text-lg text-gray-400">
                    Learn to build a complete todo application with state management, forms, and CRUD operations in NextPy.
                </p>
            </div>
            
            <div class="my-6 p-4 border border-gray-700 bg-gray-800 rounded-lg">
                <div class="flex items-start gap-3">
                    <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-gray-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                    </svg>
                    <div class="flex-1">
                        <h4 class="font-semibold text-gray-200">Prerequisites</h4>
                        <ul class="mt-2 space-y-1 text-sm text-gray-400">
                            <li class="flex items-center gap-2">
                                <svg class="w-3 h-3 text-green-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                                </svg>
                                Completed "Your First App" tutorial
                            </li>
                            <li class="flex items-center gap-2">
                                <svg class="w-3 h-3 text-green-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                                </svg>
                                Basic understanding of hooks
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <section id="overview" class="my-12 scroll-mt-20">
                <h2 class="text-3xl font-bold text-white mb-6">
                    What You'll Build
                </h2>
                <p class="text-gray-300 mb-4">
                    In this tutorial, you'll build a fully functional todo application with:
                </p>
                <ul class="list-disc list-inside space-y-2 text-gray-300 ml-4">
                    <li>Add new todos with a form</li>
                    <li>Display todo list with filtering</li>
                    <li>Mark todos as complete</li>
                    <li>Delete todos</li>
                    <li>Persist state using useState</li>
                    <li>Styled with Tailwind CSS</li>
                </ul>
            </section>
            
            <section id="setup" class="my-12 scroll-mt-20">
                <h2 class="text-3xl font-bold text-white mb-6">
                    Step 1: Project Setup
                </h2>
                <p class="text-gray-300 mb-4">
                    Create a new NextPy project if you haven't already:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-gray-700 bg-gray-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-gray-700 bg-gray-800">
                        <span class="px-2 py-0.5 text-xs font-medium text-gray-300 uppercase bg-gray-700 rounded">
                            bash
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-bash">nextpy create todo-app
cd todo-app
nextpy dev</code>
                    </pre>
                </div>
            </section>
            
            <section id="todo-component" class="my-12 scroll-mt-20">
                <h2 class="text-3xl font-bold text-white mb-6">
                    Step 2: Create the Todo Component
                </h2>
                <p class="text-gray-300 mb-4">
                    Create a todo component with state management:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-gray-700 bg-gray-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-gray-700 bg-gray-800">
                        <span class="text-sm text-gray-400 font-mono">pages/index.py</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-gray-300 uppercase bg-gray-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python">from nextpy.psx import component, useState, create_onclick

@component
def TodoApp():
    # State
    [todos, setTodos] = useState([])
    [inputValue, setInputValue] = useState("")
    
    # Handlers
    def handle_add(e):
        e.preventDefault()
        if inputValue.strip():
            setTodos(todos + [{"id": len(todos), "text": inputValue, "completed": False}])
            setInputValue("")
    
    def handle_toggle(id):
        setTodos([
            {**todo, "completed": not todo["completed"]}
            for todo in todos
        ])
    
    def handle_delete(id):
        setTodos([todo for todo in todos if todo["id"] != id])
    
    def handle_clear_completed(e):
        e.preventDefault()
        setTodos([todo for todo in todos if not todo["completed"]])
    
    return (
        &lt;div class="max-w-md mx-auto p-8 bg-gray-900 min-h-screen"&gt;
            &lt;h1 class="text-3xl font-bold text-white mb-8"&gt;Todo App&lt;/h1&gt;
            
            &lt;form onsubmit="handle_add" class="mb-6"&gt;
                &lt;input 
                    type="text"
                    value={inputValue}
                    oninput={lambda e: setInputValue(e.target.value)}
                    placeholder="Add a new todo..."
                    class="w-full px-4 py-2 rounded-lg border border-gray-700 bg-gray-800 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                /&gt;
                &lt;button 
                    type="submit"
                    class="mt-2 px-4 py-2 font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700"
                &gt;
                    Add Todo
                &lt;/button&gt;
            &lt;/form&gt;
            
            &lt;div class="space-y-2"&gt;
                {for todo in todos:
                    &lt;div class="flex items-center gap-3 p-4 border border-gray-700 rounded-lg"&gt;
                        &lt;input 
                            type="checkbox"
                            checked={todo["completed"]}
                            create_onclick="handle_toggle"
                            class="w-5 h-5 rounded"
                        /&gt;
                        &lt;span class={"flex-1 " + ("line-through text-gray-500" if todo["completed"] else "text-white")}&gt;
                            {todo["text"]}
                        &lt;/span&gt;
                        &lt;button 
                            create_onclick="handle_delete"
                            class="text-red-400 hover:text-red-300"
                        &gt;
                            Delete
                        &lt;/button&gt;
                    &lt;/div&gt;
                }
            &lt;/div&gt;
            
            {if len(todos) > 0:
                &lt;button 
                    create_onclick="handle_clear_completed"
                    class="mt-6 px-4 py-2 font-semibold text-gray-400 bg-gray-800 rounded-lg hover:bg-gray-700"
                &gt;
                    Clear Completed
                &lt;/button&gt;
            }
        &lt;/div&gt;
    )




default = TodoApp</code>
                    </pre>
                </div>
                
                <div class="my-6 p-4 border-l-4 border-purple-500 bg-purple-900/20 rounded-r-lg">
                    <div class="flex items-start gap-3">
                        <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-purple-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                        </svg>
                        <div class="flex-1">
                            <h4 class="font-semibold text-purple-400">Tip</h4>
                            <div class="mt-1 text-sm text-gray-300">
                                The useState hook returns a tuple of [state, setState]. Always use setState to update state - never modify state directly.
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            
            <section id="components" class="my-12 scroll-mt-20">
                <h2 class="text-3xl font-bold text-white mb-6">
                    Step 3: Extract Reusable Components
                </h2>
                <p class="text-gray-300 mb-4">
                    Let's extract the todo item into a reusable component:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-gray-700 bg-gray-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-gray-700 bg-gray-800">
                        <span class="text-sm text-gray-400 font-mono">components/todo_item.py</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-gray-300 uppercase bg-gray-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python">from nextpy.psx import component

@component
def TodoItem(props):
    todo = props.get("todo", {})
    on_toggle = props.get("on_toggle")
    on_delete = props.get("on_delete")
    
    return (
        &lt;div class="flex items-center gap-3 p-4 border border-gray-700 rounded-lg"&gt;
            &lt;input 
                type="checkbox"
                checked={todo.get("completed", False)}
                create_onclick="on_toggle"
                class="w-5 h-5 rounded"
            /&gt;
            &lt;span class={"flex-1 " + ("line-through text-gray-500" if todo.get("completed") else "text-white")}&gt;
                {todo.get("text", "")}
            &lt;/span&gt;
            &lt;button 
                create_onclick="on_delete"
                class="text-red-400 hover:text-red-300"
            &gt;
                Delete
            &lt;/button&gt;
        &lt;/div&gt;
    )

default = TodoItem</code>
                    </pre>
                </div>
                
                <div class="my-6 overflow-hidden rounded-lg border border-gray-700 bg-gray-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-gray-700 bg-gray-800">
                        <span class="text-sm text-gray-400 font-mono">pages/index.py (updated)</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-gray-300 uppercase bg-gray-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python">from nextpy.psx import component, useState
from components.todo_item import TodoItem

@component
def TodoApp():
    [todos, setTodos] = useState([])
    [inputValue, setInputValue] = useState("")
    
    def handle_add(e):
        e.preventDefault()
        if inputValue.strip():
            setTodos(todos + [{"id": len(todos), "text": inputValue, "completed": False}])
            setInputValue("")
    
    def handle_toggle(id):
        setTodos([
            {**todo, "completed": not todo["completed"]}
            for todo in todos
        ])
    
    def handle_delete(id):
        setTodos([todo for todo in todos if todo["id"] != id])
    
    return (
        &lt;div class="max-w-md mx-auto p-8 bg-gray-900 min-h-screen"&gt;
            &lt;h1 class="text-3xl font-bold text-white mb-8"&gt;Todo App&lt;/h1&gt;
            
            &lt;form onsubmit="handle_add" class="mb-6"&gt;
                &lt;input 
                    type="text"
                    value={inputValue}
                    oninput={lambda e: setInputValue(e.target.value)}
                    placeholder="Add a new todo..."
                    class="w-full px-4 py-2 rounded-lg border border-gray-700 bg-gray-800 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                /&gt;
                &lt;button 
                    type="submit"
                    class="mt-2 px-4 py-2 font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700"
                &gt;
                    Add Todo
                &lt;/button&gt;
            &lt;/form&gt;
            
            &lt;div class="space-y-2"&gt;
                {for todo in todos:
                    &lt;TodoItem 
                        todo={todo}
                        on_toggle={lambda e: handle_toggle(todo["id"])}
                        on_delete={lambda e: handle_delete(todo["id"])}
                    /&gt;
                }
            &lt;/div&gt;
        &lt;/div&gt;
    )

default = TodoApp</code>
                    </pre>
                </div>
            </section>
            
            <section id="styling" class="my-12 scroll-mt-20">
                <h2 class="text-3xl font-bold text-white mb-6">
                    Step 4: Add Styling
                </h2>
                <p class="text-gray-300 mb-4">
                    Enhance the UI with better styling:
                </p>
                
                <div class="my-6 overflow-hidden rounded-lg border border-gray-700 bg-gray-900">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-gray-700 bg-gray-800">
                        <span class="text-sm text-gray-400 font-mono">pages/index.py (final)</span>
                        <span class="px-2 py-0.5 text-xs font-medium text-gray-300 uppercase bg-gray-700 rounded">
                            python
                        </span>
                    </div>
                    <pre class="p-4 overflow-x-auto text-sm leading-relaxed">
                        <code class="language-python">from nextpy.psx import component, useState
from components.todo_item import TodoItem

@component
def TodoApp():
    [todos, setTodos] = useState([])
    [inputValue, setInputValue] = useState("")
    
    def handle_add(e):
        e.preventDefault()
        if inputValue.strip():
            setTodos(todos + [{"id": len(todos), "text": inputValue, "completed": False}])
            setInputValue("")
    
    def handle_toggle(id):
        setTodos([
            {**todo, "completed": not todo["completed"]}
            for todo in todos
        ])
    
    def handle_delete(id):
        setTodos([todo for todo in todos if todo["id"] != id])
    
    return (
        &lt;div class="max-w-2xl mx-auto p-8 bg-gradient-to-br from-gray-900 to-gray-800 min-h-screen"&gt;
            &lt;div class="mb-8"&gt;
                &lt;h1 class="text-4xl font-bold text-white mb-2"&gt;Todo App&lt;/h1&gt;
                &lt;p class="text-gray-400"&gt;{len(todos)} {len(todos) == 1 and "todo" or "todos"}&lt;/p&gt;
            &lt;/div&gt;
            
            &lt;form onsubmit="handle_add" class="mb-8"&gt;
                &lt;div class="flex gap-3"&gt;
                    &lt;input 
                        type="text"
                        value={inputValue}
                        oninput={lambda e: setInputValue(e.target.value)}
                        placeholder="Add a new todo..."
                        class="flex-1 px-4 py-3 rounded-lg border border-gray-600 bg-gray-800 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    /&gt;
                    &lt;button 
                        type="submit"
                        class="px-6 py-3 font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition"
                    &gt;
                        Add Todo
                    &lt;/button&gt;
                &lt;/div&gt;
            &lt;/form&gt;
            
            &lt;div class="space-y-3"&gt;
                {for todo in todos:
                    &lt;TodoItem 
                        todo={todo}
                        on_toggle={lambda e: handle_toggle(todo["id"])}
                        on_delete={lambda e: handle_delete(todo["id"])}
                    /&gt;
                }
            &lt;/div&gt;
            
            {if len(todos) > 0:
                &lt;div class="mt-8 pt-6 border-t border-gray-700"&gt;
                    &lt;p class="text-sm text-gray-400 mb-3"&gt;
                        {len([t for t in todos if not t["completed"]])} of {len(todos)} remaining
                    &lt;/p&gt;
                    &lt;button 
                        create_onclick="handle_clear_completed"
                        class="px-4 py-2 text-sm font-medium text-gray-400 bg-gray-800 rounded-lg hover:bg-gray-700 transition"
                    &gt;
                        Clear Completed
                    &lt;/button&gt;
                &lt;/div&gt;
            }
        &lt;/div&gt;
    )

default = TodoApp</code>
                    </pre>
                </div>
            </section>
            
            <section id="summary" class="my-12 scroll-mt-20">
                <h2 class="text-3xl font-bold text-white mb-6">
                    Summary
                </h2>
                <p class="text-gray-300 mb-4">
                    You've built a complete todo application with:
                </p>
                <ul class="list-disc list-inside space-y-2 text-gray-300 ml-4">
                    <li>✅ State management with useState</li>
                    <li>✅ Form handling with preventDefault</li>
                    <li>✅ CRUD operations (Create, Read, Update, Delete)</li>
                    <li>✅ Component composition and props</li>
                    <li>✅ Conditional rendering</li>
                    <li>✅ Tailwind CSS styling</li>
                </ul>
                
                <div class="my-6 p-4 border-l-4 border-green-500 bg-green-900/20 rounded-r-lg">
                    <div class="flex items-start gap-3">
                        <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-green-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <div class="flex-1">
                            <h4 class="font-semibold text-green-400">Congratulations!</h4>
                            <div class="mt-1 text-sm text-gray-300">
                                You've learned the core concepts of NextPy: state, components, forms, and styling. Try customizing the app or adding new features!
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            
            <section id="next-steps" class="my-12 scroll-mt-20">
                <h2 class="text-3xl font-bold text-white mb-6">
                    What's Next?
                </h2>
                <p class="text-gray-300 mb-4">
                    Continue your NextPy journey with these tutorials:
                </p>
                <ul class="space-y-2 text-gray-300">
                    <li>Build a Blog App with SSR and dynamic routes</li>
                    <li>Build a Full-Stack App with database and authentication</li>
                    <li>Learn about data fetching and API routes</li>
                    <li>Explore advanced hooks and state management</li>
                </ul>
            </section>
        </article>
        <aside class="hidden lg:block">
            <div class="sticky top-24 text-sm">
                <h4 class="font-semibold text-white mb-4 tracking-wide">On this page</h4>
                <ul class="space-y-3 font-medium text-zinc-400 border-l border-zinc-800/50">
                        <li><a href="#overview" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">What You'll Build</a></li>
                        <li><a href="#setup" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 1: Project Setup</a></li>
                        <li><a href="#todo-component" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 2: Todo Component</a></li>
                        <li><a href="#components" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 3: Components</a></li>
                        <li><a href="#styling" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Step 4: Styling</a></li>
                        <li><a href="#summary" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Summary</a></li>
                        <li><a href="#next-steps" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">What's Next</a></li>
                </ul>
            </div>
        </aside>
        </div>
        </div>
        """)


default = TodoAppTutorial

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
