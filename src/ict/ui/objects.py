import enum
from typing import Literal, Optional, Union

from pydantic import BaseModel, Field, RootModel, field_validator


class UIKey(RootModel):
    """UIKey object."""

    root: str

    @field_validator("root")
    @classmethod
    def check_ui_key(cls, value):
        """Check the UI key follows the correct format."""
        sp = value.split(".")  # ruff: noqa: PLR2004
        if not len(sp) == 2:
            raise ValueError(
                "The UI key must be in the format <inputs or outputs>.<parameter name>"
            )
        if not sp[0] in ["inputs", "outputs"]:
            raise ValueError(
                "The UI key must be in the format <inputs or outputs>.<parameter name>"
            )
        return value


class TypesEnum(str, enum.Enum):
    """Types enum."""

    TEXT = "text"
    NUMBER = "number"
    CHECKBOX = "checkbox"
    SELECT = "select"
    MULTISELECT = "multiselect"
    COLOR = "color"
    DATETIME = "datetime"
    PATH = "path"
    FILE = "file"


class UIBase(BaseModel):
    """UI BaseModel."""

    key: UIKey
    title: str
    description: str
    customType: Optional[str] = None
    condition: Optional[str] = None  # TODO make a validator
    # type: TypesEnum


class UIText(UIBase):
    """UIText object."""

    default: Optional[str] = None
    regex: Optional[str] = None
    toolbar: Optional[bool] = None
    type: Literal["text"]


class UINumber(UIBase):
    """UINumber object."""

    default: Optional[Union[int, float]] = None
    integer: Optional[bool] = None
    range: Optional[tuple[Union[int, float], Union[int, float]]] = None
    type: Literal["number"]


class UICheckbox(UIBase):
    """UICheckbox object."""

    default: Optional[bool] = None
    type: Literal["checkbox"]


class UISelect(UIBase):
    """UISelect object."""

    fields: list[str]
    optional: Optional[bool] = None
    type: Literal["select"]


class UIMultiselect(UIBase):
    """UIMultiselect object."""

    fields: list[str]
    optional: Optional[bool] = None
    limit: Optional[int] = None
    type: Literal["multiselect"]


class UIColor(UIBase):
    """UIColor object in RGB."""

    fields: list[int]
    type: Literal["color"]


class W3Format(str, enum.Enum):
    """W3Format enum."""

    YEAR = "YYYY"
    YEAR_MONTH = "YYYY-MM"
    COMPLETE_DATE = "YYYY-MM-DD"
    COMPLETE_DATE_TIME = "YYYY-MM-DDThh:mmTZD"
    COMPLETE_DATE_TIME_SEC = "YYYY-MM-DDThh:mm:ssTZD"
    COMPLETE_DATE_TIME_MS = "YYYY-MM-DDThh:mm:ss.sTZD"


class UIDatetime(UIBase):
    """UIDatetime object."""

    format: W3Format
    type: Literal["datetime"]


class UIPath(UIBase):
    """UIPath object absolute or relative using Unix conventions."""

    ext: Optional[list[str]] = None
    type: Literal["path"]


class UIFile(UIBase):
    """UIFile user uploaded binary data object."""

    ext: Optional[list[str]] = None
    limit: Optional[int] = None
    size: Optional[int] = None
    type: Literal["file"]
