#!/usr/bin/env python3
"""
Debug Patch class attributes
"""

import sys
import os

# Add the framework root to path
framework_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, framework_root)

from nextpy.psx.vdom.vnode import Patch

print("Patch class attributes:")
for attr in dir(Patch):
    if not attr.startswith('_'):
        print(f"  - {attr}")

print("\nPatch dataclass fields:")
import dataclasses
print(dataclasses.fields(Patch))
