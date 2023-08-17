"""ICT model."""

from typing import Optional, Union

from pydantic import Field, FieldValidationInfo, field_validator
from typing_extensions import Annotated

from ict.hardware import HardwareRequirements
from ict.io import IO
from ict.metadata import Metadata
from ict.ui import (
    UICheckbox,
    UIColor,
    UIDatetime,
    UIFile,
    UIMultiselect,
    UINumber,
    UIPath,
    UISelect,
    UIText,
)

UIItem = Annotated[
    Union[
        UIText,
        UINumber,
        UICheckbox,
        UISelect,
        UIMultiselect,
        UIColor,
        UIDatetime,
        UIPath,
        UIFile,
    ],
    Field(discriminator="ui_type"),
]


class ICT(Metadata):
    """ICT object."""

    inputs: list[IO]
    outputs: list[IO]
    ui: list[UIItem]
    hardware: Optional[HardwareRequirements] = None

    @field_validator("ui")
    @classmethod
    def validate_ui(cls, value, info: FieldValidationInfo):
        """Validate that the ui matches the inputs and outputs."""
        ui_keys = [ui.key.root.split(".")[-1] for ui in value]
        io_keys = [io.name for io in info.data["inputs"]]
        io_keys.extend([io.name for io in info.data["outputs"]])
        if not set(ui_keys) == set(io_keys):
            raise ValueError("The ui keys must match the inputs and outputs keys.")
        return value
