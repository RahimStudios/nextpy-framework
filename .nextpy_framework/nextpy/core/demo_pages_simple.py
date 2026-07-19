"""
Simple Demo Pages - Basic HTML without JSX for demo mode
"""

from typing import Dict, Any


def HomePage():
    """NextPy homepage - shows when no project is created"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NextPy - Next.js for Python</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; 
                line-height: 1.6; 
                color: #333; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
                padding: 2rem; 
                text-align: center; 
            }
            .hero { 
                padding: 4rem 0; 
                text-align: center; 
            }
            .hero h1 { 
                font-size: 4rem; 
                font-weight: 700; 
                color: white; 
                margin-bottom: 1rem; 
                text-shadow: 0 2px 4px rgba(0,0,0,0.1); 
            }
            .hero p { 
                font-size: 1.25rem; 
                color: rgba(255,255,255,0.9); 
                margin-bottom: 2rem; 
                max-width: 600px; 
            }
            .buttons { 
                display: flex; 
                gap: 1rem; 
                justify-content: center; 
                flex-wrap: wrap; 
            }
            .btn { 
                    display: inline-block; 
                    padding: 0.75rem 1.5rem; 
                    font-size: 1rem; 
                    font-weight: 500; 
                    text-decoration: none; 
                    border-radius: 0.5rem; 
                    transition: all 0.2s; 
                }
            .btn-primary { 
                    background-color: #3b82f6; 
                    color: white; 
                    border: 1px solid #2563eb; 
                }
            .btn-primary:hover { 
                    background-color: #2c528d; 
                }
            .btn-outline { 
                    background-color: transparent; 
                    color: white; 
                    border: 1px solid rgba(255,255,255,0.3); 
                }
            .btn-outline:hover { 
                    background-color: rgba(255,255,255,0.1); 
                }
            .features { 
                    display: grid; 
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
                    gap: 2rem; 
                    margin-top: 4rem; 
                }
            .feature { 
                    background: rgba(255,255,255,0.1); 
                    backdrop-filter: blur(10px); 
                    border: 1px solid rgba(255,255,255,0.2); 
                    border-radius: 0.5rem; 
                    padding: 2rem; 
                    text-align: center; 
                    transition: all 0.2s; 
                }
            .feature:hover { 
                    background: rgba(255,255,255,0.2); 
                    transform: translateY(-2px); 
                }
            .feature h3 { 
                    font-size: 1.5rem; 
                    font-weight: 600; 
                    color: white; 
                    margin-bottom: 0.5rem; 
                }
            .feature p { 
                    color: rgba(255,255,255,0.9); 
                    margin-bottom: 1rem; 
                }
            .demo-info { 
                    background: rgba(255,255,255,0.1); 
                    backdrop-filter: blur(10px); 
                    border: 1px solid rgba(255,255,255,0.2); 
                    border-radius: 0.5rem; 
                    padding: 2rem; 
                    margin-top: 4rem; 
                    text-align: center; 
                }
            .demo-info h2 { 
                    font-size: 2rem; 
                    font-weight: 600; 
                    color: white; 
                    margin-bottom: 1rem; 
                }
            .demo-info code { 
                    background: rgba(0,0,0,0.2); 
                    color: #10b981; 
                    padding: 0.25rem 0.5rem; 
                    border-radius: 0.25rem; 
                    font-family: 'Courier New', monospace; 
                    font-size: 0.875rem; 
                }
            .demo-info p { 
                    color: rgba(255,255,255,0.9); 
                    margin-bottom: 0.5rem; 
                }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="hero">
                <h1>Welcome to <span style="color: #fbbf24;">NextPy</span></h1>
                <p>The Python web framework with exact Next.js syntax!</p>
                <div class="buttons">
                    <a href="/create-project" class="btn btn-primary">Create New Project</a>
                    <a href="/docs" class="btn btn-outline">View Documentation</a>
                </div>
            </div>
            
            <div class="features">
                <div class="feature">
                    <h3>🎯 Next.js Syntax</h3>
                    <p>Write React-like code in Python with useState, useEffect, components!</p>
                </div>
                <div class="feature">
                    <h3>⚡ True JSX</h3>
                    <p>Write HTML-like components directly in Python code!</p>
                </div>
                <div class="feature">
                    <h3>🔧 Full Ecosystem</h3>
                    <p>50+ components, hooks, API routes, hot reload!</p>
                </div>
            </div>
            
            <div class="demo-info">
                <h2>🎉 Demo Mode Activated!</h2>
                <p>No NextPy project detected. Showing built-in documentation.</p>
                <p>Create a project with: <code>nextpy create my-app</code></p>
                <p>Or run: <code>mkdir my-app && cd my-app && nextpy create .</code></p>
            </div>
        </div>
    </body>
    </html>
    """


def ComponentsPage():
    """Components showcase page"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Components - NextPy</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; 
                line-height: 1.6; 
                color: #333; 
                background: #f8fafc; 
                min-height: 100vh;
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
                padding: 2rem; 
            }
            .header { 
                text-align: center; 
                margin-bottom: 3rem; 
            }
            .header h1 { 
                font-size: 3rem; 
                font-weight: 700; 
                color: #1a20212; 
                margin-bottom: 1rem; 
            }
            .header p { 
                font-size: 1.125rem; 
                color: #6b7280; 
                max-width: 800px; 
                margin: 0 auto; 
            }
            .grid { 
                    display: grid; 
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
                    gap: 2rem; 
                    margin-top: 2rem; 
                }
            .card { 
                    background: white; 
                    border: 1px solid #e5e7eb; 
                    border-radius: 0.5rem; 
                    padding: 1.5rem; 
                    box-shadow: 0 1px 3px 0 rgba(0,0,0,0.1); 
                    transition: all 0.2s; 
                }
            .card:hover { 
                    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); 
                    transform: translateY(-2px); 
                }
            .card h3 { 
                    font-size: 1.25rem; 
                    font-weight: 600; 
                    color: #1a20212; 
                    margin-bottom: 0.5rem; 
                }
            .card p { 
                    color: #6b7280; 
                    line-height: 1.5; 
                }
            .code-block { 
                    background: #1f2937; 
                    color: #e2e8f0; 
                    padding: 1rem; 
                    border-radius: 0.375rem; 
                    font-family: 'Courier New', monospace; 
                    font-size: 0.875rem; 
                    overflow-x: auto; 
                }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Components Library</h1>
                <p>50+ pre-built components for rapid development</p>
            </div>
            
            <div class="grid">
                <div class="card">
                    <h3>Form Components</h3>
                    <p>Complete form elements with validation</p>
                    <div class="code-block">
                        <pre>Input(name="email" placeholder="Enter email")
Button(text="Submit" variant="primary")</pre>
                    </div>
                </div>
                
                <div class="card">
                    <h3>UI Components</h3>
                    <p>Interactive and display elements</p>
                    <div class="code-block">
                        <pre>Button(text="Click Me" variant="primary")
Badge(text="New" variant="success")</pre>
                    </div>
                </div>
                
                <div class="card">
                    <h3>Layout Components</h3>
                    <p>Grid, flex, container layouts</p>
                    <div class="code-block">
                        <pre>Grid(columns=3, gap=4)
Container(max_width="6xl")</pre>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """


def HooksPage():
    """Hooks showcase page"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Hooks - NextPy</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; 
                line-height: 1.6; 
                color: #333; 
                background: #f8fafc; 
                min-height: 100vh; 
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
                padding: 2rem; 
            }
            .header { 
                text-align: center; 
                margin-bottom: 3rem; 
            }
            .header h1 { 
                font-size: 3rem; 
                font-weight: 700; 
                color: #1a20212; 
                margin-bottom: 1rem; 
            }
            .header p { 
                font-size: 1.125rem; 
                color: #6b7280; 
                max-width: 800px; 
                margin: 0 auto; 
            }
            .hooks-grid { 
                    display: grid; 
                    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); 
                    gap: 2rem; 
                    margin-top: 2rem; 
                }
            .hook-card { 
                    background: white; 
                    border: 1px solid #e5e7eb; 
                    border-radius: 0.5rem; 
                    padding: 2rem; 
                    box-shadow: 0 1px 3px 0 rgba(0,0,0,0.1); 
                }
            .hook-card h3 { 
                    font-size: 1.25rem; 
                    font-weight: 600; 
                    color: #1a20212; 
                    margin-bottom: 1rem; 
                }
            .hook-card pre { 
                    background: #1f2937; 
                    color: #e2e8f0; 
                    padding: 1rem; 
                    border-radius: 0.375rem; 
                    font-family: 'Courier New', monospace; 
                    font-size: 0.875rem; 
                    overflow-x: auto; 
                    margin-bottom: 1rem; 
                }
            .hook-card p { 
                    color: #6b7280; 
                    line-height: 1.5; 
                }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>React-like Hooks</h1>
                <p>All your favorite React hooks - but in Python!</p>
            </div>
            
            <div class="hooks-grid">
                <div class="hook-card">
                    <h3>useState</h3>
                    <p>State management</p>
                    <div class="code-block">
                        <pre>[count, setCount] = useState(0)
setCount(count + 1)</pre>
                    </div>
                </div>
                
                <div class="hook-card">
                    <h3>useEffect</h3>
                    <p>Side effects and lifecycle</p>
                    <div class="code-block">
                        <pre>useEffect(() => {
  console.log('Mounted!')
  return () => console.log('Cleanup!')
}, [])</pre>
                    </div>
                </div>
                
                <div class="hook-card">
                    <h3>useReducer</h3>
                    <p>Complex state management</p>
                    <div class="code-block">
                        <pre>[state, dispatch] = useReducer(reducer, initialState)
dispatch({'type': 'increment'})</pre>
                    </div>
                </div>
                
                <div class="hook-card">
                    <h3>Custom Hooks</h3>
                    <p>Built-in convenience hooks</p>
                    <div class="code-block">
                        <pre>[count, inc, dec] = useCounter(10)
[visible, toggle] = useToggle(true)</pre>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """


def DocsPage():
    """Documentation page"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Documentation - NextPy</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; 
                line-height: 1.6; 
                color: #333; 
                background: #f8fafc; 
                min-height: 100vh; 
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
                padding: 2rem; 
            }
            .header { 
                text-align: center; 
                margin-bottom: 3rem; 
            }
            .header h1 { 
                font-size: 3rem; 
                font-weight: 700; 
                color: #1a20212; 
                margin-bottom: 1rem; 
            }
            .header p { 
                font-size: 1.125rem; 
                color: #6b7280; 
                max-width: 800px; 
                margin: 0 auto; 
            }
            .doc-grid { 
                    display: grid; 
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
                    gap: 2rem; 
                    margin-top: 2rem; 
                }
            .doc-card { 
                    background: white; 
                    border: 1px solid #e5e7eb; 
                    border-radius: 0.5rem; 
                    padding: 2rem; 
                    box-shadow: 0 1px 3px 0 rgba(0,0,0,0.1); 
                }
            .doc-card h3 { 
                    font-size: 1.25rem; 
                    font-weight: 600; 
                    color: #1a20212; 
                    margin-bottom: 1rem; 
                }
            .doc-card ul { 
                    list-style: none; 
                    padding-left: 0; 
                }
            .doc-card li { 
                    margin-bottom: 0.5rem; 
                }
            .doc-card li a { 
                    color: #2563eb; 
                    text-decoration: none; 
                    font-weight: 500; 
                }
            .doc-card li a:hover { 
                    text-decoration: underline; 
                }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Documentation</h1>
                <p>Complete documentation for NextPy</p>
            </div>
            
            <div class="doc-grid">
                <div class="doc-card">
                    <h3>Getting Started</h3>
                    <ul>
                        <li><a href="/docs/installation">Installation</a></li>
                        <li><a href="/docs/quickstart">Quick Start</a></li>
                        <li><a href="/docs/project-structure">Project Structure</a></li>
                        <li><a href="/docs/configuration">Configuration</a></li>
                    </ul>
                </div>
                
                <div class="doc-card">
                    <h3>Core Concepts</h3>
                    <ul>
                        <li><a href="/docs/components">Components</a></li>
                        <li><a href="/docs/hooks">Hooks</a></li>
                        <li><a href="/docs/routing">Routing</a></li>
                        <li><a href="/docs/data-fetching">Data Fetching</a></li>
                    </ul>
                </div>
                
                <div class="doc-card">
                    <h3>Advanced Topics</h3>
                    <ul>
                        <li><a href="/docs/performance">Performance</a></li>
                        <li><a href="/docs/deployment">Deployment</a></li>
                        <li><a href="/docs/testing">Testing</a></li>
                        <li><a href="/docs/plugins">Plugins</a></li>
                    </ul>
                </div>
            </div>
        </div>
    </body>
    </html>
    """


def CreateProjectPage():
    """Create project page"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Create Project - NextPy</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; 
                line-height: 1.6; 
                color: #333; 
                background: #f8fafc; 
                min-height: 100vh; 
                display: flex; 
                align-items: center; 
                justify-content: center; 
            }
            .create-form { 
                background: white; 
                border: 1px solid #e5e7eb; 
                border-radius: 0.5rem; 
                padding: 2rem; 
                box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); 
                max-width: 500px; 
                width: 100%; 
            }
            .form-group { 
                margin-bottom: 1.5rem; 
            }
            .form-group label { 
                display: block; 
                font-weight: 500; 
                margin-bottom: 0.5rem; 
                color: #374151; 
            }
            .form-group input { 
                display: block; 
                width: 100%; 
                padding: 0.75rem; 
                border: 1px solid #d1d5db; 
                border-radius: 0.375rem; 
                font-size: 1rem; 
            }
            .form-group select { 
                display: block; 
                width: 100%; 
                padding: 0.75rem; 
                border: 1px solid #d1d5db; 
                border-radius: 0.375rem; 
                font-size: 1rem; 
            }
            .btn { 
                display: inline-block; 
                padding: 0.75rem 1.5rem; 
                font-size: 1rem; 
                font-weight: 500; 
                text-decoration: none; 
                border-radius: 0.375rem; 
                transition: all 0.2s; 
                cursor: pointer; 
            }
            .btn-primary { 
                background-color: #3b82f6; 
                color: white; 
                border: 1px solid #2563eb; 
            }
            .btn-primary:hover { 
                background-color: #2563eb; 
            }
            .btn-outline { 
                background-color: transparent; 
                color: #3b82f6; 
                border: 1px solid #3b82f6; 
            }
            .btn-outline:hover { 
                background-color: #3b82f6; 
                color: white; 
            }
            .info-text { 
                text-align: center; 
                color: #6b7280; 
                margin-top: 2rem; 
            }
        </style>
    </head>
    <body>
        <div class="create-form">
            <h2>Create Your NextPy App</h2>
            
            <div class="form-group">
                <label for="project-name">Project Name</label>
                <input type="text" id="project-name" placeholder="my-app" />
            </div>
            
            <div class="form-group">
                <label for="template">Template</label>
                <select id="template">
                    <option value="default">Default (Basic)</option>
                    <option value="blog">Blog</option>
                    <option value="ecommerce">E-commerce</option>
                    <option value="dashboard">Dashboard</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Features</label>
                <div>
                    <label>
                        <input type="checkbox" checked />
                        <span>TypeScript support</span>
                    </label>
                </div>
                <div>
                    <label>
                        <input type="checkbox" checked />
                        <span>Tailwind CSS</span>
                    </label>
                </div>
                <div>
                    <label>
                        <input type="checkbox" />
                        <span>Authentication</span>
                    </label>
                </div>
                <div>
                    <label>
                        <input type="checkbox" />
                        <span>Database setup</span>
                    </label>
                </div>
            </div>
            
            <div class="info-text">
                <p>Or run: <code>nextpy create my-app</code> in your terminal</p>
            </div>
            
            <div style="text-align: center;">
                <button class="btn btn-primary">Create Project</button>
            </div>
        </div>
    </body>
    </html>
    """


# Demo page routes - Simple HTML versions
DEMO_ROUTES = {
    '/': HomePage,
    '/components': ComponentsPage,
    '/hooks': HooksPage,
    '/docs': DocsPage,
    '/create-project': CreateProjectPage,
}
