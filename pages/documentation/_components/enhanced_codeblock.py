import json
import html
import ast
from nextpy.psx import component, psx

# Ultra-robust parser to handle NextPy's stringification quirks
def _parse_prop(prop_val, default):
    if prop_val is None:
        return default
    if isinstance(prop_val, (dict, list)):
        return prop_val
        
    # Convert Var or other types to string
    prop_val = str(prop_val)
    
    # Strip NextPy wrappers and decode HTML entities
    prop_val = prop_val.replace('_RAW_CODE:', '')
    prop_val = html.unescape(prop_val)
    
    # If the string is wrapped in extra quotes, strip them
    if prop_val.startswith('"') and prop_val.endswith('"'):
        prop_val = prop_val[1:-1]
        
    # Try JSON (strict=False allows literal newlines in strings)
    try:
        res = json.loads(prop_val, strict=False)
        if isinstance(res, (dict, list)):
            return res
    except Exception:
        pass
        
    # Try AST (handles Python dictionaries with single quotes)
    try:
        res = ast.literal_eval(prop_val)
        if isinstance(res, (dict, list)):
            return res
    except Exception:
        pass
        
    return default

@component
def EnhancedCodeBlock(props):
    """Enhanced modular code window."""
    snippet = props.get("snippet", props.get("code", ""))
    if isinstance(snippet, str):
        # Clean up NextPy formatting
        snippet = snippet.replace('_RAW_CODE:', '')
        snippet = html.unescape(snippet)
        snippet = snippet.replace('&#10;', '\n')
        snippet = snippet.replace('\\n', '\n')

    lang = props.get("lang", "python")
    filename = props.get("filename", None)

    lang_display = html.escape(str(lang))
    code_class = f"language-{lang_display} font-mono block whitespace-pre"

    filename_html = ''
    if filename:
        filename_html = (
            '<span class="text-xs font-mono font-medium text-zinc-300/90 select-none tracking-tight truncate max-w-[280px] inline-block align-bottom">'
            + html.escape(str(filename)) + '</span>'
        )

    # NB: <pre> puts the PSX parser in literal-text mode, so the snippet is
    # rendered through a {snippet} expression inside <code> (whitespace-pre
    # preserves formatting) which escapes markup as text.
    return psx(f"""
        <div class="my-6 overflow-hidden rounded-2xl border border-zinc-800/70 bg-[#0a0a0c] font-sans shadow-[0_8px_30px_rgb(0,0,0,0.35)] antialiased group ring-1 ring-white/[0.03]">
            <div class="flex items-center justify-between pl-4 pr-3 py-2.5 border-b border-zinc-800/60 bg-gradient-to-b from-zinc-900/70 to-zinc-900/30 select-none">
                <div class="flex items-center gap-3.5 min-w-0">
                    <div class="flex items-center gap-1.5 shrink-0" aria-hidden="true">
                        <span class="w-3 h-3 rounded-full bg-[#ff5f57] shadow-[inset_0_0_0_0.5px_rgba(0,0,0,0.3)]"></span>
                        <span class="w-3 h-3 rounded-full bg-[#febc2e] shadow-[inset_0_0_0_0.5px_rgba(0,0,0,0.3)]"></span>
                        <span class="w-3 h-3 rounded-full bg-[#28c840] shadow-[inset_0_0_0_0.5px_rgba(0,0,0,0.3)]"></span>
                    </div>
                    <div class="flex items-center gap-2.5 min-w-0">
                        {filename_html}
                        <span class="shrink-0 px-1.5 py-0.5 text-[10px] font-mono font-semibold tracking-wider text-zinc-500 uppercase bg-zinc-900/80 rounded-md border border-zinc-800/80">
                            {lang_display}
                        </span>
                    </div>
                </div>
                <button
                    class="shrink-0 ml-3 inline-flex items-center gap-1.5 px-2.5 py-1 text-[11px] font-medium text-zinc-400 hover:text-zinc-100 bg-zinc-900/60 hover:bg-zinc-800/70 border border-zinc-800/70 hover:border-zinc-700 rounded-lg transition-all duration-150"
                    onclick="navigator.clipboard.writeText(this.closest('.group').querySelector('code').innerText);var l=this.querySelector('.cb-label');l.textContent='Copied';setTimeout(()=>l.textContent='Copy',1500)"
                >
                    <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
                    <span class="cb-label">Copy</span>
                </button>
            </div>
            <code class="block p-5 overflow-x-auto text-[13px] leading-[1.7] text-zinc-200 scrollbar-thin bg-[#0a0a0c] selection:bg-blue-500/25 selection:text-blue-100 {code_class}">{{snippet}}</code>
        </div>
    """)

@component
def CodeTabs(props):
    """Multi-tab code suite block."""
    tabs = _parse_prop(props.get("tabs"), {})
    
    if not tabs or not isinstance(tabs, dict):
        return psx("<div class='p-4 border border-red-900 bg-red-950/20 text-red-400 text-sm rounded'>Error: Invalid tabs data provided.</div>")
        
    default_tab = props.get("default_tab", list(tabs.keys())[0] if tabs else "")
    
    tab_buttons_stream = ""
    code_panels = []
    panel_vars = {}

    for idx, (tab_name, tab_content) in enumerate(tabs.items()):
        is_active = tab_name == default_tab
        btn_active_styles = "border-blue-500 text-blue-400 bg-zinc-900/40" if is_active else "border-transparent text-zinc-400 hover:text-zinc-200"
        panel_active_styles = "" if is_active else "hidden"

        # Index-based onclick avoids JS parser issues with curly braces and spaces
        tab_label = html.escape(str(tab_name).upper())
        tab_buttons_stream += f"""
        <button
            class="px-4 py-2 text-xs font-semibold tracking-wide transition-all border-b-2 {btn_active_styles}"
            onclick="
                this.parentElement.querySelectorAll('button').forEach(b => b.classList.remove('border-blue-500', 'text-blue-400', 'bg-zinc-900/40'));
                this.parentElement.querySelectorAll('button').forEach(b => b.classList.add('border-transparent', 'text-zinc-400'));
                this.classList.remove('border-transparent', 'text-zinc-400');
                this.classList.add('border-blue-500', 'text-blue-400', 'bg-zinc-900/40');
                let container = this.parentElement.parentElement;
                container.querySelectorAll('.code-panel').forEach(p => p.classList.add('hidden'));
                let target = container.querySelectorAll('.code-panel')[{idx}];
                if(target) target.classList.remove('hidden');
            "
        >
            {tab_label}
        </button>
        """

        lang_class = html.escape(tab_name.lower().replace(' ', '').replace('/', ''))
        if isinstance(tab_content, str):
            tab_content = tab_content.replace('_RAW_CODE:', '')
            tab_content = html.unescape(tab_content)
            tab_content = tab_content.replace('&#10;', '\n')
            tab_content = tab_content.replace('\\n', '\n')
        # Each panel is its own psx() element so {content} stays an expression
        # binding (escaped text). <pre> would force literal-text mode, so the
        # panel is a <code> with block/whitespace-pre styling instead.
        panel_key = f'panel_{idx}'
        code_panels.append(
            psx(
                f'<code class="code-panel block p-5 overflow-x-auto text-sm leading-relaxed bg-zinc-950/80 {panel_active_styles} language-{lang_class} font-mono whitespace-pre">{{content}}</code>'.replace('  ', ' '),
                {'content': tab_content}
            )
        )
        panel_vars[panel_key] = code_panels[-1]

    panel_exprs = ''.join(f'{{panel_{i}}}' for i in range(len(code_panels)))

    return psx(f"""
        <div class="my-6 overflow-hidden rounded-2xl border border-zinc-800/70 bg-[#0a0a0c] font-sans shadow-[0_8px_30px_rgb(0,0,0,0.35)] antialiased ring-1 ring-white/[0.03]">
            <div class="flex items-center border-b border-zinc-800/60 bg-gradient-to-b from-zinc-900/70 to-zinc-900/30 select-none">
                <div class="flex items-center gap-1.5 pl-4 shrink-0" aria-hidden="true">
                    <span class="w-3 h-3 rounded-full bg-[#ff5f57] shadow-[inset_0_0_0_0.5px_rgba(0,0,0,0.3)]"></span>
                    <span class="w-3 h-3 rounded-full bg-[#febc2e] shadow-[inset_0_0_0_0.5px_rgba(0,0,0,0.3)]"></span>
                    <span class="w-3 h-3 rounded-full bg-[#28c840] shadow-[inset_0_0_0_0.5px_rgba(0,0,0,0.3)]"></span>
                </div>
                <div class="flex-1 flex items-center min-w-0 overflow-x-auto">
                    {tab_buttons_stream}
                </div>
            </div>
            <div>
                {panel_exprs}
            </div>
        </div>
    """, panel_vars)

@component
def FileTree(props):
    """Hierarchical design tree representation."""
    files = _parse_prop(props.get("files"), [])
    
    if not files or not isinstance(files, list):
        return psx("<div class='p-4 border border-red-900 bg-red-950/20 text-red-400 text-sm rounded'>Error: Invalid file tree data provided.</div>")

    file_rows_stream = ""
    for file in files:
        if isinstance(file, dict):
            file_name = html.escape(str(file.get("name", "")))
            is_folder = file.get("type") == "folder"
        else:
            file_name = html.escape(str(file))
            is_folder = False
            
        if is_folder:
            icon_markup = """
            <svg class="w-3.5 h-3.5 text-amber-500/90 shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2 6a2 2 0 012-2h5l2 2h5a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" />
            </svg>
            """
            row_styles = "text-zinc-200 font-semibold"
        else:
            icon_markup = """
            <svg class="w-3.5 h-3.5 text-zinc-500 shrink-0" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            """
            row_styles = "text-zinc-400 font-normal"
            
        file_rows_stream += f"""
        <div class="flex items-center gap-2.5 py-1.5 hover:text-zinc-100 transition-colors tracking-tight {row_styles}">
            {icon_markup}
            <span class="select-all">{file_name}</span>
        </div>
        """

    return psx(f"""
        <div class="my-6 p-5 overflow-hidden rounded-xl border border-zinc-800/80 bg-zinc-950 font-sans shadow-sm antialiased select-none">
            <div class="mb-4 flex items-center gap-2 text-xs font-bold tracking-wider text-zinc-500 uppercase">
                <svg class="w-4 h-4 text-zinc-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                </svg>
                Project File System Tree
            </div>
            <div class="font-mono text-xs pl-1">
                {file_rows_stream}
            </div>
        </div>
    """)