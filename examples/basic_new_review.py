"""Generate example PRISMA flow outputs."""

from pathlib import Path

from prismaflow import PrismaFlow

flow = PrismaFlow(
    title="Example PRISMA Flow Diagram",
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

output_dir = Path(__file__).parent / "output"
output_dir.mkdir(exist_ok=True)
flow.to_svg(output_dir / "basic_new_review.svg")
flow.to_html(output_dir / "basic_new_review.html")
flow.to_mermaid(output_dir / "basic_new_review.mmd")
flow.to_json(output_dir / "basic_new_review.json")
