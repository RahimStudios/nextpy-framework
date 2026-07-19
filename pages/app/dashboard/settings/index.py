# Settings Page
from nextpy.psx import component

@component
def Page(props=None):
    return (
        <div>
            <h1 class="text-2xl font-bold mb-4">Settings</h1>
            <p class="text-gray-600">Manage your account settings here.</p>
            
            <div class="mt-6 space-y-4">
                <div class="bg-white p-4 rounded shadow">
                    <h2 class="font-bold">Profile Settings</h2>
                    <p>Update your profile information</p>
                </div>
                
                <div class="bg-white p-4 rounded shadow">
                    <h2 class="font-bold">Security Settings</h2>
                    <p>Manage your password and security</p>
                </div>
            </div>
        </div>
    )

default = Page
