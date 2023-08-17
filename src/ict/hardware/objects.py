"""Hardware Requirements for ICT."""
from pydantic import BaseModel, Field


class CPU(BaseModel):
    """CPU object."""

    cpu_type: str = Field(..., alias="type")
    cpu_min: str = Field(..., alias="min")
    recommended: str = Field(..., alias="recommended")


class Memory(BaseModel):
    """Memory object."""

    memory_min: str = Field(..., alias="min")
    memory_recommended: str = Field(..., alias="recommended")


class GPU(BaseModel):
    """GPU object."""

    gpu_enabled: bool = Field(..., alias="enabled")
    gpu_required: bool = Field(..., alias="required")
    gpu_type: str = Field(..., alias="type")


class HardwareRequirements(BaseModel):
    """HardwareRequirements object."""

    cpu: CPU
    memory: Memory
    gpu: GPU
