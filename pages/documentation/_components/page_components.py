from nextpy.psx import component, psx


@component
def TutorialHeader(props):
    """Header for tutorial pages with time estimate and difficulty"""
    title = props.get("title", "")
    description = props.get("description", "")
    time_estimate = props.get("time_estimate", "")
    difficulty = props.get("difficulty", "beginner")
    version = props.get("version", "5.0.0")
    
    difficulty_colors = {
        "beginner": "bg-green-500/20 text-green-400 border-green-500",
        "intermediate": "bg-yellow-500/20 text-yellow-400 border-yellow-500",
        "advanced": "bg-red-500/20 text-red-400 border-red-500"
    }
    
    return psx(f"""
        <div class="mb-8 pb-6 border-b border-gray-800">
            <div class="flex items-center gap-3 mb-4">
                <span class="px-2 py-1 text-xs font-medium border rounded bg-blue-500/20 text-blue-400 border-blue-500">
                    Tutorial
                </span>
                <span class="px-2 py-1 text-xs font-medium border rounded {difficulty_colors.get(difficulty, difficulty_colors['beginner'])}">
                    {difficulty.capitalize()}
                </span>
                <span class="px-2 py-1 text-xs font-medium border rounded bg-gray-700 text-gray-300 border-gray-600">
                    NextPy {version}
                </span>
                <span class="ml-auto text-sm text-gray-400">
                    ⏱ {time_estimate}
                </span>
            </div>
            
            <h1 class="text-4xl font-bold text-white">
                {title}
            </h1>
            
            <p class="mt-4 text-lg text-gray-400">
                {description}
            </p>
        </div>
    """)


@component
def HowToHeader(props):
    """Header for how-to guide pages"""
    title = props.get("title", "")
    description = props.get("description", "")
    tags = props.get("tags", [])
    version = props.get("version", "5.0.0")
    
    return psx(f"""
        <div class="mb-8 pb-6 border-b border-gray-800">
            <div class="flex items-center gap-3 mb-4">
                <span class="px-2 py-1 text-xs font-medium border rounded bg-green-500/20 text-green-400 border-green-500">
                    How-to Guide
                </span>
                <span class="px-2 py-1 text-xs font-medium border rounded bg-gray-700 text-gray-300 border-gray-600">
                    NextPy {version}
                </span>
                {for tag in tags:
                    <span class="px-2 py-1 text-xs font-medium border rounded bg-purple-500/20 text-purple-400 border-purple-500">
                        {tag}
                    </span>
                }
            </div>
            
            <h1 class="text-4xl font-bold text-white">
                {title}
            </h1>
            
            <p class="mt-4 text-lg text-gray-400">
                {description}
            </p>
        </div>
    """)


@component
def ExplanationHeader(props):
    """Header for explanation pages"""
    title = props.get("title", "")
    description = props.get("description", "")
    version = props.get("version", "5.0.0")
    
    return psx(f"""
        <div class="mb-8 pb-6 border-b border-gray-800">
            <div class="flex items-center gap-3 mb-4">
                <span class="px-2 py-1 text-xs font-medium border rounded bg-purple-500/20 text-purple-400 border-purple-500">
                    Explanation
                </span>
                <span class="px-2 py-1 text-xs font-medium border rounded bg-gray-700 text-gray-300 border-gray-600">
                    NextPy {version}
                </span>
            </div>
            
            <h1 class="text-4xl font-bold text-white">
                {title}
            </h1>
            
            <p class="mt-4 text-lg text-gray-400">
                {description}
            </p>
        </div>
    """)


@component
def ReferenceHeader(props):
    """Header for reference pages"""
    title = props.get("title", "")
    description = props.get("description", "")
    version = props.get("version", "5.0.0")
    
    return psx(f"""
        <div class="mb-8 pb-6 border-b border-gray-800">
            <div class="flex items-center gap-3 mb-4">
                <span class="px-2 py-1 text-xs font-medium border rounded bg-orange-500/20 text-orange-400 border-orange-500">
                    Reference
                </span>
                <span class="px-2 py-1 text-xs font-medium border rounded bg-gray-700 text-gray-300 border-gray-600">
                    NextPy {version}
                </span>
            </div>
            
            <h1 class="text-4xl font-bold text-white">
                {title}
            </h1>
            
            <p class="mt-4 text-lg text-gray-400">
                {description}
            </p>
        </div>
    """)


@component
def PageContent(props):
    """Main content wrapper with page-level formatting"""
    children = props.get("children")
    
    return psx(f"""
        <article class="prose prose-invert prose-gray max-w-none">
            {children}
        </article>
    """)


@component
def Section(props):
    """Section wrapper with auto-generated ID"""
    id = props.get("id", "")
    title = props.get("title", "")
    children = props.get("children")
    
    return psx(f"""
        <section id="{id}" class="my-12 scroll-mt-20">
            <h2 class="text-3xl font-bold text-white mb-6">
                {title}
            </h2>
            {children}
        </section>
    """)


@component
def SubSection(props):
    """Sub-section wrapper"""
    id = props.get("id", "")
    title = props.get("title", "")
    children = props.get("children")
    
    return psx(f"""
        <div id="{id}" class="my-8 scroll-mt-20">
            <h3 class="text-2xl font-semibold text-white mb-4">
                {title}
            </h3>
            {children}
        </div>
    """)
