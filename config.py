import typing as t
from dataclasses_json import dataclass_json
from dataclasses import dataclass


@dataclass_json
@dataclass
class ConfigDestination:
    name: str
    address: str


@dataclass_json
@dataclass
class ConfigRoot:
    destinations: t.List[ConfigDestination]


def load_config():
    with open("config.json", 'r') as f:
        contents = f.read()
    return ConfigRoot.from_json(contents)


print(load_config())
