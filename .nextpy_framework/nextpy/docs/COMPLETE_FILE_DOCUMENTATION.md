# NextPy Framework - Complete File Documentation

**Documentation Date:** October 22, 2026  
**Framework Version:** 5.0.0

---

## Root Directory Files

### main.py (2,731 bytes)
**Purpose:** Application entry point  
**Functions:** Initializes framework, compiles Tailwind CSS, starts uvicorn server on port 5000  
**Related:** `server/app.py`, `db.py`, `package.json`

### README.md (3,628 bytes)
**Purpose:** Project documentation  
**Functions:** Getting started guide, installation, basic PSX example  
**Related:** `FRAMEWORK_ANALYSIS.md`, `CONTRIBUTING.md`

### FRAMEWORK_ANALYSIS.md (~50,000 bytes)
**Purpose:** Framework analysis  
**Functions:** Feature comparison, development roadmap, Next.js parity assessment  
**Related:** All framework files

### CONTRIBUTING.md (4,326 bytes)
**Purpose:** Contribution guidelines  
**Functions:** Coding standards, PR process, community guidelines

### pyproject.toml (1,937 bytes)
**Purpose:** Python package configuration  
**Functions:** Package metadata, dependencies, build system, CLI entry point  
**Related:** `requirements.txt`

### requirements.txt (343 bytes)
**Purpose:** Runtime dependencies  
**Functions:** Lists FastAPI, Uvicorn, Jinja2, SQLAlchemy, etc.

### requirements-dev.txt (75 bytes)
**Purpose:** Development dependencies  
**Functions:** Testing and linting tools

### package.json (818 bytes)
**Purpose:** Node.js dependencies for Tailwind  
**Functions:** Tailwind build scripts, PostCSS configuration  
**Related:** `tailwind.config.js`

### Dockerfile (1,162 bytes)
**Purpose:** Docker container configuration  
**Functions:** Multi-stage build, Python dependencies, health checks  
**Related:** `requirements.txt`

### render.yaml (788 bytes)
**Purpose:** Render.com deployment  
**Functions:** Web service config, build commands, PostgreSQL  
**Related:** `Procfile`

### Procfile (50 bytes)
**Purpose:** Heroku process configuration  
**Functions:** Web process command with PORT variable

### Makefile (859 bytes)
**Purpose:** Build automation  
**Functions:** Sphinx docs, Tailwind build targets

### .gitignore (532 bytes)
**Purpose:** Git ignore patterns  
**Functions:** Excludes cache, node_modules, build artifacts

### .readthedocs.yaml (597 bytes)
**Purpose:** ReadTheDocs configuration  
**Functions:** Documentation build, Python version

### nextpy-plugins.json (368 bytes)
**Purpose:** Plugin configuration  
**Functions:** Plugin registry and settings

### run_server.py (68 bytes)
**Purpose:** Quick server startup  
**Functions:** Simple server launch for development

### app.db (32,768 bytes)
**Purpose:** SQLite database  
**Functions:** Application data storage, User/Post tables  
**Related:** `db.py`

### nextpy.db (32,768 bytes)
**Purpose:** Framework database  
**Functions:** Framework caching and metadata

### styles.css (59 bytes)
**Purpose:** Tailwind source  
**Functions:** Tailwind CSS directives  
**Related:** `tailwind.config.js`

---

## Framework Core Files (.nextpy_framework/nextpy/)

### __init__.py (6,200 bytes)
**Purpose:** Main framework exports  
**Functions:** Exports all public API, PSX system, routing, hooks  
**Related:** All framework modules

### ast_parser.py (14,505 bytes)
**Purpose:** AST-based expression parser  
**Functions:** Safe expression evaluation, AST to IR conversion  
**Related:** `psx/core/evaluator.py`

### auth.py (2,973 bytes)
**Purpose:** Authentication  
**Functions:** JWT tokens, sessions, @require_auth decorator  
**Related:** `config.py`, `db.py`

### builder.py (3,960 bytes)
**Purpose:** Build system  
**Functions:** Build caching, parallel building, bundle analysis  
**Related:** `cli.py`

### cli.py (97,638 bytes)
**Purpose:** Command-line interface  
**Functions:** `nextpy` command, hot reload, dev server, AI assistant  
**Related:** `dev_server.py`, `builder.py`

### components.py (8,094 bytes)
**Purpose:** Legacy component system  
**Functions:** Component utilities, registration  
**Related:** `components/`

### conf.py (940 bytes)
**Purpose:** Configuration management  
**Functions:** Loads environment variables  
**Related:** `config.py`

### config.py (2,202 bytes)
**Purpose:** Application settings  
**Functions:** JWT, database, security settings  
**Related:** `conf.py`, `auth.py`

### db.py (3,617 bytes)
**Purpose:** Database layer  
**Functions:** SQLAlchemy ORM, connection pooling, User/Post models  
**Related:** `main.py`, `auth.py`

### dev_server.py (2,214 bytes)
**Purpose:** Development server  
**Functions:** Hot reload, auto-restart, debug mode  
**Related:** `cli.py`

### dev_tools.py (4,380 bytes)
**Purpose:** Development tools  
**Functions:** Debug helpers, performance tools  
**Related:** `debug/`

### errors.py (1,474 bytes)
**Purpose:** Error handling  
**Functions:** Custom error classes, exception formatting  
**Related:** `server/app.py`

### hooks.py (12,747 bytes)
**Purpose:** React-style hooks  
**Functions:** useState, useEffect, useContext, custom hooks  
**Related:** `psx/components/component.py`

### hooks_provider.py (3,474 bytes)
**Purpose:** Hooks context provider  
**Functions:** Provides hooks context to components  
**Related:** `hooks.py`

### jsx.py (6,646 bytes)
**Purpose:** Legacy JSX support  
**Functions:** JSX parsing and transformation  
**Related:** `jsx_preprocessor.py`

### jsx_preprocessor.py (16,346 bytes)
**Purpose:** JSX preprocessing  
**Functions:** Converts JSX to Python  
**Related:** `jsx.py`

### jsx_transformer.py (3,004 bytes)
**Purpose:** JSX transformation  
**Functions:** Transforms JSX to Python code  
**Related:** `jsx_preprocessor.py`

### main.py (2,567 bytes)
**Purpose:** Framework main module  
**Functions:** Framework initialization, setup  
**Related:** `main.py` (root)

### performance.py (2,313 bytes)
**Purpose:** Performance monitoring  
**Functions:** Metrics collection, timing utilities  
**Related:** `debug/performance.py`

### plugins.py (1,452 bytes)
**Purpose:** Plugin system  
**Functions:** Plugin loading and management  
**Related:** `nextpy-plugins.json`

### security.py (7,085 bytes)
**Purpose:** Security functions  
**Functions:** XSS protection, input sanitization, CSP headers  
**Related:** `ast_parser.py`, `server/app.py`

### websocket.py (9,361 bytes)
**Purpose:** WebSocket support  
**Functions:** Connection manager, pub/sub, state sync  
**Related:** `server/app.py`

### true_jsx.py (10,043 bytes)
**Purpose:** True JSX implementation  
**Functions:** Alternative JSX implementation  
**Related:** `jsx.py`

### .env.example (584 bytes)
**Purpose:** Environment template  
**Functions:** Example environment variables  
**Related:** `config.py`

### package.json (818 bytes)
**Purpose:** Framework Node.js deps  
**Functions:** Tailwind dependencies, build scripts  
**Related:** `tailwind.config.js`

### postcss.config.js (94 bytes)
**Purpose:** PostCSS configuration  
**Functions:** PostCSS plugins, Tailwind integration  
**Related:** `tailwind.config.js`

### tailwind.config.js (4,664 bytes)
**Purpose:** Tailwind configuration  
**Functions:** Theme, colors, fonts, content paths  
**Related:** `postcss.config.js`

### styles.css (59 bytes)
**Purpose:** Framework Tailwind source  
**Functions:** Tailwind directives  
**Related:** `tailwind.config.js`

---

## PSX System Files (.nextpy_framework/nextpy/psx/)

### __init__.py (5,859 bytes)
**Purpose:** PSX exports  
**Functions:** Exports all PSX functionality  
**Related:** All PSX modules

### core/parser.py (31,891 bytes)
**Purpose:** PSX parser  
**Functions:** Parses PSX syntax, converts to AST  
**Related:** `core/ast_nodes.py`, `core/runtime.py`

### core/ast_nodes.py (11,014 bytes)
**Purpose:** AST node definitions  
**Functions:** Defines AST node types, parser, validator  
**Related:** `core/parser.py`

### core/evaluator.py (15,075 bytes)
**Purpose:** Expression evaluator  
**Functions:** Safe expression evaluation  
**Related:** `core/parser.py`

### core/runtime.py (48,723 bytes)
**Purpose:** PSX runtime  
**Functions:** Executes PSX, processes Python logic, component registry  
**Related:** `core/parser.py`, `components/component.py`

### vdom/vnode.py (19,243 bytes)
**Purpose:** Virtual DOM  
**Functions:** VNode, create_element, render, update  
**Related:** `core/runtime.py`

### components/component.py (84,423 bytes)
**Purpose:** Component system  
**Functions:** @component decorator, state management, hooks  
**Related:** `core/runtime.py`, `vdom/vnode.py`

### hydration/__init__.py (668 bytes)
**Purpose:** Hydration exports  
**Functions:** Exports hydration functionality  
**Related:** `hydration/engine.py`

### hydration/engine.py (14,784 bytes)
**Purpose:** Hydration engine  
**Functions:** Client-side hydration, state sync  
**Related:** `hydration/decorators.py`

### hydration/decorators.py (53,736 bytes)
**Purpose:** Hydration decorators  
**Functions:** @interactive_component, hydration integration  
**Related:** `hydration/engine.py`

### hydration/integration.py (9,920 bytes)
**Purpose:** Hydration integration  
**Functions:** Server-side integration, runtime generation  
**Related:** `hydration/engine.py`

### runtime/js_actions_runtime.py
**Purpose:** JavaScript runtime  
**Functions:** Client-side JS runtime, event handling  
**Related:** `hydration/decorators.py`

### runtime/actions_runtime.py
**Purpose:** Actions runtime  
**Functions:** Action handling, event processing  
**Related:** `js_actions_runtime.py`

---

## Component Library Files (.nextpy_framework/nextpy/components/)

### __init__.py (2,862 bytes)
**Purpose:** Component exports  
**Functions:** Exports all built-in components  
**Related:** All component files

### feedback.py (5,950 bytes)
**Purpose:** Feedback components  
**Functions:** Alerts, notifications  
**Related:** `toast.py`

### form.py (11,965 bytes)
**Purpose:** Form components  
**Functions:** Form inputs, validation  
**Related:** `ui.py`

### head.py (6,007 bytes)
**Purpose:** Head/SEO component  
**Functions:** Meta tags, SEO optimization  
**Related:** `server/app.py`

### hooks_provider.py (1,879 bytes)
**Purpose:** Hooks provider  
**Functions:** Provides hooks context  
**Related:** `hooks_provider.py`

### image.py (6,196 bytes)
**Purpose:** Image component  
**Functions:** Image optimization, responsive images  
**Related:** `public/images/`

### layout.py (7,414 bytes)
**Purpose:** Layout components  
**Functions:** Layout containers, children handling  
**Related:** `pages/layout.psx`

### link.py (4,032 bytes)
**Purpose:** Link component  
**Functions:** Navigation links, client-side routing  
**Related:** `navigation.py`

### loader.py (2,019 bytes)
**Purpose:** Loading components  
**Functions:** Spinners, skeleton screens  
**Related:** `ui.py`

### navigation.py (13,829 bytes)
**Purpose:** Navigation components  
**Functions:** Menus, breadcrumbs, active state  
**Related:** `link.py`

### toast.py (2,471 bytes)
**Purpose:** Toast notifications  
**Functions:** Notification system  
**Related:** `feedback.py`

### ui.py (13,605 bytes)
**Purpose:** UI components  
**Functions:** Buttons, cards, modals  
**Related:** `form.py`

### visual.py (7,434 bytes)
**Purpose:** Visual components  
**Functions:** Graphics, charts, data viz  
**Related:** `ui.py`

### debug/AutoDebug.py
**Purpose:** Auto debugging  
**Functions:** Debug UI, overlays  
**Related:** `debug/`

### debug/AutoDebug_v3.py
**Purpose:** Auto debugging v3  
**Functions:** Enhanced debug UI  
**Related:** `debug/`

### debug/DebugIcon.py
**Purpose:** Debug icon  
**Functions:** Debug icon component  
**Related:** `debug/`

### debug/DebugIconFixed.py
**Purpose:** Fixed debug icon  
**Functions:** Fixed debug icon  
**Related:** `debug/`

---

## Core System Files (.nextpy_framework/nextpy/core/)

### __init__.py (491 bytes)
**Purpose:** Core exports  
**Functions:** Exports router, renderer, data fetching  
**Related:** All core modules

### router.py (14,394 bytes)
**Purpose:** File-based routing  
**Functions:** Static/dynamic routes, API routes, layouts  
**Related:** `component_router.py`, `server/app.py`

### component_router.py (27,184 bytes)
**Purpose:** Component routing  
**Functions:** Component-based routing, special files  
**Related:** `router.py`, `component_renderer.py`

### renderer.py (20,311 bytes)
**Purpose:** Template rendering  
**Functions:** Jinja2 integration, PSX rendering, layouts  
**Related:** `server/app.py`, `component_renderer.py`

### component_renderer.py (42,531 bytes)
**Purpose:** Component rendering  
**Functions:** PSX component rendering, state management  
**Related:** `renderer.py`, `psx/components/component.py`

### data_fetching.py (8,094 bytes)
**Purpose:** Data fetching  
**Functions:** SSR, SSG, getStaticPaths  
**Related:** `server/app.py`

### builder.py (7,979 bytes)
**Purpose:** Build system  
**Functions:** Build optimization, caching  
**Related:** `builder.py`

### demo_router.py (1,855 bytes)
**Purpose:** Demo routing  
**Functions:** Demo mode, built-in pages  
**Related:** `demo_pages_simple.py`

### demo_pages_simple.py (23,878 bytes)
**Purpose:** Demo pages  
**Functions:** Built-in demo content  
**Related:** `demo_router.py`

### sync.py (929 bytes)
**Purpose:** Sync utilities  
**Functions:** State synchronization  
**Related:** `websocket.py`

---

## Server Files (.nextpy_framework/nextpy/server/)

### __init__.py (230 bytes)
**Purpose:** Server exports  
**Functions:** Exports create_app  
**Related:** `app.py`

### app.py (58,490 bytes)
**Purpose:** FastAPI application  
**Functions:** Route handling, middleware, WebSocket, SEO routes  
**Related:** `core/router.py`, `middleware.py`, `websocket.py`

### middleware.py (2,984 bytes)
**Purpose:** Server middleware  
**Functions:** Request/response processing  
**Related:** `app.py`, `security.py`

### debug.py (3,449 bytes)
**Purpose:** Debug server  
**Functions:** Debug endpoints, dev tools  
**Related:** `debug/`

---

## Debug System Files (.nextpy_framework/nextpy/debug/)

### core.py (8,604 bytes)
**Purpose:** Debug core  
**Functions:** Debug state, session management  
**Related:** `ui.py`, `performance.py`

### performance.py (11,771 bytes)
**Purpose:** Performance debugging  
**Functions:** Metrics, profiling  
**Related:** `performance.py`

### ui.py (29,625 bytes)
**Purpose:** Debug UI  
**Functions:** Debug overlay, inspector  
**Related:** `core.py`, `components/debug/`

### websocket.py (14,572 bytes)
**Purpose:** Debug WebSocket  
**Functions:** Real-time debug updates  
**Related:** `websocket.py`

---

## Pages Directory Files

### index.py (22,615 bytes)
**Purpose:** Homepage  
**Functions:** Landing page, showcase  
**Related:** `templates/index.html`

### about.py (230 bytes)
**Purpose:** About page  
**Functions:** About information  
**Related:** `templates/about.html`

### contact.py (304 bytes)
**Purpose:** Contact page  
**Functions:** Contact form  
**Related:** `templates/contact.html`

### features.py (2,391 bytes)
**Purpose:** Features page  
**Functions:** Feature listing  
**Related:** `templates/features.html`

### login.py (1,258 bytes)
**Purpose:** Login page  
**Functions:** Authentication  
**Related:** `templates/login.html`, `auth.py`

### navbar.py (4,115 bytes)
**Purpose:** Navigation bar  
**Functions:** Navigation component  
**Related:** `components/navigation.py`

### search.py (1,010 bytes)
**Purpose:** Search page  
**Functions:** Search interface  
**Related:** `templates/search.html`

### robots.txt.py (871 bytes)
**Purpose:** Robots.txt  
**Functions:** SEO configuration  
**Related:** `server/app.py`

### sitemap.xml.py (2,972 bytes)
**Purpose:** Sitemap  
**Functions:** SEO sitemap  
**Related:** `server/app.py`

### tailwind_demo.py (432 bytes)
**Purpose:** Tailwind demo  
**Functions:** Styling examples  
**Related:** `templates/tailwind_demo.html`

### db_example.py (1,790 bytes)
**Purpose:** Database example  
**Functions:** ORM demonstration  
**Related:** `db.py`

### debug_ssr_test.py (264 bytes)
**Purpose:** SSR debug test  
**Functions:** SSR testing  
**Related:** `templates/debug_ssr_test.html`

### examples.py (303 bytes)
**Purpose:** Examples  
**Functions:** Code examples  
**Related:** `templates/examples.html`

### examples_advanced.py (1,209 bytes)
**Purpose:** Advanced examples  
**Functions:** Complex examples  
**Related:** `templates/examples_advanced.html`

### components-showcase.py (1,675 bytes)
**Purpose:** Component showcase  
**Functions:** Component demos  
**Related:** `templates/components-showcase.html`

### client_component_example.py (4,147 bytes)
**Purpose:** Client component example  
**Functions:** Interactive components  
**Related:** `psx/hydration/`

### test_nested_components.py (1,903 bytes)
**Purpose:** Nested components test  
**Functions:** Component nesting  
**Related:** `psx/components/component.py`

### clean_parser_test.py (2,062 bytes)
**Purpose:** Parser test  
**Functions:** PSX parser testing  
**Related:** `psx/core/parser.py`

### debug_test_enhanced.py (6,821 bytes)
**Purpose:** Enhanced debug test  
**Functions:** Debug system testing  
**Related:** `debug/`

### bind_test.psx (1,413 bytes)
**Purpose:** Data binding test  
**Functions:** Two-way binding  
**Related:** `psx/core/runtime.py`

### condition.psx (6,086 bytes)
**Purpose:** Conditional rendering test  
**Functions:** Logic testing  
**Related:** `psx/core/parser.py`

### eve.psx (156 bytes)
**Purpose:** Event test  
**Functions:** Event handling  
**Related:** `psx/core/runtime.py`

### form.psx (600 bytes)
**Purpose:** Form test  
**Functions:** Form handling  
**Related:** `components/form.py`

### layout.psx (10,461 bytes)
**Purpose:** Layout test  
**Functions:** Layout system  
**Related:** `components/layout.py`

### main.psx (17,592 bytes)
**Purpose:** Main PSX test  
**Functions:** Comprehensive PSX demo  
**Related:** `psx/`

### psx_test.psx (4,653 bytes)
**Purpose:** PSX test  
**Functions:** PSX functionality  
**Related:** `psx/`

### test.psx (889 bytes)
**Purpose:** Simple test  
**Functions:** Basic PSX test  
**Related:** `psx/`

### api/health.py (342 bytes)
**Purpose:** Health check  
**Functions:** Status monitoring  
**Related:** `server/app.py`

### api/contact.py (1,504 bytes)
**Purpose:** Contact API  
**Functions:** Contact submission  
**Related:** `pages/contact.py`

### api/login.py (825 bytes)
**Purpose:** Login API  
**Functions:** Authentication  
**Related:** `auth.py`

### api/posts.py (1,573 bytes)
**Purpose:** Posts API  
**Functions:** Blog CRUD  
**Related:** `db.py`

### api/protected.py (766 bytes)
**Purpose:** Protected API  
**Functions:** Auth required  
**Related:** `auth.py`

### api/users_db.py (1,981 bytes)
**Purpose:** Users API  
**Functions:** User management  
**Related:** `db.py`

### blog/index.py (5,499 bytes)
**Purpose:** Blog index  
**Functions:** Blog listing  
**Related:** `templates/blog/index.html`

### blog/[slug].py (2,348 bytes)
**Purpose:** Blog post  
**Functions:** Dynamic blog post  
**Related:** `db.py`

### blog/getting-started.py (2,973 bytes)
**Purpose:** Getting started guide  
**Functions:** Tutorial  
**Related:** `templates/blog/getting-started.html`

### blog/database-guide.py (5,430 bytes)
**Purpose:** Database guide  
**Functions:** Database tutorial  
**Related:** `db.py`

### documentation/index.py (3,048 bytes)
**Purpose:** Documentation index  
**Functions:** Docs home  
**Related:** `templates/documentation.html`

### documentation/layout.psx (1,102 bytes)
**Purpose:** Documentation layout  
**Functions:** Docs layout  
**Related:** `components/layout.py`

### documentation/components/ (20 files)
**Purpose:** Documentation components  
**Functions:** Comprehensive documentation  
**Related:** `documentation/index.py`

### app/layout.psx
**Purpose:** App router layout  
**Functions:** Root layout  
**Related:** `components/layout.py`

---

## Templates Directory Files

### _base.html (17,754 bytes)
**Purpose:** Base template  
**Functions:** HTML structure, Jinja2 blocks  
**Related:** `core/renderer.py`

### _page.html (545 bytes)
**Purpose:** Page template  
**Functions:** Default page layout  
**Related:** `_base.html`

### _404.html (692 bytes)
**Purpose:** 404 page  
**Functions:** Not found page  
**Related:** `server/app.py`

### _error.html (9,078 bytes)
**Purpose:** Error page  
**Functions:** Error details  
**Related:** `server/app.py`

### index.html (19,291 bytes)
**Purpose:** Homepage template  
**Functions:** Homepage layout  
**Related:** `pages/index.py`

### about.html (12,945 bytes)
**Purpose:** About template  
**Functions:** About layout  
**Related:** `pages/about.py`

### contact.html (1,986 bytes)
**Purpose:** Contact template  
**Functions:** Contact form  
**Related:** `pages/contact.py`

### features.html (771 bytes)
**Purpose:** Features template  
**Functions:** Feature list  
**Related:** `pages/features.py`

### login.html (1,575 bytes)
**Purpose:** Login template  
**Functions:** Login form  
**Related:** `pages/login.py`

### search.html (1,259 bytes)
**Purpose:** Search template  
**Functions:** Search interface  
**Related:** `pages/search.py`

### tailwind_demo.html (6,058 bytes)
**Purpose:** Tailwind demo template  
**Functions:** Styling examples  
**Related:** `pages/tailwind_demo.py`

### tailwind_working.html (1,392 bytes)
**Purpose:** Tailwind working template  
**Functions:** Functional demo  
**Related:** `pages/tailwind_demo.py`

### db_example.html (4,949 bytes)
**Purpose:** Database example template  
**Functions:** ORM demo  
**Related:** `pages/db_example.py`

### debug_ssr_test.html (1,034 bytes)
**Purpose:** SSR debug template  
**Functions:** Debug info  
**Related:** `pages/debug_ssr_test.py`

### examples.html (3,907 bytes)
**Purpose:** Examples template  
**Functions:** Code examples  
**Related:** `pages/examples.py`

### examples_advanced.html (1,620 bytes)
**Purpose:** Advanced examples template  
**Functions:** Complex examples  
**Related:** `pages/examples_advanced.py`

### components-showcase.html (1,985 bytes)
**Purpose:** Component showcase template  
**Functions:** Component display  
**Related:** `pages/components-showcase.py`

### hooks-demo.html (4,500 bytes)
**Purpose:** Hooks demo template  
**Functions:** Hook examples  
**Related:** `hooks.py`

### documentation.html (29,043 bytes)
**Purpose:** Documentation template  
**Functions:** Docs layout  
**Related:** `pages/documentation/index.py`

### robots.txt (371 bytes)
**Purpose:** Robots.txt template  
**Functions:** SEO config  
**Related:** `pages/robots.txt.py`

### sitemap.xml (332 bytes)
**Purpose:** Sitemap template  
**Functions:** SEO sitemap  
**Related:** `pages/sitemap.xml.py`

### blog/ (3 items)
**Purpose:** Blog templates  
**Functions:** Blog layouts  
**Related:** `pages/blog/`

### components/ (16 items)
**Purpose:** Component templates  
**Functions:** Reusable components  
**Related:** `pages/components/`

---

## Public Directory Files

### favicon.ico (196,330 bytes)
**Purpose:** Website favicon  
**Functions:** Browser tab icon  
**Related:** `templates/_base.html`

### tailwind.css (90,437 bytes)
**Purpose:** Compiled Tailwind CSS  
**Functions:** Production styles  
**Related:** `styles.css`, `tailwind.config.js`

### images/ (0 items)
**Purpose:** Image assets  
**Functions:** Static images  
**Related:** `components/image.py`

---

## Summary Statistics

- **Total Python Files:** 100+
- **Total PSX Files:** 11
- **Total Template Files:** 25+
- **Total Configuration Files:** 10+
- **Framework Core Files:** 38
- **PSX System Files:** 15+
- **Component Library:** 13+
- **Server Files:** 4
- **Debug Files:** 4

---

## Key Relationships

**Core Flow:** main.py → server/app.py → core/router.py → core/renderer.py → templates/  
**PSX Flow:** psx/core/parser.py → psx/core/runtime.py → psx/components/component.py → psx/hydration/  
**Data Flow:** Request → server/app.py → core/data_fetching.py → core/renderer.py → Response  
**Build Flow:** cli.py → builder.py → core/builder.py → optimization  
**Debug Flow:** debug/core.py → debug/ui.py → debug/performance.py → debug/websocket.py
