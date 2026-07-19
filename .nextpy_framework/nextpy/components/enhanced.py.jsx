"""Enhanced NextPy Components with Modern UI"""

def Input(props = None):
    """Enhanced Input component with validation"""
    props = props or {}
    
    name = props.get("name", "")
    type = props.get("type", "text")
    placeholder = props.get("placeholder", "")
    value = props.get("value", "")
    error = props.get("error", "")
    label = props.get("label", "")
    required = props.get("required", False)
    
    
    base_class = "w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
    error_class = "border-red-500 focus:ring-red-500" if error else "border-gray-300"
    
    return (
        <div className="mb-4">
            {label and (
                <label className="block text-sm font-medium text-gray-700 mb-1">
                    {label}
                    {required and <span className="text-red-500 ml-1">*</span>}
                </label>
            )}
            <input 
                type={type}
                name={name}
                placeholder={placeholder}
                value={value}
                className={f"{base_class} {error_class}"}
                required={required}
            />
            {error and (
                <p className="mt-1 text-sm text-red-600">{error}</p>
            )}
        </div>
    )

def Modal(props = None):
    """Modal component with overlay"""
    props = props or {}
    
    isOpen = props.get("isOpen", False)
    title = props.get("title", "Modal")
    children = props.get("children", "")
    onClose = props.get("onClose", None)
    
    if not isOpen:
        return <div></div>
    
    return (
        <div className="fixed inset-0 z-50 overflow-auto bg-black bg-opacity-50 flex items-center justify-center">
            <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
                <div className="flex items-center justify-between p-6 border-b">
                    <h3 className="text-lg font-semibold">{title}</h3>
                    {onClose and (
                        <button 
                            onClick={onClose}
                            className="text-gray-400 hover:text-gray-600"
                        >
                            ✕
                        </button>
                    )}
                </div>
                <div className="p-6">
                    {children}
                </div>
            </div>
        </div>
    )

def LoadingSpinner(props = None):
    """Loading spinner component"""
    props = props or {}
    
    size = props.get("size", "medium")
    color = props.get("color", "blue")
    
    size_classes = {
        "small": "w-4 h-4",
        "medium": "w-8 h-8", 
        "large": "w-12 h-12"
    }
    
    color_classes = {
        "blue": "border-blue-600",
        "white": "border-white",
        "gray": "border-gray-600"
    }
    
    return (
        <div className={f"animate-spin rounded-full border-2 border-t-transparent {size_classes[size]} {color_classes[color]}"}></div>
    )

def Toast(props = None):
    """Toast notification component"""
    props = props or {}
    
    message = props.get("message", "")
    variant = props.get("variant", "info")
    isVisible = props.get("isVisible", False)
    
    if not isVisible:
        return <div></div>
    
    variant_classes = {
        "success": "bg-green-500 text-white",
        "error": "bg-red-500 text-white",
        "warning": "bg-yellow-500 text-black",
        "info": "bg-blue-500 text-white"
    }
    
    return (
        <div className={`fixed bottom-4 right-4 px-6 py-3 rounded-lg shadow-lg ${variant_classes[variant]} z-50`}>
            {message}
        </div>
    )

def DataTable(props = None):
    """Data table component"""
    props = props or {}
    
    data = props.get("data", [])
    columns = props.get("columns", [])
    className = props.get("className", "")
    
    return (
        <div className={`overflow-x-auto ${className}`}>
            <table className="min-w-full bg-white border border-gray-200">
                <thead className="bg-gray-50">
                    <tr>
                        {columns.map(col => (
                            <th key={col['key']} className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                {col['title']}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                    {data.map((row, index) => (
                        <tr key={index}>
                            {columns.map(col => (
                                <td key={col['key']} className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                    {row[col['key']]}
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )

def SearchBar(props = None):
    """Search bar component"""
    props = props or {}
    
    placeholder = props.get("placeholder", "Search...")
    value = props.get("value", "")
    onChange = props.get("onChange", None)
    onSearch = props.get("onSearch", None)
    
    return (
        <div className="relative">
            <input 
                type="text"
                placeholder={placeholder}
                value={value}
                onChange={onChange}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                onKeyPress={(e) => e.key == 'Enter' and onSearch and onSearch()}
            />
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
            </div>
        </div>
    )

def Badge(props = None):
    """Badge component"""
    props = props or {}
    
    text = props.get("text", "")
    variant = props.get("variant", "primary")
    size = props.get("size", "medium")
    
    variant_classes = {
        "primary": "bg-blue-100 text-blue-800",
        "success": "bg-green-100 text-green-800",
        "warning": "bg-yellow-100 text-yellow-800",
        "error": "bg-red-100 text-red-800",
        "gray": "bg-gray-100 text-gray-800"
    }
    
    size_classes = {
        "small": "px-2 py-1 text-xs",
        "medium": "px-2.5 py-1 text-sm",
        "large": "px-3 py-1.5 text-base"
    }
    
    return (
        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full font-medium ${variant_classes[variant]} ${size_classes[size]}`}>
            {text}
        </span>
    )

def Avatar(props = None):
    """Avatar component"""
    props = props or {}
    
    src = props.get("src", "")
    alt = props.get("alt", "")
    size = props.get("size", "medium")
    fallback = props.get("fallback", "?")
    
    size_classes = {
        "small": "w-8 h-8 text-xs",
        "medium": "w-10 h-10 text-sm",
        "large": "w-12 h-12 text-base",
        "xlarge": "w-16 h-16 text-lg"
    }
    
    if src:
        return (
            <img 
                src={src}
                alt={alt}
                className={`inline-block rounded-full ${size_classes[size]}`}
            />
        )
    else:
        return (
            <div className={`inline-flex items-center justify-center rounded-full bg-gray-500 text-white font-medium ${size_classes[size]}`}>
                {fallback}
            </div>
        )

def Tabs(props = None):
    """Tabs component"""
    props = props or {}
    
    tabs = props.get("tabs", [])
    activeTab = props.get("activeTab", "")
    onChange = props.get("onChange", None)
    
    return (
        <div>
            <div className="border-b border-gray-200">
                <nav className="-mb-px flex space-x-8">
                    {tabs.map(tab => (
                        <button
                            key={tab['key']}
                            onClick={() => onChange and onChange(tab['key'])}
                            className={`py-2 px-1 border-b-2 font-medium text-sm ${
                                activeTab === tab['key']
                                    ? 'border-blue-500 text-blue-600'
                                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                            }`}
                        >
                            {tab['label']}
                        </button>
                    ))}
                </nav>
            </div>
            <div className="mt-4">
                {tabs.find(tab => tab['key'] === activeTab)?.get('content', '')}
            </div>
        </div>
    )

def Progress(props = None):
    """Progress bar component"""
    props = props or {}
    
    value = props.get("value", 0)
    max = props.get("max", 100)
    variant = props.get("variant", "primary")
    showLabel = props.get("showLabel", True)
    
    variant_classes = {
        "primary": "bg-blue-600",
        "success": "bg-green-600",
        "warning": "bg-yellow-600",
        "error": "bg-red-600"
    }
    
    percentage = min((value / max) * 100, 100)
    
    return (
        <div>
            {showLabel && (
                <div className="flex justify-between text-sm text-gray-600 mb-1">
                    <span>Progress</span>
                    <span>{percentage:.0f}%</span>
                </div>
            )}
            <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                    className={`h-2 rounded-full ${variant_classes[variant]}`}
                    style={{width: f"{percentage}%"}}
                ></div>
            </div>
        </div>
    )
