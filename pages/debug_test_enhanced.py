"""
Test page for enhanced NextPy debug panel with Next.js-style error handling
"""

@component
def Home(props=None):
    """Home component with debug panel testing"""
    props = props or {}
    
    return (
        <div class="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white p-8">
            <div class="max-w-4xl mx-auto">
                <h1 class="text-4xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
                    Enhanced NextPy Debug Panel
                </h1>
                
                <div class="mb-8">
                    <h2 class="text-2xl font-semibold mb-4">Next.js-Style Debug Experience</h2>
                    <p class="text-gray-300 mb-6">
                        This page demonstrates the enhanced debug panel with Next.js-inspired error handling and modern design.
                    </p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                    <div class="bg-gray-800 rounded-lg p-6 border border-gray-700">
                        <h3 class="text-xl font-semibold mb-4 text-blue-400">✅ Features Added</h3>
                        <ul class="space-y-2 text-gray-300">
                            <li>• Next.js-style error overlay</li>
                            <li>• Enhanced error capture & reporting</li>
                            <li>• Modern visual design with gradients</li>
                            <li>• Fixed JavaScript function definitions</li>
                            <li>• Improved performance metrics</li>
                            <li>• Better console log handling</li>
                        </ul>
                    </div>
                    
                    <div class="bg-gray-800 rounded-lg p-6 border border-gray-700">
                        <h3 class="text-xl font-semibold mb-4 text-green-400">🎨 Visual Enhancements</h3>
                        <ul class="space-y-2 text-gray-300">
                            <li>• Animated gradient headers</li>
                            <li>• Backdrop blur effects</li>
                            <li>• Hover animations</li>
                            <li>• Modern button styling</li>
                            <li>• Enhanced typography</li>
                            <li>• Responsive design</li>
                        </ul>
                    </div>
                </div>

                <div class="bg-gray-800 rounded-lg p-6 border border-gray-700 mb-8">
                    <h3 class="text-xl font-semibold mb-4 text-yellow-400">🧪 Test Debug Features</h3>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <button 
                            onclick="testConsoleError()"
                            class="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg transition-colors"
                        >
                            Test Console Error
                        </button>
                        <button 
                            onclick="testWarning()"
                            class="bg-yellow-600 hover:bg-yellow-700 px-4 py-2 rounded-lg transition-colors"
                        >
                            Test Warning
                        </button>
                        <button 
                            onclick="testRuntimeError()"
                            class="bg-orange-600 hover:bg-orange-700 px-4 py-2 rounded-lg transition-colors"
                        >
                            Test Runtime Error
                        </button>
                        <button 
                            onclick="testUnhandledPromise()"
                            class="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg transition-colors"
                        >
                            Test Promise Rejection
                        </button>
                        <button 
                            onclick="testUndefinedError()"
                            class="bg-pink-600 hover:bg-pink-700 px-4 py-2 rounded-lg transition-colors"
                        >
                            Test Undefined Error
                        </button>
                        <button 
                            onclick="clearTests()"
                            class="bg-gray-600 hover:bg-gray-700 px-4 py-2 rounded-lg transition-colors"
                        >
                            Clear Tests
                        </button>
                    </div>
                </div>

                <div class="bg-gray-800 rounded-lg p-6 border border-gray-700">
                    <h3 class="text-xl font-semibold mb-4 text-cyan-400">📊 Debug Panel Info</h3>
                    <div class="text-gray-300 space-y-2">
                        <p>The debug panel should appear in the bottom-right corner with the following enhancements:</p>
                        <ul class="list-disc list-inside space-y-1 ml-4">
                            <li>Modern gradient design with blur effects</li>
                            <li>Enhanced error overlay similar to Next.js</li>
                            <li>Better error tracking and badge notifications</li>
                            <li>Improved performance metrics display</li>
                            <li>Smooth animations and hover effects</li>
                        </ul>
                        <p class="mt-4 text-sm text-gray-400">
                            Click the debug icon (NP) in the bottom-right corner to open the enhanced debug panel.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    )

def getServerSideProps(context):
    return {
        "props": {
            "title": "Enhanced Debug Panel Test",
            "debug_enabled": True
        }
    }

# Test functions for debug panel
TEST_SCRIPTS = """
<script>
    function testConsoleError() {
        console.error('This is a test console error from the debug panel test page');
    }
    
    function testWarning() {
        console.warn('This is a test warning message');
    }
    
    function testRuntimeError() {
        try {
            undefinedVariable.someMethod();
        } catch (error) {
            console.error('Runtime error caught:', error.message);
        }
    }
    
    function testUnhandledPromise() {
        Promise.reject('This is an unhandled promise rejection for testing');
    }
    
    function testUndefinedError() {
        // This should trigger the "True is not defined" style error
        someUndefinedFunction();
    }
    
    function clearTests() {
        console.clear();
        console.log('Debug tests cleared');
    }
</script>
"""

# Default export
default = Home
