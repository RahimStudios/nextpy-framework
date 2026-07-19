add more built in compo# NextPy Quick Start (5 Minutes)

Get a NextPy app running in 5 minutes with Tailwind CSS.

## 1. Install Python Dependencies (30 seconds)

```bash
pip install nextpy-framework
```

## 2. Create Project & Install Node.js Dependencies (1 minute)

```bash
nextpy create my-blog
cd my-blog

# Initialize npm and install Tailwind CSS dependencies
npm init -y
npm install -D tailwindcss@latest postcss@latest autoprefixer@latest
```

## 3. Configure Tailwind CSS (1 minute)

Create `tailwind.config.js` in your project root:

```javascript
// tailwind.config.js
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './templates/**/*.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

Create `postcss.config.js` in your project root:

```javascript
// postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

Create `styles.css` in your project root:

```css
/* styles.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**Ensure `templates/_base.html` links to the compiled Tailwind CSS:**

```html
<!-- templates/_base.html (excerpt) -->
<head>
  <!-- ... other head elements ... -->
  <link href="/public/tailwind.css" rel="stylesheet">
</head>
```

## 4. Start Server (30 seconds)

```bash
nextpy dev
```

Visit `http://localhost:5000` - your app is live, with Tailwind CSS compiled!

## 5. Create Your First Page (2 minutes)

**Create the page:**
```python
# pages/hello.py

def get_template():
    return "hello.html"

async def get_server_side_props(context):
    return {
        "props": {
            "name": "World",
            "message": "Welcome to NextPy!"
        }
    }
```

**Create the template with Tailwind CSS classes:**
```html
<!-- templates/hello.html -->
{% extends "_base.html" %}

{% block content %}
<div class="max-w-4xl mx-auto py-12 px-4 bg-gray-100 rounded-lg shadow-md">
    <h1 class="text-5xl font-extrabold text-blue-700 mb-4">Hello {{ name }}!</h1>
    <p class="text-xl text-gray-800">{{ message }}</p>
    <button class="mt-6 bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-6 rounded-full shadow-lg transition duration-300 ease-in-out">Get Started</button>
</div>
{% endblock %}
```

**Visit:** `http://localhost:5000/hello` ✨

---

## Next Steps

### Explore Components
```html
{% from "components/button.html" import button %}
{% from "components/card.html" import card %}

{{ button("Click Me", "/action", "primary") }}
{{ card(title="My Card", content="Description") }}
```

### Create API Endpoints
```python
# pages/api/hello.py

async def get(request):
    return {"message": "Hello from API!"}

async def post(request):
    data = await request.json()
    return {"received": data}
```

Visit: `http://localhost:5000/api/hello`

### Build for Production
```bash
nextpy build    # Generate static files (includes purged Tailwind CSS)
nextpy start    # Start production server
```

---

## Learn More

- **Full Guide**: See `DOCUMENTATION.md` for in-depth information.
- **Examples**: Visit `/examples` in your development server for UI component showcases and more.
- **GitHub**: https://github.com/IBRAHIMFONYUY/nextpy-framework

---

## Troubleshooting

**Port 5000 already in use?**
```bash
nextpy dev --port 3000
```

**Hot reload not working?**
```bash
pip install --upgrade watchdog
```

**Template not found?**
Check the filename in `templates/` matches `get_template()` return value.

**Tailwind CSS not applying?**
Refer to the comprehensive troubleshooting section in `DOCUMENTATION.md`.

---

Happy coding! 🚀
