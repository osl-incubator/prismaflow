"""Validation report objects and PRISMA count checks."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from prismaflow.models import PrismaFlow

ValidationLevel = Literal["error", "warning"]


class ValidationMessage(BaseModel):
    """A single validation finding."""

    level: ValidationLevel
    field: str
    message: str
    expected: int | None = None
    found: int | None = None

    model_config = ConfigDict(frozen=True)

    def format(self) -> str:
        """Return a human-readable validation line."""
        details: list[str] = [self.message]
        if self.expected is not None:
            details.append(f"Expected: {self.expected}")
        if self.found is not None:
            details.append(f"Found: {self.found}")
        return " ".join(details)


class ValidationReport(BaseModel):
    """Structured validation result for a PRISMA flow."""

    errors: list[ValidationMessage] = Field(default_factory=list)
    warnings: list[ValidationMessage] = Field(default_factory=list)

    @property
    def ok(self) -> bool:
        """Whether the flow has no validation errors."""
        return not self.errors

    @property
    def has_errors(self) -> bool:
        """Whether the flow has validation errors."""
        return bool(self.errors)

    @property
    def has_warnings(self) -> bool:
        """Whether the flow has validation warnings."""
        return bool(self.warnings)

    def format_text(self) -> str:
        """Return a readable multi-line validation summary."""
        if self.ok and not self.warnings:
            return "Validation passed."

        sections: list[str] = []
        if self.errors:
            sections.append("Validation failed:")
            sections.extend(f"- {message.format()}" for message in self.errors)
        if self.warnings:
            if sections:
                sections.append("")
            sections.append("Validation warnings:")
            sections.extend(f"- {message.format()}" for message in self.warnings)
        return "\n".join(sections)


def _count_error(
    field: str,
    message: str,
    expected: int,
    found: int,
) -> ValidationMessage:
    return ValidationMessage(
        level="error",
        field=field,
        message=message,
        expected=expected,
        found=found,
    )


def _count_warning(
    field: str,
    message: str,
    expected: int | None = None,
    found: int | None = None,
) -> ValidationMessage:
    return ValidationMessage(
        level="warning",
        field=field,
        message=message,
        expected=expected,
        found=found,
    )


def validate_flow(
    flow: PrismaFlow,
    *,
    strict_included: bool = False,
) -> ValidationReport:
    """Validate PRISMA count relationships.

    Parameters
    ----------
    flow
        Flow model to validate.
    strict_included
        If true, treat the included-study reconciliation as an error. In v0.1
        it is a warning by default because one study can have multiple reports.

    """
    errors: list[ValidationMessage] = []
    warnings: list[ValidationMessage] = []

    expected_screened = (
        flow.identification.records_identified_total
        - flow.screening.records_removed_total
    )
    if flow.screening.records_screened != expected_screened:
        errors.append(
            _count_error(
                "screening.records_screened",
                "records_screened should equal identified records minus "
                "removed records.",
                expected_screened,
                flow.screening.records_screened,
            )
        )

    expected_reports_sought = (
        flow.screening.records_screened - flow.screening.records_excluded
    )
    if flow.eligibility.reports_sought != expected_reports_sought:
        errors.append(
            _count_error(
                "eligibility.reports_sought",
                "reports_sought should equal records_screened minus records_excluded.",
                expected_reports_sought,
                flow.eligibility.reports_sought,
            )
        )

    expected_reports_assessed = (
        flow.eligibility.reports_sought - flow.eligibility.reports_not_retrieved
    )
    if flow.eligibility.reports_assessed != expected_reports_assessed:
        errors.append(
            _count_error(
                "eligibility.reports_assessed",
                "reports_assessed should equal reports_sought minus "
                "reports_not_retrieved.",
                expected_reports_assessed,
                flow.eligibility.reports_assessed,
            )
        )

    reports_excluded_total = flow.eligibility.reports_excluded_total
    implied_exclusions = (
        flow.eligibility.reports_assessed - flow.included.studies_included
    )
    if not flow.eligibility.reports_excluded and implied_exclusions > 0:
        warnings.append(
            _count_warning(
                "eligibility.reports_excluded",
                "reports_excluded is empty, but reports_assessed is greater "
                "than studies_included.",
                implied_exclusions,
                reports_excluded_total,
            )
        )

    expected_included = flow.eligibility.reports_assessed - reports_excluded_total
    if expected_included != flow.included.studies_included:
        message = _count_warning(
            "included.studies_included",
            "studies_included does not equal reports_assessed minus "
            "reports_excluded_total; this may be valid because one study "
            "can have multiple reports.",
            expected_included,
            flow.included.studies_included,
        )
        if strict_included:
            errors.append(
                ValidationMessage(
                    level="error",
                    field=message.field,
                    message=message.message,
                    expected=message.expected,
                    found=message.found,
                )
            )
        else:
            warnings.append(message)

    return ValidationReport(errors=errors, warnings=warnings)
