"""Generate JSON schema from Pydantic model."""
import json

from ict import ICT

schema = ICT.model_json_schema()
with open("schema.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(schema, indent=2))
