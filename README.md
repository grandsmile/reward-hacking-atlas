# Reward Hacking Atlas

Public-source reward-hacking casebook, detection-skill prototypes and evaluation scripts. This repository is private and keeps large original trajectories outside Git.

## Start here

- [20 categorized cases](cases/INDEX.md): mechanisms, failure modes, verified step-level evidence and original trajectory links.
- [Case study report](reports/REWARD_HACKING_CASE_REPORT.md): five categories, key examples and insights.
- [Source registry](sources/SOURCES.md): Terminal Wrench, CheatBench, TRACE, HackBench, MALT, Goodfire and BenchJack.
- [Light Indexing Skill](skills/rh-indexer/SKILL.md): rule-based suspicious-step retrieval.
- [Heavy Analysis Skill](skills/rh-analyzer/SKILL.md): LLM-facing causal-audit protocol; **not yet executed as a model-based benchmark**.
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
