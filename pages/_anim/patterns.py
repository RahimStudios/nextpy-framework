"""Reusable animation pattern builders.

IMPORTANT: every ``demo()`` aliases closure values into true locals before
the ``return (`` JSX block — the PSX expression evaluator only sees
``f_locals``/``f_globals`` captured by ``psx()``, never enclosing freevars.
"""

from nextpy.psx import Motion, AnimatePresence, useState, interactive_component


def _card(extra=""):
    return f"w-80 rounded-xl border border-zinc-800 bg-zinc-900/60 p-6 text-center {extra}"


# ---------------------------------------------------------------------------
# entrance
# ---------------------------------------------------------------------------

def entrance(content="Hello", **kw):
    d = kw.get("duration", 0.5)
    delay = kw.get("delay", 0)
    easing = kw.get("easing", "cubic-bezier(0.22,1,0.36,1)")
    variant = kw.get("variant", "up")
    init_map = {
        "up": {"opacity": 0, "y": 24},
        "down": {"opacity": 0, "y": -24},
        "left": {"opacity": 0, "x": 32},
        "right": {"opacity": 0, "x": -32},
        "zoom": {"opacity": 0, "scale": 0.8},
        "fade": {"opacity": 0},
    }
    init = init_map[variant]
    anim = {"opacity": 1, "y": 0, "x": 0, "scale": 1}
    cls = kw.get("className", _card())
    code = f'''<Motion initial={{{init}}}
        animate={{{anim}}}
        transition={{"duration": {d}, "delay": {delay}, "easing": "{easing}"}}
        className="{cls}">
    {content}
</Motion>'''

    def demo():
        content_v, cls_v, init_v, anim_v = content, cls, init, anim
        d_v, delay_v, easing_v = d, delay, easing
        return (
            <Motion initial={init_v} animate={anim_v}
                    transition={{"duration": d_v, "delay": delay_v, "easing": easing_v}}
                    className={cls_v}>
                <span class="text-sm font-medium text-zinc-200">{content_v}</span>
            </Motion>
        )
    return demo, code


# ---------------------------------------------------------------------------
# gestures
# ---------------------------------------------------------------------------

def gestures(label="Hover me", **kw):
    hover = kw.get("hover", {"scale": 1.06, "y": -3})
    tap = kw.get("tap", {"scale": 0.94})
    dur = kw.get("duration", 0.18)
    cls = kw.get("className", "rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white shadow-lg shadow-blue-600/25")
    code = f'''<Motion as="button" whileHover={{{hover}}} whileTap={{{tap}}}
        transition={{"duration": {dur}}}
        className="{cls}">
    {label}
</Motion>'''

    def demo():
        label_v, cls_v, hover_v, tap_v, dur_v = label, cls, hover, tap, dur
        return (
            <Motion as="button" whileHover={hover_v} whileTap={tap_v}
                    transition={{"duration": dur_v}} className={cls_v}>
                {label_v}
            </Motion>
        )
    return demo, code


# ---------------------------------------------------------------------------
# pulse
# ---------------------------------------------------------------------------

def pulse(kind="opacity", **kw):
    dur = kw.get("duration", 1.6)
    content = kw.get("content", "Live")
    cls = kw.get("className", "rounded-full bg-emerald-500/15 px-4 py-1.5 text-xs font-semibold text-emerald-400")
    anim = {"scale": [1, 1.15, 1]} if kind == "scale" else \
           {"rotate": [0, 8, 0]} if kind == "rotate" else {"opacity": [1, 0.35, 1]}
    code = f'''<Motion as="span" animate={{{anim}}}
        transition={{"duration": {dur}, "easing": "ease-in-out"}}
        className="{cls}">
    {content}
</Motion>'''

    def demo():
        anim_v, dur_v, cls_v, content_v = anim, dur, cls, content
        return (
            <Motion as="span" animate={anim_v}
                    transition={{"duration": dur_v, "easing": "ease-in-out"}} className={cls_v}>
                {content_v}
            </Motion>
        )
    return demo, code


# ---------------------------------------------------------------------------
# shake
# ---------------------------------------------------------------------------

def shake(axis="x", **kw):
    dur = kw.get("duration", 0.5)
    content = kw.get("content", "Something went wrong")
    cls = kw.get("className", "w-80 rounded-lg border border-red-500/40 bg-red-500/10 p-4 text-sm text-red-200")
    anim = {"x": [0, -10, 10, -6, 6, 0]} if axis == "x" else {"y": [0, -8, 8, -5, 5, 0]}
    code = f'''<Motion animate={{{anim}}}
        transition={{"duration": {dur}, "easing": "ease-in-out"}}
        className="{cls}">
    {content}
</Motion>'''

    def demo():
        anim_v, dur_v, cls_v, content_v = anim, dur, cls, content
        return (
            <Motion animate={anim_v} transition={{"duration": dur_v, "easing": "ease-in-out"}} className={cls_v}>
                {content_v}
            </Motion>
        )
    return demo, code


# ---------------------------------------------------------------------------
# flip3d
# ---------------------------------------------------------------------------

def flip3d(axis="Y", **kw):
    dur = kw.get("duration", 2.4)
    content = kw.get("content", "3D")
    prop = f"rotate{axis}"
    anim = {prop: [0, 360]}
    cls = kw.get("className", "flex h-32 w-52 items-center justify-center rounded-xl border border-zinc-800 bg-gradient-to-br from-blue-600/30 to-violet-600/30")
    code = f'''<Motion animate={{{anim}}}
        transition={{"duration": {dur}, "easing": "ease-in-out"}}
        className="{cls}">
    {content}
</Motion>'''

    def demo():
        anim_v, dur_v, cls_v, content_v = anim, dur, cls, content
        return (
            <Motion animate={anim_v} transition={{"duration": dur_v, "easing": "ease-in-out"}} className={cls_v}>
                <span class="text-sm font-semibold text-zinc-200">{content_v}</span>
            </Motion>
        )
    return demo, code


# ---------------------------------------------------------------------------
# stagger — PSX {for i in range(n)} with items[i]
# ---------------------------------------------------------------------------

def stagger(items=None, **kw):
    items = list(items or ["One", "Two", "Three", "Four"])
    dur = kw.get("duration", 0.4)
    step = kw.get("step", 0.12)
    easing = kw.get("easing", "cubic-bezier(0.34,1.56,0.64,1)")
    cls = kw.get("itemClass", "rounded-lg bg-zinc-800 px-4 py-2 text-sm font-medium text-zinc-200")
    wrap = kw.get("wrapClass", "flex flex-wrap gap-2 justify-center")
    n = len(items)
    code = f'''# PSX for-loop + transition.delay per index
{{for i in range({n}):
    <Motion key={{i}} initial={{"scale": 0, "opacity": 0}}
            animate={{"scale": 1, "opacity": 1}}
            transition={{"duration": {dur}, "delay": i * {step}, "easing": "{easing}"}}
            className="{cls}">
        {{items[i]}}
    </Motion>
}}'''

    def demo():
        items_v, dur_v, step_v, easing_v, cls_v, wrap_v, n_v = items, dur, step, easing, cls, wrap, n
        return (
            <div class={wrap_v}>
                {for i in range(n_v):
                    <Motion key={i} initial={{"scale": 0, "opacity": 0}}
                            animate={{"scale": 1, "opacity": 1}}
                            transition={{"duration": dur_v, "delay": i * step_v, "easing": easing_v}}
                            className={cls_v}>
                        {items_v[i]}
                    </Motion>
                }
            </div>
        )
    return demo, code


# ---------------------------------------------------------------------------
# progress
# ---------------------------------------------------------------------------

def progress(mode="fill", pct=72, **kw):
    dur = kw.get("duration", 1.4)
    if mode == "fill":
        inner_cls = "h-full rounded-full bg-blue-500"
        code = f'''<Motion initial={{"width": "0%"}} animate={{"width": "{pct}%"}}
        transition={{"duration": {dur}, "easing": "cubic-bezier(0.22,1,0.36,1)"}}
        className="{inner_cls}" />'''

        def demo():
            pct_v, dur_v, cls_v = pct, dur, inner_cls
            return (
                <div class="w-80">
                    <div class="h-2.5 w-full overflow-hidden rounded-full bg-zinc-800">
                        <Motion initial={{"width": "0%"}} animate={{"width": f"{pct_v}%"}}
                                transition={{"duration": dur_v, "easing": "cubic-bezier(0.22,1,0.36,1)"}}
                                className={cls_v} />
                    </div>
                </div>
            )
    else:
        inner_cls = "absolute h-full w-1/3 rounded-full bg-blue-400"
        code = f'''<Motion animate={{"x": ["-120%", "320%"]}}
        transition={{"duration": {dur}, "easing": "ease-in-out"}}
        className="{inner_cls}" />'''

        def demo():
            dur_v, cls_v = dur, inner_cls
            return (
                <div class="w-80">
                    <div class="relative h-2.5 w-full overflow-hidden rounded-full bg-zinc-800">
                        <Motion animate={{"x": ["-120%", "320%"]}}
                                transition={{"duration": dur_v, "easing": "ease-in-out"}}
                                className={cls_v} />
                    </div>
                </div>
            )
    return demo, code


# ---------------------------------------------------------------------------
# spinner
# ---------------------------------------------------------------------------

def spinner(kind="ring", **kw):
    dur = kw.get("duration", 1)
    size = kw.get("size", "h-10 w-10")
    if kind == "dots":
        code = f'''# Dots pulse in sequence via transition.delay
{{for i in range(3):
    <Motion key={{i}} animate={{"opacity": [0.3, 1, 0.3]}}
            transition={{"duration": {dur}, "delay": i * 0.2}}
            className="h-3 w-3 rounded-full bg-blue-400" />
}}'''

        def demo():
            dur_v = dur
            return (
                <div class="flex gap-2">
                    {for i in range(3):
                        <Motion key={i} animate={{"opacity": [0.3, 1, 0.3]}}
                                transition={{"duration": dur_v, "delay": i * 0.2}}
                                className="h-3 w-3 rounded-full bg-blue-400" />
                    }
                </div>
            )
    else:
        cls = f"{size} rounded-full border-4 border-zinc-700 border-t-blue-500"
        code = f'''<Motion animate={{"rotate": [0, 360]}}
        transition={{"duration": {dur}, "easing": "linear"}}
        className="{cls}" />'''

        def demo():
            dur_v, cls_v = dur, cls
            return (
                <Motion animate={{"rotate": [0, 360]}}
                        transition={{"duration": dur_v, "easing": "linear"}}
                        className={cls_v} />
            )
    return demo, code


# ---------------------------------------------------------------------------
# dialog
# ---------------------------------------------------------------------------

def dialog(**kw):
    dur = kw.get("duration", 0.3)
    title = kw.get("title", "Dialog")
    body = kw.get("body", "This panel scales and fades in over a dimmed backdrop.")
    code = f'''# Pair with AnimatePresence for exit animations
<Motion initial={{"opacity": 0, "scale": 0.92, "y": 16}}
        animate={{"opacity": 1, "scale": 1, "y": 0}}
        exit={{"opacity": 0, "scale": 0.95, "y": 8}}
        transition={{"duration": {dur}, "easing": "ease-out"}}
        className="w-80 rounded-xl border border-zinc-800 bg-zinc-900 p-6">
    <h3 class="font-semibold text-zinc-100">{title}</h3>
    <p class="mt-2 text-sm text-zinc-400">{body}</p>
</Motion>'''

    def demo():
        dur_v, title_v, body_v = dur, title, body
        return (
            <div class="relative p-4">
                <Motion initial={{"opacity": 0}} animate={{"opacity": 1}}
                        className="absolute rounded-xl bg-black/50" style="inset:0" />
                <Motion initial={{"opacity": 0, "scale": 0.9, "y": 14}} animate={{"opacity": 1, "scale": 1, "y": 0}}
                        transition={{"duration": dur_v, "easing": "ease-out"}}
                        className="relative w-80 rounded-xl border border-zinc-800 bg-zinc-900 p-6 shadow-2xl">
                    <h3 class="font-semibold text-zinc-100">{title_v}</h3>
                    <p class="mt-2 text-sm text-zinc-400">{body_v}</p>
                </Motion>
            </div>
        )
    return demo, code


# ---------------------------------------------------------------------------
# drawer
# ---------------------------------------------------------------------------

def drawer(edge="right", **kw):
    dur = kw.get("duration", 0.35)
    content = kw.get("content", "Panel content")
    axes = {"right": {"x": [40, 0]}, "left": {"x": [-40, 0]},
            "top": {"y": [-40, 0]}, "bottom": {"y": [40, 0]}}
    anim = axes[edge]
    init = {k: v[0] for k, v in anim.items()}
    tgt = {k: v[1] for k, v in anim.items()}
    init["opacity"] = 0
    tgt["opacity"] = 1
    code = f'''<Motion initial={{{init}}} animate={{{tgt}}}
        transition={{"duration": {dur}, "easing": "ease-out"}}
        className="w-64 rounded-xl border border-zinc-800 bg-zinc-900 p-5">
    {content}
</Motion>'''

    def demo():
        init_v, tgt_v, dur_v, content_v = init, tgt, dur, content
        return (
            <Motion initial={init_v} animate={tgt_v}
                    transition={{"duration": dur_v, "easing": "ease-out"}}
                    className="w-64 rounded-xl border border-zinc-800 bg-zinc-900 p-5">
                <p class="text-sm text-zinc-300">{content_v}</p>
            </Motion>
        )
    return demo, code


# ---------------------------------------------------------------------------
# accordion — height tween
# ---------------------------------------------------------------------------

def accordion_open(content="Hidden details revealed with a height tween.", **kw):
    dur = kw.get("duration", 0.4)
    code = f'''<Motion initial={{"opacity": 0, "maxHeight": "0px"}}
        animate={{"opacity": 1, "maxHeight": "200px"}}
        exit={{"opacity": 0, "maxHeight": "0px"}}
        transition={{"duration": {dur}, "easing": "ease-in-out"}}
        className="overflow-hidden">
    <div class="p-4 text-sm text-zinc-400">{content}</div>
</Motion>'''

    def demo():
        dur_v, content_v = dur, content
        return (
            <div class="w-80 overflow-hidden rounded-xl border border-zinc-800 bg-zinc-900/50">
                <div class="border-b border-zinc-800 px-4 py-3 text-sm font-medium text-zinc-200">Section</div>
                <Motion initial={{"opacity": 0, "maxHeight": "0px"}} animate={{"opacity": 1, "maxHeight": "160px"}}
                        transition={{"duration": dur_v, "easing": "ease-in-out"}}
                        className="overflow-hidden">
                    <div class="p-4 text-sm text-zinc-400">{content_v}</div>
                </Motion>
            </div>
        )
    return demo, code


# ---------------------------------------------------------------------------
# tabs indicator
# ---------------------------------------------------------------------------

def tabs_indicator(**kw):
    code = '''# Underline indicator — layout animation or x/width tween
<Motion layout className="absolute bottom-0 h-0.5 bg-blue-500" />'''

    def demo():
        return (
            <div class="flex gap-6 border-b border-zinc-800 pb-2">
                <span class="text-sm font-medium text-zinc-100">Account</span>
                <span class="relative text-sm font-medium text-zinc-400">
                    Security
                    <Motion layout initial={False} animate={{"x": 0}}
                            className="absolute -bottom-2.5 left-0 h-0.5 w-full bg-blue-500" />
                </span>
                <span class="text-sm font-medium text-zinc-400">Billing</span>
            </div>
        )
    return demo, code


# ---------------------------------------------------------------------------
# toast
# ---------------------------------------------------------------------------

def toast(**kw):
    dur = kw.get("duration", 0.4)
    msg = kw.get("message", "Event saved")
    code = f'''<Motion initial={{"opacity": 0, "y": 30, "scale": 0.95}}
        animate={{"opacity": 1, "y": 0, "scale": 1}}
        exit={{"opacity": 0, "y": 10, "scale": 0.97}}
        transition={{"duration": {dur}, "easing": "ease-out"}}
        className="flex items-center gap-3 rounded-lg border border-zinc-700 bg-zinc-900 px-4 py-3 text-sm text-zinc-100 shadow-2xl">
    <span class="h-2 w-2 rounded-full bg-emerald-400" />
    {msg}
</Motion>'''

    def demo():
        dur_v, msg_v = dur, msg
        return (
            <Motion initial={{"opacity": 0, "y": 30, "scale": 0.95}} animate={{"opacity": 1, "y": 0, "scale": 1}}
                    transition={{"duration": dur_v, "easing": "ease-out"}}
                    className="flex items-center gap-3 rounded-lg border border-zinc-700 bg-zinc-900 px-4 py-3 text-sm text-zinc-100 shadow-2xl">
                <span class="h-2 w-2 rounded-full bg-emerald-400" />
                {msg_v}
            </Motion>
        )
    return demo, code


# ---------------------------------------------------------------------------
# shimmer
# ---------------------------------------------------------------------------

def shimmer(**kw):
    dur = kw.get("duration", 1.6)
    code = f'''<div class="relative w-64 overflow-hidden rounded-md bg-zinc-800 h-4">
    <Motion animate={{"x": ["-100%", "220%"]}}
            transition={{"duration": {dur}, "easing": "ease-in-out"}}
            className="absolute inset-y-0 w-1/2 bg-gradient-to-r from-transparent via-zinc-600/60 to-transparent" />
</div>'''

    def demo():
        dur_v = dur
        return (
            <div class="flex w-72 flex-col gap-3">
                <div class="relative h-4 w-3/4 overflow-hidden rounded-md bg-zinc-800">
                    <Motion animate={{"x": ["-100%", "220%"]}}
                            transition={{"duration": dur_v, "easing": "ease-in-out"}}
                            className="absolute inset-y-0 w-1/2 bg-gradient-to-r from-transparent via-zinc-600/60 to-transparent" />
                </div>
                <div class="relative h-4 w-1/2 overflow-hidden rounded-md bg-zinc-800">
                    <Motion animate={{"x": ["-100%", "220%"]}}
                            transition={{"duration": dur_v, "delay": 0.2, "easing": "ease-in-out"}}
                            className="absolute inset-y-0 w-1/2 bg-gradient-to-r from-transparent via-zinc-600/60 to-transparent" />
                </div>
            </div>
        )
    return demo, code


# ---------------------------------------------------------------------------
# typing
# ---------------------------------------------------------------------------

def typing(text="Compiling…", **kw):
    dur = kw.get("duration", 2)
    code = f'''# steps() easing gives a typewriter cadence
<Motion animate={{"width": ["0%", "100%"]}}
        transition={{"duration": {dur}, "easing": "steps(12)"}}
        className="h-4 overflow-hidden whitespace-nowrap text-sm text-zinc-300">
    {text}
</Motion>'''

    def demo():
        dur_v, text_v = dur, text
        return (
            <Motion animate={{"width": ["0%", "100%"]}}
                    transition={{"duration": dur_v, "easing": "steps(12)"}}
                    className="h-5 overflow-hidden whitespace-nowrap font-mono text-sm text-emerald-300">
                {text_v}
            </Motion>
        )
    return demo, code


# ---------------------------------------------------------------------------
# marquee
# ---------------------------------------------------------------------------

def marquee(items=None, **kw):
    items = list(items or ["PSX", "Motion", "WAAPI", "SSR", "Hydration", "Signals"])
    doubled = items + items
    dur = kw.get("duration", 12)
    code = f'''# Duplicate the list, translate -50%, loop linearly
<Motion animate={{"x": ["0%", "-50%"]}}
        transition={{"duration": {dur}, "easing": "linear"}}
        className="flex w-max gap-8">
    {{for label in {doubled!r}:
        <span className="text-sm font-semibold text-zinc-400">{{label}}</span>
    }}
</Motion>'''

    def demo():
        doubled_v, dur_v = doubled, dur
        return (
            <div class="w-80 overflow-hidden">
                <Motion animate={{"x": ["0%", "-50%"]}}
                        transition={{"duration": dur_v, "easing": "linear"}}
                        className="flex w-max gap-8">
                    {for label in doubled_v:
                        <span class="text-sm font-semibold text-zinc-400">{label}</span>
                    }
                </Motion>
            </div>
        )
    return demo, code


# ---------------------------------------------------------------------------
# burst
# ---------------------------------------------------------------------------

def burst(**kw):
    dur = kw.get("duration", 0.9)
    code = f'''# Particles fly outward then fade — keyframe arrays per particle
{{for i in range(8):
    <Motion key={{i}}
            initial={{"x": 0, "y": 0, "opacity": 1, "scale": 1}}
            animate={{"x": (i % 4 - 1.5) * 40, "y": -60 - (i % 3) * 30,
                      "opacity": [1, 1, 0], "scale": [1, 1, 0.4]}}
            transition={{"duration": {dur}, "delay": i * 0.03}} />
}}'''

    def demo():
        dur_v = dur
        return (
            <div class="relative flex h-24 w-24 items-center justify-center">
                <Motion animate={{"scale": [1, 1.3, 1]}} transition={{"duration": 0.6, "easing": "ease-in-out"}}
                        className="flex h-14 w-14 items-center justify-center rounded-full bg-emerald-500/20 text-2xl">!</Motion>
                {for i in range(8):
                    <Motion key={i}
                            initial={{"x": 0, "y": 0, "opacity": 1, "scale": 1}}
                            animate={{"x": (i % 4 - 1.5) * 34, "y": -50 - (i % 3) * 26,
                                      "opacity": [1, 1, 0], "scale": [1, 1, 0.3]}}
                            transition={{"duration": dur_v, "delay": i * 0.03}}
                            className={"absolute h-2 w-2 rounded-full " + ["bg-blue-400","bg-emerald-400","bg-amber-400","bg-violet-400"][i % 4]} />
                }
            </div>
        )
    return demo, code


# ---------------------------------------------------------------------------
# parallax-card — mouse-tracked tilt via onmousemove + state (interactive)
# ---------------------------------------------------------------------------

@interactive_component
def _parallax_demo():
    [rx, set_rx] = useState(0)
    [ry, set_ry] = useState(0)

    def Move(e):
        rect = e.currentTarget.getBoundingClientRect()
        px = (e.clientX - rect.left) / rect.width - 0.5
        py = (e.clientY - rect.top) / rect.height - 0.5
        set_rx(py * -18)
        set_ry(px * 18)

    def Leave(e):
        set_rx(0)
        set_ry(0)

    return (
        <Motion animate={{"rotateX": rx, "rotateY": ry}}
                transition={{"duration": 0.25, "easing": "ease-out"}}
                onmousemove={Move} onmouseleave={Leave}
                className="flex h-44 w-72 cursor-pointer items-center justify-center rounded-xl border border-zinc-800 bg-gradient-to-br from-blue-600/30 to-violet-600/30 shadow-2xl">
            <span class="text-sm font-semibold text-zinc-200">Move your mouse</span>
        </Motion>
    )


def parallax(**kw):
    code = '''# Mouse-tracked 3D tilt — onmousemove updates state,
# Motion tweens rotateX/rotateY toward it
@interactive_component
def TiltCard():
    [rx, set_rx] = useState(0)
    [ry, set_ry] = useState(0)

    def Move(e):
        rect = e.currentTarget.getBoundingClientRect()
        set_rx(((e.clientY - rect.top) / rect.height - 0.5) * -18)
        set_ry(((e.clientX - rect.left) / rect.width - 0.5) * 18)

    return (
        <Motion animate={{"rotateX": rx, "rotateY": ry}}
                transition={{"duration": 0.25, "easing": "ease-out"}}
                onmousemove={Move} className="…card…">
            …
        </Motion>
    )'''
    return _parallax_demo, code


# ---------------------------------------------------------------------------
# count-up — number tween via keyframes
# ---------------------------------------------------------------------------

def countup(target=100, **kw):
    dur = kw.get("duration", 1.6)
    code = f'''# Number tween — animate a width/opacity proxy or use rAF;
# simplest: keyframe the displayed value via steps is limited,
# so tween a bar and show the target statically'''
    # Numbers can't tween as text in WAAPI — show an odometer-style slot
    # machine instead: columns of digits translating.
    digits = list(str(target))
    code = f'''# Odometer: each digit column translates to its final value
{{for d in {digits!r}:
    <Motion animate={{"y": ["0%", f"-{int(d) * 10}%"]}}
            transition={{"duration": {dur}, "easing": "cubic-bezier(0.22,1,0.36,1)"}}
            className="inline-block h-8 overflow-hidden">
        <div class="flex flex-col">
            {{for n in range(10):
                <span className="flex h-8 items-center justify-center font-mono text-2xl font-bold text-zinc-100">{{n}}</span>
            }}
        </div>
    </Motion>
}}'''

    def demo():
        digits_v, dur_v = digits, dur
        return (
            <div class="flex items-end gap-1">
                {for d in digits_v:
                    <Motion animate={{"y": ["0%", f"-{int(d) * 10}%"]}}
                            transition={{"duration": dur_v, "delay": 0.2, "easing": "cubic-bezier(0.22,1,0.36,1)"}}
                            className="inline-block h-9 overflow-hidden">
                        <div class="flex flex-col">
                            {for n in range(10):
                                <span class="flex h-9 items-center justify-center font-mono text-2xl font-bold text-zinc-100">{n}</span>
                            }
                        </div>
                    </Motion>
                }
                <span class="ml-1 text-sm text-zinc-500">users</span>
            </div>
        )
    return demo, code


# ---------------------------------------------------------------------------
# registry
# ---------------------------------------------------------------------------

PATTERNS = {
    "entrance": entrance,
    "gestures": gestures,
    "pulse": pulse,
    "shake": shake,
    "flip3d": flip3d,
    "stagger": stagger,
    "progress": progress,
    "spinner": spinner,
    "dialog": dialog,
    "drawer": drawer,
    "accordion": accordion_open,
    "tabs": tabs_indicator,
    "toast": toast,
    "shimmer": shimmer,
    "typing": typing,
    "marquee": marquee,
    "burst": burst,
    "parallax": parallax,
    "countup": countup,
}


def variant(pattern, vtitle, vblurb, **params):
    """Build a variant dict {title, blurb, code, demo, tall} from a pattern."""
    demo, code = PATTERNS[pattern](**params)
    return {"title": vtitle, "blurb": vblurb, "code": code, "demo": demo,
            "tall": params.get("tall", False)}
