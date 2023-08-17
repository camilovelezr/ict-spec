"""Metadata Model."""
import re
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

from ict.version import Version


class Author(RootModel):
    """Author object."""

    root: str

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


class DOI(RootModel):
    """DOI object."""

    root: str

    @field_validator("root")
    @classmethod
    def check_doi(cls, value):
        """Check the doi follows the correct format."""
        if not value.startswith("10."):
            raise ValueError("The DOI must start with 10.")
        if not len(value.split("/")) == 2:
            raise ValueError("The DOI must be in the format <prefix>/<suffix>")
        return value

    def __repr__(self):
        """Repr."""
        return self.root


class Metadata(BaseModel):
    """Metadata BaseModel."""

    specVersion: Version
    name: str
    version: Version
    container: str
    entrypoint: Union[Path, str]
    title: Optional[str] = None
    description: Optional[str] = None
    author: list[Author]
    contact: Optional[Union[EmailStr, AnyHttpUrl]]
    repository: AnyHttpUrl
    citation: Optional[DOI]

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
        if not bool(re.match(r"^[a-zA-Z]*\/{0,1}[a-zA-Z_\-]+:[a-zA-Z0-9_\.]+$", value)):
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
