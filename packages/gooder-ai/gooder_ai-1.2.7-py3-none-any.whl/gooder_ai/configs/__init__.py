from json import load
from importlib import resources
from gooder_ai import configs


def load_starter_config() -> dict:
    with resources.files(configs).joinpath("gooder-configs", "user-config.json").open(
        "r"
    ) as f:
        return load(f)
