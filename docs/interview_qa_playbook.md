# Interview Q&A Playbook

这份复盘文档用于回答面试中围绕 AI agent 项目的追问。当前项目定位要说清楚：

> 这是一个 research-agent quality gate 的可运行 PoC：用 CSV ledgers 表达 task、agent role、claim、evidence、handoff，用 Python 做确定性校验和报告生成；真实 LLM 调用、RAG/vector DB、模型部署和云端生产集成还在下一步实现阶段。

## 缺口总览

| 面试问题 | 现在能否回答 | 当前证据 | 还缺什么 |
| --- | --- | --- | --- |
| 项目最大的挑战是什么 | 可以回答 | `README.md`, `docs/problem_statement.md`, `docs/quality_control_design.md` | README 里已补 implementation status；后续可补真实失败案例截图或日志。 |
| 项目用了几个 agent，分别干什么 | 可以回答 | `data/sample_agent_roles.csv`, `docs/agent_orchestration_design.md` | 当前是角色/ledger 原型，不是运行中的 agent 进程。 |
| 用了什么 LLM，哪个模型效果最好 | 目前不能声称 | 无真实模型调用或评测文件 | 需要模型调用脚本、prompt set、evaluation dataset、指标和结果表。 |
| 如何解决大模型幻觉 | 可以回答机制设计 | `data/sample_claim_ledger.csv`, `data/sample_evidence_ledger.csv`, `docs/quality_control_design.md` | 需要真实 LLM 输出前后对比和 hallucination case study。 |
| 用了什么向量数据库 | 目前不能声称 | 无 embedding/retriever/vector DB 代码 | 需要选择 Chroma/FAISS/Azure AI Search/Pinecone 等，并实现 index/query。 |
| 为什么用 RAG，有没有试过其他方法 | 只能回答设计理由 | `data/sample_evidence_ledger.csv`, `docs/quality_control_design.md` | 需要 baseline 对比：pure prompt、keyword search、manual search、RAG。 |
| 如何提升 scalability | 可以回答架构计划 | `docs/solution_architecture.md`, `docs/model_rag_deployment_plan.md` | 需要 job queue、worker、cache、monitoring、load test。 |
| 有模型部署/云端部署吗 | 只能回答 M365 蓝图 | `docs/solution_architecture.md`, `power-automate/flow_description.md` | 需要 API service、Docker/server、cloud endpoint、Power Automate export。 |
| 团队分工如何 | 当前只能按 solo/样例 owner 回答 | `data/sample_research_tasks.csv`, `docs/team_contributions.md` | 如果确实多人合作，需要补真实成员和贡献证据。 |

## 1. 项目中最大的挑战是什么？

**30 秒回答：**

最大的挑战不是让 agent 生成一段看起来流畅的文字，而是把它变成可审计、可批准、能按 deadline 交付的研究产物。LLM 很容易 overclaim、引用弱证据、把 search result 当成 evidence，多个 agent 还可能互相强化同一种写作风格。所以我把项目设计成 quality gate：先记录 claim，再检查 evidence、literature quality、style risk、handoff owner 和 human approval。

**可以引用的项目证据：**

- `README.md`: project pain points and implemented PoC status.
- `docs/quality_control_design.md`: claim ledger, evidence gate, literature quality gate, deadline-aware delivery.
- `reports/sample_weekly_report.md`: generated readiness report showing unresolved claims and evidence risks.

**不要夸大：**

不要说已经完全解决幻觉或已经生产化。更准确的说法是：这个 PoC 把 hallucination/overclaim risk 显性化，并阻止它直接进入 final deliverable。

## 2. 项目一共用了几个 agent，分别是干什么的？

**30 秒回答：**

项目定义了 8 个系统 agent role，加 1 个 human owner。`orchestrator_agent` 负责状态和路由；`skill_agent` 把重复要求变成 checklist；`draft_agent` 产出初稿；`literature_agent` 找候选文献；`evidence_agent` 判断证据是否能支撑 claim；`style_reviewer` 检查 overclaim 和 risky phrasing；`critic_agent` 做独立质疑；`delivery_agent` 决定 deadline 前哪些内容可以 ship；最后由 `human_owner` 做最终批准。

**可以引用的项目证据：**

- `data/sample_agent_roles.csv`
- `data/sample_handoff_ledger.csv`
- `docs/agent_orchestration_design.md`

**不要夸大：**

这些目前是 workflow role registry 和 handoff ledger，不是已经在后台并发运行的 agent 服务。

## 3. 用了什么 LLM 模型，哪种模型效果最好？

**安全回答：**

当前 repo 还没有接入真实 LLM API，也没有模型对比结果，所以不能声称用了某个模型或某个模型最好。这个阶段我先把模型无关的质量控制层做出来，保证无论后面接 GPT、Claude、Gemini、Qwen 或本地模型，输出都会进入同一套 claim/evidence/review gate。下一步会补模型评测：同一批 research tasks，用多个模型生成初稿，再比较 factual accuracy、evidence traceability、claim overreach rate、human revision time 和 cost。

**项目还缺：**

- `scripts/run_model_eval.py`
- prompt templates and fixed evaluation tasks
- model output samples
- metrics table
- human review rubric

## 4. 如何解决大模型幻觉问题？

**30 秒回答：**

我没有假设模型不会幻觉，而是把所有模型输出先当成 provisional。每个关键 statement 必须进入 claim ledger；需要外部支持的 claim 必须链接 evidence record；literature search hit 先按 recency、venue decision、source quality、relevance 做 triage，不能直接当证据；style reviewer 会拦截过强措辞；最后 high-risk output 需要 human approval。这样 hallucination 不会因为文字流畅就被直接写进 final report。

**可以引用的项目证据：**

- `data/sample_claim_ledger.csv`
- `data/sample_evidence_ledger.csv`
- `scripts/validate_task_fields.py`
- `scripts/generate_progress_report.py`

**项目还缺：**

- 真实 hallucination 样例和修复前后对比。
- 自动检测模型输出中 unsupported citation 的脚本。
- 每个模型的 hallucination/error taxonomy。

## 5. 你提到使用了矢量数据库，你们用了什么库？

**安全回答：**

当前 demo 没有使用向量数据库。现在的数据层是 CSV ledgers；在 Microsoft 365 版本里会映射到 Excel/SharePoint/Power Apps/Power BI。RAG/vector DB 是下一步扩展，不应该说已经用了 Pinecone、Chroma、FAISS 或 Azure AI Search。

**如果面试官问生产版本怎么选：**

如果部署在 Azure/M365 生态里，我会优先考虑 Azure AI Search 的 vector index，因为它更容易和企业权限、SharePoint 文档、Power Automate 集成。如果只是本地 PoC，我会先用 Chroma 或 FAISS，成本低、实现快，适合验证 chunking、embedding 和 retrieval quality。

**项目还缺：**

- document chunking pipeline
- embedding generation
- vector index build script
- retriever query API
- retrieval quality evaluation

## 6. 为什么用 RAG 方法，有没有试过其他方法？

**30 秒回答：**

这个项目的核心问题是 evidence traceability，所以不能只依赖模型参数记忆。RAG 的价值不是让答案更长，而是把回答绑定到可检查来源。不过在这个 repo 里，RAG 还没有实现为真实 retriever；目前只是把 retrieval/search 作为设计中的 candidate generation，然后用 evidence gate 决定哪些 source 能支持 claim。下一步我会比较 pure prompt、manual/keyword search、agent search 和 RAG，看哪种方法在 evidence coverage、citation accuracy、review time 和 cost 上更好。

**可以引用的项目证据：**

- `data/sample_evidence_ledger.csv`
- `docs/quality_control_design.md`
- `docs/model_rag_deployment_plan.md`

## 7. 你们做了什么来提升 scalability？

**30 秒回答：**

当前 PoC 的可扩展性主要体现在状态设计上：agent 不直接拥有最终状态，所有 task、claim、evidence、handoff 都落到 ledger，所以可以按 task 并行处理，也可以重跑 validation/reporting。生产化时我会把 agent work 做成异步 job：Power Automate 负责触发和审批，Python/worker service 负责批处理和校验，长任务进队列，使用 workflow_run_id、retry/backoff、cache、incremental report、monitoring dashboard 来扩展。

**可以引用的项目证据：**

- `docs/solution_architecture.md`
- `scripts/validate_task_fields.py`
- `scripts/generate_progress_report.py`

**项目还缺：**

- queue/worker implementation
- concurrency and retry policy
- persistent database
- observability and cost dashboard
- load/performance test

## 8. 有进行模型部署吗？有做云端部署吗？

**安全回答：**

目前没有模型部署，也没有完整云端部署。现在本地能运行的是 CSV + Python 的质量门控模拟；云端部分是 M365/Power Automate 架构蓝图，包括 Forms/Teams intake、SharePoint/Excel tracker、approval flow、reminder flow 和 weekly report distribution。下一步如果做云端，会把 Python validation/reporting 包成 API 或 scheduled job，再接 Azure OpenAI/OpenAI API 和 Power Automate。

**项目还缺：**

- deployable service or container
- secrets/config management
- cloud endpoint
- Power Automate importable flow package
- production tracker schema

## 9. 团队分工如何？

**安全回答：**

当前仓库记录的是样例 owner `Nongying Li`，还没有真实多人团队分工表。如果这是个人项目，我会直接说这是 solo PoC：我负责 problem framing、data ledger schema、Python validation/reporting、agent role/handoff design、Power Automate architecture 和 interview prep documentation。如果后续多人合作，应该补 `docs/team_contributions.md` 中的成员、模块、commit/PR 或 artifact evidence。

**不要混淆：**

`data/sample_agent_roles.csv` 是系统里的 agent role 分工，不等于人类团队成员分工。

## 推荐补齐顺序

1. 先补真实 project status 和 interview Q&A，避免面试中 overclaim。
2. 补 model evaluation plan，再实现一个小规模模型对比实验。
3. 补 retrieval pipeline，至少实现 local Chroma/FAISS PoC 或 Azure AI Search 方案。
4. 给 Python scripts 加 CLI 参数和 tests，让 demo 更像可复用工具。
5. 做一个静态 dashboard 或 Streamlit dashboard 展示 ledgers。
6. 做 M365 cloud integration 或明确保留为 architecture blueprint。

