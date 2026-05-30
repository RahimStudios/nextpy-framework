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
        return this.components.get(componentId);
    }

    executeAction(action, componentId = null) {
        const { type, data } = action;
        
        try {
            switch (type) {
                case 'SET_STATE':
                    return this._executeSetState(data, componentId);
                case 'GET_STATE':
                    return this._executeGetState(data, componentId);
                case 'CALL_FUNCTION':
                    return this._executeCallFunction(data);
                case 'BINARY_OP':
                    return this._executeBinaryOp(data);
                case 'UNARY_OP':
                    return this._executeUnaryOp(data);
                case 'COMPARE_OP':
                    return this._executeCompareOp(data);
                case 'BOOLEAN_OP':
                    return this._executeBooleanOp(data);
                case 'PRINT':
                    return this._executePrint(data);
                case 'CONSTANT':
                    return this._executeConstant(data);
                case 'VARIABLE':
                    return this._executeVariable(data, componentId);
                case 'LIST':
                    return this._executeList(data);
                case 'DICT':
                    return this._executeDict(data);
                case 'INDEX':
                    return this._executeIndex(data);
                case 'ATTRIBUTE':
                    return this._executeAttribute(data);
                default:
                    console.warn(`Unknown action type: ${type}`);
                    return null;
            }
        } catch (error) {
            console.error(`Action execution error:`, error);
            return null;
        }
    }

    executeActions(actions, componentId = null) {
        const results = [];
        for (const action of actions) {
            const result = this.executeAction(action, componentId);
            results.push(result);
        }
        return results;
    }

    _executeSetState(data, componentId) {
        const { key, value } = data;
        const evaluatedValue = this._evaluateExpression(value);
        
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

    _executeGetState(data, componentId) {
        const { key } = data;
        
        if (componentId && this.components.has(componentId)) {
            return this.components.get(componentId).state[key];
        } else {
            return this.globalState[key];
        }
    }

    _executeCallFunction(data) {
        const { function: funcName, args = [], kwargs = {} } = data;
        const evaluatedArgs = args.map(arg => this._evaluateExpression(arg));
        const evaluatedKwargs = {};
        
        for (const [key, value] of Object.entries(kwargs)) {
            evaluatedKwargs[key] = this._evaluateExpression(value);
        }
        
        if (this.functions.has(funcName)) {
            const func = this.functions.get(funcName);
            return func(...evaluatedArgs, evaluatedKwargs);
        } else if (typeof window[funcName] === 'function') {
            return window[funcName](...evaluatedArgs);
        } else {
            throw new Error(`Unknown function: ${funcName}`);
        }
    }

    _executeBinaryOp(data) {
        const { left, op, right } = data;
        const leftValue = this._evaluateExpression(left);
        const rightValue = this._evaluateExpression(right);
        
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

    _executeUnaryOp(data) {
        const { op, operand } = data;
        const operandValue = this._evaluateExpression(operand);
        
        switch (op) {
            case '+': return +operandValue;
            case '-': return -operandValue;
            case 'not': return !operandValue;
            case '~': return ~operandValue;
            default:
                throw new Error(`Unknown unary operator: ${op}`);
        }
    }

    _executeCompareOp(data) {
        const { left, ops, comparators } = data;
        const leftValue = this._evaluateExpression(left);
        const comparatorValues = comparators.map(c => this._evaluateExpression(c));
        
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
                    case 'in': result = leftValue in comparator; break;
                    case 'not in': result = !(leftValue in comparator); break;
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

    _executeBooleanOp(data) {
        const { op, values } = data;
        const evaluatedValues = values.map(v => this._evaluateExpression(v));
        
        switch (op) {
            case 'and': return evaluatedValues.every(v => v);
            case 'or': return evaluatedValues.some(v => v);
            default:
                throw new Error(`Unknown boolean operator: ${op}`);
        }
    }

    _executePrint(data) {
        const { args = [] } = data;
        const evaluatedArgs = args.map(arg => this._evaluateExpression(arg));
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

    _executeList(data) {
        const { elements } = data;
        return elements.map(el => this._evaluateExpression(el));
    }

    _executeDict(data) {
        const { keys, values } = data;
        const result = {};
        
        for (let i = 0; i < keys.length && i < values.length; i++) {
            const key = this._evaluateExpression(keys[i]);
            const value = this._evaluateExpression(values[i]);
            result[key] = value;
        }
        
        return result;
    }

    _executeIndex(data) {
        const { value, slice } = data;
        const valueObj = this._evaluateExpression(value);
        const sliceValue = this._evaluateExpression(slice);
        
        return valueObj[sliceValue];
    }

    _executeAttribute(data) {
        const { object, attr } = data;
        const obj = this._evaluateExpression(object);
        
        return obj[attr];
    }

    _evaluateExpression(expr) {
        if (expr === null || expr === undefined) {
            return null;
        } else if (typeof expr === 'object' && expr.type) {
            return this.executeAction(expr);
        } else {
            return expr;
        }
    }

    _triggerComponentUpdate(componentId, key, newValue, oldValue) {
        // Find DOM elements that depend on this state
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
