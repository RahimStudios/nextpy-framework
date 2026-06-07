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
        this._registerBuiltinFunctions();
    }

    registerComponent(componentId, initialState = {}) {
        this.components.set(componentId, {
            state: { ...initialState },
            listeners: []
        });
        this._ensureStateDefaults(componentId);
        return this.components.get(componentId);
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

        if (componentId && this.components.has(componentId)) {
            const component = this.components.get(componentId);
            const oldValue = component.state[key];
            component.state[key] = evaluatedValue;

            // Trigger re-render if DOM element exists
            this._triggerComponentUpdate(componentId, key, evaluatedValue, oldValue);
        } else {
            this.globalState[key] = evaluatedValue;
        }
    }

    _executeSetStateBatch(data, componentId) {
        const { updates } = data;

        if (componentId && this.components.has(componentId)) {
            const component = this.components.get(componentId);
            for (const update of updates) {
                const { key, value } = update;
                const evaluatedValue = this._evaluateExpression(value, componentId);
                const oldValue = component.state[key];
                component.state[key] = evaluatedValue;
                this._triggerComponentUpdate(componentId, key, evaluatedValue, oldValue);
            }
        } else {
            for (const update of updates) {
                const { key, value } = update;
                const evaluatedValue = this._evaluateExpression(value, componentId);
                this.globalState[key] = evaluatedValue;
            }
        }
    }

    _executeGetState(data, componentId) {
        const { key } = data;
        
        if (componentId && this.components.has(componentId)) {
            return this.components.get(componentId).state[key];
        } else {
            return this.globalState[key];
        }
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

        // Get the object - retrieve from component state
        let obj;
        if (componentId && this.components.has(componentId)) {
            const component = this.components.get(componentId);
            console.log(`DEBUG _executeCallMethod: All component state:`, component.state);
            console.log(`DEBUG _executeCallMethod: Looking for object '${object}' in state`);
            obj = component.state[object];
        } else {
            obj = this.globalState[object];
        }

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
        
        // Check component state first
        if (componentId && this.components.has(componentId)) {
            const component = this.components.get(componentId);
            if (name in component.state) {
                return component.state[name];
            }
        }
        
        // Check global state
        if (name in this.globalState) {
            return this.globalState[name];
        }
        
        // Check window object
        if (name in window) {
            return window[name];
        }
        
        throw new Error(`Unknown variable: ${name}`);
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
        
        // Trigger custom event
        const event = new CustomEvent('nextpy:stateChange', {
            detail: { componentId, key, newValue, oldValue }
        });
        document.dispatchEvent(event);
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
