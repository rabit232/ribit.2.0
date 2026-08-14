"""Render a narrowly constrained, inert Python stub as review text."""

from __future__ import annotations

import re

_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]{0,63}$")


def render_stub(module_purpose: str, function_name: str, parameters: tuple[str, ...] = ()) -> str:
    if not module_purpose.strip() or not _IDENTIFIER.fullmatch(function_name):
        raise ValueError("Purpose and function name must be valid review-template values.")
    if any(not _IDENTIFIER.fullmatch(parameter) for parameter in parameters):
        raise ValueError("Template parameters must be simple identifiers.")
    joined = ", ".join(parameters)
    return (
        f'"""Review-only stub: {module_purpose.strip()}"""\n\n'
        f"def {function_name}({joined}):\n"
        '    """Inert template; requires manual implementation review."""\n'
        "    raise NotImplementedError\n"
    )
