#!/usr/bin/env python3
"""Export TRAIN ONLY from deterministic task-disjoint 500/100 split for skill refinement.

Do not upload or read TEST data here. Original trajectory commands are text evidence
and MUST NEVER be executed.
"""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path
from run_hybrid_experiment import make_split

ROOT=Path(__file__).resolve().parents[1]
def canonical(sample):
  steps=[]
  for s in sample["trace"].get("steps",[]):
    if s.get("source")!="agent":continue
    cmds=[]
    for c in s.get("tool_calls") or []:
      args=c.get("arguments") or {}
      for k,v in args.items():
        if isinstance(v,str) and k.lower() in ("keystrokes","command","cmd","script","code","file_path","path","content"):
          cmds.append(v)
    obs=s.get("observation")
    if isinstance(obs,dict):
      obs="\n".join(str(r.get("content","")) for r in obs.get("results",[]) if isinstance(r,dict))
    elif obs is None:obs=s.get("tool_results") or ""
    steps.append({
      "step_id":s.get("step_id"),
      "message":str(s.get("message") or "")[:1800],
      "commands":cmds,
      "observation":str(obs)[:3500]
    })
  return {
    "sample_id":sample["sample_id"],
    "label":int(sample["label"]),
    "task_id":sample["task_id"],
    "model":sample.get("model"),
    "task_prompt":sample["prompt"],
    "trace_steps":steps,
    "source_kind":sample["kind"],
    "source_variant":sample.get("variant"),
    "trace_sha256":hashlib.sha256(json.dumps(sample["trace"],sort_keys=True,ensure_ascii=False).encode()).hexdigest()
  }

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--seed",type=int,default=211126)
 args=ap.parse_args()
 train,test,m=make_split(args.seed)
 assert len(train)==500 and len(test)==100
 assert len(set(s["task_id"] for s in train)&set(s["task_id"] for s in test))==0
 out=ROOT/"experiments"/"train_export"
 out.mkdir(exist_ok=True,parents=True)
 with (out/"train_semantic_500.jsonl").open("w") as f:
  for s in train:f.write(json.dumps(canonical(s),ensure_ascii=False)+"\n")
 # Compact reference for audit; no test traces or labels are persisted.
 (out/"manifest.json").write_text(json.dumps({
   "dataset":m["dataset"],"seed":args.seed,"n_train":len(train),
   "train_task_count":len(set(s["task_id"] for s in train)),
   "test_task_count":len(set(s["task_id"] for s in test)),
   "task_disjoint":m["task_disjoint"],
   "note":"ONLY TRAIN rows exported. Do not use labels or source_kind in any model inputs."
 },indent=2)+"\n")
 print("EXPORTED TRAIN",len(train),"bytes",(out/"train_semantic_500.jsonl").stat().st_size)

if __name__=="__main__":main()
