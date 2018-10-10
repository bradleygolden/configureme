# -*- coding: utf-8 -*-
# declare your configuration just like you normally would


class Config:
    DEBUG = False


class DevConfig(Config):
    DEBUG = True
    TESTING = True


class ProdConfig(Config):
    TESTING = False
