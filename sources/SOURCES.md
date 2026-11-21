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

## 4. 各公开数据集实际覆盖的任务（2026-11-21 核实）

> 这里区分 **底层 agent 任务** 与 **Reward Hacking 类型**；以下是数据集公开说明中的任务范围，不等于本仓库已下载。数量与来源可能更新；请沿链接查看原始任务或数据卡。

| 数据集 | 底层任务 / 例子 | 样本类型与标注 | 本仓库 |
|---|---|---|---|
| [Terminal Wrench](https://github.com/few-sh/terminal-wrench) | 331 个 terminal-agent 任务：系统管理（QEMU/SSH）、软件工程、SQL/编译、ML training（CartPole/Titanic）、安全等；任务来自 Terminal-Bench 2、TerminalBench Pro、OpenThoughts-TB-dev、SETA、TerminalBench-original | 3,632 条有奖励的 hack trajectories；同时有合法 baseline、合法对抗求解和失败攻击；攻击经诱导 elicited | 已整理其中 20 个案例（并非 20 个独立原始 Benchmark） |
| [CheatBench](https://huggingface.co/datasets/steinad/CheatBench) | 9 个家族：Terminal-Bench 2（终端）、CyBench（安全）、SWE-smith / SWE-bench Verified / SWE-rebench（修代码）、HAL-USACO（算法题）、MLE-bench（ML）、BountyBench（安全修复）、KernelBench（内核优化） | 4,472 条：844 cheating、41 failed attempt、3,587 benign/未足粒度审计；偏自然发生，并有 localization | 仅来源链接 |
| [TRACE](https://huggingface.co/datasets/PatronusAI/trace-dataset) | 37+ 工程领域：Finance、ML/AI、IoT/Embedded、Testing、Backend、DevOps 等；模拟 Bash/Read/Write/Edit/Grep/WebSearch 等工具使用 | 517 条 **合成**轨迹（268 hack / 249 benign），10 大类、54 细分攻击方式；有人工验证 | 仅来源链接 |
| [HackBench / Meta](https://huggingface.co/datasets/facebook/hackbench) | 13 个长时 ML research agent 任务：5 个 ResearchGym + 7 个 AutoLab Model Development + 1 个 automated-w2s-research；优化训练指标与研究代码 | 169 条带作弊的长轨迹：41 natural + 128 synthetic injection；附精确 hacked command indices，**非通用 benign/hack 二分类数据集** | 仅来源链接 |
| [MALT / METR](https://huggingface.co/datasets/metr-evals/malt-public) | 公开部分覆盖 30 个 task families、169 个 agentic tasks；数据卡未公开完整 family 名称，不应凭空补全；涉及任务约束、hardcoding、refusal/sabotage、模型能力表现 | 混合 unprompted / prompted；`bypass_constraints`、`hardcoded_solution`、`ignores_task_instructions`、`sabotage`、`match_weaker_model` 等标签；需要 HF 登录同意访问条件 | 仅来源链接 |
| [Goodfire reward-hack-data](https://huggingface.co/datasets/Goodfire/reward-hack-data) | SWE-bench Verified / DeepSWE（软件工程）、ImpossibleBench（LiveCodeBench / tools）、τ³-bench（工具化客服与任务流）、ShoppingBench（购物代理） | 完整 rollout + 多次 LLM judge 或 generic monitor；**不同子集的“标签”证据等级不同，不能一律当作人工 ground truth** | 仅来源链接 |
| [BenchJack](https://github.com/benchjack/benchjack) | 审计 SWE-bench Verified / Pro、Terminal-Bench、WebArena、FieldWorkArena、OSWorld、GAIA、CAR-bench 等 | 基准评测漏洞、PoC 与审计报告；**不是统一的 agent trajectory benchmark** | 仅方法参考 |

### 最值得优先扩展的来源

- **自然发生 + 负例：CheatBench**（需要注意其中 benign 可能包含审计粒度不足的轨迹）。
- **长轨迹定位：HackBench**（与 20 个短 trajectory 案例互补）。
- **可控合成标签：TRACE**（合成到自然真实表现要跨域测）。
- **评测边界审计：BenchJack；多场景：Goodfire、MALT**。

