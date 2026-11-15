"""MCP Server — animation playground."""

from nextpy.psx import component
from pages._anim.registry import page_for

_inner = page_for("mcp-server")


@component
def Page(props=None):
    props = props or {}
    return _inner(props)
