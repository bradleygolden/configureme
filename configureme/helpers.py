# -*- coding: utf-8 -*-
from typing import Any, Dict

BOOLEAN_STATES = {"true": True, "false": False, "True": True, "False": False}


def is_boolean_state(value: str) -> bool:
    """Check if a string is 'boolean like'."""
    return value in BOOLEAN_STATES


def is_integer(value: str) -> bool:
    """Check if a value is an integer."""
    try:
        int(value)
        return True
    except ValueError:
        return False


def is_float(value: str) -> bool:
    """Check if a value is a float."""
    if is_integer(value):
        return False
    try:
        float(value)
        return True
    except ValueError:
        return False


def get_integer(value: str) -> int:
    """Get a integer from a value."""
    if is_integer(value):
        return int(value)
    else:
        raise ValueError(f"Not a valid integer. Must be {type(int)}")


def get_float(value: str) -> float:
    """Get a float from a value."""
    if is_float(value):
        return float(value)
    else:
        raise ValueError(f"Not a valid number. Must be {type(float)}")


def get_boolean(value: str) -> bool:
    """Get a boolean from a value."""
    if is_boolean_state(value):
        return BOOLEAN_STATES[value]
    else:
        raise ValueError(f"Not a valid boolean. Must be {type(float)}")


def str_to_py(value: str):
    """Convert an string value to a native python type."""
    rv: Any
    if is_boolean_state(value):
        rv = get_boolean(value)
    elif is_integer(value):
        rv = get_integer(value)
    elif is_float(value):
        rv = get_float(value)
    else:
        rv = value
    return rv


def dotenv_to_dict(path: str) -> Dict[str, Any]:
    """Convert a .env file to a dict."""
    with open(path, "r") as dotenvfile:
        lines = dotenvfile.readlines()

    rv: Dict[str, Any] = dict()
    for line in lines:
        if line.startswith("#"):
            continue
        name, value = line.strip().split("=", 1)
        py_value = str_to_py(value)
        rv[name] = py_value
    return rv
