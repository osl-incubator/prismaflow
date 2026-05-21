from prismaflow import new_review


def test_validation_passes_for_consistent_flow() -> None:
    flow = new_review(
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
        studies_included=25,
    )
    report = flow.validate()
    assert report.ok
    assert not report.warnings


def test_validation_reports_count_errors() -> None:
    flow = new_review(
        records_identified_databases=100,
        records_identified_registers=0,
        records_removed_duplicates=10,
        records_removed_automation=0,
        records_removed_other=0,
        records_screened=99,
        records_excluded=50,
        reports_sought=40,
        reports_not_retrieved=0,
        reports_assessed=41,
        reports_excluded={},
        studies_included=40,
    )
    report = flow.validate()
    assert report.has_errors
    assert len(report.errors) == 3
    assert "records_screened" in report.format_text()


def test_included_reconciliation_is_warning_by_default() -> None:
    flow = new_review(
        records_identified_databases=10,
        records_identified_registers=0,
        records_removed_duplicates=0,
        records_removed_automation=0,
        records_removed_other=0,
        records_screened=10,
        records_excluded=0,
        reports_sought=10,
        reports_not_retrieved=0,
        reports_assessed=10,
        reports_excluded={},
        studies_included=5,
    )
    report = flow.validate()
    assert report.ok
    assert report.has_warnings
    strict_report = flow.validate(strict_included=True)
    assert strict_report.has_errors


def test_validation_checks_other_method_relationships() -> None:
    flow = new_review(
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

    report = flow.validate()

    assert report.ok
    assert not report.warnings


def test_validation_reports_other_method_count_errors() -> None:
    flow = new_review(
        records_identified_databases=10,
        records_identified_registers=0,
        records_removed_duplicates=0,
        records_removed_automation=0,
        records_removed_other=0,
        records_screened=10,
        records_excluded=0,
        reports_sought=10,
        reports_not_retrieved=0,
        reports_assessed=10,
        reports_excluded={},
        website_results=2,
        organisation_results=0,
        citations_results=0,
        other_sought_reports=1,
        other_notretrieved_reports=0,
        other_assessed=2,
        studies_included=12,
    )

    report = flow.validate()

    assert report.has_errors
    assert "other_sought_reports" in report.format_text()
    assert "other_assessed" in report.format_text()
