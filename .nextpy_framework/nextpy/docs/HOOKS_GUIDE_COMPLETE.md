# 🎣 NextPy Hooks Guide

**Complete React-like hooks system for NextPy!** Use useState, useEffect, and all your favorite React hooks - but in Python!

## 🚀 Quick Start

```python
// Import hooks just like React
from nextpy import useState, useEffect, with_hooks

// Use hooks in your components
@with_hooks
def MyComponent(props):
  [count, setCount] = useState(0)
  [name, setName] = useState('NextPy')
  
  useEffect(() => {
    console.log(f'Count changed to: {count}')
  }, [count])
  
  return (
    <div>
      <h1>Hello {name}!</h1>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
```

## 🔧 Core Hooks

### useState
**State management hook - exactly like React's useState**

```python
@with_hooks
def Counter(props):
  [count, setCount] = useState(0)
  [name, setName] = useState('Counter')
  
  return (
    <div>
      <h1>{name}: {count}</h1>
      <button onClick={() => setCount(count + 1)}>+</button>
      <button onClick={() => setCount(count - 1)}>-</button>
      <button onClick={() => setName('Updated')}>Update Name</button>
    </div>
  );
```

**Features:**
- ✅ Returns [value, setter] tuple
- ✅ Functional updates: `setCount(prev => prev + 1)`
- ✅ Multiple independent state variables
- ✅ Type safety with Python type hints

### useEffect
**Side effects hook - exactly like React's useEffect**

```python
@with_hooks
def TimerComponent(props):
  [seconds, setSeconds] = useState(0)
  
  useEffect(() => {
    // Setup
    timer = setInterval(() => {
      setSeconds(prev => prev + 1)
    }, 1000)
    
    // Cleanup
    return () => clearInterval(timer)
  }, []);  // Empty dependency array = run once
  
  useEffect(() => {
    // Run when seconds change
    console.log(f'Timer: {seconds} seconds')
  }, [seconds]);
  
  return (
    <div>
      <h2>Timer: {seconds}s</h2>
    </div>
  );
```

**Features:**
- ✅ Setup and cleanup functions
- ✅ Dependency array for controlled re-runs
- ✅ Automatic cleanup on unmount
- ✅ Multiple effects per component

### useReducer
**Complex state management - exactly like React's useReducer**

```python
def counterReducer(state, action):
  if action['type'] == 'increment':
    return {'count': state['count'] + state['step'], 'step': state['step']}
  elif action['type'] == 'decrement':
    return {'count': state['count'] - state['step'], 'step': state['step']}
  elif action['type'] == 'setStep':
    return {'count': state['count'], 'step': action['step']}
  return state

@with_hooks
def AdvancedCounter(props):
  [state, dispatch] = useReducer(counterReducer, {'count': 0, 'step': 1})
  
  return (
    <div>
      <h2>Count: {state['count']}</h2>
      <p>Step: {state['step']}</p>
      <button onClick={() => dispatch({'type': 'increment'})}>+</button>
      <button onClick={() => dispatch({'type': 'decrement'})}>-</button>
      <button onClick={() => dispatch({'type': 'setStep', 'step': 5})}>Step 5</button>
    </div>
  );
```

**Features:**
- ✅ Complex state logic in reducer function
- ✅ Dispatch actions for state updates
- ✅ Predictable state transitions
- ✅ Great for complex state management

### useContext
**Context API hook - exactly like React's useContext**

```python
from nextpy import createContext, ContextProvider

// Create context
ThemeContext = createContext('theme', 'light')

@with_hooks
def ThemedComponent(props):
  theme = useContext(ThemeContext)
  
  return (
    <div style={{'background': theme === 'dark' ? '#333' : '#fff', 'color': theme === 'dark' ? '#fff' : '#333'}}>
      <h2>Current theme: {theme}</h2>
      <p>This component uses context!</p>
    </div>
  );

// Wrap with provider
def App():
  return (
    <ContextProvider ThemeContext={'dark'}>
      <ThemedComponent />
    </ContextProvider>
  );
```

**Features:**
- ✅ Global state sharing
- ✅ Provider pattern
- ✅ Default values
- ✅ Context nesting support

### useRef
**Mutable ref object - exactly like React's useRef**

```python
@with_hooks
def InputWithFocus(props):
  inputRef = useRef()
  
  const focusInput = () => {
    if inputRef.current:
      inputRef.current.focus()
  }
  
  return (
    <div>
      <input ref={inputRef} placeholder="Click focus button" />
      <button onClick={focusInput}>Focus Input</button>
      <button onClick={() => {
        if inputRef.current:
          inputRef.current.value = ''
          inputRef.current.focus()
      }}>Clear & Focus</button>
    </div>
  );
```

**Features:**
- ✅ Persistent across re-renders
- ✅ Access DOM elements
- ✅ Store any mutable value
- ✅ No re-renders on change

### useMemo
**Memoized values - exactly like React's useMemo**

```python
@with_hooks
def ExpensiveComponent(props):
  [count, setCount] = useState(0)
  
  expensiveValue = useMemo(() => {
    // This only recalculates when count changes
    result = 0
    for i in range(1000):
      result += i * count
    return result
  }, [count]);  // Dependency array
  
  return (
    <div>
      <h2>Count: {count}</h2>
      <p>Expensive calculation: {expensiveValue}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
```

**Features:**
- ✅ Expensive calculations cached
- ✅ Dependency-based recalculation
- ✅ Performance optimization
- ✅ Reference equality

### useCallback
**Memoized callbacks - exactly like React's useCallback**

```python
@with_hooks
def CallbackComponent(props):
  [count, setCount] = useState(0)
  
  const handleClick = useCallback(() => {
    setCount(prev => prev + 1)
  }, []);  // Empty dependency = stable callback
  
  const handleCustomIncrement = useCallback((step) => {
    setCount(prev => prev + step)
  }, []);  // Stable even with step parameter
  
  return (
    <div>
      <h2>Count: {count}</h2>
      <button onClick={handleClick}>Increment</button>
      <button onClick={() => handleCustomIncrement(5)}>Add 5</button>
    </div>
  );
```

**Features:**
- ✅ Stable function references
- ✅ Prevents unnecessary re-renders
- ✅ Dependency-based recreation
- ✅ Perfect for child component props

## 🎯 Custom Hooks

### useCounter
**Built-in counter functionality**

```python
@with_hooks
def CounterDemo(props):
  [count, increment, decrement] = useCounter(10)  // Initial value = 10
  
  return (
    <div>
      <h2>Counter: {count}</h2>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
    </div>
  );
```

### useToggle
**Built-in toggle functionality**

```python
@with_hooks
def ToggleDemo(props):
  [isVisible, toggle] = useToggle(true)  // Initial value = true
  
  return (
    <div>
      <button onClick={toggle}>
        {isVisible ? 'Hide' : 'Show'} Content
      </button>
      {isVisible && <p>This content can be toggled!</p>}
    </div>
  );
```

### useLocalStorage
**LocalStorage persistence**

```python
@with_hooks
def PersistentForm(props):
  [name, setName] = useLocalStorage('user_name', 'Guest')  // Key, default value
  
  return (
    <div>
      <input 
        value={name} 
        onChange={(e) => setName(e.target.value)}
        placeholder="Your name (saved to localStorage)"
      />
      <p>Hello, {name}!</p>
    </div>
  );
```

### useFetch
**API data fetching**

```python
@with_hooks
def ApiComponent(props):
  data = useFetch('/api/users')  // URL
  
  if data['loading']:
    return <div>Loading...</div>
  
  if data['error']:
    return <div>Error: {data['error']}</div>
  
  return (
    <div>
      <h2>Users:</h2>
      <pre>{data['data']}</pre>
      <button onClick={data['refetch']}>Refetch</button>
    </div>
  );
```

### useDebounce
**Debounced values**

```python
@with_hooks
def SearchComponent(props):
  [searchTerm, setSearchTerm] = useState('')
  debouncedSearch = useDebounce(searchTerm, 500)  // Value, delay in ms
  
  useEffect(() => {
    if debouncedSearch:
      console.log('Searching for:', debouncedSearch)
      // Perform API call here
    }
  }, [debouncedSearch]);
  
  return (
    <div>
      <input 
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="Search (debounced)..."
      />
      <p>Searching for: {debouncedSearch}</p>
    </div>
  );
```

## 🎨 Advanced Patterns

### Multiple State Management
```python
@with_hooks
def ComplexForm(props):
  // Multiple useState hooks
  [formData, setFormData] = useState({'name': '', 'email': ''})
  [errors, setErrors] = useState({})
  [isSubmitting, setIsSubmitting] = useState(false)
  
  // Custom validation hook
  const validateForm = useCallback(() => {
    newErrors = {}
    if not formData['name']:
      newErrors['name'] = 'Name is required'
    if not formData['email']:
      newErrors['email'] = 'Email is required'
    setErrors(newErrors)
    return len(newErrors) === 0
  }, [formData]);
  
  // Submit handler
  const handleSubmit = useCallback(async () => {
    if (!validateForm()) return
    
    setIsSubmitting(true)
    try:
      await submitForm(formData)
    } finally:
      setIsSubmitting(false)
    setFormData({'name': '', 'email': ''})
    setErrors({})
  }, [formData, validateForm]);
  
  return (
    <form onSubmit={handleSubmit}>
      <input 
        value={formData['name']}
        onChange={(e) => setFormData({...formData, 'name': e.target.value})}
        placeholder="Name"
      />
      {errors['name'] && <span className="error">{errors['name']}</span>}
      
      <input 
        value={formData['email']}
        onChange={(e) => setFormData({...formData, 'email': e.target.value})}
        placeholder="Email"
      />
      {errors['email'] && <span className="error">{errors['email']}</span>}
      
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  );
```

### Context + Hooks Combination
```python
from nextpy import createContext, ContextProvider

// Auth context
AuthContext = createContext('auth', {'user': null, 'isAuthenticated': false})

@with_hooks
function AuthenticatedComponent(props):
  auth = useContext(AuthContext)
  [message, setMessage] = useState('')
  
  useEffect(() => {
    if auth['isAuthenticated']:
      setMessage(f'Welcome back, {auth["user"]["name"]}!')
    else:
      setMessage('Please log in')
  }, [auth])
  
  return (
    <div>
      <h2>{message}</h2>
      {auth['isAuthenticated'] && (
        <button onClick={() => logout()}>Logout</button>
      )}
    </div>
  );
}

function App() {
  [authState, setAuthState] = useState({'user': null, 'isAuthenticated': False})
  
  const login = useCallback((user) => {
    setAuthState({'user': user, 'isAuthenticated': True})
  }, []);
  
  const logout = useCallback(() => {
    setAuthState({'user': null, 'isAuthenticated': False})
  }, []);
  
  return (
    <ContextProvider AuthContext={authState}>
      <AuthenticatedComponent />
    </ContextProvider>
  );
}
```

## 🔥 Performance Tips

### 1. Use useMemo for Expensive Calculations
```python
// Bad - recalculates every render
expensiveValue = calculateExpensiveValue(data)

// Good - memoized
expensiveValue = useMemo(() => calculateExpensiveValue(data), [data])
```

### 2. Use useCallback for Stable Functions
```python
// Bad - new function every render
const handleClick = () => setCount(count + 1)

// Good - stable function
const handleClick = useCallback(() => setCount(prev => prev + 1), [])
```

### 3. Split Complex State
```python
// Bad - one large state object
[state, setState] = useState({
  user: null,
  posts: [],
  loading: false,
  error: null
})

// Good - split into logical pieces
[user, setUser] = useState(null)
[posts, setPosts] = useState([])
[loading, setLoading] = useState(false)
[error, setError] = useState(null)
```

### 4. Use useReducer for Complex State Logic
```python
// Bad - complex state updates in useState
const updatePost = (id, updates) => {
  setPosts(prev => prev.map(post => 
    post.id === id ? {...post, ...updates} : post
  ))
}

// Good - useReducer for complex logic
const [state, dispatch] = useReducer(postsReducer, initialState)
dispatch({type: 'UPDATE_POST', id, updates})
```

## 🎯 Best Practices

### ✅ Do's
- Use `@with_hooks` decorator on components that use hooks
- Keep hook calls at the top level of your component
- Use dependency arrays in `useEffect` and `useMemo`
- Use custom hooks for reusable logic
- Use `useCallback` for functions passed to child components

### ❌ Don'ts
- Don't call hooks inside loops or conditions
- Don't call hooks in regular functions (only in component functions)
- Don't mutate state directly (always use setters)
- Don't forget dependencies in useEffect
- Don't over-optimize prematurely

## 📚 Complete Hook Reference

| Hook | Purpose | Returns |
|------|---------|---------|
| `useState` | State management | `[value, setValue]` |
| `useEffect` | Side effects | `void` |
| `useReducer` | Complex state | `[state, dispatch]` |
| `useContext` | Context access | `contextValue` |
| `useRef` | Mutable refs | `{current: value}` |
| `useMemo` | Memoized values | `memoizedValue` |
| `useCallback` | Memoized functions | `memoizedFunction` |
| `useCounter` | Counter logic | `[count, increment, decrement]` |
| `useToggle` | Toggle logic | `[value, toggle]` |
| `useLocalStorage` | LocalStorage | `[value, setValue]` |
| `useFetch` | API calls | `{data, loading, error, refetch}` |
| `useDebounce` | Debounced values | `debouncedValue` |

## 🎉 You're Ready!

**NextPy hooks give you the full React experience in Python!** 

- 🎣 **Same API as React** - No learning curve if you know React
- 🚀 **Full TypeScript support** - Type-safe development
- ⚡ **Performance optimized** - Efficient rendering and state management
- 🧩 **Custom hooks** - Build reusable logic
- 🔄 **Context API** - Global state management
- 📱 **Component lifecycle** - Mount, update, unmount effects

**Start building with hooks today!** 🎯
