"""
title: Standalone HTML renderer.
"""

from __future__ import annotations

from html import escape

from prismaflow.layout.engine import DiagramLayout
from prismaflow.renderers.svg import SVGRenderer


class HTMLRenderer:
    """
    title: Render diagram layouts to standalone HTML documents.
    """

    def render(self, layout: DiagramLayout) -> str:
        """
        title: Render a layout as HTML with embedded SVG.
        parameters:
          layout:
            type: DiagramLayout
            description: Value for layout.
        returns:
          type: str
          description: Return value.
        """
        title = layout.title or "PRISMA Flow Diagram"
        svg = (
            SVGRenderer()
            .render(layout)
            .removeprefix('<?xml version="1.0" encoding="UTF-8"?>\n')
        )
        return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape(title)}</title>
  <style>
    body {{
      margin: 2rem;
      font-family: Arial, Helvetica, sans-serif;
      background: #f3f4f6;
    }}
    main {{ max-width: {layout.width:g}px; margin: 0 auto; }}
    svg {{
      max-width: 100%;
      height: auto;
      box-shadow: 0 1px 8px rgba(0, 0, 0, 0.08);
    }}
  </style>
</head>
<body>
  <main>
{svg}
  </main>
</body>
</html>
"""
