from os import path
from utils.config_utils import load_configs

config_names = ["game", "ga", "nn", "bird", "pipe"]
config = load_configs(config_names)
wd = path.realpath(path.dirname(__file__))
