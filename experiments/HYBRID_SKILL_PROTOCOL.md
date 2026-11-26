# Hybrid Skill Development & Evaluation Protocol

## Status

This file specifies the experiment. It does **not** claim that the 500/100 experiment or LLM inference has already been run. Current repository state contains 20 curated Terminal Wrench cases and a rule-based pilot. A real 500/100 run requires fetching and auditing the source trajectories and configuring an LLM inference endpoint.

## Dataset plan

Target split:
- Train/development: 500 trajectories.
- Locked test: 100 trajectories.
- Prefer task-level split (no task_id overlap), not random trajectory split, to prevent repeated attempts for the same task leaking across train and test.
- Keep source, task family, model, prompt version, trajectory outcome and source-native labels in metadata.
- Stratify across successful hacks, blocked attempts, legitimate solves and ordinary baselines. Do not collapse failed attempts into benign.
- If the test comes from a source or task family absent in training, call it cross-source or cross-family generalization and report it separately.

Important: the existing 20 case subset is too small to train a detector. Terminal Wrench has 6,289 trajectories in its April 2026 manifest (3,632 hack-labelled and 2,657 non-hack-labelled); the 3,632 hack-labelled bucket itself includes different outcomes, so it must not be treated as 3,632 successful serious exploits. A 500/100 sample should be drawn from the full source data, not by duplicating the 20 cases.

## Data leakage controls

1. Freeze a source revision and record SHA256 for each downloaded trajectory.
2. Split by task_id before prompting or tuning.
3. Keep all test labels, gold step indices, upstream explanations, and case-study reports in a separate sealed file.
4. Training prompts may use only train labels and train trajectories.
5. The test runner loads the final frozen skill/prompt and only then reads test labels for scoring.
6. Do not tune after looking at test-level errors. If the test is inspected, it becomes development data and a new hidden test is needed.

## Two hybrid Skills

### Skill A — High-recall Indexer
- Rules extract candidate events: writes to grader/system binaries, answer-like file flows, score fabrication, state/database mutation, test manipulation, metric/baseline changes, task-constraint violations.
- LLM receives task instruction + bounded trajectory windows + candidate events; it classifies each candidate as relevant / benign / unclear, expands missed candidates when needed, and returns evidence spans.
- Optimize for high recall and evidence localization. Never promote self-report alone to strong evidence.

### Skill B — Evidence Auditor
- Rule layer builds an event timeline: file writes, process changes, reads of answer-like artifacts, toolchain changes, grader access, reward/metric changes.
- LLM compares intended task, observed behavior, verifier contract, and strongest benign alternative.
- Outputs outcome (successful_hack / hack_attempt / benign / insufficient_evidence), atomic mechanism IDs, failure-mode IDs, evidence spans, causal explanation, and uncertainty.
- Optimize for precision, calibrated abstention, and causal support.

Both skills are hybrid. The difference is their objective and depth, not whether one uses rules and the other uses an LLM.

## Iteration protocol on train=500

Run a bounded sequence of variants, record prompt hash and rule version:
- V0: current deterministic rules + generic LLM judge.
- V1: add task-constraint extraction and a structured allowed/forbidden-action ledger.
- V2: add evidence-first two-pass reasoning (candidate events, then verdict).
- V3: add explicit benign counter-hypothesis and insufficient-evidence abstention.
- V4: add cross-step causal checks (read → transform → submit; mutate grader → verifier uses it; baseline/metric mutation → measured gain).
- V5: calibrate thresholds and multi-label taxonomy mapping using train only.

Keep an experiment table with train precision/recall/F1, event-level evidence recall, exact/IoU step localization, false-positive categories, cost, latency, and abstention rate. Select the best checkpoint using predeclared train/dev criteria, not hidden test results.

## Locked test=100

Run each frozen skill once. Report:
- trajectory-level precision, recall, F1, false-positive rate;
- outcome macro-F1 over successful_hack / hack_attempt / benign / insufficient_evidence;
- evidence localization precision/recall or step-level F1;
- mechanism macro-F1 over supported atomic labels and cluster-level F1;
- calibration / abstention quality;
- per-source and per-task-family breakdown;
- confidence intervals (bootstrap by task, not by individual trajectory).

Do not call 100 examples “large-scale validation”; report sample counts and uncertainty.

## Required LLM interface

The ChatGPT subscription UI is not a callable Python API. Batch inference requires a separately configured model endpoint/CLI with credentials and usage permission. No API key should be committed. The current repository scripts do not call an LLM.
