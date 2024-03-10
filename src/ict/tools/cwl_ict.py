"""CWL generation for ICT objects.""" ""

from typing import TypeVar

ICT = TypeVar("ICT")


def requirements(ict_: ICT) -> dict:
    """Return the requirements from an ICT object."""
    reqs = {}
    reqs["DockerRequirement"] = {"dockerPull": ict_.container}  # type: ignore
    output_names = [io.name for io in ict_.outputs]  # type: ignore
    if "outDir" in output_names:
        reqs["InitialWorkDirRequirement"] = {
            "listing": [{"entry": "$(inputs.outDir)", "writable": True}]
        }
        reqs["InlineJavascriptRequirement"] = {}
    return reqs


def clt_dict(ict_: ICT) -> dict:
    """Return a dict of a CommandLineTool from an ICT object."""
    clt_ = {
        "class": "CommandLineTool",
        "cwlVersion": "v1.2",
        "inputs": {
            io.name: io._input_to_cwl()  # pylint: disable=W0212
            for io in ict_.inputs + ict_.outputs  # type: ignore
        },
        "outputs": {
            io.name: io._output_to_cwl()  # pylint: disable=W0212
            for io in ict_.outputs  # type: ignore
        },
        "requirements": requirements(ict_),
    }
    return clt_
