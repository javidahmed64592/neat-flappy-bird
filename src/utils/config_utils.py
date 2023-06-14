from os import path
import json
from typing import List, Dict
from __main__ import wd

config_folder = path.join(wd, "config")


def parse_configs(config_names: List[str], config_values: Dict) -> Dict:
    """Parse config files into dictionary form for easier indexing.

    Arguments:
        config_names (List[str]): List of config file names
        config_values (Dict): Config settings

    Returns:
        (Dict): Dictionary of config names and corresponding settings
    """
    return dict(zip(config_names, config_values))


def load_json(filepath: str) -> Dict:
    """Load json file.

    Arguments:
        filepath (str): Path to json file

    Returns:
        (Dict): json values
    """
    with open(filepath, "r") as file:
        return json.load(file)


def load_configs(config_names: List[str]) -> Dict:
    """Load all configs into a dictionary.

    Arguments:
        config_names (str): List of config file names

    Returns:
        (Dict): Dictionary of config names and settings
    """
    config_values = []

    for name in config_names:
        config_values.append(load_json(path.join(config_folder, f"{name}_config.json")))

    return parse_configs(config_names, config_values)
