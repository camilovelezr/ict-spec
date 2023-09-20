"""Test model."""
import json
from pathlib import Path

from ict import validate

yml = Path(__file__).parent.parent.joinpath("example", "spec.yaml")
json_file = Path(__file__).parent.parent.joinpath("example", "spec.json")


def test_sample_yml():
    """Test sample YAML file."""
    ict = validate(yml)
    assert ict.name == "wipp/threshold"
    assert ict.specVersion == "0.1.0"
    assert ict.version == "1.1.1"
    assert ict.container == "wipp/wipp-thresh-plugin:1.1.1"
    assert ict.author == ["Mohammed Ouladi"]
    assert ict.hardware.gpu_type == "any"
    assert ict.hardware.cpu_min == "100"


def test_sample_json():
    """Test sample JSON file."""
    ict = validate(json_file)
    assert ict.name == "wipp/threshold"
    assert ict.specVersion == "0.1.0"
    assert ict.version == "1.1.1"
    assert ict.container == "wipp/wipp-thresh-plugin:1.1.1"
    assert ict.author == ["Mohammed Ouladi"]
    assert ict.hardware.gpu_type == "any"
    assert ict.hardware.cpu_min == "100"


def test_sample_json_dict():
    """Test sample JSON file as dict."""
    with open(json_file, "r", encoding="utf-8") as f_o:
        data = json.load(f_o)
    ict = validate(data)
    assert ict.name == "wipp/threshold"
    assert ict.specVersion == "0.1.0"
    assert ict.version == "1.1.1"
    assert ict.container == "wipp/wipp-thresh-plugin:1.1.1"
    assert ict.author == ["Mohammed Ouladi"]
    assert ict.hardware.gpu_type == "any"
    assert ict.hardware.cpu_min == "100"


def test_both():
    """Test JSON vs YAML."""
    ict_yaml = validate(yml)
    ict_json = validate(json_file)
    assert ict_yaml == ict_json
