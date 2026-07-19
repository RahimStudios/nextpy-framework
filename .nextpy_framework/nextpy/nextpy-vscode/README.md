# NextPy VS Code Extension

## 🚀 **Complete NextPy Development Support**

This VS Code extension provides **perfect development experience** for NextPy projects with:

- ✅ **Python IntelliSense** in `.py.jsx` files
- ✅ **JSX syntax highlighting** for components
- ✅ **No red errors** on JSX syntax
- ✅ **Auto-completion** for NextPy components
- ✅ **Hover documentation** for components and hooks
- ✅ **Emmet support** for HTML in Python

## 📁 **Project Structure**

```
nextpy-vscode/
├─ client/                  # VS Code extension client
│  ├─ package.json          # Extension manifest
│  ├─ src/
│  │  ├─ extension.ts       # Main extension entry point
│  │  ├─ language-configuration.json
│  │  └─ syntaxes/
│  │     └─ nextpy.tmLanguage.json
│  └─ tsconfig.json
│
├─ server/                  # NextPy Language Server
│  ├─ package.json          # LSP dependencies
│  ├─ src/
│  │  └─ server.ts          # Language server implementation
│  └─ tsconfig.json
│
└─ README.md
```

## 🔧 **Installation**

### **Development Mode**
```bash
cd nextpy-vscode/client
npm install
npm run compile

cd ../server  
npm install
npm run compile

# Package extension
vsce package
```

### **Install Extension**
```bash
# Install from .vsix file
code --install-extension nextpy-vscode-0.1.0.vsix
```

## 🎯 **Features**

### **1. Language Support**
- **File associations**: `.py.jsx` → NextPy language
- **Syntax highlighting**: JSX tags, Python code, strings
- **Auto-completion**: Components, hooks, attributes
- **Hover docs**: Component documentation on hover

### **2. IntelliSense Integration**
- **Python completion**: Via Jedi language server
- **NextPy components**: Button, Card, Modal, Input, etc.
- **JSX attributes**: className, onClick, onChange
- **Tailwind classes**: Common utility classes

### **3. Error Suppression**
- **No red squiggles** on JSX syntax
- **Python validation** only for actual Python code
- **JSX validation** for proper tag structure

## 🚀 **Usage**

### **Create NextPy Component**
```python
# components/Button.py.jsx
def Button(props = None):
    return (
        <button className="btn btn-primary">
            {props.text}
        </button>
    )
```

### **Get Auto-Completion**
- Type `Bu` → `Button` completion
- Type `cla` → `className` completion  
- Type `onC` → `onClick` completion

### **Hover Documentation**
- Hover over `Button` → See component props
- Hover over `useState` → See hook usage

## 🔧 **Configuration**

```json
{
  "nextpy.enableIntelliSense": true,
  "nextpy.enableJSXHighlighting": true,
  "nextpy.formatter": "black"
}
```

## 🎉 **Benefits**

- **No more red errors** on JSX syntax
- **Full IntelliSense** for Python and JSX
- **Professional development** experience
- **Auto-completion** for NextPy components
- **Hover documentation** for learning
- **Emmet expansion** in JSX

**Perfect NextPy development setup!** 🚀
