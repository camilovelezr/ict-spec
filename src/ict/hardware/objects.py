"""Hardware Requirements for ICT."""
from pydantic import BaseModel, Field


class CPU(BaseModel):
    """CPU object."""

    cpu_type: str = Field(
        ...,
        alias="type",
        description="Any non-standard or specific processor limitations.",
        examples=["arm64"],
    )
    cpu_min: str = Field(
        ...,
        alias="min",
        description="Minimum requirement for CPU allocation where 1 CPU unit is equivalent to 1 physical CPU core or 1 virtual core.",
        examples=["100m"],
    )
    recommended: str = Field(
        ...,
        alias="recommended",
        description="Recommended requirement for CPU allocation for optimal performance.",
        examples=["200m"],
    )


class Memory(BaseModel):
    """Memory object."""

    memory_min: str = Field(
        ...,
        alias="min",
        description="Minimum requirement for memory allocation, measured in bytes.",
        examples=["129Mi"],
    )
    memory_recommended: str = Field(
        ...,
        alias="recommended",
        description="Recommended requirement for memory allocation for optimal performance.",
        examples=["200Mi"],
    )


class GPU(BaseModel):
    """GPU object."""

    gpu_enabled: bool = Field(
        ...,
        alias="enabled",
        description="Boolean value indicating if the plugin is optimized for GPU.",
        examples=[False],
    )
    gpu_required: bool = Field(
        ...,
        alias="required",
        description="Boolean value indicating if the plugin requires a GPU to run.",
        examples=[False],
    )
    gpu_type: str = Field(
        ...,
        alias="type",
        description="	Any identifying label for GPU hardware specificity.",
        examples=["cuda11"],
    )


class HardwareRequirements(BaseModel):
    """HardwareRequirements object."""

    cpu: CPU = Field(description="CPU requirements.")
    memory: Memory = Field(description="Memory requirements.")
    gpu: GPU = Field(description="GPU requirements.")
