#!/usr/bin/env python3
"""PSX HTML attribute support test"""

import os
import sys

psx_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, psx_root)

from core import PSXCore


def test_html_attribute_rendering():
    core = PSXCore()

    psx_str = '''
    <>
        <button className="px-4 py-2 bg-blue-600 text-white rounded" aria-label="Submit form" disabled>
            Submit
        </button>
        <svg xmlns:xlink="http://www.w3.org/1999/xlink" class="w-6 h-6" viewBox="0 0 24 24">
            <use xlink:href="#icon-arrow" />
        </svg>
    </>
    '''

    html = core.parse_and_render(psx_str)

    assert 'class="px-4 py-2 bg-blue-600 text-white rounded"' in html
    assert 'aria-label="Submit form"' in html
    assert 'disabled' in html
    assert 'className' not in html
    assert 'xlink:href="#icon-arrow"' in html
    assert 'xmlns:xlink="http://www.w3.org/1999/xlink"' in html
    assert '<use xlink:href="#icon-arrow" />' in html


if __name__ == '__main__':
    test_html_attribute_rendering()
    print('✅ PSX HTML attribute support test passed!')
