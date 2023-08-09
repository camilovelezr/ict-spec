"""UI types."""
import enum
from typing import Optional, Union

from pydantic import BaseModel


class UIType(BaseModel):
    """Base UIType object."""


class UIText(UIType):
    """UIText object."""

    default: Optional[str] = None
    regex: Optional[str] = None
    toolbar: Optional[bool] = None


class UINumber(UIType):
    """UINumber object."""

    default: Optional[Union[int, float]] = None
    integer: Optional[bool] = None
    range: Optional[tuple[Union[int, float], Union[int, float]]] = None


class UICheckbox(UIType):
    """UICheckbox object."""

    default: Optional[bool] = None


class UISelect(UIType):
    """UISelect object."""

    fields: list[str]
    optional: Optional[bool] = None


class UIMultiselect(UIType):
    """UIMultiselect object."""

    fields: list[str]
    optional: Optional[bool] = None
    limit: Optional[int] = None


class UIColor(UIType):
    """UIColor object in RGB."""

    fields: list[int]


class W3Format(str, enum.Enum):
    """W3Format enum."""

    YEAR = "YYYY"
    YEAR_MONTH = "YYYY-MM"
    COMPLETE_DATE = "YYYY-MM-DD"
    COMPLETE_DATE_TIME = "YYYY-MM-DDThh:mmTZD"
    COMPLETE_DATE_TIME_SEC = "YYYY-MM-DDThh:mm:ssTZD"
    COMPLETE_DATE_TIME_MS = "YYYY-MM-DDThh:mm:ss.sTZD"


class UIDatetime(UIType):
    """UIDatetime object."""

    format: W3Format


class UIPath(UIType):
    """UIPath object absolute or relative using Unix conventions."""

    ext: Optional[list[str]] = None


class UIFile(UIType):
    """UIFile user uploaded binary data object."""

    ext: Optional[list[str]] = None
    limit: Optional[int] = None
    size: Optional[int] = None


# t = UIFile(ext=[".txt", ".csv"], limit=1, size=1000)
2
