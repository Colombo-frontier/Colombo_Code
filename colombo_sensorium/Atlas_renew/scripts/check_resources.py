"""Verify wheel/source instruction resources and public tool contracts without a model."""
from pathlib import Path
import json

from jsonschema import Draft202012Validator
from oracle_atlas_maintenance.runtime import _instructions


def main():
    manifest = {}
    for role in ("scout", "reviewer"):
        text, schema, hashes = _instructions(role)
        Draft202012Validator.check_schema(schema)
        assert text.strip() and schema["additionalProperties"] is False
        manifest[role] = {"instructions_characters": len(text), "files": hashes}
    print(json.dumps({"valid": True, "roles": manifest}, indent=2))


if __name__ == "__main__":
    main()
