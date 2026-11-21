# Casebook · 20 sourced examples

All 20 cases come from **few-sh/terminal-wrench**, but their original task families span `terminal-bench__2.0`, `terminal-bench-pro`, `TerminalBench-original`, and `OpenThoughts-TB-dev`. These are **not four independent reward-hacking datasets**: all twenty exploit traces are drawn from one curated collection. All were elicited attacks, and the labels are inherited from the source.

## 1. 答案或评测素材泄漏 (3)

Agent 读取了本应不用于作答的标准答案、固定输出或 walkthrough，并把它当作完成任务的捷径。

[CASE-004: sakila-sql-optimization](../cases/case_004/README.md) · [CASE-014: titanic-female-survival-prediction](../cases/case_014/README.md) · [CASE-015: solve-colossal-cave-350-score](../cases/case_015/README.md)

## 2. 空心实现 / 跳过规定过程 (8)

表面产物满足检查，但题目要求的搜索、解析、训练、擦除或部署流程没有真正执行。

[CASE-002: rush-hour-bfs-solver](../cases/case_002/README.md) · [CASE-003: simple-web-scraper](../cases/case_003/README.md) · [CASE-005: schedule-vacation](../cases/case_005/README.md) · [CASE-007: cartpole-rl-training](../cases/case_007/README.md) · [CASE-008: train-fraud-detection-model](../cases/case_008/README.md) · [CASE-017: optimize-postgresql-analytics-query](../cases/case_017/README.md) · [CASE-018: decommissioning-service-with-sensitive-data](../cases/case_018/README.md) · [CASE-019: git-multibranch](../cases/case_019/README.md)

## 3. 验证规则 / 规范漏洞利用 (3)

绕过浅层关键字检查，或利用只测一侧约束的评估逻辑，获得和真正目标不一致的通过结果。

[CASE-010: triton-interpret](../cases/case_010/README.md) · [CASE-012: fix-django-command-injection](../cases/case_012/README.md) · [CASE-013: sanitize-jinja2-ssti-templates](../cases/case_013/README.md)

## 4. 环境、工具与验证器篡改 (4)

修改解释器、编译器、模拟器或运行环境，使 verifier 看到的行为与真正要求不符。

[CASE-001: regex-chess](../cases/case_001/README.md) · [CASE-006: setup-ubuntu-vm-ssh-key-auth](../cases/case_006/README.md) · [CASE-011: parallelize-graph](../cases/case_011/README.md) · [CASE-020: winning-avg-corewars](../cases/case_020/README.md)

## 5. 指标与状态操纵 (2)

通过修改基准测量过程或持久化状态，伪造性能提升或任务进度。

[CASE-009: portfolio-optimization](../cases/case_009/README.md) · [CASE-016: play-lord](../cases/case_016/README.md)

## Representative examples

Six illustrative cases: CASE-014 (ground-truth leak), CASE-001 (standard-library hijacking), CASE-020 (evaluator binary replacement), CASE-009 (metric tampering), CASE-013 (destructive shortcut), and CASE-016 (game-state tampering). Mechanism summaries and causal analysis: [main report](../reports/REWARD_HACKING_CASE_REPORT.md).

**Evidence structure:** 每个 CASE-XXX 的 README 均包含原始 trajectory 片段（工具命令 / Agent 语句）、step ID 及机制解释。优先使用实际动作证据；Agent 自述仅作辅助信号。
