# 🛠️ VS Code Setup for NextPy

## 📁 VS Code Settings File

I've created `vscode-settings-recommended.json` with comprehensive settings for NextPy development.

### 🚀 How to Use

1. **Copy the settings**:
   ```bash
   cp vscode-settings-recommended.json ~/.vscode/settings.json
   ```

2. **Or manually copy** these key settings to your VS Code settings:

## 🎯 **Essential NextPy Settings**

### **Python Configuration**
```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.analysis.typeCheckingMode": "basic",
  "python.analysis.autoImportCompletions": true
}
```

### **File Associations**
```json
{
  "files.associations": {
    "*.py": "python",
    "*.jsx": "javascriptreact"
  }
}
```

### **Emmet Support for JSX**
```json
{
  "emmet.includeLanguages": {
    "python": "html"
  },
  "emmet.triggerExpansionOnTab": true
}
```

### **Formatting**
```json
{
  "editor.formatOnSave": true,
  "python.formatting.provider": "black",
  "python.linting.enabled": true
}
```

### **Tailwind CSS**
```json
{
  "tailwindCSS.includeLanguages": {
    "python": "html"
  }
}
```

## 📦 **Required Extensions**

Create `.vscode/extensions.json`:
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "bradlc.vscode-tailwindcss",
    "esbenp.prettier-vscode",
    "ms-python.black-formatter",
    "formulahendry.auto-rename-tag",
    "christian-kohler.path-intellisense"
  ]
}
```

## 🔧 **Language-Specific Settings**

### **Python**
```json
{
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true,
    "editor.rulers": [88],
    "editor.tabSize": 4
  }
}
```

### **HTML/JSX**
```json
{
  "[html]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.tabSize": 2
  }
}
```

## 🚀 **Quick Setup Commands**

```bash
# 1. Install VS Code extensions
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension bradlc.vscode-tailwindcss
code --install-extension esbenp.prettier-vscode
code --install-extension ms-python.black-formatter

# 2. Copy settings
cp vscode-settings-recommended.json ~/.vscode/settings.json

# 3. Open project
code .
```

## ✅ **Benefits of These Settings**

- ✅ **Python IntelliSense** with auto-completion
- ✅ **JSX support** in Python files
- ✅ **Emmet expansion** for HTML in Python
- ✅ **Auto-formatting** with Black
- ✅ **Tailwind CSS** class completion
- ✅ **Error checking** with Pylint/Flake8
- ✅ **Type hints** support
- ✅ **Debugging** configuration

## 🎯 **NextPy-Specific Features**

The settings include:
- **NextPy debug integration**
- **Hot reload configuration**
- **JSX syntax highlighting**
- **Component auto-completion**
- **Performance monitoring**

## 📋 **Verification**

After setup, verify:

1. **Open a `.py` file** - should have Python IntelliSense
2. **Type `<div>`** - should get JSX completion
3. **Type `className="`** - should get Tailwind classes
4. **Save file** - should auto-format with Black
5. **Check errors** - should see linting warnings

## 🚨 **Troubleshooting**

### **JSX not working?**
```json
{
  "files.associations": {
    "*.py": "python"
  },
  "emmet.includeLanguages": {
    "python": "html"
  }
}
```

### **No Tailwind completion?**
```json
{
  "tailwindCSS.includeLanguages": {
    "python": "html"
  }
}
```

### **Formatting not working?**
```json
{
  "python.formatting.provider": "black",
  "editor.formatOnSave": true
}
```

---

**Copy `vscode-settings-recommended.json` to your VS Code settings for the best NextPy development experience!** 🚀
