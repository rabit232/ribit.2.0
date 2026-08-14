"""Static validation for inert Python template proposals; never imports or runs them."""

from __future__ import annotations

import ast


class TemplateValidationError(ValueError):
    """Raised when a proposed Python template exceeds the inert subset."""


_ALLOWED_MODULE_NODES = (ast.FunctionDef, ast.Expr)
_ALLOWED_FUNCTION_NODES = (ast.Expr, ast.Pass, ast.Return, ast.Raise)


def validate_python_template(source: str) -> None:
    try:
        tree = ast.parse(source, mode="exec")
    except SyntaxError as exc:
        raise TemplateValidationError("Template is not valid Python syntax.") from exc
    for item in tree.body:
        if not isinstance(item, _ALLOWED_MODULE_NODES):
            raise TemplateValidationError("Only a module docstring and inert function stubs are allowed.")
        if isinstance(item, ast.Expr):
            if not isinstance(item.value, ast.Constant) or not isinstance(item.value.value, str):
                raise TemplateValidationError("Only a module docstring expression is allowed.")
            continue
        if item.decorator_list or item.returns is not None or item.type_params:
            raise TemplateValidationError("Decorators, return annotations, and type parameters are not allowed.")
        if item.args.vararg or item.args.kwarg or item.args.kwonlyargs or item.args.defaults or item.args.kw_defaults:
            raise TemplateValidationError("Only simple named parameters are allowed.")
        for arg in (*item.args.posonlyargs, *item.args.args):
            if arg.annotation is not None:
                raise TemplateValidationError("Parameter annotations are not allowed in review templates.")
        for statement in item.body:
            if not isinstance(statement, _ALLOWED_FUNCTION_NODES):
                raise TemplateValidationError("Function bodies may contain only a docstring, pass, literal return, or NotImplementedError.")
            if isinstance(statement, ast.Expr):
                if not isinstance(statement.value, ast.Constant) or not isinstance(statement.value.value, str):
                    raise TemplateValidationError("Only function docstrings are allowed as expressions.")
            elif isinstance(statement, ast.Return):
                if statement.value is not None and not isinstance(statement.value, ast.Constant):
                    raise TemplateValidationError("Return values must be literal constants.")
            elif isinstance(statement, ast.Raise):
                exception = statement.exc
                is_bare_name = isinstance(exception, ast.Name) and exception.id == "NotImplementedError"
                is_empty_call = (
                    isinstance(exception, ast.Call)
                    and isinstance(exception.func, ast.Name)
                    and exception.func.id == "NotImplementedError"
                    and not exception.args
                    and not exception.keywords
                )
                if not (is_bare_name or is_empty_call):
                    raise TemplateValidationError("Only bare NotImplementedError may be raised by a stub.")
