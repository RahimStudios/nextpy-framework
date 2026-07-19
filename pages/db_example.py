"""
Database Example Page
Shows how to use the built-in database with SQLAlchemy
"""

from nextpy.db import get_session, Post, User
from nextpy.config import settings


def get_template():
    return "db_example.html"


# SYNC STYLE - This works too!
def get_server_side_props_sync(context):
    """Example with sync function"""
    session = get_session()
    try:
        posts = session.query(Post).filter(Post.published == True).limit(5).all()
        users = session.query(User).filter(User.is_active == True).limit(5).all()
        return {
            "props": {
                "posts": [{"id": p.id, "title": p.title, "slug": p.slug} for p in posts],
                "users": [{"id": u.id, "email": u.email, "username": u.username} for u in users],
                "database_url": settings["database_url"],
                "total_posts": session.query(Post).count(),
                "total_users": session.query(User).count(),
            }
        }
    finally:
        session.close()


# ASYNC STYLE - Recommended for production
async def get_server_side_props(context):
    """Example with async function"""
    session = get_session()
    try:
        posts = session.query(Post).filter(Post.published == True).limit(5).all()
        users = session.query(User).filter(User.is_active == True).limit(5).all()
        return {
            "props": {
                "posts": [{"id": p.id, "title": p.title, "slug": p.slug} for p in posts],
                "users": [{"id": u.id, "email": u.email, "username": u.username} for u in users],
                "database_url": settings["database_url"],
                "total_posts": session.query(Post).count(),
                "total_users": session.query(User).count(),
            }
        }
    finally:
        session.close()
