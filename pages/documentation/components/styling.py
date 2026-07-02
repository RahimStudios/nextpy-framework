from nextpy.psx import psx, component, register_component, useState, create_onclick, interactive_component


@interactive_component
def StylingDemo(props):
    [theme, setTheme] = useState("light")
    handle_toggle = create_onclick(lambda e: setTheme("dark" if theme == "light" else "light"))

    bg_color = "bg-gray-900" if theme == "dark" else "bg-white"
    text_color = "text-white" if theme == "dark" else "text-gray-900"

    return psx(f"""
        <div class="p-5 border border-pink-200 rounded-2xl bg-pink-50">
            <div class="flex items-center justify-between gap-4">
                <div>
                    <h3 class="font-semibold text-pink-900">Styling Demo</h3>
                    <p class="mt-1 text-sm text-pink-700">Toggle between light and dark themes.</p>
                </div>
                <button create_onclick={handle_toggle} class="px-4 py-2 text-sm font-semibold text-white rounded-lg bg-pink-600">
                    Toggle Theme
                </button>
            </div>
            <div class="mt-4 p-4 rounded-lg {bg_color} {text_color}">
                <p class="text-sm">Current theme: {theme}</p>
            </div>
        </div>
    """)

register_component("StylingDemo", StylingDemo)


@component
def StylingGuide(props):
    return psx("""
        <section id="styling" class="space-y-6">
            <div class="pb-3 border-b border-gray-800">
                <h2 class="text-2xl font-bold text-gray-100">Styling & Tailwind CSS</h2>
                <p class="mt-2 text-gray-400">
                    Style your NextPy applications with Tailwind CSS, custom CSS, and CSS-in-JS solutions.
                </p>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-purple-400">Built-in Tailwind Support</h3>
                <p class="mt-2 text-sm text-purple-300">
                    NextPy comes with Tailwind CSS pre-configured. Use utility classes directly in your PSX components for rapid UI development.
                </p>
            </div>

            <div class="grid gap-6 lg:grid-cols-2">
                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Tailwind Classes</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">@component
def Button(props):
    variant = props.get("variant", "primary")
    
    classes = {
        "primary": "bg-blue-600 text-white",
        "secondary": "bg-gray-200 text-gray-900",
        "danger": "bg-red-600 text-white"
    }
    
    return (
        <button class={f"px-4 py-2 rounded-lg {classes[variant]}"}>
            {props.get("children")}
        </button>
    )</pre>
                </div>

                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Responsive Design</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">@component
def ResponsiveGrid(props):
    return (
        <div class="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
            {props.get("children")}
        </div>
    )

// Usage
<ResponsiveGrid>
    <Card>Item 1</Card>
    <Card>Item 2</Card>
    <Card>Item 3</Card>
</ResponsiveGrid></pre>
                </div>
            </div>

            <div class="grid gap-6 lg:grid-cols-2">
                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Custom CSS</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">// styles/custom.css

.custom-button {
    @apply px-4 py-2 rounded-lg;
    @apply bg-blue-600 text-white;
    @apply hover:bg-blue-700 transition-colors;
}

// In your component
<link rel="stylesheet" href="/styles/custom.css" />

<button class="custom-button">
    Click me
</button></pre>
                </div>

                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Dark Mode</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">@component
def ThemedCard(props):
    return (
        <div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white rounded-lg p-6">
            <h2>{props.get("title")}</h2>
            <p>{props.get("children")}</p>
        </div>
    )

// Enable dark mode in tailwind.config.js
module.exports = {
    darkMode: 'class'
}</pre>
                </div>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-gray-100">Styling Best Practices</h3>
                <ul class="pl-5 mt-3 space-y-2 text-sm text-gray-400 list-disc">
                    <li>Use Tailwind utility classes for 90% of styling needs</li>
                    <li>Extract common patterns into component classes</li>
                    <li>Use the @apply directive for reusable component styles</li>
                    <li>Keep custom CSS in the styles/ directory</li>
                    <li>Use responsive prefixes (md:, lg:) for adaptive layouts</li>
                    <li>Leverage Tailwind's dark mode for theme switching</li>
                    <li>Use arbitrary values for one-off designs (e.g., w-[137px])</li>
                </ul>
            </div>

            <StylingDemo />
        </section>
    """)
