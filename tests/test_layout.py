from prismaflow import PrismaFlow
from prismaflow.layout import DiagramLayout, Rect


def test_rect_anchor_properties() -> None:
    rect = Rect(10, 20, 100, 50)
    assert rect.center_x == 60
    assert rect.center_y == 45
    assert rect.top_center.y == 20
    assert rect.bottom_center.y == 70
    assert rect.left_center.x == 10
    assert rect.right_center.x == 110


def test_layout_contains_expected_nodes() -> None:
    flow = PrismaFlow.from_json("examples/basic_new_review.json")
    layout = flow.to_layout()
    assert isinstance(layout, DiagramLayout)
    assert layout.node_by_id("databases_registers_header").kind == "header"
    assert layout.node_by_id("identification_label").text == "Identification"
    assert layout.node_by_id("screening_label").text == "Screening"
    assert layout.node_by_id("included_label").text == "Included"
    assert layout.node_by_id("identified").text.startswith("Records identified")
    assert layout.node_by_id("included").text.startswith("New studies included")


def test_layout_follows_prisma_2020_visual_flow() -> None:
    flow = PrismaFlow.from_json("examples/basic_new_review.json")
    layout = flow.to_layout()
    identified = layout.node_by_id("identified")
    removed = layout.node_by_id("removed")
    screened = layout.node_by_id("screened")

    assert removed.rect.x > identified.rect.x
    assert screened.rect.y > identified.rect.y
    assert {edge.id for edge in layout.edges} >= {
        "identified_to_removed",
        "identified_to_screened",
    }


def test_layout_expands_when_other_methods_are_present() -> None:
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
    layout = flow.to_layout()

    assert layout.width > 1000
    assert layout.node_by_id("other_methods_header").kind == "header"
    assert layout.node_by_id("other_identified").text.startswith(
        "Records identified from"
    )
    assert layout.node_by_id("included").text.endswith("(n = 28)")
