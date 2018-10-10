# -*- coding: utf-8 -*-
import os
import warnings

from .helpers import dotenv_to_dict, str_to_py

NOT_FOUND = "not found"


class Config(dict):
    def __init__(self):
        self._aliases = dict()
        self.envs = list()

    def __getitem__(self, key):
        rv = None
        # environment variables always take precedence
        rv = self._env_value(key)
        if not rv:
            # no env variable value exists use the default if it exists
            rv = self.get(key, NOT_FOUND)
        if rv == NOT_FOUND:
            raise ValueError(
                f"Variable {key} value is not set as an environment variable and does not have a default value."
            )
        return rv

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

    def from_envar(self, name: str, rename: str = None):
        """Set configuration from an environment variable."""
        if not os.getenv(name):
            warn_msg = f"Environment variable '{name}' not found."
            warnings.warn(warn_msg, RuntimeWarning)
        elif rename:
            self._aliases[rename] = name
