# Toolflow Bootstrap Assets

This folder turns planning into executable contracts for the first implementation stage.

## Contents
- `templates/ingest_job.example.yaml`: input template for DouyinSourceIngest jobs.
- `schemas/ingest_job.schema.json`: validation schema for ingest job inputs.
- `schemas/artifact_manifest.schema.json`: validation schema for ingest outputs.
- `templates/pipeline.m1.example.yaml`: minimal M1 orchestration pipeline (P1->P2->P3).

## Recommended next action
1. Add a small validator script that checks YAML/JSON against these schemas.
2. Wrap `douyin-downloader` CLI into a connector that reads `ingest_job` and emits `artifact_manifest`.
3. Persist run state per `job_id` for resumable re-runs.


## Validation command
- `python toolflow/validate_toolflow.py`
