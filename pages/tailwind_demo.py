"""
Tailwind CSS Demo Page
Tests various Tailwind classes to verify integration
"""

def get_template():
    """Return template to render"""
    return "tailwind_demo.html"

async def get_server_side_props(context):
    """Server-side props for demo"""
    return {
        "props": {
            "title": "Tailwind CSS Demo - NextPy",
            "description": "Comprehensive Tailwind CSS demonstration in NextPy"
        }
    }
