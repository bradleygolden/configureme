# -*- coding: utf-8 -*-
import os
import warnings

from .helpers import dotenv_to_dict, str_to_py


class Config(dict):
    def __init__(self):
        self._aliases = dict()
        self._defaults = dict()
        self.envs = list()

    def __getitem__(self, key):
        rv = None
        # environment variables always take precedence
        rv = self._env_value(key)
        if rv is not None:
            return rv
        # no env variable value exists, use the config value if it exists
        if key in self:
            return self.get(key, None)
        # no config value exists, use the default value if it exists
        if key in self._defaults:
            return self._defaults[key]
        # no default value for the key, use the default value of its alias if it exists
        if key in self._aliases:
            key_alias = self._aliases[key]
            if key_alias in self._defaults:
                return self._defaults[key_alias]
        raise ValueError(
            f"Variable {key} value is not set as an environment variable or config value, and does not have a default value."
        )

    def _env_value(self, key: str):
        rv = None
        try:
            env_value = os.environ[key]
            rv = str_to_py(env_value)
        except KeyError:
            pass
        try:
            env_value = os.environ[self._aliases[key]]
            rv = str_to_py(env_value)
        except KeyError:
            pass
        return rv

    def from_object(self, obj: object):
        """Read configuration from an object."""
        _store = {key: value for key, value in obj.__dict__.items() if key.isupper()}
        for name, value in _store.items():
            self[name] = value

    def from_dotenv(self, path: str):
        """Load configuration from specified .env path."""
        _store = dotenv_to_dict(path)
        for name, value in _store.items():
            self[name] = value

    def from_envar(self, name: str, rename: str = None, default: str = None):
        """Set configuration from an environment variable."""
        if not os.getenv(name):
            warn_msg = f"Environment variable '{name}' not found."
            warnings.warn(warn_msg, RuntimeWarning)
            return
        if rename is not None:
            self._aliases[rename] = name
        if default is not None:
            self._defaults[name] = default
