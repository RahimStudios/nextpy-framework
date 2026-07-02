---
name: Evaluator eager to_html bug
description: Root cause and fix for {children} rendering as garbled JS in layout.psx
---

## The rule
`SafeExpressionEngine._evaluate_node` (evaluator.py) must return PSX/component objects as-is — it must NOT call `.to_html()` on them.

**Why:** If the evaluator calls `obj.to_html()` eagerly, it converts the object to an HTML+`<script>` string. That string flows into `process_python_logic` as a plain `str`, gets substituted into the PSX template, and the template re-parses the `<script>` block — creating ExpressionNodes from every `{...}` pattern inside the JavaScript, causing a cascade of "expression evaluation failed" runtime errors.

**How to apply:** Whenever a `Name` node resolves to a value with `to_html`, return the value itself. The rendering pipeline (`PSXRuntime._render_node`) checks `hasattr(result, 'to_html')` and calls it at the correct time. Similarly, `process_python_logic` (runtime.py) must `continue` (skip substitution) for any evaluated value that has `to_html`.
