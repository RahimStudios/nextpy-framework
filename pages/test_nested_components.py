from nextpy.psx import interactive_component as component, register_component

@component
def OuterComponent(props=None):
    props = props or {}
    children = props.get("children", [])
    

    
    return (
        <div class="border-2 border-blue-500 p-4">
            <h2 class="text-xl font-bold">Outer Component</h2>
            <div class="mt-2">
                {children}
            </div>
        </div>
    )

@component
def InnerComponent(props=None):
    props = props or {}
    message = props.get("message", "Hello from inner")
   
    
    return (
        <div class="bg-green-100 p-2 rounded">
            <p class="text-green-800">{message}</p>
            
        </div>
    )

@component
def Navbar(props=None):
    props=props or {}
    
    return (
        <nav class="bg-gray-100 p-2 flex space-x-4">
            <a class="text-gray-800 hover:text-gray-600" href="/">Home</a>
            <a class="text-gray-800 hover:text-gray-600" href="/about">About</a>
        </nav>
    )

# Register components globally
register_component("OuterComponent", OuterComponent)
register_component("InnerComponent", InnerComponent)
register_component("Navbar", Navbar)



@component
def Page(props=None):
    props = props or {}
    
    
    
    return (
        <div class="p-8">
            <h1 class="text-2xl font-bold mb-4">Nested Components Test</h1>

            
            <OuterComponent>
                <InnerComponent message="First nested component"/>
                <InnerComponent message="Second nested component"/>
                <Navbar/>
                <p class="text-gray-600">Direct text child</p>
            </OuterComponent>
            
            <div class="mt-4">
                <OuterComponent>
                    <p class="text-gray-600">Direct text child</p>
                </OuterComponent>
            </div>
        </div>
    )

default = Page
