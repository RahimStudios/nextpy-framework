"""
Search Example Page
Demonstrates search functionality
"""

from nextpy.utils.search import simple_search, fuzzy_search


def get_template():
    return "search.html"


async def get_server_side_props(context):
    # Sample data
    items = [
        {"id": 1, "title": "Getting Started", "content": "Learn NextPy basics"},
        {"id": 2, "title": "File-Based Routing", "content": "How routing works"},
        {"id": 3, "title": "Database Integration", "content": "Using SQLAlchemy"},
        {"id": 4, "title": "API Routes", "content": "Create REST endpoints"},
        {"id": 5, "title": "Components", "content": "Pre-built UI components"},
    ]
    
    query = context.get("query", {}).get("q", "")
    
    if query:
        results = simple_search(query, items, ["title", "content"])
    else:
        results = items
    
    return {
        "props": {
            "title": "Search",
            "query": query,
            "results": results,
            "total": len(results)
        }
    }
