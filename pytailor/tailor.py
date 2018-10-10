# -*- coding: utf-8 -*-
import os
import warnings

from .helpers import dotenv_to_dict, str_to_py


class Tailor(dict):
    def __init__(self):
        self.env_store = dict()

    def __getitem__(self, key):
        rv = None
        if key in self.env_store:
            # environment variables always take precedence
            try:
                env_value = os.environ[key]
                rv = str_to_py(env_value)
            except KeyError:
                # system environment variable no longer exists
                # does a saved config value exist?
                if key in self.keys():
                    rv = super().__getitem__(key)
                else:
                    # seems the user deleted their environment variable and
                    # don't have it configured in a file
                    rv = self.env_store[key]
        else:
            rv = super().__getitem__(key)

        return rv

    def from_object(self, obj: object):
        """Read configuration from an object."""
        _store = {
            key: value
            for key, value in obj.__dict__.items()
            if not key.startswith("__")
        }
        for name, value in _store.items():
            self[name] = value

    def from_dotenv(self, path: str):
        """Load configuration from specified .env path."""
        _store = dotenv_to_dict(path)
        for name, value in _store.items():
            self[name] = value

    def from_envar(self, name: str):
        """Set configuration from an environment variable."""
        value = os.getenv(name)
        if not value:
            warn_msg = f"Environment variable '{name}' not found."
            warnings.warn(warn_msg, RuntimeWarning)
        else:
            mod_value = str_to_py(value)
            self.env_store[name] = mod_value
