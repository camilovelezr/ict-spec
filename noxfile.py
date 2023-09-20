"""Nox automation file."""

from nox import Session, session


@session(python=["3.10"])
def export_json(session: Session) -> None:
    """Export Pydantic model as JSON schema."""
    session.install(".")

    session.run("python", "jsonschema.py")
