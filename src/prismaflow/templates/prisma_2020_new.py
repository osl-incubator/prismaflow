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

    DEFAULT_TITLE = "PRISMA Flow Diagram"

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
        if flow.has_other_methods:
            return self._build_with_other_methods(flow)
        return self._build_databases_registers(flow)

    def _build_databases_registers(self, flow: PrismaFlow) -> DiagramLayout:
        """
        title: Build the databases/registers-only new-review layout.
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
        identification_height = (
            148.0 if flow.identification.has_source_details else 112.0
        )
        box_height = 74.0
        tall_height = 122.0
        screened_y = identified_y + identification_height + 48.0
        reports_sought_y = screened_y + 106.0
        reports_assessed_y = reports_sought_y + 106.0
        reports_excluded_y = reports_assessed_y - 6.0
        included_y = reports_assessed_y + 158.0
        included_height = 106.0 if flow.included.reports_included is not None else 86.0
        screening_height = reports_excluded_y + tall_height - screened_y
        layout_height = included_y + included_height + 22.0
        screening = flow.screening
        eligibility = flow.eligibility

        nodes = [
            DiagramNode(
                id="databases_registers_header",
                rect=Rect(
                    main_x,
                    header_y,
                    side_x + side_width - main_x,
                    header_height,
                ),
                text="Identification of new studies via databases and registers",
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
                    screening_height,
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
                text=self._identified_text(flow),
                kind="stage",
            ),
            DiagramNode(
                id="removed",
                rect=Rect(side_x, identified_y, side_width, identification_height),
                text=self._removed_text(flow),
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
                text=f"Records excluded\n(n = {screening.records_excluded})",
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
                text=self._included_text(flow),
                kind="stage",
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
            height=layout_height,
            nodes=nodes,
            edges=edges,
            title=self._diagram_title(flow),
        )

    def _build_with_other_methods(self, flow: PrismaFlow) -> DiagramLayout:
        """
        title: Build the new-review layout with other search methods.
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
        left_x = 100.0
        left_side_x = 380.0
        right_x = 710.0
        right_side_x = 970.0
        box_width = 230.0
        left_side_width = 250.0
        right_side_width = 190.0
        header_y = 62.0
        header_height = 32.0
        identified_y = 112.0
        identification_height = (
            148.0 if flow.identification.has_source_details else 112.0
        )
        box_height = 74.0
        tall_height = 122.0
        screened_y = identified_y + identification_height + 48.0
        reports_sought_y = screened_y + 106.0
        reports_assessed_y = reports_sought_y + 106.0
        reports_excluded_y = reports_assessed_y - 6.0
        included_y = reports_assessed_y + 158.0
        included_x = 430.0
        included_width = 350.0
        included_height = 106.0 if flow.included.reports_included is not None else 86.0
        screening_height = reports_excluded_y + tall_height - screened_y
        layout_height = included_y + included_height + 22.0
        screening = flow.screening
        eligibility = flow.eligibility
        included_center_x = included_x + included_width / 2
        included_top_y = included_y
        edge_mid_y = included_y - 24.0

        nodes = [
            DiagramNode(
                id="databases_registers_header",
                rect=Rect(
                    left_x,
                    header_y,
                    left_side_x + left_side_width - left_x,
                    header_height,
                ),
                text="Identification of new studies via databases and registers",
                kind="header",
                css_class="process-header",
            ),
            DiagramNode(
                id="other_methods_header",
                rect=Rect(
                    right_x,
                    header_y,
                    right_side_x + right_side_width - right_x,
                    header_height,
                ),
                text="Identification of new studies via other methods",
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
                    screening_height,
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
                rect=Rect(left_x, identified_y, box_width, identification_height),
                text=self._identified_text(flow),
                kind="stage",
            ),
            DiagramNode(
                id="removed",
                rect=Rect(
                    left_side_x,
                    identified_y,
                    left_side_width,
                    identification_height,
                ),
                text=self._removed_text(flow),
                kind="stage",
            ),
            DiagramNode(
                id="other_identified",
                rect=Rect(right_x, identified_y, box_width, identification_height),
                text=self._other_identified_text(flow),
                kind="stage",
            ),
            DiagramNode(
                id="screened",
                rect=Rect(left_x, screened_y, box_width, box_height),
                text=f"Records screened\n(n = {screening.records_screened})",
                kind="stage",
            ),
            DiagramNode(
                id="records_excluded",
                rect=Rect(left_side_x, screened_y, left_side_width, box_height),
                text=f"Records excluded\n(n = {screening.records_excluded})",
                kind="exclusion",
            ),
            DiagramNode(
                id="reports_sought",
                rect=Rect(left_x, reports_sought_y, box_width, box_height),
                text=(
                    f"Reports sought for retrieval\n(n = {eligibility.reports_sought})"
                ),
                kind="stage",
            ),
            DiagramNode(
                id="reports_not_retrieved",
                rect=Rect(left_side_x, reports_sought_y, left_side_width, box_height),
                text=(
                    f"Reports not retrieved\n(n = {eligibility.reports_not_retrieved})"
                ),
                kind="exclusion",
            ),
            DiagramNode(
                id="other_reports_sought",
                rect=Rect(right_x, reports_sought_y, box_width, box_height),
                text=(
                    "Reports sought for retrieval\n"
                    f"(n = {eligibility.other_sought_reports})"
                ),
                kind="stage",
            ),
            DiagramNode(
                id="other_reports_not_retrieved",
                rect=Rect(right_side_x, reports_sought_y, right_side_width, box_height),
                text=(
                    "Reports not retrieved\n"
                    f"(n = {eligibility.other_notretrieved_reports})"
                ),
                kind="exclusion",
            ),
            DiagramNode(
                id="reports_assessed",
                rect=Rect(left_x, reports_assessed_y, box_width, box_height),
                text=(
                    "Reports assessed for eligibility\n"
                    f"(n = {eligibility.reports_assessed})"
                ),
                kind="stage",
            ),
            DiagramNode(
                id="reports_excluded",
                rect=Rect(
                    left_side_x, reports_excluded_y, left_side_width, tall_height
                ),
                text=self._reports_excluded_text(flow),
                kind="exclusion",
            ),
            DiagramNode(
                id="other_reports_assessed",
                rect=Rect(right_x, reports_assessed_y, box_width, box_height),
                text=(
                    "Reports assessed for eligibility\n"
                    f"(n = {eligibility.other_assessed})"
                ),
                kind="stage",
            ),
            DiagramNode(
                id="other_reports_excluded",
                rect=Rect(
                    right_side_x,
                    reports_excluded_y,
                    right_side_width,
                    tall_height,
                ),
                text=self._other_reports_excluded_text(flow),
                kind="exclusion",
            ),
            DiagramNode(
                id="included",
                rect=Rect(included_x, included_y, included_width, included_height),
                text=self._included_text(flow),
                kind="stage",
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
                id="reports_assessed_to_reports_excluded",
                source_id="reports_assessed",
                target_id="reports_excluded",
                source_anchor="right",
                target_anchor="left",
                path=[
                    Point(left_x + box_width, reports_assessed_y + box_height / 2),
                    Point(left_side_x, reports_assessed_y + box_height / 2),
                ],
            ),
            DiagramEdge(
                id="other_identified_to_reports_sought",
                source_id="other_identified",
                target_id="other_reports_sought",
                source_anchor="bottom",
                target_anchor="top",
            ),
            DiagramEdge(
                id="other_reports_sought_to_assessed",
                source_id="other_reports_sought",
                target_id="other_reports_assessed",
                source_anchor="bottom",
                target_anchor="top",
            ),
            DiagramEdge(
                id="other_reports_sought_to_not_retrieved",
                source_id="other_reports_sought",
                target_id="other_reports_not_retrieved",
                source_anchor="right",
                target_anchor="left",
            ),
            DiagramEdge(
                id="other_reports_assessed_to_excluded",
                source_id="other_reports_assessed",
                target_id="other_reports_excluded",
                source_anchor="right",
                target_anchor="left",
                path=[
                    Point(right_x + box_width, reports_assessed_y + box_height / 2),
                    Point(right_side_x, reports_assessed_y + box_height / 2),
                ],
            ),
            DiagramEdge(
                id="reports_assessed_to_included",
                source_id="reports_assessed",
                target_id="included",
                source_anchor="bottom",
                target_anchor="top",
                path=[
                    Point(left_x + box_width / 2, reports_assessed_y + box_height),
                    Point(left_x + box_width / 2, edge_mid_y),
                    Point(included_center_x, edge_mid_y),
                    Point(included_center_x, included_top_y),
                ],
            ),
            DiagramEdge(
                id="other_reports_assessed_to_included",
                source_id="other_reports_assessed",
                target_id="included",
                source_anchor="bottom",
                target_anchor="top",
                path=[
                    Point(right_x + box_width / 2, reports_assessed_y + box_height),
                    Point(right_x + box_width / 2, edge_mid_y),
                    Point(included_center_x, edge_mid_y),
                    Point(included_center_x, included_top_y),
                ],
            ),
        ]

        return DiagramLayout(
            width=1180.0,
            height=layout_height,
            nodes=nodes,
            edges=edges,
            title=self._diagram_title(flow),
        )

    @classmethod
    def _diagram_title(cls, flow: PrismaFlow) -> str:
        """
        title: Return the user title or the PRISMA template title.
        parameters:
          flow:
            type: PrismaFlow
            description: Value for flow.
        returns:
          type: str
          description: Return value.
        """
        if flow.title is not None:
            return flow.title
        return cls.DEFAULT_TITLE

    @staticmethod
    def _identified_text(flow: PrismaFlow) -> str:
        """
        title: Build the databases/registers identification text.
        parameters:
          flow:
            type: PrismaFlow
            description: Value for flow.
        returns:
          type: str
          description: Return value.
        """
        identification = flow.identification
        lines = [
            "Records identified from:",
            f"Databases (n = {identification.records_identified_databases})",
        ]
        if identification.database_specific_results:
            lines.append(identification.database_specific_results)
        lines.append(f"Registers (n = {identification.records_identified_registers})")
        if identification.register_specific_results:
            lines.append(identification.register_specific_results)
        return "\n".join(lines)

    @staticmethod
    def _other_identified_text(flow: PrismaFlow) -> str:
        """
        title: Build the other-methods identification text.
        parameters:
          flow:
            type: PrismaFlow
            description: Value for flow.
        returns:
          type: str
          description: Return value.
        """
        identification = flow.identification
        return "\n".join(
            [
                "Records identified from:",
                f"Websites (n = {identification.website_results})",
                f"Organisations (n = {identification.organisation_results})",
                f"Citation searching (n = {identification.citations_results})",
            ]
        )

    @staticmethod
    def _removed_text(flow: PrismaFlow) -> str:
        """
        title: Build the removed-before-screening text.
        parameters:
          flow:
            type: PrismaFlow
            description: Value for flow.
        returns:
          type: str
          description: Return value.
        """
        screening = flow.screening
        return "\n".join(
            [
                "Records removed before screening:",
                f"Duplicate records (n = {screening.records_removed_duplicates})",
                (
                    "Records marked as ineligible by automation tools "
                    f"(n = {screening.records_removed_automation})"
                ),
                "Records removed for other reasons",
                f"(n = {screening.records_removed_other})",
            ]
        )

    @staticmethod
    def _included_text(flow: PrismaFlow) -> str:
        """
        title: Build the included-stage text.
        parameters:
          flow:
            type: PrismaFlow
            description: Value for flow.
        returns:
          type: str
          description: Return value.
        """
        included = flow.included
        lines = [
            "New studies included in review",
            f"(n = {included.studies_included})",
        ]
        if included.reports_included is not None:
            lines.extend(
                [
                    "Reports of new included studies",
                    f"(n = {included.reports_included})",
                ]
            )
        return "\n".join(lines)

    @staticmethod
    def _reports_excluded_text(flow: PrismaFlow) -> str:
        """
        title: Build the databases/registers exclusion text.
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

    @staticmethod
    def _other_reports_excluded_text(flow: PrismaFlow) -> str:
        """
        title: Build the other-methods exclusion text.
        parameters:
          flow:
            type: PrismaFlow
            description: Value for flow.
        returns:
          type: str
          description: Return value.
        """
        if not flow.eligibility.other_excluded:
            return "Reports excluded\n(n = 0)"
        lines = ["Reports excluded:"]
        lines.extend(
            f"{reason} (n = {count})"
            for reason, count in flow.eligibility.other_excluded.items()
        )
        return "\n".join(lines)
