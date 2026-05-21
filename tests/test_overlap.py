from prismaflow import PrismaFlow
from prismaflow.layout.overlap import find_overlaps


def test_default_template_has_no_node_overlaps() -> None:
    flow = PrismaFlow.from_json("examples/basic_new_review.json")
    assert find_overlaps(flow.to_layout(), padding=8) == []


def test_other_methods_template_has_no_node_overlaps() -> None:
    flow = PrismaFlow.new_review(
        records_identified_databases=100,
        records_identified_registers=20,
        records_removed_duplicates=10,
        records_removed_automation=5,
        records_removed_other=5,
        records_screened=100,
        records_excluded=60,
        reports_sought=40,
        reports_not_retrieved=5,
        reports_assessed=35,
        reports_excluded={"Wrong population": 10},
        website_results=2,
        organisation_results=1,
        citations_results=2,
        other_sought_reports=5,
        other_notretrieved_reports=1,
        other_assessed=4,
        other_excluded={"Wrong outcome": 1},
        studies_included=28,
        reports_included=28,
    )
    assert find_overlaps(flow.to_layout(), padding=8) == []
