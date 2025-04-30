"""Automation runtime for Cognyx BOM SDK."""

import base64
import inspect
from collections.abc import Awaitable, Callable
from typing import Any

import dill
from typing_extensions import TypedDict


class ExecutionResult(TypedDict):
    """Result of code execution."""

    scope: dict[str, dict[str, str]]
    result: dict[str, Any]
    success: bool
    error: str | None


def serialize(value: Any) -> str:  # noqa: ANN401
    """Serialize a value to a string."""
    try:
        return base64.b64encode(dill.dumps(value)).decode("utf-8")
    except Exception:
        return "<unable to serialize>"


def deserialize(value: str) -> Any:  # noqa: ANN401
    """Deserialize a string to a value."""
    try:
        return dill.loads(base64.b64decode(value.encode("utf-8")))
    except Exception:
        return "<unable to deserialize>"


def extract_scope(namespace: dict, global_variables: dict, global_ignore: list[str]) -> dict:
    """Extract scope information from a namespace."""
    filtered_vars = {}
    for name, value in namespace.items():
        # Skip globals that are loaded in pyodide
        if name in global_ignore:
            continue

        # Skip names that start with underscore (internal/private)
        if name.startswith("_"):
            continue

        # Skip modules and built-in functions
        if inspect.ismodule(value) or inspect.isbuiltin(value):
            continue

        # Determine the type of each variable
        var_type = type(value).__name__

        # For classes, get their methods and attributes
        if inspect.isclass(value) or inspect.isfunction(value):
            try:
                filtered_vars[name] = {"type": "serialized", "value": serialize(value)}
            except Exception:
                filtered_vars[name] = {"type": var_type, "value": "<unable to represent>"}
        else:
            # Try to get a string representation, but handle potential errors
            try:
                filtered_vars[name] = {"type": "primitive", "value": value}
            except Exception:
                filtered_vars[name] = {"type": var_type, "value": "<unable to represent>"}

    for name, value in global_variables.items():
        filtered_vars[name] = value

    return filtered_vars


async def execute_code(
    code: str,
    eval_async: Callable[[str, dict[str, Any]], Awaitable[dict[str, Any]]],
    global_variables: dict[str, dict[str, str]],
    global_ignore: list[str],
    scope: dict[str, Any],
) -> ExecutionResult:
    """Execute code and capture the result and scope."""
    global_scope = scope

    for name, value in global_variables.items():
        if name in global_ignore:
            continue
        match value["type"]:
            case "serialized":
                global_scope[name] = deserialize(value["value"])
            case _:
                global_scope[name] = value["value"]

    # Use eval_code_async to evaluate the code and capture the last expression
    result = await eval_async(code, global_scope)

    # Extract the scope information
    scope_info = extract_scope(
        namespace=global_scope,
        global_variables=global_variables,
        global_ignore=global_ignore,
    )

    # Create the result object
    return {"scope": scope_info, "result": result, "success": True, "error": None}
