# prisma-flow

![CI](https://img.shields.io/github/actions/workflow/status/osl-incubator/prisma-flow/ci.yml?logo=github&label=CI)
[![Python Versions](https://img.shields.io/pypi/pyversions/prisma-flow)](https://pypi.org/project/prisma-flow/)
[![Package Version](https://img.shields.io/pypi/v/prisma-flow?color=blue)](https://pypi.org/project/prisma-flow/)
![License](https://img.shields.io/pypi/l/prisma-flow?color=blue)

`prisma-flow` is a lightweight Python package for generating PRISMA-style flow
diagrams for evidence synthesis workflows.

Unlike Graphviz-based tools, `prisma-flow` does not require system-level graph
layout binaries. Unlike Mermaid-based tools, it does not require Node or Mermaid
CLI. The default renderer is a pure-Python, template-based SVG generator.

The project is designed for systematic reviews, scoping reviews, evidence
syntheses, and literature review workflows.

## Features

- Pure-Python SVG rendering by default
- Standalone HTML export
- Mermaid text export without Mermaid CLI
- JSON input/output in the base install
- Optional YAML input/output via `prisma-flow[yaml]`
- Optional PNG method that clearly reports the missing optional dependency
- Inline SVG display in notebook frontends
- Python API and `prisma-flow` command-line interface
- PRISMA count validation with errors and warnings

## Installation

```bash
pip install prisma-flow
```

or:

```bash
uv add prisma-flow
```

Optional YAML support:

```bash
uv add "prisma-flow[yaml]"
```

Optional PNG support, when a supported backend is added:

```bash
uv add "prisma-flow[png]"
```

## Python API

```python
from prismaflow import new_review

flow = new_review(
    records_identified_databases=1240,
    records_identified_registers=50,
    records_removed_duplicates=210,
    records_removed_automation=0,
    records_removed_other=0,
    records_screened=1080,
    records_excluded=950,
    reports_sought=130,
    reports_not_retrieved=10,
    reports_assessed=120,
    reports_excluded={
        "Wrong population": 30,
        "Wrong intervention": 20,
        "Wrong outcome": 15,
        "Not primary research": 15,
    },
    studies_included=40,
)

report = flow.validate()
print(report.format_text())

flow.to_svg("prisma.svg")
flow.to_html("prisma.html")
flow.to_mermaid("prisma.mmd")
flow.to_json("review.json")
```

## CLI usage

Validate input data:

```bash
prisma-flow validate examples/basic_new_review.json
```

Render SVG:

```bash
prisma-flow render examples/basic_new_review.json -o prisma.svg
```

Render other base-install formats:

```bash
prisma-flow render examples/basic_new_review.json --format html -o prisma.html
prisma-flow render examples/basic_new_review.json --format mermaid -o prisma.mmd
```

If validation fails, the CLI prints a report and exits with a non-zero status:

```text
Validation failed:
- records_screened should equal identified records minus removed records. Expected: 1080 Found: 1090
```

## Data model

The v0.1 implementation supports the PRISMA 2020 new-review databases/registers
template:

```python
from prismaflow import (
    EligibilityStage,
    IdentificationStage,
    IncludedStage,
    PrismaFlow,
    PrismaTemplate,
    ScreeningStage,
)

flow = PrismaFlow(
    template=PrismaTemplate.PRISMA_2020_NEW_DATABASES_REGISTERS,
    identification=IdentificationStage(
        records_identified_databases=1240,
        records_identified_registers=50,
    ),
    screening=ScreeningStage(
        records_removed_duplicates=210,
        records_removed_automation=0,
        records_removed_other=0,
        records_screened=1080,
        records_excluded=950,
    ),
    eligibility=EligibilityStage(
        reports_sought=130,
        reports_not_retrieved=10,
        reports_assessed=120,
        reports_excluded={"Wrong population": 30},
    ),
    included=IncludedStage(studies_included=40),
)
```

## Dependency policy

SVG, HTML, Mermaid, and JSON work with the base install. YAML is optional. PNG
is intentionally optional and not implemented as a required renderer in v0.1.

The package does **not** require Graphviz, Cairo, CairoSVG, Node, Mermaid CLI,
Inkscape, Playwright, browser engines, Matplotlib, or Plotly.

## Development

```bash
conda env create -f conda/dev.yaml
conda activate prismaflow
poetry config virtualenvs.create false
poetry install --extras "dev yaml"
```

Run the same workflow through Makim:

```bash
makim tests.linter
makim tests.unit
makim package.build
makim docs.build
makim all.ci
```

## Documentation

The documentation site is built with Quarto:

```bash
quarto render docs
```

Preview locally:

```bash
quarto preview docs
```

## License

BSD-3-Clause.
