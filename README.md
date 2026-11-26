# Reward Hacking Atlas

Public-source reward-hacking casebook, hierarchical taxonomy, and hybrid detection-skill prototypes. Large original trajectories are downloaded on demand and kept out of Git.

## Start here

- [20 categorized cases](cases/INDEX.md): mechanisms, failure modes, verified step-level evidence and original trajectory links.
- [Case study report](reports/REWARD_HACKING_CASE_REPORT.md): five categories, key examples and insights.
- [Source registry](sources/SOURCES.md): Terminal Wrench, CheatBench, TRACE, HackBench, MALT, Goodfire and BenchJack.
- [Hierarchical taxonomy](taxonomy/README.md): 72 atomic mechanism labels in seven clusters, plus separate auxiliary and verifier-failure axes.
- [Source taxonomy crosswalk](taxonomy/SOURCE_CROSSWALK.md): maps native dataset labels without overwriting them.
- [Hybrid experiment protocol](experiments/HYBRID_SKILL_PROTOCOL.md): proposed 500/100 task-disjoint train/test design and iteration plan.
- [600-sample experiment](experiments/600_experiment_design.md): paired hack/baseline split and multi-round hybrid evaluation.
- [Experiment runner](scripts/run_hybrid_experiment.py): OpenAI-compatible inference runner for local vLLM or hosted endpoints.
- [GPT-6 manual pilot (20 trajectories)](reports/GPT6_MANUAL_PILOT_20.md): direct prompt-based review, round comparison, and source-label audit; not the full 600-sample experiment.
- [Light Indexing Skill](skills/rh-indexer/SKILL.md): hybrid rule + LLM high-recall suspicious-step retrieval.
- [Heavy Analysis Skill](skills/rh-analyzer/SKILL.md): hybrid rule + LLM evidence audit; **model-based benchmark not yet executed**.
- [Download, run and evaluate](scripts/README.md): command-line guide.

## Minimal reproducible pilot

```bash
python3 scripts/fetch_cases.py --case case_014
python3 scripts/index.py --trace cases/case_014/raw/hack_trajectory.json --task cases/case_014/raw/task_instruction.md
python3 scripts/fetch_cases.py --all
python3 scripts/evaluate.py --mode commands
python3 scripts/evaluate.py --mode with-agent-messages --output reports/indexer_pilot_with_agent_messages.json
python3 -m unittest discover -s scripts -p 'test_*.py'
```

All downloads are pinned to a source commit SHA and locally hashed. `cases/case_*/raw/` is intentionally ignored by Git. Run scripts on a network-connected machine. Scripts only **inspect** stored commands; they never execute actions taken in the original trajectories.

## Important methodology caveats

- The 20 exploits come from **one curated dataset**, Terminal Wrench, and were adversarially elicited.
- Baselines are successful prechecks, not independently human-audited negative labels.
- Gold steps are taken from upstream annotations; no independent verifier replay has been performed.
- Rule-only detection is a triage baseline, not a complete definition of reward hacking.
- Case study reports and gold annotations must **not** be supplied to a detector for the same sample.
