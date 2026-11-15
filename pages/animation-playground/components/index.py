"""Components — animation playground index."""

from nextpy.psx import component, Link


@component
def Page():
    return (
        <div class="mx-auto max-w-5xl px-6 py-16">
            <nav class="mb-6 flex items-center gap-2 text-sm text-zinc-500">
                <Link href="/animation-playground" className="hover:text-zinc-300">Playground</Link>
                <span class="text-zinc-700">/</span>
                <span class="font-medium text-zinc-200">Components</span>
            </nav>
            <header class="mb-10">
                <h1 class="text-2xl font-semibold tracking-tight text-white">Components</h1>
                <p class="mt-2 max-w-2xl text-[15px] leading-relaxed text-zinc-500">
                    66 animated examples — live previews with copy-paste PSX code.
                </p>
            </header>
            <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                        <Link href="/animation-playground/components/accordion" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Accordion</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Expand/collapse sections with height tweens and staggered items.</p>
                        </Link>
                        <Link href="/animation-playground/components/alert" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Alert</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Inline alerts — slide, drop, shake and pulse entrances.</p>
                        </Link>
                        <Link href="/animation-playground/components/alert-dialog" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Alert Dialog</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Confirmation modal with backdrop fade and panel zoom.</p>
                        </Link>
                        <Link href="/animation-playground/components/aspect-ratio" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Aspect Ratio</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Fixed-ratio containers with animated reveals.</p>
                        </Link>
                        <Link href="/animation-playground/components/attachment" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Attachment</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">File chips with hover lift and remove animation.</p>
                        </Link>
                        <Link href="/animation-playground/components/avatar" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Avatar</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Avatar groups that spring in and tilt on hover.</p>
                        </Link>
                        <Link href="/animation-playground/components/badge" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Badge</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Status badges with pulse, scale and staggered entrances.</p>
                        </Link>
                        <Link href="/animation-playground/components/breadcrumb" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Breadcrumb</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Trail links with staggered fade-ins.</p>
                        </Link>
                        <Link href="/animation-playground/components/bubble" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Bubble</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Chat bubbles that pop in from either side.</p>
                        </Link>
                        <Link href="/animation-playground/components/button" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Button</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Buttons with hover/tap gestures, loading pulse and spring pop.</p>
                        </Link>
                        <Link href="/animation-playground/components/button-group" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Button Group</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Attached buttons with shared hover and press states.</p>
                        </Link>
                        <Link href="/animation-playground/components/calendar" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Calendar</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Month grids with day-cell hover and selection pop.</p>
                        </Link>
                        <Link href="/animation-playground/components/card" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Card</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Cards that lift on hover, flip in 3D and stagger in.</p>
                        </Link>
                        <Link href="/animation-playground/components/carousel" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Carousel</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Slide tracks translated by keyframes with dot indicators.</p>
                        </Link>
                        <Link href="/animation-playground/components/chart" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Chart</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Bars and lines that draw in with scale/width tweens.</p>
                        </Link>
                        <Link href="/animation-playground/components/checkbox" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Checkbox</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Checkboxes with check-mark scale pop and ripple.</p>
                        </Link>
                        <Link href="/animation-playground/components/code-block" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Code Block</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Code windows with typing reveal and copy feedback.</p>
                        </Link>
                        <Link href="/animation-playground/components/collapsible" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Collapsible</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Show/hide regions animated by maxHeight.</p>
                        </Link>
                        <Link href="/animation-playground/components/combobox" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Combobox</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Searchable dropdowns with filtered-list transitions.</p>
                        </Link>
                        <Link href="/animation-playground/components/command" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Command</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">⌘K palettes that scale in over a blurred backdrop.</p>
                        </Link>
                        <Link href="/animation-playground/components/context-menu" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Context Menu</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Right-click menus that scale from the cursor.</p>
                        </Link>
                        <Link href="/animation-playground/components/data-table" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Data Table</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Sortable rows with hover highlights and layout shifts.</p>
                        </Link>
                        <Link href="/animation-playground/components/date-picker" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Date Picker</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Calendar popovers with month-slide transitions.</p>
                        </Link>
                        <Link href="/animation-playground/components/dialog" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Dialog</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Modals with backdrop fade, panel zoom and exit shrink.</p>
                        </Link>
                        <Link href="/animation-playground/components/direction" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Direction</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">RTL/LTR wrappers — layout flips animate smoothly.</p>
                        </Link>
                        <Link href="/animation-playground/components/drawer" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Drawer</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Edge panels that slide in from any side.</p>
                        </Link>
                        <Link href="/animation-playground/components/dropdown-menu" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Dropdown Menu</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Menus that scale+fade from their trigger.</p>
                        </Link>
                        <Link href="/animation-playground/components/empty" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Empty</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Empty states with gentle float and fade entrances.</p>
                        </Link>
                        <Link href="/animation-playground/components/field" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Field</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Label/control wrappers with focus-ring transitions.</p>
                        </Link>
                        <Link href="/animation-playground/components/hover-card" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Hover Card</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Hover-reveal cards with delayed fade-up.</p>
                        </Link>
                        <Link href="/animation-playground/components/input" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Input</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Inputs with focus ring glow and shake-on-error.</p>
                        </Link>
                        <Link href="/animation-playground/components/input-group" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Input Group</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Addon-attached inputs with segmented focus states.</p>
                        </Link>
                        <Link href="/animation-playground/components/input-otp" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Input OTP</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">OTP cells that pop as digits arrive.</p>
                        </Link>
                        <Link href="/animation-playground/components/item" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Item</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">List rows with hover slide and icon wiggle.</p>
                        </Link>
                        <Link href="/animation-playground/components/kbd" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Kbd</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Key caps with press-down scale on active.</p>
                        </Link>
                        <Link href="/animation-playground/components/label" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Label</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Form labels with subtle emphasis transitions.</p>
                        </Link>
                        <Link href="/animation-playground/components/marker" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Marker</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Inline highlights that sweep in behind text.</p>
                        </Link>
                        <Link href="/animation-playground/components/menubar" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Menubar</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Menu bars whose dropdowns scale from the item.</p>
                        </Link>
                        <Link href="/animation-playground/components/message" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Message</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Chat messages that pop from their side.</p>
                        </Link>
                        <Link href="/animation-playground/components/message-scroller" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Message Scroller</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Scrollable transcripts with smooth auto-scroll.</p>
                        </Link>
                        <Link href="/animation-playground/components/native-select" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Native Select</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Styled selects with animated chevron rotation.</p>
                        </Link>
                        <Link href="/animation-playground/components/navigation-menu" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Navigation Menu</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Top nav with hover panels and underline slides.</p>
                        </Link>
                        <Link href="/animation-playground/components/pagination" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Pagination</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Page buttons with active-state pop and hover lift.</p>
                        </Link>
                        <Link href="/animation-playground/components/popover" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Popover</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Floating panels that scale from their anchor.</p>
                        </Link>
                        <Link href="/animation-playground/components/progress" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Progress</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Bars that fill, sweep and pulse while loading.</p>
                        </Link>
                        <Link href="/animation-playground/components/questionnaire" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Questionnaire</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Multi-step forms with progress and reveal motion.</p>
                        </Link>
                        <Link href="/animation-playground/components/radio-group" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Radio Group</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Options whose dot pops into the selected ring.</p>
                        </Link>
                        <Link href="/animation-playground/components/resizable" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Resizable</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Split panes with drag-handle highlight.</p>
                        </Link>
                        <Link href="/animation-playground/components/scroll-area" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Scroll Area</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Custom scrollbars that fade in on scroll.</p>
                        </Link>
                        <Link href="/animation-playground/components/select" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Select</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Dropdown selects with option highlight transitions.</p>
                        </Link>
                        <Link href="/animation-playground/components/separator" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Separator</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Dividers that draw in with width/scale tweens.</p>
                        </Link>
                        <Link href="/animation-playground/components/sheet" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Sheet</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Edge sheets sliding in with backdrop dim.</p>
                        </Link>
                        <Link href="/animation-playground/components/sidebar" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Sidebar</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">App sidebars with item hover slides and collapse.</p>
                        </Link>
                        <Link href="/animation-playground/components/skeleton" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Skeleton</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Loading placeholders with shimmer sweeps.</p>
                        </Link>
                        <Link href="/animation-playground/components/slider" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Slider</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Range sliders with thumb scale and fill transitions.</p>
                        </Link>
                        <Link href="/animation-playground/components/spinner" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Spinner</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Spinners — rotating rings, pulsing dots, typing bars.</p>
                        </Link>
                        <Link href="/animation-playground/components/switch" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Switch</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Toggles whose thumb slides with spring easing.</p>
                        </Link>
                        <Link href="/animation-playground/components/table" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Table</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Tables with row hover sweeps and sort indicators.</p>
                        </Link>
                        <Link href="/animation-playground/components/tabs" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Tabs</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Tab bars with sliding underline and panel fades.</p>
                        </Link>
                        <Link href="/animation-playground/components/textarea" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Textarea</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Auto-growing inputs with focus glow.</p>
                        </Link>
                        <Link href="/animation-playground/components/toast" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Toast</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Notifications that slide up, stack and auto-dismiss.</p>
                        </Link>
                        <Link href="/animation-playground/components/toggle" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Toggle</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Pressed states with scale pop and color tween.</p>
                        </Link>
                        <Link href="/animation-playground/components/toggle-group" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Toggle Group</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Exclusive toggles with sliding selection.</p>
                        </Link>
                        <Link href="/animation-playground/components/tooltip" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Tooltip</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Tooltips that fade-up after a hover delay.</p>
                        </Link>
                        <Link href="/animation-playground/components/trace" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Trace</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Step traces whose connector fills as you progress.</p>
                        </Link>
                        <Link href="/animation-playground/components/typography" className="group rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 transition-colors hover:border-blue-500/40 hover:bg-zinc-900">
                            <h3 className="text-sm font-semibold text-zinc-200 group-hover:text-blue-400">Typography</h3>
                            <p className="mt-1 text-xs leading-relaxed text-zinc-500">Type scale with staggered line reveals.</p>
                        </Link>
            </div>
        </div>
    )
