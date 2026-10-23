"""
JobHub - Logout fallback page.

The nav uses a direct POST form to /api/logout so the browser follows the
redirect and applies the cleared cookie.  This page remains for bookmarks and
offers the same form.
"""

from nextpy.psx import component


@component
def LogoutPage(props=None):
    return (
        <div class="py-16 text-center">
            <h1 class="text-2xl font-bold text-gray-900">Log out</h1>
            <p class="mt-2 text-gray-600">End your JobHub session on this device.</p>
            <form method="post" action="/api/logout" class="mt-6">
                <button
                    type="submit"
                    class="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700"
                >
                    Log out
                </button>
            </form>
        </div>
    )


default = LogoutPage
