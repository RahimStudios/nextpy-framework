"""
Form components for NextPy - Updated for JSX system
Input, TextArea, Select, Checkbox, Radio, Form, etc.
"""

from typing import Optional, List, Dict, Any, Union
from ..jsx import jsx, input, textarea, select, option, button, label, div, form as form_tag


def Input(
    name: str = "",
    type: str = "text",
    placeholder: str = "",
    value: str = "",
    required: bool = False,
    disabled: bool = False,
    class_name: str = "",
    **kwargs
):
    """Input component - returns JSX element"""
    default_class = "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
    props = {
        'type': type,
        'name': name,
        'placeholder': placeholder,
        'value': value,
        'className': class_name or default_class
    }
    
    if required:
        props['required'] = 'True'
    if disabled:
        props['disabled'] = 'True'
    
    return input(props)


def TextArea(
    name: str = "",
    placeholder: str = "",
    value: str = "",
    rows: int = 4,
    required: bool = False,
    disabled: bool = False,
    class_name: str = "",
    **kwargs
):
    """TextArea component - returns JSX element"""
    default_class = "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
    props = {
        'name': name,
        'placeholder': placeholder,
        'rows': rows,
        'className': class_name or default_class
    }
    
    if required:
        props['required'] = True
    if disabled:
        props['disabled'] = True
    
    return textarea(props, value or '')


def Select(
    name: str = "",
    options: List[Dict[str, str]] = None,
    placeholder: str = "Select an option",
    value: str = "",
    required: bool = False,
    disabled: bool = False,
    class_name: str = "",
    **kwargs
):
    """Select component - returns JSX element"""
    if options is None:
        options = []
    
    default_class = "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
    props = {
        'name': name,
        'className': class_name or default_class
    }
    
    if required:
        props['required'] = True
    if disabled:
        props['disabled'] = True
    
    children = []
    if placeholder:
        children.append(option({'value': ''}, placeholder))
    
    for opt in options:
        opt_props = {'value': opt.get('value', opt.get('label', ''))}
        if opt.get('value') == value:
            opt_props['selected'] = True
        children.append(option(opt_props, opt.get('label', '')))
    
    return select(props, *children)


def Checkbox(
    name: str = "",
    label: str = "",
    checked: bool = False,
    required: bool = False,
    disabled: bool = False,
    class_name: str = "",
    **kwargs
):
    """Checkbox component - returns JSX element"""
    input_class = "h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
    label_class = "ml-2 block text-sm text-gray-900"
    
    input_props = {
        'type': 'checkbox',
        'name': name,
        'className': class_name or input_class
    }
    
    if checked:
        input_props['checked'] = True
    if required:
        input_props['required'] = True
    if disabled:
        input_props['disabled'] = True
    
    return div({'className': 'flex items-center'},
        input(input_props),
        label({'className': label_class}, label)
    )


def Radio(
    name: str = "",
    label: str = "",
    value: str = "",
    checked: bool = False,
    required: bool = False,
    disabled: bool = False,
    class_name: str = "",
    **kwargs
):
    """Radio component - returns JSX element"""
    input_class = "h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
    label_class = "ml-2 block text-sm text-gray-900"
    
    input_props = {
        'type': 'radio',
        'name': name,
        'value': value,
        'className': class_name or input_class
    }
    
    if checked:
        input_props['checked'] = True
    if required:
        input_props['required'] = True
    if disabled:
        input_props['disabled'] = True
    
    return div({'className': 'flex items-center'},
        input(input_props),
        label({'className': label_class}, label)
    )


def RadioGroup(
    name: str = "",
    options: List[Dict[str, str]] = None,
    value: str = "",
    required: bool = False,
    disabled: bool = False,
    class_name: str = "",
    **kwargs
):
    """RadioGroup component - returns JSX element"""
    if options is None:
        options = []
    
    container_class = "space-y-2"
    radios = []
    
    for opt in options:
        opt_value = opt.get('value', opt.get('label', ''))
        radios.append(Radio(
            name=name,
            label=opt.get('label', ''),
            value=opt_value,
            checked=opt_value == value,
            required=required,
            disabled=disabled
        ))
    
    return div({'className': class_name or container_class}, *radios)


def Form(
    action: str = "",
    method: str = "POST",
    children: List = None,
    class_name: str = "",
    **kwargs
):
    """Form component - returns JSX element"""
    if children is None:
        children = []
    
    default_class = "space-y-6"
    props = {
        'action': action,
        'method': method,
        'className': class_name or default_class
    }
    
    return form_tag(props, *children)


def FormGroup(
    label: str = "",
    children: List = None,
    error: str = "",
    required: bool = False,
    class_name: str = "",
    **kwargs
):
    """FormGroup component - returns JSX element"""
    if children is None:
        children = []
    
    container_class = "space-y-2"
    label_class = "block text-sm font-medium text-gray-700"
    error_class = "text-red-600 text-sm mt-1"
    
    content = []
    if label:
        label_text = label + (" *" if required else "")
        content.append(label({'className': label_class}, label_text))
    
    content.extend(children)
    
    if error:
        content.append(div({'className': error_class}, error))
    
    return div({'className': class_name or container_class}, *content)


def FileInput(
    name: str = "",
    accept: str = "",
    multiple: bool = False,
    required: bool = False,
    disabled: bool = False,
    class_name: str = "",
    **kwargs
):
    """FileInput component - returns JSX element"""
    input_class = "block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
    
    props = {
        'type': 'file',
        'name': name,
        'className': class_name or input_class
    }
    
    if accept:
        props['accept'] = accept
    if multiple:
        props['multiple'] = True
    if required:
        props['required'] = True
    if disabled:
        props['disabled'] = True
    
    return input(props)


def NumberInput(
    name: str = "",
    placeholder: str = "",
    value: Union[int, float] = "",
    min: Union[int, float] = None,
    max: Union[int, float] = None,
    step: Union[int, float] = 1,
    required: bool = False,
    disabled: bool = False,
    class_name: str = "",
    **kwargs
):
    """NumberInput component - returns JSX element"""
    default_class = "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
    props = {
        'type': 'number',
        'name': name,
        'placeholder': placeholder,
        'value': str(value),
        'className': class_name or default_class
    }
    
    if min is not None:
        props['min'] = min
    if max is not None:
        props['max'] = max
    if step is not None:
        props['step'] = step
    if required:
        props['required'] = True
    if disabled:
        props['disabled'] = True
    
    return input(props)


def DateInput(
    name: str = "",
    value: str = "",
    required: bool = False,
    disabled: bool = False,
    class_name: str = "",
    **kwargs
):
    """DateInput component - returns JSX element"""
    default_class = "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
    props = {
        'type': 'date',
        'name': name,
        'value': value,
        'className': class_name or default_class
    }
    
    if required:
        props['required'] = True
    if disabled:
        props['disabled'] = True
    
    return input(props)


def TimeInput(
    name: str = "",
    value: str = "",
    required: bool = False,
    disabled: bool = False,
    class_name: str = "",
    **kwargs
):
    """TimeInput component - returns JSX element"""
    default_class = "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
    props = {
        'type': 'time',
        'name': name,
        'value': value,
        'className': class_name or default_class
    }
    
    if required:
        props['required'] = True
    if disabled:
        props['disabled'] = True
    
    return input(props)


def PasswordInput(
    name: str = "",
    placeholder: str = "",
    value: str = "",
    required: bool = False,
    disabled: bool = False,
    class_name: str = "",
    **kwargs
):
    """PasswordInput component - returns JSX element"""
    default_class = "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
    props = {
        'type': 'password',
        'name': name,
        'placeholder': placeholder,
        'value': value,
        'className': class_name or default_class
    }
    
    if required:
        props['required'] = True
    if disabled:
        props['disabled'] = True
    
    return input(props)


def RangeInput(
    name: str = "",
    value: Union[int, float] = 0,
    min: Union[int, float] = 0,
    max: Union[int, float] = 100,
    step: Union[int, float] = 1,
    required: bool = False,
    disabled: bool = False,
    class_name: str = "",
    **kwargs
):
    """RangeInput component - returns JSX element"""
    default_class = "w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
    props = {
        'type': 'range',
        'name': name,
        'value': str(value),
        'min': min,
        'max': max,
        'step': step,
        'className': class_name or default_class
    }
    
    if required:
        props['required'] = True
    if disabled:
        props['disabled'] = True
    
    return input(props)


def ColorInput(
    name: str = "",
    value: str = "#000000",
    required: bool = False,
    disabled: bool = False,
    class_name: str = "",
    **kwargs
):
    """ColorInput component - returns JSX element"""
    default_class = "h-10 w-20 border border-gray-300 rounded cursor-pointer"
    props = {
        'type': 'color',
        'name': name,
        'value': value,
        'className': class_name or default_class
    }
    
    if required:
        props['required'] = True
    if disabled:
        props['disabled'] = True
    
    return input(props)


def SubmitButton(
    text: str = "Submit",
    loading: bool = False,
    disabled: bool = False,
    class_name: str = "",
    **kwargs
):
    """SubmitButton component - returns JSX element"""
    default_class = "w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
    
    props = {
        'type': 'submit',
        'className': class_name or default_class
    }
    
    if disabled or loading:
        props['disabled'] = True
    
    button_text = "Loading..." if loading else text
    
    return button(props, button_text)
