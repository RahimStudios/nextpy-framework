"""Shared building blocks for animation playground pages.

Everything here renders with the framework's own PSX primitives —
``Motion`` for WAAPI-driven animation, ``AnimatePresence`` for exits,
Tailwind classes for CSS transitions — so every demo on the site is
real, copy-pasteable framework code.
"""

from nextpy.psx import component, Motion, clsx
from nextpy.psx.core.parser import PSXElement


def el(tag, class_name="", children=None, data=None, **attrs):
    """Build a PSXElement for an arbitrary tag (data-* via dict)."""
    props = {"class": class_name}
    props.update({k: v for k, v in attrs.items() if v is not None})
    if data:
        props.update({f"data-{k}": v for k, v in data.items() if v is not None})
    if isinstance(children, (list, tuple)):
        child_list = [c for c in children if c is not None]
    elif children is None:
        child_list = []
    else:
        child_list = [children]
    return PSXElement(tag=tag, props=props, children=child_list)


# ---------------------------------------------------------------------------
# Preview frame — dotted canvas + centered card, same on every page
# ---------------------------------------------------------------------------

@component
def DemoFrame(props=None):
    """Well-aligned preview canvas for a live demo."""
    props = props or {}
    children = props.get("children") if isinstance(props, dict) else getattr(props, "children", None)
    tall = props.get("tall", False) if isinstance(props, dict) else getattr(props, "tall", False)
    min_h = "min-h-[16rem]" if tall else "min-h-[10rem]"
    return (
        <div class={clsx("relative flex items-center justify-center overflow-hidden rounded-xl border border-zinc-800",
                          "bg-[radial-gradient(circle,#27272a_1px,transparent_1px)] bg-[length:20px_20px]",
                          min_h)}>
            <Motion initial={{"opacity": 0, "y": 14, "scale": 0.97}} animate={{"opacity": 1, "y": 0, "scale": 1}}
                   transition={{"duration": 0.45, "easing": "cubic-bezier(0.22,1,0.36,1)"}}
                   className="rounded-xl border border-zinc-800 bg-zinc-950/90 p-8 shadow-2xl">
                {children}
            </Motion>
        </div>
    )


# ---------------------------------------------------------------------------
# Code block with copy button
# ---------------------------------------------------------------------------

@component
def CodeBlock(props=None):
    """Code block with a copy button.

    Plain component (no hydration runtime) — the button uses a small inline
    ``onclick`` JS snippet that copies the sibling ``<code>`` text, so these
    blocks stay lightweight even with many per page.
    """
    props = props or {}
    code = props.get("code", "") if isinstance(props, dict) else getattr(props, "code", "")
    language = props.get("language", "python") if isinstance(props, dict) else getattr(props, "language", "python")

    copy_js = ("navigator.clipboard&&navigator.clipboard.writeText("
               "this.parentElement.nextElementSibling.innerText);"
               "this.textContent='Copied!';setTimeout(()=>this.textContent='Copy',1500)")
    copy_btn = el("button", "rounded-md bg-zinc-800 px-2.5 py-1 text-xs font-medium text-zinc-400 transition-colors hover:text-zinc-200",
                  "Copy", type="button", onclick=copy_js)

    return (
        <div class="overflow-hidden rounded-xl border border-zinc-800 bg-zinc-950">
            <div class="flex items-center justify-between border-b border-zinc-800/80 bg-zinc-900/60 px-4 py-2">
                <div class="flex items-center gap-1.5">
                    <span class="h-2.5 w-2.5 rounded-full bg-red-500/70" />
                    <span class="h-2.5 w-2.5 rounded-full bg-amber-500/70" />
                    <span class="h-2.5 w-2.5 rounded-full bg-emerald-500/70" />
                </div>
                <span class="font-mono text-[11px] text-zinc-500">{language}</span>
                {copy_btn}
            </div>
            <pre class="overflow-x-auto p-4 font-mono text-[13px] leading-6 text-zinc-300"><code>{code}</code></pre>
        </div>
    )


# ---------------------------------------------------------------------------
# Section: title + blurb + live demo + code, all in one
# ---------------------------------------------------------------------------

@component
def AnimSection(props=None):
    """One animation variant: heading, description, live preview, code."""
    props = props or {}
    title = props.get("title", "") if isinstance(props, dict) else getattr(props, "title", "")
    blurb = props.get("blurb", "") if isinstance(props, dict) else getattr(props, "blurb", "")
    code = props.get("code", "") if isinstance(props, dict) else getattr(props, "code", "")
    tall = props.get("tall", False) if isinstance(props, dict) else getattr(props, "tall", False)
    demo = props.get("demo") if isinstance(props, dict) else getattr(props, "demo", None)
    index = props.get("index", 0) if isinstance(props, dict) else getattr(props, "index", 0)
    num = f"{index + 1:02d}"
    blurb_el = el("p", "mt-0.5 text-sm text-zinc-500", blurb) if blurb else None

    return (
        <section class="mb-12">
            <div class="mb-4 flex items-baseline gap-3">
                <span class="font-mono text-xs text-zinc-600">{num}</span>
                <div>
                    <h3 class="text-lg font-semibold text-zinc-100">{title}</h3>
                    {blurb_el}
                </div>
            </div>
            <div class="grid gap-6 lg:grid-cols-2">
                <DemoFrame tall={tall}>{demo}</DemoFrame>
                <CodeBlock code={code} language="python" />
            </div>
        </section>
    )
