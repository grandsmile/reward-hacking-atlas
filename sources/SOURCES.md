# Source Registry — 公共资料与追溯信息

> 本版只把 **Terminal Wrench** 的 20 个案例收进 casebook；其他资源仅作后续扩展候选，**没有**声称已取得、合并或复核它们的原始轨迹。字段、许可、下载权限应按后续拉取时的最新数据卡确认。

## 1. 实际使用的案例来源

- **Terminal Wrench**：https://github.com/few-sh/terminal-wrench  
  Fixed revision: [d8a29613235a0ef56a8b70b3142626a533da28c2](https://github.com/few-sh/terminal-wrench/tree/d8a29613235a0ef56a8b70b3142626a533da28c2)  
  Case-level folders: `tasks/<task>/<model>/original_task/instruction.md`, `hack_trajectories/<variant>/trial/agent/trajectory.json`, `baseline_trajectories/1/trial/agent/trajectory.json`, `task.json`, `tasks/<task>/hack_summary.md`。  
  Data provenance: elicited rewarded exploits; task families recorded individually in the upstream `task.json`.  
  Current status: 20 case summaries and source-linked full trajectories; **not independently relabeled**; no raw large data duplicated in this repository.

## 2. 后续扩展来源（目前只记录链接）

| Source | URL | Potential role | Ingestion status |
|---|---|---|---|
| CheatBench | https://huggingface.co/datasets/steinad/CheatBench | More naturally observed reward hacking and negatives, mechanism labels | Not ingested |
| TRACE | https://huggingface.co/datasets/PatronusAI/trace-dataset | Synthetic / human-verified examples and fine-grained patterns | Not ingested |
| HackBench (Meta) | https://huggingface.co/datasets/facebook/hackbench | Long trajectories and command localization | Not ingested |
| MALT (METR) | https://huggingface.co/datasets/metr-evals/malt-public | Natural and prompted trajectories; some data may require access approval | Not ingested |
| Goodfire reward-hack-data | https://huggingface.co/datasets/Goodfire/reward-hack-data | Additional judge/monitor data of varied provenance | Not ingested |
| BenchJack | https://github.com/benchjack/benchjack | Benchmark vulnerability and verifier auditing reference | Reference only |

## 3. Future schema minimum

Store: `source_id`, `source_revision`, `original_task`, `trace_url`, `origin`, `native_label`, `mechanism`, `failure_mode`, `key_steps`, `evidence_level`, `license`. Do not merge natural, elicited and synthetic cases into one undifferentiated evaluation population. Preserve attribution and honor source licenses before copying full traces.
