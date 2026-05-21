from datetime import date
from pathlib import Path

from prismaflow import FlowMetadata, PrismaFlow, PrismaTemplate, new_review
from prismaflow.cli import main
from prismaflow.layout.overlap import find_overlaps

ARTIFACTS_DIR = Path("tmp/test-outputs/complex")


def complex_review() -> PrismaFlow:
    return new_review(
        title="Complex PRISMA Flow Diagram",
        template=PrismaTemplate.PRISMA_2020_NEW_DATABASES_REGISTERS_OTHER,
        records_identified_databases=2600,
        records_identified_registers=140,
        previous_studies=10,
        previous_reports=28,
        database_specific_results=(
            "MEDLINE, 900; Embase, 760; CENTRAL, 540; CINAHL, 400"
        ),
        register_specific_results="ClinicalTrials.gov, 80; WHO ICTRP, 60",
        website_results=12,
        organisation_results=8,
        citations_results=10,
        records_removed_duplicates=410,
        records_removed_automation=75,
        records_removed_other=55,
        records_screened=2200,
        records_excluded=1840,
        reports_sought=360,
        reports_not_retrieved=25,
        reports_assessed=335,
        reports_excluded={
            "Wrong population": 78,
            "Wrong intervention": 61,
            "Wrong outcome": 44,
            "Not primary research": 39,
            "Duplicate report": 16,
            "Non-English full text": 12,
        },
        other_sought_reports=30,
        other_notretrieved_reports=3,
        other_assessed=27,
        other_excluded={
            "Ineligible source": 5,
            "Superseded citation": 4,
            "Not retrievable": 3,
        },
        studies_included=100,
        reports_included=100,
        total_studies=110,
        total_reports=128,
        metadata=FlowMetadata(
            review_id="complex-review",
            authors=["Open Science Labs", "Prisma Flow Contributors"],
            created_at=date(2026, 5, 21),
            notes="Full-feature integration fixture.",
            extra={"protocol": "PRISMA 2020", "dataset": "synthetic"},
        ),
    )


def test_complex_review_exercises_model_validation_layout_and_renderers() -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    flow = complex_review()

    report = flow.validate(strict_included=True)
    assert report.ok
    assert not report.warnings
    assert flow.has_other_methods
    assert flow.identification.has_source_details
    assert flow.identification.has_previous_studies
    assert flow.included.has_previous_totals
    assert flow.identification.records_identified_total == 2740
    assert flow.identification.other_methods_total == 30
    assert flow.screening.records_removed_total == 540
    assert flow.eligibility.reports_excluded_total == 250
    assert flow.eligibility.other_excluded_total == 12

    layout = flow.to_layout()
    assert layout.width == 1180
    assert layout.node_by_id("other_methods_header").text.endswith("other methods")
    assert layout.node_by_id("other_reports_excluded").kind == "exclusion"
    assert find_overlaps(layout, padding=8) == []

    svg_path = ARTIFACTS_DIR / "complex_review.svg"
    html_path = ARTIFACTS_DIR / "complex_review.html"
    mermaid_path = ARTIFACTS_DIR / "complex_review.mmd"
    json_path = ARTIFACTS_DIR / "complex_review.json"
    yaml_path = ARTIFACTS_DIR / "complex_review.yaml"
    png_path = ARTIFACTS_DIR / "complex_review.png"

    svg = flow.to_svg(svg_path)
    html = flow.to_html(html_path)
    mermaid = flow.to_mermaid(mermaid_path)
    json_output = flow.to_json(json_path)
    yaml_output = flow.to_yaml(yaml_path)
    png = flow.to_png(png_path)

    assert svg_path.read_text(encoding="utf-8") == svg
    assert html_path.read_text(encoding="utf-8") == html
    assert mermaid_path.read_text(encoding="utf-8") == mermaid
    assert json_path.read_text(encoding="utf-8") == json_output + "\n"
    assert yaml_path.read_text(encoding="utf-8") == yaml_output
    assert png_path.read_bytes() == png

    assert "Complex PRISMA Flow Diagram" in svg
    assert "MEDLINE, 900; Embase, 760;" in svg
    assert "CENTRAL, 540; CINAHL, 400" in svg
    assert "ClinicalTrials.gov, 80; WHO" in svg
    assert "ICTRP, 60" in svg
    assert "Identification of new studies via other methods" in svg
    assert "Records marked as ineligible by" in svg
    assert "Reports of new included studies" in svg
    assert "Superseded citation" in svg
    assert html.startswith("<!doctype html>")
    assert mermaid.startswith("flowchart TD")
    assert "other methods" not in mermaid
    assert png.startswith(b"\x89PNG\r\n\x1a\n")

    json_roundtrip = PrismaFlow.from_json(json_path)
    yaml_roundtrip = PrismaFlow.from_yaml(yaml_path)
    assert json_roundtrip.model_dump(mode="json") == flow.model_dump(mode="json")
    assert yaml_roundtrip.model_dump(mode="json") == flow.model_dump(mode="json")

    data, metadata = flow._repr_mimebundle_()
    assert metadata == {}
    assert data["image/svg+xml"] == flow._repr_svg_()


def test_complex_review_cli_renders_all_supported_formats() -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    input_path = ARTIFACTS_DIR / "complex_cli_input.json"
    complex_review().to_json(input_path)

    assert main(["validate", str(input_path), "--strict-included"]) == 0

    outputs = {
        "svg": ARTIFACTS_DIR / "complex_cli.svg",
        "html": ARTIFACTS_DIR / "complex_cli.html",
        "mermaid": ARTIFACTS_DIR / "complex_cli.mmd",
        "json": ARTIFACTS_DIR / "complex_cli.json",
        "yaml": ARTIFACTS_DIR / "complex_cli.yaml",
        "png": ARTIFACTS_DIR / "complex_cli.png",
    }
    for output_format, output_path in outputs.items():
        exit_code = main(
            [
                "render",
                str(input_path),
                "--format",
                output_format,
                "--output",
                str(output_path),
            ]
        )
        assert exit_code == 0
        assert output_path.exists()

    assert outputs["svg"].read_text(encoding="utf-8").startswith("<?xml")
    assert outputs["html"].read_text(encoding="utf-8").startswith("<!doctype html>")
    assert outputs["mermaid"].read_text(encoding="utf-8").startswith("flowchart TD")
    assert outputs["json"].read_text(encoding="utf-8").startswith("{\n")
    assert outputs["yaml"].read_text(encoding="utf-8").startswith("template:")
    assert outputs["png"].read_bytes().startswith(b"\x89PNG\r\n\x1a\n")


def test_complex_official_alias_payload_is_supported() -> None:
    flow = PrismaFlow.model_validate(
        {
            "template": "prisma_2020_new_databases_registers_other",
            "title": "Complex official alias payload",
            "identification": {
                "database_results": 2600,
                "register_results": 140,
                "previous_studies": 10,
                "previous_reports": 28,
                "website_results": 12,
                "organisation_results": 8,
                "citations_results": 10,
            },
            "screening": {
                "duplicates": 410,
                "excluded_automatic": 75,
                "excluded_other": 55,
                "records_screened": 2200,
                "records_excluded": 1840,
            },
            "eligibility": {
                "dbr_sought_reports": 360,
                "dbr_notretrieved_reports": 25,
                "dbr_assessed": 335,
                "dbr_excluded": {
                    "Wrong population": 78,
                    "Wrong intervention": 61,
                    "Wrong outcome": 44,
                    "Not primary research": 39,
                    "Duplicate report": 16,
                    "Non-English full text": 12,
                },
                "other_sought_reports": 30,
                "other_notretrieved_reports": 3,
                "other_assessed": 27,
                "other_excluded": {
                    "Ineligible source": 5,
                    "Superseded citation": 4,
                    "Not retrievable": 3,
                },
            },
            "included": {
                "new_studies": 100,
                "new_reports": 100,
                "total_studies": 110,
                "total_reports": 128,
            },
        }
    )

    assert flow.validate(strict_included=True).ok
    assert flow.has_other_methods
    assert flow.identification.records_identified_total == 2740
    assert flow.included.reports_included == 100
