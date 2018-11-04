# -*- coding: utf-8 -*-
import os

import pytest

from configureme import helpers

pytestmark = pytest.mark.unit

BOOLEAN_MAP = helpers.BOOLEAN_STATES
POSSIBLE_BOOLEANS = BOOLEAN_MAP.keys()
NON_BOOLEANS = ["1.0", "1", "foobar"]

INTEGER_MAP = {"-1": -1, "0": 0, "1": 1}
POSSIBLE_INTEGERS = INTEGER_MAP.keys()
NON_INTEGERS = ["1.0", "hello", "true"]

FLOAT_MAP = {"-1.0": -1.0, "0.0": 0.0, "1.0": 1.0, "1.2345": 1.2345}
POSSIBLE_FLOATS = FLOAT_MAP.keys()
NON_FLOATS = ["0", "-1", "1", "foobar", "true"]

TYPE_MAP = {**BOOLEAN_MAP, **INTEGER_MAP, **FLOAT_MAP}


def test_is_boolean_state():
    for boolean in POSSIBLE_BOOLEANS:
        assert helpers.is_boolean_state(boolean)

    for non_boolean in NON_BOOLEANS:
        assert not helpers.is_boolean_state(non_boolean)


def test_is_integer():
    for integer in POSSIBLE_INTEGERS:
        assert helpers.is_integer(integer)

    for non_integer in NON_INTEGERS:
        assert not helpers.is_integer(non_integer)


def test_is_float():
    for a_float in POSSIBLE_FLOATS:
        assert helpers.is_float(a_float)

    for non_float in NON_FLOATS:
        assert not helpers.is_float(non_float)


def test_get_integer():
    for int_str, expected_value in INTEGER_MAP.items():
        assert helpers.get_integer(int_str) == expected_value

    for non_integer in NON_INTEGERS:
        with pytest.raises(ValueError):
            helpers.get_integer(non_integer)


def test_get_float():
    for float_str, expected_value in FLOAT_MAP.items():
        assert helpers.get_float(float_str) == expected_value

    for non_float in NON_FLOATS:
        with pytest.raises(ValueError):
            helpers.get_float(non_float)


def test_get_boolean():
    for bool_str, expected_value in BOOLEAN_MAP.items():
        assert helpers.get_boolean(bool_str) == expected_value

    for non_bool in NON_BOOLEANS:
        with pytest.raises(ValueError):
            helpers.get_boolean(non_bool)


def test_str_to_py():
    for actual_value, expected_value in TYPE_MAP.items():
        assert helpers.str_to_py(actual_value) == expected_value


def test_dotenv_to_dict(env_path):
    expected = {
        "DEBUG": True,
        "MAX_LINES": 10,
        "TEMPERATURE": 98.2,
        "TRICKY": "This is a string with = sign",
        "FOO": "1.0 starts with float",
        "BAR": "Has newline \\n",
    }
    actual = helpers.dotenv_to_dict(env_path)
    assert actual == expected


def test_get_envar_that_doesnt_exist():
    assert helpers.get_envar("BLAH") is None


def test_get_envar_that_does_exist():
    os.environ["FOO"] = "true"
    assert helpers.get_envar("FOO") is True
    del os.environ["FOO"]


def test_envar_exists_is_false_when_no_var_exists():
    assert helpers.envar_exists("BLAH") is False


def test_envar_exists_is_true_when_env_var_exists():
    os.environ["FOO"] = "true"
    assert helpers.envar_exists("FOO") is True
    del os.environ["FOO"]
