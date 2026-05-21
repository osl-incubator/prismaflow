"""
title: Validation report objects and PRISMA count checks.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from prismaflow.models import PrismaFlow

ValidationLevel = Literal["error", "warning"]


class ValidationMessage(BaseModel):
    """
    title: A single validation finding.
    attributes:
      level:
        type: ValidationLevel
        description: Value for level.
      field:
        type: str
        description: Value for field.
      message:
        type: str
        description: Value for message.
      expected:
        type: int | None
        description: Value for expected.
      found:
        type: int | None
        description: Value for found.
    """

    level: ValidationLevel
    field: str
    message: str
    expected: int | None = None
    found: int | None = None

    model_config = ConfigDict(frozen=True)

    def format(self) -> str:
        """
        title: Return a human-readable validation line.
        returns:
          type: str
          description: Return value.
        """
        details: list[str] = [self.message]
        if self.expected is not None:
            details.append(f"Expected: {self.expected}")
        if self.found is not None:
            details.append(f"Found: {self.found}")
        return " ".join(details)


class ValidationReport(BaseModel):
    """
    title: Structured validation result for a PRISMA flow.
    attributes:
      errors:
        type: list[ValidationMessage]
        description: Value for errors.
      warnings:
        type: list[ValidationMessage]
        description: Value for warnings.
    """

    errors: list[ValidationMessage] = Field(default_factory=list)
    warnings: list[ValidationMessage] = Field(default_factory=list)

    @property
    def ok(self) -> bool:
        """
        title: Whether the flow has no validation errors.
        returns:
          type: bool
          description: Return value.
        """
        return not self.errors

    @property
    def has_errors(self) -> bool:
        """
        title: Whether the flow has validation errors.
        returns:
          type: bool
          description: Return value.
        """
        return bool(self.errors)

    @property
    def has_warnings(self) -> bool:
        """
        title: Whether the flow has validation warnings.
        returns:
          type: bool
          description: Return value.
        """
        return bool(self.warnings)

    def format_text(self) -> str:
        """
        title: Return a readable multi-line validation summary.
        returns:
          type: str
          description: Return value.
        """
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
    """
    title: _count_error.
    parameters:
      field:
        type: str
        description: Value for field.
      message:
        type: str
        description: Value for message.
      expected:
        type: int
        description: Value for expected.
      found:
        type: int
        description: Value for found.
    returns:
      type: ValidationMessage
      description: Return value.
    """
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
    """
    title: _count_warning.
    parameters:
      field:
        type: str
        description: Value for field.
      message:
        type: str
        description: Value for message.
      expected:
        type: int | None
        description: Value for expected.
      found:
        type: int | None
        description: Value for found.
    returns:
      type: ValidationMessage
      description: Return value.
    """
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
    """
    title: Validate PRISMA count relationships.
    parameters:
      flow:
        type: PrismaFlow
        description: Value for flow.
      strict_included:
        type: bool
        description: Value for strict_included.
    returns:
      type: ValidationReport
      description: Return value.
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

    if flow.has_other_methods:
        expected_other_sought = flow.identification.other_methods_total
        if flow.eligibility.other_sought_reports != expected_other_sought:
            errors.append(
                _count_error(
                    "eligibility.other_sought_reports",
                    "other_sought_reports should equal records identified "
                    "through other methods.",
                    expected_other_sought,
                    flow.eligibility.other_sought_reports,
                )
            )

        expected_other_assessed = (
            flow.eligibility.other_sought_reports
            - flow.eligibility.other_notretrieved_reports
        )
        if flow.eligibility.other_assessed != expected_other_assessed:
            errors.append(
                _count_error(
                    "eligibility.other_assessed",
                    "other_assessed should equal other_sought_reports minus "
                    "other_notretrieved_reports.",
                    expected_other_assessed,
                    flow.eligibility.other_assessed,
                )
            )

    reports_excluded_total = flow.eligibility.all_reports_excluded_total
    implied_exclusions = flow.eligibility.all_reports_assessed - (
        flow.included.studies_included
    )
    if (
        not flow.eligibility.reports_excluded
        and not flow.eligibility.other_excluded
        and implied_exclusions > 0
    ):
        warnings.append(
            _count_warning(
                "eligibility.reports_excluded",
                "reports_excluded is empty, but reports_assessed is greater "
                "than studies_included.",
                implied_exclusions,
                reports_excluded_total,
            )
        )

    expected_included = flow.eligibility.all_reports_assessed - reports_excluded_total
    if expected_included != flow.included.studies_included:
        message = _count_warning(
            "included.studies_included",
            "studies_included does not equal total reports assessed minus "
            "total reports excluded; this may be valid because one study can "
            "have multiple reports.",
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

    if (
        flow.included.reports_included is not None
        and expected_included != flow.included.reports_included
    ):
        warnings.append(
            _count_warning(
                "included.reports_included",
                "reports_included does not equal total reports assessed minus "
                "total reports excluded.",
                expected_included,
                flow.included.reports_included,
            )
        )

    return ValidationReport(errors=errors, warnings=warnings)
