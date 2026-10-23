"""Focused tests for PSX client reactivity metadata extraction."""

import sys
sys.path.insert(0, './.nextpy_framework')

from nextpy.psx.components.component import useState, useEffect
from nextpy.psx.hydration.decorators import (
    _extract_state_and_derived,
    _extract_client_effects,
)
from nextpy.psx.compiler.actions import compile_handler_to_actions


def _sample_component(props=None):
    [count, setCount] = useState(0)
    [theme, setTheme] = useState("light")
    bg = "bg-gray-900 text-white" if theme == "dark" else "bg-white text-gray-900"
    useEffect(lambda: setCount(count + 1), [count])
    useEffect(lambda: setTheme("dark"), [])
    return None


def test_extracts_state_and_derived_expressions():
    state_keys, derived = _extract_state_and_derived(_sample_component)
    assert state_keys == ["count", "theme"]
    assert "bg" in derived
    assert "if theme == 'dark'" in derived["bg"]


def test_extracts_client_effects_with_deps():
    effects = _extract_client_effects(_sample_component)
    assert len(effects) == 2
    assert effects[0]["deps"] == ["count"]
    assert effects[1]["deps"] == []
    assert effects[0]["actions"][0]["type"] == "SET_STATE"


def test_compiles_python_ternary_to_conditional_action():
    actions = compile_handler_to_actions(
        "lambda e: setTheme('dark' if theme == 'light' else 'light')",
        "toggle_theme",
    )
    assert actions[0]["type"] == "SET_STATE"
    value = actions[0]["data"]["value"]
    assert value["type"] == "CONDITIONAL"
    assert value["data"]["then"]["data"]["value"] == "dark"


def test_compiles_not_operator():
    actions = compile_handler_to_actions("lambda e: setShow(not show)", "toggle_show")
    value = actions[0]["data"]["value"]
    assert value["type"] == "UNARY_OP"
    assert value["data"]["op"] in ("!", "not")
