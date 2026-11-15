/**
 * NextPy Enhanced Client Runtime
 * Provides seamless client-server communication for full-stack applications
 */

(function() {
    'use strict';

    if (window.__nextpyEnhancedRuntime) return;
    window.__nextpyEnhancedRuntime = true;

    class NextPyClient {
        constructor() {
            this.serverActions = new Map();
            this.stateSubscriptions = new Map();
            this.websocket = null;
            this.reconnectAttempts = 0;
            this.maxReconnectAttempts = 5;
            this.reconnectDelay = 2000;
            this.pendingRequests = new Map();
            this.requestId = 0;
        }

        /**
         * Execute a server action from client-side code
         */
        async executeServerAction(actionName, params = {}) {
            const requestId = ++this.requestId;
            
            try {
                const response = await fetch('/__nextpy/actions/execute', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({
                        action: actionName,
                        params: params
                    })
                });

                if (!response.ok) {
                    throw new Error(`Server action failed: ${response.status}`);
                }

                const result = await response.json();
                
                if (result.success) {
                    return result.data;
                } else {
                    throw new Error(result.error?.message || 'Server action failed');
                }
            } catch (error) {
                console.error(`[NextPy] Server action '${actionName}' failed:`, error);
                throw error;
            }
        }

        /**
         * List all available server actions
         */
        async listServerActions() {
            try {
                const response = await fetch('/__nextpy/actions', {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json'
                    }
                });

                if (!response.ok) {
                    throw new Error(`Failed to list actions: ${response.status}`);
                }

                const result = await response.json();
                return result.actions || {};
            } catch (error) {
                console.error('[NextPy] Failed to list server actions:', error);
                return {};
            }
        }

        /**
         * Get server action schema
         */
        async getActionSchema(actionName) {
            try {
                const response = await fetch(`/__nextpy/actions/${actionName}/schema`, {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json'
                    }
                });

                if (!response.ok) {
                    throw new Error(`Failed to get schema: ${response.status}`);
                }

                return await response.json();
            } catch (error) {
                console.error(`[NextPy] Failed to get schema for '${actionName}':`, error);
                return null;
            }
        }

        /**
         * Connect to WebSocket for real-time updates
         */
        connectWebSocket() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/ws`;

            try {
                this.websocket = new WebSocket(wsUrl);

                this.websocket.onopen = () => {
                    console.log('[NextPy] WebSocket connected');
                    this.reconnectAttempts = 0;
                    this.dispatchEvent('websocket:connected');
                };

                this.websocket.onmessage = (event) => {
                    try {
                        const message = JSON.parse(event.data);
                        this.handleWebSocketMessage(message);
                    } catch (error) {
                        console.error('[NextPy] Failed to parse WebSocket message:', error);
                    }
                };

                this.websocket.onclose = () => {
                    console.log('[NextPy] WebSocket disconnected');
                    this.dispatchEvent('websocket:disconnected');
                    this.attemptReconnect();
                };

                this.websocket.onerror = (error) => {
                    console.error('[NextPy] WebSocket error:', error);
                    this.dispatchEvent('websocket:error', error);
                };

            } catch (error) {
                console.error('[NextPy] Failed to create WebSocket connection:', error);
                this.attemptReconnect();
            }
        }

        /**
         * Attempt to reconnect WebSocket
         */
        attemptReconnect() {
            if (this.reconnectAttempts >= this.maxReconnectAttempts) {
                console.error('[NextPy] Max reconnection attempts reached');
                return;
            }

            this.reconnectAttempts++;
            const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);

            console.log(`[NextPy] Attempting to reconnect in ${delay}ms...`);
            setTimeout(() => this.connectWebSocket(), delay);
        }

        /**
         * Handle WebSocket messages
         */
        handleWebSocketMessage(message) {
            switch (message.type) {
                case 'STATE_CHANGE':
                    this.handleStateChange(message);
                    break;
                case 'TODO_CHANGED':
                    this.handleTodoChange(message);
                    break;
                default:
                    console.log('[NextPy] Unknown WebSocket message type:', message.type);
            }
        }

        /**
         * Handle state change messages
         */
        handleStateChange(message) {
            const { key, old_value, new_value, timestamp, version } = message;
            
            // Update local state cache
            this.stateCache = this.stateCache || {};
            this.stateCache[key] = new_value;

            // Notify subscribers
            const subscribers = this.stateSubscriptions.get(key) || [];
            subscribers.forEach(callback => {
                try {
                    callback(new_value, old_value, message);
                } catch (error) {
                    console.error(`[NextPy] State subscription callback failed for '${key}':`, error);
                }
            });

            this.dispatchEvent('state:changed', { key, old_value, new_value, timestamp, version });
        }

        /**
         * Handle todo change messages (for backwards compatibility)
         */
        handleTodoChange(message) {
            this.dispatchEvent('todo:changed', message);
        }

        /**
         * Subscribe to state changes
         */
        subscribeToState(key, callback) {
            if (!this.stateSubscriptions.has(key)) {
                this.stateSubscriptions.set(key, new Set());
            }
            
            this.stateSubscriptions.get(key).add(callback);

            // Return unsubscribe function
            return () => {
                const subscribers = this.stateSubscriptions.get(key);
                if (subscribers) {
                    subscribers.delete(callback);
                    if (subscribers.size === 0) {
                        this.stateSubscriptions.delete(key);
                    }
                }
            };
        }

        /**
         * Dispatch custom event
         */
        dispatchEvent(eventName, detail = {}) {
            const event = new CustomEvent(`nextpy:${eventName}`, { detail });
            window.dispatchEvent(event);
        }

        /**
         * Form validation helper
         */
        validateForm(formData, schema) {
            const errors = {};

            for (const [fieldName, fieldConfig] of Object.entries(schema)) {
                const value = formData[fieldName];

                // Required validation
                if (fieldConfig.required && (!value || value.trim() === '')) {
                    errors[fieldName] = `${fieldName} is required`;
                    continue;
                }

                // Type validation
                if (value && fieldConfig.type) {
                    switch (fieldConfig.type) {
                        case 'email':
                            if (!this.isValidEmail(value)) {
                                errors[fieldName] = `${fieldName} must be a valid email`;
                            }
                            break;
                        case 'number':
                            if (isNaN(Number(value))) {
                                errors[fieldName] = `${fieldName} must be a number`;
                            }
                            break;
                    }
                }

                // Custom validation
                if (value && fieldConfig.validator) {
                    const validationResult = fieldConfig.validator(value);
                    if (validationResult !== true) {
                        errors[fieldName] = validationResult || `${fieldName} is invalid`;
                    }
                }
            }

            return {
                isValid: Object.keys(errors).length === 0,
                errors
            };
        }

        /**
         * Email validation helper
         */
        isValidEmail(email) {
            const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return pattern.test(email);
        }

        /**
         * Debounce function
         */
        debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        }

        /**
         * Throttle function
         */
        throttle(func, limit) {
            let inThrottle;
            return function executedFunction(...args) {
                if (!inThrottle) {
                    func.apply(this, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            };
        }

        /**
         * Local storage helper with state sync
         */
        storage = {
            get(key, defaultValue = null) {
                try {
                    const item = localStorage.getItem(key);
                    return item ? JSON.parse(item) : defaultValue;
                } catch (error) {
                    console.error(`[NextPy] Failed to get from localStorage:`, error);
                    return defaultValue;
                }
            },

            set(key, value) {
                try {
                    localStorage.setItem(key, JSON.stringify(value));
                    window.dispatchEvent(new CustomEvent('nextpy:storage:changed', { 
                        detail: { key, value } 
                    }));
                } catch (error) {
                    console.error(`[NextPy] Failed to set localStorage:`, error);
                }
            },

            remove(key) {
                try {
                    localStorage.removeItem(key);
                    window.dispatchEvent(new CustomEvent('nextpy:storage:changed', { 
                        detail: { key, value: null } 
                    }));
                } catch (error) {
                    console.error(`[NextPy] Failed to remove from localStorage:`, error);
                }
            }
        };
    }

    // ── PSX hooks shim ──────────────────────────────────────────────────────
    // PSX components are server-rendered in Python; the hydration runtime only
    // patches DOM bindings and never re-invokes component functions, so these
    // hooks have no call site during normal rendering. They are exposed for
    // parity with the Python implementations (nextpy.psx.components.component)
    // and for any client code that drives them manually.
    //
    //   useContext(ctx)          — reads window.__nextpyContextStack (Provider
    //                              pushes {context, value} frames around its
    //                              subtree render on the server; client code
    //                              may push frames the same way).
    //   useDeferredValue(value)  — returns the previous value for one tick
    //                              (microtask) after the input changes.
    //   useTransition()          — startTransition(cb) runs cb and reports
    //                              isPending until the microtask queue drains.
    //   useImperativeHandle(...) — writes the handle onto ref.current, matching
    //                              the Python useRef shape ({ current } object).
    window.__nextpyContextStack = window.__nextpyContextStack || [];
    window.__nextpyHooks = {
        useContext(context) {
            const stack = window.__nextpyContextStack;
            for (let i = stack.length - 1; i >= 0; i--) {
                const frame = stack[i];
                if (frame.context === context || frame.context == context) {
                    return frame.value;
                }
            }
            return context && context.default_value !== undefined
                ? context.default_value
                : context && context.defaultValue !== undefined
                    ? context.defaultValue
                    : undefined;
        },

        useDeferredValue(value) {
            const state = window.__nextpyDeferredState ||
                (window.__nextpyDeferredState = { current: value });
            if (state.current === value) return state.current;
            // Return the previous value for this tick; the next call sees
            // the new value already committed.
            const previous = state.current;
            state.current = value;
            return previous;
        },

        useTransition() {
            const state = window.__nextpyTransitionState ||
                (window.__nextpyTransitionState = { pending: 0 });
            return [state.pending > 0, function startTransition(cb) {
                state.pending += 1;
                try {
                    return cb();
                } finally {
                    // Transition "completes" once the microtask queue drains.
                    queueMicrotask(() => { state.pending = Math.max(0, state.pending - 1); });
                }
            }];
        },

        useImperativeHandle(ref, createHandle, deps) {
            if (!ref) return;
            // Refs are { current } objects (same shape as useRef); fall back to
            // a plain property assignment for dict-like refs.
            try {
                ref.current = createHandle();
            } catch (e) {
                ref['current'] = createHandle();
            }
        },

        useRef(initialValue) {
            return { current: initialValue };
        }
    };

    // Initialize the client
    const nextpyClient = new NextPyClient();
    
    // Make it available globally
    window.nextpy = window.nextpy || {};
    window.nextpy.client = nextpyClient;

    // Auto-connect WebSocket
    if (window.location.protocol !== 'file:') {
        nextpyClient.connectWebSocket();
    }

    // Expose convenience functions
    window.nextpy.executeAction = nextpyClient.executeServerAction.bind(nextpyClient);
    window.nextpy.listActions = nextpyClient.listServerActions.bind(nextpyClient);
    window.nextpy.subscribe = nextpyClient.subscribeToState.bind(nextpyClient);
    window.nextpy.storage = nextpyClient.storage;
    window.nextpy.validate = nextpyClient.validateForm.bind(nextpyClient);
    window.nextpy.debounce = nextpyClient.debounce.bind(nextpyClient);
    window.nextpy.throttle = nextpyClient.throttle.bind(nextpyClient);

    console.log('[NextPy] Enhanced client runtime initialized');

})();