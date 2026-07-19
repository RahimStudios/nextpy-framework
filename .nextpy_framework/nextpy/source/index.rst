NextPy - Complete Documentation
================================

Welcome to the NextPy framework documentation!
This documentation covers everything from installation to advanced usage.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started
   file_routing
   pages_data_fetching
   api_routes
   database_integration
   authentication
   components_templates
   built_in_utilities
   configuration
   deployment
   api_reference

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

---

Getting Started
===============

Installation
------------

.. code-block:: bash

   pip install nextpy-framework
   nextpy create my-app
   cd my-app
   nextpy dev

Visit `http://localhost:5000` - your app runs with hot reload!

Project Structure
-----------------

.. code-block::

   my-app/
   ├── pages/                      
   │   ├── index.py               
   │   ├── about.py               
   │   ├── blog/
   │   │   ├── index.py          
   │   │   └── [slug].py         
   │   └── api/
   │       ├── posts.py          
   │       ├── posts.py (POST)   
   │       └── users/[id].py     
   ├── templates/
   │   ├── _base.html            
   │   ├── index.html            
   │   └── components/
   │       ├── button.html       
   │       ├── card.html
   │       └── modal.html
   ├── models/                    
   │   └── user.py
   ├── nextpy.config.py          
   ├── main.py                   
   └── .env                      

File-Based Routing
=================

Basic Routes
------------

Files in `pages/` automatically become HTTP routes:

+----------------------+-----------------+
| File                 | Route           |
+======================+=================+
| `pages/index.py`     | `/`             |
| `pages/about.py`     | `/about`        |
| `pages/blog/index.py`| `/blog`         |
| `pages/contact.py`   | `/contact`      |

Dynamic Routes
--------------

Use `[param]` for dynamic segments:

.. code-block:: python

   # pages/blog/[slug].py
   def get_template():
       return "blog/post.html"

   async def get_server_side_props(context):
       slug = context["params"]["slug"]
       post = await fetch_post(slug)
       return {"props": {"post": post}}

Catch-All Routes
----------------

Use `[...path]` to capture multiple segments:

.. code-block:: python

   # pages/docs/[...path].py
   async def get_server_side_props(context):
       path = context["params"]["path"]
       page = await get_docs(path)
       return {"props": {"page": page}}

Pages & Data Fetching
=====================

Basic Page
----------

.. code-block:: python

   # pages/hello.py
   def get_template():
       return "hello.html"

   async def get_server_side_props(context):
       return {
           "props": {
               "name": "NextPy",
               "year": 2025
           }
       }

Template (`templates/hello.html`):

.. code-block:: html

   {% extends "_base.html" %}
   {% block content %}
   <h1>Hello {{ name }}!</h1>
   <p>Year: {{ year }}</p>
   {% endblock %}

Server-Side Rendering (SSR)
---------------------------

Data fetched **per request**:

.. code-block:: python

   async def get_server_side_props(context):
       data = await fetch_from_database()
       return {"props": {"data": data}, "revalidate": 60}

Static Generation (SSG)
-----------------------

.. code-block:: python

   async def get_static_props():
       posts = await get_all_posts()
       return {"props": {"posts": posts}, "revalidate": 3600}

   async def get_static_paths():
       posts = await get_all_posts()
       return ["/blog/" + post.slug for post in posts]

API Routes
==========

Basic GET Request
-----------------

.. code-block:: python

   # pages/api/posts.py
   async def get(request):
       posts = await fetch_posts()
       return {"posts": posts}

POST Request
------------

.. code-block:: python

   # pages/api/posts.py
   from pydantic import BaseModel

   class CreatePost(BaseModel):
       title: str
       content: str

   async def post(request):
       body = await request.json()
       post = CreatePost(**body)
       new_post = await save_post(post)
       return {"id": new_post.id, "title": new_post.title}, 201

Dynamic API Routes
-----------------

.. code-block:: python

   # pages/api/posts/[id].py
   async def get(request):
       post_id = request.path_params["id"]
       post = await fetch_post(post_id)
       if not post:
           return {"error": "Not found"}, 404
       return {"post": post}

Database Integration
====================

Setup
-----

.. code-block:: python

   from nextpy.db import engine, Base, Session
   from sqlalchemy import Column, String, Integer, DateTime
   from datetime import datetime

   class User(Base):
       __tablename__ = "users"
       id = Column(Integer, primary_key=True)
       name = Column(String(255))
       email = Column(String(255), unique=True)
       created_at = Column(DateTime, default=datetime.utcnow)

Configuration
-------------

.. code-block:: ini

   DATABASE_URL=sqlite:///app.db
   # or PostgreSQL / MySQL URLs

Authentication
==============

JWT Authentication
------------------

.. code-block:: python

   # pages/api/login.py
   from nextpy.auth import AuthManager
   from pydantic import BaseModel

   class LoginRequest(BaseModel):
       username: str
       password: str

   async def post(request):
       body = await request.json()
       data = LoginRequest(**body)
       user = await verify_user(data.username, data.password)
       if not user:
           return {"error": "Invalid credentials"}, 401
       token = AuthManager.create_token(user_id=user.id, expires_in=3600)
       return {"token": token}

Components & Templates
=====================

Built-in Components
------------------

.. code-block:: html

   {% from 'components/button.html' import button %}
   {{ button('Click me', href='/page', disabled=False, variant='primary') }}

Configuration
=============

Environment Variables
---------------------

.. code-block:: ini

   DATABASE_URL=sqlite:///app.db
   DEBUG=True
   SECRET_KEY=your-secret-key

Deployment
==========

Build & Start
-------------

.. code-block:: bash

   nextpy build
   nextpy start

API Reference
=============

.. code-block:: python

   async def get_server_side_props(context):
       return {"props": {"key": "value"}, "revalidate": 60}

CLI Commands
============

.. code-block:: bash

   nextpy create my-app
   nextpy dev
   nextpy build
   nextpy start
   nextpy create page my-page
   nextpy routes

Resources
=========

- GitHub: `https://github.com/IBRAHIMFONYUY/nextpy-framework`
- Community Discord: Join the NextPy community
- Tutorials and Blog: Visit our blog for tutorials and updates