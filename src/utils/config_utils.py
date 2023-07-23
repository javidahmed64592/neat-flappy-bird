import json
import os
from importlib import import_module
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, List, cast


def get_config_module(settings_module: str = "") -> ModuleType:
    """
    Load configs from janitor/config folder using environment variable.

    Arguments:
        settings_module (str): the settings module to load

    Returns:
        [ModuleType]: config module, available to use via `config.<param>`
    """
    if not settings_module:
        settings_module = os.environ.get("SETTINGS_MODULE", "src.config.defaults")

    config = import_module(settings_module)
    return config


def parse_configs(config_names: List[str], config_values: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Parse config files into dictionary form for easier indexing.

    Arguments:
        config_names (List(str)): List of config file names
        config_values (Dict(str, Any)): Config settings

    Returns:
        (Dict): Dictionary of config names and corresponding settings
    """
    return dict(zip(config_names, config_values))


def load_json(filepath: Path) -> Dict[str, Any]:
    """Load json file.

    Arguments:
        filepath (str): Path to json file

    Returns:
        (Dict(str, Any)): json values
    """
    with open(filepath, "r") as file:
        return cast(Dict[str, Any], json.load(file))


def load_configs(config_names: List[str]) -> Dict[str, Any]:
    """Load all configs into a dictionary.

    Arguments:
        config_names (List(str)): List of config file names

    Returns:
        (Dict(str, Any)): Dictionary of config names and settings
    """
    config_values = []
    config_folder = Path("./src/config")

    for name in config_names:
        config_values.append(load_json(config_folder / f"{name}_config.json"))

    return parse_configs(config_names, config_values)
