"""IO objects for ICT."""
import enum
from typing import Optional, Union

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

    name: str = Field(
        description="Unique input or output name for this plugin, case-sensitive match to corresponding variable expected by tool.",
        examples=["thresholdtype"],
    )
    io_type: TypesEnum = Field(
        ...,
        alias="type",
        description="Defines the parameter passed to the ICT tool based on broad categories of basic types.",
        examples=["string"],
    )
    description: Optional[str] = Field(
        None,
        description="Short text description of expected value for field.",
        examples=["Algorithm type for thresholding"],
    )
    required: bool = Field(
        description="Boolean (true/false) value indicating whether this "
        + "field needs an associated value.",
        examples=["true"],
    )
    io_format: Union[list[str], dict] = Field(
        ...,
        alias="format",
        description="Defines the actual value(s) that the input/output parameter represents"
        + "represents using an ontology schema.",
    )  # TODO ontology
