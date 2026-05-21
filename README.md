# Prisma Flow

![CI](https://img.shields.io/github/actions/workflow/status/osl-incubator/prisma-flow/main.yaml?logo=github&label=CI)
[![Python Versions](https://img.shields.io/pypi/pyversions/prisma-flow)](https://pypi.org/project/prisma-flow/)
[![Package Version](https://img.shields.io/pypi/v/prisma-flow?color=blue)](https://pypi.org/project/prisma-flow/)
![License](https://img.shields.io/pypi/l/prisma-flow?color=blue)

**Prisma Flow** is a new Python package under the Open Science Labs Incubator.
The current repository state focuses on the reusable project workflow:
packaging, tests, linting, documentation, and release automation.

Package-specific functionality will be defined and implemented later.

- License: BSD 3-Clause
- Repository: <https://github.com/osl-incubator/prisma-flow>
- Documentation: <https://osl-incubator.github.io/prisma-flow>

---

## Development

Create and activate the development environment:

```bash
conda env create -f conda/dev.yaml
conda activate prismaflow
```

Install the package and development dependencies:

```bash
poetry config virtualenvs.create false
poetry install
```

Run the main workflow tasks:

```bash
makim prisma-flow.unittests
makim prisma-flow.typecheck
makim prisma-flow.lint
makim prisma-flow.build
makim docs.build
```

Run the full local CI workflow:

```bash
makim all.ci
```

## Project layout

```text
src/prisma_flow/  Python package scaffold
tests/            pytest test suite
docs/             MkDocs documentation
conda/            development and release environments
.github/          issue templates and CI workflows
```

## Status

This package is intentionally minimal for now. Please keep changes focused on
shared infrastructure until the Prisma Flow package plan is added.
