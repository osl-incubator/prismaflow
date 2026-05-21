"""
title: JSON input/output helpers.
"""

from __future__ import annotations

from pathlib import Path

from prismaflow.models import PrismaFlow


def load_json(source: str | Path) -> PrismaFlow:
    """
    title: Load a PrismaFlow model from a JSON file path or JSON string.
    parameters:
      source:
        type: str | Path
        description: Value for source.
    returns:
      type: PrismaFlow
      description: Return value.
    """
    if isinstance(source, Path) or _looks_like_path(source):
        path = Path(source)
        if path.exists():
            return PrismaFlow.model_validate_json(path.read_text(encoding="utf-8"))
    return PrismaFlow.model_validate_json(str(source))


def dump_json(flow: PrismaFlow, path: str | Path | None = None) -> str:
    """
    title: Serialize a flow to JSON and optionally write it.
    parameters:
      flow:
        type: PrismaFlow
        description: Value for flow.
      path:
        type: str | Path | None
        description: Value for path.
    returns:
      type: str
      description: Return value.
    """
    output = flow.model_dump_json(indent=2)
    if path is not None:
        Path(path).write_text(output + "\n", encoding="utf-8")
    return output


def _looks_like_path(source: str | Path) -> bool:
    """
    title: _looks_like_path.
    parameters:
      source:
        type: str | Path
        description: Value for source.
    returns:
      type: bool
      description: Return value.
    """
    if isinstance(source, Path):
        return True
    text = str(source)
    return text.endswith(".json") or "/" in text or "\\" in text
