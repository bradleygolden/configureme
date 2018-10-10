# -*- coding: utf-8 -*-
class Config(object):
    TESTING = True
    DEBUG = False


class DevConfig(Config):
    DEBUG = True
    TESTING = False
    FOO = "BAZ"
