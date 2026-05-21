# Contributing

Thank you for contributing to `prisma-flow`.

## Development setup

```bash
conda env create -f conda/dev.yaml
conda activate prismaflow
poetry config virtualenvs.create false
poetry install --extras "dev yaml"
```

## Checks

Run the same core checks used by CI:

```bash
makim tests.linter
makim tests.unit
makim package.build
makim docs.build
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
