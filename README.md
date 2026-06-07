# prisma-flow

![CI](https://img.shields.io/github/actions/workflow/status/osl-incubator/prisma-flow/ci.yml?logo=github&label=CI)
[![Python Versions](https://img.shields.io/pypi/pyversions/prisma-flow)](https://pypi.org/project/prisma-flow/)
[![Package Version](https://img.shields.io/pypi/v/prisma-flow?color=blue)](https://pypi.org/project/prisma-flow/)
![License](https://img.shields.io/pypi/l/prisma-flow?color=blue)

`prisma-flow` is a lightweight Python package for generating PRISMA-style flow
diagrams for evidence synthesis workflows.

PRISMA means **Preferred Reporting Items for Systematic reviews and
Meta-Analyses**. `prisma-flow` is an independent Python implementation for
generating diagrams based on PRISMA 2020 flow diagram structures; it is not the
PRISMA reporting guideline itself and is not affiliated with or endorsed by the
PRISMA Executive.

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
- Optional Jupyter widget UI via `prisma-flow[ui]`
- PNG export through the bundled `resvg` Python dependency
- Inline SVG display in notebook frontends
- Python API and `prisma-flow` command-line interface
- PRISMA count validation with errors and warnings

## Installation

```bash
pip install prisma-flow
```

Optional YAML support:

```bash
pip install "prisma-flow[yaml]"
```

Optional Jupyter widget support:

```bash
pip install "prisma-flow[ui]"
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
    reports_included=40,
)

report = flow.validate()
print(report.format_text())

flow.to_svg("prisma.svg")
flow.to_html("prisma.html")
flow.to_mermaid("prisma.mmd")
flow.to_json("review.json")
```

## Jupyter widget UI

Install the optional UI extra, then call `load()` in a notebook cell:

```python
from prismaflow.ui import load

load(
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
    reports_excluded={"Wrong population": 30},
    studies_included=70,
)
```

The widget can generate an inline SVG preview and save SVG or PNG files.

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
prisma-flow render examples/basic_new_review.json --format png -o prisma.png
```

If validation fails, the CLI prints a report and exits with a non-zero status:

```text
Validation failed:
- records_screened should equal identified records minus removed records. Expected: 1080 Found: 1090
```

## Data model

The implementation supports PRISMA 2020 new-review databases/registers fields,
with optional other-method fields for expanded SVG diagrams:

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
        other_sought_reports=0,
        other_notretrieved_reports=0,
        other_assessed=0,
    ),
    included=IncludedStage(studies_included=40, reports_included=90),
)
```

## Dependency policy

SVG, HTML, Mermaid, PNG, and JSON work with the base install. YAML and Jupyter
widget support are optional. PNG rasterization uses the pip-installable `resvg`
Python package; no Graphviz, Cairo, browser engine, or Node-based renderer is
required.

If PNG text is missing in a minimal notebook image such as Google Colab, install
a font package before rendering:

```bash
apt-get update && apt-get install -y fonts-dejavu-core
```

The package does **not** require Graphviz, Cairo, CairoSVG, Node, Mermaid CLI,
Inkscape, Playwright, browser engines, Matplotlib, or Plotly.

## PRISMA acknowledgement and citation

If `prisma-flow` helps produce diagrams or serialized flow data for your work,
it is appropriate to cite the software as well as the PRISMA guideline. Citation
metadata for `prisma-flow` is provided in [`CITATION.cff`](CITATION.cff); please
cite the version you used.

Suggested wording:

```text
PRISMA flow diagrams were generated with prisma-flow and reported according to
the PRISMA 2020 statement.
```

The PRISMA 2020 reporting guideline, checklist, and flow diagram templates were
developed by the PRISMA 2020 authors and are maintained through the PRISMA
Executive. When using PRISMA-style diagrams in reports, manuscripts, or
presentations, cite the original PRISMA 2020 publications in addition to any
software citation:

- Page MJ, McKenzie JE, Bossuyt PM, Boutron I, Hoffmann TC, Mulrow CD, et al.
  The PRISMA 2020 statement: an updated guideline for reporting systematic
  reviews. _BMJ_. 2021;372:n71. doi:
  [10.1136/bmj.n71](https://doi.org/10.1136/bmj.n71).
- Page MJ, Moher D, Bossuyt PM, Boutron I, Hoffmann TC, Mulrow CD, et al. PRISMA
  2020 explanation and elaboration: updated guidance and exemplars for reporting
  systematic reviews. _BMJ_. 2021;372:n160. doi:
  [10.1136/bmj.n160](https://doi.org/10.1136/bmj.n160).

See the official [PRISMA website](https://www.prisma-statement.org/) and
[PRISMA 2020 flow diagram page](https://www.prisma-statement.org/prisma-2020-flow-diagram)
for source templates and usage guidance.

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
