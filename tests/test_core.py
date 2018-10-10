# -*- coding: utf-8 -*-
import os

import pytest

from configureme import Config

from .config import DevConfig

pytestmark = pytest.mark.unit


def setup_function():
    try:
        del os.environ["FOO"]
    except KeyError:
        pass
    os.environ["FOO"] = "BAR"


def teardown_function():
    try:
        del os.environ["FOO"]
    except KeyError:
        pass


def test_from_object():
    config = Config()
    config.from_object(DevConfig)
    assert "DEBUG" in config
    assert config["DEBUG"] is True


def test_from_dotenv(env_path):
    config = Config()
    config.from_dotenv(env_path)
    assert "DEBUG" in config
    assert config["DEBUG"] is True


def test_from_obj_and_then_dotenv(env_path):
    config = Config()
    config.from_dotenv(env_path)
    config.from_object(DevConfig)
    assert "DEBUG" in config
    assert "TESTING" in config
    assert config["DEBUG"] is True
    assert config["TESTING"] is False


def test_from_envar_that_doesnt_exist_raises_warning():
    config = Config()
    with pytest.warns(RuntimeWarning) as warn:
        config.from_envar("BAR")

    assert len(warn) == 1
    assert "not found" in warn[0].message.args[0]


def test_from_envar_that_doesnt_exist_but_exists_in_config_object():
    config = Config()
    config["BAR"] = "BAZ"
    config.from_envar("BAR")
    assert "BAR" in config
    assert config["BAR"] == "BAZ"


def test_from_envar_and_change_after_setting_value():
    config = Config()
    config.from_envar("FOO")
    assert config["FOO"] == "BAR"
    os.environ["FOO"] = "BAZ"
    assert config["FOO"] == "BAZ"


def test_env_var_is_set_then_gets_removed_without_default_raises_exception():
    config = Config()
    config.from_envar("FOO")
    del os.environ["FOO"]
    with pytest.raises(ValueError):
        config["FOO"]


def test_env_var_is_set_then_gets_removed_with_config_value_set():
    config = Config()
    config.from_object(DevConfig)
    config.from_envar("FOO")
    assert config["FOO"] == "BAR"
    del os.environ["FOO"]
    assert config["FOO"] == "BAZ"


def test_user_can_change_value_manually():
    config = Config()
    config["BAZ"] = "FOO"
    assert config["BAZ"] == "FOO"


def test_user_can_change_value_manually_but_env_value_takes_precedence():
    config = Config()
    config["FOO"] = "BAZ"
    assert config["FOO"] == "BAR"


def test_user_can_use_number_types_with_dotenv(env_path):
    config = Config()
    config.from_dotenv(env_path)
    assert isinstance(config["MAX_LINES"], int)
    assert config["MAX_LINES"] == 10
    assert isinstance(config["TEMPERATURE"], float)
    assert config["TEMPERATURE"] == 98.2


def test_dunder_str():
    expected = "{'DEBUG': True}"
    config = Config()
    config["DEBUG"] = True
    assert str(config) == expected


def test_dunder_eq():
    config_one = Config()
    config_one["DEBUG"] = True

    config_two = Config()
    config_two["DEBUG"] = True

    assert config_one == config_two


def test_dunder_ne():
    config_one = Config()
    config_one["DEBUG"] = True

    config_two = Config()
    config_two["DEBUG"] = False

    assert config_one != config_two


def test_env_var_can_be_renamed():
    try:
        del os.environ["FOO_DEBUG"]
    except KeyError:
        pass
    assert os.getenv("FOO_DEBUG") is None
    os.environ["FOO_DEBUG"] = "true"
    config = Config()
    config.from_envar("FOO_DEBUG", rename="DEBUG")
    assert config["DEBUG"] is True


def test_from_env_var_that_equals_not_found():
    config = Config()
    os.environ["FOO"] = "not found"
    config.from_envar("FOO")
    assert config["FOO"] == "not found"


def test_from_env_var_with_default_value():
    config = Config()
    os.environ["FOO"] = "BAR"
    config.from_envar("FOO", default="BAZ")
    assert config["FOO"] == "BAR"
    del os.environ["FOO"]
    assert config["FOO"] == "BAZ"


def test_from_env_var_with_default_value_and_alias():
    config = Config()
    os.environ["FOO"] = "BAR"
    config.from_envar("FOO", rename="FOOBAR", default="BAZ")
    assert config["FOO"] == "BAR"
    assert config["FOOBAR"] == "BAR"
    del os.environ["FOO"]
    assert config["FOO"] == "BAZ"
    assert config["FOOBAR"] == "BAZ"
