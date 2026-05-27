#!/usr/bin/env python3
"""
TEST: Handler Extraction
Test if extract_create_handler_assignments works
"""

import sys
sys.path.insert(0, '/home/ibrahim-fonyuy/Downloads/NextPyVision (1)/NextPyVision/.nextpy_framework')

from nextpy.psx.hydration.decorators import extract_create_handler_assignments
from nextpy.psx import create_onclick, useState

from nextpy.psx.hydration import interactive_component

@interactive_component
def test_func():
    [count, setCount] = useState(0)
    handleIncrement = create_onclick(lambda e: setCount(count + 1))
    return "test"

handlers = extract_create_handler_assignments(test_func)

print("Handlers found:", handlers)