"""Animation variants for primitive/display components.

Each variant dict: title, blurb, tall, code (copy-paste), demo (function
returning JSX — must be a def with ``return (``, never a lambda).
"""

VARIANTS = {}


# ---------------- Button ----------------

def _btn_hover():
    return (
        <div class="flex items-center gap-6">
            <Motion as="button" whileHover={{"scale": 1.06, "y": -2}} whileTap={{"scale": 0.94}}
                    transition={{"duration": 0.15, "easing": "ease-out"}}
                    className="rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white shadow-lg shadow-blue-600/30">
                Save
            </Motion>
            <Motion as="button" whileHover={{"scale": 1.06, "y": -2}} whileTap={{"scale": 0.94}}
                    transition={{"duration": 0.15}}
                    className="rounded-lg border border-zinc-700 px-6 py-3 font-semibold text-zinc-200">
                Cancel
            </Motion>
        </div>
    )


def _btn_loading():
    return (
        <Motion as="button" animate={{"opacity": [1, 0.55, 1]}}
                transition={{"duration": 1.1, "easing": "ease-in-out"}}
                className="rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white">
            Processing
        </Motion>
    )


def _btn_pop():
    return (
        <Motion initial={{"scale": 0, "opacity": 0}} animate={{"scale": 1, "opacity": 1}}
                transition={{"duration": 0.55, "easing": "cubic-bezier(0.34,1.56,0.64,1)"}}
                className="rounded-lg bg-emerald-600 px-6 py-3 font-semibold text-white">
            Get started
        </Motion>
    )


VARIANTS["button"] = [
    {"title": "Hover & tap gestures", "blurb": "whileHover lifts and scales; whileTap presses down — pure WAAPI, zero JS bundle.",
     "code": '''from nextpy.psx import Motion

<Motion as="button" whileHover={{"scale": 1.05, "y": -2}}
        whileTap={{"scale": 0.95}}
        transition={{"duration": 0.15}}
        className="rounded-lg bg-blue-600 px-5 py-2.5 font-semibold text-white">
    Save changes
</Motion>''',
     "demo": _btn_hover},
    {"title": "Loading pulse", "blurb": "Keyframed opacity loop while an action runs.",
     "code": '''<Motion as="button" animate={{"opacity": [1, 0.55, 1]}}
        transition={{"duration": 1.1, "easing": "ease-in-out"}}
        className="rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white">
    Processing…
</Motion>''',
     "demo": _btn_loading},
    {"title": "Springy entrance", "blurb": "Overshoot easing gives a playful pop on mount.",
     "code": '''<Motion initial={{"scale": 0, "opacity": 0}}
        animate={{"scale": 1, "opacity": 1}}
        transition={{"duration": 0.55, "easing": "cubic-bezier(0.34,1.56,0.64,1)"}}
        className="rounded-lg bg-emerald-600 px-6 py-3 font-semibold text-white">
    Get started
</Motion>''',
     "demo": _btn_pop},
]


# ---------------- Badge ----------------

def _badge_pulse():
    return (
        <div class="flex gap-3">
            <Motion as="span" animate={{"opacity": [1, 0.35, 1]}}
                    transition={{"duration": 1.6, "easing": "ease-in-out"}}
                    className="rounded-full bg-emerald-500/15 px-3 py-1 text-xs font-semibold text-emerald-400">
                Live
            </Motion>
            <Motion as="span" animate={{"scale": [1, 1.12, 1]}}
                    transition={{"duration": 2, "easing": "ease-in-out"}}
                    className="rounded-full bg-blue-500/15 px-3 py-1 text-xs font-semibold text-blue-400">
                New
            </Motion>
        </div>
    )


def _badge_stagger():
    return (
        <div class="flex gap-2">
            <Motion as="span" initial={{"scale": 0, "opacity": 0}} animate={{"scale": 1, "opacity": 1}}
                    transition={{"duration": 0.4, "delay": 0, "easing": "cubic-bezier(0.34,1.56,0.64,1)"}}
                    className="rounded-full bg-zinc-800 px-3 py-1 text-xs font-semibold text-zinc-300">Stable</Motion>
            <Motion as="span" initial={{"scale": 0, "opacity": 0}} animate={{"scale": 1, "opacity": 1}}
                    transition={{"duration": 0.4, "delay": 0.12, "easing": "cubic-bezier(0.34,1.56,0.64,1)"}}
                    className="rounded-full bg-zinc-800 px-3 py-1 text-xs font-semibold text-zinc-300">Beta</Motion>
            <Motion as="span" initial={{"scale": 0, "opacity": 0}} animate={{"scale": 1, "opacity": 1}}
                    transition={{"duration": 0.4, "delay": 0.24, "easing": "cubic-bezier(0.34,1.56,0.64,1)"}}
                    className="rounded-full bg-zinc-800 px-3 py-1 text-xs font-semibold text-zinc-300">v2.0</Motion>
        </div>
    )


VARIANTS["badge"] = [
    {"title": "Attention pulse", "blurb": "Infinite opacity/scale loops for live status.",
     "code": '''<Motion as="span" animate={{"opacity": [1, 0.4, 1]}}
        transition={{"duration": 1.6, "easing": "ease-in-out"}}
        className="rounded-full bg-emerald-500/15 px-3 py-1 text-xs font-semibold text-emerald-400">
    Live
</Motion>''',
     "demo": _badge_pulse},
    {"title": "Staggered entrance", "blurb": "transition.delay sequences multiple badges.",
     "code": '''# One Motion per badge, increasing delay
<Motion as="span" initial={{"scale": 0, "opacity": 0}}
        animate={{"scale": 1, "opacity": 1}}
        transition={{"duration": 0.4, "delay": 0.12,
                     "easing": "cubic-bezier(0.34,1.56,0.64,1)"}}
        className="rounded-full bg-zinc-800 px-3 py-1 text-xs font-semibold text-zinc-300">
    Beta
</Motion>''',
     "demo": _badge_stagger},
]


# ---------------- Alert ----------------

def _alert_slide():
    return (
        <div class="flex w-96 flex-col gap-3">
            <Motion initial={{"x": -30, "opacity": 0}} animate={{"x": 0, "opacity": 1}}
                    transition={{"duration": 0.5, "easing": "ease-out"}}
                    className="rounded-lg border border-emerald-500/40 bg-emerald-500/10 p-4 text-sm text-emerald-200">
                Saved successfully — slide-in from the left.
            </Motion>
            <Motion initial={{"y": 20, "opacity": 0}} animate={{"y": 0, "opacity": 1}}
                    transition={{"duration": 0.5, "delay": 0.15, "easing": "ease-out"}}
                    className="rounded-lg border border-amber-500/40 bg-amber-500/10 p-4 text-sm text-amber-200">
                Warning — drops in from above.
            </Motion>
        </div>
    )


def _alert_shake():
    return (
        <Motion animate={{"x": [0, -8, 8, -5, 5, 0]}}
                transition={{"duration": 0.5, "easing": "ease-in-out"}}
                className="w-96 rounded-lg border border-red-500/40 bg-red-500/10 p-4 text-sm text-red-200">
            Error — shake keyframes signal something failed.
        </Motion>
    )


VARIANTS["alert"] = [
    {"title": "Slide & drop entrances", "blurb": "Directional entrances per severity.",
     "code": '''<Motion initial={{"x": -30, "opacity": 0}}
        animate={{"x": 0, "opacity": 1}}
        transition={{"duration": 0.5, "easing": "ease-out"}}
        className="rounded-lg border border-emerald-500/40 bg-emerald-500/10 p-4 text-sm text-emerald-200">
    Saved successfully
</Motion>''',
     "demo": _alert_slide},
    {"title": "Error shake", "blurb": "Keyframe x offsets produce a shake.",
     "code": '''<Motion animate={{"x": [0, -8, 8, -5, 5, 0]}}
        transition={{"duration": 0.5, "easing": "ease-in-out"}}
        className="rounded-lg border border-red-500/40 bg-red-500/10 p-4 text-sm text-red-200">
    Something went wrong
</Motion>''',
     "demo": _alert_shake},
]


# ---------------- Card ----------------

def _card_hover():
    return (
        <Motion whileHover={{"y": -6, "scale": 1.02}} whileTap={{"scale": 0.98}}
                transition={{"duration": 0.25, "easing": "ease-out"}}
                className="w-72 cursor-pointer rounded-xl border border-zinc-800 bg-zinc-900/60 p-6 shadow-xl">
            <p class="text-xs font-semibold uppercase tracking-widest text-blue-400">Project</p>
            <h3 class="mt-1 text-lg font-bold text-zinc-100">Aurora dashboard</h3>
            <p class="mt-2 text-sm text-zinc-500">Hover me — the whole card lifts with a spring.</p>
        </Motion>
    )


def _card_flip():
    return (
        <Motion animate={{"rotateY": [0, 360]}}
                transition={{"duration": 2.4, "easing": "ease-in-out"}}
                className="flex h-36 w-56 items-center justify-center rounded-xl border border-zinc-800 bg-gradient-to-br from-blue-600/30 to-violet-600/30">
            <span class="text-sm font-semibold text-zinc-200">3D flip loop</span>
        </Motion>
    )


VARIANTS["card"] = [
    {"title": "Lift on hover", "blurb": "whileHover translate + scale, whileTap press.",
     "code": '''<Motion whileHover={{"y": -6, "scale": 1.02}} whileTap={{"scale": 0.98}}
        transition={{"duration": 0.25, "easing": "ease-out"}}
        className="w-72 rounded-xl border border-zinc-800 bg-zinc-900/60 p-6">
    …card content…
</Motion>''',
     "demo": _card_hover},
    {"title": "3D flip", "blurb": "rotateY keyframes spin the card in 3D.",
     "code": '''<Motion animate={{"rotateY": [0, 360]}}
        transition={{"duration": 2.4, "easing": "ease-in-out"}}
        className="h-36 w-56 rounded-xl bg-gradient-to-br from-blue-600/30 to-violet-600/30">
    …
</Motion>''',
     "demo": _card_flip},
]


# ---------------- Avatar ----------------

def _avatar():
    return (
        <div class="flex items-center gap-4">
            <Motion initial={{"scale": 0}} animate={{"scale": 1}}
                    transition={{"duration": 0.5, "delay": 0, "easing": "cubic-bezier(0.34,1.56,0.64,1)"}}
                    className="flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-br from-blue-600 to-violet-600 text-lg font-bold text-white">A</Motion>
            <Motion initial={{"scale": 0}} animate={{"scale": 1}}
                    transition={{"duration": 0.5, "delay": 0.12, "easing": "cubic-bezier(0.34,1.56,0.64,1)"}}
                    whileHover={{"scale": 1.15, "rotate": 8}}
                    className="flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-br from-emerald-600 to-teal-600 text-lg font-bold text-white">G</Motion>
            <Motion initial={{"scale": 0}} animate={{"scale": 1}}
                    transition={{"duration": 0.5, "delay": 0.24, "easing": "cubic-bezier(0.34,1.56,0.64,1)"}}
                    className="flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-br from-amber-600 to-orange-600 text-lg font-bold text-white">T</Motion>
        </div>
    )


VARIANTS["avatar"] = [
    {"title": "Staggered pop-in", "blurb": "Each avatar springs in with delay; hover tilts one.",
     "code": '''# Delay per avatar: transition={{"delay": index * 0.12}}
<Motion initial={{"scale": 0}} animate={{"scale": 1}}
        transition={{"duration": 0.5, "delay": 0.12,
                     "easing": "cubic-bezier(0.34,1.56,0.64,1)"}}
        whileHover={{"scale": 1.15, "rotate": 8}}
        className="flex h-14 w-14 items-center justify-center rounded-full bg-blue-600 text-white">
    G
</Motion>''',
     "demo": _avatar},
]


# ---------------- Progress ----------------

def _progress():
    return (
        <div class="w-80">
            <Motion initial={{"width": "0%"}} animate={{"width": "72%"}}
                    transition={{"duration": 1.4, "easing": "cubic-bezier(0.22,1,0.36,1)"}}
                    className="h-2.5 rounded-full bg-blue-500" />
            <p class="mt-2 text-xs text-zinc-500">width tweens from 0% to 72%</p>
        </div>
    )


def _progress_fill():
    return (
        <div class="w-80">
            <div class="h-2.5 w-full overflow-hidden rounded-full bg-zinc-800">
                <Motion initial={{"width": "0%"}} animate={{"width": "72%"}}
                        transition={{"duration": 1.4, "easing": "cubic-bezier(0.22,1,0.36,1)"}}
                        className="h-full rounded-full bg-blue-500" />
            </div>
            <p class="mt-2 text-xs text-zinc-500">Fill tweens width 0% → 72%</p>
        </div>
    )


def _progress_sweep():
    return (
        <div class="w-80">
            <div class="relative h-2.5 w-full overflow-hidden rounded-full bg-zinc-800">
                <Motion animate={{"x": ["-120%", "320%"]}}
                        transition={{"duration": 1.4, "easing": "ease-in-out"}}
                        className="absolute h-full w-1/3 rounded-full bg-blue-400" />
            </div>
            <p class="mt-2 text-xs text-zinc-500">Indeterminate sweep via translateX keyframes</p>
        </div>
    )


VARIANTS["progress"] = [
    {"title": "Determinate fill", "blurb": "Width tweens from 0 to the target value.",
     "code": '''<Motion initial={{"width": "0%"}} animate={{"width": "72%"}}
        transition={{"duration": 1.4, "easing": "cubic-bezier(0.22,1,0.36,1)"}}
        className="h-full rounded-full bg-blue-500" />''',
     "demo": _progress_fill},
    {"title": "Indeterminate sweep", "blurb": "A highlight slides across an unknown-duration task.",
     "code": '''<Motion animate={{"x": ["-120%", "320%"]}}
        transition={{"duration": 1.4, "easing": "ease-in-out"}}
        className="absolute h-full w-1/3 rounded-full bg-blue-400" />''',
     "demo": _progress_sweep},
]
