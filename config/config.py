import json
from pathlib import Path


def load_config(file_name="config.json") -> dict:
    """
    Loads config.json file with configuration for the app; config.json
    has to be in the same directory as config.py

    Args:
        file_name (str, optional): Config file name.
        Defaults to "config.json".

    Returns:
        dict: Dictionary with configuration.
    """
    file_path = Path(__file__).parent.joinpath(file_name)
    with open(file_path, "r") as f:
        return json.load(f)
