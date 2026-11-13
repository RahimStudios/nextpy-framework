from nextpy.psx import psx, component, register_component
from datetime import datetime


@component
def ApiAndDeployment(props):
    return psx("""
        <section id="api-and-deployment" class="space-y-6">
            <div class="pb-3 border-b border-gray-800">
                <h2 class="text-2xl font-bold text-gray-100">API Routes and Deployment</h2>
                <p class="mt-2 text-gray-400">
                    Build backend endpoints and ship your app with the same framework you use for UI development.
                </p>
            </div>

            <div class="grid gap-6 lg:grid-cols-2">
                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">API routes</h3>
                    <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400"># pages/api/health.py
                        
                        async def get(request, params):
                            
                            return {
                                "status": "healthy",
                                "timestamp": datetime.now().isoformat(),
                                "version": "1.0.0",
                                "framework": "NextPy"
                                }
                            

                    </pre>
                </div>

                <div class="p-6 border border-gray-700 rounded-2xl bg-gray-900">
                    <h3 class="font-semibold text-gray-100">Deployment checklist</h3>
                    <ul class="pl-5 mt-3 space-y-2 text-sm text-gray-400 list-disc">
                        <li>Set your environment variables</li>
                        <li>Use a production-ready WSGI or ASGI entrypoint</li>
                        <li>Deploy to Render, Railway, Docker, or your hosting platform of choice</li>
                    </ul>
                </div>
            </div>

            <div class="p-6 border border-gray-700 rounded-2xl bg-gray-800">
                <h3 class="font-semibold text-gray-100">Production commands</h3>
                <pre class="p-4 mt-4 overflow-x-auto text-sm bg-gray-950 rounded-lg text-emerald-400">nextpy build
nextpy dev</pre>
            </div>
        </section>
   """)
    
def getServerSideProps(context):
    return {
        "props": {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "framework": "NextPy"
                            
        }
    }
