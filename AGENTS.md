# prisma-flow Contributor Guide

This file is the shared operating manual for AI contributors working in
`prisma-flow`.

## Project identity

- PyPI package: `prisma-flow`
- Python import package: `prismaflow`
- CLI command: `prisma-flow`
- Repository: `osl-incubator/prisma-flow`
- Build backend: Poetry
- Environment/workflow: conda + Poetry + Makim
- Runtime: Python 3.10+

## Design constraints

`prisma-flow` treats PRISMA diagrams as structured, template-based documents,
not arbitrary graph-layout problems.

Required base-install outputs:

- SVG via pure Python
- HTML with embedded SVG
- Mermaid text only
- JSON input/output

Optional outputs:

- YAML via `prisma-flow[yaml]`
- PNG via `prisma-flow[png]` when a pip/uv-installable backend is available

Do not add required dependencies on Graphviz, Cairo, CairoSVG, Node, Mermaid
CLI, Inkscape, Playwright, browser engines, Matplotlib, Plotly, or other system
rendering stacks.

## Repository layout

- `src/prismaflow/models.py`: Pydantic data models and public methods
- `src/prismaflow/validation.py`: validation report objects and count checks
- `src/prismaflow/templates/`: PRISMA template layout builders
- `src/prismaflow/layout/`: geometry, layout dataclasses, overlap checks
- `src/prismaflow/renderers/`: SVG, HTML, Mermaid, optional PNG renderer
- `src/prismaflow/io/`: JSON and optional YAML helpers
- `src/prismaflow/cli.py`: command-line interface
- `examples/`: runnable example inputs/scripts
- `tests/`: pytest coverage
- `docs/`: Quarto documentation website

## Development commands

```bash
conda env create -f conda/dev.yaml
conda activate prismaflow
poetry config virtualenvs.create false
poetry install --extras "dev yaml"
```

Makim workflow:

```bash
makim tests.linter
makim tests.unit
makim package.build
makim docs.build
makim all.ci
```

## Implementation rules

1. Keep the base install lightweight.
2. Keep SVG rendering pure Python.
3. Keep Mermaid export as text generation only; never invoke Mermaid CLI.
4. Validate PRISMA count relationships and return structured reports.
5. Add tests for model, validation, layout, renderer, IO, and CLI changes.
6. Keep README examples, docs, and examples in sync with public API changes.
