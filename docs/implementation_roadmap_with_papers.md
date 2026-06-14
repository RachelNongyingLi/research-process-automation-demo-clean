# Implementation Roadmap With Paper Support

这份文档回答一个实际问题：如果我们真的要补齐面试会追问的 LLM、RAG、向量数据库、模型评测、云端部署、scalability 和团队分工内容，应该怎么做。

当前仓库已经有可运行的 CSV ledger + Python quality gate PoC。下一步不要直接跳到“完整生产系统”，而是按三个阶段补齐证据链：

1. 面试可展示的短期补齐。
2. 真实 LLM/RAG PoC。
3. 云端/M365 部署和可扩展化。

## Phase 1: 面试可展示的短期补齐

目标：把现在的方案型 PoC 变成可复跑、可测试、可演示的 demo。这个阶段一周内最有性价比。

| 要补的内容 | 新增/修改文件 | 验收方式 | 面试价值 |
| --- | --- | --- | --- |
| 依赖管理 | `requirements.txt` 或 `pyproject.toml` | 新环境能安装依赖并运行脚本 | 说明项目不是只在本机能跑。 |
| 一键 demo | `scripts/run_demo.py` | 一条命令跑 validation + report generation | 面试现场能演示端到端流程。 |
| 最小测试 | `tests/test_validate_task_fields.py`, `tests/test_generate_progress_report.py` | `pytest` 通过 | 证明质量门逻辑有回归保护。 |
| CLI 参数 | 修改 `scripts/validate_task_fields.py`, `scripts/generate_progress_report.py` | 支持 `--data-dir`, `--output`, `--report-date` | 从 sample script 变成可复用工具。 |
| 演示说明 | `docs/demo_walkthrough.md` | 跟着文档能复现报告 | 面试时讲得清楚。 |
| 静态 dashboard | `web/index.html` 或 `app/streamlit_dashboard.py` | 展示 approval queue, claim gate, evidence risk, handoff trail | 把 CSV/Markdown 变成可视化产品原型。 |

建议先做的顺序：

1. `requirements.txt`
2. `scripts/run_demo.py`
3. `tests/`
4. `docs/demo_walkthrough.md`
5. 简单 dashboard

## Phase 2: 真实 LLM/RAG PoC

目标：证明 quality gate 不只处理手写 CSV，也能接住真实模型输出和检索结果。这个阶段是技术含金量核心，通常需要一到三周。

| 要补的内容 | 新增/修改文件 | 验收方式 | 论文支撑 |
| --- | --- | --- | --- |
| Prompt 模板 | `prompts/claim_extraction.md`, `prompts/evidence_review.md`, `prompts/style_review.md`, `prompts/report_summary.md` | 固定任务上能稳定输出结构化结果 | ReAct, Toolformer |
| 模型输出 ledger | `data/model_outputs.csv` | 保存 `model_name`, `prompt_version`, `raw_output_path`, `latency_ms`, `cost_estimate` | HELM, AgentBench |
| 模型评测集 | `data/eval_tasks.csv`, `data/model_eval_results.csv`, `docs/model_evaluation.md` | 至少 10-20 个固定任务，比较 evidence traceability 和 unsupported claim rate | HELM, AgentBench, GAIA |
| Claim extraction | `scripts/run_llm_task.py`, `scripts/extract_claims.py` | LLM 输出能转成 claim ledger 格式并被现有 validator 检查 | FIRE |
| Hallucination case study | `docs/hallucination_case_study.md`, `data/hallucination_cases.csv` | 展示模型初稿、claim gate、evidence gate、修正后输出 | SelfCheckGPT, hallucinated references paper, Chain-of-Verification |
| RAG corpus | `data/corpus/`, `data/chunks.jsonl` | 有可索引的项目文档/论文摘要/来源元数据 | RAG 2020, OpenScholar |
| Vector index | `scripts/build_corpus_index.py` | 本地生成 Chroma 或 FAISS index | RAG 2020 |
| Retriever | `scripts/query_retriever.py`, `data/retrieval_runs.csv` | claim 能检索 top-k source candidates | RAG 2020, OpenScholar |
| Retrieval-to-evidence | `scripts/promote_retrieval_to_evidence.py` | 检索结果能进入 evidence ledger，但仍标记 `verification_status` | FIRE, scientific evidence extraction |
| RAG 对比实验 | `scripts/run_rag_eval.py`, `docs/rag_poc_results.md` | 对比 pure prompt, keyword search, RAG 的 citation accuracy/evidence coverage | OpenScholar, RAG 2020 |

推荐技术选择：

- 本地 PoC：Chroma 或 FAISS。
- Azure/M365 生产版本：Azure AI Search vector index。
- Embeddings：先用可用 API 或 `sentence-transformers`，后续再换企业部署方案。
- LLM：至少比较一个强模型和一个便宜模型；先用同一批 fixed tasks，不要靠主观感觉判断哪个“最好”。

关键指标：

- claim extraction parse rate
- unsupported claim rate
- citation accuracy
- retrieval precision@k
- evidence gate pass rate
- human revision time
- latency and cost

## Phase 3: 云端/M365 部署和 scalability

目标：把本地 PoC 接到真实 workflow。这个阶段适合回答 deployment/scalability，但不要在 Phase 2 之前夸大。

| 要补的内容 | 新增/修改文件 | 验收方式 |
| --- | --- | --- |
| API/service skeleton | `service/main.py`, `service/jobs.py`, `service/models.py` | 本地 API 能触发 validation/report job |
| 容器化 | `Dockerfile`, `docker-compose.yml` | 本地容器能运行 healthcheck 和 demo job |
| SharePoint schema | `sharepoint/list_schema.md` | Tasks, AgentOutputs, Claims, Evidence, Handoffs, WorkflowRuns 字段完整 |
| M365 setup | `deploy/m365_setup.md`, `power-automate/export/` | 能手动或导入创建 intake/approval/reminder/report flows |
| Cloud deployment | `deploy/azure_app_service.md` 或 `deploy/azure_functions.md` | 有部署步骤、环境变量、secret 管理说明 |
| Sync scripts | `scripts/sync_sharepoint_lists.py`, `scripts/migrate_csv_to_sharepoint.py` | CSV 和 SharePoint list 能同步或迁移 |
| Operations | `docs/security_and_permissions.md`, `docs/operations_runbook.md` | 有权限、日志、重试、失败恢复和成本监控说明 |

端到端验收：

1. 从 Forms/Teams 创建 task。
2. Task 写入 SharePoint 或 Excel tracker。
3. Power Automate 触发 approval/reminder。
4. Python service 读取 tracker，运行 validation/report。
5. LLM/RAG 产物写回 claim/evidence ledgers。
6. Human owner 审批 delivery package。
7. Teams/email 发出 weekly report。

Scalability 设计：

- 用 `workflow_run_id` 追踪每次执行。
- 把 LLM/RAG 调用放进异步 job queue。
- 对 embeddings、retrieval results、validated evidence 做缓存。
- 对失败调用做 retry/backoff。
- 报告生成采用增量模式。
- 监控 latency、cost、failure rate、review-pass rate、unresolved blockers。

## Paper Map

| 设计点 | 推荐引用 | 为什么引用 |
| --- | --- | --- |
| Agent reasoning + tool/action loop | [ReAct, ICLR 2023](https://openreview.net/forum?id=WE_vluYUL-X) | 支持 agent 不只是生成文本，还可以交替推理和调用外部信息源。 |
| Tool use | [Toolformer, NeurIPS 2023](https://proceedings.neurips.cc/paper/2023/hash/d842425e4bf79ba039352da0f658a906-Abstract-Conference.html) | 支持模型通过工具补足事实查询、搜索、计算等能力。 |
| RAG / vector retrieval | [RAG, NeurIPS 2020](https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html) | RAG 基础引用，说明 parametric memory + non-parametric retrieval。 |
| Scientific literature RAG | [OpenScholar, Nature 2026](https://www.nature.com/articles/s41586-025-10072-4) | 支持科研文献合成需要 citation-backed responses、retrieval data store、citation accuracy evaluation。 |
| Hallucination detection | [SelfCheckGPT, EMNLP 2023](https://aclanthology.org/2023.emnlp-main.557/) | 支持将模型输出视为 provisional，并用一致性/事实性检查发现风险。 |
| Hallucinated references | [Do Language Models Know When They're Hallucinating References?, Findings of EACL 2024](https://aclanthology.org/2024.findings-eacl.62/) | 支持 citation/reference gate，尤其适合研究报告场景。 |
| Verification loop | [Chain-of-Verification, 2023](https://arxiv.org/abs/2309.11495) | 支持生成后规划验证问题并独立检查事实。 |
| Iterative retrieval + verification | [FIRE, Findings of NAACL 2025](https://aclanthology.org/2025.findings-naacl.158/) | 和 claim ledger + evidence gate 的 atomic claim verification 很贴合。 |
| Scientific evidence extraction | [Query-driven Document-level Scientific Evidence Extraction, ACL 2025](https://aclanthology.org/2025.acl-long.1359/) | 支持 search candidate 和 accepted evidence 必须分开。 |
| Agent evaluation | [AgentBench, ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/e9df36b21ff4ee211a8b71ee8b7e9f57-Abstract-Conference.html) | 支持用多维 benchmark 和 failure taxonomy 评估 LLM-as-agent。 |
| Model evaluation framework | [HELM, 2022](https://arxiv.org/abs/2211.09110) | 支持多指标评测，不只看准确率，也看 robustness、calibration、efficiency 等。 |
| General assistant benchmark | [GAIA, 2023](https://arxiv.org/abs/2311.12983) | 支持评估 tool use、web browsing、reasoning 等真实助理能力。 |
| Self-feedback refinement | [Self-Refine, NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/hash/91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.html) | 支持 draft -> critique -> revise 模式。 |
| Verbal feedback memory | [Reflexion, NeurIPS 2023](https://papers.neurips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html) | 支持把反馈记录成后续尝试可用的记忆，但需要 deadline gate 防止无限迭代。 |
| Multi-agent faithfulness refinement | [MAMM-Refine, NAACL 2025](https://aclanthology.org/2025.naacl-long.498/) | 支持多 agent/multi-model 在 error detection、critique、faithfulness refinement 上的价值。 |
| Multi-agent engineering inspiration | [MetaGPT, 2023](https://arxiv.org/abs/2308.00352), [AutoGen, 2023](https://arxiv.org/abs/2308.08155) | 适合当工程设计参考，但引用时要说明它们主要是 framework/design inspiration。 |

## What To Say In Interviews

如果被问“如果要补齐这些内容，你会怎么做”，可以这样答：

> 我会分三步做。第一步先把当前 PoC 变成可复跑 demo：加依赖、测试、一键运行、dashboard 和 walkthrough。第二步接真实 LLM/RAG：固定 eval tasks，记录 model outputs，抽取 claims，构建本地 vector index，把 retrieval candidates 送进 evidence gate，并用 citation accuracy、unsupported claim rate、human revision time 做评测。第三步再做 M365/Azure 部署：SharePoint/Excel 作为 tracker，Power Automate 做 intake/approval/reminder，Python service 做 validation/report/LLM-RAG job，最后用 workflow_run_id、queue、cache、retry 和 monitoring 支撑 scalability。

如果被问“参考了哪些论文”，可以这样答：

> RAG 的设计参考 Lewis et al. 2020 和 OpenScholar 2026；agent 工具使用参考 ReAct 和 Toolformer；幻觉检测参考 SelfCheckGPT、hallucinated references 和 Chain-of-Verification；agent 评测参考 AgentBench、HELM 和 GAIA；多 agent critique/refinement 参考 Self-Refine、Reflexion 和 MAMM-Refine。我的项目不是把这些论文都完整复现，而是把它们转化成一个面向 research deliverable 的 quality-gate workflow。

