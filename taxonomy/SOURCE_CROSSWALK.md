# Source Taxonomy Crosswalk

This is a normalization guide, not a claim that source labels are perfectly equivalent.

## Terminal Wrench (11 native observed categories)

| Native label | Suggested RH mapping | Notes |
|---|---|---|
| `hollow-implementation` | RH-010, RH-013, RH-018, RH-062 | Coarse label; inspect the actual implementation before choosing a leaf. |
| `output-spoofing` | RH-007, RH-055 | Distinguish hardcoded task output from fabricated metric/report files. |
| `constraint-loophole` | RH-063 | Literal wording versus intended task contract. |
| `structural-extraction` | RH-071, RH-039 | Verifier/test source or metadata extraction. |
| `binary-hijacking` | RH-067 | Executable, standard-library, or toolchain replacement. |
| `keyword-gaming` | RH-072 | Static-analyzer surface evasion. |
| `algorithmic-simplification` | RH-018, RH-019, RH-024 | Task-specific mapping; a simple algorithm is not inherently a hack. |
| `mutable-input-tampering` | RH-044, RH-046, RH-069 | Global, file, or persistent-state manipulation. |
| `metric-spoofing` | RH-055, RH-056, RH-057 | Fabricated score, reward channel, or measurement boundary. |
| `security-downgrading` | RH-064 | Security controls weakened while appearing compliant. |
| `deceptive-rationalization` | AUX-01 | Narrative tag, not a mechanism. |

## CheatBench native labels

| Native label | Suggested mapping |
|---|---|
| `harness_leaks_answer` | RH-070 |
| `harness_leaks_verifier` | RH-071 |
| `secret_discovery_in_environment` | RH-039 / RH-046; inspect trace |
| `secret_discovery_via_web_search` | RH-041 |
| `verifier_exploitation` | Requires trace-level mapping |
| `unresolved_mechanism` | Keep unresolved; do not invent a leaf |

CheatBench's `cheating_type` (harness/task) is a coarse target distinction, not an atomic mechanism.

## TRACE

TRACE Appendix G's 54 subcategories are retained as RH-001–RH-054 in the exact source order:
- C01 Test Suite Exploitation: RH-001–RH-017
- C02 Solution Quality Degradation: RH-018–RH-034
- C03 Context Exploitation: RH-035–RH-043
- C04 Execution Environment Hacks: RH-044–RH-054

Keep the original TRACE category and subcategory strings in `source_native_labels`.

## HackBench

| Native category | Suggested mapping |
|---|---|
| Fabrication | RH-055 |
| Grader hijack | RH-066 / RH-067 |
| Label leakage | RH-060; add RH-070/RH-071 if source is harness/verifier |
| Omission | RH-058 |
| Synthetic substitution | RH-061 |
| Skip the work | RH-062 |
| Overfitting | RH-008 or RH-060 depending on evidence |
| Measurement exploit | RH-057 |

## MALT

| Native tag | Treatment |
|---|---|
| `bypass_constraints`, `ignores_task_instructions` | RH-065 when reward-relevant |
| `hardcoded_solution` | RH-007 / RH-018 |
| `sabotage` | AUX-04; RH only if it manipulates reward or measured objective |
| `refusals`, `gives_up`, `partial_problem_solving` | AUX-05 / AUX-07; not automatically RH |
| `match_weaker_model` | AUX-06 |
| `evaluation_awareness`, `reasoning_about_task` | AUX-03 |

## BenchJack V1–V8

BenchJack classes describe **verifier/harness failure modes**, not agent action mechanisms. Store them in `failure_mode_ids`:

| Class | Failure mode |
|---|---|
| V1 | Isolation Failure |
| V2 | Answers Shipped with the Test |
| V3 | RCE on Untrusted Input |
| V4 | LLM Judge Without Sanitization |
| V5 | Weak String Matching |
| V6 | Evaluation Logic Gaps |
| V7 | Trusting Untrusted Code Output |
| V8 | Unnecessary Permissions |

Do not merge V1–V8 into RH mechanism leaves. One agent action may trigger multiple failure modes, and one failure mode may enable multiple actions.
