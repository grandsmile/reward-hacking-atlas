# 600-Trajectory Hybrid Skill Experiment

## Dataset and sampling

Use the public Hugging Face dataset [shiv96/terminal-wrench-resanitized](https://huggingface.co/datasets/shiv96/terminal-wrench-resanitized), a fixed Terminal Wrench snapshot with 3,604 accepted re-sanitized reward-hacking traces. Each row includes a matched canonical baseline from the same task/model pair, the task prompt, and full ATIF JSON.

- Positive: accepted re-sanitized reward-hacking trajectory.
- Negative: paired canonical successful baseline trajectory.
- Select 300 distinct task IDs, one deterministic row per task.
- Train: 250 task pairs = 500 trajectories (250 positive, 250 negative).
- Test: 50 task pairs = 100 trajectories (50 positive, 50 negative).
- Task IDs are disjoint.
- The LLM receives only task prompt, trajectory, and rule candidates. It never receives labels, sample kind, source path, or task ID.

The positive traces are re-sanitized, not raw original trajectories. The dataset's stated purpose is to remove explicit linguistic indicators while preserving technical actions. This is useful for testing whether detection relies on actions rather than agent self-reports.

## Hybrid architecture

**Light Indexer:** deterministic candidate extraction, then LLM semantic triage, then suspicious steps, atomic mechanisms and exact evidence. Optimize for recall and evidence localization.

**Heavy Evidence Auditor:** deterministic event reconstruction, then LLM causal analysis, then verdict, mechanism, verifier failure mode, benign alternative and uncertainty. Optimize for precision and causal support.

## Iterations

Run V0–V3 on the 500 training trajectories:
- V0: baseline task/trajectory judgment.
- V1: task-constraint-first reasoning.
- V2: evidence-first reasoning and exact step localization.
- V3: strongest benign counter-hypothesis and abstention.

Choose the best version using training metrics only (F1, then precision). Freeze it and run the 100 test trajectories once. This is prompt/rule refinement, not model-weight fine-tuning.

## Metrics

- Trajectory-level precision, recall, F1 and false-positive rate.
- Abstention rate for Heavy Auditor.
- Evidence quote grounding: whether excerpts occur verbatim in the supplied trace and cited step IDs exist.
- Per-model and per-task breakdown.
- Cost and latency.

The HF table does not provide independent gold evidence-step annotations. Quote grounding is therefore not gold step-localization accuracy.

## Execution

Install requirements-experiment.txt, then set OPENAI_BASE_URL, OPENAI_API_KEY and RH_LLM_MODEL. The endpoint must implement OpenAI-compatible chat completions; a local vLLM server can be used.

Prepare the deterministic split without inference:

    python3 scripts/run_hybrid_experiment.py --prepare-only

Run the multi-round experiment:

    python3 scripts/run_hybrid_experiment.py --model "$RH_LLM_MODEL" --rounds v0,v1,v2,v3 --run-heavy

The script writes split manifests, round metrics and predictions under experiments/results/. These local results are ignored by Git; review them before promoting the best Skill files.

## Interpretation limits

- One Terminal Wrench-derived source; this is not cross-benchmark generalization.
- Baselines are canonical successful prechecks, not newly human-audited negatives.
- Sanitization fidelity is inherited from the dataset's published pipeline.
- No model weights are fine-tuned.
- No experiment result is claimed until an inference endpoint has actually run the script.
