from src.utils.config_utils import load_configs

_CONFIG_NAMES = ["game", "ga", "nn", "bird", "pipe"]
_CONFIG = load_configs(_CONFIG_NAMES)

GAME = _CONFIG["game"]
GA = _CONFIG["ga"]
NN = _CONFIG["nn"]
BIRD = _CONFIG["bird"]
PIPE = _CONFIG["pipe"]
