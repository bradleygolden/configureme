# -*- coding: utf-8 -*-
# alternatively, you can load config values from a .env file path
# note: you can choose which file is more important, .env or from object
#       by choosing which order to load the files in
from pathlib import Path

from configureme import Config

from .config import DevConfig

# create your config object to be used in your application
config = Config()

# load your configuration from a default object
config.from_object(DevConfig)


path = Path("examples/basic") / ".env"
config.from_dotenv(str(path))

# you can also watch environment variables
# note: environment variables will always take precedence
#       over any other value
config.from_envar("TESTING")
