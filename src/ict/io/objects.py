"""IO objects for ICT."""
import enum
from typing import Union

from pydantic import BaseModel, Field


class TypesEnum(str, enum.Enum):
    """Types enum for IO."""

    STRING = "string"
    NUMBER = "number"
    ARRAY = "array"
    BOOLEAN = "boolean"
    PATH = "path"


class IO(BaseModel):
    """IO BaseModel."""

    name: str
    io_type: TypesEnum = Field(..., alias="type")
    description: str
    required: bool
    io_format: Union[list[str], dict] = Field(..., alias="format")  # TODO ontology?
