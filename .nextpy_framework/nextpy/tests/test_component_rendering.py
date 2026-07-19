import sys
sys.path.insert(0, '.nextpy_framework')
from nextpy.psx import component, psx, useState

# Create a simple test component
@component
def TestComponent(props=None):
    name = props.get('name', 'World') if props else 'World'
    return (
        <div className="test-component">
            <h1>Hello {name}!</h1>
            <p>This is a test component</p>
        </div>
    )

# Test component rendering
print('🔍 Testing Component Rendering:')
print('==============================')

# Test 1: Direct component call
print('✅ Test 1: Direct component call')
try:
    result = TestComponent({'name': 'NextPy'})
    if hasattr(result, 'to_html'):
        html = result.to_html()
        print('✅ HTML output:')
        print(html)
    else:
        print('❌ No to_html method')
except Exception as e:
    print(f'❌ Error: {e}')

# Test 2: Component in PSX with context
print('\n✅ Test 2: Component in PSX with context')
component_jsx = '''<TestComponent name="PSX" />'''

try:
    # Register component in context
    context = {'TestComponent': TestComponent}
    result = psx(component_jsx, context)
    
    if hasattr(result, 'to_html'):
        html = result.to_html()
        print('✅ HTML output:')
        print(html)
        
        if 'Hello PSX!' in html:
            print('🎉 SUCCESS: Component rendering working!')
        else:
            print('❌ Component not rendered correctly')
    else:
        print('❌ No to_html method')
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()

# Test 3: Component with children
print('\n✅ Test 3: Component with children')
component_with_children_jsx = '''<TestComponent name="Nested"><span>Child content</span></TestComponent>'''

try:
    context = {'TestComponent': TestComponent}
    result = psx(component_with_children_jsx, context)
    
    if hasattr(result, 'to_html'):
        html = result.to_html()
        print('✅ HTML output:')
        print(html)
        
        if 'Hello Nested!' in html and 'Child content' in html:
            print('🎉 SUCCESS: Component with children working!')
        else:
            print('❌ Component with children not rendered correctly')
    else:
        print('❌ No to_html method')
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
