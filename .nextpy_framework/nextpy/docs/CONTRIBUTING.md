# Contributing to NextPy

Thank you for your interest in contributing to NextPy! We welcome contributions of all sizes.

## Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/IBRAHIMFONYUY/nextpy-framework.git
   cd nextpy-framework
   ```

2. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -e .
   pip install -r requirements-dev.txt
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Making Changes

1. Write your code in the appropriate module:
   - **Pages**: `pages/` directory
   - **Components**: `nextpy/components/` or `templates/components/`
   - **Core**: `nextpy/core/` for routing, rendering, data fetching
   - **Server**: `nextpy/server/` for FastAPI app
   - **Utils**: `nextpy/utils/` for helpers

2. Follow code style:
   - Use type hints
   - Write docstrings for functions
   - Format with black
   - Use meaningful variable names

3. Test your changes
   ```bash
   nextpy dev  # Test development server
   nextpy build  # Test static generation
   ```

### Commit Guidelines

Write clear commit messages:
```
feat: Add image optimization component
fix: Resolve hot reload indicator bug
docs: Update README with new examples
chore: Bump dependency versions
```

## Pull Request Process

1. Update README.md if adding new features
2. Update DOCUMENTATION.md with usage examples
3. Write clear PR description explaining:
   - What problem does it solve?
   - How does it work?
   - Any breaking changes?

4. Link related issues:
   ```
   Fixes #123
   Related to #456
   ```

## Code Style

### Python
- Use 4 spaces for indentation
- Format with [black](https://github.com/psf/black)
- Type hints required for new code
- Docstrings for all public functions

```python
async def get_server_side_props(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fetch page data for server-side rendering.
    
    Args:
        context: Request context with params, query, headers
        
    Returns:
        Dictionary with props for template rendering
    """
    data = await fetch_data()
    return {"props": {"data": data}}
```

### Templates (Jinja2)
- Use 2 spaces for indentation
- Use descriptive variable names
- Add comments for complex logic

```html
{# Card component for displaying product #}
{% macro card(title, price, image) %}
<div class="card">
    <img src="{{ image }}" alt="{{ title }}">
    <h3>{{ title }}</h3>
    <p class="price">${{ price }}</p>
</div>
{% endmacro %}
```

## Testing

Create tests in `tests/` directory:

```python
# tests/test_routing.py
async def test_dynamic_route():
    client = TestClient(app)
    response = client.get("/blog/hello-world")
    assert response.status_code == 200
```

Run tests:
```bash
pytest
```

## Documentation

- Update docs for new features in DOCUMENTATION.md
- Add examples in pages/examples.py
- Include docstrings in code

## Reporting Bugs

Create an issue with:
- **Title**: Clear, concise description
- **Description**: Steps to reproduce
- **Expected**: What should happen
- **Actual**: What actually happens
- **Environment**: Python version, OS, etc.

## Feature Requests

Suggest new features by:
1. Checking existing issues first
2. Describing use case
3. Proposing solution or asking for discussion

## Areas for Contribution

### High Priority
- [ ] Database integration (SQLAlchemy, Tortoise)
- [ ] Authentication (JWT, sessions)
- [ ] Testing framework setup
- [ ] Performance optimization
- [ ] Error handling improvements

### Medium Priority
- [ ] GraphQL support
- [ ] WebSocket support
- [ ] Email utilities
- [ ] File upload helpers
- [ ] Caching layer

### Low Priority
- [ ] Additional UI components
- [ ] Example projects
- [ ] Blog posts / tutorials
- [ ] Language translations

## Questions?

- **Documentation**: https://nextpy.dev/docs
- **Discussions**: https://github.com/IBRAHIMFONYUY/nextpy-framework/discussions
- **Discord**: [Join our community](https://discord.gg/nextpy)

---

## License

By contributing, you agree that your contributions will be licensed under the NextPy License.

Thank you for making NextPy better! 🚀

Built with love ❤️ by the NextPy community.
