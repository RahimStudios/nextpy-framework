# 📁 NextPy Project Structure Guide

## 🎯 **Correct Folder Organization**

### **Framework vs User Project Separation**

It's crucial to understand the separation between the **NextPy framework** and **user projects**:

## 🏗️ **Framework Structure** (`.nextpy_framework/nextpy/`)

This is where the **NextPy framework code** lives. Users should **not** modify these files.

```
.nextpy_framework/nextpy/
├── __init__.py              # Main exports
├── cli.py                   # CLI commands
├── main.py                  # Main entry point
├── hooks.py                 # Built-in hooks
├── jsx.py                   # JSX system
├── jsx_preprocessor.py      # JSX processing
├── true_jsx.py             # True JSX parser
├── components/              # Built-in components
│   ├── __init__.py         # Component exports
│   ├── ui.py               # Basic UI components
│   ├── forms.py            # Form components
│   ├── layout.py           # Layout components
│   ├── navigation.py       # Navigation components
│   └── enhanced.py         # Enhanced components
├── core/                   # Core framework
│   ├── router.py           # Routing system
│   ├── component_router.py # Component rendering
│   ├── renderer.py         # Template rendering
│   └── demo_router.py      # Demo mode
├── plugins/                # Plugin system
│   ├── __init__.py         # Plugin exports
│   ├── base.py             # Base plugin classes
│   ├── builtin.py          # Built-in plugins
│   └── config.py           # Plugin configuration
├── server/                 # Server code
│   └── app.py              # FastAPI application
└── components/             # Framework components
    └── debug/              # Debug system
        ├── AutoDebug.py     # Auto debug system
        ├── DebugIcon.py     # Debug icon
        └── DebugIcon.css    # Debug styles
```

## 📁 **User Project Structure** (when user runs `nextpy create my-app`)

This is where **user code** lives. Users create and modify these files.

```
my-app/
├── pages/                  # ✅ User's pages (file-based routing)
│   ├── index.py           # Homepage (/)
│   ├── about.py           # About page (/about)
│   ├── [slug].py          # Dynamic routes (/:slug)
│   └── api/               # ✅ User's API routes
│       ├── users.py        # (/api/users)
│       └── posts.py        # (/api/posts)
├── components/             # ✅ User's reusable components
│   ├── ui/                # User's UI components
│   │   ├── Button.py       # Custom button
│   │   └── Card.py         # Custom card
│   ├── forms/             # User's form components
│   │   ├── ContactForm.py  # Contact form
│   │   └── SearchForm.py   # Search form
│   ├── layout/            # User's layout components
│   │   ├── Header.py       # Custom header
│   │   ├── Footer.py       # Custom footer
│   │   └── Sidebar.py      # Custom sidebar
│   └── features/          # User's feature components
│       ├── DataTable.py    # Data table
│       └── Chart.py        # Chart component
├── hooks/                  # ✅ User's custom hooks
│   ├── useAuth.py         # Authentication hook
│   ├── useApi.py          # API hook
│   └── useLocalStorage.py # Local storage hook
├── utils/                  # ✅ User's utility functions
│   ├── helpers.py         # Helper functions
│   ├── constants.py       # Constants
│   └── validators.py      # Validation functions
├── types/                  # ✅ User's TypeScript definitions
│   ├── components.d.ts    # Component types
│   ├── hooks.d.ts         # Hook types
│   └── nextpy.d.ts        # NextPy types
├── tests/                  # ✅ User's test files
│   ├── pages/             # Page tests
│   │   ├── test_index.py  # Homepage tests
│   │   └── test_about.py  # About page tests
│   ├── components/         # Component tests
│   │   ├── test_Button.py # Button tests
│   │   └── test_Card.py   # Card tests
│   └── conftest.py       # Pytest configuration
├── docs/                   # ✅ User's documentation
│   ├── components/         # Component docs
│   ├── api/               # API documentation
│   └── guides/            # User guides
├── styles/                 # ✅ User's CSS files
│   ├── globals.css        # Global styles
│   ├── components.css      # Component styles
│   └── utilities.css      # Utility classes
├── public/                 # ✅ User's static files
│   ├── css/               # CSS files
│   ├── js/                # JavaScript files
│   ├── images/            # Images
│   └── icons/             # Icons
├── templates/              # ✅ User's Jinja2 templates (optional)
│   ├── base.html          # Base template
│   └── layout.html        # Layout template
├── .vscode/               # ✅ VS Code configuration
│   ├── settings.json      # Editor settings
│   ├── extensions.json    # Recommended extensions
│   └── launch.json        # Debug configuration
├── .env.example           # Environment variables example
├── .gitignore             # Git ignore file
├── main.py                # ✅ User's application entry point
├── requirements.txt       # ✅ User's Python dependencies
├── package.json           # ✅ User's package configuration
├── tailwind.config.js     # ✅ Tailwind CSS configuration
├── pytest.ini            # ✅ Test configuration
├── .pre-commit-config.yaml # ✅ Pre-commit hooks
└── README.md              # ✅ User's project README
```

## 🚫 **What Should NOT Be in Framework Folder**

These folders should **NEVER** be in `.nextpy_framework/nextpy/`:

```
❌ .nextpy_framework/nextpy/types/     # Should be in user project
❌ .nextpy_framework/nextpy/tests/     # Should be in user project  
❌ .nextpy_framework/nextpy/docs/      # Should be in user project
❌ .nextpy_framework/nextpy/utils/    # Should be in user project
❌ .nextpy_framework/nextpy/hooks/     # User hooks, not framework
❌ .nextpy_framework/nextpy/public/   # Should be in user project
```

## ✅ **What SHOULD Be in Framework Folder**

```
✅ .nextpy_framework/nextpy/components/    # Built-in components
✅ .nextpy_framework/nextpy/core/          # Core framework code
✅ .nextpy_framework/nextpy/plugins/       # Plugin system
✅ .nextpy_framework/nextpy/server/        # Server code
✅ .nextpy_framework/nextpy/cli.py         # CLI commands
✅ .nextpy_framework/nextpy/hooks.py       # Built-in hooks
```

## 🔄 **Import Patterns**

### **User Importing Framework Components**
```python
# ✅ Correct: Import from framework
from nextpy.components import Button, Card
from nextpy import useState, useEffect
from nextpy.hooks import useAuth

# ❌ Wrong: Don't import from user's own components folder
from components.Button import Button  # Only for user's own components
```

### **User Creating Their Own Components**
```python
# ✅ Correct: Create in user's components folder
# components/ui/MyButton.py
def MyButton(props = None):
    return <button>{props.text}</button>

# ✅ Correct: Import user's own component
from components.ui.MyButton import MyButton
```

## 🎯 **CLI Commands and Folder Creation**

### **When User Runs `nextpy create my-app`**
The CLI creates the **user project structure**:

```bash
nextpy create my-app
# Creates:
# my-app/pages/
# my-app/components/
# my-app/types/
# my-app/tests/
# my-app/docs/
# etc.
```

### **When User Runs `nextpy enhance create`**
The enhanced CLI creates **additional user project folders**:

```bash
nextpy enhance create my-app --typescript --testing
# Creates additional:
# my-app/types/
# my-app/tests/
# my-app/docs/
# my-app/hooks/
# my-app/utils/
```

## 📋 **Quick Reference**

| Folder | Location | Purpose |
|--------|----------|---------|
| `pages/` | User Project | File-based routing |
| `components/` | Both | Framework: Built-in, User: Custom |
| `types/` | User Project | TypeScript definitions |
| `tests/` | User Project | Test files |
| `docs/` | User Project | Documentation |
| `hooks/` | Both | Framework: Built-in, User: Custom |
| `utils/` | User Project | Utility functions |
| `public/` | User Project | Static files |
| `core/` | Framework | Core framework code |
| `plugins/` | Framework | Plugin system |
| `server/` | Framework | Server code |

## 🎉 **Summary**

- **Framework folders**: Contain NextPy's core functionality
- **User project folders**: Contain user's application code
- **Never mix**: Don't put user code in framework folders
- **Clear separation**: Framework provides tools, users build applications

This structure ensures:
- ✅ Clean separation of concerns
- ✅ Easy framework updates
- ✅ No conflicts between framework and user code
- ✅ Clear ownership of files
- ✅ Better maintainability
