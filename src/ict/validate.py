from pathlib import Path
from typing import TypeVar

from yaml import safe_load

from ict.model import ICT

StrPath = TypeVar("StrPath", str, Path)


def validate(yaml_file: StrPath):
    """Validate an ICT YAML file."""
    with open(yaml_file, "r", encoding="utf-8") as file:
        data = safe_load(file)
    return ICT(**data)
