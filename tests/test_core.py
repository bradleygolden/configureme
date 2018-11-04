# -*- coding: utf-8 -*-
import os

import pytest

from configureme import Config

from .config import DevConfig

pytestmark = pytest.mark.unit


class TestConfig:
    def test_from_object(self):
        config = Config()
        config.from_object(DevConfig)
        assert "DEBUG" in config
        assert config["DEBUG"] is True

    def test_from_dotenv(self, env_path):
        config = Config()
        config.from_dotenv(env_path)
        assert "DEBUG" in config
        assert config["DEBUG"] is True

    def test_from_obj_and_then_dotenv(self, env_path):
        config = Config()
        config.from_dotenv(env_path)
        config.from_object(DevConfig)
        assert "DEBUG" in config
        assert "TESTING" in config
        assert config["DEBUG"] is True
        assert config["TESTING"] is False

    def test_from_envar_that_doesnt_exist_raises_warning(self):
        config = Config()
        with pytest.warns(RuntimeWarning) as warn:
            config.from_envar("BAR")

        assert len(warn) == 1
        assert "not found" in warn[0].message.args[0]

    def test_from_envar_that_doesnt_exist_but_exists_in_config_object(self):
        config = Config()
        config["BAR"] = "BAZ"
        config.from_envar("BAR")
        assert "BAR" in config
        assert config["BAR"] == "BAZ"

    def test_from_envar_and_change_after_setting_value(self):
        os.environ["FOO"] = "BAR"
        config = Config()
        config.from_envar("FOO")
        assert config["FOO"] == "BAR"
        os.environ["FOO"] = "BAZ"
        assert config["FOO"] == "BAZ"
        del os.environ["FOO"]

    def test_env_var_is_set_then_gets_removed_without_default_raises_exception(self):
        os.environ["FOO"] = "BAR"
        config = Config()
        config.from_envar("FOO")
        del os.environ["FOO"]
        with pytest.raises(KeyError):
            config["FOO"]

    def test_env_var_is_set_then_gets_removed_with_config_value_set(self):
        os.environ["FOO"] = "BAR"
        config = Config()
        config.from_object(DevConfig)
        config.from_envar("FOO")
        assert config["FOO"] == "BAR"
        del os.environ["FOO"]
        assert config["FOO"] == "BAZ"

    def test_user_can_change_value_manually(self):
        config = Config()
        config["BAZ"] = "FOO"
        assert config["BAZ"] == "FOO"

    def test_user_can_change_value_manually_but_env_value_takes_precedence(self):
        os.environ["FOO"] = "expected"
        config = Config()
        config["FOO"] = "not expected"
        config.from_envar("FOO")
        assert config["FOO"] == "expected"

    def test_user_can_use_number_types_with_dotenv(self, env_path):
        config = Config()
        config.from_dotenv(env_path)
        assert isinstance(config["MAX_LINES"], int)
        assert config["MAX_LINES"] == 10
        assert isinstance(config["TEMPERATURE"], float)
        assert config["TEMPERATURE"] == 98.2

    def test_dunder_str(self):
        expected = "{'DEBUG': True}"
        config = Config()
        config["DEBUG"] = True
        assert str(config) == expected

    def test_env_var_can_be_renamed(self):
        try:
            del os.environ["FOO_DEBUG"]
        except KeyError:
            pass
        os.environ["FOO_DEBUG"] = "true"
        config = Config()
        config.from_envar("FOO_DEBUG", rename="DEBUG")
        assert config["DEBUG"] is True

    def test_from_env_var_that_equals_not_found(self):
        config = Config()
        os.environ["FOO"] = "not found"
        config.from_envar("FOO")
        assert config["FOO"] == "not found"

    def test_from_env_var_with_default_value(self):
        config = Config()
        os.environ["FOO"] = "BAR"
        config.from_envar("FOO", default="BAZ")
        assert config["FOO"] == "BAR"
        del os.environ["FOO"]
        assert config["FOO"] == "BAZ"

    def test_from_env_var_with_default_value_and_alias(self):
        config = Config()
        os.environ["FOO"] = "BAR"
        config.from_envar("FOO", rename="FOOBAR", default="BAZ")
        assert config["FOOBAR"] == "BAR"
        del os.environ["FOO"]
        assert config["FOOBAR"] == "BAZ"
        with pytest.raises(KeyError):
            config["FOO"]  # should not be part of config
