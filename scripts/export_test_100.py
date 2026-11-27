#!/usr/bin/env python3
"""Export ONLY the locked 100 test tool-call trajectories, with no labels or source metadata."""
import argparse,json,pathlib,hashlib
from run_hybrid_experiment import make_split

def view(s):
  steps=[]
  for st in s["trace"].get("steps",[]):
    if st.get("source")!="agent":continue
    cmds=[]
    for c in st.get("tool_calls") or []:
      for k,v in (c.get("arguments") or {}).items():
        if isinstance(v,str) and k.lower() in ("keystrokes","command","cmd","script","code","file_path","path","content"):
          cmds.append(v)
    steps.append({"step_id":st.get("step_id"),"commands":cmds})
  return {"sample_id":s["sample_id"],"task_prompt":s["prompt"],"trace_steps":steps}
def main():
 p=argparse.ArgumentParser();p.add_argument("--seed",type=int,default=211126);a=p.parse_args()
 tr,te,m=make_split(a.seed)
 assert len(te)==100 and not(set(x["task_id"] for x in tr)&set(x["task_id"] for x in te))
 out=pathlib.Path("experiments/locked_test_inputs");out.mkdir(parents=True,exist_ok=True)
 rows=[view(s) for s in te]
 with (out/"test_semantic_100.jsonl").open("w") as f:
  for r in rows:f.write(json.dumps(r,ensure_ascii=False)+"\n")
 ids=hashlib.sha256("\n".join(sorted(r["sample_id"] for r in rows)).encode()).hexdigest()
 (out/"manifest.json").write_text(json.dumps({"n":100,"seed":a.seed,"test_sample_ids_sha256":ids,"labels_included":False,"source_kind_included":False,"note":"locked test; score only using frozen configs; do not tune"},indent=2)+"\n")
 print("exported locked test",len(rows),"hash",ids)
if __name__=="__main__":main()
