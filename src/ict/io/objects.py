from pydantic import BaseModel


class IO(BaseModel):
    """IO BaseModel."""

    name: str
    type: str
    description: str
    required: bool
    format: str  # TODO ontology schema?
