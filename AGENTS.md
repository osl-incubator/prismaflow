# Prisma Flow Contributor Guide

This file is the shared operating manual for AI contributors working in
`prisma-flow`. Use it to keep implementation style, review standards, and
project workflow consistent across agents.

## Current Scope

Prisma Flow is currently in scaffold mode. The repository contains project
infrastructure only: package metadata, tests, linting, documentation, CI, and
release automation.

Do not add Prisma Flow-specific runtime behavior until the package plan is
provided.

## Project Snapshot

- Distribution package: `prisma-flow`
- Python import package: `prisma_flow`
- Runtime: Python `>=3.10,<4`
- License: BSD 3-Clause
- Docs stack: MkDocs Material
- Task runner: Makim via `.makim.yaml`
- Package manager/build backend: Poetry

## Repository Layout

- `src/prisma_flow/`: Python package scaffold
- `tests/`: `pytest` test suite
- `docs/`: MkDocs documentation
- `conda/`: development and release environments
- `.github/workflows/`: CI, docs, and release workflows
- `.makim.yaml`: local task definitions
- `.pre-commit-config.yaml`: formatting and quality hooks

## Development Commands

```bash
conda env create -f conda/dev.yaml
conda activate prismaflow
poetry config virtualenvs.create false
poetry install
```

Useful tasks:

```bash
makim prisma-flow.unittests
makim prisma-flow.typecheck
makim prisma-flow.lint
makim prisma-flow.build
makim docs.build
makim all.ci
```

Direct equivalents:

```bash
pytest tests -vv
mypy src tests
pre-commit run --all-files
poetry build
mkdocs build --config-file mkdocs.yaml --strict
```

## Contribution Rules

1. Keep edits minimal and targeted.
2. Preserve the package scaffold until an explicit implementation plan is added.
3. Keep `pyproject.toml`, `.makim.yaml`, pre-commit hooks, and CI workflows in
   sync when changing tooling.
4. Keep release-managed version strings aligned in:
   - `pyproject.toml`
   - `src/prisma_flow/__init__.py`
   - `.releaserc.json`
5. Add or update tests for any future runtime behavior.
6. Prefer local workspace inspection over remote repository state.

## Quality Gates

Before handing off code, run the narrowest relevant checks. For workflow or
scaffold changes, prefer:

```bash
pytest tests -vv
mypy src tests
ruff check src tests
ruff format --check src tests
poetry check
poetry build
mkdocs build --config-file mkdocs.yaml --strict
```
