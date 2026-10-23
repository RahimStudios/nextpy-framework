"""
PSX Package - Clean Python Syntax eXtension for NextPy
Production-ready PSX with clean architecture and enhanced full-stack support
"""

# Core imports
from .core.parser import PSXElement, PSXParser, psx, render_psx, fragment, key
from .core.runtime import process_python_logic, runtime
from .core.evaluator import SafeExpressionEngine
from .vdom.vnode import VNode, create_element, render, update, get_vdom_metrics
from .renderer.renderer import PSXRenderer, renderer
from .components.component import (
    PSXComponent, component, class_component, ChildrenComponent,
    register_component, clsx, Component, Props, Children,
    Head, Link, Script, Image, Meta, Title, Layout, Container,
    Row, Col, Form, Input, Button, Navbar, NavItem, Card, List,
    Conditional, Loop, ErrorBoundary, Suspense,
    # React Hooks
    useState, useEffect, useContext, useReducer, useRef, useMemo, useCallback,
    useImperativeHandle, useLayoutEffect, useDebugValue, useTransition,
    useDeferredValue, useId,
    # Custom Hooks
    useCounter, useToggle, useLocalStorage, useFetch, useAction, useCrudEvent, useDebounce,
    useInterval, usePrevious, useAsync, useMediaQuery, useGeolocation, usePerformance,
    # Server action bridge
    callServerAction,
    # Event Handlers
    create_onclick, create_ondblclick, create_onmousedown, create_onmouseup,
    create_onmouseover, create_onmouseout, create_onmouseenter, create_onmouseleave, create_onmousemove,
    create_onchange, create_onsubmit, create_onreset, create_onfocus, create_onblur,
    create_oninput, create_oninvalid, create_onselect,
    create_onkeydown, create_onkeyup, create_onkeypress,
    create_ontouchstart, create_ontouchend, create_ontouchmove, create_ontouchcancel,
    create_onload, create_onunload, create_onresize, create_onscroll,
    create_ondrag, create_ondragstart, create_ondragend, create_ondragenter,
    create_ondragleave, create_ondragover, create_ondrop,
    create_onplay, create_onpause, create_onended, create_onvolumechange,
    create_ontimeupdate, create_onseeking, create_onseeked,
    create_onloadstart, create_onprogress, create_onerror, create_onabort,
    create_onanimationstart, create_onanimationend, create_onanimationiteration,
    create_ontransitionend, create_ontransitionrun, create_ontransitionstart,
    create_onwheel, create_oncopy, create_oncut, create_onpaste,
    create_onbeforeprint, create_onafterprint, create_onstorage,
    create_onopen, create_onmessage, create_onclose, create_oninstall, create_onactivate
)
from .utils.helpers import compile_psx, compile_psx_file, is_psx_file, PSXCompiler

# Load enhanced client runtime
import os
enhanced_runtime_path = os.path.join(os.path.dirname(__file__), 'runtime', 'enhanced_client_runtime.js')
try:
    with open(enhanced_runtime_path, 'r') as f:
        ENHANCED_CLIENT_RUNTIME_SCRIPT = f.read()
except FileNotFoundError:
    ENHANCED_CLIENT_RUNTIME_SCRIPT = ""

CLIENT_ROUTER_SCRIPT = r"""
(function () {
    if (window.__nextpyRouterInstalled) return;
    window.__nextpyRouterInstalled = true;

    var FRESH_MS = 5 * 60 * 1000;        // serve from cache without revalidation
    var STALE_MS = 15 * 60 * 1000;       // serve stale, then revalidate in background
    var MAX_ENTRIES = 40;
    var MAX_PARALLEL_PREFETCH = 3;

    var cache = new Map();               // href -> {html, ts, fragment, title, sig, stale}
    var inflight = new Map();            // key -> Promise
    var executedSrc = new Set();
    var scrollPositions = new Map();
    var prefetchQueue = [];
    var prefetchActive = 0;
    var observedLinks = new Set();
    var observer = null;
    var navToken = 0;
    // The URL currently rendered in the DOM. Location changes before popstate
    // fires, so compare against this instead of window.location.
    var renderedHref = window.location.pathname + window.location.search;

    function isInternal(url) {
        return url.origin === window.location.origin &&
            (url.protocol === 'http:' || url.protocol === 'https:');
    }

    function currentUrl() {
        return window.location.pathname + window.location.search;
    }

    function layoutSig() {
        var meta = document.querySelector('meta[name="nextpy-layout"]');
        return meta ? (meta.getAttribute('content') || '') : '';
    }

    function updateLayoutSig(sig) {
        if (!sig) return;
        var meta = document.querySelector('meta[name="nextpy-layout"]');
        if (!meta) {
            meta = document.createElement('meta');
            meta.setAttribute('name', 'nextpy-layout');
            document.head.appendChild(meta);
        }
        meta.setAttribute('content', sig);
    }

    function cacheGet(href) {
        var entry = cache.get(href);
        if (!entry) return null;
        var age = Date.now() - entry.ts;
        if (age > STALE_MS) {
            cache.delete(href);
            return null;
        }
        cache.delete(href);
        cache.set(href, entry);
        // Personalized (uncacheable) pages paint instantly from cache but are
        // always revalidated in the background.
        entry.stale = entry.personal === true || age > FRESH_MS;
        return entry;
    }

    function cacheSet(href, entry) {
        entry.ts = Date.now();
        entry.stale = false;
        if (cache.has(href)) cache.delete(href);
        cache.set(href, entry);
        while (cache.size > MAX_ENTRIES) {
            cache.delete(cache.keys().next().value);
        }
    }

    function fetchPage(href, opts) {
        opts = opts || {};
        var key = href + (opts.fragment ? '|fragment' : '|full');
        if (inflight.has(key)) return inflight.get(key);

        var headers = {'X-NextPy-Navigation': 'true', 'Accept': 'text/html'};
        if (opts.fragment) {
            headers['X-NextPy-Fragment'] = 'true';
            var sig = layoutSig();
            if (sig) headers['X-NextPy-Layout-Sig'] = sig;
        }

        var promise = fetch(href, {headers: headers})
            .then(function (response) {
                if (!response.ok) throw new Error('HTTP ' + response.status);
                var fragment = response.headers.get('X-NextPy-Fragment') === 'true';
                var title = response.headers.get('X-NextPy-Title') || '';
                var sig = response.headers.get('X-NextPy-Layout-Sig') || '';
                var personal = response.headers.get('X-NextPy-Cacheable') === 'false';
                return response.text().then(function (html) {
                    return {
                        html: html,
                        fragment: fragment,
                        title: title,
                        sig: sig,
                        personal: personal,
                    };
                });
            })
            .finally(function () { inflight.delete(key); });

        inflight.set(key, promise);
        return promise;
    }

    function runScripts(root) {
        var scripts = (root || document).querySelectorAll('script');
        scripts.forEach(function (oldScript) {
            // Framework runtimes are already executing in this document.
            if (oldScript.hasAttribute('data-nextpy-runtime')) {
                oldScript.parentNode.removeChild(oldScript);
                return;
            }
            // External scripts already loaded once need not be fetched/executed again.
            if (oldScript.src) {
                if (executedSrc.has(oldScript.src)) return;
                executedSrc.add(oldScript.src);
            }
            var newScript = document.createElement('script');
            for (var i = 0; i < oldScript.attributes.length; i++) {
                newScript.setAttribute(oldScript.attributes[i].name, oldScript.attributes[i].value);
            }
            newScript.textContent = oldScript.textContent;
            oldScript.parentNode.replaceChild(newScript, oldScript);
        });
    }

    function finishNavigation(href, opts) {
        if (opts.replace) {
            history.replaceState({}, '', href);
        } else if (opts.push !== false) {
            history.pushState({}, '', href);
        }
        renderedHref = href;
        if (opts.scroll !== false) {
            var y = opts.restoreScroll ? (scrollPositions.get(href) || 0) : 0;
            window.scrollTo(0, y);
        }
        document.dispatchEvent(new CustomEvent('nextpy:navigate', {detail: {url: href}}));
        scanLinks();
    }

    function applyEntry(entry, href, opts) {
        if (entry.fragment) {
            // Fragments only contain page content, not the layout. Applying a
            // cached fragment from another layout would keep the previous
            // layout (e.g. docs sidebar) around an unrelated page.
            if (!entry.sig || entry.sig !== layoutSig()) return false;
            var target = document.getElementById('nextpy-page');
            if (!target) return false;
            var holder = document.createElement('div');
            holder.innerHTML = entry.html;
            var incoming = holder.querySelector('#nextpy-page');
            var node = incoming || holder;
            target.replaceWith(node);
            runScripts(node);
            if (entry.title) document.title = entry.title;
            if (entry.sig) updateLayoutSig(entry.sig);
            finishNavigation(href, opts);
            return true;
        }

        var parsed = new DOMParser().parseFromString(entry.html, 'text/html');
        if (!parsed.body) throw new Error('Navigation returned invalid HTML');
        document.body.replaceWith(parsed.body);
        if (parsed.title && parsed.title.textContent) {
            document.title = parsed.title.textContent;
        }
        var meta = parsed.querySelector('meta[name="nextpy-layout"]');
        if (meta) updateLayoutSig(meta.getAttribute('content'));
        runScripts(document.body);
        finishNavigation(href, opts);
        return true;
    }

    async function load(url, opts) {
        opts = opts || {};
        var target = new URL(url, window.location.href);
        if (!isInternal(target)) {
            window.location.href = target.href;
            return;
        }

        // Same rendered document: only the hash changed. Do not compare with
        // window.location here; on popstate the URL has already changed while
        // the DOM still shows the previous page.
        if (target.pathname + target.search === renderedHref) {
            if (target.hash) {
                var el = document.querySelector(target.hash);
                if (el) el.scrollIntoView();
                else window.location.hash = target.hash;
                if (opts.push !== false) history.pushState({}, '', target.href);
            } else if (opts.scroll !== false) {
                window.scrollTo(0, 0);
            }
            return;
        }

        var href = target.pathname + target.search;
        var token = ++navToken;
        scrollPositions.set(currentUrl(), window.scrollY);

        var cached = cacheGet(href);
        if (cached) {
            var applied = applyEntry(cached, href, opts);
            if (applied === false) {
                // Cached fragment belongs to a different layout; discard it
                // and fetch the page for the current layout.
                cache.delete(href);
                cached = null;
            }
        }
        if (cached && !cached.stale) {
            return;
        }

        if (cached && cached.stale) {
            // Instant paint from cache, refresh in the background.
            fetchPage(href, {fragment: cached.fragment})
                .then(function (fresh) {
                    cacheSet(href, fresh);
                    if (token === navToken && currentUrl() === href) {
                        applyEntry(fresh, href, {replace: true, scroll: false});
                    }
                })
                .catch(function () {});
            return;
        }

        try {
            var entry;
            try {
                entry = await fetchPage(href, {fragment: !!layoutSig()});
            } catch (fragmentError) {
                entry = await fetchPage(href, {fragment: false});
            }
            if (token !== navToken) return;
            cacheSet(href, entry);
            var applied = applyEntry(entry, href, opts);
            if (applied === false) {
                entry = await fetchPage(href, {fragment: false});
                if (token !== navToken) return;
                cacheSet(href, entry);
                applyEntry(entry, href, opts);
            }
        } catch (error) {
            console.error('[NextPy] client navigation failed; using browser navigation', error);
            window.location.href = target.href;
        }
    }

    function enqueuePrefetch(href) {
        if (prefetchQueue.indexOf(href) !== -1) return;
        prefetchQueue.push(href);
        pumpPrefetch();
    }

    function pumpPrefetch() {
        while (prefetchActive < MAX_PARALLEL_PREFETCH && prefetchQueue.length) {
            var href = prefetchQueue.shift();
            if (cache.has(href)) continue;
            prefetchActive++;
            fetchPage(href, {fragment: !!layoutSig()})
                .then(function (entry) { cacheSet(href, entry); })
                .catch(function () {})
                .finally(function () {
                    prefetchActive--;
                    pumpPrefetch();
                });
        }
    }

    function prefetch(url) {
        var target;
        try { target = new URL(url, window.location.href); } catch (e) { return; }
        if (!isInternal(target)) return;
        if (target.pathname === window.location.pathname &&
            target.search === window.location.search) return;
        var href = target.pathname + target.search;
        if (cache.has(href)) return;
        enqueuePrefetch(href);
    }

    function idlePrefetch(href) {
        if (window.requestIdleCallback) {
            window.requestIdleCallback(function () { prefetch(href); }, {timeout: 1500});
        } else {
            setTimeout(function () { prefetch(href); }, 200);
        }
    }

    function scanLinks() {
        var links = document.querySelectorAll('a[data-nextpy-link], a[data-nextpy-prefetch]');
        if (!links.length || !('IntersectionObserver' in window)) return;

        if (!observer) {
            observer = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (!entry.isIntersecting) return;
                    observer.unobserve(entry.target);
                    var href = entry.target.getAttribute('href');
                    if (href) idlePrefetch(href);
                });
            }, {rootMargin: '200px'});
        }

        links.forEach(function (link) {
            if (observedLinks.has(link)) return;
            observedLinks.add(link);
            observer.observe(link);
        });
    }

    document.addEventListener('click', function (event) {
        if (event.defaultPrevented || event.button !== 0 ||
            event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;

        var target = event.target;
        if (!target || typeof target.closest !== 'function') return;
        var link = target.closest('a[data-nextpy-link], a[href]');
        if (!link) return;
        if (link.target && link.target !== '_self') return;
        if (link.hasAttribute('download')) return;

        var raw = link.getAttribute('href');
        if (!raw || raw.indexOf('mailto:') === 0 || raw.indexOf('tel:') === 0) return;

        var url = new URL(link.href, window.location.href);
        if (!isInternal(url)) return;

        event.preventDefault();
        // Prevent HTMX's bubbling click handler from issuing a second request.
        event.stopPropagation();

        load(url.href, {
            replace: link.dataset.nextpyReplace === 'true',
            scroll: link.dataset.nextpyScroll !== 'false'
        });
    }, true);

    document.addEventListener('mouseenter', function (event) {
        var target = event.target;
        if (!target || typeof target.closest !== 'function') return;
        var link = target.closest('a[data-nextpy-prefetch], a[data-nextpy-link]');
        if (!link) return;
        var href = link.getAttribute('href');
        if (href) prefetch(link.href);
    }, true);

    window.addEventListener('popstate', function () {
        load(window.location.href, {push: false, restoreScroll: true});
    });

    window.__nextpyNavigate = function (url, replace, scroll) {
        load(url, {replace: !!replace, scroll: scroll !== false});
    };

    window.__nextpyRouter = {
        navigate: window.__nextpyNavigate,
        prefetch: prefetch,
        cacheSize: function () { return cache.size; },
        clearCache: function () { cache.clear(); }
    };

    document.addEventListener('nextpy:navigate', scanLinks);
    if (document.readyState !== 'loading') scanLinks();
    else document.addEventListener('DOMContentLoaded', scanLinks);
})();
"""

CRUD_RUNTIME_SCRIPT = r"""
(function () {
    if (window.__nextpyCrudRuntime) return;
    window.__nextpyCrudRuntime = true;

    // --- DOM Utilities ---
    function getElementTarget(event) {
        var target = event.target;
        if (target instanceof Element) return target;
        if (target && target.parentElement instanceof Element) return target.parentElement;
        return null;
    }

    function findItem(root, id) {
        var items = root.querySelectorAll('[data-nextpy-item]');
        var searchId = String(id);
        for (var i = 0; i < items.length; i++) {
            if (items[i].getAttribute('data-nextpy-item') === searchId) return items[i];
        }
        return null;
    }

    // --- CSS ---
    if (!document.getElementById('nextpy-modal-styles')) {
        var style = document.createElement('style');
        style.id = 'nextpy-modal-styles';
        style.textContent = '.nextpy-modal-open { overflow: hidden; }';
        document.head.appendChild(style);
    }

    // --- State ---
    var pendingDelete = { id: null, config: null };

    // --- Core Helpers ---
    function roots() { return document.querySelectorAll('[data-nextpy-crud]'); }
    function error(root, message) {
        var target = root.querySelector('[data-nextpy-error]');
        if (target) { target.textContent = message || ''; target.classList.toggle('hidden', !message); }
    }
    function status(root, message) {
        var target = root.querySelector('[data-nextpy-status]');
        if (target) target.textContent = message;
    }
    async function callServerAction(actionName, data) {
        var token = window.localStorage.getItem('nextpy_access_token') ||
            window.sessionStorage.getItem('nextpy_access_token');
        var headers = {'Content-Type': 'application/json', 'Accept': 'application/json'};
        if (token) headers.Authorization = 'Bearer ' + token;
        var response = await fetch('/__nextpy/actions/execute', {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({action: actionName, params: data || {}})
        });
        var result = await response.json();
        if (!response.ok || result.error) {
            var msg = 'Server action failed';
            if (result.error) {
                msg = typeof result.error === 'object' ? (result.error.message || JSON.stringify(result.error)) : result.error;
            }
            throw new Error(msg);
        }
        return result;
    }

    // --- Modal ---
    function showCustomConfirm(opts) {
        if (typeof opts === 'string') opts = { message: opts };
        var title = opts.title || 'Confirm Action';
        var message = opts.message || '';
        var confirmText = opts.confirmText || 'Confirm';
        var cancelText = opts.cancelText || 'Cancel';

        return new Promise(function (resolve) {
            var overlay = document.createElement('div');
            overlay.className = 'fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/5 bg-opacity-25 backdrop-blur-sm transition-opacity duration-200';

            var card = document.createElement('div');
            card.className = 'w-full max-w-sm p-6 bg-white rounded-xl shadow-xl';

            var h3 = document.createElement('h3');
            h3.className = 'text-lg font-semibold text-gray-900 mb-2';
            h3.textContent = title;
            card.appendChild(h3);

            var bodyText = document.createElement('p');
            bodyText.className = 'text-sm text-gray-600 mb-6';
            bodyText.textContent = message;
            card.appendChild(bodyText);

            var actions = document.createElement('div');
            actions.className = 'flex justify-end gap-3';

            var cancelBtn = document.createElement('button');
            cancelBtn.type = 'button';
            cancelBtn.className = 'px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500';
            cancelBtn.textContent = cancelText;

            var confirmBtn = document.createElement('button');
            confirmBtn.type = 'button';
            confirmBtn.className = 'px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500';
            confirmBtn.textContent = confirmText;

            actions.appendChild(cancelBtn);
            actions.appendChild(confirmBtn);
            card.appendChild(actions);
            overlay.appendChild(card);

            document.body.appendChild(overlay);
            document.body.classList.add('nextpy-modal-open');

            function close(result) {
                cancelBtn.removeEventListener('click', handleCancel);
                confirmBtn.removeEventListener('click', handleConfirm);
                document.removeEventListener('keydown', handleKey);
                overlay.removeEventListener('click', handleBackdrop);
                if (overlay.parentNode) overlay.parentNode.removeChild(overlay);
                document.body.classList.remove('nextpy-modal-open');
                resolve(result);
            }
            function handleCancel() { close(false); }
            function handleConfirm() { close(true); }
            function handleKey(e) { if (e.key === 'Escape') close(false); }
            function handleBackdrop(e) { if (e.target === overlay) close(false); }

            cancelBtn.addEventListener('click', handleCancel);
            confirmBtn.addEventListener('click', handleConfirm);
            document.addEventListener('keydown', handleKey);
            overlay.addEventListener('click', handleBackdrop);
            confirmBtn.focus();
        });
    }

    // --- Generic applyChange ---
    function applyFieldValues(element, item) {
        var fields = element.querySelectorAll('[data-nextpy-field]');
        for (var i = 0; i < fields.length; i++) {
            var el = fields[i];
            var name = el.getAttribute('data-nextpy-field');
            if (name === undefined || name === null || name === '') continue;
            var value = item[name];
            if (value === undefined) continue;

            if (el.type === 'checkbox' || el.type === 'radio') {
                el.checked = !!value;
            } else if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.tagName === 'SELECT') {
                el.value = value;
            } else {
                el.textContent = value;
            }
        }
    }

    function applyChange(root, message, config) {
        var item = message.data;
        var idParam = config.idParam || 'id';
        var itemId = item[idParam] !== undefined ? item[idParam] : item.id;

        // --- DELETED ---
        if (message.action === 'deleted') {
            var el = findItem(root, itemId);
            if (el) el.remove();
            window.dispatchEvent(new CustomEvent('nextpy:crud:changed', { detail: { action: 'deleted', item: item, config: config, root: root } }));
            return;
        }

        // --- CREATED: clone template from existing item ---
        if (message.action === 'created') {
            if (findItem(root, itemId)) return;
            var list = root.querySelector('[data-nextpy-list]');
            if (!list) return;

            // Find a template: first existing item, or build a generic one from item keys
            var template = list.querySelector('[data-nextpy-item]');
            var newItem;
            if (template) {
                newItem = template.cloneNode(true);
            } else {
                // No template: build a generic <li> with data-nextpy-field for each key
                newItem = document.createElement('li');
                newItem.className = 'flex items-center gap-4 p-4 rounded-lg bg-gray-50';
                var itemKeys = Object.keys(item);
                for (var k = 0; k < itemKeys.length; k++) {
                    var key = itemKeys[k];
                    var val = item[key];
                    if (key === 'id') continue;
                    if (typeof val === 'boolean') {
                        var cb = document.createElement('input');
                        cb.type = 'checkbox';
                        cb.setAttribute('data-nextpy-field', key);
                        cb.setAttribute('data-nextpy-toggle', itemId);
                        cb.className = 'w-5 h-5 text-blue-600 rounded focus:ring-blue-500';
                        cb.checked = !!val;
                        newItem.appendChild(cb);
                    } else if (typeof val === 'string' || typeof val === 'number') {
                        var span = document.createElement('span');
                        span.setAttribute('data-nextpy-field', key);
                        span.className = 'flex-1 text-gray-900';
                        span.textContent = String(val);
                        newItem.appendChild(span);
                    }
                }
                // Add delete button
                var del = document.createElement('button');
                del.type = 'button';
                del.setAttribute('data-nextpy-delete', itemId);
                del.className = 'text-sm font-medium text-red-600 hover:text-red-800';
                del.textContent = 'Delete';
                newItem.appendChild(del);
            }

            // Set the item id attribute
            newItem.setAttribute('data-nextpy-item', itemId);

            // Rewrite any id-scoped data attributes (data-nextpy-toggle, data-nextpy-delete)
            var toggle = newItem.querySelector('[data-nextpy-toggle]');
            if (toggle) toggle.setAttribute('data-nextpy-toggle', itemId);
            var delBtn = newItem.querySelector('[data-nextpy-delete]');
            if (delBtn) delBtn.setAttribute('data-nextpy-delete', itemId);

            // Fill field values from item data
            applyFieldValues(newItem, item);

            list.appendChild(newItem);
            window.dispatchEvent(new CustomEvent('nextpy:crud:changed', { detail: { action: 'created', item: item, config: config, root: root } }));
            return;
        }

        // --- UPDATED: generic field update ---
        var element = findItem(root, itemId);
        if (!element) return;
        applyFieldValues(element, item);
        window.dispatchEvent(new CustomEvent('nextpy:crud:changed', { detail: { action: 'updated', item: item, config: config, root: root } }));
    }

    // --- Initialization per CRUD root ---
    roots().forEach(function (root) {
        var config = JSON.parse(root.dataset.nextpyCrud || '{}');
        var createAction = config.createAction || 'create';
        var updateAction = config.updateAction || 'update';
        var deleteAction = config.deleteAction || 'delete';
        var wsChannel = config.wsChannel || config.resource || 'items';
        var messageType = config.messageType || (config.resource || 'ITEM') + '_CHANGED';

        // --- Create form ---
        var form = root.querySelector('[data-nextpy-action="create"]');
        if (form) form.addEventListener('submit', async function (event) {
            event.preventDefault(); error(root, '');
            var body = {};
            form.querySelectorAll('[data-nextpy-field]').forEach(function (field) {
                body[field.dataset.nextpyField] = field.value;
            });
            try {
                await callServerAction(createAction, body);
                if (config.createReset !== false) form.reset();
            }
            catch (err) { error(root, err.message); }
        });

        // --- Toggle (change) ---
        root.addEventListener('change', async function (event) {
            var target = getElementTarget(event);
            if (!target) return;
            var toggle = target.closest('[data-nextpy-toggle]');
            if (!toggle) return;
            var itemId = toggle.dataset.nextpyToggle;
            var idParam = config.idParam || 'id';
            var body = {};
            body[idParam] = Number(itemId);
            if (config.updateFields) {
                for (var f in config.updateFields) {
                    body[f] = config.updateFields[f];
                }
            }
            try { await callServerAction(updateAction, body); }
            catch (err) { error(root, err.message); toggle.checked = !toggle.checked; }
        });

        // --- Click: modal confirm/cancel + delete ---
        root.addEventListener('click', async function (event) {
            var target = getElementTarget(event);
            if (!target) return;

            // Modal confirm
            var confirmBtn = target.closest('[data-nextpy-modal-confirm]');
            if (confirmBtn) {
                event.preventDefault();
                event.stopPropagation();
                var modal = document.querySelector('[data-delete-modal]');
                if (modal) { modal.classList.add('hidden'); modal.style.display = ''; }
                if (pendingDelete.id !== null && pendingDelete.config) {
                    var idParam = pendingDelete.config.idParam || 'id';
                    var body = {};
                    body[idParam] = pendingDelete.id;
                    try { await callServerAction(pendingDelete.config.deleteAction, body); }
                    catch (err) { error(root, err.message); }
                    pendingDelete = { id: null, config: null };
                }
                return;
            }

            // Modal cancel
            var cancelBtn = target.closest('[data-nextpy-modal-cancel]');
            if (cancelBtn) {
                event.preventDefault();
                event.stopPropagation();
                var modal = document.querySelector('[data-delete-modal]');
                if (modal) { modal.classList.add('hidden'); modal.style.display = ''; }
                pendingDelete = { id: null, config: null };
                return;
            }

            // Delete button
            var button = target.closest('[data-nextpy-delete]');
            if (!button) return;
            var itemId = button.dataset.nextpyDelete;

            // PSX-rendered modal
            if (config.deleteConfirm === 'psx') {
                var itemTitle = 'this item';
                var listItem = button.closest('[data-nextpy-item]');
                if (listItem) {
                    var firstText = listItem.querySelector('[data-nextpy-field]');
                    if (firstText) itemTitle = firstText.textContent || itemTitle;
                }
                pendingDelete = { id: Number(itemId), config: config };
                var modal = document.querySelector('[data-delete-modal]');
                if (modal) {
                    var titleEl = modal.querySelector('[data-nextpy-modal-title]');
                    if (titleEl) titleEl.textContent = itemTitle;
                    modal.classList.remove('hidden');
                    modal.style.display = 'flex';
                    return;
                }
            }

            // Default confirm modal
            if (config.deleteConfirm !== false && config.deleteConfirm !== 'psx') {
                var confirmMsg = typeof config.deleteConfirm === 'string' ? config.deleteConfirm : 'Delete this item?';
                var confirmed = await showCustomConfirm({ message: confirmMsg, confirmText: 'Delete' });
                if (!confirmed) return;
            }

            var idParam = config.idParam || 'id';
            var body = {};
            body[idParam] = Number(itemId);
            try {
                await callServerAction(deleteAction, body);
            } catch (err) {
                error(root, err.message);
            }
        });

        // --- WebSocket ---
        var protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        var socket;
        var reconnectTimer;
        var reconnectDelay = 1000;

        function connect() {
            socket = new WebSocket(protocol + '//' + window.location.host + '/ws');
            socket.addEventListener('open', function () {
                status(root, 'Live');
                reconnectDelay = 1000;
                socket.send(JSON.stringify({type: 'subscribe', channel: wsChannel}));
            });
            socket.addEventListener('close', function () {
                status(root, 'Offline');
                clearTimeout(reconnectTimer);
                reconnectTimer = setTimeout(function () {
                    reconnectDelay = Math.min(reconnectDelay * 2, 30000);
                    connect();
                }, reconnectDelay);
            });
            socket.addEventListener('error', function () {
                status(root, 'Offline');
            });
            socket.addEventListener('message', function (event) {
                var message;
                try { message = JSON.parse(event.data); }
                catch (err) { return; }
                if (message.type === messageType) applyChange(root, message, config);
            });
        }
        connect();
    });
})();
"""

            



# Hydration Engine imports
from .hydration import (
    HydrationEngine, get_hydration_engine,
    interactive_component, enable_hydration_globally, create_interactive_page,
    hydrate_component, get_component_hydrator,
)

# Convenience functions
def render_psx_component(element, context=None):
    """Render PSX component using the clean renderer with enhanced full-stack support"""
    html = renderer.render(element, context)
    
    # Inject JavaScript runtime scripts for interactive components and full HTML documents
    try:
        from .runtime.js_actions_runtime import JS_ACTION_RUNTIME_SCRIPT
        
        # Always inject enhanced runtime for full-stack applications
        if ENHANCED_CLIENT_RUNTIME_SCRIPT:
            html = f"<script>{ENHANCED_CLIENT_RUNTIME_SCRIPT}</script>{html}"
        
        # Inject legacy runtime for backwards compatibility
        if 'data-handler-' in html or 'data-bind' in html or '<html' in html:
            html = f"<script>{JS_ACTION_RUNTIME_SCRIPT}</script>{html}"
            
    except ImportError:
        # Fallback to enhanced runtime only
        if ENHANCED_CLIENT_RUNTIME_SCRIPT:
            html = f"<script>{ENHANCED_CLIENT_RUNTIME_SCRIPT}</script>{html}"
    
    return html

# Auto-export all PSX features
__all__ = [
    # Core
    'PSXElement', 'PSXParser', 'psx', 'render_psx', 'fragment', 'key',
    'process_python_logic', 'runtime', 'SafeExpressionEngine',
    'CLIENT_ROUTER_SCRIPT',
    'CRUD_RUNTIME_SCRIPT',
    
    # VDOM
    'VNode', 'create_element', 'render', 'update', 'get_vdom_metrics',
    
    # Renderer
    'PSXRenderer', 'renderer', 'render_psx_component',
    
    # Components
    'PSXComponent', 'component', 'Component', 'class_component', 'Props', 'Children',
    'Head', 'Link', 'Script', 'Image', 'Meta', 'Title', 'Layout', 'Container',
    'Row', 'Col', 'Form', 'Input', 'Button', 'Navbar', 'NavItem', 'Card', 'List',
    'Conditional', 'Loop', 'ErrorBoundary', 'Suspense', 'ChildrenComponent',
    'register_component', 'clsx',
    
    # React Hooks
    'useState', 'useEffect', 'useContext', 'useReducer', 'useRef',
    'useMemo', 'useCallback', 'useImperativeHandle', 'useLayoutEffect',
    'useDebugValue', 'useTransition', 'useDeferredValue', 'useId',
    
    # Custom Hooks
    'useCounter', 'useToggle', 'useLocalStorage', 'useFetch', 'useAction', 'useCrudEvent', 'useDebounce',
    'useInterval', 'usePrevious', 'useAsync', 'useMediaQuery', 'useGeolocation', 'usePerformance',
    
    # Event Handlers
    'create_onclick', 'create_ondblclick', 'create_onmousedown', 'create_onmouseup',
    'create_onmouseover', 'create_onmouseout', 'create_onmouseenter', 'create_onmouseleave', 'create_onmousemove',
    'create_onchange', 'create_onsubmit', 'create_onreset', 'create_onfocus', 'create_onblur',
    'create_oninput', 'create_oninvalid', 'create_onselect',
    'create_onkeydown', 'create_onkeyup', 'create_onkeypress',
    'create_ontouchstart', 'create_ontouchend', 'create_ontouchmove', 'create_ontouchcancel',
    'create_onload', 'create_onunload', 'create_onresize', 'create_onscroll',
    'create_ondrag', 'create_ondragstart', 'create_ondragend', 'create_ondragenter',
    'create_ondragleave', 'create_ondragover', 'create_ondrop',
    'create_onplay', 'create_onpause', 'create_onended', 'create_onvolumechange',
    'create_ontimeupdate', 'create_onseeking', 'create_onseeked',
    'create_onloadstart', 'create_onprogress', 'create_onerror', 'create_onabort',
    'create_onanimationstart', 'create_onanimationend', 'create_onanimationiteration',
    'create_ontransitionend', 'create_ontransitionrun', 'create_ontransitionstart',
    'create_onwheel', 'create_oncopy', 'create_oncut', 'create_onpaste',
    'create_onbeforeprint', 'create_onafterprint', 'create_onstorage',
    'create_onopen', 'create_onmessage', 'create_onclose', 'create_oninstall', 'create_onactivate',
    
    # Utils
    'compile_psx', 'compile_psx_file', 'is_psx_file', 'PSXCompiler',
    
    # Hydration Engine
    'HydrationEngine', 'get_hydration_engine',
    'interactive_component', 'enable_hydration_globally', 'create_interactive_page',
    'hydrate_component', 'get_component_hydrator',
    
    # Enhanced Full-Stack Runtime
    'ENHANCED_CLIENT_RUNTIME_SCRIPT',
]
