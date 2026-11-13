"""
JobHub - Theme Toggler Page. Uses interactive_component with useState to toggle dark mode.
"""

from nextpy.psx import component, interactive_component, useState


@interactive_component
def ThemeTogglerPage(props=None):
    # theme state can be "light" or "dark"
    [theme, setTheme] = useState("light")

    def toggle_theme(e):
        setTheme("dark" if theme == "light" else "light")

    return (
        <div class={"min-h-screen transition-colors duration-300 px-4 py-16 " + 
               "bg-gray-900 text-white" if theme == "dark" else "bg-gray-50 text-gray-900"}>
            
            <div class="max-w-md mx-auto text-center">
                <div class={"p-8 border rounded-xl shadow-sm transition-all duration-300 " + 
                       "bg-gray-800 border-gray-700" if theme == "dark" else "bg-white border-gray-200"}>
                    
                    <h1 class="mb-2 text-3xl font-bold tracking-tight">
                        {theme.title()} Mode Enabled
                    </h1>
                    
                    <p class={"text-sm mb-8 transition-colors " + 
                           "text-gray-400" if theme == "dark" else "text-gray-600"}>
                        Click the button below to toggle the application layout between light and dark spectrums.
                    </p>

                    <button 
                        type="button" 
                        onclick={toggle_theme}
                        class={"w-full rounded-lg px-4 py-3 font-semibold shadow-sm transition-all flex items-center justify-center gap-2 " + 
                               "bg-yellow-500 hover:bg-yellow-400 text-gray-900" if theme == "dark" else "bg-indigo-600 hover:bg-indigo-700 text-white"}
                    >
                        {"☀️ Switch to Light Mode" if theme == "dark" else "🌙 Switch to Dark Mode"}
                    </button>
                    
                </div>
                
                <p class={"mt-6 text-xs transition-colors " + 
                       "text-gray-500" if theme == "dark" else "text-gray-400"}>
                    Powered by Nextpy UI Compilation Engine
                </p>
            </div>
        </div>
    )


default = ThemeTogglerPage
