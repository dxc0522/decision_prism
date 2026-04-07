# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Decision Prism Pro** — a Python backend for a "digital sandbox" strategic decision system. It dynamically dispatches domain-expert AI agents, runs a structured 3-round debate (statement → cross-examination → risk revision), and produces decision reports with probability intervals, causal chains, and Nash equilibrium analysis.

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python (managed by `uv`) |
| Agent Orchestration | LangGraph (StateGraph) |
| LLM Gateway | OpenRouter → `langchain-openai` (OpenAI-compatible) |
| Default Model | `qwen/qwen3.6-plus:free` |
| Data Retrieval | Tavily AI + Firecrawl |
| CLI | Typer + Rich |
| Analysis | numpy + scipy (Monte Carlo) |
| Tests | pytest + pytest-asyncio + pytest-cov |
| Linting | ruff |
| Type Check | mypy |

## Architecture

```
User Query ─▶ Intent Parsing ─▶ SME Dispatch ─▶ Research ─▶ R1 Debate ─▶ R2 Debate ─▶ R3 Debate ─▶ Synthesize ─▶ Analysis ─▶ Report
```

### Package Structure

```
decision_prism/
├── agents/        # SMEExpertAgent, RiskAgent, SynthesizerAgent + Registry (keyword dispatch)
├── analysis/      # bayesian.py (Monte Carlo), causal.py, equilibrium.py (Nash)
├── graph/         # LangGraph StateGraph — nodes.py, edges.py, workflow.py
├── llm/           # Abstract LLMProvider + OpenRouter implementation + ModelConfig
├── models/        # Pydantic models: DebateState, FinalReport, DebateEntry, etc.
├── prompts/       # Jinja2 prompt loader + templates
└── tools/         # tavily_search.py, firecrawl.py, sentiment.py
prompts/           # Markdown prompt templates (debate rounds, report)
tests/             # Unit tests + integration tests
```

### LangGraph Workflow

The `StateGraph` is assembled in `decision_prism/graph/workflow.py`. It uses a `DebateState` TypedDict (defined in `decision_prism/models/state.py`) with LangGraph reducers for accumulating errors, research materials, and debate rounds. The flow is linear for MVP: 8 nodes connected sequentially, with edge stubs for future conditional routing.

## Key Commands

```bash
uv run decision-prism debate "Your query here"   # Run a full debate
uv run decision-prism info                        # Show config/model info
make test                                         # Run tests with coverage
make lint                                         # Ruff check
make format                                       # Ruff format
make check                                        # lint + format + mypy
```

### Run a single test
```bash
uv run pytest tests/test_graph/test_nodes.py -v
```

### Run integration test
```bash
uv run pytest tests/integration/test_debate_flow.py -v
```

## Dependencies

All in `pyproject.toml`. Key deps: `langgraph`, `langchain`, `langchain-openai`, `pydantic`, `pydantic-settings`, `typer`, `rich`, `tavily-python`, `firecrawl-py`, `numpy`, `scipy`, `jinja2`, `httpx`, `tenacity`. Dev deps: `pytest`, `pytest-asyncio`, `pytest-cov`, `ruff`, `mypy`, `respx`.

## Configuration

Env vars in `.env` (create from `.env.example`):
- `OPENROUTER_API_KEY` — required
- `TAVILY_API_KEY` — required for research
- `FIRECRAWL_API_KEY` — required for deep extraction

Model config in `decision_prism/llm/model_config.py` supports swapping to any OpenAI-compatible endpoint via `base_url`.

## Testing Strategy

- **Unit tests**: Mock LLM provider, test each agent/graph node with known inputs
- **Integration tests**: Full E2E with mocked LLM — verify state flows through all 3 rounds, report has all required keys
- **Analysis tests**: Seeded Monte Carlo simulations for deterministic results (p5 < p50 < p95)
- Target: 80%+ coverage
