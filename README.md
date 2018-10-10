# configureme

[![Build Status](https://travis-ci.org/bradleygolden/configureme.svg?branch=master)](https://travis-ci.org/bradleygolden/configureme)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![codecov](https://codecov.io/gh/bradleygolden/configureme/branch/master/graph/badge.svg)](https://codecov.io/gh/bradleygolden/configureme)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/bradleygolden/configureme.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/bradleygolden/configureme/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/bradleygolden/configureme.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/bradleygolden/configureme/context:python)
[![GitHub license](https://img.shields.io/github/license/bradleygolden/configureme.svg)](https://github.com/bradleygolden/configureme/blob/master/LICENSE)

Set up configuration for your application or library with ease.

## Features

configureme gives you a few key features that make your life easy when creating libraries or applications:

- Easily create configuration following the config.py pattern
- Use environment variables in your configuration and change them dynamically at runtime
- Use a .env file and follow the [twelve-factor app](https://12factor.net/) methodology

## Example

Get up and running with full configuration quickly:

```python
from configureme import Config

class Config(object):
    DEBUG = False

config = Config()
# load from a simple object
config.from_object(Config)
# add and watch environment variables
config.from_envar("DEBUG")
# use a dotenv file
config.from_dotenv("/path/to/.env/")
# config works like a dict!
config["DEBUG"] # True
```

## Installation

Installation is easy using pip:

```bash
pip install configureme
```

## Advanced Usage

### Usage with pipenv

If your using a dev workflow tool like [Pipenv](https://pipenv.readthedocs.io/en/latest/), you can easily pair configureme with it. Pipenv will automatically load .env files for you out of the box. To track variables loaded from a .env file when using Pipenv, simply use this pattern:

```.env
# .env file
DEBUG=true
```

```python
from configureme import Config
config = Config()
# watch each variable loaded by Pipenv
config.from_envar("DEBUG")
config["DEBUG"]  # True
```

### Usage with python-dotenv

[python-dotenv](https://github.com/theskumar/python-dotenv) is a useful tool for managing .env files in multiple environments. As with the previous example, it's easy to pair with configureme.

```.env
# .env file
DEBUG=true
```

```python
from dotenv import load_dotenv
from configureme import Config

load_dotenv()
config = Config()
# watch each variable loaded by python-dotenv
config.from_envar("DEBUG")
config["DEBUG"]  # True
```

## How to contribute

1. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.

2. Fork the repository on GitHub to start making your changes to the master branch (or branch off of it).

3. Write a test which shows that the bug was fixed or that the feature works as expected. Make sure to use [pre-commit](https://pre-commit.com/) too!

4. Send a pull request and bug the maintainer until it gets merged and published. Make sure to add yourself to AUTHORS.
