"""Legacy docs catch-all &mdash; old v0 documentation URLs.

The documentation was rewritten for the PSX engine. This page catches any
/legacy/* URL and points readers at the new docs.
"""

from nextpy.psx import component, Link


@component
def LegacyRedirect(props=None):
    props = props or {}
    slug = props.get("slug") or props.get("...slug") or ""
    if isinstance(slug, (list, tuple)):
        slug = "/".join(str(s) for s in slug)
    target = "/documentation"

    mapping = {
        "installation": "/documentation/getting-started/installation",
        "quickstart": "/documentation/getting-started/installation",
        "project-architecture": "/documentation/getting-started/project-structure",
        "migration": "/documentation/getting-started/upgrading",
    }
    if slug in mapping:
        target = mapping[slug]

    return (
        <div class="min-h-[70vh] flex items-center justify-center px-4">
            <div class="max-w-lg text-center">
                <div class="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-blue-500/10 border border-blue-500/20 text-blue-400 mb-6">
                    <svg class="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                </div>
                <h1 class="text-3xl font-bold text-white tracking-tight">Documentation moved</h1>
                <p class="mt-4 text-zinc-400 leading-relaxed">
                    The legacy documentation has been replaced by the new NextPy docs.
                    Everything there has been rewritten for the current PSX engine.
                </p>
                <div class="mt-8 flex items-center justify-center gap-4">
                    <Link href={target} className="rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-blue-500 transition-colors">
                        Go to new docs
                    </Link>
                    <Link href="/documentation" className="rounded-lg border border-zinc-700 px-5 py-2.5 text-sm font-medium text-zinc-300 hover:bg-zinc-800 transition-colors">
                        Documentation home
                    </Link>
                </div>
            </div>
        </div>
    )


def getServerSideProps(context):
    params = context.get("params") or {}
    return {"props": {"slug": params.get("slug", "")}}


default = LegacyRedirect
