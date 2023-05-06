import os
from collections import namedtuple

ENV = {
    "CONFIG_PATH": os.environ.get("CONFIG_PATH", 'promptbot.toml'),
}

env = namedtuple("env", ENV.keys())(*ENV.values())