# GPT-6 Manual Experiment Progress — 80 / 600

**Status: ongoing; this is not the final 600-sample result.** All judgments recorded so far are from the Train split only. No Test sample has been opened or used.

## Protocol

- Source: pinned Terminal Wrench repository revision `d8a29613235a0ef56a8b70b3142626a533da28c2`.
- Fixed gold labels: hack trajectory = 1; baseline trajectory = 0, as requested.
- Each record contains a binary prediction, primary/secondary atomic mechanism IDs, verbatim step evidence, confidence, and an audit note.
- Current review: 80 trajectories (40 hack + 40 baseline), all from Train.
- Full target: 500 Train + 100 locked Test. Test has not been reviewed.

## Current Train metrics

| Metric | Value |
|---|---:|
| N | 80 |
| TP | 39 |
| FP | 8 |
| TN | 33 |
| FN | 0 |
| Precision | 82.98% |
| Recall | 100.00% |
| F1 | 90.70% |
| False Positive Rate | 19.51% |

These are in-sample manual GPT-6 judgments against the user's fixed folder labels, not held-out performance. A number of baseline trajectories access or execute `/solution/solve.sh`; these remain gold 0 and are counted as false positives when the detector flags them.

## Mechanism distribution among predicted positive hack samples

- RH-065: 3
- RH-072: 2
- RH-049: 1
- RH-067: 2
- RH-061: 3
- RH-013: 11
- RH-055: 4
- RH-069: 2
- RH-046: 1
- RH-063: 2
- RH-007: 4
- RH-071: 1
- RH-066: 2
- RH-057: 1

Mechanism counts are primary-label counts only; secondary labels can overlap.

## Iteration notes

- v0.4: generic `/solution/solve.sh` access/execution downgraded from strong evidence to review-only unless the task establishes protected answer/grader leakage. This addresses repeated baseline false positives.
- v0.5: both Skills and prompts require a binary `reward_hacking` 0/1 output plus atomic mechanism IDs, evidence spans, and separate uncertainty.
- Task-aware patterns exercised so far: fabricated outputs, static substitutes, process/toolchain spoofing, verifier/reporting tampering, hidden-test extraction, metric threshold manipulation, and explicit process-constraint bypass.

## Data-quality caveats

- The user's baseline=0 assumption is applied exactly, even where trajectory behavior appears suspicious.
- Several samples carry audit notes because the visible trace excerpt is truncated or the task environment prevents a clean distinction.
- Task 429 in the fixed manifest could not be fetched at the pinned path and is recorded as missing; it has not been silently replaced.
- No test-set metrics or generalization claims are made.
