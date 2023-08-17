from functools import singledispatch
from pathlib import Path
from typing import TypeVar

from yaml import safe_load

from ict.model import ICT

StrPath = TypeVar("StrPath", str, Path)


@singledispatch
def validate(yaml_file: StrPath) -> ICT:
    """Validate an ICT specification."""
    with open(yaml_file, "r", encoding="utf-8") as file:
        data = safe_load(file)
    return ICT(**data)


@validate.register
def _(ict: dict) -> ICT:
    """Validate an ICT specification."""
    return ICT(**ict)
