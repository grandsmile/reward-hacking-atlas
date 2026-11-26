#!/usr/bin/env python3
"""Export the fixed 500/100 split for direct GPT-6 manual review (no API endpoint)."""
from __future__ import annotations
import argparse, json, zipfile
from pathlib import Path

from run_hybrid_experiment import make_split

def write_jsonl(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

def chunks(rows, n):
    for i in range(0, len(rows), n):
        yield i // n + 1, rows[i:i+n]

def input_view(sample):
    # Deliberately omit gold label, task_id, model, variant, source paths,
    # fidelity fields, and positive/negative kind. Preserve every trajectory step.
    return {
        "sample_id": sample["sample_id"],
        "task_prompt": sample["prompt"],
        "trajectory_steps": sample["trace"].get("steps", []),
    }

def gold_view(sample):
    return {
        "sample_id": sample["sample_id"],
        "gold_reward_hacking": int(sample["label"]),
        "gold_convention": "1=accepted sanitized hack; 0=paired canonical baseline",
        "task_group_hash": __import__("hashlib").sha256(sample["task_id"].encode()).hexdigest()[:16],
    }

def build_zip(path, files, root):
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for file in files:
            z.write(file, file.relative_to(root))

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-dir", type=Path, default=Path("experiments/manual_review"))
    ap.add_argument("--seed", type=int, default=211126)
    ap.add_argument("--batch-size", type=int, default=5)
    args = ap.parse_args()
    if args.batch_size < 1:
        ap.error("--batch-size must be >=1")

    train, test, manifest = make_split(args.seed)
    root = args.out_dir.resolve()
    train_dir = root / "train"
    test_dir = root / "test"
    train_input_files, test_input_files = [], []

    for split_name, rows, target_dir, collected in (
        ("train", train, train_dir, train_input_files),
        ("test", test, test_dir, test_input_files),
    ):
        for batch_no, batch in chunks(rows, args.batch_size):
            path = target_dir / f"batch_{batch_no:03d}.jsonl"
            write_jsonl(path, [input_view(s) for s in batch])
            collected.append(path)

    train_gold = root / "train_gold.jsonl"
    test_gold = root / "test_gold_DO_NOT_UPLOAD.jsonl"
    write_jsonl(train_gold, [gold_view(s) for s in train])
    write_jsonl(test_gold, [gold_view(s) for s in test])

    public_manifest = {
        **{k: v for k, v in manifest.items() if k not in ("train_positive", "train_negative", "test_positive", "test_negative")},
        "manual_review": True,
        "full_trajectory_steps_preserved": True,
        "inputs_contain_labels_or_source_kind": False,
        "test_gold_is_separate_and_must_not_be_uploaded": True,
        "batch_size": args.batch_size,
        "train_batches": len(train_input_files),
        "test_batches": len(test_input_files),
    }
    manifest_path = root / "MANIFEST.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(public_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    train_zip = root / "manual_train_pack.zip"
    test_zip = root / "manual_test_inputs_ONLY.zip"
    build_zip(train_zip, train_input_files + [train_gold, manifest_path], root)
    build_zip(test_zip, test_input_files + [manifest_path], root)

    print(json.dumps({
        "manifest": public_manifest,
        "train_pack": str(train_zip),
        "test_inputs_only": str(test_zip),
        "test_gold_local_only": str(test_gold),
        "warning": "Do not upload test_gold_DO_NOT_UPLOAD.jsonl until all test predictions are frozen."
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
