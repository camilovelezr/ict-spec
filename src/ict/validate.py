import json
from functools import singledispatch
from pathlib import Path
from typing import Any, TypeVar

from yaml import safe_load

from ict.model import ICT

StrPath = TypeVar("StrPath", str, Path)


@singledispatch
def validate(file: Any) -> ICT:
    """Validate an ICT specification."""
    raise NotImplementedError(f"File type not supported: {file}")


@validate.register
def _(file: StrPath) -> ICT:
    """Validate an ICT specification."""
    if str(file).endswith(".yaml") or str(file).endswith(".yml"):
        with open(file, "r", encoding="utf-8") as f_o:
            data = safe_load(f_o)
    elif str(file).endswith(".json"):
        with open(file, "r", encoding="utf-8") as f_o:
            data = json.load(f_o)
    else:
        raise ValueError(f"File extension not supported: {file}")
    return validate(data)


@validate.register
def _(ict: dict) -> ICT:
    """Validate an ICT specification."""
    return ICT(**ict)
