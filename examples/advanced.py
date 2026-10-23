"""
Advanced Examples Page - SSG, ISR, Redirects, and more
"""

def get_template():
    return "examples_advanced.html"


async def get_static_props(context):
    """Use static generation for this page"""
    return {
        "props": {
            "title": "Advanced Examples",
            "description": "Explore advanced NextPy features",
            "examples": [
                {
                    "name": "Static Generation",
                    "desc": "Pre-rendered at build time",
                    "file": "pages/blog/[slug].py"
                },
                {
                    "name": "File Uploads",
                    "desc": "Handle multipart form data",
                    "file": "pages/api/upload.py"
                },
                {
                    "name": "Protected Routes",
                    "desc": "Redirect unauthenticated users",
                    "file": "pages/dashboard.py"
                },
                {
                    "name": "Error Handling",
                    "desc": "Custom 404 and 500 pages",
                    "file": "pages/_404.py"
                }
            ]
        },
        "revalidate": 86400  # Revalidate daily
    }
