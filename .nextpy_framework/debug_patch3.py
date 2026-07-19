#!/usr/bin/env python3
"""
Debug Patch class more thoroughly
"""

import sys
import os

# Add the framework root to path
framework_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, framework_root)

from nextpy.psx.vdom.vnode import Patch
import dataclasses

print("Patch class info:")
print(f"Class: {Patch}")
print(f"Is dataclass: {dataclasses.is_dataclass(Patch)}")

if dataclasses.is_dataclass(Patch):
    fields = dataclasses.fields(Patch)
    print(f"Fields: {[f.name for f in fields]}")
    
    # Create a test patch
    test_patch = Patch(
        type="test",
        old_vnode=None,
        new_vnode=None,
        path=[],
        data={}
    )
    
    print(f"Test patch: {test_patch}")
    print(f"Test patch dir: {[attr for attr in dir(test_patch) if not attr.startswith('_')]}")
    
    # Check attributes on instance
    attributes = ['type', 'old_vnode', 'new_vnode', 'path', 'data']
    for attr in attributes:
        has_attr = hasattr(test_patch, attr)
        print(f"  {attr}: {has_attr}")
        if has_attr:
            value = getattr(test_patch, attr)
            print(f"    value: {value}")
