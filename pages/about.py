"""
About page 

"""

def get_template():
    return "about.html"


async def get_server_side_props(context):
    return {
        "props": {
            "title": "About",
            "description": "About Nextpy"
        }
    }
