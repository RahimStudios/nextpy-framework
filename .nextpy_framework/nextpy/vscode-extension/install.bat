@echo off
REM NextPy PSX VS Code Extension Installation Script for Windows
echo 🚀 Installing NextPy PSX VS Code Extension...

REM Check if VS Code is installed
where code >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ VS Code is not installed or not in PATH
    echo Please install VS Code first: https://code.visualstudio.com/
    pause
    exit /b 1
)

REM Install dependencies
echo 📦 Installing dependencies...
npm install

REM Compile TypeScript
echo 🔨 Compiling TypeScript...
npm run compile

REM Package extension
echo 📦 Packaging extension...
vsce package

REM Install extension
echo 🔧 Installing extension in VS Code...
code --install-extension nextpy-psx-*.vsix

echo ✅ NextPy PSX extension installed successfully!
echo 🎯 Restart VS Code to activate the extension
echo 📚 Use Ctrl+Shift+P and search for 'NextPy PSX' to access commands
pause
