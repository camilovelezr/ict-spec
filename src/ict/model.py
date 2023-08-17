"""ICT model."""

from typing import Optional, Union

from pydantic import BaseModel, Field, FieldValidationInfo, field_validator
from typing_extensions import Annotated

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


class HardwareRequirements(BaseModel):
    """HardwareRequirements object."""

    cpu_type: str = Field(..., alias="cpu.type")
    cpu_min: str = Field(..., alias="cpu.min")
    cpu_recommended: str = Field(..., alias="cpu.recommended")
    memory_min: str = Field(..., alias="memory.min")
    memory_recommended: str = Field(..., alias="memory.recommended")
    gpu_enabled: bool = Field(..., alias="gpu.enabled")
    gpu_required: bool = Field(..., alias="gpu.required")
    gpu_type: str = Field(..., alias="gpu.type")


class ICT(Metadata):
    """ICT object."""

    inputs: list[IO]
    outputs: list[IO]
    ui: list[UIItem]
    hardware_requirements: Optional[HardwareRequirements] = None

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
