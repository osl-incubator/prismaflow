"""
title: Template builder interfaces.
"""

from __future__ import annotations

from typing import Protocol

from prismaflow.layout.engine import DiagramLayout


class TemplateBuilder(Protocol):
    """
    title: Protocol implemented by PRISMA template builders.
    """

    def build(self, flow: object) -> DiagramLayout:
        """
        title: Build a diagram layout for a flow.
        parameters:
          flow:
            type: object
            description: Value for flow.
        returns:
          type: DiagramLayout
          description: Return value.
        """
        ...
