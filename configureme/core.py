# -*- coding: utf-8 -*-
import os
import warnings

from .helpers import dotenv_to_dict, envar_exists, get_envar


class ConfigVar:
    def __init__(self, name, value=None, alias=None, default=None, use_env=False):
        self.name = name
        self._value = value
        self.alias = alias
        self.default = default
        self.use_env = use_env

    @property
    def value(self):
        if self.use_env:
            if envar_exists(self.name):
                return get_envar(self.name)
            elif not envar_exists(self.name) and self._value:
                return self._value
            elif not envar_exists(self.name) and self.default:
                return self.default
            elif not envar_exists(self.name):
                raise KeyError(f"{self.name} is not a valid value.")
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def is_renamed(self):
        return self.alias is not None


class ConfigVars:
    def __init__(self):
        self.store = {}

    def add(self, name, **kwargs):
        if self.exists(name):
            for key, value in kwargs.items():
                if value:
                    setattr(self.store[name], key, value)
        else:
            self.store[name] = ConfigVar(name, **kwargs)

    def get(self, name):
        try:
            return self.store[name]
        except KeyError:
            for _, var in self.store.items():
                if var.is_renamed:
                    return var

    def exists(self, name):
        return name in self.store.keys()

    def to_dict(self):
        rv = {}
        for key in self.store.keys():
            rv[key] = self.get(key).value
        return rv


class Config(dict):
    def __init__(self):
        self.config_vars = ConfigVars()

    def __contains__(self, key):
        return self.config_vars.exists(key)

    def __setitem__(self, key, value):
        self.config_vars.add(key, value=value)

    def __getitem__(self, key):
        var = self.config_vars.get(key)
        if var.alias and var.alias != key:
            raise KeyError(f"{key} is not a valid key.")
        return var.value

    def __str__(self):
        return str(self.config_vars.to_dict())

    def from_object(self, obj: object):
        """Read configuration from an object."""
        _store = {key: value for key, value in obj.__dict__.items() if key.isupper()}
        for name, value in _store.items():
            self.config_vars.add(name, value=value)

    def from_dotenv(self, path: str):
        """Load configuration from specified .env path."""
        for name, value in dotenv_to_dict(path).items():
            self.config_vars.add(name, value=value)

    def from_envar(self, name: str, rename: str = None, default: str = None):
        """Set configuration from an environment variable."""
        if not os.getenv(name) and rename is None:
            warn_msg = f"Environment variable '{name}' not found."
            warnings.warn(warn_msg, RuntimeWarning)
            return
        self.config_vars.add(name, alias=rename, default=default, use_env=True)
