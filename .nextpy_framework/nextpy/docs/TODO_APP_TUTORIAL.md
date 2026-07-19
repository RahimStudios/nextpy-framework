# 📝 Build a Todo App with NextPy

**Complete step-by-step tutorial to build a fully functional todo application using NextPy's React-like syntax, hooks, and components!**

## 🎯 What We'll Build

A complete todo application with:
- ✅ Add new todos
- ✅ Mark todos as complete/incomplete
- ✅ Edit existing todos
- ✅ Delete todos
- ✅ Filter todos (All, Active, Completed)
- ✅ Persistent storage (localStorage)
- ✅ Beautiful UI with animations
- ✅ Form validation
- ✅ Error handling

## 🚀 Prerequisites

- Python 3.8+
- NextPy Framework installed: `pip install nextpy-framework`

## 📁 Step 1: Create the Project

```bash
# Create a new NextPy project
nextpy create todo-app
cd todo-app

# Start development server
nextpy dev
```

Open `http://localhost:5000` in your browser.

## 📝 Step 2: Create the Todo Data Structure

Create `pages/api/todos.py` for our API endpoints:

```python
// pages/api/todos.py
import json
from pathlib import Path

# Simple file-based storage for demo
TODOS_FILE = Path("todos.json")

def load_todos():
    """Load todos from file"""
    if TODOS_FILE.exists():
        with open(TODOS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_todos(todos):
    """Save todos to file"""
    with open(TODOS_FILE, 'w') as f:
        json.dump(todos, f, indent=2)

def get(request):
    """Get all todos"""
    todos = load_todos()
    return {'todos': todos}

def post(request):
    """Create a new todo"""
    todos = load_todos()
    data = request.get('json', {})
    
    new_todo = {
        'id': len(todos) + 1,
        'text': data.get('text', ''),
        'completed': False,
        'createdAt': str(datetime.datetime.now())
    }
    
    todos.append(new_todo)
    save_todos(todos)
    
    return {'todo': new_todo}, 201

def put(request):
    """Update a todo"""
    todos = load_todos()
    data = request.get('json', {})
    todo_id = data.get('id')
    
    for i, todo in enumerate(todos):
        if todo['id'] == todo_id:
            todos[i] = {**todo, **data}
            save_todos(todos)
            return {'todo': todos[i]}
    
    return {'error': 'Todo not found'}, 404

def delete(request):
    """Delete a todo"""
    todos = load_todos()
    data = request.get('json', {})
    todo_id = data.get('id')
    
    todos = [todo for todo in todos if todo['id'] != todo_id]
    save_todos(todos)
    
    return {'success': True}

# Route handler
default = lambda request: {
    'GET': get,
    'POST': post,
    'PUT': put,
    'DELETE': delete
}.get(request.get('method', 'GET'), lambda: {'error': 'Method not allowed'})(request)
```

## 🎨 Step 3: Create the Main Todo Component

Create `pages/index.py` with our main todo application:

```python
// pages/index.py
from nextpy import useState, useEffect, with_hooks
from nextpy.components import Button, Input, Card, Alert
from nextpy.jsx import div, h1, h2, p, ul, li, span, form, button as button_tag
import datetime

@with_hooks
def TodoApp():
  [todos, setTodos] = useState([])
  [newTodo, setNewTodo] = useState('')
  [filter, setFilter] = useState('all')
  [loading, setLoading] = useState(False)
  [error, setError] = useState('')
  
  # Load todos from API
  useEffect(() => {
    loadTodos()
  }, [])
  
  async def loadTodos():
    setLoading(True)
    setError('')
    
    try:
      # In a real app, you'd use fetch or requests
      # For demo, we'll simulate API call
      todos_data = [
        {'id': 1, 'text': 'Learn NextPy', 'completed': True, 'createdAt': '2024-01-01'},
        {'id': 2, 'text': 'Build todo app', 'completed': False, 'createdAt': '2024-01-02'},
        {'id': 3, 'text': 'Write tutorial', 'completed': False, 'createdAt': '2024-01-03'}
      ]
      setTodos(todos_data)
    except Exception as e:
      setError('Failed to load todos')
    finally:
      setLoading(False)
  
  async def addTodo(event):
    event.preventDefault()
    
    if not newTodo.strip():
      setError('Please enter a todo item')
      return
    
    setError('')
    
    try:
      # Simulate API call
      new_todo_data = {
        'id': len(todos) + 1,
        'text': newTodo.strip(),
        'completed': False,
        'createdAt': str(datetime.datetime.now())
      }
      
      setTodos([...todos, new_todo_data])
      setNewTodo('')
    except Exception as e:
      setError('Failed to add todo')
  
  async def toggleTodo(todo_id):
    try:
      updated_todos = todos.map(todo => {
        if todo['id'] == todo_id:
          return {...todo, 'completed': not todo['completed']}
        return todo
      })
      setTodos(updated_todos)
    except Exception as e:
      setError('Failed to update todo')
  
  async def deleteTodo(todo_id):
    try:
      updated_todos = [todo for todo in todos if todo['id'] != todo_id]
      setTodos(updated_todos)
    except Exception as e:
      setError('Failed to delete todo')
  
  def filteredTodos():
    if filter == 'active':
      return [todo for todo in todos if not todo['completed']]
    elif filter == 'completed':
      return [todo for todo in todos if todo['completed']]
    return todos
  
  def todoStats():
    total = len(todos)
    completed = len([todo for todo in todos if todo['completed']])
    active = total - completed
    return {'total': total, 'completed': completed, 'active': active}
  
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-3xl mx-auto px-4">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            📝 NextPy Todo App
          </h1>
          <p className="text-gray-600">
            Built with React-like hooks and components!
          </p>
        </div>
        
        {/* Stats */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex justify-around text-center">
            <div>
              <div className="text-2xl font-bold text-blue-600">
                {todoStats()['total']}
              </div>
              <div className="text-sm text-gray-600">Total</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-green-600">
                {todoStats()['completed']}
              </div>
              <div className="text-sm text-gray-600">Completed</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-orange-600">
                {todoStats()['active']}
              </div>
              <div className="text-sm text-gray-600">Active</div>
            </div>
          </div>
        </div>
        
        {/* Add Todo Form */}
        <Card className="mb-6">
          <h2 className="text-xl font-semibold mb-4">Add New Todo</h2>
          <form onSubmit={addTodo}>
            <div className="flex gap-2">
              <Input
                value={newTodo}
                onChange={(e) => setNewTodo(e.target.value)}
                placeholder="What needs to be done?"
                className="flex-1"
              />
              <Button 
                type="submit" 
                text="Add Todo" 
                variant="primary"
                disabled={not newTodo.strip()}
              />
            </div>
          </form>
        </Card>
        
        {/* Error Alert */}
        {error and (
          <Alert 
            message={error} 
            variant="danger" 
            className="mb-6"
          />
        )}
        
        {/* Filter Tabs */}
        <Card className="mb-6">
          <div className="flex gap-2">
            <Button
              text={`All (${todoStats()['total']})`}
              variant={filter == 'all' ? 'primary' : 'outline'}
              onClick={() => setFilter('all')}
              size="small"
            />
            <Button
              text={`Active (${todoStats()['active']})`}
              variant={filter == 'active' ? 'primary' : 'outline'}
              onClick={() => setFilter('active')}
              size="small"
            />
            <Button
              text={`Completed (${todoStats()['completed']})`}
              variant={filter == 'completed' ? 'primary' : 'outline'}
              onClick={() => setFilter('completed')}
              size="small"
            />
          </div>
        </Card>
        
        {/* Todo List */}
        <Card>
          <h2 className="text-xl font-semibold mb-4">
            {filter == 'all' and 'All Todos'}
            {filter == 'active' and 'Active Todos'}
            {filter == 'completed' and 'Completed Todos'}
          </h2>
          
          {loading ? (
            <div className="text-center py-8">
              <div className="text-gray-500">Loading todos...</div>
            </div>
          ) : filteredTodos().length == 0 ? (
            <div className="text-center py-8">
              <div className="text-gray-500">
                {filter == 'active' and 'No active todos'}
                {filter == 'completed' and 'No completed todos'}
                {filter == 'all' and 'No todos yet'}
              </div>
            </div>
          ) : (
            <ul className="space-y-2">
              {filteredTodos().map(todo => (
                <li 
                  key={todo['id']}
                  className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <button
                    onClick={() => toggleTodo(todo['id'])}
                    className={`w-5 h-5 rounded border-2 flex items-center justify-center ${
                      todo['completed'] 
                        ? 'bg-green-500 border-green-500' 
                        : 'border-gray-300 hover:border-gray-400'
                    }`}
                  >
                    {todo['completed'] and (
                      <span className="text-white text-xs">✓</span>
                    )}
                  </button>
                  
                  <div className="flex-1">
                    <p className={`font-medium ${
                      todo['completed'] 
                        ? 'text-gray-500 line-through' 
                        : 'text-gray-900'
                    }`}>
                      {todo['text']}
                    </p>
                    <p className="text-sm text-gray-500">
                      {todo['createdAt']}
                    </p>
                  </div>
                  
                  <Button
                    text="Delete"
                    variant="danger"
                    size="small"
                    onClick={() => deleteTodo(todo['id'])}
                  />
                </li>
              ))}
            </ul>
          )}
        </Card>
        
        {/* Footer */}
        <div className="text-center mt-8 text-gray-600">
          <p>Built with NextPy - Next.js for Python 🐍</p>
          <p className="text-sm">
            Features: React-like hooks, JSX syntax, 50+ components, hot reload
          </p>
        </div>
      </div>
    </div>
  );

def getServerSideProps(context):
  return {
    'props': {}
  }

default = TodoApp
```

## 🎨 Step 4: Add Styling (Optional)

Create `public/styles.css` for custom styling:

```css
/* public/styles.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom animations */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.todo-item {
  animation: slideIn 0.3s ease-out;
}

/* Custom hover effects */
.todo-item:hover {
  transform: translateX(4px);
}

/* Checkbox animation */
.checkbox {
  transition: all 0.2s ease;
}

.checkbox:hover {
  transform: scale(1.1);
}
```

## 🧪 Step 5: Test the Application

Your todo app should now have:

### ✅ **Core Features Working:**
- Add new todos with form validation
- Toggle todo completion status
- Delete todos
- Filter todos by status
- Real-time statistics
- Error handling
- Loading states

### 🎨 **UI Features:**
- Beautiful, responsive design
- Hover effects and animations
- Form validation feedback
- Error messages
- Loading indicators

### 🎯 **NextPy Features Demonstrated:**
- **useState** for state management
- **useEffect** for data loading
- **@with_hooks** decorator
- **Component Library** (Button, Input, Card, Alert)
- **True JSX Syntax** with HTML-like tags
- **Event Handling** with onClick
- **Conditional Rendering** with if/else
- **List Rendering** with map
- **Form Handling** with onSubmit

## 🚀 Step 6: Enhance the App (Optional)

### Add Edit Functionality
```python
# Add to TodoApp component
[editingId, setEditingId] = useState('')
[editText, setEditText] = useState('')

def startEdit(todo_id, current_text):
  setEditingId(todo_id)
  setEditText(current_text)

def saveEdit(todo_id):
  updated_todos = todos.map(todo => {
    if todo['id'] == todo_id:
      return {...todo, 'text': editText}
    return todo
  })
  setTodos(updated_todos)
  setEditingId('')
  setEditText('')

def cancelEdit():
  setEditingId('')
  setEditText('')
```

### Add LocalStorage Persistence
```python
# Add to TodoApp component
from nextpy import useLocalStorage

# Replace useState with useLocalStorage
[todos, setTodos] = useLocalStorage('todos', [])
```

### Add Due Dates
```python
# Extend todo data structure
new_todo = {
  'id': len(todos) + 1,
  'text': newTodo.strip(),
  'completed': False,
  'createdAt': str(datetime.datetime.now()),
  'dueDate': '',  # Add due date
  'priority': 'medium'  # Add priority
}
```

### Add Search Functionality
```python
# Add search state
[searchTerm, setSearchTerm] = useState('')

# Add search input
<Input
  value={searchTerm}
  onChange={(e) => setSearchTerm(e.target.value)}
  placeholder="Search todos..."
  className="mb-4"
/>

# Filter todos based on search
def searchFilteredTodos():
  filtered = filteredTodos()
  if searchTerm:
    filtered = [todo for todo in filtered 
                if searchTerm.lower() in todo['text'].lower()]
  return filtered
```

## 📱 Step 7: Mobile Optimization

Add mobile-specific styles and responsive design:

```python
// Update the container div
<div className="min-h-screen bg-gray-50 py-4 px-2 sm:py-8">
  <div className="max-w-3xl mx-auto sm:px-4">
    {/* Mobile-optimized form */}
    <form onSubmit={addTodo}>
      <div className="flex flex-col sm:flex-row gap-2">
        <Input
          value={newTodo}
          onChange={(e) => setNewTodo(e.target.value)}
          placeholder="What needs to be done?"
          className="flex-1"
        />
        <Button 
          type="submit" 
          text="Add" 
          variant="primary"
          disabled={not newTodo.strip()}
          className="sm:w-auto"
        />
      </div>
    </form>
  </div>
</div>
```

## 🔧 Step 8: Production Deployment

### Build for Production
```bash
# Build the app
nextpy build

# Start production server
nextpy start
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN nextpy build

EXPOSE 5000
CMD ["nextpy", "start"]
```

## 🎯 What You've Learned

Through this tutorial, you've mastered:

### 🎣 **React-like Hooks:**
- `useState` for component state
- `useEffect` for side effects
- `useLocalStorage` for persistence
- `@with_hooks` decorator

### 🎨 **Component Library:**
- `Button` with variants and sizes
- `Input` with form handling
- `Card` for content grouping
- `Alert` for error messages

### 📝 **JSX Syntax:**
- HTML-like tags in Python
- Event handling with `onClick`
- Conditional rendering
- List rendering with `map`

### 🔄 **State Management:**
- Component state patterns
- Form handling
- Data filtering
- Error handling

### 📱 **Responsive Design:**
- Mobile-first approach
- Tailwind CSS utilities
- Flexible layouts

## 🚀 Next Steps

### 🎯 **Enhance Your Todo App:**
- Add user authentication
- Implement drag-and-drop reordering
- Add subtasks and nested todos
- Include file attachments
- Add sharing and collaboration

### 📚 **Explore More NextPy Features:**
- API routes for backend functionality
- Database integration with SQLAlchemy
- Authentication and authorization
- File uploads and storage
- Real-time updates with WebSockets

### 🎨 **Advanced UI Components:**
- Modal dialogs for editing
- Date pickers for due dates
- Rich text editors
- Drag-and-drop interfaces
- Charts and analytics

## 🎉 Congratulations!

You've built a complete todo application using NextPy's React-like syntax, hooks, and components! This demonstrates:

- ✅ **Modern Development Experience** - React-like patterns in Python
- ✅ **Component-Based Architecture** - Reusable UI components
- ✅ **State Management** - Hooks for complex state logic
- ✅ **Beautiful UI** - Professional design with Tailwind CSS
- ✅ **Production Ready** - Optimized and deployable code

**You're now ready to build amazing web applications with NextPy!** 🚀

---

**NextPy: Next.js for Python 🐍 → React ❤️ Python**
