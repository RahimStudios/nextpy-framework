#!/usr/bin/env python3
"""
PSX Developer Tools Setup Script
Automatically sets up the complete PSX developer environment
"""

import os
import sys
import subprocess
import json
from pathlib import Path


def print_step(step: str, description: str):
    """Print a setup step"""
    print(f"🔧 {step}: {description}")


def print_success(message: str):
    """Print success message"""
    print(f"✅ {message}")


def print_error(message: str):
    """Print error message"""
    print(f"❌ {message}")


def print_info(message: str):
    """Print info message"""
    print(f"ℹ️  {message}")


def run_command(cmd: str, description: str) -> bool:
    """Run a command and return success status"""
    print_step("Running", description)
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print_success(f"{description} completed")
            return True
        else:
            print_error(f"{description} failed: {result.stderr}")
            return False
    except Exception as e:
        print_error(f"{description} error: {e}")
        return False


def install_python_deps():
    """Install Python dependencies for language server"""
    print_step("Installing", "Python dependencies")
    
    deps = ["pygls", "lsprotocol"]
    for dep in deps:
        try:
            __import__(dep)
            print_success(f"{dep} already installed")
        except ImportError:
            if run_command(f"pip install {dep}", f"Installing {dep}"):
                print_success(f"{dep} installed")
            else:
                print_error(f"Failed to install {dep}")
                return False
    
    return True


def setup_vscode_extension():
    """Set up VS Code extension for development"""
    print_step("Setting up", "VS Code extension")
    
    ext_dir = Path(__file__).parent / "vscode-extension"
    if not ext_dir.exists():
        print_error("VS Code extension directory not found")
        return False
    
    # Install Node.js dependencies
    if run_command("cd vscode-extension && npm install", "Installing Node.js dependencies"):
        print_success("Node.js dependencies installed")
    else:
        print_error("Failed to install Node.js dependencies")
        return False
    
    # Compile extension
    if run_command("cd vscode-extension && npm run compile", "Compiling extension"):
        print_success("Extension compiled")
    else:
        print_error("Failed to compile extension")
        return False
    
    return True


def create_dev_config():
    """Create development configuration"""
    print_step("Creating", "development configuration")
    
    # Create VS Code settings
    vscode_dir = Path.home() / ".vscode"
    vscode_dir.mkdir(exist_ok=True)
    
    settings_file = vscode_dir / "settings.json"
    settings = {
        "psx.languageServer.enabled": True,
        "psx.languageServer.path": str(Path(__file__).parent / "psx-language-server"),
        "psx.formatting.enabled": True,
        "psx.validation.enabled": True,
        "python.defaultInterpreterPath": sys.executable
    }
    
    try:
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=2)
        print_success("VS Code settings created")
    except Exception as e:
        print_error(f"Failed to create VS Code settings: {e}")
        return False
    
    return True


def create_file_associations():
    """Create file associations for PSX"""
    print_step("Creating", "file associations")
    
    # Add PSX file association to VS Code
    associations = {
        "files.associations": {
            "*.psx": "psx"
        }
    }
    
    vscode_dir = Path.home() / ".vscode"
    settings_file = vscode_dir / "settings.json"
    
    try:
        if settings_file.exists():
            with open(settings_file, 'r') as f:
                current_settings = json.load(f)
        else:
            current_settings = {}
        
        current_settings.update(associations)
        
        with open(settings_file, 'w') as f:
            json.dump(current_settings, f, indent=2)
        
        print_success("File associations created")
    except Exception as e:
        print_error(f"Failed to create file associations: {e}")
        return False
    
    return True


def test_language_server():
    """Test the language server"""
    print_step("Testing", "language server")
    
    server_script = Path(__file__).parent / "language_server_lsp.py"
    if not server_script.exists():
        print_error("Language server script not found")
        return False
    
    try:
        # Test import
        sys.path.insert(0, str(Path(__file__).parent))
        from language_server_lsp import PSXLanguageServer
        
        # Create server instance
        server = PSXLanguageServer()
        
        # Test basic functionality
        test_completions = server.get_completions("<div", type('MockPosition', (), {'line': 0, 'character': 5})())
        if test_completions and len(test_completions.items) > 0:
            print_success("Language server test passed")
            return True
        else:
            print_error("Language server test failed")
            return False
    
    except Exception as e:
        print_error(f"Language server test error: {e}")
        return False


def create_sample_psx_file():
    """Create a sample PSX file for testing"""
    print_step("Creating", "sample PSX file")
    
    sample_content = '''# Sample PSX File
# This demonstrates PSX syntax with full IDE support

def UserCard(user):
    """A simple user card component"""
    return (
        <div className="user-card" key={user.id}>
            <div className="avatar">
                <img src={user.avatar} alt={user.name} />
            </div>
            <div className="info">
                <h3>{user.name}</h3>
                <p>{user.email}</p>
                {if user.is_active:
                    <span className="status active">Active</span>
                else:
                    <span className="status inactive">Inactive</span>
                }
            </div>
            <div className="actions">
                <button onClick={() => edit_user(user.id)}>
                    Edit
                </button>
                <button onClick={() => delete_user(user.id)} className="danger">
                    Delete
                </button>
            </div>
        </div>
    )

# Example usage
users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com", "avatar": "/avatar1.jpg", "is_active": True},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "avatar": "/avatar2.jpg", "is_active": False}
]

def App():
    """Main application component"""
    return (
        <div className="app">
            <header>
                <h1>PSX Developer Tools Demo</h1>
                <p>Full JSX-like experience for Python!</p>
            </header>
            <main>
                <h2>User List</h2>
                <div className="user-list">
                    {for user in users:
                        <UserCard user={user} />
                    }
                </div>
            </main>
        </div>
    )
'''
    
    try:
        with open('sample.psx', 'w') as f:
            f.write(sample_content)
        print_success("Sample PSX file created: sample.psx")
        return True
    except Exception as e:
        print_error(f"Failed to create sample file: {e}")
        return False


def main():
    """Main setup function"""
    print("🚀 PSX Developer Tools Setup")
    print("=" * 50)
    print("Setting up complete PSX development environment...")
    print()
    
    steps = [
        ("Python Dependencies", install_python_deps),
        ("VS Code Extension", setup_vscode_extension),
        ("Development Configuration", create_dev_config),
        ("File Associations", create_file_associations),
        ("Language Server Test", test_language_server),
        ("Sample File", create_sample_psx_file)
    ]
    
    passed = 0
    total = len(steps)
    
    for step_name, step_func in steps:
        if step_func():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Setup Complete: {passed}/{total} steps successful")
    
    if passed == total:
        print("🎉 PSX Developer Tools setup completed successfully!")
        print()
        print("📋 Next Steps:")
        print("1. Open VS Code")
        print("2. Install the PSX extension from the vscode-extension directory")
        print("3. Open the sample.psx file to test the experience")
        print("4. Enjoy JSX-like development with Python!")
    else:
        print("⚠️  Some setup steps failed. Check the errors above.")
    
    print()
    print("📚 For more information, see:")
    print("   - PSX Language Server: language_server_lsp.py")
    print("   - VS Code Extension: vscode-extension/")
    print("   - Code Formatter: psx_formatter.py")
    print("   - Documentation: README.md")


if __name__ == "__main__":
    main()
