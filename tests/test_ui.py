from pathlib import Path

import pytest

from prismaflow import FlowMetadata, OptionalDependencyError, PrismaFlow, PrismaTemplate

VALID_WIDGET_KWARGS = {
    "title": "Widget example",
    "records_identified_databases": 100,
    "records_identified_registers": 20,
    "records_removed_duplicates": 10,
    "records_removed_automation": 5,
    "records_removed_other": 5,
    "records_screened": 100,
    "records_excluded": 80,
    "reports_sought": 20,
    "reports_not_retrieved": 2,
    "reports_assessed": 18,
    "reports_excluded": {"Wrong population": 8},
    "studies_included": 10,
}


def test_ui_package_exports_load() -> None:
    from prismaflow.ui import load

    assert callable(load)


def test_ui_optional_dependency_error(monkeypatch: pytest.MonkeyPatch) -> None:
    from prismaflow.ui import widgets

    def fake_import_module(name: str) -> object:
        if name == "ipywidgets":
            raise ImportError("missing ipywidgets")
        raise AssertionError(name)

    monkeypatch.setattr(widgets, "import_module", fake_import_module)

    with pytest.raises(OptionalDependencyError, match=r"prisma-flow\[ui\]"):
        widgets._load_ipywidgets()


def test_load_builds_flow_from_new_review_parameters() -> None:
    pytest.importorskip("ipywidgets")
    pytest.importorskip("IPython")
    from prismaflow.ui import load

    widget = load(
        display_widget=False,
        previous_studies=2,
        previous_reports=3,
        reports_included=12,
        total_studies=12,
        total_reports=15,
        metadata={"review_id": "review-1", "authors": ["Ada"]},
        template=PrismaTemplate.PRISMA_2020_NEW_DATABASES_REGISTERS_OTHER,
        website_results=4,
        organisation_results=3,
        citations_results=2,
        other_sought_reports=9,
        other_notretrieved_reports=1,
        other_assessed=8,
        other_excluded={"Not relevant": 1},
        **VALID_WIDGET_KWARGS,
    )

    flow = widget.prisma_flow_build_flow()

    assert isinstance(flow, PrismaFlow)
    assert flow.title == "Widget example"
    assert flow.template is PrismaTemplate.PRISMA_2020_NEW_DATABASES_REGISTERS_OTHER
    assert flow.identification.previous_studies == 2
    assert flow.included.total_reports == 15
    assert flow.metadata == FlowMetadata(review_id="review-1", authors=["Ada"])
    assert flow.eligibility.other_excluded == {"Not relevant": 1}


def test_widget_fields_parse_json_updates() -> None:
    pytest.importorskip("ipywidgets")
    pytest.importorskip("IPython")
    from prismaflow.ui import load

    widget = load(display_widget=False, **VALID_WIDGET_KWARGS)
    widget.prisma_flow_fields["reports_excluded"].value = '{"Wrong outcome": 4}'
    widget.prisma_flow_fields["metadata"].value = '{"review_id": "manual"}'

    flow = widget.prisma_flow_build_flow()

    assert flow.eligibility.reports_excluded == {"Wrong outcome": 4}
    assert flow.metadata == FlowMetadata(review_id="manual")


def test_widget_rejects_invalid_json_fields() -> None:
    pytest.importorskip("ipywidgets")
    pytest.importorskip("IPython")
    from prismaflow.ui import load

    widget = load(display_widget=False, **VALID_WIDGET_KWARGS)
    widget.prisma_flow_fields["reports_excluded"].value = "{not json}"

    with pytest.raises(ValueError, match="reports_excluded"):
        widget.prisma_flow_build_kwargs()


def test_widget_buttons_save_svg_and_png(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pytest.importorskip("ipywidgets")
    pytest.importorskip("IPython")
    from prismaflow.ui import load

    def fake_to_png(self: PrismaFlow, path: str | Path | None = None) -> bytes:
        png = b"fake png"
        if path is not None:
            Path(path).write_bytes(png)
        return png

    monkeypatch.setattr(PrismaFlow, "to_png", fake_to_png)

    svg_path = tmp_path / "widget.svg"
    png_path = tmp_path / "widget.png"
    widget = load(
        display_widget=False,
        svg_path=svg_path,
        png_path=png_path,
        **VALID_WIDGET_KWARGS,
    )

    widget.prisma_flow_buttons["save_svg"].click()
    widget.prisma_flow_buttons["save_png"].click()

    assert svg_path.read_text().startswith('<?xml version="1.0"')
    assert png_path.read_bytes() == b"fake png"
