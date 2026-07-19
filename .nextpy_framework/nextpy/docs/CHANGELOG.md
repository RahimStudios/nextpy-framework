# Changelog

All notable changes to NextPy will be documented in this file.

## [2.0.0] - 2025-01-19

### 🎉 MAJOR RELEASE - Complete React.js Experience in Python!

### Added
- **🎯 True JSX Syntax (NEW!)**
  - Write exact Next.js JSX syntax in Python: `<div>Hello</div>`
  - Full HTML tag support with attributes and event handlers
  - Automatic transformation to valid Python
  - Event handling with onClick, onChange, onSubmit, etc.
  - Component composition with children and props

- **🎣 React-Like Hooks (NEW!)**
  - `useState` - State management: `[count, setCount] = useState(0)`
  - `useEffect` - Side effects and lifecycle management
  - `useReducer` - Complex state management with reducers
  - `useContext` - Global state sharing with context API
  - `useRef` - Mutable references for DOM access
  - `useMemo` - Memoized expensive calculations
  - `useCallback` - Memoized function references
  - `@with_hooks` decorator for hook integration

- **🎨 Custom Hooks (NEW!)**
  - `useCounter` - Counter with increment/decrement functions
  - `useToggle` - Boolean state toggle
  - `useLocalStorage` - Persistent storage with localStorage
  - `useFetch` - API data fetching with loading/error states
  - `useDebounce` - Debounced values for search inputs

- **🎉 Demo Mode (NEW!)**
  - Beautiful built-in documentation when no project exists
  - Automatic demo mode activation: `nextpy dev` works anywhere
  - Professional landing page with NextPy showcase
  - Component demonstrations with live examples
  - Hooks tutorials and API reference
  - Project creation interface
  - Complete documentation hub

- **🧩 Complete Component Library (NEW!)**
  - **50+ Pre-built Components** for rapid development
  - **Form Components**: Input, TextArea, Select, Checkbox, Radio, Form, FormGroup, FileInput, NumberInput, DateInput, TimeInput, PasswordInput, RangeInput, ColorInput, SubmitButton
  - **UI Components**: Button, Badge, Avatar, Icon, Alert, Progress, Skeleton, Tooltip, Chip, Breadcrumb, Table, Code, Blockquote
  - **Layout Components**: Container, Grid, Flex, Stack, Sidebar, MainContent, Section, Article, Header, Footer, Navigation, Center, Spacer, Divider, AspectRatio, Card
  - **Navigation Components**: Navbar, Sidebar, Menu, Dropdown, Tabs, Pagination, SearchBar, BreadcrumbNav

- **📚 Comprehensive Documentation (NEW!)**
  - Complete README.md with all features and examples
  - Step-by-step TODO_APP_TUTORIAL.md tutorial
  - HOOKS_GUIDE_COMPLETE.md with all hooks documentation
  - DEMO_MODE_GUIDE.md for demo mode features
  - PROJECT_SUMMARY.md with implementation overview
  - Reusable components documentation
  - Default export pattern explanation

- **🏗️ Enhanced Framework Structure**
  - Updated project structure with components/ directory
  - JSX preprocessing system with true_jsx.py
  - Component router for JSX rendering
  - Demo router for built-in pages
  - Enhanced hooks provider integration
  - Improved import system and exports

### Enhanced
- **🎯 Multiple Syntax Styles**
  - True JSX Syntax (Recommended): `<div>Hello</div>`
  - Component Style: `div({}, 'Hello')`
  - Template Style: Jinja2 templates (Traditional)
  - Seamless switching between syntax styles

- **🔧 Improved Import System**
  - Clean imports from `nextpy` package
  - Proper component library organization
  - Fixed circular import issues
  - Better error messages for missing imports

- **📱 Enhanced Development Experience**
  - Better error handling and debugging
  - Improved hot reload functionality
  - Enhanced component rendering pipeline
  - Better state management integration

### Fixed
- **🐛 Import Issues**
  - Fixed circular imports in components
  - Resolved hooks import problems
  - Fixed JSX element imports
  - Corrected component library imports

- **🔧 Framework Stability**
  - Fixed hooks state management
  - Resolved component rendering issues
  - Fixed demo mode routing
  - Improved error handling

- **📦 Package Structure**
  - Removed duplicate files and components
  - Cleaned up unused test files
  - Organized documentation properly
  - Fixed package exports

### Breaking Changes
- **🔄 Import Changes**
  - Updated import paths for components
  - Changed hooks import structure
  - Modified JSX element imports
  - Updated package exports

- **🏗️ Structure Changes**
  - New components/ directory structure
  - Updated framework organization
  - Modified routing system
  - Enhanced hooks integration

### Migration Guide
```python
# Old way (v1.x)
from nextpy.components import Button
from nextpy.hooks_new import useState

# New way (v2.0)
from nextpy import Button, useState
from nextpy import useState, useEffect, with_hooks

# New JSX syntax (v2.0)
@with_hooks
def MyComponent():
  [count, setCount] = useState(0)
  return <div>Count: {count}</div>
```

## [1.1.1] - 2024-12-15

### Added
- **🎨 Enhanced Components**
  - New form validation components
  - Improved button variants and sizes
  - Enhanced card component with more options
  - Better navigation components

- **🔧 Framework Improvements**
  - Better error handling in development
  - Improved hot reload performance
  - Enhanced static file serving
  - Better template inheritance

### Fixed
- **🐛 Bug Fixes**
  - Fixed routing issues with dynamic segments
  - Resolved template rendering problems
  - Fixed component import issues
  - Better error messages

## [1.1.0] - 2024-12-01

### Added
- **🎨 Component Library Expansion**
  - 20+ new components added
  - Form validation with Pydantic models
  - Enhanced styling options
  - Better component documentation

- **🔧 Framework Features**
  - Middleware support system
  - Enhanced template inheritance
  - Better HTMX integration
  - Improved static file serving

### Enhanced
- **📱 Development Experience**
  - Better error messages
  - Improved hot reload
  - Enhanced debugging tools
  - Better component organization

## [1.0.0] - 2024-11-29

### Added
- **🏗️ Core Framework**
  - File-based routing with dynamic segments `[slug]` and catch-all `[...path]`
  - Server-side rendering (SSR) with `get_server_side_props`
  - Static site generation (SSG) with `get_static_props`
  - Incremental static regeneration (ISR) with revalidation intervals
  - API routes with full HTTP method support (GET, POST, PUT, DELETE, PATCH)
  
- **🎨 Components**
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
  
- **⚡ Features**
  - Hot reload indicator with visual feedback
  - Debug panel for development errors
  - SEO utilities and structured data generation
  - Form validation with Pydantic models
  - Middleware support system
  - Template inheritance with Jinja2
  - HTMX integration for SPA-like experience
  - Static file serving
  
- **🛠️ CLI Tools**
  - `nextpy dev` - Development server with hot reload
  - `nextpy build` - Static site generation
  - `nextpy start` - Production server
  - `nextpy create` - Project scaffolding
  - `nextpy routes` - Route listing
  
- **📚 Documentation**
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

### Added
- Initial framework concept
- Basic routing system
- Template rendering
- Development server
- Project scaffolding

---

## 🎉 Version 2.0.0 Highlights

**NextPy 2.0.0 represents a complete transformation** from a traditional Python web framework to a **React.js-like experience in Python**:

### 🚀 **What's New in 2.0.0:**
- **🎯 True JSX Syntax** - Write `<div>Hello</div>` directly in Python
- **🎣 React-Like Hooks** - useState, useEffect, useReducer, useContext, useRef, useMemo, useCallback
- **🎨 50+ Components** - Complete UI component library
- **🎉 Demo Mode** - Built-in documentation and examples
- **📚 Comprehensive Docs** - Tutorials, guides, and API reference
- **🧩 Reusable Components** - Component-based architecture
- **🏗️ Enhanced Structure** - Better organization and imports

### 🎯 **Developer Experience:**
```python
# React.js Developer? This feels exactly like home!
@with_hooks
def Counter():
  [count, setCount] = useState(0)
  
  useEffect(() => {
    print(f'Count: {count}')
  }, [count])
  
  return (
    <div>
      <h1>Count: {count}</h1>
      <Button onClick={() => setCount(count + 1)}>Increment</Button>
    </div>
  );
```

### 🚀 **Zero-Friction Onboarding:**
```bash
pip install nextpy-framework
nextpy dev  # Works anywhere - no project needed!
# Shows beautiful demo pages with documentation
```

**NextPy 2.0.0: The exact Next.js experience, now in Python!** 🎉
