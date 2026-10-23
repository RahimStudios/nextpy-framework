/**
 * NextPy Client-Side Router
 * Provides SPA (Single Page Application) routing with history API
 * Features:
 * - Hash-based and history-based routing
 * - Route parameters and query strings
 * - Route guards/middleware
 * - 404 handling
 * - Programmatic navigation
 */

class NextPyRouter {
    constructor(options = {}) {
        this.routes = [];
        this.currentRoute = null;
        this.currentParams = {};
        this.currentQuery = {};
        this.middleware = [];
        this.notFoundHandler = null;
        this.mode = options.mode || 'history'; // 'history' or 'hash'
        this.basePath = options.basePath || '/';
        
        // Bind event handlers
        this.handlePopState = this.handlePopState.bind(this);
        this.handleHashChange = this.handleHashChange.bind(this);
        
        // Initialize
        this.init();
    }
    
    /**
     * Initialize the router
     */
    init() {
        if (this.mode === 'history') {
            window.addEventListener('popstate', this.handlePopState);
        } else {
            window.addEventListener('hashchange', this.handleHashChange);
        }
    }
    
    /**
     * Register a route
     * @param {string} path - Route path (e.g., '/users/:id')
     * @param {Function} handler - Route handler function
     * @param {Object} options - Route options (meta, middleware, etc.)
     */
    addRoute(path, handler, options = {}) {
        const route = {
            path,
            handler,
            options,
            // Convert path to regex pattern
            pattern: this.pathToRegex(path),
            paramNames: this.extractParamNames(path)
        };
        this.routes.push(route);
        return this;
    }
    
    /**
     * Convert path to regex pattern
     * @param {string} path - Route path
     * @returns {RegExp} Regex pattern
     */
    pathToRegex(path) {
        // Escape special regex characters except for :param and *wildcard
        const escaped = path.replace(/[.+?^${}()|[\]\\]/g, '\\$&');
        // Replace :param with named capture group
        const withParams = escaped.replace(/:([a-zA-Z0-9_]+)/g, '([^/]+)');
        // Replace * with wildcard
        const withWildcard = withParams.replace(/\*/g, '.*');
        return new RegExp(`^${withWildcard}$`);
    }
    
    /**
     * Extract parameter names from path
     * @param {string} path - Route path
     * @returns {Array<string>} Parameter names
     */
    extractParamNames(path) {
        const matches = path.match(/:([a-zA-Z0-9_]+)/g);
        return matches ? matches.map(m => m.substring(1)) : [];
    }
    
    /**
     * Match a path against registered routes
     * @param {string} path - Path to match
     * @returns {Object|null} Matched route with params
     */
    match(path) {
        for (const route of this.routes) {
            const match = path.match(route.pattern);
            if (match) {
                const params = {};
                route.paramNames.forEach((name, index) => {
                    params[name] = match[index + 1];
                });
                return {
                    route,
                    params
                };
            }
        }
        return null;
    }
    
    /**
     * Parse query string from URL
     * @param {string} queryString - Query string (without ?)
     * @returns {Object} Parsed query parameters
     */
    parseQuery(queryString) {
        const query = {};
        if (!queryString) return query;
        
        const pairs = queryString.split('&');
        pairs.forEach(pair => {
            const [key, value] = pair.split('=');
            query[decodeURIComponent(key)] = decodeURIComponent(value || '');
        });
        return query;
    }
    
    /**
     * Get current path based on router mode
     * @returns {string} Current path
     */
    getCurrentPath() {
        if (this.mode === 'history') {
            const path = window.location.pathname;
            return path.substring(this.basePath.length) || '/';
        } else {
            const hash = window.location.hash.slice(1) || '/';
            return hash.split('?')[0];
        }
    }
    
    /**
     * Get current query string
     * @returns {Object} Current query parameters
     */
    getCurrentQuery() {
        if (this.mode === 'history') {
            const queryString = window.location.search.slice(1);
            return this.parseQuery(queryString);
        } else {
            const hash = window.location.hash.slice(1);
            const queryString = hash.split('?')[1];
            return this.parseQuery(queryString);
        }
    }
    
    /**
     * Navigate to a path
     * @param {string} path - Path to navigate to
     * @param {Object} options - Navigation options
     */
    push(path, options = {}) {
        const { query = {}, replace = false } = options;
        
        // Build full URL with query string
        const queryString = Object.keys(query)
            .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(query[key])}`)
            .join('&');
        
        const fullPath = queryString ? `${path}?${queryString}` : path;
        
        if (this.mode === 'history') {
            const url = this.basePath + fullPath;
            if (replace) {
                window.history.replaceState({}, '', url);
            } else {
                window.history.pushState({}, '', url);
            }
        } else {
            const hash = fullPath.startsWith('/') ? fullPath : '/' + fullPath;
            if (replace) {
                window.location.replace('#' + hash);
            } else {
                window.location.hash = hash;
            }
        }
        
        // Trigger route change
        this.handleRouteChange();
    }
    
    /**
     * Replace current route (no history entry)
     * @param {string} path - Path to replace with
     * @param {Object} options - Navigation options
     */
    replace(path, options = {}) {
        this.push(path, { ...options, replace: true });
    }
    
    /**
     * Go back in history
     */
    back() {
        window.history.back();
    }
    
    /**
     * Go forward in history
     */
    forward() {
        window.history.forward();
    }
    
    /**
     * Go to specific history entry
     * @param {number} delta - Number of steps to go
     */
    go(delta) {
        window.history.go(delta);
    }
    
    /**
     * Handle popstate event (history mode)
     */
    handlePopState() {
        this.handleRouteChange();
    }
    
    /**
     * Handle hashchange event (hash mode)
     */
    handleHashChange() {
        this.handleRouteChange();
    }
    
    /**
     * Handle route change
     */
    async handleRouteChange() {
        const path = this.getCurrentPath();
        const query = this.getCurrentQuery();
        
        // Match route
        const matched = this.match(path);
        
        if (matched) {
            const { route, params } = matched;
            this.currentRoute = route;
            this.currentParams = params;
            this.currentQuery = query;
            
            // Run middleware
            for (const middleware of this.middleware) {
                const result = await middleware(route, params, query);
                if (result === false) {
                    return; // Stop navigation
                }
            }
            
            // Run route-specific middleware
            if (route.options.middleware) {
                for (const middleware of route.options.middleware) {
                    const result = await middleware(route, params, query);
                    if (result === false) {
                        return; // Stop navigation
                    }
                }
            }
            
            // Execute route handler
            await route.handler(params, query);
        } else {
            // 404 - route not found
            if (this.notFoundHandler) {
                await this.notFoundHandler(path);
            } else {
                console.warn(`Route not found: ${path}`);
            }
        }
    }
    
    /**
     * Add global middleware
     * @param {Function} middleware - Middleware function
     */
    use(middleware) {
        this.middleware.push(middleware);
        return this;
    }
    
    /**
     * Set 404 handler
     * @param {Function} handler - 404 handler function
     */
    setNotFound(handler) {
        this.notFoundHandler = handler;
        return this;
    }
    
    /**
     * Start the router
     */
    start() {
        this.handleRouteChange();
    }
    
    /**
     * Destroy the router
     */
    destroy() {
        if (this.mode === 'history') {
            window.removeEventListener('popstate', this.handlePopState);
        } else {
            window.removeEventListener('hashchange', this.handleHashChange);
        }
    }
}

// Export for use in browser
if (typeof window !== 'undefined') {
    window.NextPyRouter = NextPyRouter;
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = NextPyRouter;
}
