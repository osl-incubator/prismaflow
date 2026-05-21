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
        main_x = 300.0
        side_x = 660.0
        box_width = 300.0
        side_width = 270.0
        box_height = 82.0
        tall_height = 118.0
        y0 = 90.0
        gap = 104.0
        identification = flow.identification
        screening = flow.screening
        eligibility = flow.eligibility
        included = flow.included

        nodes = [
            DiagramNode(
                id="identified",
                rect=Rect(main_x, y0, box_width, box_height),
                text=(
                    "Records identified from:\n"
                    f"Databases (n = {identification.records_identified_databases})\n"
                    f"Registers (n = {identification.records_identified_registers})"
                ),
                kind="stage",
            ),
            DiagramNode(
                id="removed",
                rect=Rect(main_x, y0 + gap, box_width, tall_height),
                text=(
                    "Records removed before screening:\n"
                    "Duplicate records removed "
                    f"(n = {screening.records_removed_duplicates})\n"
                    "Records marked as ineligible by automation tools "
                    f"(n = {screening.records_removed_automation})\n"
                    "Records removed for other reasons "
                    f"(n = {screening.records_removed_other})"
                ),
                kind="stage",
            ),
            DiagramNode(
                id="screened",
                rect=Rect(main_x, y0 + gap * 2 + 36, box_width, box_height),
                text=f"Records screened\n(n = {screening.records_screened})",
                kind="stage",
            ),
            DiagramNode(
                id="records_excluded",
                rect=Rect(side_x, y0 + gap * 2 + 36, side_width, box_height),
                text=f"Records excluded\n(n = {screening.records_excluded})",
                kind="exclusion",
            ),
            DiagramNode(
                id="reports_sought",
                rect=Rect(main_x, y0 + gap * 3 + 36, box_width, box_height),
                text=(
                    f"Reports sought for retrieval\n(n = {eligibility.reports_sought})"
                ),
                kind="stage",
            ),
            DiagramNode(
                id="reports_not_retrieved",
                rect=Rect(side_x, y0 + gap * 3 + 36, side_width, box_height),
                text=(
                    f"Reports not retrieved\n(n = {eligibility.reports_not_retrieved})"
                ),
                kind="exclusion",
            ),
            DiagramNode(
                id="reports_assessed",
                rect=Rect(main_x, y0 + gap * 4 + 36, box_width, box_height),
                text=(
                    "Reports assessed for eligibility\n"
                    f"(n = {eligibility.reports_assessed})"
                ),
                kind="stage",
            ),
            DiagramNode(
                id="reports_excluded",
                rect=Rect(side_x, y0 + gap * 4 + 22, side_width, tall_height),
                text=self._reports_excluded_text(flow),
                kind="exclusion",
            ),
            DiagramNode(
                id="included",
                rect=Rect(main_x, y0 + gap * 5 + 50, box_width, box_height),
                text=(f"Studies included in review\n(n = {included.studies_included})"),
                kind="stage",
            ),
        ]

        edges = [
            DiagramEdge(
                id="identified_to_removed",
                source_id="identified",
                target_id="removed",
                source_anchor="bottom",
                target_anchor="top",
            ),
            DiagramEdge(
                id="removed_to_screened",
                source_id="removed",
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
                    Point(main_x + box_width, y0 + gap * 4 + 77),
                    Point(side_x, y0 + gap * 4 + 77),
                ],
            ),
        ]

        return DiagramLayout(
            width=980.0,
            height=780.0,
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
