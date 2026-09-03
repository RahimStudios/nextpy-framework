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

class NextPyActionRuntime {
    constructor() {
        this.components = new Map();
        this.globalState = {};
        this.functions = new Map();
        this.dependencyMap = new Map(); // FIX: Track state dependencies
        this._registerBuiltinFunctions();
    }

    registerComponent(componentId, initialState = {}) {
        this.components.set(componentId, {
            state: { ...initialState },
            listeners: []
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
                default:
                    console.warn(`Unknown action type: ${type}`);
                    return null;
            }
        } catch (error) {
            console.error(`Action execution error:`, error);
            if (window.NEXTPY_DEBUG) throw error;
            return null;
        }
    }

    async executeActions(actions, componentId = null) {
        const results = [];
        for (const action of actions) {
            const result = await this.executeAction(action, componentId);
            results.push(result);
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

        if (this.functions.has(funcName)) {
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
            case 'not': return !operandValue;
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
            component.state['_server_loading'] = true;
            component.state['_server_error'] = null;
            this._triggerComponentUpdate(componentId, '_server_loading', true);
        }

        try {
            const response = await fetch('/__nextpy/actions/execute', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                body: JSON.stringify({ action: actionName, params: params }),
            });

            const result = await response.json();

            if (component) {
                component.state['_server_loading'] = false;
                component.state['_server_result'] = result;
                this._triggerComponentUpdate(componentId, '_server_loading', false);
                this._triggerComponentUpdate(componentId, '_server_result', result);
            }

            return result;
        } catch (err) {
            console.error('CALL_SERVER_ACTION error:', err);
            if (component) {
                component.state['_server_loading'] = false;
                component.state['_server_error'] = err.message || String(err);
                this._triggerComponentUpdate(componentId, '_server_loading', false);
                this._triggerComponentUpdate(componentId, '_server_error', err.message || String(err));
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
        // Sync to hydration component's StateManager to trigger DOM data-bind updates
        if (window.nextpyComponents && window.nextpyComponents[componentId]) {
            const hydComp = window.nextpyComponents[componentId];
            if (hydComp.stateManager && hydComp.stateManager.state[key] !== newValue) {
                hydComp.stateManager.set(key, newValue);
            }
        }

        // Find DOM elements that depend on this state (legacy data-state-* attributes)
        const elements = document.querySelectorAll(`[data-state-${key}]`);
        elements.forEach(element => {
            if (element.dataset.componentId === componentId) {
                element.textContent = newValue;
            }
        });
        
        // FIX: Re-evaluate ALL conditional elements for this component on ANY state change.
        // Conditions reference derived Python variables (user, is_employer, etc.) that
        // don't match state keys (_fetch_data_0, etc.), so we can't rely on the
        // dependency map for targeted updates. Instead, re-evaluate all conditionals.
        // Also update layout elements with empty data-component-id that reference the
        // same state (e.g., layout nav conditionals for user/login).
        const allConditionals = document.querySelectorAll(`[data-if-condition]`);
        const component = this.components.get(componentId);
        allConditionals.forEach(element => {
            if (element.dataset.componentId === componentId) {
                const condition = element.dataset.ifCondition;
                if (condition) {
                    this._updateConditionalElement(element, componentId, condition);
                }
            } else if (!element.dataset.componentId && component) {
                // Layout element with empty component ID — update using this component's state
                const condition = element.dataset.ifCondition;
                if (condition) {
                    this._updateConditionalElement(element, componentId, condition);
                }
            }
        });
        
        // Trigger custom event
        const event = new CustomEvent('nextpy:stateChange', {
            detail: { componentId, key, newValue, oldValue }
        });
        document.dispatchEvent(event);
    }

    _updateConditionalElement(element, componentId, condition) {
        // Evaluate the condition with current state
        const component = this.components.get(componentId);
        if (!component) {
            return;
        }
        
        try {
            // FIX: Safe expression evaluation
            const result = this._evaluateCondition(condition, component.state);
            
            // Get the true and false branches from data attributes
            const trueContent = element.dataset.ifTrue || '';
            const falseContent = element.dataset.ifFalse || '';
            
            // FIX: Unescape HTML content before setting as innerHTML
            const unescapeHtml = (html) => {
                const textArea = document.createElement('textarea');
                textArea.innerHTML = html;
                return textArea.value;
            };
            
            // FIX: Evaluate PSX expressions inside the content before setting innerHTML
            const derived = this._deriveVariables(component.state);
            const fullState = { ...component.state, ...derived };
            
            // Update the element content based on condition result
            if (result) {
                const raw = unescapeHtml(trueContent);
                element.innerHTML = this._evaluatePSXContent(raw, fullState);
            } else {
                const raw = unescapeHtml(falseContent);
                element.innerHTML = this._evaluatePSXContent(raw, fullState);
            }
        } catch (error) {
            console.error('Conditional update error:', error);
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
        
        // Fast path: simple string literals
        if ((expr.startsWith('"') && expr.endsWith('"')) || (expr.startsWith("'") && expr.endsWith("'"))) {
            return expr.slice(1, -1);
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
                return '${' + this._evaluatePSXExpr(subExpr, state) + '}';
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
        
        // 10. Replace variable names with values from state
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
            
            // Word boundary match — but skip if inside a string or part of a longer identifier
            const regex = new RegExp(`(?<![\\w$.])${key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(?![\\w$])`, 'g');
            if (regex.test(jsExpr)) {
                const valStr = typeof val === 'string' ? JSON.stringify(val) : (val === null ? 'null' : JSON.stringify(val));
                jsExpr = jsExpr.replace(regex, valStr);
                replacedKeys.add(key);
            }
        }
        
        // 10. Handle remaining unknown identifiers — declare as null to avoid ReferenceError
        const builtins = new Set(['true','false','null','undefined','NaN','Infinity','Math','JSON','String','Number','Array','Object','console','window','document']);
        const idRegex = /(?<![\\w$.])([a-zA-Z_][a-zA-Z0-9_]*)(?![\\w$(])/g;
        let m;
        const unknownIds = [];
        while ((m = idRegex.exec(jsExpr)) !== null) {
            const id = m[1];
            if (!replacedKeys.has(id) && !builtins.has(id) && !id.startsWith('__')) {
                unknownIds.push(id);
            }
        }
        
        const varDecls = unknownIds.map(id => `let ${id} = null;`).join(' ');
        
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
            return expr;
        }
    }
    
    /**
     * Convert Python "A" if cond else "B" ternary to JS ternary.
     * Handles nested conditions.
     */
    _convertTernary(expr, state) {
        // Find " if " pattern — but not inside strings
        // We need to match: <then-expr> if <condition> else <else-expr>
        // This is tricky because the else part could contain another ternary
        // Strategy: find " if " from right to left, matching the outermost one
        
        let result = expr;
        // Keep converting until no more "if...else" patterns
        let maxIterations = 10;
        while (result.includes(' if ') && result.includes(' else ') && maxIterations-- > 0) {
            // Find the LAST " if " that has a matching " else "
            const ifIdx = result.lastIndexOf(' if ');
            if (ifIdx <= 0) break;
            
            // Find the matching " else " after this " if "
            const elseIdx = result.indexOf(' else ', ifIdx + 4);
            if (elseIdx < 0) break;
            
            // Extract the then-expr (everything before " if ")
            const thenExpr = result.substring(0, ifIdx).trim();
            // Extract the condition (between " if " and " else ")
            const condExpr = result.substring(ifIdx + 4, elseIdx).trim();
            // Extract the else-expr (everything after " else ")
            let elseExpr = result.substring(elseIdx + 6).trim();
            
            // The else-expr might contain another ternary, so we need to find where it ends
            // For simplicity, if elseExpr contains " if ", we'll handle it in the next iteration
            // unless it's wrapped in parentheses
            
            // Convert condition
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
            
            // Build JS ternary
            result = '(' + condJS + ') ? (' + thenExpr + ') : (' + elseExpr + ')';
        }
        
        return result;
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
        return tagStr.replace(/(\w+)=["']([^"']*?\{[^}]+[^"']*?)["']/g, (match, attrName, attrValue) => {
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

    _evaluateCondition(expr, state) {
        // Derive common Python variables from fetch data before evaluating
        const derived = this._deriveVariables(state);
        
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

    _deriveVariables(state) {
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

        // Console functions
        this.functions.set('console_log', console.log);
        this.functions.set('alert', (msg) => alert(msg));
    }

    _executeForLoop(data, componentId) {
        // Placeholder implementation
        // For loops require more complex execution context
        console.warn('FOR_LOOP not yet implemented in JS runtime');
    }

    _executeWhileLoop(data, componentId) {
        // Placeholder implementation
        // While loops require more complex execution context
        console.warn('WHILE_LOOP not yet implemented in JS runtime');
    }

    _executeBreak() {
        // Placeholder implementation
        // Break requires loop context
        throw new Error('BREAK not yet implemented');
    }

    _executeContinue() {
        // Placeholder implementation
        // Continue requires loop context
        throw new Error('CONTINUE not yet implemented');
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

console.log('[NextPy] Action Runtime loaded');
})();
"""
