#!/usr/bin/env python3
"""
Debug Patch attributes specifically
"""

import sys
import os

# Add the framework root to path
framework_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, framework_root)

from nextpy.psx.vdom.vnode import Patch

print("Checking Patch attributes:")
attributes = ['type', 'old_vnode', 'new_vnode', 'path', 'data']
for attr in attributes:
    has_attr = hasattr(Patch, attr)
    print(f"  {attr}: {has_attr}")

print(f"\nAll attributes present: {all(hasattr(Patch, attr) for attr in attributes)}")
