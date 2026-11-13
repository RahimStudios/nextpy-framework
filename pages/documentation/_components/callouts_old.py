from nextpy.psx import component, psx


@component
def InfoCallout(props):
    """Info callout box for general information"""
    title = props.get("title", "Note")
    children = props.get("children")
    
    return psx(f"""
        <div class="my-6 p-4 border-l-4 border-blue-500 bg-blue-900/20 rounded-r-lg">
            <div class="flex items-start gap-3">
                <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-blue-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div class="flex-1">
                    <h4 class="font-semibold text-blue-400">{title}</h4>
                    <div class="mt-1 text-sm text-gray-300">
                        {children}
                    </div>
                </div>
            </div>
        </div>
    """)


@component
def WarningCallout(props):
    """Warning callout box for common pitfalls and breaking changes"""
    title = props.get("title", "Warning")
    children = props.get("children")
    
    return psx(f"""
        <div class="my-6 p-4 border-l-4 border-yellow-500 bg-yellow-900/20 rounded-r-lg">
            <div class="flex items-start gap-3">
                <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-yellow-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <div class="flex-1">
                    <h4 class="font-semibold text-yellow-400">{title}</h4>
                    <div class="mt-1 text-sm text-gray-300">
                        {children}
                    </div>
                </div>
            </div>
        </div>
    """)


@component
def ErrorCallout(props):
    """Error callout box for critical issues and security concerns"""
    title = props.get("title", "Error")
    children = props.get("children")
    
    return psx(f"""
        <div class="my-6 p-4 border-l-4 border-red-500 bg-red-900/20 rounded-r-lg">
            <div class="flex items-start gap-3">
                <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-red-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 10h6v4H9z" />
                </svg>
                <div class="flex-1">
                    <h4 class="font-semibold text-red-400">{title}</h4>
                    <div class="mt-1 text-sm text-gray-300">
                        {children}
                    </div>
                </div>
            </div>
        </div>
    """)


@component
def SuccessCallout(props):
    """Success callout box for achievements and successful outcomes"""
    title = props.get("title", "Success")
    children = props.get("children")
    
    return psx(f"""
        <div class="my-6 p-4 border-l-4 border-green-500 bg-green-900/20 rounded-r-lg">
            <div class="flex items-start gap-3">
                <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-green-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div class="flex-1">
                    <h4 class="font-semibold text-green-400">{title}</h4>
                    <div class="mt-1 text-sm text-gray-300">
                        {children}
                    </div>
                </div>
            </div>
        </div>
    """)


@component
def TipCallout(props):
    """Tip callout box for helpful suggestions and best practices"""
    title = props.get("title", "Tip")
    children = props.get("children")
    
    return psx(f"""
        <div class="my-6 p-4 border-l-4 border-purple-500 bg-purple-900/20 rounded-r-lg">
            <div class="flex items-start gap-3">
                <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-purple-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                <div class="flex-1">
                    <h4 class="font-semibold text-purple-400">{title}</h4>
                    <div class="mt-1 text-sm text-gray-300">
                        {children}
                    </div>
                </div>
            </div>
        </div>
    """)


@component
def PrerequisiteCallout(props):
    """Prerequisite callout box showing what's needed before starting"""
    prerequisites = props.get("prerequisites", [])
    
    return psx(f"""
        <div class="my-6 p-4 border border-gray-700 bg-gray-800 rounded-lg">
            <div class="flex items-start gap-3">
                <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-gray-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
                <div class="flex-1">
                    <h4 class="font-semibold text-gray-200">Prerequisites</h4>
                    <ul class="mt-2 space-y-1 text-sm text-gray-400">
                        {for prereq in prerequisites:
                            <li class="flex items-center gap-2">
                                <svg class="w-3 h-3 text-green-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                                </svg>
                                {prereq}
                            </li>
                        }
                    </ul>
                </div>
            </div>
        </div>
    """)


@component
def CommonMistakeCallout(props):
    """Common mistake callout showing frequent errors"""
    mistake = props.get("mistake", "")
    solution = props.get("solution", "")
    
    return psx(f"""
        <div class="my-6 p-4 border-l-4 border-orange-500 bg-orange-900/20 rounded-r-lg">
            <div class="flex items-start gap-3">
                <svg class="mt-0.5 h-5 w-5 flex-shrink-0 text-orange-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <div class="flex-1">
                    <h4 class="font-semibold text-orange-400">Common Mistake</h4>
                    <div class="mt-2 space-y-2 text-sm">
                        <div>
                            <span class="text-red-400 font-medium">❌ Don't:</span>
                            <code class="ml-2 px-2 py-1 bg-red-900/30 rounded text-red-300">{mistake}</code>
                        </div>
                        <div>
                            <span class="text-green-400 font-medium">✅ Do:</span>
                            <code class="ml-2 px-2 py-1 bg-green-900/30 rounded text-green-300">{solution}</code>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    """)
