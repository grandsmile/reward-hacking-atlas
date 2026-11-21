# Scripts: quick start

Python 3 standard library only; run commands from the repository root.

```bash
# Download one case (or use --all)
python3 scripts/fetch_cases.py --case case_014

# Rule-only suspicious-command indexing
python3 scripts/index.py --trace cases/case_014/raw/hack_trajectory.json --task cases/case_014/raw/task_instruction.md --mode commands

# Compare 20 hack traces with 20 matched baseline successful prechecks
python3 scripts/fetch_cases.py --all
python3 scripts/evaluate.py --mode commands
python3 scripts/evaluate.py --mode with-agent-messages --output reports/indexer_pilot_with_agent_messages.json

# Offline unit tests
python3 -m unittest discover -s scripts -p 'test_*.py'
```

### Inputs and outputs

- `cases_manifest.json` stores the task/model/variant identifiers, a **fixed source revision** and upstream gold step IDs. Gold IDs are used only by `evaluate.py` after detector predictions have been generated.
- `fetch_cases.py` downloads original instructions, attack ATIF trajectory, legitimate baseline precheck, upstream audit and source task metadata. It saves a local SHA256 download manifest.
- `index.py` reads original task instructions plus agent ATIF `steps[]` and returns `status`, `strong_signal`, `triage_candidate` and evidence findings with `step_id`.
- `evaluate.py` produces confusion-matrix counts for both strong evidence and broad triage, plus reference-step recall.

### Boundaries

Do not run any commands found inside downloaded traces. An agent saying 'bypass' is not independently sufficient evidence of cheating, and merely reading tests can be normal development. Heavy LLM analysis is currently a Skill protocol, not an executable runner. No cross-dataset generalization is claimed.
Baseline labels are inherited successful prechecks and should not be treated as independently audited 'clean' ground truth.
