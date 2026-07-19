#!/bin/bash

# NextPy PSX VS Code Extension Installation Script
echo "🚀 Installing NextPy PSX VS Code Extension..."

# Check if VS Code is installed
if ! command -v code &> /dev/null; then
    echo "❌ VS Code is not installed or not in PATH"
    echo "Please install VS Code first: https://code.visualstudio.com/"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Compile TypeScript
echo "🔨 Compiling TypeScript..."
npm run compile

# Package extension
echo "📦 Packaging extension..."
vsce package

# Install extension
echo "🔧 Installing extension in VS Code..."
code --install-extension nextpy-psx-*.vsix

echo "✅ NextPy PSX extension installed successfully!"
echo "🎯 Restart VS Code to activate the extension"
echo "📚 Use Ctrl+Shift+P and search for 'NextPy PSX' to access commands"
