"""
title: PRISMA 2020 new-review databases/registers layout template.
"""

from __future__ import annotations

from prismaflow.layout.engine import DiagramEdge, DiagramLayout, DiagramNode
from prismaflow.layout.geometry import Point, Rect
from prismaflow.models import PrismaFlow


class Prisma2020NewTemplate:
    """
    title: Template for PRISMA 2020 new reviews using databases/registers.
    """

    def build(self, flow: PrismaFlow) -> DiagramLayout:
        """
        title: Build a stable template-based layout.
        parameters:
          flow:
            type: PrismaFlow
            description: Value for flow.
        returns:
          type: DiagramLayout
          description: Return value.
        """
        stage_label_x = 38.0
        stage_label_width = 34.0
        main_x = 100.0
        side_x = 440.0
        box_width = 260.0
        side_width = 260.0
        header_y = 62.0
        header_height = 32.0
        identified_y = 112.0
        identification_height = 112.0
        box_height = 74.0
        tall_height = 122.0
        screened_y = 272.0
        reports_sought_y = 378.0
        reports_assessed_y = 484.0
        reports_excluded_y = 478.0
        included_y = 642.0
        included_height = 86.0
        notes_x = 28.0
        notes_width = 690.0
        identification = flow.identification
        screening = flow.screening
        eligibility = flow.eligibility
        included = flow.included

        nodes = [
            DiagramNode(
                id="databases_registers_header",
                rect=Rect(
                    main_x,
                    header_y,
                    side_x + side_width - main_x,
                    header_height,
                ),
                text="Identification of studies via databases and registers",
                kind="header",
                css_class="process-header",
            ),
            DiagramNode(
                id="identification_label",
                rect=Rect(
                    stage_label_x,
                    identified_y,
                    stage_label_width,
                    identification_height,
                ),
                text="Identification",
                kind="header",
                css_class="stage-label",
            ),
            DiagramNode(
                id="screening_label",
                rect=Rect(
                    stage_label_x,
                    screened_y,
                    stage_label_width,
                    reports_excluded_y + tall_height - screened_y,
                ),
                text="Screening",
                kind="header",
                css_class="stage-label",
            ),
            DiagramNode(
                id="included_label",
                rect=Rect(
                    stage_label_x,
                    included_y,
                    stage_label_width,
                    included_height,
                ),
                text="Included",
                kind="header",
                css_class="stage-label",
            ),
            DiagramNode(
                id="identified",
                rect=Rect(main_x, identified_y, box_width, identification_height),
                text=(
                    "Records identified from*:\n"
                    f"Databases (n = {identification.records_identified_databases})\n"
                    f"Registers (n = {identification.records_identified_registers})"
                ),
                kind="stage",
            ),
            DiagramNode(
                id="removed",
                rect=Rect(side_x, identified_y, side_width, identification_height),
                text=(
                    "Records removed before screening:\n"
                    "Duplicate records removed\n"
                    f"(n = {screening.records_removed_duplicates})\n"
                    "Records marked as ineligible by automation tools\n"
                    f"(n = {screening.records_removed_automation})\n"
                    "Records removed for other reasons\n"
                    f"(n = {screening.records_removed_other})"
                ),
                kind="stage",
            ),
            DiagramNode(
                id="screened",
                rect=Rect(main_x, screened_y, box_width, box_height),
                text=f"Records screened\n(n = {screening.records_screened})",
                kind="stage",
            ),
            DiagramNode(
                id="records_excluded",
                rect=Rect(side_x, screened_y, side_width, box_height),
                text=f"Records excluded**\n(n = {screening.records_excluded})",
                kind="exclusion",
            ),
            DiagramNode(
                id="reports_sought",
                rect=Rect(main_x, reports_sought_y, box_width, box_height),
                text=(
                    f"Reports sought for retrieval\n(n = {eligibility.reports_sought})"
                ),
                kind="stage",
            ),
            DiagramNode(
                id="reports_not_retrieved",
                rect=Rect(side_x, reports_sought_y, side_width, box_height),
                text=(
                    f"Reports not retrieved\n(n = {eligibility.reports_not_retrieved})"
                ),
                kind="exclusion",
            ),
            DiagramNode(
                id="reports_assessed",
                rect=Rect(main_x, reports_assessed_y, box_width, box_height),
                text=(
                    "Reports assessed for eligibility\n"
                    f"(n = {eligibility.reports_assessed})"
                ),
                kind="stage",
            ),
            DiagramNode(
                id="reports_excluded",
                rect=Rect(side_x, reports_excluded_y, side_width, tall_height),
                text=self._reports_excluded_text(flow),
                kind="exclusion",
            ),
            DiagramNode(
                id="included",
                rect=Rect(main_x, included_y, box_width, included_height),
                text=(f"Studies included in review\n(n = {included.studies_included})"),
                kind="stage",
            ),
            DiagramNode(
                id="database_note",
                rect=Rect(notes_x, 762.0, notes_width, 44.0),
                text=(
                    "*Consider, if feasible to do so, reporting the number of "
                    "records identified from each database or register searched "
                    "(rather than the total number across all databases/registers)."
                ),
                kind="note",
                css_class="footnote",
            ),
            DiagramNode(
                id="automation_note",
                rect=Rect(notes_x, 816.0, notes_width, 38.0),
                text=(
                    "**If automation tools were used, indicate how many records "
                    "were excluded by a human and how many were excluded by "
                    "automation tools."
                ),
                kind="note",
                css_class="footnote",
            ),
            DiagramNode(
                id="source_citation",
                rect=Rect(notes_x, 900.0, notes_width, 40.0),
                text=(
                    "From: Page MJ, McKenzie JE, Bossuyt PM, Boutron I, "
                    "Hoffmann TC, Mulrow CD, et al. The PRISMA 2020 statement: "
                    "an updated guideline for reporting systematic reviews. "
                    "BMJ. 2021;372:n71. doi: 10.1136/bmj.n71"
                ),
                kind="note",
                css_class="source",
            ),
            DiagramNode(
                id="source_link",
                rect=Rect(214.0, 948.0, 332.0, 18.0),
                text="For more information, visit: http://www.prisma-statement.org/",
                kind="note",
                href="https://www.prisma-statement.org/",
                css_class="source-link",
            ),
        ]

        edges = [
            DiagramEdge(
                id="identified_to_removed",
                source_id="identified",
                target_id="removed",
                source_anchor="right",
                target_anchor="left",
            ),
            DiagramEdge(
                id="identified_to_screened",
                source_id="identified",
                target_id="screened",
                source_anchor="bottom",
                target_anchor="top",
            ),
            DiagramEdge(
                id="screened_to_reports_sought",
                source_id="screened",
                target_id="reports_sought",
                source_anchor="bottom",
                target_anchor="top",
            ),
            DiagramEdge(
                id="screened_to_records_excluded",
                source_id="screened",
                target_id="records_excluded",
                source_anchor="right",
                target_anchor="left",
            ),
            DiagramEdge(
                id="reports_sought_to_reports_assessed",
                source_id="reports_sought",
                target_id="reports_assessed",
                source_anchor="bottom",
                target_anchor="top",
            ),
            DiagramEdge(
                id="reports_sought_to_not_retrieved",
                source_id="reports_sought",
                target_id="reports_not_retrieved",
                source_anchor="right",
                target_anchor="left",
            ),
            DiagramEdge(
                id="reports_assessed_to_included",
                source_id="reports_assessed",
                target_id="included",
                source_anchor="bottom",
                target_anchor="top",
            ),
            DiagramEdge(
                id="reports_assessed_to_reports_excluded",
                source_id="reports_assessed",
                target_id="reports_excluded",
                source_anchor="right",
                target_anchor="left",
                path=[
                    Point(main_x + box_width, reports_assessed_y + box_height / 2),
                    Point(side_x, reports_assessed_y + box_height / 2),
                ],
            ),
        ]

        return DiagramLayout(
            width=740.0,
            height=982.0,
            nodes=nodes,
            edges=edges,
            title=flow.title,
        )

    @staticmethod
    def _reports_excluded_text(flow: PrismaFlow) -> str:
        """
        title: _reports_excluded_text.
        parameters:
          flow:
            type: PrismaFlow
            description: Value for flow.
        returns:
          type: str
          description: Return value.
        """
        if not flow.eligibility.reports_excluded:
            return "Reports excluded\n(n = 0)"
        lines = ["Reports excluded:"]
        lines.extend(
            f"{reason} (n = {count})"
            for reason, count in flow.eligibility.reports_excluded.items()
        )
        return "\n".join(lines)
