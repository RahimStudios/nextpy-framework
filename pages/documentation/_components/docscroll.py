"""Shared docs scroll-spy island.

Rendered once by ``pages/documentation/layout.psx`` — every docs page gets
the progress bar, section reveal attributes, TOC highlighting and sidebar
route highlighting without per-page boilerplate.

Two update mechanisms, on purpose:

* ``scroll_progress`` is component state bound with ``style={...}`` — the
  runtime re-evaluates it and writes the ``style`` attribute directly.
* Section/TOC/sidebar highlighting mutates ``data-docs-*`` attributes on
  arbitrary DOM nodes. There is no reactive binding for "the <a> whose href
  matches the current section", so the effect writes attributes itself —
  the same pattern the docs pages used before this component existed.
"""

from nextpy.psx import interactive_component, useState, useEffect, psx, register_component


@interactive_component
def DocsScrollSpy():
    [scroll_progress, set_scroll_progress] = useState(0)

    def SetupScroll():
        def OnScroll():
            doc_height = document.documentElement.scrollHeight - window.innerHeight
            if doc_height > 0:
                pct = (window.scrollY / doc_height) * 100
                if pct > 100:
                    pct = 100
                if pct < 0:
                    pct = 0
                set_scroll_progress(pct)

            # "Last section whose top crossed the line" — robust against
            # short sections and scroll jumps (unlike top<=X<=bottom checks).
            current = ""
            sections = document.querySelectorAll("article div[id], article header[id], section[id]")
            for sec in sections:
                rect = sec.getBoundingClientRect()
                if rect.top <= 160:
                    current = sec.id
                in_view = rect.top < window.innerHeight * 0.92 and rect.bottom > 0
                if in_view:
                    sec.setAttribute("data-docs-revealed", "")
                else:
                    sec.removeAttribute("data-docs-revealed")

            links = document.querySelectorAll("aside a[href^='#'], nav a[href^='#']")
            matched = False
            first_link = None
            for a in links:
                if not first_link:
                    first_link = a
                if a.getAttribute("href") == "#" + current:
                    a.setAttribute("data-docs-toc-active", "")
                    matched = True
                else:
                    a.removeAttribute("data-docs-toc-active")
            # At the very top `current` is the header (no TOC entry) — keep
            # the first link lit instead of leaving the TOC dark.
            if not matched and first_link:
                first_link.setAttribute("data-docs-toc-active", "")

            path = window.location.pathname
            nav_links = document.querySelectorAll("aside a[href^='/']")
            for a in nav_links:
                if a.getAttribute("href") == path:
                    a.setAttribute("data-docs-nav-active", "")
                    parent = a.closest("details")
                    if parent:
                        parent.setAttribute("open", "")
                else:
                    a.removeAttribute("data-docs-nav-active")

        sections = document.querySelectorAll("article div[id], article header[id], section[id]")
        for sec in sections:
            sec.setAttribute("data-docs-reveal", "")

        window.addEventListener("scroll", OnScroll)
        document.addEventListener("nextpy:navigate", OnScroll)
        OnScroll()
        return lambda: window.removeEventListener("scroll", OnScroll)

    useEffect(SetupScroll, [])

    progress_style = f"width: {scroll_progress}%"

    return psx("""
        <div class="fixed top-0 left-0 right-0 z-[70] h-[3px] pointer-events-none">
            <div style={progress_style} class="h-full bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 transition-[width] duration-100"></div>
        </div>
    """)


register_component("DocsScrollSpy", DocsScrollSpy)
