"""
Sitemap page for SEO - generates raw XML sitemap for Google
"""

def get_template():
    return "sitemap.xml"


async def get_server_side_props(context):
    """Generate sitemap with all important pages"""
    import os
    from datetime import datetime
    from fastapi.responses import Response
    
    # Get base URL from environment or use default
    base_url = os.getenv("FRONTEND_URL", "https://nextpy-framework.onrender.com")
    
    # Define all pages with their priorities and update frequencies
    pages = [
        {
            "loc": f"{base_url}/",
            "lastmod": datetime.now().strftime("%Y-%m-%d"),
            "changefreq": "daily",
            "priority": "1.0"
        },
        {
            "loc": f"{base_url}/documentation",
            "lastmod": datetime.now().strftime("%Y-%m-%d"),
            "changefreq": "weekly",
            "priority": "0.9"
        },
        {
            "loc": f"{base_url}/examples",
            "lastmod": datetime.now().strftime("%Y-%m-%d"),
            "changefreq": "weekly",
            "priority": "0.8"
        },
        {
            "loc": f"{base_url}/features",
            "lastmod": datetime.now().strftime("%Y-%m-%d"),
            "changefreq": "weekly",
            "priority": "0.8"
        },
        {
            "loc": f"{base_url}/about",
            "lastmod": datetime.now().strftime("%Y-%m-%d"),
            "changefreq": "monthly",
            "priority": "0.7"
        },
        {
            "loc": f"{base_url}/blog",
            "lastmod": datetime.now().strftime("%Y-%m-%d"),
            "changefreq": "weekly",
            "priority": "0.7"
        },
        {
            "loc": f"{base_url}/blog/getting-started",
            "lastmod": datetime.now().strftime("%Y-%m-%d"),
            "changefreq": "monthly",
            "priority": "0.6"
        },
        {
            "loc": f"{base_url}/blog/database-guide",
            "lastmod": datetime.now().strftime("%Y-%m-%d"),
            "changefreq": "monthly",
            "priority": "0.6"
        },
        {
            "loc": f"{base_url}/db_example",
            "lastmod": datetime.now().strftime("%Y-%m-%d"),
            "changefreq": "monthly",
            "priority": "0.5"
        },
        {
            "loc": f"{base_url}/hooks-demo",
            "lastmod": datetime.now().strftime("%Y-%m-%d"),
            "changefreq": "monthly",
            "priority": "0.5"
        }
    ]
    
    # Generate raw XML
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for page in pages:
        xml += f"""  <url>
    <loc>{page['loc']}</loc>
    <lastmod>{page['lastmod']}</lastmod>
    <changefreq>{page['changefreq']}</changefreq>
    <priority>{page['priority']}</priority>
  </url>
"""
    
    xml += '\n</urlset>'
    
    # Return as raw XML response
    return Response(content=xml, media_type="application/xml")
