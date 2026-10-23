"""Regression tests for page caching, SPA fragments and link rewriting."""

import os
import time

import pytest

from nextpy.core.component_router import ComponentRouter
from nextpy.server.app import NextPyApp


PAGE = """
from nextpy.psx import component


@component
def Page(**props):
    return (
        <div class="page">
            <h1>{props.get('slug', 'home')}</h1>
        </div>
    )


def getStaticProps(context):
    return {"props": {"slug": context.get('params', {}).get('slug', 'home')}}
"""

DYNAMIC_PAGE = PAGE

SSP_PAGE = """
from nextpy.psx import component


@component
def Page(**props):
    return (
        <div class="private">
            <h1>{props.get('user', 'anonymous')}</h1>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"user": context.get('user', 'anonymous')}}
"""

LAYOUT = """
from nextpy.psx import component


@component
def Layout(children, **props):
    return (
        <html>
            <head><title>Layout</title></head>
            <body>
                <nav><a class="nav" href="/">Home</a></nav>
                {children}
            </body>
        </html>
    )
"""


class FakeRequest:
    def __init__(self, cookies=None, headers=None):
        self.cookies = cookies or {}
        self.headers = headers or {}


def make_router(tmp_path):
    pages = tmp_path / "pages"
    posts = pages / "posts"
    posts.mkdir(parents=True)
    (pages / "layout.psx").write_text(LAYOUT)
    (pages / "index.psx").write_text(PAGE)
    (pages / "posts" / "[slug].psx").write_text(DYNAMIC_PAGE)
    router = ComponentRouter(pages_dir=str(pages))
    router.scan_pages()
    return router


def context_for(params, query=None, request=None):
    return {
        "params": params,
        "query": query or {},
        "request": request or FakeRequest(),
    }


def test_repeated_render_is_served_from_cache(tmp_path):
    router = make_router(tmp_path)
    route, params = router.match("/posts/one")
    calls = {"n": 0}
    original = router._render_component_route

    def counted(route, context, include_layout=True):
        calls["n"] += 1
        return original(route, context, include_layout)

    router._render_component_route = counted

    first = router.render_route(route, context_for(params))
    second = router.render_route(route, context_for(params))

    assert first == second
    assert calls["n"] == 1


def test_cache_key_separates_url_params(tmp_path):
    router = make_router(tmp_path)
    route, _ = router.match("/posts/one")
    one = router.render_route(route, context_for({"slug": "one"}))
    two = router.render_route(route, context_for({"slug": "two"}))
    assert "one" in one and "two" not in one
    assert "two" in two and "one" not in two


def test_cache_key_ignores_request_but_cookies_disable_cache(tmp_path):
    router = make_router(tmp_path)
    route, params = router.match("/posts/one")
    anonymous = context_for(params, request=FakeRequest(cookies={}))
    assert router.is_cacheable(route, anonymous)

    personalised = context_for(
        params, request=FakeRequest(cookies={"session": "abc"})
    )
    assert not router.is_cacheable(route, personalised)

    calls = {"n": 0}
    original = router._render_component_route

    def counted(route, context, include_layout=True):
        calls["n"] += 1
        return original(route, context, include_layout)

    router._render_component_route = counted
    router.render_route(route, personalised)
    router.render_route(route, personalised)
    assert calls["n"] == 2


def test_get_server_side_props_pages_are_not_cached(tmp_path):
    router = make_router(tmp_path)
    ssp = tmp_path / "pages" / "private.psx"
    ssp.write_text(SSP_PAGE)
    router.scan_pages()

    route, params = router.match("/private")
    assert not router.is_cacheable(route, context_for(params))


def test_fragment_render_contains_only_page_wrapper(tmp_path):
    router = make_router(tmp_path)
    route, params = router.match("/posts/one")

    full = router.render_route(route, context_for(params))
    fragment = router.render_route(
        route, context_for(params), include_layout=False
    )

    assert "<html" in full.lower()
    assert "nextpy-layout" not in full
    assert 'id="nextpy-page"' in full
    assert "<html" not in fragment.lower()
    assert fragment.count('id="nextpy-page"') == 1
    assert "nav" not in fragment


def test_layout_signature_changes_when_layout_changes(tmp_path):
    router = make_router(tmp_path)
    route, _ = router.match("/posts/one")
    first = router.get_layout_signature(route)

    layout = tmp_path / "pages" / "layout.psx"
    time.sleep(0.01)
    layout.write_text(LAYOUT + "\n# changed\n")

    assert router.get_layout_signature(route) != first


def test_render_errors_are_not_cached(tmp_path):
    router = make_router(tmp_path)
    broken = tmp_path / "pages" / "broken.psx"
    broken.write_text(
        """
from nextpy.psx import component


@component
def Page(**props):
    raise RuntimeError('boom')
"""
    )
    router.scan_pages()
    route, params = router.match("/broken")

    calls = {"n": 0}
    original = router._render_component_route

    def counted(route, context, include_layout=True):
        calls["n"] += 1
        return original(route, context, include_layout)

    router._render_component_route = counted
    first = router.render_route(route, context_for(params))
    second = router.render_route(route, context_for(params))

    assert "Error rendering route" in first
    assert "Error rendering route" in second
    assert calls["n"] == 2


def test_mark_internal_links_marks_navigation_and_strips_htmx():
    html = (
        '<a class="x" href="/about" hx-get="/about" '
        'hx-target="#main-content" hx-trigger="mouseenter">About</a>'
        '<a href="https://example.com" hx-get="https://example.com">Ext</a>'
        "<a href='/contact' target='_blank'>New tab</a>"
    )
    marked = NextPyApp._mark_internal_links(html)

    assert 'data-nextpy-link="true"' in marked
    assert 'data-nextpy-prefetch="true"' in marked
    assert "hx-get=\"/about\"" not in marked
    assert "hx-trigger" not in marked
    assert 'href="https://example.com"' in marked
    assert "data-nextpy-prefetch=\"true\" href=\"https://" not in marked
    assert "target='_blank'" in marked


def test_inline_scripts_are_injected_before_body_end():
    html = "<html><body><main>Hi</main></body></html>"
    result = NextPyApp._inject_inline_script(html, "window.x = 1;", "router")
    assert 'data-nextpy-runtime="router"' in result
    assert result.index("window.x = 1;") < result.lower().rindex("</body>")
    assert result.lower().rindex("</html>") > result.index("window.x = 1;")

    assert NextPyApp._inject_inline_script(
        result, "window.x = 1;", "router"
    ) == result
