"""
NextPy Client-Side Router - SPA navigation runtime
Provides client-side routing with prefetching, transitions, and history support.
"""

CLIENT_ROUTER_SCRIPT = r"""
(function() {
    if (window.__nextpyRouterLoaded) return;
    window.__nextpyRouterLoaded = true;

    class NextPyRouter {
        constructor(options = {}) {
            this.routes = options.routes || [];
            this.containerSelector = options.container || '#app';
            this.prefetchCache = new Map();
            this.prefetchTimeout = options.prefetchTimeout || 50;
            this.transitionDuration = options.transitionDuration || 0;
            this.isNavigating = false;
            this.history = [];
            this.maxHistory = options.maxHistory || 50;
            this.currentPath = window.location.pathname;

            this.init();
        }

        init() {
            window.addEventListener('popstate', (e) => this.onPopState(e));
            document.addEventListener('click', (e) => this.onClick(e));
            document.addEventListener('mouseover', (e) => this.onPrefetch(e));
            window.__nextpyNavigate = (url, opts) => this.navigate(url, opts);

            document.dispatchEvent(new CustomEvent('nextpy:router:ready', {
                detail: { router: this }
            }));
        }

        onClick(e) {
            const link = e.target.closest('a[href]');
            if (!link) return;

            const href = link.getAttribute('href');
            if (!href) return;

            if (href.startsWith('#')) return;
            if (link.target && link.target !== '_self') return;
            if (link.hasAttribute('download')) return;
            if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;

            const url = new URL(href, window.location.origin);
            if (url.origin !== window.location.origin) return;

            e.preventDefault();
            this.navigate(url.pathname + url.search + url.hash);
        }

        onPrefetch(e) {
            const link = e.target.closest('a[href]');
            if (!link) return;

            const href = link.getAttribute('href');
            if (!href || href.startsWith('#') || href.startsWith('http')) return;

            if (this.prefetchCache.has(href)) return;

            clearTimeout(link._prefetchTimer);
            link._prefetchTimer = setTimeout(() => {
                this.prefetch(href);
            }, this.prefetchTimeout);
        }

        onPopState(e) {
            const path = window.location.pathname + window.location.search;
            this.loadPage(path, { pushState: false });
        }

        async prefetch(url) {
            if (this.prefetchCache.has(url)) return;

            try {
                const resp = await fetch(url, {
                    headers: { 'X-NextPy-Prefetch': 'true' }
                });
                if (resp.ok) {
                    const html = await resp.text();
                    this.prefetchCache.set(url, {
                        html,
                        timestamp: Date.now()
                    });
                }
            } catch (e) {
                // Prefetch failures are silent
            }
        }

        async navigate(url, options = {}) {
            if (this.isNavigating) return;
            if (url === this.currentPath && !options.force) return;

            this.isNavigating = true;
            const container = document.querySelector(this.containerSelector);
            if (!container) {
                window.location.href = url;
                this.isNavigating = false;
                return;
            }

            document.dispatchEvent(new CustomEvent('nextpy:router:navigationStart', {
                detail: { from: this.currentPath, to: url }
            }));

            try {
                await this.loadPage(url, { pushState: options.pushState !== false });
            } catch (e) {
                console.error('Navigation failed:', e);
                window.location.href = url;
            }

            this.isNavigating = false;
        }

        async loadPage(url, options = {}) {
            const container = document.querySelector(this.containerSelector);
            if (!container) return;

            // Clean up existing hydrated components
            if (window.nextpyComponents) {
                Object.keys(window.nextpyComponents).forEach(id => {
                    try { window.nextpyComponents[id].destroy(); } catch (e) {}
                });
                window.nextpyComponents = {};
            }

            let html;
            const cached = this.prefetchCache.get(url);

            if (cached && (Date.now() - cached.timestamp) < 30000) {
                html = cached.html;
                this.prefetchCache.delete(url);
            } else {
                const resp = await fetch(url, {
                    headers: { 'X-NextPy-Navigation': 'true' }
                });
                if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
                html = await resp.text();
            }

            if (options.pushState) {
                this.history.push(this.currentPath);
                if (this.history.length > this.maxHistory) this.history.shift();
                window.history.pushState({}, '', url);
            }

            this.currentPath = url;

            // Apply transition if configured
            if (this.transitionDuration > 0) {
                container.style.transition = `opacity ${this.transitionDuration}ms ease`;
                container.style.opacity = '0';
                await new Promise(r => setTimeout(r, this.transitionDuration));
            }

            // Extract body content and scripts
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newContainer = doc.querySelector(this.containerSelector);

            if (newContainer) {
                container.innerHTML = newContainer.innerHTML;
            } else {
                container.innerHTML = doc.body.innerHTML;
            }

            // Execute scripts in the new content
            this.executeScripts(container);

            // Update scroll position
            if (!url.includes('#')) {
                window.scrollTo(0, 0);
            }

            // Restore opacity after transition
            if (this.transitionDuration > 0) {
                requestAnimationFrame(() => {
                    container.style.opacity = '1';
                });
            }

            // Update document title
            const newTitle = doc.querySelector('title');
            if (newTitle) document.title = newTitle.textContent;

            document.dispatchEvent(new CustomEvent('nextpy:router:navigationComplete', {
                detail: { url, title: document.title }
            }));
        }

        executeScripts(container) {
            const scripts = container.querySelectorAll('script');
            scripts.forEach(oldScript => {
                const newScript = document.createElement('script');
                Array.from(oldScript.attributes).forEach(attr => {
                    newScript.setAttribute(attr.name, attr.value);
                });
                newScript.textContent = oldScript.textContent;
                oldScript.parentNode.replaceChild(newScript, oldScript);
            });
        }

        back() {
            if (this.history.length > 0) {
                window.history.back();
            } else {
                window.history.back();
            }
        }

        forward() {
            window.history.forward();
        }

        getRoute(path) {
            for (const route of this.routes) {
                if (route.regex && route.regex.test(path)) return route;
                if (route.path === path) return route;
            }
            return null;
        }
    }

    window.NextPyRouter = NextPyRouter;

    // Auto-initialize with empty routes (routes are server-registered)
    window.nextpyRouter = new NextPyRouter({
        container: window.__nextpyRouterContainer || '#app',
        transitionDuration: window.__nextpyRouterTransition || 0
    });
})();
"""


def generate_client_router_script(
    routes: list = None,
    container: str = "#app",
    transition_duration: int = 0,
    prefetch_timeout: int = 50,
) -> str:
    """
    Generate the client-side router script.

    Args:
        routes: List of route definitions [{"path": str, "dynamic": bool}]
        container: CSS selector for the app container
        transition_duration: Milliseconds for navigation transitions
        prefetch_timeout: Milliseconds before prefetching on hover

    Returns:
        JavaScript string for client-side routing
    """
    script = CLIENT_ROUTER_SCRIPT

    config = {
        "container": container,
        "transitionDuration": transition_duration,
        "prefetchTimeout": prefetch_timeout,
        "routes": routes or [],
    }

    config_json = __import__("json").dumps(config)
    return f"""
<script type="text/javascript">
{script}
window.__nextpyRouterConfig = {config_json};
</script>
"""


def generate_navigation_script(url: str, replace: bool = False) -> str:
    """Generate a script for programmatic navigation."""
    if replace:
        js = f"window.location.replace('{url}')"
    else:
        js = f"window.nextpyRouter ? window.nextpyRouter.navigate('{url}') : window.location.href='{url}'"
    return f'<script type="text/javascript">{js};</script>'


def get_router():
    """Get the client router instance (call from server-side context)."""
    return None
