from nextpy.psx import component, psx


@component
def CodeBlock(props):
    lang = props.get("lang", "text")
    code = props.get("code", "")

    return psx(f"""
        <div class="relative rounded-xl border border-gray-800 bg-[#0d1117] overflow-hidden group">

            <!-- Header -->
            <div class="flex items-center justify-between px-4 py-2 bg-gray-900 border-b border-gray-800">

                <!-- Mac-style dots -->
                <div class="flex items-center space-x-2">
                    <span class="w-3 h-3 bg-red-500 rounded-full"></span>
                    <span class="w-3 h-3 bg-yellow-500 rounded-full"></span>
                    <span class="w-3 h-3 bg-green-500 rounded-full"></span>
                </div>

                <!-- Language -->
                <span class="text-xs text-sky-400 uppercase tracking-wider font-medium">
                    {lang}
                </span>

                <!-- Copy button -->
                <button
                    onclick="navigator.clipboard.writeText(this.closest('.group').querySelector('code').innerText)"
                    class="text-xs text-gray-400 hover:text-sky-400 transition"
                >
                    Copy
                </button>

            </div>

            <!-- Code block -->
            <pre class="p-4 overflow-x-auto text-sm leading-relaxed font-mono text-gray-200">
<code class="language-{lang}">
{code}
</code>
            </pre>

        </div>
    """)