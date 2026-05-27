"""
Homepage - NextPy Demo
Demonstrates SSR with getServerSideProps
"""

def get_template():
    """Return the template to render"""
    return "index.html"


async def get_server_side_props(context):
    """
    Fetch data on every request (SSR)
    Similar to Next.js getServerSideProps
    """
    features = [
        {
            "icon": "folder",
            "title": "File-based Routing",
            "description": "Automatic routing based on your pages directory structure. Just like Next.js."
        },
        {
            "icon": "lightning",
            "title": "Server-Side Rendering",
            "description": "Fast initial page loads with SSR. Data fetching happens on the server."
        },
        {
            "icon": "building",
            "title": "Static Site Generation",
            "description": "Pre-render pages at build time for blazing fast performance."
        },
        {
            "icon": "plug",
            "title": "API Routes",
            "description": "Build your API with FastAPI in the pages/api directory."
        },
        {
            "icon": "target",
            "title": "Type Safety",
            "description": "Full Pydantic integration for validated, type-safe data handling."
        },
        {
            "icon": "refresh",
            "title": "HTMX Integration",
            "description": "SPA-like experience with minimal JavaScript using HTMX."
        },
    ]
    
    return {
        "props": {
            "title": "NextPy",
            "description": "The Python web framework. Build modern web applications with file-based routing, SSR, SSG, and more.",
            "features": features,
        }
    }