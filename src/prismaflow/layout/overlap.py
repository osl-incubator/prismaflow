"""
title: Overlap checks for diagram layouts.
"""

from __future__ import annotations

from prismaflow.layout.engine import DiagramLayout, DiagramNode


def find_overlaps(
    layout: DiagramLayout,
    *,
    padding: float = 0,
) -> list[tuple[DiagramNode, DiagramNode]]:
    """
    title: Return node pairs with overlapping rectangles.
    parameters:
      layout:
        type: DiagramLayout
        description: Value for layout.
      padding:
        type: float
        description: Value for padding.
    returns:
      type: list[tuple[DiagramNode, DiagramNode]]
      description: Return value.
    """
    overlaps: list[tuple[DiagramNode, DiagramNode]] = []
    nodes = layout.nodes
    for index, node in enumerate(nodes):
        for other in nodes[index + 1 :]:
            if node.rect.overlaps(other.rect, padding=padding):
                overlaps.append((node, other))
    return overlaps


def assert_no_overlaps(layout: DiagramLayout, *, padding: float = 0) -> None:
    """
    title: Raise AssertionError if any layout nodes overlap.
    parameters:
      layout:
        type: DiagramLayout
        description: Value for layout.
      padding:
        type: float
        description: Value for padding.
    """
    overlaps = find_overlaps(layout, padding=padding)
    if overlaps:
        pairs = ", ".join(f"{left.id}/{right.id}" for left, right in overlaps)
        raise AssertionError(f"Diagram nodes overlap: {pairs}")
