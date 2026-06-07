"""Launch the optional prisma-flow Jupyter widget in a notebook cell."""

from prismaflow.ui import load

load(
    title="Notebook widget example",
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
    reports_excluded={"Wrong population": 30, "Wrong intervention": 20},
    studies_included=70,
)
