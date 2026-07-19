NextPy - Documentation
=======================

This manual describes the core features and usage of NextPy, a Python web
framework inspired by Next.js. Topics include project setup, routing, data
handling, and deployment.

.. toctree::
   :maxdepth: 2

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

Install the framework, scaffold a project, and start the development server:

.. code-block:: bash

   pip install nextpy-framework
   nextpy create my-app
   cd my-app
   nextpy dev

The server runs at ``http://localhost:8000`` by default with hot reload.

Project Structure
-----------------

A typical project contains the following top-level directories and files:

```
my-app/
├── pages/        # route definitions and components
├── templates/    # Jinja2 templates
├── public/       # static assets (CSS, JS, images)
├── nextpy.config.py  # optional configuration
├── main.py       # application entry point
└── .env          # environment variables
```

Refer to the linked sections above for detailed explanations of routing,
data fetching, APIs, and deployment.
