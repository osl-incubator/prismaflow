"""
title: Layout dataclasses and template dispatch.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from prismaflow.enums import PrismaTemplate
from prismaflow.exceptions import TemplateNotSupportedError
from prismaflow.layout.geometry import Anchor, Point, Rect

NodeKind = Literal["stage", "exclusion", "header", "note"]


@dataclass
class DiagramNode:
    """
    title: A positioned text box in a diagram.
    attributes:
      id:
        type: str
        description: Value for id.
      rect:
        type: Rect
        description: Value for rect.
      text:
        type: str
        description: Value for text.
      kind:
        type: NodeKind
        description: Value for kind.
      href:
        type: str | None
        description: Value for href.
      tooltip:
        type: str | None
        description: Value for tooltip.
      css_class:
        type: str | None
        description: Value for css_class.
    """

    id: str
    rect: Rect
    text: str
    kind: NodeKind = "stage"
    href: str | None = None
    tooltip: str | None = None
    css_class: str | None = None


@dataclass
class DiagramEdge:
    """
    title: An arrow connecting two diagram nodes.
    attributes:
      id:
        type: str
        description: Value for id.
      source_id:
        type: str
        description: Value for source_id.
      target_id:
        type: str
        description: Value for target_id.
      source_anchor:
        type: Anchor
        description: Value for source_anchor.
      target_anchor:
        type: Anchor
        description: Value for target_anchor.
      label:
        type: str | None
        description: Value for label.
      path:
        type: list[Point] | None
        description: Value for path.
      css_class:
        type: str | None
        description: Value for css_class.
    """

    id: str
    source_id: str
    target_id: str
    source_anchor: Anchor
    target_anchor: Anchor
    label: str | None = None
    path: list[Point] | None = None
    css_class: str | None = None


@dataclass
class DiagramLayout:
    """
    title: Complete intermediate representation for a rendered diagram.
    attributes:
      width:
        type: float
        description: Value for width.
      height:
        type: float
        description: Value for height.
      nodes:
        type: list[DiagramNode]
        description: Value for nodes.
      edges:
        type: list[DiagramEdge]
        description: Value for edges.
      title:
        type: str | None
        description: Value for title.
    """

    width: float
    height: float
    nodes: list[DiagramNode] = field(default_factory=list)
    edges: list[DiagramEdge] = field(default_factory=list)
    title: str | None = None

    def node_by_id(self, node_id: str) -> DiagramNode:
        """
        title: Return a node by ID.
        parameters:
          node_id:
            type: str
            description: Value for node_id.
        returns:
          type: DiagramNode
          description: Return value.
        """
        for node in self.nodes:
            if node.id == node_id:
                return node
        raise KeyError(node_id)


def build_layout(flow: object) -> DiagramLayout:
    """
    title: Build a diagram layout for a supported PRISMA flow template.
    parameters:
      flow:
        type: object
        description: Value for flow.
    returns:
      type: DiagramLayout
      description: Return value.
    """
    from prismaflow.models import PrismaFlow
    from prismaflow.templates.prisma_2020_new import Prisma2020NewTemplate

    if not isinstance(flow, PrismaFlow):
        raise TypeError("build_layout expects a PrismaFlow instance")

    if flow.template == PrismaTemplate.PRISMA_2020_NEW_DATABASES_REGISTERS:
        return Prisma2020NewTemplate().build(flow)

    raise TemplateNotSupportedError(
        f"Template is not implemented in v0.1: {flow.template.value}"
    )
