# pylint: disable=no-member, disable=too-many-arguments
"""Test Pydantic Model."""

import hypothesis.strategies as st
import pytest
from hypothesis import given
from pydantic import ValidationError

from ict.hardware.objects import CPU, GPU, HardwareRequirements, Memory
from ict.metadata import Metadata


@given(
    model_name=st.sampled_from(
        ["wipp/threshold", "wipp/segmentation", "nist/wipp/segmentation"]
    ),
    version=st.sampled_from(["0.1.0", "0.2.0", "0.1.1-dev3"]),
    container=st.from_regex(r"^[a-zA-Z]*\/{0,1}[a-zA-Z_\-]+:[a-zA-Z0-9_\.]+$"),
    entrypoint=st.text(),  # TODO path
    author=st.lists(st.from_regex(r"^[a-zA-Z]{3,} [a-zA-Z]{2,}$")),
    contact=st.sampled_from(
        ["abc@git.com", "re@he.com", "user123@gmail.com", "https://github.com/issues"]
    ),  # emails from hypothesis not good
    citation=st.from_regex(r"^10\.[0-9a-zA-z]{2,}\/[0-9a-zA-z]{4,}$"),
)
def test_metadata1(
    model_name,
    version,
    container,
    entrypoint,
    author,
    contact,
    citation,
):
    """Test Metadata Model."""
    repository = "https://github.com/myrepo/myrepo"
    documentation = "https://github.com/myrepo/myrepo/documentation"
    ict = Metadata(
        specVersion="0.1.0",
        name=model_name,
        version=version,
        container=container,
        entrypoint=entrypoint,
        author=author,
        contact=contact,
        repository=repository,
        documentation=documentation,
        citation=citation,
    )
    assert ict.name == model_name
    assert ict.version == version
    assert ict.container == container
    assert ict.entrypoint == entrypoint
    assert ict.author == author
    assert str(ict.contact).lower() == contact.lower()
    assert str(ict.repository) == repository
    assert str(ict.documentation) == documentation
    assert str(ict.citation) == citation  # checking str of DOI object
    assert ict.title == ict.name


@given(
    model_name=st.sampled_from(
        ["wipp/threshold", "wipp/segmentation", "nist/wipp/segmentation"]
    ),
    version=st.sampled_from(["0.1.0", "0.2.0", "0.1.1-dev3"]),
    container=st.from_regex(r"^[a-zA-Z]*\/{0,1}[a-zA-Z_\-]+:[a-zA-Z0-9_\.]+$"),
    entrypoint=st.text(),  # TODO path
    author=st.lists(st.from_regex(r"^[a-zA-Z]{3,} [a-zA-Z]{2,}$")),
    contact=st.sampled_from(
        ["abc@git.com", "re@he.com", "user123@gmail.com", "https://github.com/issues"]
    ),  # emails from hypothesis not good
    citation=st.from_regex(r"^10\.[0-9a-zA-z]{2,}\/[0-9a-zA-z]{4,}$"),
)
def test_metadata2(
    model_name,
    version,
    container,
    entrypoint,
    author,
    contact,
    citation,
):
    """Test Metadata Model."""
    repository = "https://github.com/myrepo/myrepo"
    documentation = "https://github.com/myrepo/myrepo/documentation"
    ict = Metadata(
        specVersion="0.1.0",
        name=model_name,
        version=version,
        container=container,
        entrypoint=entrypoint,
        author=author,
        contact=contact,
        repository=repository,
        documentation=documentation,
        citation=citation,
        title="mytitle",
    )
    assert ict.name == model_name
    assert ict.version == version
    assert ict.container == container
    assert ict.entrypoint == entrypoint
    assert ict.author == author
    assert str(ict.contact).lower() == contact.lower()
    assert str(ict.repository) == repository
    assert str(ict.documentation) == documentation
    assert ict.citation == citation
    assert ict.title == "mytitle"


@given(
    cpu_min=st.text(min_size=1),
    cpu_type=st.text(min_size=2, max_size=4),
    cpu_recommended=st.integers(1, 120),
    memory_min=st.floats(1, 120),
    gpu_enabled=st.booleans(),
    gpu_required=st.booleans(),
)
def test_hr(cpu_min, cpu_type, cpu_recommended, memory_min, gpu_enabled, gpu_required):
    """Test HardwareRequirements Model."""
    cpu = CPU(min=cpu_min, type=cpu_type, recommended=cpu_recommended)
    memory = Memory(min=memory_min)
    gpu = GPU(enabled=gpu_enabled, required=gpu_required)
    h_r = HardwareRequirements(cpu=cpu, memory=memory, gpu=gpu)
    assert h_r.cpu.cpu_min == cpu_min
    assert h_r.cpu.cpu_type == cpu_type
    assert h_r.cpu.cpu_recommended == str(cpu_recommended)
    assert h_r.memory.memory_min == str(memory_min)
    assert h_r.memory.memory_recommended is None
    assert isinstance(h_r.memory.memory_min, str)
    assert h_r.gpu.gpu_enabled == gpu_enabled
    assert h_r.gpu.gpu_required == gpu_required


def test_hr_cpu_fail_1():
    """Test HardwareRequirements Model."""
    with pytest.raises(ValidationError):
        CPU(min=bool, type="2", recommended="3")


def test_hr_cpu_fail_2():
    """Test HardwareRequirements Model."""
    with pytest.raises(ValidationError):
        Memory(min=2.3, recommended=True)
