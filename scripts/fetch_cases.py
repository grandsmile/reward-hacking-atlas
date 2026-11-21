#!/usr/bin/env python3
"""Fetch pinned Terminal Wrench case assets, without running the agent's commands."""
import argparse
import hashlib
import json
import sys
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((Path(__file__).with_name("cases_manifest.json")).read_text())
LIMIT = 20 * 1024 * 1024

def paths(case):
    base = "tasks/{}/{}".format(case["task"], case["model"])
    version = case["variant"]
    return {
        "task_instruction.md": "{}/original_task/instruction.md".format(base),
        "hack_trajectory.json": "{}/hack_trajectories/{}/trial/agent/trajectory.json".format(base, version),
        "baseline_trajectory.json": "{}/baseline_trajectories/1/trial/agent/trajectory.json".format(base),
        "task_metadata.json": "{}/task.json".format(base),
        "hack_summary.md": "tasks/{}/hack_summary.md".format(case["task"]),
    }

def fetch_one(case, overwrite=False):
    out = ROOT / "cases" / case["id"] / "raw"
    out.mkdir(parents=True, exist_ok=True)
    assets, errors = {}, {}
    for name, relative in paths(case).items():
        url = "https://raw.githubusercontent.com/{}/{}/{}".format(
            MANIFEST["source_repo"], MANIFEST["source_revision"], relative)
        path = out / name
        try:
            if path.exists() and not overwrite:
                data = path.read_bytes()
                state = "cached"
            else:
                with urlopen(Request(url, headers={"User-Agent": "reward-hacking-atlas/0.2"}), timeout=40) as stream:
                    data = stream.read(LIMIT + 1)
                if len(data) > LIMIT:
                    raise ValueError("Asset over 20 MB")
                if name.endswith(".json"):
                    parsed = json.loads(data)
                    if name.endswith("_trajectory.json") and not isinstance(parsed.get("steps"), list):
                        raise ValueError("Expected ATIF steps[]")
                path.write_bytes(data)
                state = "downloaded"
            assets[name] = {
                "url": url, "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": len(data), "status": state
            }
        except Exception as exc:
            errors[name] = "{}: {}".format(type(exc).__name__, exc)
    result = {
        "case_id": case["id"], "source_revision": MANIFEST["source_revision"],
        "assets": assets, "errors": errors
    }
    (out / "download_manifest.json").write_text(json.dumps(result, indent=2) + "\n")
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true")
    group.add_argument("--case", help="case_014")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    cases = MANIFEST["cases"] if args.all else [
        c for c in MANIFEST["cases"] if c["id"] == args.case]
    if not cases:
        parser.error("Unknown case ID")
    failed = False
    for case in cases:
        result = fetch_one(case, args.overwrite)
        print("{}: {}/{} assets, {} errors".format(
            case["id"], len(result["assets"]), len(paths(case)), len(result["errors"])))
        for name, error in result["errors"].items():
            print(name, error, file=sys.stderr)
        failed |= bool(result["errors"])
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
