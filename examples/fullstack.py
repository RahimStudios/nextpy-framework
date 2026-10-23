"""
NextPy Full-Stack Demo
Demonstrates enhanced client-server communication with server actions, state synchronization,
useFetch for client-side data loading, and useCrudEvent for reactive CRUD event handling.
"""

import json
from nextpy.psx import component, useCrudEvent, useFetch
from nextpy.db import get_session, Todo

# Import server actions (triggers registration)
from pages.actions.todo_actions import create_todo, toggle_todo, delete_todo, get_todos, get_todo_stats  # noqa: F401




@component
def FullStackDemo(props=None):
    """Enhanced full-stack demo with server actions and state sync"""
    props = props or {}
    stats = useFetch("/__nextpy/actions/execute", {
            "method": "POST",
            "headers": {"Content-Type": "application/json", "Accept": "application/json"},
            "body": '{"action":"get_todo_stats","params":{}}',
        })
    
    data_key = stats["_dataKey"]
    loading_key = stats["_loadingKey"]
    error_key = stats["_errorKey"]
    event = useCrudEvent(resource="todos")
    event_key = event["_eventKey"]

    server_todos = props.get("todos", [])

    crud_config = {
        "createAction": "create_todo",
        "updateAction": "toggle_todo",
        "deleteAction": "delete_todo",
        "resource": "todos",
        "wsChannel": "todos",
        "messageType": "TODO_CHANGED",
        "idParam": "todo_id",
        "deleteConfirm": "psx",
        "createReset": True,
    }
    crud = json.dumps(crud_config)

    return (
        <main data-nextpy-crud={crud} class="min-h-screen px-4 py-12 bg-gradient-to-br from-gray-50 to-gray-100">
            <div class="max-w-3xl mx-auto">
                <div class="mb-12 text-center">
                    <h1 class="mb-4 text-4xl font-bold text-gray-900">
                        NextPy Full-Stack Demo
                    </h1>
                    <p class="text-lg text-gray-600">
                        Enhanced client-server communication with server actions and real-time sync
                    </p>
                </div>

                <div class="p-6 mb-8 bg-white shadow-lg rounded-xl">
                    <h2 class="mb-4 text-xl font-semibold text-gray-900">Server Actions Available</h2>
                    <ul class="space-y-2 text-gray-600">
                        <li>- <code>create_todo</code> - Create new todo items</li>
                        <li>- <code>toggle_todo</code> - Toggle todo completion</li>
                        <li>- <code>delete_todo</code> - Delete todo items</li>
                        <li>- <code>get_todos</code> - Fetch all todos</li>
                    </ul>
                </div>

                <div class="p-6 mb-8 bg-white shadow-lg rounded-xl">
                    <div class="flex items-center justify-between mb-4">
                        <h2 class="text-xl font-semibold text-gray-900">Interactive Todos (Generic CRUD)</h2>
                        <span data-nextpy-status class="text-sm text-gray-500">Connecting...</span>
                    </div>

                    <form data-nextpy-action="create" class="flex gap-2 mb-6">
                        <input
                            data-nextpy-field="title"
                            required
                            maxlength="255"
                            placeholder="What needs doing?"
                            class="flex-1 min-w-0 px-3 py-2 border rounded-lg border-slate-300 focus:border-blue-500 focus:outline-none"
                        />
                        <button type="submit" class="px-4 py-2 font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700">Add</button>
                    </form>

                    <p data-nextpy-error class="hidden p-3 mb-4 text-sm text-red-700 rounded-lg bg-red-50"></p>

                    <ul data-nextpy-list class="space-y-3">
                        {for todo in server_todos:
                            <li data-nextpy-item={todo["id"]} class="flex items-center gap-4 p-4 rounded-lg bg-gray-50">
                                <input
                                    data-nextpy-toggle={todo["id"]}
                                    data-nextpy-field="completed"
                                    type="checkbox"
                                    checked={todo["completed"]}
                                    aria-label="Complete todo"
                                    class="w-5 h-5 text-blue-600 rounded focus:ring-blue-500"
                                />
                                <span data-nextpy-field="title" class={"flex-1 " + (todo["completed"] and "line-through text-gray-400" or "text-gray-900")}>
                                    {todo["title"]}
                                </span>
                                <button
                                    data-nextpy-delete={todo["id"]}
                                    type="button"
                                    class="text-sm font-medium text-red-600 hover:text-red-800"
                                >
                                    Delete
                                </button>
                            </li>
                        }
                    </ul>
                </div>

                <div class="grid grid-cols-1 gap-6 mt-8 md:grid-cols-3">
                    <div class="p-6 bg-white rounded-lg shadow">
                        <h3 class="mb-2 font-semibold text-gray-900">Server Actions</h3>
                        <p class="text-sm text-gray-600">
                            CRUD operations use server actions - no API endpoints needed
                        </p>
                    </div>

                    <div class="p-6 bg-white rounded-lg shadow">
                        <h3 class="mb-2 font-semibold text-gray-900">useFetch</h3>
                        <p class="text-sm text-gray-600">
                            Client-side data fetching with reactive state updates
                        </p>
                    </div>

                    <div class="p-6 bg-white rounded-lg shadow">
                        <h3 class="mb-2 font-semibold text-gray-900">useCrudEvent</h3>
                        <p class="text-sm text-gray-600">
                            Reactive bridge between CRUD operations and PSX components
                        </p>
                    </div>
                </div>
                
                
                
                    
                        <div class="p-6 bg-white rounded-lg shadow">
                            <h3 class="mb-3 font-semibold text-gray-900">Event Log (useCrudEvent)</h3>
                            <p class="mb-4 text-sm text-gray-500">
                                Listens for <code>nextpy:crud:changed</code> events via <code>useCrudEvent</code>
                            </p>
                            <div data-bind="textContent:{event_key}" class="text-sm text-gray-600">
                                No events yet. Try adding, toggling, or deleting a todo above.
                            </div>
                        </div>
                        
                        <div class="p-6 bg-white rounded-lg shadow">
                                    <h3 class="mb-3 font-semibold text-gray-900">Live Statistics (useFetch)</h3>
                                    <p class="mb-4 text-sm text-gray-500">
                                        Fetched client-side via <code>useFetch</code> + server action
                                    </p>
                                    <div data-bind="textContent:{loading_key}" class="text-sm text-blue-600">
                                        Loading...
                                    </div>
                                    <div data-bind="textContent:{error_key}" class="text-sm text-red-600">
                                    </div>
                                    <div data-bind="innerHTML:{data_key}" class="text-sm text-gray-700">
                                    </div>
                        </div>
                    

                

                <div class="p-6 mt-8 font-mono text-sm text-green-400 bg-gray-900 rounded-lg">
                    <h3 class="mb-4 text-white">Server Actions CRUD Configuration:</h3>
                    <pre>
# Configure CRUD using Server Actions
crud_config = {
    "createAction": "create_post",
    "updateAction": "update_post",
    "deleteAction": "delete_post",
    "resource": "posts",
    "wsChannel": "posts",
    "messageType": "POST_CHANGED",
    "idParam": "post_id",
    "deleteConfirm": "Delete this post?"
}

# useFetch - client-side data loading
stats = useFetch("/api/stats")
# Returns { "data": ..., "loading": ..., "error": ..., "refetch": ... }

# useCrudEvent - reactive CRUD event bridge
event = useCrudEvent(resource="posts")
# Returns { "data": ..., "_eventKey": "..." }
# Use data-bind={f"textContent:{event['_eventKey']}"} to display
                    </pre>
                </div>

                <div data-delete-modal class="fixed inset-0 z-50 items-center justify-center hidden p-4 bg-opacity-50 bg-black/10 backdrop-blur-sm" style="display:none;">
                    <div class="w-full max-w-sm p-6 bg-white shadow-xl rounded-xl">
                        <h3 class="mb-2 text-lg font-semibold text-gray-900">Confirm Delete</h3>
                        <p class="mb-6 text-sm text-gray-600">Are you sure you want to delete <span data-nextpy-modal-title>this item</span>?</p>
                        <div class="flex justify-end gap-3">
                            <button
                                type="button"
                                data-nextpy-modal-cancel
                                class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
                            >
                                Cancel
                            </button>
                            <button
                                type="button"
                                data-nextpy-modal-confirm
                                class="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                            >
                                Delete
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    )


def getServerSideProps(context):
    """Server-side data fetching"""
    with get_session() as db:
        todos = db.query(Todo).order_by(Todo.created_at.desc()).limit(10).all()

        return {
            "props": {
                "title": "NextPy Full-Stack Demo",
                "description": "Enhanced client-server communication with server actions and real-time sync",
                "todos": [
                    {
                        "id": todo.id,
                        "title": todo.title,
                        "completed": todo.completed,
                        "created_at": todo.created_at.isoformat() if todo.created_at else None,
                    }
                    for todo in todos
                ],
            }
        }


default = FullStackDemo
