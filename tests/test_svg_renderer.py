import re

from prismaflow import PrismaFlow, new_review


def test_svg_renderer_outputs_accessible_svg() -> None:
    flow = PrismaFlow.from_json("examples/basic_new_review.json")
    svg = flow.to_svg()
    assert svg.startswith('<?xml version="1.0"')
    assert "<svg" in svg
    assert "<title" in svg
    assert 'marker-end="url(#arrowhead)"' in svg
    assert "Identification of new studies via databases and registers" in svg
    assert 'class="node header stage-label"' in svg
    assert "PRISMA 2020 statement" not in svg
    assert "prisma-statement.org" not in svg
    assert "Wrong population" in svg


def test_svg_renderer_uses_default_title_when_no_title_is_provided() -> None:
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

    svg = flow.to_svg()

    assert '<title id="title">PRISMA Flow Diagram</title>' in svg
    assert ">PRISMA Flow Diagram<" in svg
    assert "Example PRISMA Flow Diagram" not in svg
    assert '<text class="diagram-title"' in svg


def test_svg_renderer_keeps_removed_text_away_from_top_border() -> None:
    flow = PrismaFlow.from_json("examples/basic_new_review.json")
    svg = flow.to_svg()

    match = re.search(
        r'<g id="removed" class="node stage">\n'
        r'  <rect x="(?P<rect_x>[\d.]+)" y="(?P<rect_y>[\d.]+)" '
        r'width="(?P<rect_width>[\d.]+)" height="(?P<rect_height>[\d.]+)" />\n'
        r'  <text x="(?P<text_x>[\d.]+)" y="(?P<text_y>[\d.]+)"',
        svg,
    )

    assert match is not None
    assert float(match.group("text_y")) - float(match.group("rect_y")) >= 18
    assert "Duplicate records (n = 210)" in svg
    assert "automation tools (n = 0)" in svg


def test_svg_renderer_escapes_text() -> None:
    flow = PrismaFlow.from_json("examples/basic_new_review.json")
    flow.title = "A < B & C"
    svg = flow.to_svg()
    assert "A &lt; B &amp; C" in svg


def test_svg_renderer_includes_other_methods_when_present() -> None:
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

    svg = flow.to_svg()

    assert 'width="1180"' in svg
    assert "PRISMA Flow Diagram" in svg
    assert "Identification of new studies via other methods" in svg
    assert "Reports of new included studies" in svg
    assert "Wrong outcome" in svg


def test_svg_renderer_includes_source_details_when_present() -> None:
    flow = PrismaFlow.new_review(
        records_identified_databases=10,
        records_identified_registers=5,
        database_specific_results="MEDLINE, 7; Embase, 3",
        register_specific_results="ClinicalTrials.gov, 5",
        records_removed_duplicates=1,
        records_removed_automation=1,
        records_removed_other=1,
        records_screened=12,
        records_excluded=8,
        reports_sought=4,
        reports_not_retrieved=1,
        reports_assessed=3,
        reports_excluded={"Wrong population": 1},
        studies_included=2,
        reports_included=2,
    )

    svg = flow.to_svg()

    assert "MEDLINE, 7; Embase, 3" in svg
    assert "ClinicalTrials.gov, 5" in svg
