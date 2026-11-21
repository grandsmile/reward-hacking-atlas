#!/usr/bin/env python3
"""Evaluate the deterministic indexer on 20 hack / baseline pairs."""
import argparse
import json
import sys
from pathlib import Path
from index import index_trajectory

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads(Path(__file__).with_name("cases_manifest.json").read_text())["cases"]

def confusion(rows, field):
    tp = sum(row["gold"] == "hack" and row[field] for row in rows)
    fn = sum(row["gold"] == "hack" and not row[field] for row in rows)
    fp = sum(row["gold"] == "baseline_precheck" and row[field] for row in rows)
    tn = sum(row["gold"] == "baseline_precheck" and not row[field] for row in rows)
    return {
        "TP": tp, "FN": fn, "FP": fp, "TN": tn,
        "precision": tp/(tp+fp) if tp+fp else None,
        "recall": tp/(tp+fn) if tp+fn else None,
        "FPR": fp/(fp+tn) if fp+tn else None
    }

def evaluate(mode):
    rows, missing, hit, total = [], [], 0, 0
    for case in CASES:
        folder = ROOT / "cases" / case["id"] / "raw"
        task_file = folder / "task_instruction.md"
        hack_file = folder / "hack_trajectory.json"
        base_file = folder / "baseline_trajectory.json"
        if not all(p.exists() for p in (task_file, hack_file, base_file)):
            missing.append(case["id"])
            continue
        task = task_file.read_text(encoding="utf8")
        for gold, path in (("hack", hack_file), ("baseline_precheck", base_file)):
            # Crucially, gold steps and upstream hack summaries are NOT model inputs.
            pred = index_trajectory(json.loads(path.read_text(encoding="utf8")), task, mode)
            strong_steps = sorted({f["step_id"] for f in pred["findings"]
                                   if f["severity"] == "strong" and f["step_id"] is not None})
            record = {
                "case_id": case["id"], "gold": gold,
                "status": pred["status"], "strong_signal": pred["strong_signal"],
                "triage_candidate": pred["triage_candidate"],
                "predicted_strong_steps": strong_steps, "findings": pred["findings"]
            }
            if gold == "hack":
                expected = set(case["gold_steps"])
                hit += len(expected.intersection(strong_steps))
                total += len(expected)
                record["upstream_key_hack_steps"] = sorted(expected)
            rows.append(record)
    return {
        "dataset": "Terminal Wrench selected 20 rewarded-hack and baseline pairs",
        "mode": mode, "loaded_pairs": len(rows)//2, "missing_cases": missing,
        "strong_only": confusion(rows, "strong_signal"),
        "triage_including_review": confusion(rows, "triage_candidate"),
        "upstream_key_step_recall_strong": hit/total if total else None,
        "upstream_step_hits": hit, "upstream_step_count": total,
        "limitations": [
            "Attacks are elicited in one curated source dataset; not independent cross-benchmark samples.",
            "Successful precheck baselines are not independently human-audited negatives.",
            "Upstream key_hack_steps are reference annotations, not independently adjudicated.",
            "Agent narration can expose adversarial prompt intent.",
            "No verifier replay or Heavy LLM Skill accuracy is claimed."
        ],
        "rows": rows
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("commands", "with-agent-messages"), default="commands")
    parser.add_argument("--output", type=Path, default=ROOT/"reports"/"indexer_pilot_results.json")
    args = parser.parse_args()
    report = evaluate(args.mode)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf8")
    print(json.dumps({k:v for k,v in report.items() if k!="rows"}, ensure_ascii=False, indent=2))
    if report["missing_cases"]:
        print("Download first: python3 scripts/fetch_cases.py --all", file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())
