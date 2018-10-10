# -*- coding: utf-8 -*-
import os


def test_basic_example():
    os.environ["TESTING"] = "false"
    from examples.basic.app import config

    assert config["TESTING"] is False
    del os.environ["TESTING"]
    assert config["TESTING"] is True  # default state in config
    assert config["DATABASE"] is True
