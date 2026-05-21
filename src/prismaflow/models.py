"""
title: Pydantic data models for PRISMA-style flow diagrams.
"""

from __future__ import annotations

from collections.abc import Container
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from prismaflow.enums import PrismaTemplate

if TYPE_CHECKING:
    from prismaflow.validation import ValidationReport

Count = Annotated[int, Field(ge=0, strict=True)]
PathLike = str | Path


class FlowMetadata(BaseModel):
    """
    title: Optional metadata associated with a PRISMA flow.
    attributes:
      review_id:
        type: str | None
        description: Value for review_id.
      authors:
        type: list[str]
        description: Value for authors.
      created_at:
        type: date | None
        description: Value for created_at.
      notes:
        type: str | None
        description: Value for notes.
      extra:
        type: dict[str, str]
        description: Value for extra.
    """

    review_id: str | None = None
    authors: list[str] = Field(default_factory=list)
    created_at: date | None = None
    notes: str | None = None
    extra: dict[str, str] = Field(default_factory=dict)


class IdentificationStage(BaseModel):
    """
    title: Identification-stage counts.
    attributes:
      records_identified_databases:
        type: Count
        description: Value for records_identified_databases.
      records_identified_registers:
        type: Count
        description: Value for records_identified_registers.
    """

    records_identified_databases: Count
    records_identified_registers: Count

    @property
    def records_identified_total(self) -> int:
        """
        title: Total records identified from databases and registers.
        returns:
          type: int
          description: Return value.
        """
        return self.records_identified_databases + self.records_identified_registers


class ScreeningStage(BaseModel):
    """
    title: Screening-stage counts.
    attributes:
      records_removed_duplicates:
        type: Count
        description: Value for records_removed_duplicates.
      records_removed_automation:
        type: Count
        description: Value for records_removed_automation.
      records_removed_other:
        type: Count
        description: Value for records_removed_other.
      records_screened:
        type: Count
        description: Value for records_screened.
      records_excluded:
        type: Count
        description: Value for records_excluded.
    """

    records_removed_duplicates: Count
    records_removed_automation: Count
    records_removed_other: Count
    records_screened: Count
    records_excluded: Count

    @property
    def records_removed_total(self) -> int:
        """
        title: Total records removed before screening.
        returns:
          type: int
          description: Return value.
        """
        return (
            self.records_removed_duplicates
            + self.records_removed_automation
            + self.records_removed_other
        )


class EligibilityStage(BaseModel):
    """
    title: Eligibility-stage counts.
    attributes:
      reports_sought:
        type: Count
        description: Value for reports_sought.
      reports_not_retrieved:
        type: Count
        description: Value for reports_not_retrieved.
      reports_assessed:
        type: Count
        description: Value for reports_assessed.
      reports_excluded:
        type: dict[str, Count]
        description: Value for reports_excluded.
    """

    reports_sought: Count
    reports_not_retrieved: Count
    reports_assessed: Count
    reports_excluded: dict[str, Count] = Field(default_factory=dict)

    @field_validator("reports_excluded")
    @classmethod
    def _validate_reports_excluded(
        cls,
        value: dict[str, Count],
    ) -> dict[str, Count]:
        """
        title: _validate_reports_excluded.
        parameters:
          value:
            type: dict[str, Count]
            description: Value for value.
        returns:
          type: dict[str, Count]
          description: Return value.
        """
        for reason, count in value.items():
            if not isinstance(reason, str) or not reason.strip():
                raise ValueError("reports_excluded reasons must be non-empty strings")
            if not isinstance(count, int) or count < 0:
                raise ValueError(
                    "reports_excluded counts must be non-negative integers"
                )
        return value

    @property
    def reports_excluded_total(self) -> int:
        """
        title: Total reports excluded after eligibility assessment.
        returns:
          type: int
          description: Return value.
        """
        return sum(self.reports_excluded.values())


class IncludedStage(BaseModel):
    """
    title: Included-stage counts.
    attributes:
      studies_included:
        type: Count
        description: Value for studies_included.
    """

    studies_included: Count


class PrismaFlow(BaseModel):
    """
    title: A validated PRISMA-style flow diagram document.
    attributes:
      template:
        type: PrismaTemplate
        description: Value for template.
      title:
        type: str | None
        description: Value for title.
      identification:
        type: IdentificationStage
        description: Value for identification.
      screening:
        type: ScreeningStage
        description: Value for screening.
      eligibility:
        type: EligibilityStage
        description: Value for eligibility.
      included:
        type: IncludedStage
        description: Value for included.
      metadata:
        type: FlowMetadata | None
        description: Value for metadata.
    """

    template: PrismaTemplate = PrismaTemplate.PRISMA_2020_NEW_DATABASES_REGISTERS
    title: str | None = None
    identification: IdentificationStage
    screening: ScreeningStage
    eligibility: EligibilityStage
    included: IncludedStage
    metadata: FlowMetadata | None = None

    model_config = ConfigDict(
        use_enum_values=False,
        validate_assignment=True,
    )

    @classmethod
    def new_review(
        cls,
        *,
        records_identified_databases: int,
        records_identified_registers: int,
        records_removed_duplicates: int,
        records_removed_automation: int,
        records_removed_other: int,
        records_screened: int,
        records_excluded: int,
        reports_sought: int,
        reports_not_retrieved: int,
        reports_assessed: int,
        reports_excluded: dict[str, int] | None = None,
        studies_included: int,
        title: str | None = None,
        metadata: FlowMetadata | None = None,
        template: PrismaTemplate = PrismaTemplate.PRISMA_2020_NEW_DATABASES_REGISTERS,
    ) -> PrismaFlow:
        """
        title: Create a PRISMA 2020 new-review flow from flat count arguments.
        parameters:
          records_identified_databases:
            type: int
            description: Value for records_identified_databases.
          records_identified_registers:
            type: int
            description: Value for records_identified_registers.
          records_removed_duplicates:
            type: int
            description: Value for records_removed_duplicates.
          records_removed_automation:
            type: int
            description: Value for records_removed_automation.
          records_removed_other:
            type: int
            description: Value for records_removed_other.
          records_screened:
            type: int
            description: Value for records_screened.
          records_excluded:
            type: int
            description: Value for records_excluded.
          reports_sought:
            type: int
            description: Value for reports_sought.
          reports_not_retrieved:
            type: int
            description: Value for reports_not_retrieved.
          reports_assessed:
            type: int
            description: Value for reports_assessed.
          reports_excluded:
            type: dict[str, int] | None
            description: Value for reports_excluded.
          studies_included:
            type: int
            description: Value for studies_included.
          title:
            type: str | None
            description: Value for title.
          metadata:
            type: FlowMetadata | None
            description: Value for metadata.
          template:
            type: PrismaTemplate
            description: Value for template.
        returns:
          type: PrismaFlow
          description: Return value.
        """
        return cls(
            template=template,
            title=title,
            identification=IdentificationStage(
                records_identified_databases=records_identified_databases,
                records_identified_registers=records_identified_registers,
            ),
            screening=ScreeningStage(
                records_removed_duplicates=records_removed_duplicates,
                records_removed_automation=records_removed_automation,
                records_removed_other=records_removed_other,
                records_screened=records_screened,
                records_excluded=records_excluded,
            ),
            eligibility=EligibilityStage(
                reports_sought=reports_sought,
                reports_not_retrieved=reports_not_retrieved,
                reports_assessed=reports_assessed,
                reports_excluded=reports_excluded or {},
            ),
            included=IncludedStage(studies_included=studies_included),
            metadata=metadata,
        )

    def validate(  # type: ignore[override]
        self,
        *,
        strict_included: bool = False,
    ) -> ValidationReport:
        """
        title: Validate PRISMA count relationships and return a report.
        parameters:
          strict_included:
            type: bool
            description: Value for strict_included.
        returns:
          type: ValidationReport
          description: Return value.
        """
        from prismaflow.validation import validate_flow

        return validate_flow(self, strict_included=strict_included)

    def to_layout(self) -> Any:
        """
        title: Build the intermediate layout representation for this flow.
        returns:
          type: Any
          description: Return value.
        """
        from prismaflow.layout.engine import build_layout

        return build_layout(self)

    def to_svg(self, path: PathLike | None = None) -> str:
        """
        title: Render the flow as SVG and optionally write it to a file.
        parameters:
          path:
            type: PathLike | None
            description: Value for path.
        returns:
          type: str
          description: Return value.
        """
        from prismaflow.renderers.svg import SVGRenderer

        output = SVGRenderer().render(self.to_layout())
        _write_text(path, output)
        return output

    def _repr_svg_(self) -> str:
        """
        title: Return SVG for notebook rich display.
        returns:
          type: str
          description: >-
            SVG representation rendered inline by notebook frontends.
        """
        return self.to_svg()

    def _repr_mimebundle_(
        self,
        include: object = None,
        exclude: object = None,
    ) -> tuple[dict[str, str], dict[str, dict[str, str]]]:
        """
        title: Return a Jupyter MIME bundle for notebook rich display.
        parameters:
          include:
            type: object
            description: Optional frontend include filter.
          exclude:
            type: object
            description: Optional frontend exclude filter.
        returns:
          type: tuple[dict[str, str], dict[str, dict[str, str]]]
          description: SVG MIME data and empty metadata.
        """
        mime_type = "image/svg+xml"
        if _mime_filter_excludes(mime_type, include=include, exclude=exclude):
            return {}, {}
        return {mime_type: self.to_svg()}, {}

    def to_html(self, path: PathLike | None = None) -> str:
        """
        title: Render the flow as standalone HTML and optionally write it.
        parameters:
          path:
            type: PathLike | None
            description: Value for path.
        returns:
          type: str
          description: Return value.
        """
        from prismaflow.renderers.html import HTMLRenderer

        output = HTMLRenderer().render(self.to_layout())
        _write_text(path, output)
        return output

    def to_mermaid(self, path: PathLike | None = None) -> str:
        """
        title: Render the flow as Mermaid text and optionally write it.
        parameters:
          path:
            type: PathLike | None
            description: Value for path.
        returns:
          type: str
          description: Return value.
        """
        from prismaflow.renderers.mermaid import MermaidRenderer

        output = MermaidRenderer().render(self.to_layout())
        _write_text(path, output)
        return output

    def to_png(self, path: PathLike | None = None) -> bytes:
        """
        title: Export PNG if an optional backend is available.
        parameters:
          path:
            type: PathLike | None
            description: Value for path.
        returns:
          type: bytes
          description: Return value.
        """
        from prismaflow.renderers.png import PNGRenderer

        return PNGRenderer().render(self.to_layout(), path=path)

    def to_json(self, path: PathLike | None = None) -> str:
        """
        title: Serialize the flow to JSON and optionally write it.
        parameters:
          path:
            type: PathLike | None
            description: Value for path.
        returns:
          type: str
          description: Return value.
        """
        output = self.model_dump_json(indent=2)
        _write_text(path, output + "\n")
        return output

    @classmethod
    def from_json(cls, source: str | Path) -> PrismaFlow:
        """
        title: Load a flow from a JSON path or JSON string.
        parameters:
          source:
            type: str | Path
            description: Value for source.
        returns:
          type: PrismaFlow
          description: Return value.
        """
        from prismaflow.io.json import load_json

        return load_json(source)

    def to_yaml(self, path: PathLike | None = None) -> str:
        """
        title: Serialize the flow to YAML when PyYAML is installed.
        parameters:
          path:
            type: PathLike | None
            description: Value for path.
        returns:
          type: str
          description: Return value.
        """
        from prismaflow.io.yaml import dump_yaml

        output = dump_yaml(self)
        _write_text(path, output)
        return output

    @classmethod
    def from_yaml(cls, source: str | Path) -> PrismaFlow:
        """
        title: Load a flow from YAML when PyYAML is installed.
        parameters:
          source:
            type: str | Path
            description: Value for source.
        returns:
          type: PrismaFlow
          description: Return value.
        """
        from prismaflow.io.yaml import load_yaml

        return load_yaml(source)


def new_review(
    *,
    records_identified_databases: int,
    records_identified_registers: int,
    records_removed_duplicates: int,
    records_removed_automation: int,
    records_removed_other: int,
    records_screened: int,
    records_excluded: int,
    reports_sought: int,
    reports_not_retrieved: int,
    reports_assessed: int,
    reports_excluded: dict[str, int] | None = None,
    studies_included: int,
    title: str | None = None,
    metadata: FlowMetadata | None = None,
    template: PrismaTemplate = PrismaTemplate.PRISMA_2020_NEW_DATABASES_REGISTERS,
) -> PrismaFlow:
    """
    title: Create a PRISMA 2020 new-review flow from flat count arguments.
    parameters:
      records_identified_databases:
        type: int
        description: Value for records_identified_databases.
      records_identified_registers:
        type: int
        description: Value for records_identified_registers.
      records_removed_duplicates:
        type: int
        description: Value for records_removed_duplicates.
      records_removed_automation:
        type: int
        description: Value for records_removed_automation.
      records_removed_other:
        type: int
        description: Value for records_removed_other.
      records_screened:
        type: int
        description: Value for records_screened.
      records_excluded:
        type: int
        description: Value for records_excluded.
      reports_sought:
        type: int
        description: Value for reports_sought.
      reports_not_retrieved:
        type: int
        description: Value for reports_not_retrieved.
      reports_assessed:
        type: int
        description: Value for reports_assessed.
      reports_excluded:
        type: dict[str, int] | None
        description: Value for reports_excluded.
      studies_included:
        type: int
        description: Value for studies_included.
      title:
        type: str | None
        description: Value for title.
      metadata:
        type: FlowMetadata | None
        description: Value for metadata.
      template:
        type: PrismaTemplate
        description: Value for template.
    returns:
      type: PrismaFlow
      description: Return value.
    """
    return PrismaFlow.new_review(
        template=template,
        title=title,
        records_identified_databases=records_identified_databases,
        records_identified_registers=records_identified_registers,
        records_removed_duplicates=records_removed_duplicates,
        records_removed_automation=records_removed_automation,
        records_removed_other=records_removed_other,
        records_screened=records_screened,
        records_excluded=records_excluded,
        reports_sought=reports_sought,
        reports_not_retrieved=reports_not_retrieved,
        reports_assessed=reports_assessed,
        reports_excluded=reports_excluded,
        studies_included=studies_included,
        metadata=metadata,
    )


def _mime_filter_excludes(
    mime_type: str,
    *,
    include: object,
    exclude: object,
) -> bool:
    """
    title: Return whether a Jupyter MIME filter excludes a MIME type.
    parameters:
      mime_type:
        type: str
        description: MIME type to test.
      include:
        type: object
        description: Optional include filter provided by a notebook frontend.
      exclude:
        type: object
        description: Optional exclude filter provided by a notebook frontend.
    returns:
      type: bool
      description: Whether the MIME type should be omitted.
    """
    if include is not None and not _contains_mime_type(include, mime_type):
        return True
    return exclude is not None and _contains_mime_type(exclude, mime_type)


def _contains_mime_type(values: object, mime_type: str) -> bool:
    """
    title: Return whether a filter object contains a MIME type.
    parameters:
      values:
        type: object
        description: Filter value provided by a notebook frontend.
      mime_type:
        type: str
        description: MIME type to find.
    returns:
      type: bool
      description: Whether the filter contains the MIME type.
    """
    return isinstance(values, Container) and mime_type in values


def _write_text(path: PathLike | None, content: str) -> None:
    """
    title: _write_text.
    parameters:
      path:
        type: PathLike | None
        description: Value for path.
      content:
        type: str
        description: Value for content.
    """
    if path is None:
        return
    Path(path).write_text(content, encoding="utf-8")
