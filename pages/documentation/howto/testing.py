"""Testing (Unit & E2E) - NextPy Documentation"""

from nextpy.psx import component, Link, register_component
from pages.documentation._components.enhanced_codeblock import EnhancedCodeBlock

register_component("EnhancedCodeBlock", EnhancedCodeBlock)

@component
def TestingGuide():
    unit_example = '''# tests/test_pricing.py — pure logic, no server needed
from lib.pricing import calculate_total

def test_calculate_total_with_tax():
    assert calculate_total(100, tax_rate=0.2) == 120

def test_calculate_total_zero():
    assert calculate_total(0) == 0'''

    action_example = '''# tests/test_actions.py — server actions are plain async functions
import pytest
from unittest.mock import AsyncMock, MagicMock
from lib.user_actions import create_user

@pytest.mark.asyncio
async def test_create_user_validates_email():
    request = MagicMock()
    response = MagicMock()
    result = await create_user(request, response, email="", name="x")
    assert result.get("success") is False'''

    api_example = '''# tests/test_api.py — hit routes through the ASGI app
import pytest
import httpx
from nextpy.server.app import create_app

@pytest.mark.asyncio
async def test_health_endpoint():
    app = create_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport,
                                 base_url="http://test") as client:
        resp = await client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"'''

    e2e_example = '''# tests/e2e/test_home.py — Playwright against the dev server
import re
from playwright.sync_api import Page, expect

def test_homepage_renders(page: Page):
    page.goto("http://localhost:5000")
    expect(page).to_have_title(re.compile("NextPy"))
    expect(page.locator("h1")).to_be_visible()'''

    return (
        <div class="flex flex-col xl:flex-row items-start justify-between gap-2 w-full max-w-6xl mx-auto">
            <article class="flex-1 min-w-0 max-w-4xl antialiased text-zinc-300 selection:bg-blue-500/20 selection:text-blue-300 space-y-12 pb-24 pt-6">
                <div class="flex items-center justify-between border-b border-zinc-800/50 pb-4">
                    <div class="flex items-center gap-2 text-sm font-medium text-zinc-400">
                        <span>Documentation</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span>How-to Guides</span>
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                        <span class="text-white">Testing (Unit & E2E)</span>
                    </div>
                </div>

                <header id="header" class="mb-12">
                    <h1 class="text-2xl sm:text-2xl font-bold tracking-tight text-white mb-6">
                        Testing (Unit & E2E)
                    </h1>
                    <p class="leading-relaxed text-zinc-300">
                        Learn how to test your NextPy application with unit tests and E2E tests.
                    </p>
                </header>

                <div id="overview" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Overview</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        NextPy supports pytest for unit tests and Playwright for E2E testing.
                    </p>
                </div>

                <div id="unit-tests" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Unit tests</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Plain Python modules — pricing helpers, validators, formatters — test directly with pytest:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="tests/test_pricing.py" snippet={unit_example} />
                </div>

                <div id="action-tests" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Testing server actions</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        Actions are async functions — call them with mocked <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">request</code>/<code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">response</code> objects under <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">pytest-asyncio</code>:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="tests/test_actions.py" snippet={action_example} />
                </div>

                <div id="api-tests" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">Testing API routes</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        The app is a standard FastAPI instance — drive it in-process with <code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">httpx.ASGITransport</code>, no running server needed:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="tests/test_api.py" snippet={api_example} />
                </div>

                <div id="e2e-tests" class="space-y-6 pt-8 border-t border-zinc-800/50">
                    <h2 class="text-2xl font-semibold text-white tracking-tight">E2E tests</h2>
                    <p class="text-base leading-7 text-zinc-300">
                        For browser-level coverage, Playwright drives the dev server (<code class="text-zinc-200 font-mono text-sm px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800">nextpy dev</code> on port 5000) and asserts on real rendered pages:
                    </p>
                    <EnhancedCodeBlock lang="python" filename="tests/e2e/test_home.py" snippet={e2e_example} />
                </div>

                <footer class="py-12 flex items-center justify-between gap-6 border-t border-zinc-800/50 mt-12">
                    <div class="w-1/2">
                        <Link href="/documentation/howto/i18n" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Previous</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
                                Internationalization (i18n)
                            </span>
                        </Link>
                    </div>
                    <div class="w-1/2 text-right">
                        <Link href="/documentation/concepts/why-nextpy" className="group block p-5 rounded-xl border border-zinc-800/60 bg-zinc-950/20 hover:border-zinc-700 hover:bg-zinc-900/20 transition-all">
                            <span class="block text-xs font-medium text-zinc-500 tracking-wide uppercase mb-1">Next</span>
                            <span class="text-base font-bold text-white group-hover:text-blue-400 flex items-center justify-end gap-1 transition-colors">
                                Core Concepts
                                <svg class="w-4 h-4 text-zinc-500 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                            </span>
                        </Link>
                    </div>
                </footer>
            </article>

            <aside class="hidden xl:block w-64 shrink-0 sticky top-24 pt-4 pl-8 pb-24 h-[calc(100vh-6rem)] overflow-y-auto">
                <div class="text-sm">
                    <h4 class="font-semibold text-white mb-4 tracking-wide">On this page</h4>
                    <ul class="space-y-3 font-medium text-zinc-400 border-l border-zinc-800/50">
                        <li><a href="#overview" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Overview</a></li>
                        <li><a href="#unit-tests" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Unit tests</a></li>
                        <li><a href="#action-tests" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">Server actions</a></li>
                        <li><a href="#api-tests" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">API routes</a></li>
                        <li><a href="#e2e-tests" class="block pl-4 -ml-px border-l border-transparent hover:text-white hover:border-zinc-500 transition-colors">E2E tests</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    )


def getServerSideProps(context):
    return {"props": {"title": "Testing (Unit & E2E) - NextPy Docs"}}

default = TestingGuide

