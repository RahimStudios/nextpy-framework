from nextpy.psx import interactive_component

@interactive_component
def BlogPost(props=None):
    props = props or {}
    post = props.get("post", {})

    if not post:
        return (
            <div class="flex items-center justify-center min-h-screen bg-gray-50">
                <div class="text-center">
                    <h1 class="mb-4 text-4xl font-bold text-gray-900">Post Not Found</h1>
                    <a href="/blog" class="text-blue-600 hover:underline">Back to blog</a>
                </div>
            </div>
        )

    return (
        <div class="min-h-screen bg-white">
            <article class="max-w-3xl px-4 py-16 mx-auto sm:px-6 lg:px-8">
                <header class="mb-10">
                    <h1 class="text-5xl font-extrabold leading-tight text-gray-900">
                        {post["title"]}
                    </h1>
                    <div class="flex items-center mt-4 text-lg text-gray-500">
                        <span>{post["date"]}</span>
                        <span class="mx-2"></span>
                        <span>{post["author"]}</span>
                    </div>
                </header>
                <div class="prose prose-lg text-gray-800 max-w-none">
                    {post["content"]}
                </div>
                <div class="pt-8 mt-12 border-t">
                    <a href="/blog" class="font-medium text-blue-600 transition-colors hover:text-blue-800">
                        Back to all posts
                    </a>
                </div>
            </article>
        </div>
    )

def getServerSideProps(context):
    slug = context.get("params", {}).get("slug", "")
    
    posts = {
        "hello-world": {
            "slug": "hello-world",
            "title": "Hello World",
            "date": "2025-01-15",
            "author": "Team NextPy",
            "content": "This is the full content of the Hello World post.",
        },
        "why-python-web": {
            "slug": "why-python-web",
            "title": "Why Python for Web Apps",
            "date": "2025-02-20",
            "author": "Jane Doe",
            "content": "Python has evolved far beyond scripting.",
        },
    }

    post = posts.get(slug, {})
    if not post:
        return {"not_found": True}
    return {"props": {"post": post}}

default = BlogPost
