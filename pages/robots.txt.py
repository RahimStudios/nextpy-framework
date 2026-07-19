"""
Robots.txt page for SEO - generates raw robots.txt for search engines
"""

def get_template():
    return "robots.txt"

async def get_server_side_props(context):
    """Generate robots.txt"""
    import os
    from fastapi.responses import Response
    
    # Get base URL from environment or use default
    base_url = os.getenv("FRONTEND_URL", "https://nextpy-framework.onrender.com")
    
    # Generate robots.txt content
    # Note: 'Allow: /' at the top covers all sub-paths unless specifically disallowed.
    robots_content = f"""User-agent: *
Allow: /

# Block common non-content or sensitive paths
Disallow: /api/
Disallow: /_nextpy_debug/
Disallow: /static/
Disallow: *.py$
Disallow: *.html$

# Sitemap location
Sitemap: {base_url}/sitemap.xml
"""
    
    # Return as raw text response
    return Response(content=robots_content, media_type="text/plain")
