from nextpy.psx import interactive_component as component, register_component, psx
from pages.main import interactive_component

@interactive_component
def Navbar(props=None):
    props =props or {}

    return psx(f"""
        <nav class="sticky py-4 top-0 z-50 w-full border-b border-gray-100 bg-white/80 backdrop-blur-md">
                    <div class="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
                        <div class="flex items-center justify-between h-16">
                            <div class="flex items-center">
                                <a href="/" class="flex items-center space-x-2 group" hx-get="/" hx-target="#main-content" hx-push-url="true">
                                    <div>
                                        <img src="/static/images/icon.png" alt="NextPy Logo" class="h-20 w-auto bg-white  p-2">
                                    </div>
                                    <div class="flex items-baseline font-bold tracking-tight text-black">
                                        <span class="text-3xl font-black">N</span>
                                        <span class="text-xl font-light">ext</span>
                                        <span class="text-3xl font-black">P</span>
                                        <span class="text-xl font-light">y</span>
                                    </div>
                                </a>
                            </div>
                            
                            <div class="items-center hidden space-x-1 md:flex">
                                <a href="/" class="px-3 py-2 text-sm font-medium text-gray-600 transition-colors rounded-md hover:text-black hover:bg-gray-50" hx-get="/" hx-target="#main-content" hx-push-url="true">Home</a>
                                <a href="/about" class="px-3 py-2 text-sm font-medium text-gray-600 transition-colors rounded-md hover:text-black hover:bg-gray-50" hx-get="/about" hx-target="#main-content" hx-push-url="true">About</a>
                                <a href="/blog" class="px-3 py-2 text-sm font-medium text-gray-600 transition-colors rounded-md hover:text-black hover:bg-gray-50" hx-get="/blog" hx-target="#main-content" hx-push-url="true">Blog</a>
                                <a href="/documentation" class="px-3 py-2 text-sm font-medium text-gray-600 transition-colors rounded-md hover:text-black hover:bg-gray-50" hx-get="/documentation" hx-target="#main-content" hx-push-url="true">Docs</a>
                            </div>

                            <div class="flex items-center space-x-4">
                                <a href="https://github.com/IBRAHIMFONYUY/nextpy-framework/" target="_blank" class="items-center hidden text-gray-500 transition-colors md:flex hover:text-black">
                                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.43.372.823 1.102.823 2.222 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>
                                </a>
                                <a href="/login" class="px-4 py-1.5 text-sm font-medium text-white bg-black rounded-full hover:bg-gray-800 transition-all shadow-sm" hx-get="/login" hx-target="#main-content" hx-push-url="true">
                                    Sign In
                                </a>
                            </div>
                        </div>
                    </div>
                </nav>
    """)

default = Navbar