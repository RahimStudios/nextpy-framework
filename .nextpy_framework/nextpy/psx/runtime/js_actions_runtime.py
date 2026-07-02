"""
NextPy PSX JavaScript Runtime - Structured Action Execution
Replaces JS string evaluation with structured action processing
"""

# JavaScript runtime script as a constant
JS_ACTION_RUNTIME_SCRIPT = """
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
        console.log('DEBUG: Building dependency map for component', componentId, 'found', conditionalElements.length, 'conditional elements');
        
        // FIX: Initialize dependency map for component if not exists
        if (!this.dependencyMap.has(componentId)) {
            this.dependencyMap.set(componentId, {});
            console.log('DEBUG: Initialized dependency map for component:', componentId);
        }
        
        conditionalElements.forEach(element => {
            if (element.dataset.componentId === componentId) {
                console.log('DEBUG: Registering conditional element with componentId:', componentId);
                this._registerConditionalElement(element, componentId);
            }
        });
        console.log('DEBUG: Dependency map for component', componentId, ':', this.dependencyMap.get(componentId));
        
        // FIX: Set up input bindings for elements with data-bind attribute
        this._setupInputBindings(componentId);
    }
    
    _setupInputBindings(componentId) {
        // FIX: Set up automatic input bindings for elements with data-bind attribute
        const boundElements = document.querySelectorAll(`[data-bind]`);
        console.log('DEBUG: Setting up input bindings for component', componentId, 'found', boundElements.length, 'bound elements');
        
        boundElements.forEach(element => {
            const bindSpec = element.dataset.bind;
            if (!bindSpec) return;
            
            // Parse bind specification: "value:name" or "checked:name"
            const [bindType, stateKey] = bindSpec.split(':');
            console.log('DEBUG: Processing bind:', bindSpec, 'type:', bindType, 'key:', stateKey);
            
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
                
                console.log('DEBUG: Input changed:', stateKey, '->', newValue);
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
                console.log('DEBUG: State changed, updating input:', stateKey, '->', newValue);
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

    executeActions(actions, componentId = null) {
        console.log('DEBUG executeNextPyActions: Executing actions:', JSON.stringify(actions, null, 2));
        console.log('DEBUG executeNextPyActions: componentId:', componentId);
        const results = [];
        for (const action of actions) {
            const result = this.executeAction(action, componentId);
            results.push(result);
        }
        console.log('DEBUG executeNextPyActions: Results:', results);
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

        // FIX: Require componentId to prevent state contamination
        if (!componentId || !this.components.has(componentId)) {
            console.warn('CALL_METHOD: componentId required or component not found:', componentId);
            throw new Error(`Cannot call method without component context`);
        }

        // Get the object - retrieve from component state only
        const component = this.components.get(componentId);
        console.log(`DEBUG _executeCallMethod: All component state:`, component.state);
        console.log(`DEBUG _executeCallMethod: Looking for object '${object}' in state`);
        const obj = component.state[object];

        console.log(`DEBUG _executeCallMethod: Object value:`, obj);
        console.log(`DEBUG _executeCallMethod: Object type:`, typeof obj);

        if (obj === undefined || obj === null) {
            console.warn(`Object '${object}' is undefined or null, returning empty string`);
            return "";
        }

        // Safety check: ensure method exists and is callable
        // Allow methods on strings, arrays, and objects
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

        if (Array.isArray(leftValue) && Array.isArray(rightValue)) {
            return [...leftValue, ...rightValue];
        }

        if (Array.isArray(leftValue)) {
            return [...leftValue, rightValue];
        }

        if (Array.isArray(rightValue)) {
            return [leftValue, ...rightValue];
        }

        return leftValue + rightValue;
        
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
        
        switch (op) {
            case 'and': return evaluatedValues.every(v => v);
            case 'or': return evaluatedValues.some(v => v);
            default:
                throw new Error(`Unknown boolean operator: ${op}`);
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
                // Update the element content
                element.textContent = newValue;
            }
        });
        
        // FIX: Handle conditional rendering updates using dependency map
        const componentDeps = this.dependencyMap.get(componentId);
        console.log('DEBUG: State changed', key, '->', newValue, 'for component', componentId);
        console.log('DEBUG: Component dependencies:', componentDeps);
        if (componentDeps && componentDeps[key]) {
            console.log('DEBUG: Found', componentDeps[key].length, 'conditional elements depending on', key);
            componentDeps[key].forEach(element => {
                const condition = element.dataset.ifCondition;
                console.log('DEBUG: Updating conditional element with condition:', condition);
                this._updateConditionalElement(element, componentId, condition);
            });
        } else {
            console.log('DEBUG: No conditional elements depend on', key);
        }
        
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
            console.log('DEBUG: Component not found:', componentId);
            return;
        }
        
        try {
            // FIX: Safe expression evaluation
            console.log('DEBUG: Evaluating condition:', condition, 'with state:', component.state);
            const result = this._evaluateCondition(condition, component.state);
            console.log('DEBUG: Condition result:', result);
            
            // Get the true and false branches from data attributes
            const trueContent = element.dataset.ifTrue || '';
            const falseContent = element.dataset.ifFalse || '';
            console.log('DEBUG: True content:', trueContent);
            console.log('DEBUG: False content:', falseContent);
            
            // FIX: Unescape HTML content before setting as innerHTML
            const unescapeHtml = (html) => {
                const textArea = document.createElement('textarea');
                textArea.innerHTML = html;
                return textArea.value;
            };
            
            // Update the element content based on condition result
            if (result) {
                element.innerHTML = unescapeHtml(trueContent);
                console.log('DEBUG: Updated element with true content');
            } else {
                element.innerHTML = unescapeHtml(falseContent);
                console.log('DEBUG: Updated element with false content');
            }
        } catch (error) {
            console.error('Conditional update error:', error);
        }
    }

    _evaluateCondition(expr, state) {
        // FIX: Safe condition evaluation with proper variable substitution
        // Replace state variable names with their values
        let evalExpr = expr;
        for (const [key, value] of Object.entries(state)) {
            // Try exact match first, then word boundary regex
            if (evalExpr === key) {
                evalExpr = typeof value === 'string' ? `'${value}'` : JSON.stringify(value);
            } else {
                const regex = new RegExp(`\\b${key}\\b`, 'g');
                evalExpr = evalExpr.replace(regex, typeof value === 'string' ? `'${value}'` : JSON.stringify(value));
            }
        }
        
        console.log('DEBUG: Evaluating condition:', expr, '->', evalExpr, 'with state:', state);
        
        // Safe evaluation of simple boolean expressions
        try {
            return Function(`"use strict"; return (${evalExpr})`)();
        } catch (e) {
            console.warn('Failed to evaluate condition:', expr, e);
            return false;
        }
    }

    _registerConditionalElement(element, componentId) {
        // FIX: Register conditional element and build dependency map
        const condition = element.dataset.ifCondition;
        if (!condition) return;
        
        // FIX: Initialize dependency map for component if not exists
        if (!this.dependencyMap.has(componentId)) {
            this.dependencyMap.set(componentId, {});
            console.log('DEBUG: Initialized dependency map for component:', componentId);
        }
        
        const componentDeps = this.dependencyMap.get(componentId);
        const component = this.components.get(componentId);
        console.log('DEBUG: Condition:', condition, 'State keys:', Object.keys(component.state));
        
        // Extract state dependencies from condition using exact match or word boundary
        for (const key of Object.keys(component.state)) {
            // Try exact match first, then word boundary
            const exactMatch = condition === key;
            const regex = new RegExp(`\\b${key}\\b`);
            const wordBoundaryMatch = regex.test(condition);
            console.log('DEBUG: Testing key:', key, 'exact match:', exactMatch, 'word boundary match:', wordBoundaryMatch);
            
            if (exactMatch || wordBoundaryMatch) {
                if (!componentDeps[key]) {
                    componentDeps[key] = [];
                }
                if (!componentDeps[key].includes(element)) {
                    componentDeps[key].push(element);
                    console.log('DEBUG: Registered element for state key:', key);
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
window.executeNextPyActions = function(actions, componentId = null) {
    return window.NextPyActionRuntime.executeActions(actions, componentId);
};

// Component registration function
window.registerNextPyComponent = function(componentId, initialState = {}) {
    return window.NextPyActionRuntime.registerComponent(componentId, initialState);
};

console.log('[NextPy] Action Runtime loaded');
"""
