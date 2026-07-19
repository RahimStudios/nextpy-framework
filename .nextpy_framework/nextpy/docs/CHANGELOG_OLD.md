# Changelog

All notable changes to NextPy will be documented in this file.

## [1.0.0] - 2024-11-29

### Added
- **Core Framework**
  - File-based routing with dynamic segments `[slug]` and catch-all `[...path]`
  - Server-side rendering (SSR) with `get_server_side_props`
  - Static site generation (SSG) with `get_static_props`
  - Incremental static regeneration (ISR) with revalidation intervals
  - API routes with full HTTP method support (GET, POST, PUT, DELETE, PATCH)
  
- **Components**
  - Image component with lazy loading and responsive sizing
  - Link component with HTMX prefetch integration
  - Button component with 5 variants and 3 sizes
  - Card component with featured variant
  - Form components (input, textarea, select)
  - Alert component with 4 types (info, success, warning, error)
  - Navigation bar with HTMX integration
  - Pagination component
  - Modal component
  - Breadcrumb component
  
- **Features**
  - Hot reload indicator with visual feedback
  - Debug panel for development errors
  - SEO utilities and structured data generation
  - Form validation with Pydantic models
  - Middleware support system
  - Template inheritance with Jinja2
  - HTMX integration for SPA-like experience
  - Static file serving
  
- **CLI Tools**
  - `nextpy dev` - Development server with hot reload
  - `nextpy build` - Static site generation
  - `nextpy start` - Production server
  - `nextpy create` - Project scaffolding
  - `nextpy routes` - Route listing
  
- **Documentation**
  - Comprehensive README.md
  - Full DOCUMENTATION.md (600+ lines)
  - API reference
  - Component examples
  - Deployment guides

### Technical
- Built on FastAPI + Uvicorn
- Jinja2 templating engine
- Pydantic for type-safe validation
- Watchdog for file monitoring
- Click for CLI framework
- Tailwind CSS for styling

### Installation
```bash
pip install nextpy-framework
```

## [0.9.0] - Pre-release

### Initial Release
- Experimental version with core routing and rendering

---

## Development

### Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Roadmap
- [ ] Database ORM integration
- [ ] Authentication plugins
- [ ] GraphQL support
- [ ] WebSocket support
- [ ] Caching layer
- [ ] Rate limiting
- [ ] Request/response compression
- [ ] Analytics integration
- [ ] Monitoring & logging
- [ ] Plugin system

---

## Support

- **Issues**: https://github.com/nextpy/nextpy-framework/issues
- **Discussions**: https://github.com/nextpy/nextpy-framework/discussions
- **Documentation**: https://nextpy.dev/docs
