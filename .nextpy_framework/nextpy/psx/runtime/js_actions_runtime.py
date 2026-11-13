"""
NextPy PSX JavaScript Runtime - Structured Action Execution
Replaces JS string evaluation with structured action processing
"""

# JavaScript runtime script as a constant
JS_ACTION_RUNTIME_SCRIPT = r"""
(function() {
if (window.__nextpyActionRuntimeLoaded) return;
window.__nextpyActionRuntimeLoaded = true;
/**
 * NextPy PSX JavaScript Runtime - Structured Action Execution
 * Replacing JS string evaluation with structured action processing
 */

/**
 * PSXSignal - fine-grained reactive primitive (SolidJS-style pub/sub).
 * Tracks active subscribers so computed effects re-run only when a
 * signal they actually read changes.
 */
class PSXSignal {
    constructor(value) {
        this._value = value;
        this._subs = new Set();
    }

    get() {
        // Register dependency when read inside an effect/computed.
        if (PSXSignal._active) {
            PSXSignal._active.add(this);
        }
        return this._value;
    }

    set(newValue) {
        if (Object.is(this._value, newValue)) return;
        const oldValue = this._value;
        this._value = newValue;
        // Snapshot: subscribers may unsubscribe or subscribe during notify.
        Array.from(this._subs).forEach(fn => {
            try { fn(newValue, oldValue); }
            catch (error) { console.error('[NextPy] Signal subscriber error:', error); }
        });
    }

    subscribe(fn) {
        this._subs.add(fn);
        return () => this._subs.delete(fn);
    }
}
PSXSignal._active = null;

/**
 * psxEffect - run fn, tracking every signal read, and re-run only when
 * one of those signals changes. Returns a dispose function.
 */
function psxEffect(fn) {
    let deps = new Set();
    let unsubscribers = [];
    const subscribeAll = () => {
        unsubscribers.forEach(u => u());
        unsubscribers = [];
        deps.forEach(sig => unsubscribers.push(sig.subscribe(run)));
    };
    const run = () => {
        deps = new Set();
        PSXSignal._active = deps;
        try { fn(); }
        finally { PSXSignal._active = null; }
        subscribeAll();
    };
    run();
    return () => unsubscribers.forEach(u => u());
}

class NextPyActionRuntime {
    constructor() {
        this.components = new Map();
        this.globalState = {};
        this.functions = new Map();
        this.dependencyMap = new Map(); // FIX: Track state dependencies
        this._effectsRunning = new Set();
        // Fine-grained reactivity state
        this.signals = new Map();          // componentId -> Map(key -> PSXSignal)
        this._dirtyComponents = new Map(); // componentId -> Set(changedKeys)
        this._rafScheduled = false;
        this._domTasks = new Map();        // id -> fn, flushed once per frame
        this.refs = new Map();             // componentId -> Map(refName -> element)
        this._oldValues = new Map();       // componentId -> Map(key -> oldValue)
        this._flipElements = new Set();    // elements with layout:true motion config
        this._registerBuiltinFunctions();
    }

    registerComponent(componentId, initialState = {}) {
        this.components.set(componentId, {
            state: { ...initialState },
            listeners: [],
            functions: new Map()
        });
        this.dependencyMap.set(componentId, {}); // FIX: Initialize dependency map for component
        this._ensureStateDefaults(componentId);
        // FIX: Build dependency map for conditional elements (deferred to after DOM is ready)
        setTimeout(() => this._buildDependencyMap(componentId), 100); // Delay to ensure DOM is ready
        return this.components.get(componentId);
    }

    _buildDependencyMap(componentId) {
        // FIX: Scan DOM and build dependency map for conditional elements
        const conditionalElements = document.querySelectorAll(`[data-if-condition]`);
        // FIX: Initialize dependency map for component if not exists
        if (!this.dependencyMap.has(componentId)) {
            this.dependencyMap.set(componentId, {});
        }
        
        conditionalElements.forEach(element => {
            if (element.dataset.componentId === componentId) {
                this._registerConditionalElement(element, componentId);
            }
        });
        // FIX: Set up input bindings for elements with data-bind attribute
        this._setupInputBindings(componentId);
        // Collect data-psx-ref element references for useRef support.
        this._collectRefs(componentId);
        // Apply SSR-reactive class/style/attribute bindings on mount.
        this._applyAttributeBindings(null, componentId);
        // Run useEffect callbacks on mount (once per component).
        this._runEffects(componentId, null, true);
    }
    
    _setupInputBindings(componentId) {
        // FIX: Set up automatic input bindings for elements with data-bind attribute
        const boundElements = document.querySelectorAll(`[data-bind]`);
        boundElements.forEach(element => {
            const bindSpec = element.dataset.bind;
            if (!bindSpec) return;
            
            // Parse bind specification: "value:name" or "checked:name"
            const [bindType, stateKey] = bindSpec.split(':');
            // Determine the appropriate event based on element type
            let eventType = 'input';
            if (element.tagName === 'SELECT' || element.type === 'checkbox' || element.type === 'radio') {
                eventType = 'change';
            }
            
            // Add event listener to update state when input changes
            element.addEventListener(eventType, (e) => {
                const component = this.components.get(componentId);
                if (!component) return;
                
                let newValue;
                if (bindType === 'value') {
                    newValue = e.target.value;
                } else if (bindType === 'checked') {
                    newValue = e.target.checked;
                } else {
                    newValue = e.target.value;
                }
                
                this._executeSetState(componentId, stateKey, newValue);
            });
            
            // Set initial value from state
            const component = this.components.get(componentId);
            if (component && component.state[stateKey] !== undefined) {
                if (bindType === 'value') {
                    element.value = component.state[stateKey];
                } else if (bindType === 'checked') {
                    element.checked = component.state[stateKey];
                }
            }
            
            // Listen for state changes to update input value
            this._addStateListener(componentId, stateKey, (newValue) => {
                if (bindType === 'value') {
                    element.value = newValue;
                } else if (bindType === 'checked') {
                    element.checked = newValue;
                }
            });
        });
    }
    
    _addStateListener(componentId, stateKey, callback) {
        // FIX: Add a listener for state changes
        const component = this.components.get(componentId);
        if (!component) return;
        
        component.listeners.push({ stateKey, callback });
    }

    // FIX: Public method to rebuild dependency map after DOM is ready
    rebuildDependencyMap(componentId) {
        this.dependencyMap.set(componentId, {});
        this._buildDependencyMap(componentId);
    }

    _ensureStateDefaults(componentId) {
        if (!this.components.has(componentId)) return;
        const state = this.components.get(componentId).state;
        for (const key of Object.keys(state)) {
            if (!(key in state)) state[key] = null;
        }
    }

    executeAction(action, componentId = null) {
        const { type, data } = action;

        try {
            switch (type) {
                case 'SET_STATE':
                    return this._executeSetState(data, componentId);
                case 'SET_STATE_BATCH':
                    return this._executeSetStateBatch(data, componentId);
                case 'GET_STATE':
                    return this._executeGetState(data, componentId);
                case 'CALL_FUNCTION':
                    return this._executeCallFunction(data, componentId);
                case 'CALL_METHOD':
                    return this._executeCallMethod(data, componentId);
                case 'BINARY_OP':
                    return this._executeBinaryOp(data, componentId);
                case 'UNARY_OP':
                    return this._executeUnaryOp(data, componentId);
                case 'COMPARE_OP':
                    return this._executeCompareOp(data, componentId);
                case 'BOOLEAN_OP':
                    return this._executeBooleanOp(data, componentId);
                case 'PRINT':
                    return this._executePrint(data, componentId);
                case 'CONSTANT':
                    return this._executeConstant(data);
                case 'VARIABLE':
                    return this._executeVariable(data, componentId);
                case 'LIST':
                    return this._executeList(data, componentId);
                case 'DICT':
                    return this._executeDict(data, componentId);
                case 'INDEX':
                    return this._executeIndex(data, componentId);
                case 'ATTRIBUTE':
                    return this._executeAttribute(data, componentId);
                case 'FOR_LOOP':
                    return this._executeForLoop(data, componentId);
                case 'WHILE_LOOP':
                    return this._executeWhileLoop(data, componentId);
                case 'BREAK':
                    return this._executeBreak();
                case 'CONTINUE':
                    return this._executeContinue();
                case 'TRY':
                    return this._executeTry(data, componentId);
                case 'RETURN':
                    return this._executeReturn(data);
                case 'LAMBDA':
                    return this._executeLambda(data);
                case 'JSX_UPDATE':
                    return this._executeJsxUpdate(data, componentId);
                case 'FETCH_DATA':
                    return this._executeFetchData(data, componentId);
                case 'SUBSCRIBE_CRUD_EVENT':
                    return this._executeSubscribeCrudEvent(data, componentId);
                case 'CALL_SERVER_ACTION':
                    return this._executeCallServerAction(data, componentId);
                case 'IF':
                    return this._executeIf(data, componentId);
                case 'NAVIGATE':
                    return this._executeNavigate(data, componentId);
                case 'CONDITIONAL':
                    return this._executeConditional(data, componentId);
                case 'DEFINE_FUNCTION':
                    return this._executeDefineFunction(data, componentId);
                default:
                    console.warn(`Unknown action type: ${type}`);
                    return null;
            }
        } catch (error) {
            // Swallow RETURN sentinel from nested function returns; it's only
            // for unwinding control flow, not a real error.
            if (error && error.type === 'RETURN') {
                return error.value;
            }
            console.error(`Action execution error:`, error);
            if (window.NEXTPY_DEBUG) throw error;
            return null;
        }
    }

    async executeActions(actions, componentId = null) {
        const results = [];
        // Expose the active component id so compiled code can reach
        // per-component client APIs (window.nextpy.getRef, .signal, ...).
        const _np = window.nextpy;
        const _prevCid = _np ? _np._componentId : undefined;
        if (_np) _np._componentId = componentId;
        try {
            for (const action of actions) {
                const result = await this.executeAction(action, componentId);
                results.push(result);
            }
        } catch (error) {
            // Swallow RETURN sentinel from nested function returns; it's only
            // for unwinding control flow, not a real error.
            if (error && error.type === 'RETURN') {
                return error.value;
            }
            throw error;
        } finally {
            if (_np) _np._componentId = _prevCid;
        }
        return results;
    }

    _executeSetState(data, componentId) {
        const { key, value } = data;
        const evaluatedValue = this._evaluateExpression(value, componentId);

        // FIX: Require componentId to prevent state contamination
        if (!componentId || !this.components.has(componentId)) {
            console.warn('SET_STATE: componentId required or component not found:', componentId);
            return;
        }

        const component = this.components.get(componentId);
        const oldValue = component.state[key];
        component.state[key] = evaluatedValue;

        // FIX: Call state listeners for this key
        component.listeners.forEach(listener => {
            if (listener.stateKey === key) {
                listener.callback(evaluatedValue);
            }
        });

        // Trigger re-render if DOM element exists
        this._triggerComponentUpdate(componentId, key, evaluatedValue, oldValue);
    }

    _executeSetStateBatch(data, componentId) {
        const { updates } = data;

        // FIX: Require componentId to prevent state contamination
        if (!componentId || !this.components.has(componentId)) {
            console.warn('SET_STATE_BATCH: componentId required or component not found:', componentId);
            return;
        }

        const component = this.components.get(componentId);
        for (const update of updates) {
            const { key, value } = update;
            const evaluatedValue = this._evaluateExpression(value, componentId);
            const oldValue = component.state[key];
            component.state[key] = evaluatedValue;
            this._triggerComponentUpdate(componentId, key, evaluatedValue, oldValue);
        }
    }

    _executeConditional(data, componentId) {
        const { condition, then: thenValue, else: elseValue } = data;
        const result = this._evaluateExpression(condition, componentId);
        return this._evaluateExpression(result ? thenValue : elseValue, componentId);
    }

    _executeGetState(data, componentId) {
        const { key } = data;
        
        // FIX: Require componentId to prevent state contamination
        if (!componentId || !this.components.has(componentId)) {
            console.warn('GET_STATE: componentId required or component not found:', componentId);
            return undefined;
        }
        
        return this.components.get(componentId).state[key];
    }

    _executeCallFunction(data, componentId) {
        const { function: funcName, args = [], kwargs = {} } = data;
        const evaluatedArgs = args.map(arg => this._evaluateExpression(arg, componentId));
        const evaluatedKwargs = {};

        for (const [key, value] of Object.entries(kwargs)) {
            evaluatedKwargs[key] = this._evaluateExpression(value, componentId);
        }

        const component = componentId ? this.components.get(componentId) : null;
        if (component && component.functions && component.functions.has(funcName)) {
            const func = component.functions.get(funcName);
            try {
                return func(...evaluatedArgs, evaluatedKwargs || {});
            } catch (e) {
                if (e && e.type === 'RETURN') return e.value;
                throw e;
            }
        } else if (this.functions.has(funcName)) {
            const func = this.functions.get(funcName);
            return func(...evaluatedArgs, evaluatedKwargs || {});
        } else if (typeof window[funcName] === 'function') {
            return window[funcName](...evaluatedArgs);
        } else {
            throw new Error(`Unknown function: ${funcName}`);
        }
    }

    _executeCallMethod(data, componentId) {
        const { object, method, args = [], kwargs = {} } = data;
        const evaluatedArgs = args.map(arg => this._evaluateExpression(arg, componentId));
        const evaluatedKwargs = {};

        for (const [key, value] of Object.entries(kwargs)) {
            evaluatedKwargs[key] = this._evaluateExpression(value, componentId);
        }

        if (!componentId || !this.components.has(componentId)) {
            console.warn('CALL_METHOD: componentId required or component not found:', componentId);
            throw new Error(`Cannot call method without component context`);
        }

        const component = this.components.get(componentId);
        let obj = component.state[object];

        // Handle global objects (window, document, etc.)
        if (obj === undefined || obj === null) {
            if (object === 'window' && typeof window !== 'undefined') {
                obj = window;
            } else if (object === 'document' && typeof document !== 'undefined') {
                obj = document;
            } else if (object === 'console' && typeof console !== 'undefined') {
                obj = console;
            } else if (object === 'localStorage' && typeof localStorage !== 'undefined') {
                obj = localStorage;
            } else if (object === 'Math' && typeof Math !== 'undefined') {
                obj = Math;
            } else if ((object === 'nextpy' || object === 'window.nextpy') && window.nextpy) {
                obj = window.nextpy;
            } else {
                console.warn(`Object '${object}' is undefined or null, returning empty string`);
                return "";
            }
        }

        // Handle Python dict.get() as bracket notation
        if (method === 'get' && typeof obj === 'object' && !Array.isArray(obj)) {
            const key = evaluatedArgs[0];
            const defaultVal = evaluatedArgs.length > 1 ? evaluatedArgs[1] : undefined;
            if (key in obj) return obj[key];
            return defaultVal !== undefined ? defaultVal : "";
        }

        // Handle Python dict.keys(), dict.values(), dict.items()
        if (typeof obj === 'object' && !Array.isArray(obj)) {
            if (method === 'keys') return Object.keys(obj);
            if (method === 'values') return Object.values(obj);
            if (method === 'items') return Object.entries(obj);
        }

        if (obj && typeof obj[method] === 'function') {
            return obj[method](...evaluatedArgs);
        } else {
            throw new Error(`Method '${method}' not found on object '${object}' (type: ${typeof obj})`);
        }
    }


    _executeBinaryOp(data, componentId) {
        const { left, op, right } = data;
        const leftValue = this._evaluateExpression(left, componentId);
        const rightValue = this._evaluateExpression(right, componentId);

        // Array concat when either operand is an array
        if (op === '+') {
            if (Array.isArray(leftValue) && Array.isArray(rightValue)) {
                return [...leftValue, ...rightValue];
            }
            if (Array.isArray(leftValue)) {
                return [...leftValue, rightValue];
            }
            if (Array.isArray(rightValue)) {
                return [leftValue, ...rightValue];
            }
        }

        switch (op) {
            case '+': return leftValue + rightValue;
            case '-': return leftValue - rightValue;
            case '*': return leftValue * rightValue;
            case '/': return leftValue / rightValue;
            case '%': return leftValue % rightValue;
            case '**': return leftValue ** rightValue;
            case '//': return Math.floor(leftValue / rightValue);
            case '<<': return leftValue << rightValue;
            case '>>': return leftValue >> rightValue;
            case '|': return leftValue | rightValue;
            case '^': return leftValue ^ rightValue;
            case '&': return leftValue & rightValue;
            default:
                throw new Error(`Unknown binary operator: ${op}`);
        }
    }

    _executeUnaryOp(data, componentId) {
        const { op, operand } = data;
        const operandValue = this._evaluateExpression(operand, componentId);
        
        switch (op) {
            case '+': return +operandValue;
            case '-': return -operandValue;
            case 'not':
            case '!': return !operandValue;
            case '~': return ~operandValue;
            default:
                throw new Error(`Unknown unary operator: ${op}`);
        }
    }

    _executeCompareOp(data, componentId) {
        const { left, ops, comparators } = data;
        const leftValue = this._evaluateExpression(left, componentId);
        const comparatorValues = comparators.map(c => this._evaluateExpression(c, componentId));

        let result = true;
        for (let i = 0; i < ops.length && i < comparatorValues.length; i++) {
            const op = ops[i];
            const comparator = comparatorValues[i];

            if (i === 0) {
                switch (op) {
                    case '==': result = leftValue == comparator; break;
                    case '!=': result = leftValue != comparator; break;
                    case '<': result = leftValue < comparator; break;
                    case '<=': result = leftValue <= comparator; break;
                    case '>': result = leftValue > comparator; break;
                    case '>=': result = leftValue >= comparator; break;
                    case 'is': result = leftValue === comparator; break;
                    case 'is not': result = leftValue !== comparator; break;
                    case 'in':
                        result = Array.isArray(comparator)
                            ? comparator.includes(leftValue)
                            : leftValue in comparator;
                        break;
                    case 'not in':
                        result = Array.isArray(comparator)
                            ? !comparator.includes(leftValue)
                            : !(leftValue in comparator);
                        break;
                    default:
                        throw new Error(`Unknown comparison operator: ${op}`);
                }
            } else {
                // Chain comparisons (simplified)
                const prevComparator = comparatorValues[i - 1];
                switch (op) {
                    case '<': result = result && prevComparator < comparator; break;
                    case '<=': result = result && prevComparator <= comparator; break;
                    case '>': result = result && prevComparator > comparator; break;
                    case '>=': result = result && prevComparator >= comparator; break;
                    default:
                        break;
                }
            }
        }

        return result;
    }

    _executeBooleanOp(data, componentId) {
        const { op, values } = data;
        const evaluatedValues = values.map(v => this._evaluateExpression(v, componentId));
        const trimmedOp = (op || '').trim();
        
        switch (trimmedOp) {
            case 'and': return evaluatedValues.every(v => v);
            case 'or': return evaluatedValues.some(v => v);
            case '&&': return evaluatedValues.every(v => v);
            case '||': return evaluatedValues.some(v => v);
            default:
                throw new Error(`Unknown boolean operator: '${trimmedOp}'`);
        }
    }

    _executePrint(data, componentId) {
        const { args = [] } = data;
        const evaluatedArgs = args.map(arg => this._evaluateExpression(arg, componentId));
        console.log(...evaluatedArgs);
    }

    _executeConstant(data) {
        return data.value;
    }

    _executeVariable(data, componentId) {
        const { name } = data;
        
        // FIX: Only check component state to prevent cross-component contamination
        if (!componentId || !this.components.has(componentId)) {
            console.warn('VARIABLE: componentId required or component not found:', componentId);
            throw new Error(`Unknown variable: ${name} (no component context)`);
        }
        
        const component = this.components.get(componentId);
        if (name in component.state) {
            return component.state[name];
        }

        // Registered functions (nested defs, builtins) resolve as values so
        // they can be passed as callbacks: addEventListener("scroll", OnScroll)
        if (component.functions && component.functions.has(name)) {
            return component.functions.get(name);
        }
        if (this.functions.has(name)) {
            return this.functions.get(name);
        }

        // Only allow window object access for built-in functions/constants
        if (name in window && typeof window[name] !== 'undefined') {
            return window[name];
        }
        
        throw new Error(`Unknown variable: ${name} in component ${componentId}`);
    }

    _executeList(data, componentId) {
        const { elements } = data;
        return elements.map(el => this._evaluateExpression(el, componentId));
    }

    _executeDict(data, componentId) {
        const { keys, values } = data;
        const result = {};
        
        for (let i = 0; i < keys.length && i < values.length; i++) {
            const key = this._evaluateExpression(keys[i], componentId);
            const value = this._evaluateExpression(values[i], componentId);
            result[key] = value;
        }
        
        return result;
    }

    _executeIndex(data, componentId) {
        const { value, slice } = data;
        const valueObj = this._evaluateExpression(value, componentId);
        const sliceValue = this._evaluateExpression(slice, componentId);
        
        return valueObj[sliceValue];
    }

    _executeAttribute(data, componentId) {
        const { object, attr } = data;
        const obj = this._evaluateExpression(object, componentId);
        
        return obj[attr];
    }

    async _executeFetchData(data, componentId) {
        const { url, options, dataKey, loadingKey, errorKey } = data;
        const component = this.components.get(componentId);
        if (!component) {
            console.warn('FETCH_DATA: component not found:', componentId);
            return null;
        }

        // Set loading state
        if (loadingKey) {
            component.state[loadingKey] = true;
            this._triggerComponentUpdate(componentId, loadingKey, true);
        }
        if (errorKey) {
            component.state[errorKey] = null;
            this._triggerComponentUpdate(componentId, errorKey, null);
        }

        try {
            const fetchOptions = options || {};
            const response = await fetch(url, fetchOptions);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const contentType = response.headers.get('content-type') || '';
            let result;
            if (contentType.includes('application/json')) {
                result = await response.json();
            } else {
                result = await response.text();
            }

            if (dataKey) {
                component.state[dataKey] = result;
                this._triggerComponentUpdate(componentId, dataKey, result);
            }
        } catch (err) {
            console.error('FETCH_DATA error:', err);
            if (errorKey) {
                component.state[errorKey] = err.message || String(err);
                this._triggerComponentUpdate(componentId, errorKey, err.message || String(err));
            }
        } finally {
            if (loadingKey) {
                component.state[loadingKey] = false;
                this._triggerComponentUpdate(componentId, loadingKey, false);
            }
        }
    }

    async _executeSubscribeCrudEvent(data, componentId) {
        const { eventKey, resource } = data;
        const component = this.components.get(componentId);
        if (!component) {
            console.warn('SUBSCRIBE_CRUD_EVENT: component not found:', componentId);
            return null;
        }

        const handler = (e) => {
            const detail = e.detail || {};
            if (resource && detail.config && detail.config.resource !== resource) return;

            this._executeSetState({key: eventKey, value: detail}, componentId);
        };

        window.addEventListener('nextpy:crud:changed', handler);

        const cleanupFn = () => {
            window.removeEventListener('nextpy:crud:changed', handler);
        };

        if (window.nextpyComponents && window.nextpyComponents[componentId]) {
            window.nextpyComponents[componentId].unsubscribers.push(cleanupFn);
        }

        return cleanupFn;
    }

    async _executeCallServerAction(data, componentId) {
        let actionName = data.action;
        let params = data.params || {};
        const loadingKey = data.loadingKey || '_server_loading';
        const dataKey = data.dataKey || '_server_result';
        const errorKey = data.errorKey || '_server_error';

        // Resolve action name if it's a dynamic value
        if (actionName && typeof actionName === 'object' && actionName.type) {
            actionName = this._evaluateExpression(actionName, componentId);
        }
        if (params && typeof params === 'object' && params.type) {
            params = this._evaluateExpression(params, componentId);
        }

        const component = componentId ? this.components.get(componentId) : null;

        // Store loading state
        if (component) {
            component.state[loadingKey] = true;
            component.state[errorKey] = null;
            this._triggerComponentUpdate(componentId, loadingKey, true);
        }

        try {
            const response = await fetch('/__nextpy/actions/execute', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                body: JSON.stringify({ action: actionName, params: params }),
            });

            const responseData = await response.json();

            // ServerAction.execute wraps every action result as
            // {success, data, timestamp}. Handlers expect the action's own
            // result ({success, error, user, ...}), so unwrap it; otherwise
            // failed actions look successful and clients redirect anyway.
            const result = (
                responseData &&
                responseData.success === true &&
                Object.prototype.hasOwnProperty.call(responseData, 'data') &&
                Object.prototype.hasOwnProperty.call(responseData, 'timestamp')
            ) ? responseData.data : responseData;

            if (!response.ok) {
                const message = (responseData && (responseData.error || responseData.detail)) || `HTTP ${response.status}`;
                if (component) {
                    component.state[loadingKey] = false;
                    component.state[errorKey] = message;
                    this._triggerComponentUpdate(componentId, loadingKey, false);
                    this._triggerComponentUpdate(componentId, errorKey, message);
                }
                return { success: false, error: message };
            }

            if (component) {
                component.state[loadingKey] = false;
                component.state[dataKey] = result;
                this._triggerComponentUpdate(componentId, loadingKey, false);
                this._triggerComponentUpdate(componentId, dataKey, result);
            }

            return result;
        } catch (err) {
            console.error('CALL_SERVER_ACTION error:', err);
            if (component) {
                component.state[loadingKey] = false;
                component.state[errorKey] = err.message || String(err);
                this._triggerComponentUpdate(componentId, loadingKey, false);
                this._triggerComponentUpdate(componentId, errorKey, err.message || String(err));
            }
            return { success: false, error: err.message || String(err) };
        }
    }

    async _executeIf(data, componentId) {
        const { condition, then: thenActions, else: elseActions } = data;
        const result = this._evaluateExpression(condition, componentId);

        if (result) {
            if (thenActions && thenActions.length > 0) {
                await this.executeActions(thenActions, componentId);
            }
        } else {
            if (elseActions && elseActions.length > 0) {
                await this.executeActions(elseActions, componentId);
            }
        }
        return null;
    }

    _executeNavigate(data, componentId) {
        const { url } = data;
        const resolvedUrl = typeof url === 'object' ? this._evaluateExpression(url, componentId) : url;
        if (window.__nextpyNavigate) {
            window.__nextpyNavigate(resolvedUrl);
        } else {
            window.location.href = resolvedUrl;
        }
    }

    _evaluateExpression(expr, componentId = null) {
        if (expr === null || expr === undefined) {
            return null;
        } else if (typeof expr === 'object' && expr.type) {
            return this.executeAction(expr, componentId);
        } else {
            return expr;
        }
    }

    _triggerComponentUpdate(componentId, key, newValue, oldValue) {
        // Sync to hydration component's StateManager to trigger DOM data-bind updates.
        // Guard the bridge so StateManager.set does not call back into this method
        // and run conditionals/effects a second time.
        if (window.nextpyComponents && window.nextpyComponents[componentId]) {
            const hydComp = window.nextpyComponents[componentId];
            if (hydComp.stateManager && hydComp.stateManager.state[key] !== newValue) {
                this._hydrationSyncDepth = (this._hydrationSyncDepth || 0) + 1;
                try {
                    hydComp.stateManager.set(key, newValue);
                } finally {
                    this._hydrationSyncDepth = Math.max(0, (this._hydrationSyncDepth || 1) - 1);
                }
            }
        }

        // Notify the per-key fine-grained signal so user effects subscribed
        // via window.nextpy.effect / createSignal re-run immediately.
        const sig = this._signalFor(componentId, key);
        sig.set(newValue);

        // Mark the component dirty and batch all DOM work into the next
        // animation frame. High-frequency events (scroll, mousemove, input)
        // coalesce into a single flush per frame — no layout thrash.
        let dirty = this._dirtyComponents.get(componentId);
        if (!dirty) {
            dirty = new Set();
            this._dirtyComponents.set(componentId, dirty);
        }
        dirty.add(key);
        let olds = this._oldValues.get(componentId);
        if (!olds) {
            olds = new Map();
            this._oldValues.set(componentId, olds);
        }
        if (!olds.has(key)) olds.set(key, oldValue);
        this._scheduleFrame();
    }

    /**
     * Lazily create (or fetch) the fine-grained signal for a state key.
     * Signals are synced from component.state at creation time.
     */
    _signalFor(componentId, key) {
        let compSignals = this.signals.get(componentId);
        if (!compSignals) {
            compSignals = new Map();
            this.signals.set(componentId, compSignals);
        }
        let sig = compSignals.get(key);
        if (!sig) {
            const component = this.components.get(componentId);
            sig = new PSXSignal(component ? component.state[key] : undefined);
            compSignals.set(key, sig);
        }
        return sig;
    }

    /**
     * Schedule a one-shot DOM task (e.g. hydration StateManager binding
     * refresh) to run once per animation frame. Tasks are keyed so repeated
     * scheduling within the same frame dedupes.
     */
    scheduleDomTask(id, fn) {
        this._domTasks.set(id, fn);
        this._scheduleFrame();
    }

    /**
     * Coalesce all pending DOM mutations into a single requestAnimationFrame.
     * Falls back to setTimeout when rAF is unavailable or the tab is hidden
     * (rAF stalls in background tabs).
     */
    _scheduleFrame() {
        if (this._rafScheduled) return;
        this._rafScheduled = true;
        const flush = () => {
            this._rafScheduled = false;
            this._flushDirty();
        };
        const hidden = typeof document !== 'undefined' && document.hidden;
        if (typeof requestAnimationFrame === 'function' && !hidden) {
            requestAnimationFrame(flush);
        } else {
            setTimeout(flush, hidden ? 16 : 0);
        }
        // Safety net: if rAF stalls (e.g., headless Chrome throttling), force flush after 100ms.
        if (!this._rafFallback) {
            this._rafFallback = setTimeout(() => {
                if (this._rafScheduled) {
                    this._rafScheduled = false;
                    this._flushDirty();
                }
            }, 100);
        }
    }

    /**
     * Synchronously flush all pending DOM updates. Useful for tests and
     * for code paths that must observe DOM changes immediately.
     */
    flush() {
        if (this._rafScheduled) {
            // Can't cancel a queued rAF portably; _flushDirty is idempotent
            // because dirty sets are cleared on flush.
        }
        this._flushDirty();
    }

    _flushDirty() {
        // FLIP: snapshot layout-animated elements before any DOM mutation so
        // we can invert their position deltas afterwards.
        const flipSnap = this._flipElements.size ? this._snapshotFlip() : null;

        // Clear the rAF fallback timer when flush runs.
        if (this._rafFallback) {
            clearTimeout(this._rafFallback);
            this._rafFallback = null;
        }

        // Run ad-hoc DOM tasks first (hydration binding refreshes, etc.)
        if (this._domTasks.size) {
            const tasks = Array.from(this._domTasks.values());
            this._domTasks.clear();
            tasks.forEach(fn => {
                try { fn(); } catch (e) { console.error('[NextPy] DOM task error:', e); }
            });
        }
        if (!this._dirtyComponents.size) return;
        const dirty = new Map(this._dirtyComponents);
        this._dirtyComponents.clear();
        dirty.forEach((keys, componentId) => {
            try {
                this._flushComponent(componentId, keys);
            } catch (error) {
                console.error('Component update flush error:', error);
            }
        });

        if (flipSnap) this._playFlip(flipSnap);
    }

    /**
     * Apply all pending DOM mutations for one component.
     * Only elements whose expressions reference a changed key are
     * re-evaluated — the fine-grained equivalent of React's targeted
     * re-render, without a VDOM diff.
     */
    _flushComponent(componentId, changedKeys) {
        const component = this.components.get(componentId);
        if (!component) return;

        // Derive variables once per flush and diff against the previous
        // snapshot so changes to derived names (user, is_employer, ...)
        // also trigger dependent conditionals/bindings.
        const derived = this._deriveVariables(component.state, componentId);
        const prevDerived = component._lastDerived || {};
        const allChanged = new Set(changedKeys);
        for (const [k, v] of Object.entries(derived)) {
            if (!(k in prevDerived) || !Object.is(prevDerived[k], v)) {
                allChanged.add(k);
            }
        }
        component._lastDerived = derived;

        // Conditional elements: only re-evaluate those whose condition
        // references a changed key (or whose deps can't be determined).
        const allConditionals = document.querySelectorAll(`[data-if-condition]`);
        allConditionals.forEach(element => {
            const isOwner = element.dataset.componentId === componentId;
            const isLayout = !element.dataset.componentId && component;
            if (!isOwner && !isLayout) return;
            if (!this._elementDependsOn(element, element.dataset.ifCondition, allChanged)) {
                return;
            }
            const condition = element.dataset.ifCondition;
            if (condition) {
                this._updateConditionalElement(element, componentId, condition);
            }
        });

        // Reactive class/style/attribute bindings — targeted per element.
        this._applyAttributeBindingsForKeys(component, componentId, allChanged);

        // Legacy data-state-* text bindings for changed keys only.
        changedKeys.forEach(key => {
            const elements = document.querySelectorAll(`[data-state-${key}]`);
            elements.forEach(element => {
                if (element.dataset.componentId === componentId || !element.dataset.componentId) {
                    const value = component.state[key];
                    const text = (value === null || value === undefined) ? '' : String(value);
                    element.textContent = text;
                    if (element.hasAttribute('data-state-toggle')) {
                        element.style.display = text ? '' : 'none';
                    }
                }
            });
        });

        // useEffect callbacks whose deps contain any changed key.
        allChanged.forEach(key => this._runEffects(componentId, key));

        // Custom event per changed state key.
        const olds = this._oldValues.get(componentId);
        changedKeys.forEach(key => {
            const event = new CustomEvent('nextpy:stateChange', {
                detail: {
                    componentId, key,
                    newValue: component.state[key],
                    oldValue: olds ? olds.get(key) : undefined
                }
            });
            document.dispatchEvent(event);
        });
        if (olds) changedKeys.forEach(key => olds.delete(key));
    }

    /**
     * Extract identifier tokens from an expression/template once and cache
     * them per-expression on the element. Returns true when the element's
     * expression references any name in changedKeys — elements with no
     * identifiable deps are always considered dependent (conservative
     * correctness for conditions the extractor can't parse).
     */
    _elementDependsOn(element, expr, changedKeys) {
        if (!expr) return true;
        const exprStr = String(expr);
        if (!element._psxDepCache) element._psxDepCache = new Map();
        let ids = element._psxDepCache.get(exprStr);
        if (!ids) {
            ids = new Set();
            const idRe = /[A-Za-z_][A-Za-z0-9_]*/g;
            let m;
            while ((m = idRe.exec(exprStr)) !== null) {
                ids.add(m[0]);
            }
            element._psxDepCache.set(exprStr, ids);
        }
        if (ids.size === 0) return true;
        for (const id of ids) {
            if (changedKeys.has(id)) return true;
        }
        return false;
    }

    /**
     * Apply only the attribute bindings whose template references a
     * changed key. Registrations live on component._attrBindings and are
     * populated by _applyAttributeBindings (mount + post-conditional
     * injection).
     */
    _applyAttributeBindingsForKeys(component, componentId, allChanged) {
        const bindings = component._attrBindings;
        if (!bindings || !bindings.length) return;
        const scope = { ...component.state, ...this._deriveVariables(component.state, componentId) };
        for (const entry of bindings) {
            const { element, bindName, spec, template } = entry;
            if (!element.isConnected) continue;
            const owner = element.closest('[data-component-id]');
            if (owner && owner.dataset.componentId !== componentId) continue;
            if (!this._elementDependsOn(element, template, allChanged)) continue;
            try {
                const value = this._evaluateAttributeTemplate(template, scope);
                // _evaluatePSXExpr returns the source expression unchanged when
                // evaluation fails — writing that back would clobber the valid
                // SSR attribute with raw Python source.  Keep the SSR value.
                if (String(value) === String(template).trim()) continue;
                if (spec === 'class') {
                    element.className = String(value);
                } else if (spec === 'style') {
                    element.setAttribute('style', String(value));
                } else if (spec.startsWith('attr-')) {
                    const attrName = spec.slice(5);
                    const booleanAttrs = ['disabled', 'checked', 'readonly', 'required', 'multiple', 'selected', 'autofocus', 'hidden', 'open'];
                    if (booleanAttrs.includes(attrName)) {
                        if (value) {
                            element.setAttribute(attrName, '');
                        } else {
                            element.removeAttribute(attrName);
                        }
                    } else {
                        element.setAttribute(attrName, String(value));
                    }
                }
            } catch (error) {
                console.warn('Attribute binding update failed:', bindName, error);
            }
        }
    }

    /**
     * Collect elements carrying data-psx-ref="name" into the component's
     * ref registry so Python useRef() values can reach DOM nodes.
     */
    _collectRefs(componentId) {
        const root = document.getElementById(componentId);
        if (!root) return;
        let refs = this.refs.get(componentId);
        if (!refs) {
            refs = new Map();
            this.refs.set(componentId, refs);
        }
        root.querySelectorAll('[data-psx-ref]').forEach(el => {
            refs.set(el.getAttribute('data-psx-ref'), el);
        });
    }

    /** Public: get a DOM element registered via data-psx-ref. */
    getRef(componentId, name) {
        const refs = this.refs.get(componentId);
        return refs ? refs.get(name) : null;
    }

    // ── Motion / AnimatePresence (Web Animations API) ────────────────────────

    /**
     * Initialize every [data-psx-motion] element under root that hasn't been
     * initialized yet. Applies `initial` styles, plays the `animate` entrance,
     * wires whileHover/whileTap, and registers FLIP elements (layout: true).
     */
    _initMotionElements(root) {
        if (typeof document === 'undefined' || typeof Element === 'undefined') return;
        const scope = root && root.querySelectorAll ? root : document;
        const candidates = [];
        if (scope.matches && scope.matches('[data-psx-motion]')) candidates.push(scope);
        scope.querySelectorAll('[data-psx-motion]').forEach(el => candidates.push(el));
        candidates.forEach(el => {
            if (el._psxMotion || typeof el.animate !== 'function') return;
            let cfg;
            try { cfg = JSON.parse(el.getAttribute('data-psx-motion') || '{}'); }
            catch (e) { return; }
            el._psxMotion = cfg;
            if (cfg.layout) this._flipElements.add(el);
            if (cfg.initial) this._applyInstantStyles(el, cfg.initial);
            // Snapshot computed values for every animated prop so gesture
            // reverts can restore props that `animate` doesn't mention
            // (e.g. whileHover's `scale` when animate only has opacity).
            el._psxMotionBase = this._captureMotionBase(el, cfg);
            if (cfg.animate) {
                const anim = el.animate(
                    this._psxKeyframes(cfg.animate, el),
                    this._psxAnimOptions(cfg.transition)
                );
                this._commitOnFinish(anim);
            }
            if (cfg.whileHover || cfg.whileTap) this._bindMotionGestures(el, cfg);
        });
        this._observeMotionDom();
    }

    /** Lazily start a MutationObserver so SSR/innerHTML-injected motion
     *  elements get initialized without explicit calls. */
    _observeMotionDom() {
        if (this._motionObserver || typeof MutationObserver !== 'function') return;
        if (typeof document === 'undefined' || !document.documentElement) return;
        let scheduled = false;
        this._motionObserver = new MutationObserver(() => {
            if (scheduled) return;
            scheduled = true;
            setTimeout(() => {
                scheduled = false;
                this._initMotionElements(document);
            }, 0);
        });
        this._motionObserver.observe(document.documentElement, { childList: true, subtree: true });
    }

    /** camelCase style prop → kebab-case CSS property for getComputedStyle. */
    _cssPropName(prop) {
        return String(prop).replace(/[A-Z]/g, m => '-' + m.toLowerCase());
    }

    /** Computed value of a motion style prop on el ('' if unavailable). */
    _computedMotionValue(el, prop) {
        try {
            const v = getComputedStyle(el).getPropertyValue(this._cssPropName(prop));
            return (v === null || v === undefined) ? '' : String(v).trim();
        } catch (e) { return ''; }
    }

    /**
     * Snapshot computed values for every prop named in any motion spec.
     * Used to revert gesture-only props (scale, rotate, ...) that `animate`
     * doesn't cover.
     */
    _captureMotionBase(el, cfg) {
        const base = {};
        const specs = [cfg.initial, cfg.animate, cfg.exit, cfg.whileHover, cfg.whileTap];
        specs.forEach(spec => {
            Object.keys(spec || {}).forEach(prop => {
                if (base[prop] === undefined) {
                    base[prop] = this._computedMotionValue(el, prop);
                }
            });
        });
        return base;
    }

    /**
     * Convert a style spec ({prop: scalar|[v1,v2,...]}) into WAAPI keyframes.
     * Scalars are expanded to [currentValue, target] — a single-element
     * keyframe array produces no visible tween in WAAPI.
     */
    _psxKeyframes(spec, el) {
        const kf = {};
        for (const [prop, value] of Object.entries(spec || {})) {
            const vals = Array.isArray(value) ? value.slice() : [value];
            if (vals.length === 1) {
                const target = vals[0];
                const cur = el ? this._computedMotionValue(el, prop) : '';
                kf[prop] = (cur && cur !== String(target)) ? [cur, target] : [target, target];
            } else {
                kf[prop] = vals;
            }
        }
        return kf;
    }

    _psxAnimOptions(transition) {
        const t = transition || {};
        return {
            duration: (t.duration !== undefined ? t.duration : 0.3) * 1000,
            delay: (t.delay || 0) * 1000,
            easing: t.easing || 'ease-out',
            fill: 'none',
        };
    }

    _applyInstantStyles(el, styleSpec) {
        for (const [prop, value] of Object.entries(styleSpec || {})) {
            const vals = Array.isArray(value) ? value : [value];
            el.style[prop] = vals[vals.length - 1];
        }
    }

    /** Persist the animation's end state as inline styles, then release it. */
    _commitOnFinish(anim) {
        if (!anim || !anim.finished) return;
        anim.finished.then(() => {
            try {
                if (typeof anim.commitStyles === 'function') anim.commitStyles();
            } catch (e) {}
            try { anim.cancel(); } catch (e) {}
        }).catch(() => {});
    }

    /**
     * Spec that returns a gesture-touched element to its resting state:
     * `animate` values where defined, otherwise the init-time computed base
     * (so e.g. whileHover's `scale` is reset even when `animate` omits it).
     */
    _motionRevertSpec(el, cfg) {
        const spec = {};
        const gestureProps = new Set([
            ...Object.keys(cfg.whileHover || {}),
            ...Object.keys(cfg.whileTap || {}),
        ]);
        gestureProps.forEach(prop => {
            if (cfg.animate && cfg.animate[prop] !== undefined) {
                spec[prop] = cfg.animate[prop];
            } else {
                const base = (el._psxMotionBase || {})[prop];
                if (base) spec[prop] = base;
            }
        });
        return spec;
    }

    _bindMotionGestures(el, cfg) {
        const play = (spec) => {
            if (!spec) return;
            const anim = el.animate(this._psxKeyframes(spec, el), this._psxAnimOptions(cfg.transition));
            this._commitOnFinish(anim);
        };
        const revert = () => {
            const spec = this._motionRevertSpec(el, cfg);
            if (Object.keys(spec).length) play(spec);
        };
        if (cfg.whileHover) {
            el.addEventListener('mouseenter', () => play(cfg.whileHover));
            el.addEventListener('mouseleave', revert);
        }
        if (cfg.whileTap) {
            el.addEventListener('pointerdown', () => play(cfg.whileTap));
            el.addEventListener('pointerup', revert);
            el.addEventListener('pointerleave', revert);
        }
    }

    /**
     * Collect motion elements inside a container that are about to be
     * removed, for AnimatePresence-style exit animations.
     */
    _collectExitingMotions(container) {
        const exiting = [];
        container.querySelectorAll('[data-psx-motion]').forEach(m => {
            if (m._psxMotion && m._psxMotion.exit) exiting.push(m);
        });
        return exiting;
    }

    /** Play exit animations; resolves when all finish or maxWait elapses. */
    _playExitAnimations(exiting, maxWait) {
        const anims = exiting.map(m => {
            try {
                return m.animate(
                    this._psxKeyframes(m._psxMotion.exit, m),
                    this._psxAnimOptions(m._psxMotion.transition)
                );
            } catch (e) { return null; }
        }).filter(Boolean);
        if (!anims.length) return Promise.resolve();
        const finished = Promise.all(anims.map(a => a.finished.catch(() => {})));
        const timeout = new Promise(r => setTimeout(r, maxWait));
        return Promise.race([finished, timeout]);
    }

    // ── FLIP layout animations ───────────────────────────────────────────────

    _snapshotFlip() {
        const snap = new Map();
        this._flipElements.forEach(el => {
            if (el.isConnected) snap.set(el, el.getBoundingClientRect());
        });
        return snap;
    }

    _playFlip(snapshot) {
        snapshot.forEach((first, el) => {
            if (!el.isConnected) return;
            const last = el.getBoundingClientRect();
            const dx = first.left - last.left;
            const dy = first.top - last.top;
            const sx = last.width ? first.width / last.width : 1;
            const sy = last.height ? first.height / last.height : 1;
            if (Math.abs(dx) < 1 && Math.abs(dy) < 1 && Math.abs(sx - 1) < 0.01 && Math.abs(sy - 1) < 0.01) return;
            if (typeof el.animate !== 'function') return;
            el.animate([
                {
                    transform: `translate(${dx}px, ${dy}px) scale(${sx}, ${sy})`,
                    transformOrigin: 'top left',
                },
                { transform: 'none', transformOrigin: 'top left' },
            ], { duration: 300, easing: 'ease-out' });
        });
    }

    _updateConditionalElement(element, componentId, condition) {
        // Evaluate the condition with current state
        const component = this.components.get(componentId);
        if (!component) {
            return;
        }
        
        try {
            // FIX: Safe expression evaluation
            const result = this._evaluateCondition(condition, component.state, componentId);
            
            // Get the true and false branches from data attributes
            const trueContent = element.dataset.ifTrue || '';
            const falseContent = element.dataset.ifFalse || '';
            
            // dataset.ifTrue/ifFalse are already entity-decoded once by the
            // browser — the result is valid innerHTML as-is. Decoding again
            // (e.g. via a textarea) would turn &quot; inside attribute values
            // into literal quotes and break data-psx-motion JSON.
            const derived = this._deriveVariables(component.state, componentId);
            const fullState = { ...component.state, ...derived };
            const branchContent = result ? trueContent : falseContent;
            const newHtml = this._sanitizeHTML(this._evaluatePSXContent(branchContent, fullState));

            // No-op guard: identical content means no DOM churn and no
            // spurious exit animations.
            if (element.innerHTML === newHtml) return;

            const applySwap = () => {
                element.innerHTML = newHtml;
                this._applyStateBindings(element, componentId);
                this._applyAttributeBindings(element, componentId);
                this._initMotionElements(element);
            };

            // AnimatePresence: play exit animations on motion descendants
            // before removing them, then swap in the new branch.
            const exiting = this._collectExitingMotions(element);
            if (exiting.length) {
                const token = (element._psxSwapToken = (element._psxSwapToken || 0) + 1);
                const durations = exiting.map(m => {
                    const t = (m._psxMotion.transition || {});
                    return ((t.duration !== undefined ? t.duration : 0.3) + (t.delay || 0)) * 1000;
                });
                const maxWait = Math.min(Math.max(...durations) + 100, 2000);
                this._playExitAnimations(exiting, maxWait).then(() => {
                    if (element._psxSwapToken === token && element.isConnected) {
                        applySwap();
                    }
                });
                return;
            }

            applySwap();
        } catch (error) {
            console.error('Conditional update error:', error);
        }
    }

    _sanitizeHTML(html) {
        if (typeof window.nextpySanitizeHTML === 'function') {
            return window.nextpySanitizeHTML(html);
        }
        const template = document.createElement('template');
        template.innerHTML = String(html == null ? '' : html);
        const blocked = 'script,iframe,object,embed,link,meta,base,svg,math';
        template.content.querySelectorAll(blocked).forEach(node => node.remove());
        const walker = document.createTreeWalker(template.content, NodeFilter.SHOW_ELEMENT, null);
        const nodes = [];
        while (walker.nextNode()) nodes.push(walker.currentNode);
        nodes.forEach(node => {
            Array.from(node.attributes).forEach(attr => {
                const name = attr.name.toLowerCase();
                const value = String(attr.value || '').trim().toLowerCase();
                const dangerousUrl = /^(javascript|vbscript|data:text\/html|data:image\/svg\+xml):/.test(value);
                if (name.startsWith('on') || name === 'srcdoc' ||
                    ((name === 'href' || name === 'src' || name === 'xlink:href' ||
                      name === 'formaction' || name === 'action') && dangerousUrl)) {
                    node.removeAttribute(attr.name);
                }
            });
        });
        return template.innerHTML;
    }

    _runEffects(componentId, changedKey = null, mount = false) {
        const component = this.components.get(componentId);
        if (!component || !Array.isArray(component.effects) || !component.effects.length) return;
        if (this._effectsRunning.has(componentId)) return;
        if (!component._effectState) component._effectState = {};
        this._effectsRunning.add(componentId);
        try {
            component.effects.forEach((effect, index) => {
                const deps = effect.deps;
                const previous = component._effectState[index];
                let shouldRun = false;
                if (mount && previous === undefined) {
                    shouldRun = true;
                } else if (deps === null || deps === undefined) {
                    shouldRun = true;
                } else if (Array.isArray(deps)) {
                    if (deps.length === 0) {
                        shouldRun = previous === undefined;
                    } else if (changedKey !== null) {
                        shouldRun = deps.includes(changedKey);
                    }
                }
                if (!shouldRun) return;
                component._effectState[index] = {
                    deps: Array.isArray(deps) ? deps.slice() : deps,
                };
                try {
                    this.executeActions(effect.actions || [], componentId).catch(err => {
                        if (err && err.type === 'RETURN') return;
                        console.error('Effect execution error:', err);
                    });
                } catch (error) {
                    console.error('Effect execution error:', error);
                }
            });
        } finally {
            this._effectsRunning.delete(componentId);
        }
    }

    _evaluateAttributeTemplate(template, state) {
        if (template === null || template === undefined) return '';
        const text = String(template);
        // Prefer whole-expression evaluation first.  Templates that are
        // themselves a Python expression — f-strings like
        // ``f"{acc_icon} rotate-45" if open else f"{acc_icon} rotate-0"`` —
        // contain ``{...}`` holes, but the brace pass below would substitute
        // the holes and leave the surrounding Python syntax unevaluated.
        // _evaluatePSXExpr returns the trimmed input unchanged on failure,
        // which is our "not a whole expression" signal.
        const direct = this._evaluatePSXExpr(text, state);
        const failed = direct === text.trim();
        if (!failed && (direct === null || typeof direct !== 'object')) {
            return direct;
        }
        if (!text.includes('{')) {
            return failed ? text : direct;
        }
        return text.replace(/\{([^{}]+)\}/g, (_, expr) => {
            const value = this._evaluatePSXExpr(expr.trim(), state);
            return value === null || value === undefined ? '' : String(value);
        });
    }

    _applyAttributeBindings(root, componentId) {
        const component = this.components.get(componentId);
        if (!component) return;
        const scope = { ...component.state, ...this._deriveVariables(component.state, componentId) };
        const candidates = root ? root.querySelectorAll('*') : document.querySelectorAll('*');
        candidates.forEach(element => {
            const owner = element.closest('[data-component-id]');
            if (owner && owner.dataset.componentId !== componentId) return;
            let bindName = null;
            for (const name of element.getAttributeNames()) {
                if (name.startsWith('data-bind-') && name !== 'data-bind') {
                    bindName = name;
                    break;
                }
            }
            if (!bindName) return;
            const spec = bindName.slice('data-bind-'.length);
            const template = element.getAttribute(bindName);
            // Register for fine-grained per-frame updates.
            if (!component._attrBindings) component._attrBindings = [];
            if (!component._attrBindings.some(e => e.element === element && e.bindName === bindName)) {
                component._attrBindings.push({ element, bindName, spec, template });
            }
            try {
                const value = this._evaluateAttributeTemplate(template, scope);
                // _evaluatePSXExpr returns the source expression unchanged when
                // evaluation fails — writing that back would clobber the valid
                // SSR attribute with raw Python source.  Keep the SSR value.
                if (String(value) === String(template).trim()) return;
                if (spec === 'class') {
                    element.className = String(value);
                } else if (spec === 'style') {
                    element.setAttribute('style', String(value));
                } else if (spec.startsWith('attr-')) {
                    const attrName = spec.slice(5);
                    const booleanAttrs = ['disabled', 'checked', 'readonly', 'required', 'multiple', 'selected', 'autofocus', 'hidden', 'open'];
                    if (booleanAttrs.includes(attrName)) {
                        if (value) {
                            element.setAttribute(attrName, '');
                        } else {
                            element.removeAttribute(attrName);
                        }
                    } else {
                        element.setAttribute(attrName, String(value));
                    }
                }
            } catch (error) {
                console.warn('Attribute binding update failed:', bindName, error);
            }
        });
    }

    _applyStateBindings(root, componentId) {
        const component = this.components.get(componentId);
        if (!component) return;
        for (const [stateKey, stateValue] of Object.entries(component.state)) {
            const nodes = root.querySelectorAll(`[data-state-${stateKey}]`);
            if (!nodes.length) continue;
            const text = (stateValue === null || stateValue === undefined) ? '' : String(stateValue);
            nodes.forEach(node => {
                node.textContent = text;
                if (node.hasAttribute('data-state-toggle')) {
                    node.style.display = text ? '' : 'none';
                }
            });
        }
    }

    /**
     * Generic PSX expression evaluator — evaluates any Python-like expression
     * against a state object. Handles:
     *   - Variable access: user, is_employer, my_jobs
     *   - Attribute/dict access: user.full_name, user["key"], user.get("key", default)
     *   - Method calls: user.get("full_name", ""), value.title(), value.strip()
     *   - Function calls: job_type_label(x), len(x), str(x), int(x)
     *   - Ternary / inline if: "A" if cond else "B"
     *   - Comparison: ==, !=, <, >, <=, >=, in, not in
     *   - Boolean: and, or, not
     *   - F-strings: f"prefix {expr} suffix"
     *   - String concatenation: "a" + "b"
     *   - Subscript: x[0], x["key"], x["key"]
     *   - None / True / False
     */
    _evaluatePSXExpr(expr, state) {
        expr = expr.trim();
        if (expr === '') return '';
        
        // Fast path: simple string literals.  Do not mistake a ternary such
        // as ``'a' if cond else 'b'`` for one quoted string — it starts and
        // ends with a quote but contains inner quotes.
        if ((expr.startsWith('"') && expr.endsWith('"')) || (expr.startsWith("'") && expr.endsWith("'"))) {
            const quote = expr[0];
            const inner = expr.slice(1, -1);
            if (!inner.includes(quote) && !inner.includes('\\' + quote)) {
                // Recursively evaluate nested string literals — JSON-serialized
                // Python expressions arrive as "'value'" (double-quoted string
                // containing a single-quoted literal).
                const trimmedInner = inner.trim();
                if ((trimmedInner.startsWith('"') && trimmedInner.endsWith('"')) ||
                    (trimmedInner.startsWith("'") && trimmedInner.endsWith("'"))) {
                    return this._evaluatePSXExpr(trimmedInner, state);
                }
                return inner;
            }
        }
        // Fast path: numeric literals
        if (/^-?\d+(\.\d+)?$/.test(expr)) {
            return Number(expr);
        }
        // Fast path: simple True/False/None
        if (expr === 'True') return true;
        if (expr === 'False') return false;
        if (expr === 'None') return null;
        
        let jsExpr = expr;
        
        // 1. Convert Python operators to JS
        jsExpr = jsExpr
            .replace(/\bTrue\b/g, 'true')
            .replace(/\bFalse\b/g, 'false')
            .replace(/\bNone\b/g, 'null')
            .replace(/\band\b/g, '&&')
            .replace(/\bor\b/g, '||')
            .replace(/\bnot\s+/g, '!');
        
        // 2. Handle f-strings: f"prefix {expr} suffix" → `prefix ${eval(expr)} suffix`
        jsExpr = jsExpr.replace(/f(["'])((?:\\.|(?!\1).)*?)\1/g, (_, quote, inner) => {
            let tmpl = inner
                .replace(/\{\{/g, '__LBRACE__')
                .replace(/\}\}/g, '__RBRACE__');
            tmpl = tmpl.replace(/\{([^}]+)\}/g, (_, subExpr) => {
                // Evaluate the sub-expression and substitute its value directly
                // into the template literal — don't leave a variable reference
                // that won't resolve in the JS scope.
                const subValue = this._evaluatePSXExpr(subExpr.trim(), state);
                const subStr = (subValue === null || subValue === undefined) ? '' : String(subValue);
                return subStr.replace(/\\/g, '\\\\').replace(/`/g, '\\`').replace(/\$/g, '\\$');
            });
            tmpl = tmpl.replace(/__LBRACE__/g, '{').replace(/__RBRACE__/g, '}');
            return '`' + tmpl + '`';
        });
        
        // 3. Handle inline if/else: "A" if cond else "B" → cond ? "A" : "B"
        // Support both: expr if cond else expr  AND nested ternaries
        jsExpr = this._convertTernary(jsExpr, state);
        
        // 4. Handle len(x) → x.length
        jsExpr = jsExpr.replace(/\blen\(([^)]+)\)/g, '($1).length');
        
        // 5. Handle .get("key") and .get("key", default) → bracket notation
        // Use balanced-paren scanning instead of regex (handles nested .get() calls)
        let maxGetIter = 20;
        while (jsExpr.includes('.get(') && maxGetIter-- > 0) {
            const idx = jsExpr.indexOf('.get(');
            if (idx === -1) break;
            
            // Find the object path before .get( — walk backwards from idx
            let objStart = idx - 1;
            while (objStart >= 0 && /[\w$\]]/.test(jsExpr[objStart])) objStart--;
            objStart++;
            const objPath = jsExpr.substring(objStart, idx);
            
            // Find the balanced closing paren for .get(
            const argsStart = idx + 5; // position after '.get('
            let depth = 1;
            let ci = argsStart;
            let inStr = false;
            let strCh = '';
            while (ci < jsExpr.length && depth > 0) {
                const ch = jsExpr[ci];
                if (inStr) {
                    if (ch === strCh && jsExpr[ci - 1] !== '\\') inStr = false;
                } else if (ch === '"' || ch === "'") {
                    inStr = true;
                    strCh = ch;
                } else if (ch === '(') depth++;
                else if (ch === ')') depth--;
                ci++;
            }
            
            if (depth !== 0) break; // unbalanced, skip
            
            const argsStr = jsExpr.substring(argsStart, ci - 1);
            
            // Split args by comma at depth 0
            const parts = [];
            let depth2 = 0;
            let current = '';
            inStr = false;
            strCh = '';
            for (let ai = 0; ai < argsStr.length; ai++) {
                const ch = argsStr[ai];
                if (inStr) {
                    current += ch;
                    if (ch === strCh && argsStr[ai - 1] !== '\\') inStr = false;
                } else if (ch === '"' || ch === "'") {
                    inStr = true;
                    strCh = ch;
                    current += ch;
                } else if (ch === '(') { depth2++; current += ch; }
                else if (ch === ')') { depth2--; current += ch; }
                else if (ch === ',' && depth2 === 0) {
                    parts.push(current.trim());
                    current = '';
                } else {
                    current += ch;
                }
            }
            if (current.trim()) parts.push(current.trim());
            
            const key = parts[0] || '';
            const defaultVal = parts[1];
            
            let replacement;
            if (defaultVal !== undefined) {
                replacement = '(' + objPath + '[' + key + '] !== undefined ? ' + objPath + '[' + key + '] : ' + defaultVal + ')';
            } else {
                replacement = objPath + '[' + key + ']';
            }
            
            jsExpr = jsExpr.substring(0, objStart) + replacement + jsExpr.substring(ci);
        }
        
        // 6. Handle Python string methods → JS equivalents
        // .title() → use _title() helper (defined at eval time)
        jsExpr = jsExpr.replace(/\.title\(\)/g, '.___psx_title()');
        jsExpr = jsExpr.replace(/\.strip\(\)/g, '.trim()');
        jsExpr = jsExpr.replace(/\.lower\(\)/g, '.toLowerCase()');
        jsExpr = jsExpr.replace(/\.upper\(\)/g, '.toUpperCase()');
        jsExpr = jsExpr.replace(/\bstr\(([^)]+)\)/g, 'String($1)');
        jsExpr = jsExpr.replace(/\bint\(([^)]+)\)/g, 'parseInt($1)');
        jsExpr = jsExpr.replace(/\bfloat\(([^)]+)\)/g, 'parseFloat($1)');
        jsExpr = jsExpr.replace(/\bbool\(([^)]+)\)/g, '!!($1)');
        
        // 7. Handle Python slicing: x[:150] → x.substring(0, 150), x[1:5] → x.substring(1, 5), x[:] → x
        jsExpr = jsExpr.replace(/(\w+(?:\[[^\]]+\])*)\[([^:]*?):([^)]*?)\]/g, (full, obj, start, end) => {
            const s = start.trim() || '0';
            const e = end.trim();
            if (e === '') return obj + '.substring(' + s + ')';
            return obj + '.substring(' + s + ', ' + e + ')';
        });
        
        // 8. Handle x not in y → !y.includes(x), x in y → y.includes(x)
        jsExpr = jsExpr.replace(/(\S+)\s+not\s+in\s+(\S+)/g, '!$2.includes($1)');
        jsExpr = jsExpr.replace(/(\S+)\s+in\s+(?!=)(\S+)/g, '$2.includes($1)');
        
        // 9. Handle == and != (already JS compatible)
        
        // 10. Replace variable names with values from state.
        // Protect string literals first so identifiers inside quotes
        // (e.g. "password" in a ternary) are not replaced.
        const stringLiterals = [];
        jsExpr = jsExpr.replace(/"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`/g, (match) => {
            stringLiterals.push(match);
            return `__PSX_STR_${stringLiterals.length - 1}__`;
        });
        
        const replacedKeys = new Set();
        // Sort keys by length (longest first) to avoid partial replacements
        const sortedKeys = Object.keys(state).sort((a, b) => b.length - a.length);
        
        for (const key of sortedKeys) {
            const val = state[key];
            if (val === undefined) continue;
            
            // Exact match
            if (jsExpr === key) {
                jsExpr = typeof val === 'string' ? JSON.stringify(val) : (val === null ? 'null' : JSON.stringify(val));
                replacedKeys.add(key);
                continue;
            }
            
            // Word boundary match — skip if inside a placeholder or part of a longer identifier
            const regex = new RegExp(`(?<![\\w$.])${key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(?![\\w$])`, 'g');
            if (regex.test(jsExpr)) {
                const valStr = typeof val === 'string' ? JSON.stringify(val) : (val === null ? 'null' : JSON.stringify(val));
                jsExpr = jsExpr.replace(regex, valStr);
                replacedKeys.add(key);
            }
        }
        
        // 10. Handle remaining unknown identifiers — declare as null to avoid ReferenceError
        // Do this BEFORE restoring string literals so identifiers inside
        // quotes (e.g. "password") are not detected.
        const builtins = new Set(['true','false','null','undefined','NaN','Infinity','Math','JSON','String','Number','Array','Object','console','window','document']);
        const stateKeys = new Set(Object.keys(state));
        const idRegex = /(?<![\\w$.])([a-zA-Z_][a-zA-Z0-9_]*)(?![\\w$(])/g;
        let m;
        const unknownIds = [];
        while ((m = idRegex.exec(jsExpr)) !== null) {
            const id = m[1];
            if (!replacedKeys.has(id) && !builtins.has(id) && !stateKeys.has(id) && !id.startsWith('__')) {
                unknownIds.push(id);
            }
        }
        
        const uniqueUnknownIds = [...new Set(unknownIds)];
        const varDecls = uniqueUnknownIds.map(id => `let ${id} = null;`).join(' ');
        
        // Restore string literals
        jsExpr = jsExpr.replace(/__PSX_STR_(\d+)__/g, (_, idx) => stringLiterals[parseInt(idx)]);
        
        // 11. Evaluate
        try {
            // Ensure String.prototype.___psx_title is defined (for .title() support)
            if (!String.prototype.___psx_title) {
                String.prototype.___psx_title = function() { 
                    return String(this).replace(/\b\w/g, function(c) { return c.toUpperCase(); });
                };
            }
            
            // Build a closure that has all state variables available
            const stateEntries = Object.entries(state).filter(([k, v]) => v !== undefined);
            const paramNames = stateEntries.map(([k]) => k);
            const paramVals = stateEntries.map(([, v]) => v);
            
            // Add built-in helpers as parameters
            paramNames.push('len');
            paramVals.push(function(x) { return x != null ? x.length : 0; });
            
            // Build function body: declare unknowns as null, then return the expression
            const body = varDecls + '\nreturn (' + jsExpr + ');';
            const factory = Function(...paramNames, body);
            const result = factory(...paramVals);
            return result;
        } catch (e) {
            // If evaluation fails, return the original expression (so at least something shows)
            console.warn('PSX expr eval failed:', expr, '→', jsExpr, 'error:', e.message);
            return expr;
        }
    }
    
    /**
     * Convert Python "A" if cond else "B" ternary to JS ternary.
     * Handles nested conditions.
     */
    _convertTernary(expr, state) {
        expr = expr.trim();
        // Unwrap fully-parenthesized expressions that contain a ternary so the
        // inner ``if/else`` sits at depth 0 for the scan below.  ``ast.unparse``
        // emits chained else-branches as ``else (a if c else b)``.
        if (expr.startsWith('(') && expr.endsWith(')') && expr.includes(' if ') && expr.includes(' else ')) {
            let d = 0, quote = null, wraps = true;
            for (let i = 0; i < expr.length; i++) {
                const ch = expr[i];
                if (quote) {
                    if (ch === '\\') { i++; continue; }
                    if (ch === quote) quote = null;
                    continue;
                }
                if (ch === '"' || ch === "'" || ch === '`') { quote = ch; continue; }
                if (ch === '(') d++;
                else if (ch === ')') {
                    d--;
                    if (d === 0 && i !== expr.length - 1) { wraps = false; break; }
                    if (d < 0) { wraps = false; break; }
                }
            }
            if (wraps && d === 0) {
                return '(' + this._convertTernary(expr.substring(1, expr.length - 1), state) + ')';
            }
        }
        // Python ternary is RIGHT-associative:
        //   A if c1 else B if c2 else C  ===  c1 ? A : (c2 ? B : C)
        // Find the FIRST top-level " if " (outside strings/parens/brackets)
        // and the FIRST top-level " else " after it — that else pairs with
        // this if; everything after it is the else-branch (recursively a
        // ternary).  The previous lastIndexOf approach mangled chained
        // ternaries into unbalanced JS.
        const len = expr.length;
        let depth = 0;
        let quote = null;
        const ifs = [];
        const elses = [];
        for (let i = 0; i < len; i++) {
            const ch = expr[i];
            if (quote) {
                if (ch === '\\') { i++; continue; }
                if (ch === quote) quote = null;
                continue;
            }
            if (ch === '"' || ch === "'" || ch === '`') { quote = ch; continue; }
            if (ch === '(' || ch === '[' || ch === '{') { depth++; continue; }
            if (ch === ')' || ch === ']' || ch === '}') { depth = Math.max(0, depth - 1); continue; }
            if (depth !== 0) continue;
            if (expr.startsWith(' if ', i)) { ifs.push(i); i += 3; }
            else if (expr.startsWith(' else ', i)) { elses.push(i); i += 5; }
        }
        if (!ifs.length) return expr;

        const ifIdx = ifs[0];
        const elseIdx = elses.find(e => e > ifIdx);
        if (elseIdx === undefined) return expr;

        const thenExpr = expr.substring(0, ifIdx).trim();
        const condExpr = expr.substring(ifIdx + 4, elseIdx).trim();
        const elseExpr = expr.substring(elseIdx + 6).trim();
        if (!thenExpr || !condExpr || !elseExpr) return expr;

        // Convert condition operators
        let condJS = condExpr
            .replace(/\bTrue\b/g, 'true')
            .replace(/\bFalse\b/g, 'false')
            .replace(/\bNone\b/g, 'null')
            .replace(/\band\b/g, '&&')
            .replace(/\bor\b/g, '||')
            .replace(/\bnot\s+/g, '!');

        // Replace variables in condition
        for (const [key, value] of Object.entries(state)) {
            if (value === undefined) continue;
            const regex = new RegExp(`(?<![\\w$.])${key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(?![\\w$])`, 'g');
            const valStr = typeof value === 'string' ? JSON.stringify(value) : (value === null ? 'null' : JSON.stringify(value));
            condJS = condJS.replace(regex, valStr);
        }

        // Recurse: then/else branches may themselves contain ternaries
        // (e.g. parenthesized ``(a if c else b)`` or chained ``x if c1 else y if c2 else z``)
        const thenJS = this._convertTernary(thenExpr, state);
        const elseJS = this._convertTernary(elseExpr, state);

        return '(' + condJS + ') ? (' + thenJS + ') : (' + elseJS + ')';
    }
    
    /**
     * Evaluate PSX expressions inside HTML content.
     * Finds all {expr} patterns (not inside HTML attributes) and evaluates them.
     * Also handles escaped HTML entities like &quot; that came from data attributes.
     */
    _evaluatePSXContent(html, state) {
        if (!html || typeof html !== 'string') return html || '';
        
        // Step 1: Unescape any HTML entities that were encoded in data attributes
        // This handles &quot; → ", &lt; → <, &gt; → >, &amp; → &
        let result = html;
        
        // Step 2: Find and evaluate {expr} patterns
        // But we must NOT evaluate {expr} inside HTML attribute values
        // Strategy: split by HTML tags, only evaluate expressions in text nodes
        
        const parts = [];
        let i = 0;
        
        while (i < result.length) {
            // Check if we're entering an HTML tag
            if (result[i] === '<') {
                // Find the end of this tag
                let tagEnd = result.indexOf('>', i);
                if (tagEnd === -1) tagEnd = result.length - 1;
                
                // Check if this is a self-closing tag
                let tagStr = result.substring(i, tagEnd + 1);
                
                // Check for {expr} inside tag attributes (like href={f"/jobs/{job['id']}"})
                // These need evaluation too!
                let tagParts = this._evaluateTagAttributes(tagStr, state);
                
                parts.push(tagParts);
                i = tagEnd + 1;
            } else if (result[i] === '{' && i + 1 < result.length && result[i + 1] !== '{') {
                // Find matching closing brace
                let braceDepth = 1;
                let j = i + 1;
                while (j < result.length && braceDepth > 0) {
                    if (result[j] === '{') braceDepth++;
                    else if (result[j] === '}') braceDepth--;
                    j++;
                }
                
                if (braceDepth === 0) {
                    const expr = result.substring(i + 1, j - 1).trim();
                    
                    // Skip if this looks like it's not a PSX expression
                    // (e.g., CSS { } blocks, JSON, etc.)
                    if (expr && !expr.includes('{') && !expr.includes('}')) {
                        const val = this._evaluatePSXExpr(expr, state);
                        if (val !== null && val !== undefined) {
                            parts.push(String(val));
                        } else {
                            parts.push('');
                        }
                    } else {
                        parts.push(result.substring(i, j));
                    }
                    i = j;
                } else {
                    parts.push(result[i]);
                    i++;
                }
            } else if (result[i] === '{' && i + 1 < result.length && result[i + 1] === '{') {
                // Escaped brace {{ — output single {
                parts.push('{');
                i += 2;
            } else if (result[i] === '}' && i + 1 < result.length && result[i + 1] === '}') {
                // Escaped brace }} — output single }
                parts.push('}');
                i += 2;
            } else {
                // Plain text — accumulate until next special character
                let textEnd = i;
                while (textEnd < result.length && result[textEnd] !== '<' && result[textEnd] !== '{') {
                    textEnd++;
                }
                parts.push(result.substring(i, textEnd));
                i = textEnd;
            }
        }
        
        return parts.join('');
    }
    
    /**
     * Evaluate PSX expressions inside HTML tag attribute values.
     * E.g., <a href={f"/jobs/{job['id']}"}> → <a href="/jobs/123">
     */
    _evaluateTagAttributes(tagStr, state) {
        // Find attribute values that contain {expr}
        return tagStr.replace(/(\w[\w-]*)=["']([^"']*?\{[^}]+[^"']*?)["']/g, (match, attrName, attrValue) => {
            // Internal runtime attributes (data-psx-motion JSON, data-bind
            // templates, data-if-* branches) contain braces that are NOT
            // PSX expressions — evaluating them corrupts the payload.
            if (/^(data-psx-|data-bind|data-if-|data-handler-|data-component-id|data-state-)/.test(attrName)) {
                return match;
            }
            // Check if the attribute value contains {expr}
            if (!attrValue.includes('{')) return match;
            
            // Evaluate the attribute value
            let evaluated = attrValue.replace(/\{([^}]+)\}/g, (_, expr) => {
                const val = this._evaluatePSXExpr(expr, state);
                return val !== null && val !== undefined ? String(val) : '';
            });
            
            return attrName + '="' + evaluated + '"';
        });
    }

    _evaluateCondition(expr, state, componentId = null) {
        // Derive common Python variables from fetch data before evaluating
        const derived = this._deriveVariables(state, componentId);
        
        // Merge derived variables with state for evaluation
        const fullState = { ...state, ...derived };
        
        try {
            const result = this._evaluatePSXExpr(expr, fullState);
            return !!result; // coerce to boolean
        } catch (e) {
            console.warn('Failed to evaluate condition:', expr, e);
            return false;
        }
    }

    _deriveVariables(state, componentId = null) {
        // Derive common Python variables from fetch data
        // This bridges the gap between Python server-side derived variables
        // and client-side state that only has raw fetch data
        const derived = {};
        
        for (const [key, value] of Object.entries(state)) {
            // Only process fetch data keys
            if (!key.startsWith('_fetch_data_')) continue;
            if (value === null || value === undefined || typeof value !== 'object') continue;
            
            // Pattern 1: Direct response like {"user": {...}} from get_me
            // The Python code does: me_data.get("data") or {} then me.get("user")
            // At client-side, _fetch_data_0 IS the raw response (no wrapping)
            // But Python's useFetch wraps it in {"data": raw_response}
            // So _fetch_data_0 = {"data": {"user": {...}}} or {"data": {"user": None}}
            const data = value.data !== undefined ? value.data : value;
            if (data === null || data === undefined || typeof data !== 'object') continue;
            
            // Extract 'user' from get_me response
            if (data.user !== undefined && !derived.user) {
                derived.user = data.user;
                derived.not = data.user ? false : true;
                if (data.user) {
                    derived.is_employer = data.user.role === 'employer';
                    derived.is_jobseeker = data.user.role !== 'employer';
                } else {
                    derived.is_employer = false;
                    derived.is_jobseeker = false;
                }
            }
            
            // Pattern 2: get_my_jobs returns {"data": [...]} or {"data": {"data": [...]}}
            if (Array.isArray(data) && !derived.my_jobs) {
                derived.my_jobs = data;
                derived.has_my_jobs = data.length > 0;
            } else if (data.data && Array.isArray(data.data) && !derived.my_jobs) {
                derived.my_jobs = data.data;
                derived.has_my_jobs = data.data.length > 0;
            } else if (data.jobs && Array.isArray(data.jobs) && !derived.my_jobs) {
                derived.my_jobs = data.jobs;
                derived.has_my_jobs = data.jobs.length > 0;
            }
            
            // Pattern 3: get_my_applications
            if (Array.isArray(data) && !derived.my_apps) {
                derived.my_apps = data;
                derived.has_my_apps = data.length > 0;
            } else if (data.data && Array.isArray(data.data) && !derived.my_apps) {
                derived.my_apps = data.data;
                derived.has_my_apps = data.data.length > 0;
            } else if (data.applications && Array.isArray(data.applications) && !derived.my_apps) {
                derived.my_apps = data.applications;
                derived.has_my_apps = data.applications.length > 0;
            }
        }

        // Re-evaluate source-level derived expressions captured during SSR.
        // This is what makes values like ``bg_color = ... if theme == ...``
        // (flattened by Python f-strings before rendering) reactive again.
        const runtimeComponent = componentId ? this.components.get(componentId) : null;
        const expressions = runtimeComponent && runtimeComponent.derivedExpressions
            ? runtimeComponent.derivedExpressions
            : {};
        const scope = { ...state, ...derived };
        const pending = new Map(Object.entries(expressions));
        // Iterate to a fixpoint: derived vars may depend on other derived
        // vars (nav_link_active -> nav_link_base), and dict order is not
        // guaranteed to be topological.  _evaluatePSXExpr returns the raw
        // expression string on failure, so a value identical to the source
        // expression means "not yet resolvable" — retry on the next pass.
        for (let pass = 0; pass < 6 && pending.size; pass++) {
            let progressed = false;
            for (const [name, expr] of [...pending.entries()]) {
                const src = String(expr);
                try {
                    const value = this._evaluatePSXExpr(src, scope);
                    if (value === src.trim()) {
                        continue; // unresolved — may resolve on a later pass
                    }
                    scope[name] = value;
                    derived[name] = value;
                    pending.delete(name);
                    progressed = true;
                } catch (error) {
                    // Keep SSR value if the client evaluator cannot handle an
                    // expression (e.g. a server-only helper call).
                    pending.delete(name);
                }
            }
            if (!progressed) break;
        }
        
        return derived;
    }

    _registerConditionalElement(element, componentId) {
        // FIX: Register conditional element and build dependency map
        const condition = element.dataset.ifCondition;
        if (!condition) return;
        
        // FIX: Initialize dependency map for component if not exists
        if (!this.dependencyMap.has(componentId)) {
            this.dependencyMap.set(componentId, {});
        }
        
        const componentDeps = this.dependencyMap.get(componentId);
        const component = this.components.get(componentId);
        
        // Extract state dependencies from condition using exact match or word boundary
        for (const key of Object.keys(component.state)) {
            // Try exact match first, then word boundary
            const exactMatch = condition === key;
            const regex = new RegExp(`\\b${key}\\b`);
            const wordBoundaryMatch = regex.test(condition);
            
            if (exactMatch || wordBoundaryMatch) {
                if (!componentDeps[key]) {
                    componentDeps[key] = [];
                }
                if (!componentDeps[key].includes(element)) {
                    componentDeps[key].push(element);
                }
            }
        }
    }

    _registerBuiltinFunctions() {
        // Register built-in functions
        this.functions.set('len', (obj) => {
            if (Array.isArray(obj)) return obj.length;
            if (typeof obj === 'object') return Object.keys(obj).length;
            if (typeof obj === 'string') return obj.length;
            return 0;
        });

        this.functions.set('str', (obj) => String(obj));
        this.functions.set('int', (obj) => parseInt(obj));
        this.functions.set('float', (obj) => parseFloat(obj));
        this.functions.set('bool', (obj) => Boolean(obj));
        this.functions.set('list', (obj) => Array.from(obj));
        this.functions.set('dict', (obj) => ({ ...obj }));
        this.functions.set('abs', Math.abs);
        this.functions.set('min', Math.min);
        this.functions.set('max', Math.max);
        this.functions.set('sum', (arr) => arr.reduce((a, b) => a + b, 0));
        this.functions.set('any', (arr) => arr.some(Boolean));
        this.functions.set('all', (arr) => arr.every(Boolean));
        this.functions.set('round', Math.round);
        this.functions.set('range', (n) => Array.from({ length: n }, (_, i) => i));

        // Console functions
        this.functions.set('console_log', console.log);
        this.functions.set('alert', (msg) => alert(msg));
    }

    _executeDefineFunction(data, componentId) {
        // Register a nested def as a callable thunk. Params are bound into
        // component state for the duration of the call (restored after), so
        // compiled VARIABLE lookups inside the body resolve correctly.
        const { name, params = [], actions = [] } = data;
        const target = componentId && this.components.has(componentId)
            ? this.components.get(componentId).functions
            : this.functions;

        const fn = (...args) => {
            const comp = componentId ? this.components.get(componentId) : null;
            const saved = {};
            if (comp) {
                params.forEach((p, i) => {
                    saved[p] = comp.state[p];
                    comp.state[p] = args[i];
                });
            }
            const restore = () => {
                if (!comp) return;
                for (const p of Object.keys(saved)) {
                    if (saved[p] === undefined) delete comp.state[p];
                    else comp.state[p] = saved[p];
                }
            };
            return this.executeActions(actions, componentId).then(
                (res) => { restore(); return res; },
                (err) => {
                    restore();
                    if (err && err.type === 'RETURN') return err.value;
                    throw err;
                }
            );
        };
        target.set(name, fn);
        return fn;
    }

    async _executeForLoop(data, componentId) {
        const { vars = [], iter, body = [], orelse = [] } = data;
        const iterable = this._evaluateExpression(iter, componentId);

        let items = [];
        if (iterable != null) {
            if (typeof iterable === 'string') {
                items = [...iterable];
            } else if (typeof iterable[Symbol.iterator] === 'function') {
                items = [...iterable];
            } else if (typeof iterable.length === 'number') {
                items = Array.from(iterable);
            }
        }

        const comp = componentId ? this.components.get(componentId) : null;
        let broke = false;
        for (const item of items) {
            const saved = {};
            if (comp) {
                vars.forEach((v, i) => {
                    saved[v] = comp.state[v];
                    comp.state[v] = (vars.length > 1 && Array.isArray(item)) ? item[i] : item;
                });
            }
            try {
                await this.executeActions(body, componentId);
            } catch (e) {
                if (e && e.type === 'PSX_BREAK') { broke = true; break; }
                if (e && e.type === 'PSX_CONTINUE') continue;
                throw e;
            } finally {
                if (comp) {
                    for (const v of vars) {
                        if (saved[v] === undefined) delete comp.state[v];
                        else comp.state[v] = saved[v];
                    }
                }
            }
        }
        // Python semantics: else runs only when the loop did not break.
        if (!broke && orelse.length) {
            await this.executeActions(orelse, componentId);
        }
    }

    _executeWhileLoop(data, componentId) {
        // Placeholder implementation
        // While loops require more complex execution context
        console.warn('WHILE_LOOP not yet implemented in JS runtime');
    }

    _executeBreak() {
        throw { type: 'PSX_BREAK' };
    }

    _executeContinue() {
        throw { type: 'PSX_CONTINUE' };
    }

    _executeTry(data, componentId) {
        // Placeholder implementation
        // Try/except requires exception handling context
        console.warn('TRY not yet implemented in JS runtime');
    }

    _executeReturn(data) {
        // Placeholder implementation
        // Return requires function context
        const value = this._evaluateExpression(data.value);
        throw { type: 'RETURN', value };
    }

    _executeLambda(data) {
        // Placeholder implementation
        // Lambdas require function creation context
        const { args, body } = data;
        return (...lambdaArgs) => {
            // Create a scope for lambda arguments
            const scope = {};
            args.forEach((arg, i) => {
                scope[arg] = lambdaArgs[i];
            });
            return this._evaluateExpression(body);
        };
    }

    _executeJsxUpdate(data, componentId) {
        // Placeholder implementation
        // JSX updates require DOM manipulation context
        console.warn('JSX_UPDATE not yet implemented in JS runtime');
    }
}

// Global runtime instance
window.NextPyActionRuntime = new NextPyActionRuntime();

// Handler execution function
window.executeNextPyActions = async function(actions, componentId = null) {
    return await window.NextPyActionRuntime.executeActions(actions, componentId);
};

// Component registration function
window.registerNextPyComponent = function(componentId, initialState = {}) {
    return window.NextPyActionRuntime.registerComponent(componentId, initialState);
};

// ── Fine-grained reactivity primitives ──────────────────────────────────────
// window.nextpy.createSignal(v)  → PSXSignal with .get()/.set()/.subscribe()
// window.nextpy.signal(cid, k)   → per-component state signal (auto-synced)
// window.nextpy.effect(fn)       → re-run fn only when signals it read change
// window.nextpy.flush()          → synchronously flush pending rAF DOM updates
// window.nextpy.getRef(cid, n)   → DOM element registered via data-psx-ref
// window.nextpy.useRef(v)        → plain client-side ref object { current: v }
window.nextpy = window.nextpy || {};
window.nextpy.createSignal = function(initial) {
    return new PSXSignal(initial);
};
window.nextpy.signal = function(componentId, key) {
    return window.NextPyActionRuntime._signalFor(componentId, key);
};
window.nextpy.effect = function(fn) {
    return psxEffect(fn);
};
window.nextpy.flush = function() {
    window.NextPyActionRuntime.flush();
};
window.nextpy.getRef = function(componentId, name) {
    return window.NextPyActionRuntime.getRef(componentId, name);
};
window.nextpy.useRef = function(initial) {
    return { current: initial };
};

// SPA-style navigation function — called by lambda handlers after actions
window.navigateTo = function(url) {
    if (window.__nextpyNavigate) {
        window.__nextpyNavigate(url);
    } else if (window.htmx) {
        const target = document.getElementById('main-content') || document.querySelector('main');
        if (target) {
            htmx.ajax('GET', url, { target: '#main-content', swap: 'innerHTML' });
            history.pushState({}, '', url);
            return;
        }
        window.location.href = url;
    } else {
        window.location.href = url;
    }
};

// Full navigation — used after auth changes so SSR layout (nav/auth state)
// is refreshed along with the page.
window.nextpyHardNavigate = function(url) {
    window.location.href = url;
};

// SPA-style reload — re-fetches current page content without full reload
window.spaReload = function() {
    const url = window.location.pathname + window.location.search;
    if (window.__nextpyNavigate) {
        window.__nextpyNavigate(url, true);
    } else if (window.htmx) {
        const target = document.getElementById('main-content') || document.querySelector('main');
        if (target) {
            htmx.ajax('GET', url, { target: '#main-content', swap: 'innerHTML' });
            return;
        }
    }
    window.location.reload();
};

// Initialize Motion/AnimatePresence elements on pages that don't go through
// component hydration (plain render_psx_component output).
if (typeof document !== 'undefined') {
    const bootMotion = () => window.NextPyActionRuntime._initMotionElements(document);
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bootMotion);
    } else {
        bootMotion();
    }
}

console.log('[NextPy] Action Runtime loaded');
})();
"""
