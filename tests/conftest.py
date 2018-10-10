# -*- coding: utf-8 -*-
from pathlib import Path

import pytest


@pytest.fixture
def env_path():
    return Path("tests") / ".env"
