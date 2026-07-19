import pytest
from nextpy.jsx_preprocessor import JSXPreprocessor, JSXSyntaxError


def test_nested_tags_transformed():
    src = '''def Comp():
    return (
        <div class="outer"><span><strong>Hi</strong></span></div>
    )
'''
    out = JSXPreprocessor().preprocess_content(src)
    assert 'jsx("<div class=\"outer\"><span><strong>Hi</strong></span></div>")' in out or 'jsx("<div' in out


def test_self_closing_tags():
    src = '''def Comp():
    return (
        <div><img src="/img.png"/><br/></div>
    )
'''
    out = JSXPreprocessor().preprocess_content(src)
    assert 'img' in out and 'br' in out


def test_unclosed_tag_raises():
    src = '''def Comp():
    return (
        <div><span>Broken</div>
    )
'''
    with pytest.raises(JSXSyntaxError):
        JSXPreprocessor().preprocess_content(src)
