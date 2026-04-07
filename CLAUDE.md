# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此代码库中工作时提供指导。

## 项目概述

**Decision Prism Pro** — 一个"数字沙盘"战略决策系统的 Python 后端。它动态调度领域专家 AI Agent，执行结构化的 3 轮辩论（陈述 → 交叉审查 → 风险修订），并生成包含概率区间、因果链和纳什均衡分析的决策报告。

## 技术栈

| 组件 | 技术 |
|-----------|-----------|
| 语言 | Python（由 `uv` 管理） |
| Agent 编排 | LangGraph (StateGraph) |
| LLM 网关 | OpenRouter → `langchain-openai`（OpenAI 兼容） |
| 默认模型 | `qwen/qwen3.6-plus:free` |
| 数据检索 | Tavily AI + Firecrawl |
| CLI | Typer + Rich |
| 分析 | numpy + scipy（蒙特卡洛） |
| 测试 | pytest + pytest-asyncio + pytest-cov |
| 代码检查 | ruff |
| 类型检查 | mypy |

## 架构

```
用户查询 ─▶ 意图解析 ─▶ SME 调度 ─▶ 研究 ─▶ R1 辩论 ─▶ R2 辩论 ─▶ R3 辩论 ─▶ 综合 ─▶ 分析 ─▶ 报告
```

### 包结构

```
decision_prism/
├── agents/        # SMEExpertAgent, RiskAgent, SynthesizerAgent + Registry（关键词分发）
├── analysis/      # bayesian.py（蒙特卡洛）, causal.py, equilibrium.py（纳什均衡）
├── graph/         # LangGraph StateGraph — nodes.py, edges.py, workflow.py
├── llm/           # 抽象 LLMProvider + OpenRouter 实现 + ModelConfig
├── models/        # Pydantic 模型：DebateState, FinalReport, DebateEntry 等
├── prompts/       # Jinja2 提示词加载器 + 模板
└── tools/         # tavily_search.py, firecrawl.py, sentiment.py
prompts/           # Markdown 提示词模板（辩论轮次、报告）
tests/             # 单元测试 + 集成测试
```

### LangGraph 工作流

`StateGraph` 在 `decision_prism/graph/workflow.py` 中组装。它使用 `DebateState` TypedDict（定义在 `decision_prism/models/state.py` 中），带有 LangGraph reducer 用于累积错误、研究材料和辩论轮次。MVP 阶段为线性流程：8 个节点按顺序连接，带有用于未来条件路由的边存根。

## 关键命令

```bash
uv run decision-prism debate "你的查询"    # 执行完整辩论
uv run decision-prism info                 # 显示配置/模型信息
make test                                  # 运行测试并生成覆盖率报告
make lint                                  # Ruff 代码检查
make format                                # Ruff 格式化
make check                                 # lint + format + mypy 类型检查
```

### 运行单个测试
```bash
uv run pytest tests/test_graph/test_nodes.py -v
```

### 运行集成测试
```bash
uv run pytest tests/integration/test_debate_flow.py -v
```

## 依赖

全部定义在 `pyproject.toml` 中。关键依赖：`langgraph`、`langchain`、`langchain-openai`、`pydantic`、`pydantic-settings`、`typer`、`rich`、`tavily-python`、`firecrawl-py`、`numpy`、`scipy`、`jinja2`、`httpx`、`tenacity`。开发依赖：`pytest`、`pytest-asyncio`、`pytest-cov`、`ruff`、`mypy`、`respx`。

## 配置

环境变量在 `.env` 中创建（从 `.env.example` 复制）：
- `OPENROUTER_API_KEY` — 必需
- `TAVILY_API_KEY` — 研究功能必需
- `FIRECRAWL_API_KEY` — 深度提取功能必需

`decision_prism/llm/model_config.py` 中的模型配置支持通过 `base_url` 切换到任何 OpenAI 兼容的端点。

## 测试策略

- **单元测试**：模拟 LLM Provider，使用已知输入测试每个 Agent/图节点
- **集成测试**：全流程 E2E 测试（模拟 LLM）— 验证状态流经全部 3 轮辩论，报告包含所有必需的键
- **分析测试**：使用种子的蒙特卡洛模拟以获得确定性结果（p5 < p50 < p95）
- **目标覆盖率**：80%+
