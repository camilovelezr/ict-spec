"""Nox automation file."""

from nox import Session, session


@session(python=["3.10"])
def export_json(session: Session) -> None:
    """Export Pydantic model as JSON schema."""
    session.install(".")

    session.run("python", "jsonschema.py")


# from polusai.microjson
@session(python=["3.10"])
def typescript(session: Session):
    """Generate TypeScript types from JSON schema."""

    # Install json-schema-to-typescript
    session.run("npm", "install", "json-schema-to-typescript", external=True)

    # Use json-schema-to-typescript
    session.run(
        "npx",
        "json-schema-to-typescript",
        "schema.json",
        "-o",
        "ictspec.d.ts",
        external=True,
    )
