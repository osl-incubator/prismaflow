"""
title: Mermaid text renderer.
"""

from __future__ import annotations

from prismaflow.layout.engine import DiagramLayout


class MermaidRenderer:
    """
    title: Render diagram layouts as Mermaid flowchart text only.
    """

    def render(self, layout: DiagramLayout) -> str:
        """
        title: Render Mermaid flowchart text without invoking Mermaid CLI.
        parameters:
          layout:
            type: DiagramLayout
            description: Value for layout.
        returns:
          type: str
          description: Return value.
        """
        aliases = self._aliases(layout)
        lines = ["flowchart TD"]
        for node in layout.nodes:
            label = self._label(node.text)
            lines.append(f'    {aliases[node.id]}["{label}"]')
        lines.append("")
        for edge in layout.edges:
            lines.append(f"    {aliases[edge.source_id]} --> {aliases[edge.target_id]}")
        return "\n".join(lines) + "\n"

    @staticmethod
    def _aliases(layout: DiagramLayout) -> dict[str, str]:
        """
        title: _aliases.
        parameters:
          layout:
            type: DiagramLayout
            description: Value for layout.
        returns:
          type: dict[str, str]
          description: Return value.
        """
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        aliases: dict[str, str] = {}
        for index, node in enumerate(layout.nodes):
            if index < len(alphabet):
                aliases[node.id] = alphabet[index]
            else:
                aliases[node.id] = f"N{index + 1}"
        return aliases

    @staticmethod
    def _label(text: str) -> str:
        """
        title: _label.
        parameters:
          text:
            type: str
            description: Value for text.
        returns:
          type: str
          description: Return value.
        """
        return text.replace('"', "'").replace("\n", "<br/>")
