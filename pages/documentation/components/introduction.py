from nextpy.psx import component, psx


@component
def Introduction(props):
    return psx("""
<article class="mx-auto max-w-4xl">

    
    <header class="pb-10 border-b border-gray-800">

        <p class="text-sm font-medium tracking-wide text-blue-400 uppercase">
            NextPy Docs
        </p>

        <h1 class="mt-3 text-4xl font-bold tracking-tight text-white">
            Welcome to the NextPy documentation!
        </h1>

        <p class="mt-6 text-lg leading-8 text-gray-400">
            Learn how to build modern, full-stack web applications with NextPy.
            Whether you're creating your first project or building production-scale
            applications, these guides will help you understand the framework and
            its core concepts.
        </p>

    </header>


    
    <section class="py-12 border-b border-gray-800">

        <h2 class="text-2xl font-semibold tracking-tight text-white">
            What is NextPy?
        </h2>

        <div class="mt-6 space-y-6 text-gray-400 leading-8">

            <p>
                NextPy is a Python framework for building modern full-stack web
                applications. It lets you create interactive user interfaces using
                reusable Python components while providing built-in routing,
                server-side rendering, APIs, state management, and developer tools.
            </p>

            <p>
                Instead of configuring multiple frontend and backend technologies,
                NextPy provides an integrated development experience so you can
                focus on building your application rather than managing tooling.
            </p>

            <p>
                Whether you're an individual developer, startup, or enterprise
                team, NextPy helps you build fast, scalable, and maintainable web
                applications entirely with Python.
            </p>

        </div>

    </section>


    
    <section class="py-12 border-b border-gray-800">

        <h2 class="text-2xl font-semibold tracking-tight text-white">
            How to use the documentation
        </h2>

        <p class="mt-6 text-gray-400 leading-8">
            The documentation is organized into three main sections:
        </p>

        <div class="mt-8 space-y-8">

            <div class="flex gap-4">

                <svg class="mt-1 h-5 w-5 flex-shrink-0 text-gray-500"
                     fill="none"
                     stroke="currentColor"
                     stroke-width="2"
                     viewBox="0 0 24 24">

                    <path stroke-linecap="round"
                          stroke-linejoin="round"
                          d="M12 6v12M6 12h12"/>
                </svg>

                <div>

                    <h3 class="font-medium text-white">
                        Getting Started
                    </h3>

                    <p class="mt-1 text-gray-400">
                        Learn how to install NextPy, create your first application,
                        and understand the framework's core concepts.
                    </p>

                </div>

            </div>


            <div class="flex gap-4">

                <svg class="mt-1 h-5 w-5 flex-shrink-0 text-gray-500"
                     fill="none"
                     stroke="currentColor"
                     stroke-width="2"
                     viewBox="0 0 24 24">

                    <path stroke-linecap="round"
                          stroke-linejoin="round"
                          d="M9 5l7 7-7 7"/>
                </svg>

                <div>

                    <h3 class="font-medium text-white">
                        Guides
                    </h3>

                    <p class="mt-1 text-gray-400">
                        Explore routing, components, state management,
                        deployment, authentication, databases, and more.
                    </p>

                </div>

            </div>


            <div class="flex gap-4">

                <svg class="mt-1 h-5 w-5 flex-shrink-0 text-gray-500"
                     fill="none"
                     stroke="currentColor"
                     stroke-width="2"
                     viewBox="0 0 24 24">

                    <path stroke-linecap="round"
                          stroke-linejoin="round"
                          d="M8 7h8M8 12h8M8 17h5"/>
                </svg>

                <div>

                    <h3 class="font-medium text-white">
                        API Reference
                    </h3>

                    <p class="mt-1 text-gray-400">
                        Detailed technical documentation for every NextPy module,
                        component, decorator, and CLI command.
                    </p>

                </div>

            </div>

        </div>

        <p class="mt-8 text-gray-400 leading-8">
            Use the navigation sidebar to browse each section, or use the
            documentation search to quickly find specific topics.
        </p>

    </section>


    
    <section class="py-12">

        <h2 class="text-2xl font-semibold tracking-tight text-white">
            Next Steps
        </h2>

        <p class="mt-6 text-gray-400 leading-8">
            Ready to build your first application? Start with the installation
            guide to create a new NextPy project and learn the framework's
            fundamental concepts.
        </p>

        <div class="mt-8">

            <a href="#installation"
               class="inline-flex items-center gap-2 font-medium text-blue-400 hover:text-blue-300">

                Get Started

                <svg class="h-4 w-4"
                     fill="none"
                     stroke="currentColor"
                     stroke-width="2"
                     viewBox="0 0 24 24">

                    <path stroke-linecap="round"
                          stroke-linejoin="round"
                          d="M9 5l7 7-7 7"/>

                </svg>

            </a>

        </div>

    </section>

</article>
""")