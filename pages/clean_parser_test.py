"""
Test the clean PSX parser
"""

@component
def CleanParserTest(props=None):
    """Test component for the clean tokenizer + stack parser"""
    
    count = 42
    items = ["apple", "banana", "cherry"]
    
    return (
       
            <div class="relative min-h-screen pt-0 pb-24 overflow-hidden bg-white place-content-center">
                
                <div class="relative px-4 mx-auto max-w-7xl lg:px-8">
                    <div class="max-w-4xl mx-auto text-center">
                        <h1 class="text-6xl font-extrabold tracking-tight text-black sm:text-8xl animate-fadeIn">
                            Build Your Next Idea <br />
                            <span class="text-transparent bg-clip-text bg-gradient-to-r from-gray-900 via-gray-700 to-gray-500">Faster With Python</span>
                        </h1>
                        
                        <p class="max-w-2xl mx-auto mt-8 text-xl leading-8 text-gray-600">
                            {description}
                        </p>
                        
                        <div class="flex flex-col items-center justify-center mt-12 gap-y-4 sm:flex-row sm:gap-x-6">
                            <a href="/documentation" class="w-full px-8 py-4 text-sm font-bold text-white transition-all bg-black rounded-full shadow-xl sm:w-auto hover:bg-gray-800 shadow-gray-200">
                                Get Started 
                            </a>
                            <a href="/features" class="w-full px-8 py-4 text-sm font-bold text-black transition-all bg-white border border-gray-200 rounded-full sm:w-auto hover:bg-gray-50">
                                Explore Components
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        
    )

def getServerSideProps(context):
    return {
        "props": {
            "title": "Clean Parser Test",
            "description": "Testing the clean PSX parser"
        }
    }

# Default export
default = CleanParserTest
