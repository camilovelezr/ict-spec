import enum
from typing import Optional

from pydantic import (
    BaseModel,
    RootModel,
    ValidationError,
    create_model,
    field_validator,
)

from ict.ui.ui_types import (
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


TYPESDICT = {
    "text": UIText,
    "number": UINumber,
    "checkbox": UICheckbox,
    "select": UISelect,
    "multiselect": UIMultiselect,
    "color": UIColor,
    "datetime": UIDatetime,
    "path": UIPath,
    "file": UIFile,
}


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


class UIBase(BaseModel, extra="forbid"):
    """UI BaseModel."""

    key: UIKey
    title: str
    description: str
    customType: Optional[str] = None
    condition: Optional[str] = None  # make a validator
    type: TypesEnum


class UI:
    """UI object."""

    def __new__(cls, **kwargs):
        """Dynamically create UI object model."""
        options = {
            name: (value.annotation, value.default)
            for name, value in TYPESDICT[kwargs["type"]].model_fields.items()
        }
        model = create_model("UI", **options, __base__=UIBase)
        return model(**kwargs)


# def create_ui(ui_type: UIType):
#     """Dynamically create UI object model."""
#     kwargs = {
#         name: (value.annotation, value.default)
#         for name, value in ui_type.model_fields.items()
#     }
#     return create_model("UI", **kwargs, __base__=UIBase)
