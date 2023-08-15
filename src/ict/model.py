"""ICT model."""

from typing import Union

from pydantic import Field
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
    Field(discriminator="type"),
]


class ICT(Metadata):
    """ICT object."""

    inputs: list[IO]
    outputs: list[IO]
    ui: list[UIItem]

    # TODO validate that I/O matches ui


t = ICT(
    **{
        "specVersion": "0.1.2",
        "name": "test/t2",
        "version": "0.1.0",
        "entrypoint": "test.py",
        "title": "Test Title",
        "description": "Test Description",
        "author": ["John Doe", "Jane Doe"],
        "contact": "c@u.edu",
        "repository": "https://github.com/ict",
        "citation": "10.5281/zenodo.1234",
        "inputs": [
            {
                "name": "foo",
                "type": "text",
                "description": "bar",
                "required": True,
                "format": "es",
            }
        ],
        "outputs": [
            {
                "name": "cgfd",
                "type": "text",
                "description": "bar",
                "required": "no",
                "format": "es",
            }
        ],
        "ui": [
            {
                "key": "inputs.foo",
                "title": "foo",
                "description": "bar",
                "type": "number",
                "toolbar": True,
            },
            {
                "key": "inputs.foo",
                "title": "foo",
                "description": "bar",
                "type": "nothing",
            },
        ],
    }
)
2
