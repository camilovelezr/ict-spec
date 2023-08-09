"""Metadata Models"""
from pathlib import Path
from typing import Optional, Union

from pydantic import (
    AnyHttpUrl,
    BaseModel,
    EmailStr,
    RootModel,
    field_validator,
    model_validator,
)

from ict.common import Version

v = Version("2.0.1")


class Author(RootModel):
    """Author object."""

    root: str

    # TODO maybe too specific
    @field_validator("root")
    @classmethod
    def check_author(cls, value):
        """Check the author follows the correct format."""
        if not len(value.split(" ")) == 2:
            raise ValueError(
                "The author must be in the format <first name> <last name>"
            )
        return value

    def __repr__(self):
        """Repr."""
        return self.root


class Doi(RootModel):
    """DOI object."""

    root: str


class Metadata(BaseModel):
    """Metadata BaseModel."""

    specVersion: Version
    name: str
    version: Version
    container: str = "dockerhub"
    entrypoint: Union[Path, str]
    title: Optional[str] = None
    description: Optional[str] = None
    author: list[Author]
    contact: Optional[Union[EmailStr, AnyHttpUrl]]
    repository: AnyHttpUrl
    citation: Optional[Doi]

    @field_validator("name")
    @classmethod
    def check_name(cls, value):
        """Check the name follows the correct format."""
        if not len(value.split("/")) in [2, 3]:
            raise ValueError(
                "The name must be in the format <organization/user>/<ICT name>"
            )
        return value

    @field_validator("container")
    @classmethod
    def check_container(cls, value):
        """Check the container follows the correct format."""
        if not len(value.split("/")) in [2, 3]:
            raise ValueError(
                "The name must be in the format <registry path>/<image repository>:<tag>"
            )
        return value

    @model_validator(mode="after")
    def default_title(self):
        """Set the title to the name if not provided."""
        if self.title is None:
            self.title = self.name
        return self


d = {
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
}
t = Metadata(**d)
