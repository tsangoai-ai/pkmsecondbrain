#!/usr/bin/env python3
import json
import sys
from pathlib import Path

class ValidationError(Exception):
    pass


def load_json(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValidationError(f"File not found: {path}")
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON in {path}: {e}")


def type_name(value):
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int) and not isinstance(value, bool):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def validate_instance(schema, instance, path="$"):
    """
    Minimal JSON Schema validator for the TrevorOS schema.
    Supports:
      - type
      - required
      - properties
      - items
      - enum
    """
    if not isinstance(schema, dict):
        raise ValidationError(f"{path}: schema must be an object")

    # type
    if "type" in schema:
        expected = schema["type"]
        actual = type_name(instance)
        if isinstance(expected, list):
            if actual not in expected:
                raise ValidationError(f"{path}: expected type in {expected}, got {actual}")
        else:
            if actual != expected:
                raise ValidationError(f"{path}: expected type {expected}, got {actual}")

    # enum
    if "enum" in schema:
        if instance not in schema["enum"]:
            raise ValidationError(f"{path}: value {instance!r} not in enum {schema['enum']}")

    # object
    if isinstance(instance, dict):
        props = schema.get("properties", {})
        required = schema.get("required", [])

        for key in required:
            if key not in instance:
                raise ValidationError(f"{path}: missing required property {key!r}")

        for key, value in instance.items():
            if key in props:
                child_schema = props[key]
            else:
                # additionalProperties not fully handled; allow unknown by default
                continue
            validate_instance(child_schema, value, f"{path}.{key}")

    # array
    if isinstance(instance, list):
        items_schema = schema.get("items")
        if items_schema:
            for idx, item in enumerate(instance):
                validate_instance(items_schema, item, f"{path}[{idx}]")


def collect_schema_enums(schema, path="$", acc=None):
    if acc is None:
        acc = set()
    if isinstance(schema, dict):
        if "enum" in schema and isinstance(schema["enum"], list):
            for v in schema["enum"]:
                if isinstance(v, str):
                    acc.add(v)
        for k, v in schema.items():
            collect_schema_enums(v, f"{path}.{k}", acc)
    elif isinstance(schema, list):
        for idx, item in enumerate(schema):
            collect_schema_enums(item, f"{path}[{idx}]", acc)
    return acc


def collect_ontology_labels(ontology):
    """
    Try to build a set of labels from ontology.json in a tolerant way.
    Supports a few likely shapes:

    1) {"labels": ["People", "Systems", ...]}
    2) {"labels": [{"label": "People", ...}, ...]}
    3) [{"label": "People"}, {"label": "Systems"}]
    4) Generic object/list where we scan for "label"/"name"/"id" string fields.
    """
    labels = set()

    def scan(value):
        if isinstance(value, dict):
            # direct shape
            if "label" in value and isinstance(value["label"], str):
                labels.add(value["label"])
            for k, v in value.items():
                if k in ("label", "name", "id") and isinstance(v, str):
                    labels.add(v)
                else:
                    scan(v)
        elif isinstance(value, list):
            for item in value:
                scan(item)

    if isinstance(ontology, dict) and "labels" in ontology:
        # common pattern: { "labels": [...] }
        scan(ontology["labels"])
    else:
        scan(ontology)

    return labels


def validate_ontology_vs_schema(schema, ontology):
    metadata_type_enum = (
        schema.get("properties", {})
        .get("metadata", {})
        .get("properties", {})
        .get("type", {})
        .get("enum", [])
    )
    schema_enum_values = {v for v in metadata_type_enum if isinstance(v, str)}
    ontology_labels = collect_ontology_labels(ontology)

    if not ontology_labels:
        print("WARN: No ontology labels detected in ontology.json", file=sys.stderr)
        return

    if not schema_enum_values:
        print("WARN: No enum values detected in schema.json", file=sys.stderr)
        return

    extra_in_schema = schema_enum_values - ontology_labels
    extra_in_ontology = ontology_labels - schema_enum_values

    if extra_in_schema:
        raise ValidationError(
            "Schema metadata.type enum values not present in ontology.json: "
            + ", ".join(sorted(extra_in_schema))
        )

    if extra_in_ontology:
        raise ValidationError(
            "Ontology labels not present in schema metadata.type enum: "
            + ", ".join(sorted(extra_in_ontology))
        )


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_schema.py <path-to-instance-json>", file=sys.stderr)
        sys.exit(1)

    instance_path = Path(sys.argv[1]).resolve()

    # Assume script is in TrevorOS_v41/tools/
    tools_dir = Path(__file__).resolve().parent
    root_dir = tools_dir.parent

    schema_path = root_dir / "schema.json"
    ontology_path = root_dir / "ontology.json"

    try:
        schema = load_json(schema_path)
        ontology = load_json(ontology_path)
        instance = load_json(instance_path)

        # Validate instance against schema
        validate_instance(schema, instance, "$")

        # Validate consistency between schema enums and ontology labels
        validate_ontology_vs_schema(schema, ontology)

    except ValidationError as e:
        print(f"INVALID: {e}", file=sys.stderr)
        sys.exit(1)
    else:
        print("VALID")
        sys.exit(0)


if __name__ == "__main__":
    main()
