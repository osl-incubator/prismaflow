# Contributing

Thank you for contributing to `prisma-flow`.

## Development setup

```bash
uv sync --all-extras --dev
```

## Checks

Run the same core checks used by CI:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
uv build
quarto render docs
```

## Scope

The v0.1 scope focuses on template-based PRISMA diagrams with pure-Python SVG,
HTML, Mermaid, JSON, optional YAML, and a CLI. Do not add required system
dependencies such as Graphviz, Cairo, Node, Mermaid CLI, browser engines,
Matplotlib, or Plotly.

## Documentation

Documentation lives in `docs/` and is built with Quarto:

```bash
quarto render docs
```
