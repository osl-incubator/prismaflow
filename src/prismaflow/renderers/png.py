"""
title: Optional PNG renderer placeholder.
"""

from __future__ import annotations

from pathlib import Path

from prismaflow.exceptions import OptionalDependencyError
from prismaflow.layout.engine import DiagramLayout


class PNGRenderer:
    """
    title: PNG export placeholder for optional future backends.
    """

    def render(self, layout: DiagramLayout, *, path: str | Path | None = None) -> bytes:
        """
        title: Raise an optional dependency error for v0.1 PNG export.
        parameters:
          layout:
            type: DiagramLayout
            description: Value for layout.
          path:
            type: str | Path | None
            description: Value for path.
        returns:
          type: bytes
          description: Return value.
        """
        raise OptionalDependencyError(
            "PNG export requires the optional dependency.\n\n"
            "Install it with:\n\n"
            '  pip install "prisma-flow[png]"\n\n'
            "or:\n\n"
            '  uv add "prisma-flow[png]"'
        )
