# NextPy PSX VS Code Extension

🚀 **Complete VS Code extension for NextPy PSX development** with syntax highlighting, IntelliSense, and powerful development tools.

## ✨ Features

### 🎨 **Syntax Highlighting**
- **Complete PSX syntax** - JSX-like syntax in Python
- **Python logic blocks** - `{for}`, `{if}`, `{try}`, `{python}` highlighting
- **Element attributes** - Props, classes, styles, events
- **Embedded Python** - `{expression}` highlighting
- **Comments and documentation** - Full comment support

### 🧠 **IntelliSense & Auto-Completion**
- **PSX elements** - All HTML elements with auto-closing
- **Logic blocks** - `{for}`, `{if}`, `{try}`, `{python}` snippets
- **NextPy components** - `Link`, `Head`, `Fragment`
- **Hooks** - `useState`, `useEffect`, `useMemo`, `useCallback`
- **Event handlers** - onClick, onChange, onSubmit, etc.
- **Props and attributes** - Smart attribute completion

### 🛠️ **Development Tools**
- **Component generator** - Create PSX components instantly
- **Page generator** - Create PSX pages with templates
- **Hover documentation** - Get help with PSX syntax
- **Code snippets** - 20+ ready-to-use snippets
- **Toggle features** - Toggle highlighting options

### 📝 **Code Snippets**
```psx
# Component creation
@component
def MyComponent(props):
    return psx(
        "<div className=\"container\">",
        "    <h1>{props.get('title')}</h1>",
        "</div>"
    )

# Python logic blocks
{for item in items:
    <div key={item}>{item}</div>
}

{if condition:
    <div>Content</div>
}

{try:
    <div>{risky()}</div>
}{except Error as e:
    <div>Error: {e}</div>
}

{python:
    result = complex_calculation()
    return psx("<div>{result}</div>")
}
```

## 🚀 Installation

### From VS Code Marketplace
1. Open VS Code
2. Press `Ctrl+Shift+X` (or `Cmd+Shift+X` on Mac)
3. Search for "NextPy PSX"
4. Click **Install**

### Manual Installation
1. Download the extension from the [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=nextpy-framework.nextpy-psx)
2. Open the downloaded `.vsix` file
3. VS Code will prompt you to install the extension

## 🎯 Usage

### File Associations
The extension automatically associates with:
- `.psx` files - PSX syntax highlighting
- `.py` files - PSX syntax when detected

### Commands
Access commands via `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac):

- **`NextPy PSX: Create PSX Component`** - Generate a new component
- **`NextPy PSX: Create PSX Page`** - Generate a new page
- **`NextPy PSX: Toggle Python Logic Highlighting`** - Toggle logic block highlighting
- **`NextPy PSX: Show PSX Documentation`** - Open documentation

### Context Menu
Right-click on `.py` or `.psx` files:
- **Create PSX Component** - Generate component file
- **Create PSX Page** - Generate page file

### Key Bindings
- `Ctrl+Shift+P` - Toggle Python logic highlighting (when in PSX file)

## ⚙️ Settings

Configure the extension in VS Code settings:

```json
{
  "nextpyPsx.enableSyntaxHighlighting": true,
  "nextpyPsx.enableIntelliSense": true,
  "nextpyPsx.enableFormatting": true,
  "nextpyPsx.pythonLogicHighlighting": true,
  "nextpyPsx.componentSnippets": true
}
```

### Settings Description
- **`enableSyntaxHighlighting`** - Enable PSX syntax highlighting
- **`enableIntelliSense`** - Enable auto-completion and suggestions
- **`enableFormatting`** - Enable code formatting (coming soon)
- **`pythonLogicHighlighting`** - Highlight Python logic blocks
- **`componentSnippets`** - Enable component and page snippets

## 🎨 Syntax Highlighting Examples

### PSX Elements
```psx
<div className="container">
    <h1>Hello World</h1>
    <button onClick={handleClick}>Click me</button>
</div>
```

### Python Logic Blocks
```psx
{for user in users:
    <div key={user.id} className="user-card">
        <h2>{user.name}</h2>
        <p>{user.email}</p>
    </div>
}

{if user.is_active:
    <span className="status active">Active</span>
else:
    <span className="status inactive">Inactive</span>
}

{try:
    <div>{risky_operation()}</div>
}{except Exception as e:
    <div className="error">Error: {e}</div>
}

{python:
    # Complex Python logic
    result = compute_complex_data()
    filtered = filter_list(result, lambda x: x.is_valid)
    return psx("<div>{len(filtered)} items processed</div>")
}
```

### Embedded Python
```psx
<div className="stats">
    <p>Total: {len(items)}</p>
    <p>Active: {sum(1 for item in items if item.active)}</p>
    <p>Score: {calculate_score(items)}</p>
</div>
```

## 🧠 IntelliSense Features

### Auto-Completion
- **HTML Elements**: `<div>`, `<span>`, `<button>`, etc.
- **Logic Blocks**: `{for}`, `{if}`, `{try}`, `{python}`
- **NextPy Components**: `Link`, `Head`, `Fragment`
- **Hooks**: `useState`, `useEffect`, `useMemo`
- **Attributes**: `className`, `onClick`, `onChange`, etc.

### Hover Documentation
Hover over any PSX syntax to see:
- Syntax explanations
- Usage examples
- Best practices

## 📚 Available Snippets

### Components & Pages
- `component` - Create a PSX component
- `page` - Create a PSX page
- `layout` - Create a layout component

### Elements
- `psx` - Basic PSX element
- `form` - Form with inputs
- `list` - List with items
- `link` - NextPy Link component

### Logic Blocks
- `for` - For loop block
- `if` - If condition block
- `try` - Try-catch block
- `python` - Python logic block

### Hooks
- `useState` - State hook
- `useEffect` - Effect hook
- `useMemo` - Memoization hook
- `useCallback` - Callback hook

### Utilities
- `classnames` - Class names utility
- `style` - Inline styles
- `conditional` - Conditional rendering
- `fragment` - Fragment wrapper

## 🔧 Development

### Building the Extension
```bash
# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Watch for changes
npm run watch

# Run tests
npm test
```

### File Structure
```
vscode-extension/
├── src/
│   └── extension.ts          # Main extension file
├── syntaxes/
│   └── nextpy-psx.tmLanguage.json  # Syntax highlighting grammar
├── snippets/
│   └── nextpy-psx.json       # Code snippets
├── package.json              # Extension manifest
├── tsconfig.json            # TypeScript configuration
└── README.md                # This file
```

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Links

- **NextPy Framework**: https://github.com/nextpy-framework/nextpy
- **Documentation**: https://nextpy-framework.github.io/docs
- **Issues**: https://github.com/nextpy-framework/vscode-nextpy-psx/issues
- **VS Code Marketplace**: https://marketplace.visualstudio.com/items?itemName=nextpy-framework.nextpy-psx

## 🎉 Enjoy!

Happy coding with NextPy PSX! 🚀

---

*The NextPy PSX extension brings the power of revolutionary Python JSX syntax to your VS Code editor, making NextPy development faster, more productive, and more enjoyable than ever before!*
