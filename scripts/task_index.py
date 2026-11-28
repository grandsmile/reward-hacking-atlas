#!/usr/bin/env python3
"""Read-only task/environment attack-surface scanner. Does not execute task files."""
from __future__ import annotations
import argparse, json, re, stat
from pathlib import Path

SKIP_PARTS={".git","__pycache__","solution","oracle","trajectories","agent","runs"}
TEXT_SUFFIXES={".md",".txt",".toml",".yaml",".yml",".json",".py",".sh",".cfg",".ini",".conf",".env",".service",".xml",".js",".ts",".sql",".dockerfile"}
PATTERNS={
 "T01":[r"ground[_ -]?truth",r"gold[_ -]?(?:label|answer)",r"answer[_ -]?key",r"expected[_ -]?(?:answer|output)",r"hidden[_ -]?test"],
 "T02":[r"tests?/",r"grader",r"verifier",r"pytest",r"assert\s+",r"monkeypatch"],
 "T03":[r"reward\.txt",r"score\.txt",r"reward\s*=",r"write_text\(.*reward",r"open\(.*(?:reward|score).*(?:w|a)"],
 "T04":[r"/var/run/",r"/var/lib/",r"/tmp/",r"shared[_ -]?volume",r"privileged:\s*true",r"network_mode:\s*host"],
 "T05":[r"/usr/bin/(?:python|node|gcc|g\+\+)",r"/usr/local/bin/",r"PATH\s*=",r"LD_PRELOAD",r"sitecustomize\.py"],
 "T06":[r"network[_ -]?egress",r"allow[_ -]?internet",r"curl\b",r"wget\b",r"requests\.get",r"network_mode"],
 "T07":[r"process[_ -]?attest",r"must use",r"required tool",r"only via",r"must run",r"subprocess"],
 "T08":[r"tests?/",r"fixtures?/",r"conftest\.py",r"assert\s+",r"expected"],
 "T09":[r"train(?:ing)?[_ -]?(?:set|data)",r"validation",r"holdout",r"test[_ -]?(?:set|labels?)",r"ground[_ -]?truth"],
 "T10":[r"llm[_ -]?judge",r"judge[_ -]?prompt",r"system prompt",r"untrusted.*(?:prompt|instruction)",r"tool output"]
}
RH_MAP={
 "T01":["RH-038","RH-060","RH-070","RH-071"],
 "T02":["RH-001","RH-002","RH-003","RH-066","RH-072"],
 "T03":["RH-055","RH-056","RH-057"],
 "T04":["RH-044","RH-045","RH-046","RH-069"],
 "T05":["RH-065","RH-067"],
 "T06":["RH-041","RH-047","RH-065"],
 "T07":["RH-007","RH-013","RH-018","RH-061","RH-062","RH-063","RH-065"],
 "T08":["RH-001","RH-002","RH-003","RH-066"],
 "T09":["RH-038","RH-060"],
 "T10":["RH-068"]
}
FM_MAP={
 "T01":["V2"],"T02":["V1","V6"],"T03":["V1","FM-10"],"T04":["V1","V8","FM-11"],
 "T05":["V1","V8"],"T06":["V6"],"T07":["FM-09","V6"],"T08":["V1","V5","V6"],
 "T09":["V2","FM-10"],"T10":["V4"]
}
def should_skip(p:Path, root:Path):
    rel=p.relative_to(root)
    return any(x in SKIP_PARTS for x in rel.parts)
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("task_dir",type=Path)
    ap.add_argument("--max-bytes",type=int,default=1_000_000)
    ap.add_argument("--output",type=Path)
    a=ap.parse_args()
    root=a.task_dir.resolve()
    if not root.is_dir(): raise SystemExit("task_dir must be a directory")
    findings=[]; inventory=[]; unknown=[]
    for p in sorted(root.rglob("*")):
        if not p.is_file() or should_skip(p,root): continue
        rel=str(p.relative_to(root))
        try:
            st=p.stat()
            mode=stat.filemode(st.st_mode)
            inventory.append({"path":rel,"size":st.st_size,"mode":mode})
            if st.st_size>a.max_bytes: unknown.append({"path":rel,"reason":"over max-bytes"});continue
            if p.suffix.lower() not in TEXT_SUFFIXES and p.name.lower() not in {"dockerfile","makefile"}: continue
            txt=p.read_text(encoding="utf-8",errors="replace")
        except OSError as e:
            unknown.append({"path":rel,"reason":str(e)});continue
        for lineno,line in enumerate(txt.splitlines(),1):
            for risk,patterns in PATTERNS.items():
                for pattern in patterns:
                    if re.search(pattern,line,re.I):
                        findings.append({"risk_id":risk,"evidence_file":rel,"line":lineno,
                         "excerpt":line.strip()[:300],"rule":pattern,
                         "possible_rh_mechanisms":RH_MAP[risk],"possible_failure_modes":FM_MAP[risk],
                         "status":"candidate_not_confirmed"})
                        break
    payload={"task_dir":str(root),"verdict":"incomplete" if unknown else ("exposed" if findings else "no_issue_found_in_scope"),
      "inventory":inventory,"rule_candidates":findings,"unassessed":unknown,
      "warning":"Static scan only. A candidate is not proof of reachability or exploitability. Verify container mounts, runtime user, network policy and verifier boundary with LLM/human review."}
    s=json.dumps(payload,ensure_ascii=False,indent=2)+"\n"
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    else:print(s,end="")
if __name__=="__main__":main()
