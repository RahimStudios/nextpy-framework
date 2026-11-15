"""Animation playground registry — catalog, variants, page factory.

Routes: /animation-playground/<group>/<slug>
Groups are subfolders: components, ai, utilities, get-started,
integrations, registry, api.
"""

from nextpy.psx import component, Link
from .base import AnimSection, el
from . import patterns


GROUPS = [
    ("components", "Components"),
    ("ai", "AI Elements"),
    ("utilities", "Utilities"),
    ("get-started", "Get Started"),
    ("integrations", "Integrations"),
    ("registry", "Registry"),
    ("api", "API Reference"),
]

# slug -> (name, group, one-line description)
ITEMS = {
    # ---------------- Components ----------------
    "accordion": ("Accordion", "components", "Expand/collapse sections with height tweens and staggered items."),
    "alert": ("Alert", "components", "Inline alerts — slide, drop, shake and pulse entrances."),
    "alert-dialog": ("Alert Dialog", "components", "Confirmation modal with backdrop fade and panel zoom."),
    "aspect-ratio": ("Aspect Ratio", "components", "Fixed-ratio containers with animated reveals."),
    "attachment": ("Attachment", "components", "File chips with hover lift and remove animation."),
    "avatar": ("Avatar", "components", "Avatar groups that spring in and tilt on hover."),
    "badge": ("Badge", "components", "Status badges with pulse, scale and staggered entrances."),
    "breadcrumb": ("Breadcrumb", "components", "Trail links with staggered fade-ins."),
    "bubble": ("Bubble", "components", "Chat bubbles that pop in from either side."),
    "button": ("Button", "components", "Buttons with hover/tap gestures, loading pulse and spring pop."),
    "button-group": ("Button Group", "components", "Attached buttons with shared hover and press states."),
    "calendar": ("Calendar", "components", "Month grids with day-cell hover and selection pop."),
    "card": ("Card", "components", "Cards that lift on hover, flip in 3D and stagger in."),
    "carousel": ("Carousel", "components", "Slide tracks translated by keyframes with dot indicators."),
    "chart": ("Chart", "components", "Bars and lines that draw in with scale/width tweens."),
    "checkbox": ("Checkbox", "components", "Checkboxes with check-mark scale pop and ripple."),
    "code-block": ("Code Block", "components", "Code windows with typing reveal and copy feedback."),
    "collapsible": ("Collapsible", "components", "Show/hide regions animated by maxHeight."),
    "combobox": ("Combobox", "components", "Searchable dropdowns with filtered-list transitions."),
    "command": ("Command", "components", "⌘K palettes that scale in over a blurred backdrop."),
    "context-menu": ("Context Menu", "components", "Right-click menus that scale from the cursor."),
    "data-table": ("Data Table", "components", "Sortable rows with hover highlights and layout shifts."),
    "date-picker": ("Date Picker", "components", "Calendar popovers with month-slide transitions."),
    "dialog": ("Dialog", "components", "Modals with backdrop fade, panel zoom and exit shrink."),
    "direction": ("Direction", "components", "RTL/LTR wrappers — layout flips animate smoothly."),
    "drawer": ("Drawer", "components", "Edge panels that slide in from any side."),
    "dropdown-menu": ("Dropdown Menu", "components", "Menus that scale+fade from their trigger."),
    "empty": ("Empty", "components", "Empty states with gentle float and fade entrances."),
    "field": ("Field", "components", "Label/control wrappers with focus-ring transitions."),
    "hover-card": ("Hover Card", "components", "Hover-reveal cards with delayed fade-up."),
    "input": ("Input", "components", "Inputs with focus ring glow and shake-on-error."),
    "input-group": ("Input Group", "components", "Addon-attached inputs with segmented focus states."),
    "input-otp": ("Input OTP", "components", "OTP cells that pop as digits arrive."),
    "item": ("Item", "components", "List rows with hover slide and icon wiggle."),
    "kbd": ("Kbd", "components", "Key caps with press-down scale on active."),
    "label": ("Label", "components", "Form labels with subtle emphasis transitions."),
    "marker": ("Marker", "components", "Inline highlights that sweep in behind text."),
    "menubar": ("Menubar", "components", "Menu bars whose dropdowns scale from the item."),
    "message": ("Message", "components", "Chat messages that pop from their side."),
    "message-scroller": ("Message Scroller", "components", "Scrollable transcripts with smooth auto-scroll."),
    "native-select": ("Native Select", "components", "Styled selects with animated chevron rotation."),
    "navigation-menu": ("Navigation Menu", "components", "Top nav with hover panels and underline slides."),
    "pagination": ("Pagination", "components", "Page buttons with active-state pop and hover lift."),
    "popover": ("Popover", "components", "Floating panels that scale from their anchor."),
    "progress": ("Progress", "components", "Bars that fill, sweep and pulse while loading."),
    "questionnaire": ("Questionnaire", "components", "Multi-step forms with progress and reveal motion."),
    "radio-group": ("Radio Group", "components", "Options whose dot pops into the selected ring."),
    "resizable": ("Resizable", "components", "Split panes with drag-handle highlight."),
    "scroll-area": ("Scroll Area", "components", "Custom scrollbars that fade in on scroll."),
    "select": ("Select", "components", "Dropdown selects with option highlight transitions."),
    "separator": ("Separator", "components", "Dividers that draw in with width/scale tweens."),
    "sheet": ("Sheet", "components", "Edge sheets sliding in with backdrop dim."),
    "sidebar": ("Sidebar", "components", "App sidebars with item hover slides and collapse."),
    "skeleton": ("Skeleton", "components", "Loading placeholders with shimmer sweeps."),
    "slider": ("Slider", "components", "Range sliders with thumb scale and fill transitions."),
    "spinner": ("Spinner", "components", "Spinners — rotating rings, pulsing dots, typing bars."),
    "switch": ("Switch", "components", "Toggles whose thumb slides with spring easing."),
    "table": ("Table", "components", "Tables with row hover sweeps and sort indicators."),
    "tabs": ("Tabs", "components", "Tab bars with sliding underline and panel fades."),
    "textarea": ("Textarea", "components", "Auto-growing inputs with focus glow."),
    "toast": ("Toast", "components", "Notifications that slide up, stack and auto-dismiss."),
    "toggle": ("Toggle", "components", "Pressed states with scale pop and color tween."),
    "toggle-group": ("Toggle Group", "components", "Exclusive toggles with sliding selection."),
    "tooltip": ("Tooltip", "components", "Tooltips that fade-up after a hover delay."),
    "trace": ("Trace", "components", "Step traces whose connector fills as you progress."),
    "typography": ("Typography", "components", "Type scale with staggered line reveals."),

    # ---------------- AI Elements ----------------
    "ai-introduction": ("Introduction", "ai", "What AI elements are and how they animate."),
    "chain-of-thought": ("Chain of Thought", "ai", "Reasoning traces that expand step by step."),
    "ai-chat": ("Chat", "ai", "Message streams that append with pop and typing dots."),
    "checkpoint": ("Checkpoint", "ai", "Saved-state markers that pulse when reached."),
    "confirmation": ("Confirmation", "ai", "Approval cards that slide in awaiting a decision."),
    "context": ("Context", "ai", "Memory chips that fade in as context grows."),
    "file-tree": ("File Tree", "ai", "Nested file trees with expand/collapse rotation."),
    "inline-citation": ("Inline Citation", "ai", "Citation chips that pop on hover."),
    "ai-message": ("Message", "ai", "Single bubbles for user/assistant roles."),
    "model-selector": ("Model Selector", "ai", "Model pickers with dropdown scale-in."),
    "plan": ("Plan", "ai", "Agent plans whose steps check off with motion."),
    "prompt-input": ("Prompt Input", "ai", "Composer boxes that focus-glow and send."),
    "queue": ("Queue", "ai", "Queued-message indicators with pulse."),
    "reasoning": ("Reasoning", "ai", "Thinking blocks with shimmer and collapse."),
    "sources": ("Sources", "ai", "Citation lists that stagger in."),
    "stack-trace": ("Stack Trace", "ai", "Error traces that slide down into view."),
    "subagent": ("Subagent", "ai", "Agent cards with status pulse and progress."),
    "suggestion": ("Suggestion", "ai", "Suggestion chips that wiggle for attention."),
    "task": ("Task", "ai", "Task items with status icon transitions."),
    "terminal": ("Terminal", "ai", "Terminal output that types line by line."),
    "test-results": ("Test Results", "ai", "Result summaries whose bars fill on load."),
    "tool": ("Tool", "ai", "Tool-call cards that expand args on hover."),

    # ---------------- Utilities ----------------
    "scroll-fade": ("scroll-fade", "utilities", "Edge-faded scroll containers."),
    "shimmer": ("shimmer", "utilities", "Shimmer loading sweeps for any surface."),

    # ---------------- Get Started ----------------
    "installation": ("Installation", "get-started", "Setup steps animated as a guided tour."),
    "components-json": ("components.json", "get-started", "Config file tour with field highlights."),
    "package-imports": ("Package Imports", "get-started", "Import paths revealed with typing."),
    "theming": ("Theming", "get-started", "Theme tokens transitioning live."),
    "typeset": ("Typeset", "get-started", "Prose styling with staggered reveals."),
    "dark-mode": ("Dark Mode", "get-started", "Theme toggle with crossfade."),
    "cli": ("CLI", "get-started", "Command animations and spinner states."),
    "monorepo": ("Monorepo", "get-started", "Workspace graph with animated edges."),
    "skills": ("Skills", "get-started", "Skill cards that deal in on hover."),
    "javascript": ("JavaScript", "get-started", "JS interop snippets with highlight sweep."),
    "figma": ("Figma", "get-started", "Design-to-code flow animations."),
    "llms-txt": ("llms.txt", "get-started", "Doc indexing visualization."),
    "legacy-docs": ("Legacy Docs", "get-started", "Migration path animations."),

    # ---------------- Integrations ----------------
    "shadcn-react": ("@shadcn/react", "integrations", "React interop layer notes."),
    "shadcn-helpers": ("@shadcn/helpers", "integrations", "Helper utilities overview."),
    "ai-sdk": ("AI SDK", "integrations", "Model streaming into chat elements."),
    "tanstack-ai": ("TanStack AI", "integrations", "TanStack adapter overview."),
    "react-hook-form": ("React Hook Form", "integrations", "Form state with animated validation."),
    "tanstack-form": ("TanStack Form", "integrations", "Schema-driven form animations."),
    "formisch": ("Formisch", "integrations", "Lightweight form validation motion."),

    # ---------------- Registry ----------------
    "registry-introduction": ("Introduction", "registry", "How the component registry works."),
    "registry-getting-started": ("Getting Started", "registry", "Registry setup walkthrough."),
    "github-registries": ("GitHub Registries", "registry", "Registry hosting on GitHub."),
    "registry-directory": ("Registry Directory", "registry", "Browsing the component index."),
    "registry-health": ("Registry Health", "registry", "Registry status indicators."),
    "registry-examples": ("Examples", "registry", "Registry usage patterns."),
    "namespaces": ("Namespaces", "registry", "Namespaced registry items."),
    "registry-authentication": ("Authentication", "registry", "Private registry auth flows."),
    "dynamic-search": ("Dynamic Search", "registry", "Live-filtered registry search."),
    "mcp-server": ("MCP Server", "registry", "Registry MCP endpoint."),
    "open-in-v0": ("Open in v0", "registry", "One-click v0 handoff."),
    "registry-faq": ("FAQ", "registry", "Registry questions answered."),

    # ---------------- API Reference ----------------
    "registry-json": ("registry.json", "api", "The registry index schema."),
    "registry-item-json": ("registry-item.json", "api", "The item schema reference."),
}


# ---------------------------------------------------------------------------
# Explicit animation variants for key items. Everything else gets the
# themed fallback below (entrance + gestures + pulse, named per item).
# ---------------------------------------------------------------------------

def _v(pattern, t, b, **params):
    return patterns.variant(pattern, t, b, **params)


VARIANTS = {
    "accordion": [
        _v("accordion", "Height expand", "maxHeight keyframes animate the open/close.", content="Four frameworks compared — the panel grows smoothly."),
        _v("stagger", "Staggered items", "Each row pops in with an increasing delay.", items=["Overview", "Pricing", "Docs", "Changelog"]),
        _v("entrance", "Section entrance", "Whole accordion fades up on mount.", content="Accordion", variant="up"),
    ],
    "alert": [
        _v("entrance", "Slide-in alerts", "Severity-colored alerts enter from the left.", content="Deploy finished in 42s", variant="left",
           className="w-80 rounded-lg border border-emerald-500/40 bg-emerald-500/10 p-4 text-sm text-emerald-200"),
        _v("shake", "Error shake", "Failures shake horizontally.", content="Payment failed — try again", axis="x"),
        _v("pulse", "Warning pulse", "Warnings breathe until acknowledged.", kind="opacity", content="Rate limit in 5 min",
           className="rounded-lg border border-amber-500/40 bg-amber-500/10 px-4 py-3 text-sm text-amber-200"),
    ],
    "alert-dialog": [
        _v("dialog", "Confirm dialog", "Backdrop fades, panel zooms, exits shrink.", title="Delete project?",
           body="This permanently removes files and deployments."),
        _v("shake", "Destructive shake", "The confirm button shakes to demand attention.", content="Are you absolutely sure?", axis="x",
           className="rounded-lg border border-red-500/40 bg-red-500/10 px-5 py-3 text-sm font-semibold text-red-200"),
    ],
    "aspect-ratio": [
        _v("entrance", "Reveal on mount", "The framed media fades and rises into place.", content="16:9 media", variant="zoom",
           className="flex h-40 w-72 items-center justify-center rounded-xl border border-zinc-800 bg-gradient-to-br from-zinc-800 to-zinc-900"),
        _v("flip3d", "Ratio flip", "Content flips to show the alternate ratio.", axis="Y", content="4:3"),
    ],
    "attachment": [
        _v("gestures", "Chip hover", "Attachment chips lift on hover.", label="report.pdf · 2.4 MB",
           className="inline-flex items-center gap-2 rounded-lg border border-zinc-700 bg-zinc-900 px-3 py-2 text-sm text-zinc-200"),
        _v("entrance", "Drop-in", "New attachments drop in from above.", content="design.png · 840 KB", variant="down",
           className="inline-flex items-center gap-2 rounded-lg border border-zinc-700 bg-zinc-900 px-3 py-2 text-sm text-zinc-200"),
    ],
    "avatar": [
        _v("stagger", "Group pop-in", "Avatars spring in sequence.", items=["A", "G", "T", "E"],
           itemClass="flex h-11 w-11 items-center justify-center rounded-full bg-gradient-to-br from-blue-600 to-violet-600 text-sm font-bold text-white"),
        _v("pulse", "Online pulse", "Presence ring pulses for active users.", kind="scale", content="",
           className="flex h-4 w-4 items-center justify-center rounded-full bg-emerald-500"),
    ],
    "badge": [
        _v("pulse", "Live pulse", "Status badges loop opacity.", kind="opacity", content="Live",
           className="rounded-full bg-emerald-500/15 px-3 py-1 text-xs font-semibold text-emerald-400"),
        _v("stagger", "Staggered badges", "Badges pop in one after another.", items=["Stable", "Beta", "v2.0"]),
    ],
    "breadcrumb": [
        _v("stagger", "Trail reveal", "Crumbs fade in left to right.", items=["Home", "Docs", "Components", "Button"],
           itemClass="text-sm text-zinc-400", wrapClass="flex items-center gap-2"),
        _v("entrance", "Page load", "Whole trail slides in.", content="Home / Docs / Button", variant="left"),
    ],
    "bubble": [
        _v("entrance", "Incoming bubble", "Assistant bubbles pop from the left.", content="Here's the answer…", variant="left",
           className="max-w-xs rounded-2xl rounded-bl-sm border border-zinc-800 bg-zinc-900 px-4 py-2 text-sm text-zinc-200"),
        _v("entrance", "Outgoing bubble", "User bubbles pop from the right.", content="Thanks!", variant="right",
           className="max-w-xs rounded-2xl rounded-br-sm bg-blue-600 px-4 py-2 text-sm text-white"),
    ],
    "button": [
        _v("gestures", "Hover & tap", "whileHover lifts, whileTap presses.", label="Save changes"),
        _v("pulse", "Loading", "Opacity loop while processing.", kind="opacity", content="Processing…",
           className="rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white"),
        _v("entrance", "Spring pop", "Overshoot easing on mount.", content="Get started", variant="zoom",
           className="rounded-lg bg-emerald-600 px-6 py-3 font-semibold text-white"),
    ],
    "button-group": [
        _v("gestures", "Segment hover", "Each segment reacts independently.", label="Week",
           className="border-x border-zinc-700 bg-zinc-900 px-5 py-2.5 text-sm font-medium text-zinc-200"),
        _v("stagger", "Segment reveal", "Segments cascade in.", items=["Day", "Week", "Month", "Year"]),
    ],
    "calendar": [
        _v("stagger", "Day cells pop", "Dates stagger in across the grid.", items=["1", "2", "3", "4", "5", "6", "7", "8"],
           itemClass="flex h-8 w-8 items-center justify-center rounded-lg bg-zinc-800 text-xs text-zinc-300"),
        _v("pulse", "Today marker", "Today's cell pulses.", kind="scale", content="14",
           className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-600 text-xs font-bold text-white"),
    ],
    "card": [
        _v("gestures", "Lift on hover", "The whole card floats up.", label="Hover me",
           className="w-72 cursor-pointer rounded-xl border border-zinc-800 bg-zinc-900/60 p-6 text-left shadow-xl"),
        _v("flip3d", "3D flip", "rotateY loop.", axis="Y", content="Card"),
        _v("entrance", "Deal-in", "Cards enter with a spring.", content="New card", variant="zoom"),
    ],
    "carousel": [
        _v("entrance", "Slide track", "The track translates horizontally.", variant="left",
           className="flex h-32 w-72 items-center justify-center rounded-xl bg-gradient-to-br from-blue-600/40 to-violet-600/40 text-lg font-bold text-white"),
        _v("pulse", "Autoplay dot", "Active dot pulses.", kind="scale", content="",
           className="h-2.5 w-2.5 rounded-full bg-blue-500"),
    ],
    "chart": [
        _v("progress", "Bars fill", "Each bar grows with scaleY.", mode="fill", pct=80),
        _v("stagger", "Series stagger", "Data points pop in sequence.", items=["Q1", "Q2", "Q3", "Q4"],
           itemClass="flex h-10 w-10 items-end justify-center rounded-t bg-blue-500/70"),
    ],
    "checkbox": [
        _v("gestures", "Check pop", "Box scales on toggle.", label="Accept terms",
           className="flex h-5 w-5 items-center justify-center rounded border-2 border-blue-500 bg-blue-600 text-xs text-white"),
        _v("pulse", "Required nudge", "Unchecked required fields pulse gently.", kind="opacity", content="Required",
           className="rounded border border-zinc-600 px-3 py-1.5 text-xs text-zinc-400"),
    ],
    "code-block": [
        _v("typing", "Typewriter", "Code appears with steps() cadence.", text="def hello(): …"),
        _v("shimmer", "Highlight sweep", "A sheen passes over the block.", duration=2.2),
    ],
    "collapsible": [
        _v("accordion", "Expand region", "maxHeight tween reveals content.", content="Additional settings and options…"),
        _v("gestures", "Trigger hover", "The trigger pill lifts.", label="Show details",
           className="rounded-lg border border-zinc-700 px-4 py-2 text-sm text-zinc-200"),
    ],
    "combobox": [
        _v("dialog", "Dropdown open", "Panel scales from the input.", title="Pick a language",
           body="Python, JavaScript, Rust, Go…"),
        _v("shimmer", "Filtering shimmer", "List shimmers while searching.", duration=1.2),
    ],
    "command": [
        _v("dialog", "⌘K palette", "Palette scales over a dim backdrop.", title="Type a command…",
           body="New file · Open settings · Deploy"),
        _v("typing", "Command hint", "Placeholder types itself.", text="> deploy --prod"),
    ],
    "context-menu": [
        _v("dialog", "Menu pop", "Menu scales from bottom-left.", title="Actions", body="Copy · Paste · Delete"),
        _v("stagger", "Item cascade", "Menu items stagger in.", items=["Copy", "Paste", "Cut", "Delete"]),
    ],
    "data-table": [
        _v("stagger", "Row entrance", "Rows cascade into the grid.", items=["Ada", "Grace", "Alan", "Edsger"],
           itemClass="rounded bg-zinc-800/70 px-3 py-2 text-sm text-zinc-300"),
        _v("gestures", "Row hover", "Rows highlight on hover.", label="hover row",
           className="w-72 rounded-lg border border-zinc-800 bg-zinc-900/60 px-4 py-3 text-sm text-zinc-300"),
    ],
    "date-picker": [
        _v("dialog", "Calendar popover", "Picker scales from the input.", title="November 2026", body="Pick a date"),
        _v("stagger", "Day grid", "Days stagger across the month.", items=["1","2","3","4","5","6","7","8","9","10"],
           itemClass="flex h-7 w-7 items-center justify-center rounded text-xs text-zinc-400"),
    ],
    "dialog": [
        _v("dialog", "Modal entrance", "Backdrop + panel zoom.", title="Settings", body="Configure your workspace."),
        _v("entrance", "Sheet variant", "Side-anchored entrance.", variant="right",
           className="flex h-40 w-64 items-center justify-center rounded-xl border border-zinc-800 bg-zinc-900 p-5"),
    ],
    "direction": [
        _v("flip3d", "RTL flip", "Direction flip animates rotation.", axis="Y", content="RTL"),
        _v("entrance", "Content reveal", "Bidi text fades in.", content="نص من اليمين إلى اليسار", variant="fade"),
    ],
    "drawer": [
        _v("drawer", "Slide from right", "Panel translates in from the edge.", edge="right", content="Filters & options"),
        _v("drawer", "Slide from left", "Opposite edge variant.", edge="left", content="Navigation"),
        _v("drawer", "Slide from bottom", "Bottom sheet variant.", edge="bottom", content="Share sheet"),
    ],
    "dropdown-menu": [
        _v("dialog", "Menu open", "Scales from trigger corner.", title="Options", body="Edit · Duplicate · Delete"),
        _v("stagger", "Items cascade", "Entries stagger downward.", items=["Edit", "Duplicate", "Archive", "Delete"]),
    ],
    "empty": [
        _v("entrance", "Gentle float", "Empty state drifts in.", content="No results found", variant="up",
           className="flex w-72 flex-col items-center gap-3 rounded-xl border border-dashed border-zinc-800 p-8"),
        _v("pulse", "Icon breathe", "The empty icon pulses softly.", kind="opacity", content="◇",
           className="flex h-12 w-12 items-center justify-center rounded-full bg-zinc-800 text-xl text-zinc-500"),
    ],
    "field": [
        _v("shake", "Error shake", "Invalid fields shake on submit.", content="Email is required", axis="x",
           className="w-72 rounded-lg border border-red-500/50 bg-zinc-900 px-4 py-3 text-sm text-zinc-300"),
        _v("gestures", "Focus lift", "Field lifts when focused.", label="you@example.com",
           className="w-72 rounded-lg border border-blue-500/60 bg-zinc-900 px-4 py-3 text-sm text-zinc-200 shadow-lg shadow-blue-500/10"),
    ],
    "hover-card": [
        _v("entrance", "Delayed reveal", "Card fades up after hover.", content="@nextpy — Python framework", variant="up",
           className="w-72 rounded-xl border border-zinc-800 bg-zinc-900 p-4 shadow-xl"),
        _v("flip3d", "Card flip", "Hover card flips for detail.", axis="X", content="Profile"),
    ],
    "input": [
        _v("shake", "Invalid shake", "Bad input shakes on blur.", content="not-an-email", axis="x",
           className="w-72 rounded-lg border border-red-500/60 bg-zinc-900 px-4 py-3 font-mono text-sm text-zinc-300"),
        _v("gestures", "Focus glow", "Ring brightens on focus.", label="Focus me",
           className="w-72 rounded-lg border border-blue-500/60 bg-zinc-900 px-4 py-3 text-sm text-zinc-200 shadow-lg shadow-blue-500/10"),
    ],
    "input-group": [
        _v("stagger", "Addon cascade", "Prefix/suffix/input stagger in.", items=["@", "username", ".com"],
           itemClass="flex h-10 items-center border border-zinc-700 bg-zinc-800/60 px-3 text-sm text-zinc-300"),
        _v("entrance", "Group reveal", "Whole group slides up.", content="@user.com", variant="up",
           className="flex w-72 items-center rounded-lg border border-zinc-700 bg-zinc-900"),
    ],
    "input-otp": [
        _v("stagger", "Cell pop", "Each OTP cell pops as filled.", items=["1","2","3","4","5","6"],
           itemClass="flex h-12 w-10 items-center justify-center rounded-lg border border-zinc-700 bg-zinc-900 font-mono text-lg text-zinc-100"),
        _v("pulse", "Waiting pulse", "Empty cells breathe until typed.", kind="opacity", content="_",
           className="flex h-12 w-10 items-center justify-center rounded-lg border border-blue-500/50 bg-blue-500/5 font-mono text-lg text-blue-300"),
    ],
    "item": [
        _v("gestures", "Row lift", "List items lift on hover.", label="invoice.pdf",
           className="flex w-80 items-center gap-3 rounded-lg border border-zinc-800 bg-zinc-900/50 p-3"),
        _v("entrance", "List cascade", "Items drop in sequence.", variant="down",
           className="flex w-80 items-center gap-3 rounded-lg border border-zinc-800 bg-zinc-900/50 p-3"),
    ],
    "kbd": [
        _v("gestures", "Key press", "Cap presses down on :active.", label="⌘K",
           className="inline-flex h-6 items-center rounded border border-zinc-700 bg-zinc-900 px-2 font-mono text-xs text-zinc-300"),
        _v("stagger", "Shortcut combo", "Keys pop in sequence.", items=["⌘", "K"],
           itemClass="flex h-6 w-6 items-center justify-center rounded border border-zinc-700 bg-zinc-900 font-mono text-xs text-zinc-300"),
    ],
    "label": [
        _v("entrance", "Label fade", "Labels fade in with their fields.", content="Email address", variant="fade"),
        _v("pulse", "Required marker", "Asterisk pulses for required fields.", kind="scale", content="*",
           className="text-sm font-bold text-red-400"),
    ],
    "marker": [
        _v("entrance", "Highlight sweep", "Marker wipes in behind text.", content="important",
           className="rounded-sm bg-amber-400/30 px-1.5 py-0.5 text-amber-200"),
        _v("pulse", "Attention blink", "Marker blinks gently.", kind="opacity", content="new!",
           className="rounded-sm bg-amber-400/30 px-1.5 py-0.5 text-amber-200"),
    ],
    "menubar": [
        _v("stagger", "Menu cascade", "Top-level items stagger in.", items=["File", "Edit", "View", "Help"],
           itemClass="px-3 py-1.5 text-sm text-zinc-300"),
        _v("dialog", "Dropdown panel", "Dropdown scales from its item.", title="File", body="New · Open · Save"),
    ],
    "message": [
        _v("entrance", "Assistant pop", "AI messages pop from the left.", content="Sure — here's how…", variant="left",
           className="max-w-xs rounded-2xl rounded-bl-sm border border-zinc-800 bg-zinc-900 px-4 py-2 text-sm text-zinc-200"),
        _v("entrance", "User pop", "User messages pop from the right.", content="Build me a dashboard", variant="right",
           className="max-w-xs rounded-2xl rounded-br-sm bg-blue-600 px-4 py-2 text-sm text-white"),
    ],
    "message-scroller": [
        _v("stagger", "Message cascade", "Transcript messages cascade in.", items=["Hey!", "Hi there", "How are you?", "Great!"],
           itemClass="max-w-xs rounded-2xl bg-zinc-800 px-3 py-1.5 text-sm text-zinc-200"),
        _v("typing", "Streaming reply", "Assistant text types out.", text="Streaming response…"),
    ],
    "native-select": [
        _v("flip3d", "Chevron flip", "Dropdown arrow rotates on open.", axis="Y", content="Select…"),
        _v("stagger", "Option list", "Options cascade in the popup.", items=["Python", "JS", "Rust", "Go"],
           itemClass="rounded px-3 py-1.5 text-sm text-zinc-300"),
    ],
    "navigation-menu": [
        _v("stagger", "Nav cascade", "Top-level links stagger in.", items=["Docs", "Components", "Blog", "Pricing"],
           itemClass="px-3 py-1.5 text-sm text-zinc-300"),
        _v("entrance", "Mega panel", "Hover panel fades up.", content="Resources", variant="up",
           className="w-72 rounded-xl border border-zinc-800 bg-zinc-900 p-4 shadow-xl"),
    ],
    "pagination": [
        _v("stagger", "Page cascade", "Numbered buttons stagger in.", items=["1","2","3","4","5"],
           itemClass="flex h-8 w-8 items-center justify-center rounded-lg border border-zinc-700 text-sm text-zinc-400"),
        _v("pulse", "Active page", "Current page pulses.", kind="scale", content="3",
           className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-600 text-sm font-bold text-white"),
    ],
    "popover": [
        _v("dialog", "Popover open", "Panel scales from anchor.", title="Dimensions", body="320px × auto"),
        _v("entrance", "Content reveal", "Inner content staggers.", variant="fade", content="Popover body"),
    ],
    "progress": [
        _v("progress", "Determinate fill", "Width tweens to the value.", mode="fill", pct=72),
        _v("progress", "Indeterminate", "Highlight sweeps for unknown duration.", mode="sweep", pct=0),
    ],
    "questionnaire": [
        _v("stagger", "Option cascade", "Choices stagger per question.", items=["A", "B", "C", "D"],
           itemClass="rounded-lg border border-zinc-700 px-4 py-2 text-sm text-zinc-300"),
        _v("progress", "Step progress", "Progress bar fills per answer.", mode="fill", pct=60),
    ],
    "radio-group": [
        _v("stagger", "Option cascade", "Choices stagger in.", items=["Basic", "Pro", "Team"],
           itemClass="flex items-center gap-2 rounded-lg border border-zinc-800 px-3 py-2 text-sm text-zinc-300"),
        _v("pulse", "Selected dot", "Chosen dot pops.", kind="scale", content="●",
           className="flex h-4 w-4 items-center justify-center rounded-full border-2 border-blue-500"),
    ],
    "resizable": [
        _v("gestures", "Handle drag", "Divider highlights on hover.", label="⠿ drag",
           className="h-64 w-2 cursor-col-resize rounded bg-zinc-800"),
        _v("entrance", "Pane reveal", "Panes slide apart on load.", variant="left",
           className="flex h-40 w-72 overflow-hidden rounded-xl border border-zinc-800"),
    ],
    "scroll-area": [
        _v("marquee", "Scroll strip", "Content marquees inside the viewport.", duration=10),
        _v("shimmer", "Scrollbar fade", "Edge fade on scroll.", duration=1.8),
    ],
    "select": [
        _v("dialog", "Select open", "Panel scales from trigger.", title="Plan", body="Free · Pro · Team"),
        _v("stagger", "Option cascade", "Options stagger in popup.", items=["Free", "Pro", "Team", "Enterprise"],
           itemClass="rounded px-3 py-1.5 text-sm text-zinc-300"),
    ],
    "separator": [
        _v("progress", "Draw-in", "Divider scaleX from 0 to full.", mode="fill", pct=100),
        _v("entrance", "Fade divider", "Separator fades in.", content="—", variant="fade"),
    ],
    "sheet": [
        _v("drawer", "Right sheet", "Slides from the right edge.", edge="right", content="Share · Export · Print"),
        _v("drawer", "Bottom sheet", "Mobile sheet from below.", edge="bottom", content="Actions"),
    ],
    "sidebar": [
        _v("stagger", "Nav cascade", "Sidebar items stagger in.", items=["Dashboard", "Projects", "Team", "Settings"],
           itemClass="flex items-center gap-2 rounded-lg px-3 py-2 text-sm text-zinc-400"),
        _v("drawer", "Collapse drawer", "Sidebar slides out.", edge="left", content="Navigation"),
    ],
    "skeleton": [
        _v("shimmer", "Shimmer blocks", "Loading placeholders sweep.", duration=1.6),
        _v("pulse", "Pulse block", "Simple opacity pulse.", kind="opacity", content="",
           className="h-16 w-64 rounded-lg bg-zinc-800"),
    ],
    "slider": [
        _v("progress", "Value fill", "Track fills to the thumb.", mode="fill", pct=40),
        _v("gestures", "Thumb grab", "Thumb scales on drag.", label="◉",
           className="flex h-5 w-5 items-center justify-center rounded-full bg-blue-500 shadow"),
    ],
    "spinner": [
        _v("spinner", "Rotating ring", "Border ring spins linearly.", kind="ring", duration=1),
        _v("spinner", "Pulsing dots", "Three dots pulse in sequence.", kind="dots", duration=0.9),
        _v("typing", "Typing caret", "Steps() width reveal.", text="Loading…", duration=1.6),
    ],
    "switch": [
        _v("gestures", "Thumb slide", "Toggle slides with spring.", label="Enable",
           className="relative flex h-6 w-11 items-center rounded-full bg-blue-600 px-0.5"),
        _v("pulse", "State nudge", "Off state breathes.", kind="opacity", content="Off",
           className="rounded-full bg-zinc-700 px-3 py-1 text-xs text-zinc-400"),
    ],
    "table": [
        _v("stagger", "Row cascade", "Body rows stagger in.", items=["Ada", "Grace", "Alan", "Katherine"],
           itemClass="rounded bg-zinc-800/60 px-3 py-2 text-sm text-zinc-300"),
        _v("gestures", "Header hover", "Header cells highlight.", label="Name ↑",
           className="rounded bg-zinc-800/60 px-3 py-2 text-xs font-semibold uppercase text-zinc-400"),
    ],
    "tabs": [
        _v("tabs", "Sliding indicator", "Underline tracks the active tab.", duration=0.3),
        _v("stagger", "Tab cascade", "Tabs stagger in.", items=["Account", "Security", "Billing"],
           itemClass="border-b-2 border-transparent px-4 py-2 text-sm text-zinc-400"),
    ],
    "textarea": [
        _v("entrance", "Auto-grow", "Box expands with content.", content="Multi-line input…", variant="up",
           className="w-80 rounded-lg border border-zinc-700 bg-zinc-900 p-3 text-sm text-zinc-300"),
        _v("shake", "Limit shake", "Over-limit shakes.", content="Too long", axis="y",
           className="w-80 rounded-lg border border-red-500/50 bg-zinc-900 p-3 text-sm text-zinc-300"),
    ],
    "toast": [
        _v("toast", "Slide-up toast", "Notification rises and fades.", message="Profile saved", duration=0.4),
        _v("stagger", "Toast stack", "Multiple toasts cascade.", items=["Saved", "Copied", "Deployed"],
           itemClass="rounded-lg border border-zinc-700 bg-zinc-900 px-4 py-2 text-sm text-zinc-200"),
    ],
    "toggle": [
        _v("gestures", "Press pop", "Toggle scales on press.", label="Bold",
           className="rounded-lg border border-zinc-700 px-4 py-2 text-sm text-zinc-300"),
        _v("pulse", "Active glow", "On-state glows.", kind="scale", content="ON",
           className="rounded-lg bg-blue-600/20 px-4 py-2 text-sm font-semibold text-blue-300"),
    ],
    "toggle-group": [
        _v("stagger", "Segment cascade", "Options stagger in.", items=["Day", "Week", "Month"],
           itemClass="border border-zinc-700 px-4 py-2 text-sm text-zinc-400"),
        _v("pulse", "Selected pulse", "Active segment pulses.", kind="scale", content="Week",
           className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white"),
    ],
    "tooltip": [
        _v("entrance", "Fade-up tip", "Tooltip rises after delay.", content="Helpful hint", variant="up",
           className="rounded-md border border-zinc-700 bg-zinc-900 px-2.5 py-1.5 text-xs text-zinc-200 shadow-lg"),
        _v("flip3d", "Flip tip", "Tooltip flips on hover.", axis="X", content="Tip"),
    ],
    "trace": [
        _v("progress", "Step fill", "Connector fills to current step.", mode="fill", pct=50),
        _v("stagger", "Step cascade", "Steps pop in order.", items=["Cart", "Ship", "Pay", "Done"],
           itemClass="flex h-7 w-7 items-center justify-center rounded-full bg-zinc-800 text-xs text-zinc-300"),
    ],
    "typography": [
        _v("stagger", "Line reveal", "Each line staggers upward.", items=["Heading one", "Body copy", "Caption text"],
           itemClass="text-zinc-200"),
        _v("entrance", "Type on", "Heading types in.", variant="fade", content="The quick brown fox"),
    ],

    # ---------------- AI Elements ----------------
    "ai-introduction": [
        _v("stagger", "Element kinds", "AI element categories cascade.", items=["Chat", "Reasoning", "Tools", "Sources"],
           itemClass="rounded-lg border border-zinc-800 bg-zinc-900/60 px-4 py-2 text-sm text-zinc-300"),
        _v("marquee", "Streaming ticker", "Tokens stream endlessly.", duration=14),
    ],
    "chain-of-thought": [
        _v("accordion", "Expand trace", "Reasoning steps reveal with height tween.", content="Step 3 of 5 — analyzing imports…"),
        _v("stagger", "Step cascade", "Thought steps stagger in.", items=["Parse", "Plan", "Execute", "Verify"],
           itemClass="flex items-center gap-2 text-sm text-zinc-400"),
    ],
    "ai-chat": [
        _v("stagger", "Message stream", "Chat bubbles cascade in.", items=["Hi!", "Hello!", "Build a dashboard", "On it…"],
           itemClass="max-w-xs rounded-2xl bg-zinc-800 px-3 py-1.5 text-sm text-zinc-200"),
        _v("typing", "Assistant typing", "Reply streams with steps cadence.", text="Generating response…", duration=2.4),
    ],
    "checkpoint": [
        _v("pulse", "Checkpoint pulse", "Saved markers breathe.", kind="scale", content="✓ v3",
           className="flex items-center gap-2 rounded-lg border border-emerald-500/30 bg-emerald-500/5 px-4 py-2 text-sm text-emerald-300"),
        _v("stagger", "Timeline", "Checkpoints cascade.", items=["init", "auth", "api", "deploy"],
           itemClass="rounded-full bg-zinc-800 px-3 py-1 text-xs text-zinc-400"),
    ],
    "confirmation": [
        _v("dialog", "Approval card", "Slides in awaiting decision.", title="Run migration?", body="3 tables, no data loss"),
        _v("shake", "Urgent confirm", "High-risk actions shake.", content="Deploy to production?", axis="x",
           className="w-80 rounded-lg border border-amber-500/40 bg-amber-500/10 p-4 text-sm text-amber-200"),
    ],
    "context": [
        _v("stagger", "Memory chips", "Context items cascade.", items=["prefs", "docs", "history", "files"],
           itemClass="rounded-full border border-zinc-700 bg-zinc-800/60 px-2.5 py-1 text-xs text-zinc-400"),
        _v("pulse", "Active context", "Live context indicator.", kind="opacity", content="3 items",
           className="rounded-full bg-blue-500/15 px-3 py-1 text-xs text-blue-400"),
    ],
    "file-tree": [
        _v("stagger", "Node cascade", "Files stagger in.", items=["src/", "pages/", "main.py", "README.md"],
           itemClass="font-mono text-xs text-zinc-400"),
        _v("flip3d", "Expand flip", "Directories flip open.", axis="Y", content="src/"),
    ],
    "inline-citation": [
        _v("gestures", "Citation pop", "Superscript pops on hover.", label="[1]",
           className="ml-1 inline-flex h-4 w-4 items-center justify-center rounded bg-zinc-800 text-[10px] font-bold text-blue-400"),
        _v("pulse", "New source", "Fresh citations pulse.", kind="scale", content="[2]",
           className="ml-1 inline-flex h-4 w-4 items-center justify-center rounded bg-blue-500/20 text-[10px] font-bold text-blue-300"),
    ],
    "ai-message": [
        _v("entrance", "Assistant bubble", "Pops from the left.", content="Here's the diff…", variant="left",
           className="max-w-xs rounded-2xl rounded-bl-sm border border-zinc-800 bg-zinc-900 px-4 py-2 text-sm text-zinc-200"),
        _v("entrance", "User bubble", "Pops from the right.", content="Fix the bug", variant="right",
           className="max-w-xs rounded-2xl rounded-br-sm bg-blue-600 px-4 py-2 text-sm text-white"),
    ],
    "model-selector": [
        _v("dialog", "Model dropdown", "Picker scales open.", title="Model", body="coder-1 · coder-mini · reasoner"),
        _v("stagger", "Model list", "Models cascade.", items=["coder-1", "coder-mini", "reasoner"],
           itemClass="rounded px-3 py-1.5 font-mono text-sm text-zinc-300"),
    ],
    "plan": [
        _v("stagger", "Plan steps", "Steps cascade with status icons.", items=["Explore", "Design", "Build", "Test"],
           itemClass="flex items-center gap-2 text-sm text-zinc-300"),
        _v("progress", "Plan progress", "Bar fills as steps complete.", mode="fill", pct=65),
    ],
    "prompt-input": [
        _v("gestures", "Composer focus", "Input lifts on focus.", label="Ask the agent…",
           className="w-80 rounded-xl border border-blue-500/50 bg-zinc-900 p-3 text-sm text-zinc-300 shadow-lg shadow-blue-500/10"),
        _v("entrance", "Send pop", "Send button pops on ready.", content="Send", variant="zoom",
           className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white"),
    ],
    "queue": [
        _v("pulse", "Queue pulse", "Pending count breathes.", kind="opacity", content="3 queued",
           className="inline-flex items-center gap-2 rounded-full border border-zinc-700 bg-zinc-900 px-3 py-1 text-xs text-zinc-400"),
        _v("stagger", "Queue items", "Queued messages cascade.", items=["msg 1", "msg 2", "msg 3"],
           itemClass="rounded bg-zinc-800/60 px-2 py-1 text-xs text-zinc-400"),
    ],
    "reasoning": [
        _v("shimmer", "Thinking shimmer", "Reasoning text shimmers while thinking.", duration=2),
        _v("accordion", "Collapse trace", "Reasoning expands/collapses.", content="Weighing trade-offs between options A and B…"),
    ],
    "sources": [
        _v("stagger", "Source cascade", "Citations stagger in.", items=["Docs", "GitHub", "RFC", "Blog"],
           itemClass="flex items-center gap-2 rounded-lg px-3 py-2 text-sm text-zinc-300"),
        _v("pulse", "Cited pulse", "Referenced source highlights.", kind="scale", content="[1] Docs",
           className="rounded bg-blue-500/15 px-2 py-1 text-xs text-blue-300"),
    ],
    "stack-trace": [
        _v("entrance", "Trace slide", "Stack slides down into view.", variant="down",
           className="w-80 rounded-lg border border-red-500/30 bg-zinc-950 p-4 font-mono text-xs text-red-300"),
        _v("shake", "Error shake", "Trace header shakes.", content="ValueError: bad input", axis="x",
           className="w-80 rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-2 font-mono text-xs text-red-300"),
    ],
    "subagent": [
        _v("pulse", "Running pulse", "Active agent breathes.", kind="opacity", content="researcher · running",
           className="flex w-72 items-center gap-3 rounded-lg border border-blue-500/30 bg-blue-500/5 px-4 py-3"),
        _v("stagger", "Agent roster", "Subagents cascade.", items=["researcher", "coder", "reviewer"],
           itemClass="flex items-center gap-2 rounded-lg border border-zinc-800 bg-zinc-900/50 px-3 py-2 text-sm text-zinc-300"),
    ],
    "suggestion": [
        _v("pulse", "Suggestion nudge", "Chips wiggle for attention.", kind="rotate", content="Add tests?",
           className="inline-flex items-center gap-2 rounded-full border border-blue-500/30 bg-blue-500/10 px-3 py-1.5 text-sm text-blue-200"),
        _v("stagger", "Suggestion row", "Suggestions cascade.", items=["Refactor?", "Add docs?", "Write tests?"],
           itemClass="rounded-full border border-zinc-700 px-3 py-1 text-xs text-zinc-400"),
    ],
    "task": [
        _v("stagger", "Task cascade", "Tasks pop in order.", items=["Scaffold", "Auth", "API", "Tests"],
           itemClass="flex items-center gap-2 text-sm text-zinc-300"),
        _v("progress", "Task progress", "Bar fills per completion.", mode="fill", pct=40),
    ],
    "terminal": [
        _v("typing", "Line typing", "Commands type with steps cadence.", text="$ nextpy dev …", duration=2.2),
        _v("stagger", "Output cascade", "Output lines stagger.", items=["$ nextpy dev", "✓ compiled", "➜ :5000"],
           itemClass="font-mono text-xs text-emerald-300"),
    ],
    "test-results": [
        _v("progress", "Pass bar", "Result bar fills on load.", mode="fill", pct=95),
        _v("stagger", "Suite cascade", "Test files stagger.", items=["auth: 12 ✓", "api: 8 ✓", "ui: 20 ✓"],
           itemClass="rounded bg-zinc-800/60 px-3 py-1.5 font-mono text-xs text-zinc-300"),
    ],
    "tool": [
        _v("accordion", "Tool expand", "Args reveal on expand.", content='read_file(path="main.py") → 248 lines'),
        _v("gestures", "Tool hover", "Card lifts on hover.", label="⚙ run_tests",
           className="w-72 rounded-lg border border-zinc-800 bg-zinc-900/60 p-3 font-mono text-xs text-zinc-300"),
    ],

    # ---------------- Utilities ----------------
    "scroll-fade": [
        _v("shimmer", "Edge fade", "Scroll edges fade via gradient overlay.", duration=1.8),
        _v("marquee", "Fading strip", "Content scrolls under edge fades.", duration=11),
    ],
    "shimmer": [
        _v("shimmer", "Text shimmer", "Gradient sweeps across loading text.", duration=1.6),
        _v("shimmer", "Block shimmer", "Skeleton block shimmer.", duration=2),
    ],
}


def _fallback_variants(slug):
    """Themed fallback: entrance + gestures + pulse named after the item."""
    name = ITEMS[slug][0]
    return [
        _v("entrance", f"{name} entrance", "Fade-and-rise on mount.", content=name, variant="up"),
        _v("gestures", f"{name} interaction", "Hover lift and tap press.", label=f"{name} action"),
        _v("pulse", f"{name} attention", "Attention loop for live state.", kind="opacity", content=name),
    ]


def variants_for(slug):
    return VARIANTS.get(slug) or _fallback_variants(slug)


# ---------------------------------------------------------------------------
# Page factory
# ---------------------------------------------------------------------------

def _ordered():
    out = []
    for g, _ in GROUPS:
        for slug in ITEMS:
            if ITEMS[slug][1] == g:
                out.append(slug)
    return out


def _neighbors(slug):
    order = _ordered()
    i = order.index(slug)
    return (order[i - 1] if i else None, order[i + 1] if i < len(order) - 1 else None)


@component
def AnimPage(props=None):
    """Placeholder — real pages are built by page_for()."""
    return <div>Animation</div>


def page_for(slug):
    """Build the docs-style animation page for a registry slug.

    The page body is a dynamically-built ``psx()`` string: one literal
    ``<AnimSection>`` per variant (component props with ``{expr}`` attrs
    don't resolve loop variables inside ``{for}`` blocks, so we emit them
    explicitly). All values are passed through an explicit context dict.
    """
    from nextpy.psx import psx
    name, group, desc = ITEMS[slug]
    group_label = dict(GROUPS).get(group, group)
    variants = variants_for(slug)
    prev_slug, next_slug = _neighbors(slug)

    prev_el = None
    next_el = None
    if prev_slug:
        pn, pg = ITEMS[prev_slug][0], ITEMS[prev_slug][1]
        prev_el = el("a", "group block p-4 rounded-xl border border-zinc-800 bg-zinc-900/40 hover:border-zinc-700", [
            el("span", "block text-xs text-zinc-500 uppercase tracking-wide", "Previous"),
            el("span", "text-sm font-semibold text-zinc-200 group-hover:text-blue-400", pn)],
            href=f"/animation-playground/{pg}/{prev_slug}")
    if next_slug:
        nn, ng = ITEMS[next_slug][0], ITEMS[next_slug][1]
        next_el = el("a", "group block p-4 rounded-xl border border-zinc-800 bg-zinc-900/40 hover:border-zinc-700 text-right", [
            el("span", "block text-xs text-zinc-500 uppercase tracking-wide", "Next"),
            el("span", "text-sm font-semibold text-zinc-200 group-hover:text-blue-400", nn)],
            href=f"/animation-playground/{ng}/{next_slug}")
    footer_el = el("footer", "grid gap-4 border-t border-zinc-800/60 pt-8 sm:grid-cols-2",
                   [prev_el or el("div"), next_el or el("div")])

    sections_jsx = "".join(
        f'<AnimSection title={{v{i}_title}} blurb={{v{i}_blurb}} code={{v{i}_code}} '
        f'tall={{v{i}_tall}} demo={{v{i}_demo}} index={{v{i}_num}} />'
        for i in range(len(variants)))

    page_jsx = f"""<div class="mx-auto max-w-5xl px-6 py-16">
        <nav class="mb-8 flex items-center gap-2 text-sm text-zinc-500">
            <Link href="/animation-playground" className="hover:text-zinc-300">Playground</Link>
            <span class="text-zinc-700">/</span>
            <span class="text-zinc-300">{{group_v}}</span>
            <span class="text-zinc-700">/</span>
            <span class="text-zinc-300">{{name_v}}</span>
        </nav>
        <header class="mb-10 max-w-2xl">
            <div class="mb-3 flex items-center gap-3">
                <h1 class="text-2xl font-semibold tracking-tight text-white">{{name_v}}</h1>
                <span class="rounded-full border border-blue-500/30 bg-blue-500/10 px-2.5 py-0.5 text-xs font-medium text-blue-400">{{group_v}}</span>
            </div>
            <p class="text-[15px] leading-relaxed text-zinc-500">{{desc_v}}</p>
            <p class="mt-3 text-sm text-zinc-600">
                {{variants_len}} animation variants — every demo runs on the Web Animations API
                via <code class="font-mono text-[13px] text-zinc-400">Motion</code>. Copy any snippet into a PSX page.
            </p>
        </header>
        {sections_jsx}
        {{footer_el}}
        {{runtime_js}}
    </div>"""

    try:
        from nextpy.psx.runtime.js_actions_runtime import JS_ACTION_RUNTIME_SCRIPT
        runtime_tag = "<script>" + JS_ACTION_RUNTIME_SCRIPT + "</script>"
    except Exception:
        runtime_tag = ""

    ctx = {
        "Link": Link,
        "runtime_js": "_RAW_CODE:" + runtime_tag,
        "AnimSection": AnimSection,
        "footer_el": footer_el,
        "name_v": name,
        "group_v": group_label,
        "desc_v": desc,
        "variants_len": str(len(variants)),
    }
    for i, v in enumerate(variants):
        ctx[f"v{i}_title"] = v["title"]
        ctx[f"v{i}_blurb"] = v["blurb"]
        ctx[f"v{i}_code"] = v["code"]
        ctx[f"v{i}_tall"] = bool(v.get("tall", False))
        ctx[f"v{i}_demo"] = v["demo"]()
        ctx[f"v{i}_num"] = i

    @component
    def Page(props=None):
        props = props or {}
        return psx(page_jsx, dict(ctx))

    Page.__name__ = f"AnimPage_{slug.replace('-', '_')}"
    Page.__doc__ = f"{name} - animation playground"
    return Page
