#!/usr/bin/env python3
"""Validate toolflow templates against JSON schemas.

Usage:
  python toolflow/validate_toolflow.py
  python toolflow/validate_toolflow.py --job path/to/job.yaml --pipeline path/to/pipeline.yaml
"""

import argparse
import json
from pathlib import Path

import yaml

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None


def _load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _validate(instance, schema, name):
    if jsonschema is None:
        required = schema.get("required", [])
        missing = [k for k in required if k not in instance]
        if missing:
            raise ValueError("{} missing required keys: {}".format(name, ", ".join(missing)))
        print("[WARN] jsonschema not installed; ran required-key fallback for {}".format(name))
        return
    jsonschema.validate(instance=instance, schema=schema)
    print("[OK] {} validation passed".format(name))


def main():
    parser = argparse.ArgumentParser(description="Validate toolflow templates")
    parser.add_argument(
        "--job",
        default="toolflow/templates/ingest_job.example.yaml",
        help="Path to ingest job yaml",
    )
    parser.add_argument(
        "--pipeline",
        default="toolflow/templates/pipeline.m1.example.yaml",
        help="Path to pipeline yaml",
    )
    parser.add_argument(
        "--job-schema",
        default="toolflow/schemas/ingest_job.schema.json",
        help="Path to ingest job schema",
    )
    args = parser.parse_args()

    job_path = Path(args.job)
    pipeline_path = Path(args.pipeline)
    job_schema_path = Path(args.job_schema)

    job = _load_yaml(job_path)
    pipeline = _load_yaml(pipeline_path)
    job_schema = _load_json(job_schema_path)

    _validate(job, job_schema, "ingest_job")

    required_pipeline_keys = ["pipeline_id", "version", "stages"]
    missing = [k for k in required_pipeline_keys if k not in pipeline]
    if missing:
        raise ValueError("Pipeline missing required keys: {}".format(", ".join(missing)))

    if not isinstance(pipeline.get("stages"), list) or not pipeline["stages"]:
        raise ValueError("Pipeline stages must be a non-empty list")

    print("[OK] pipeline basic structure check passed")
    print("All checks passed.")


if __name__ == "__main__":
    main()
