from nextpy.psx import interactive_component, psx, useState

@interactive_component
def Input(props):
    props=props or {}
    [bindname, setBindName] = useState("")
    name=props.get('name', '')
    label=props.get('label', '')
    type=props.get('type', '')
    value=props.get('value', '')
    placeholder=props.get('placeholder')
    required=props.get('required', '')
    required_tag=''
    
    if required=='True':
        required_tag="""<span class="text-red-500">*</span>"""
        required_app="required"
    else:
        required_tag=""
        required_app=""
   
          
            
        
    
    
    return psx(f"""
               <div class="mb-4 ">
               
                    <label for="{name}" class="block mb-1 text-sm font-medium text-gray-700">
                        { label }
                        { required_tag}
                        
                    </label>
                    <input 
                        type="{type}" 
                        id="{name }" 
                        name="{name }" 
                        value="{ value}"
                        placeholder="{placeholder}"
                        {required_app}
                        class="w-full px-4 py-2 transition-all border border-gray-300 rounded-lg outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    >
                    </div>
               """)