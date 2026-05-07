# Toolflow Skill Architecture for 《狼人杀试炼之地》 Novel + Motion Comic Pipeline

## 1) Overall Objective
Build a **multi-agent, multi-skill production system** that turns long-form Douyin match videos (starting from “京城大师赛”) into:
1. Structured material library (audio/persona/dialogue/event)
2. High-quality serialized novel drafts
3. Motion-comic-ready scripts, shot lists, and asset prompts

The workflow is intentionally **hierarchical**, not linear. Each subplan is owned by a specialized agent with dedicated skill/MCP capabilities.

---

## 2) System Architecture (Agent Graph)

### Layer A — Orchestrator
- **Agent A0: Executive Orchestrator**
  - Responsibilities:
    - Route tasks to sub-agents
    - Enforce quality gates and versioning
    - Handle retries/escalation
  - Required capabilities:
    - Workflow state machine
    - Cross-agent memory indexing
    - Cost/time budget tracking

### Layer B — Ingestion & Understanding
- **Agent B1: Douyin Acquisition Agent**
- **Agent B2: Media Normalization Agent**
- **Agent B3: Speech/Transcript Agent**
- **Agent B4: Speaker & Character Attribution Agent**
- **Agent B5: Event Timeline Structuring Agent**

### Layer C — Creative Adaptation
- **Agent C1: Narrative Bible Agent**
- **Agent C2: Novel Drafting Agent**
- **Agent C3: Novel QA & Continuity Agent**

### Layer D — Motion Comic Production
- **Agent D1: Script-to-Storyboard Agent**
- **Agent D2: Visual Prompt & Asset Planning Agent**
- **Agent D3: Voice/SFX/BGM Direction Agent**
- **Agent D4: Edit Packaging Agent**

### Layer E — Governance
- **Agent E1: Compliance & Risk Agent**
- **Agent E2: Metrics & A/B Evaluation Agent**

---

## 3) Subplan Design (Detailed)

## Subplan P1: Douyin Material Acquisition (B1)
### Goal
Stable, resumable download of complete “京城大师赛” videos and metadata.

### Inputs
- Seed URLs / user主页链接 / playlist keywords
- Cookie/MS token secrets
- Download policy (resolution, concurrency, output naming)

### Processing Steps
1. URL discovery queue initialization
2. Account/cookie validation and rotation
3. Download mode strategy selection (`user`/`mix`/`music` etc.)
4. Concurrent pull with rate limiting and retry backoff
5. Metadata extraction: title, publish time, author, aweme_id
6. Deduplication and incremental sync
7. Raw-to-staging manifest generation

### Outputs
- `raw/videos/*.mp4`
- `raw/meta/*.json`
- `raw/manifests/session_*.json`

### Quality Gates
- Completeness rate >= 98%
- Broken file rate < 1%
- Duplicate aweme_id rate < 0.5%

### Suggested Skill/MCP
- Skill: `douyin-downloader-wrapper`
- MCP: secret vault, object storage, job queue

---

## Subplan P2: Media Preprocessing & Normalization (B2)
### Goal
Produce editing/analysis-friendly standardized media units.

### Steps
1. Verify container integrity (ffprobe)
2. Transcode to standard mezzanine format (H.264 + AAC)
3. Loudness normalization (e.g., -16 LUFS dialogue target)
4. Vocal enhancement + noise suppression
5. Scene-based segmentation (time windows)
6. Keyframe extraction

### Outputs
- `processed/video_mezzanine/*.mp4`
- `processed/audio_clean/*.wav`
- `processed/segments/*.json`
- `processed/keyframes/*.jpg`

### Quality Gates
- Audio clipping ratio < threshold
- Segment boundary confidence >= threshold
- Transcode failure auto-retry + quarantine bucket

---

## Subplan P3: ASR + Transcript Intelligence (B3)
### Goal
Generate accurate, punctuated, time-aligned Chinese transcripts.

### Steps
1. VAD chunking
2. ASR per chunk with overlap stitching
3. Punctuation restoration
4. Named-entity hints injection (狼人杀术语、选手名)
5. Timestamp alignment refinement
6. Confidence calibration

### Outputs
- `analysis/transcript/{video_id}.jsonl`
- `analysis/transcript/{video_id}.srt`

### Quality Gates
- CER/WER benchmark within acceptable range
- Time sync drift < 500ms median

---

## Subplan P4: Speaker Diarization + Character Mapping (B4)
### Goal
Map “who said what” to stable character identities.

### Steps
1. Speaker diarization (speaker segments)
2. Face/person clustering from keyframes
3. Audio-visual linkage (speaker ↔ face)
4. Alias consolidation (e.g., 选手昵称/ID)
5. Uncertainty labeling for manual review queue

### Outputs
- `analysis/speakers/{video_id}.json`
- `analysis/character_registry.json`

### Quality Gates
- Top-N known speaker accuracy target
- Unknown speaker ratio decreasing trend across episodes

---

## Subplan P5: Game Event Structuring (B5)
### Goal
Extract structured狼人杀对局事件 for downstream storytelling.

### Event Schema (example)
- round_id
- phase (夜晚/白天/放逐)
- speaker_id
- action_type (发言/投票/技能/冲突/反转)
- evidence_span (timestamps + transcript refs)
- confidence

### Steps
1. Rule-aware parser over transcript + metadata
2. Phase boundary detection
3. Action extraction and linking
4. Contradiction/event conflict resolution
5. Knowledge graph construction

### Outputs
- `analysis/events/{match_id}.parquet`
- `analysis/graphs/{match_id}.graphml`

### Quality Gates
- Event recall on validation set
- Rule-consistency checks (no impossible phase transitions)

---

## Subplan P6: Narrative Bible Construction (C1)
### Goal
Create a canonical story world from real match material.

### Bible Sections
1. Character dossiers (speech style, tactics, arcs)
2. Faction dynamics
3. Signature scenes and turning points
4. Lexicon/style constraints
5. Timeline canon rules

### Outputs
- `creative/bible/v1/*.md`
- `creative/style_guide.yml`

### Quality Gates
- Cross-document consistency score
- No timeline contradictions

---

## Subplan P7: Novel Generation (C2)
### Goal
Produce chapterized novel drafts with controllable pacing and tone.

### Steps
1. Plot decomposition by chapter goals
2. Scene card generation (objective/conflict/reveal)
3. Draft writing (multi-pass)
4. Dialogue naturalization
5. Suspense calibration (chapter hooks)

### Outputs
- `creative/novel/chapter_*.md`
- `creative/novel/outline.md`

### Quality Gates
- Chapter objective completion
- Character voice consistency
- Readability/style scoring

---

## Subplan P8: Novel QA & Continuity (C3)
### Goal
Enforce long-arc coherence before comic adaptation.

### Steps
1. Fact extraction from chapters
2. Continuity graph validation
3. Character motivation drift detection
4. Repetition and pacing anomaly detection
5. Patch suggestions + auto-fix loops

### Outputs
- `qa/novel_report_v*.md`
- patched chapter versions

### Quality Gates
- Blocking issues = 0
- Major issues below threshold

---

## Subplan P9: Motion Comic Scripting (D1)
### Goal
Convert approved chapters into production scripts.

### Script Units
- scene_id
- panel/shot list
- camera language
- dialogue + narration
- transition cues

### Outputs
- `comic/script/episode_*.md`
- `comic/storyboard/episode_*.json`

---

## Subplan P10: Visual Asset Planning (D2)
### Goal
Standardize visual direction for reproducible asset generation.

### Steps
1. Character visual bible (front/side expressions)
2. Environment pack definition (房间、法庭、夜晚场景)
3. Prompt templates by shot type
4. Negative prompt and consistency tags

### Outputs
- `comic/visual_bible/*.md`
- `comic/prompts/*.yml`

---

## Subplan P11: Audio Direction & Post (D3)
### Goal
Deliver voice/SFX/BGM plan synchronized to storyboard.

### Steps
1. Voice casting matrix by role
2. Emotion-tagged TTS or human VO plan
3. SFX cue sheet
4. BGM tension curve map

### Outputs
- `comic/audio_plan/*.csv`
- `comic/mix_notes/*.md`

---

## Subplan P12: Packaging, Versioning, Release (D4)
### Goal
Create distributable episode packages and traceable provenance.

### Steps
1. Assemble assets and render list
2. Validate subtitle/audio sync
3. Export multi-platform deliverables
4. Emit provenance manifest (source refs -> output refs)

### Outputs
- `release/episodes/*`
- `release/manifests/*.json`

---

## Subplan P13: Compliance & Risk Control (E1)
### Goal
Manage版权、肖像、平台政策 and model safety concerns.

### Controls
- Source usage policy tagging
- Copyright risk scoring
- Sensitive-content redaction policy
- Human-review escalation channels

### Outputs
- `governance/compliance/*.md`
- risk dashboards

---

## Subplan P14: Evaluation & Iteration (E2)
### Goal
Quantify quality and drive iterative improvement.

### Metrics (examples)
- Ingestion: completeness, retry cost, freshness lag
- Transcript: CER/WER, diarization purity
- Narrative: reader retention proxy, hook strength
- Comic: shot clarity score, production efficiency

### Iteration Loop
1. Collect metrics
2. Diagnose bottlenecks
3. Tune prompts/models/rules
4. Re-run impacted stages only

---

## 4) Agent Contracts (Interface Design)
Each agent should publish:
- `inputs.schema.json`
- `outputs.schema.json`
- `quality_gate.yml`
- `retry_policy.yml`
- `observability.yml`

This makes orchestration deterministic and allows plug-and-play replacement.

---

## 5) Data Model & Storage Layers
- **Raw Layer**: immutable source captures
- **Processed Layer**: normalized media + cleaned transcript
- **Semantic Layer**: speakers, events, knowledge graph
- **Creative Layer**: bible, novel, scripts
- **Release Layer**: final comic packages

Use content-addressed IDs and lineage fields:
- `source_hash`
- `parent_artifact_ids`
- `agent_version`

---

## 6) Recommended First Implementation Milestones
1. M1 (2-3 weeks): P1 + P2 + P3 minimal pipeline
2. M2 (2 weeks): P4 + P5 structured event extraction
3. M3 (2 weeks): P6 + P7 novel MVP
4. M4 (2 weeks): P9 + P10 comic pre-production MVP
5. M5 (ongoing): P13 + P14 governance and optimization

---

## 7) Repository Bootstrap Proposal (Your New Project)
Suggested new repo name: `wolf-trial-creative-pipeline`

Top-level structure:
- `agents/` (one folder per sub-agent)
- `schemas/` (all contracts)
- `orchestrator/` (workflow engine)
- `connectors/` (`douyin_downloader`, ASR, storage, LLMs)
- `pipelines/` (stage compositions)
- `prompts/` (versioned prompt packs)
- `eval/` (metrics + benchmark sets)
- `governance/` (policy and review)
- `docs/` (runbooks + architecture)

---

## 8) How `douyin-downloader` Fits as a Skill
Treat this repo as **Skill S1: DouyinSourceIngest**.

### Skill Responsibilities
- Validate/cycle cookies
- Pull videos in configured modes
- Emit deterministic metadata manifest
- Expose resumable ingestion API to orchestrator

### Skill I/O Contract (minimal)
- Input: `seed_urls`, `mode`, `time_range`, `output_root`
- Output: `artifact_manifest.json` with file paths + metadata + hashes

### Why this decomposition works
It isolates unstable platform acquisition complexity from downstream creative agents, minimizing cascading failures.
