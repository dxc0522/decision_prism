# Decision Prism Pro

Dynamic Strategic Decision System — AI-powered expert debate and analysis.

## Setup

```bash
uv sync
cp .env.example .env  # and fill in API keys
```

## Usage

```bash
uv run decision-prism debate "Your strategic question here"
uv run decision-prism info
```

## Development

```bash
make test       # run tests with coverage
make lint       # ruff check
make format     # ruff format
make check      # lint + type check
```
