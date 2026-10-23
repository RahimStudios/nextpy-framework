"""
TodoStats Component
useFetch demo - loads todo statistics from a server action endpoint
and reactively updates when the user performs CRUD operations.
"""

from nextpy.psx import interactive_component, useFetch


@interactive_component
def TodoStats(props=None):
    stats = useFetch("/__nextpy/actions/execute", {
        "method": "POST",
        "headers": {"Content-Type": "application/json", "Accept": "application/json"},
        "body": '{"action":"get_todo_stats","params":{}}',
    })

    data_key = stats["_dataKey"]
    loading_key = stats["_loadingKey"]
    error_key = stats["_errorKey"]

    return (
        <div class="p-6 bg-white rounded-lg shadow">
            <h3 class="mb-3 font-semibold text-gray-900">Live Statistics (useFetch)</h3>
            <p class="mb-4 text-sm text-gray-500">
                Fetched client-side via <code>useFetch</code> + server action
            </p>
            <div data-bind={f"textContent:{loading_key}"} class="text-sm text-blue-600">
                Loading...
            </div>
            <div data-bind={f"textContent:{error_key}"} class="text-sm text-red-600">
            </div>
            <div data-bind={f"innerHTML:{data_key}"} class="text-sm text-gray-700">
            </div>
        </div>
    )

default=TodoStats
