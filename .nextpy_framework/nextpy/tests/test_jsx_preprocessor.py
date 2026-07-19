import pytest

from nextpy.jsx_preprocessor import JSXPreprocessor, JSXSyntaxError

pre = JSXPreprocessor()


def normalize(s: str) -> str:
    # strip leading/trailing whitespace and collapse newlines for easier comparison
    return "\n".join(line.rstrip() for line in s.strip().splitlines())


def test_simple_div_transformation():
    src = """def Comp():
    return (
        <div class=\"foo\">Hello</div>
    )
"""
    out = pre.preprocess_content(src)
    # output may escape quotes with backslashes, normalize for check
    assert 'jsx("<div class=\"foo\">Hello</div>")' in out or 'jsx("<div class=\\"foo\\">Hello</div>")' in out
    assert 'from nextpy.true_jsx import jsx' in out


def test_nested_elements():
    src = """def Comp():
    return (<div><span>Hi</span></div>)
"""
    out = pre.preprocess_content(src)
    assert 'jsx("<div><span>Hi</span></div>")' in out


def test_self_closing_tag():
    src = """def Comp():
    return (<img src=\"/img.png\" />)
"""
    out = pre.preprocess_content(src)
    assert 'jsx("<img src=\"/img.png\" />")' in out or 'jsx("<img src=\\"/img.png\\" />")' in out


def test_attributes_with_braces():
    # braces should be preserved inside JSX string
    src = """def Comp():
    return (<div>{value}</div>)
"""
    out = pre.preprocess_content(src)
    assert '{value}' in out


def test_unclosed_tag_raises_error():
    src = """def Comp():
    return (<div><span></div>)
"""
    with pytest.raises(JSXSyntaxError) as excinfo:
        pre.preprocess_content(src)
    msg = str(excinfo.value)
    assert "Unclosed" in msg or "Malformed JSX" in msg


def test_invalid_block_does_nothing():
    # if no JSX tags are present the preprocessor should leave content untouched
    src = """def Comp():
    return (div>oops</div>)
"""
    out = pre.preprocess_content(src)
    assert "div>oops" in out
