"""Login page"""
from nextpy.psx import interactive_component, register_component, useState
from pages.components.forms import Input


register_component('Input', Input)



@interactive_component
def LoginPage(props):
    props= props or {}
    title=props.get('title', "Login")
    
    return(
        
        <div class="max-w-md px-4 py-16 mx-auto">
            <div class="p-8 bg-white rounded-lg shadow-lg">
                <h1 class="mb-6 text-3xl font-bold text-center">{title}</h1>
                
                <form id="loginForm" class="space-y-4" method='POST'>
                    <Input name="username" label="username" type="text"  placeholder="your username" required=True/>
                    <Input name="password" label="password" type="password"  placeholder="your password" required=True/>
                    
                    <button type="submit" class="w-full px-4 py-2 text-white bg-blue-600 rounded hover:bg-blue-700">Sign In</button>
                </form>
                
                <p class="mt-4 text-center text-gray-600">Demo: email@example.com / password</p>
            </div>
        </div>
    )
    


async def get_server_side_props(context):
    return {"props": {"title": "Login"}}

default=LoginPage
