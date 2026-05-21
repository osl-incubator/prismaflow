from pydantic import ValidationError

from prismaflow import (
    EligibilityStage,
    IdentificationStage,
    IncludedStage,
    PrismaFlow,
    PrismaTemplate,
    ScreeningStage,
    new_review,
)


def new_review_kwargs() -> dict[str, object]:
    return {
        "title": "Example",
        "records_identified_databases": 1240,
        "records_identified_registers": 50,
        "records_removed_duplicates": 210,
        "records_removed_automation": 0,
        "records_removed_other": 0,
        "records_screened": 1080,
        "records_excluded": 950,
        "reports_sought": 130,
        "reports_not_retrieved": 10,
        "reports_assessed": 120,
        "reports_excluded": {"Wrong population": 30, "Wrong intervention": 20},
        "studies_included": 70,
    }


def make_flow() -> PrismaFlow:
    return new_review(**new_review_kwargs())


def test_new_review_builds_model() -> None:
    flow = make_flow()
    assert flow.template is PrismaTemplate.PRISMA_2020_NEW_DATABASES_REGISTERS
    assert flow.identification.records_identified_total == 1290
    assert flow.screening.records_removed_total == 210
    assert flow.eligibility.reports_excluded_total == 50


def test_prismaflow_new_review_remains_available() -> None:
    flow = PrismaFlow.new_review(**new_review_kwargs())
    assert flow.title == "Example"
    assert flow.identification.records_identified_total == 1290


def test_nested_constructor_still_works() -> None:
    flow = PrismaFlow(
        title="Nested",
        identification=IdentificationStage(
            records_identified_databases=10,
            records_identified_registers=5,
        ),
        screening=ScreeningStage(
            records_removed_duplicates=1,
            records_removed_automation=1,
            records_removed_other=1,
            records_screened=12,
            records_excluded=8,
        ),
        eligibility=EligibilityStage(
            reports_sought=4,
            reports_not_retrieved=1,
            reports_assessed=3,
            reports_excluded={"Wrong population": 1},
        ),
        included=IncludedStage(studies_included=2),
    )
    assert flow.title == "Nested"
    assert flow.identification.records_identified_total == 15


def test_negative_count_is_rejected() -> None:
    kwargs = make_flow().model_dump()
    kwargs["included"]["studies_included"] = -1
    try:
        PrismaFlow.model_validate(kwargs)
    except ValidationError as exc:
        assert "studies_included" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("negative counts should fail validation")
