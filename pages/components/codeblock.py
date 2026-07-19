from nextpy.psx import interactive_component as component, psx, useState, create_onclick


@component
def CodeBlock(props):
    props = props or {}
    [copy, setCopy]= useState(False)
    lang = props.get("lang", "text")
    code = props.get("code", "")
    
    handletoggle=create_onclick(lambda e: setCopy(not copy))

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
                <span class="text-xs font-medium tracking-wider uppercase text-sky-400">
                    {lang}
                </span>

                <!-- Copy button -->
                <div create_onlick={handletoggle}>
                {{if copy:
                     <button
                        onclick="navigator.clipboard.writeText(this.closest('.group').querySelector('code').innerText)"
                        class="text-xs text-gray-400 transition hover:text-sky-400"
                    >
                        Copied
                    </button>
                {{else:
                
                    <button
                        onclick="navigator.clipboard.writeText(this.closest('.group').querySelector('code').innerText)"
                        class="text-xs text-gray-400 transition hover:text-sky-400"
                    >
                        Copy
                    </button>
                
                }}
                   
                </div>

            </div>

            <!-- Code block -->
            <pre class="p-4 overflow-x-auto font-mono text-sm leading-relaxed text-gray-200">
<code class="language-{lang}">
{code}
</code>
            </pre>

        </div>
    """)