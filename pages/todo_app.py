from nextpy.psx import component, create_onclick
from nextpy.db import Todo, get_session
from nextpy import fetch_api


@component
def TodoPage(props=None):
    props = props or {}
    todos = props.get("todos", [])
    
    return (
        <main data-nextpy-crud="todo" class="min-h-screen px-4 py-12 bg-slate-100 text-slate-900">
            <section class="max-w-2xl p-6 mx-auto bg-white shadow-sm rounded-xl">
                <div class="flex items-center justify-between mb-6">
                    <div>
                        <p class="text-sm font-semibold tracking-wide text-blue-600 uppercase">NextPy</p>
                        <h1 class="text-3xl font-bold">Shared Todos</h1>
                    </div>
                    <span data-nextpy-status class="text-sm text-slate-500">Connecting...</span>
                </div>
                <form data-nextpy-action="create" class="flex gap-2 mb-6">
                    <input data-nextpy-field="title" required maxlength="255" placeholder="What needs doing?" class="flex-1 min-w-0 px-3 py-2 border rounded-lg border-slate-300 focus:border-blue-500 focus:outline-none" />
                    <button type="submit" class="px-4 py-2 font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700">Add</button>
                </form>
                <p data-nextpy-error class="hidden p-3 mb-4 text-sm text-red-700 rounded-lg bg-red-50"></p>
                <ul data-nextpy-list class="space-y-2">
                    {for todo in todos:
                        <li data-nextpy-item={todo["id"]} class="flex items-center gap-3 p-3 border rounded-lg border-slate-200">
                            <input data-nextpy-toggle={todo["id"]} type="checkbox" checked={todo["completed"]} aria-label="Complete todo" />
                            <span class={"min-w-0 flex-1 " + ("text-slate-400 line-through" if todo["completed"] else "")}>{todo["title"]}</span>
                            <button data-nextpy-delete={todo["id"]} type="button" class="text-sm font-semibold text-red-600">Delete</button>
                        </li>
                    }
                </ul>
            </section>
        </main>
    )


def getServerSideProps(context):
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
                        "created_at": todo.created_at.isoformat() if todo.created_at else None
                    }
                    for todo in todos
                ]
            }
        }


default = TodoPage