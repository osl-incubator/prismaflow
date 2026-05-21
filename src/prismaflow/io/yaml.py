"""
title: Optional YAML input/output helpers.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol

from prismaflow.exceptions import OptionalDependencyError
from prismaflow.models import PrismaFlow


class _YamlModule(Protocol):
    """
    title: Minimal PyYAML module protocol used by prisma-flow.
    """

    def safe_load(self, stream: str) -> Any:
        """
        title: Load YAML text.
        parameters:
          stream:
            type: str
            description: Value for stream.
        returns:
          type: Any
          description: Return value.
        """
        ...

    def safe_dump(self, data: Any, *, sort_keys: bool = ...) -> str:
        """
        title: Dump data as YAML text.
        parameters:
          data:
            type: Any
            description: Value for data.
          sort_keys:
            type: bool
            description: Value for sort_keys.
        returns:
          type: str
          description: Return value.
        """
        ...


def _yaml_module() -> _YamlModule:
    """
    title: _yaml_module.
    returns:
      type: _YamlModule
      description: Return value.
    """
    try:
        import yaml
    except ModuleNotFoundError as exc:
        raise OptionalDependencyError(
            "YAML support requires the optional dependency.\n\n"
            "Install it with:\n\n"
            '  pip install "prisma-flow[yaml]"\n\n'
            "or:\n\n"
            '  uv add "prisma-flow[yaml]"'
        ) from exc
    module: _YamlModule = yaml
    return module


def load_yaml(source: str | Path) -> PrismaFlow:
    """
    title: Load a PrismaFlow model from a YAML file path or YAML string.
    parameters:
      source:
        type: str | Path
        description: Value for source.
    returns:
      type: PrismaFlow
      description: Return value.
    """
    yaml = _yaml_module()
    if isinstance(source, Path) or _looks_like_path(source):
        path = Path(source)
        if path.exists():
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            return PrismaFlow.model_validate(data)
    data = yaml.safe_load(str(source))
    return PrismaFlow.model_validate(data)


def dump_yaml(flow: PrismaFlow, path: str | Path | None = None) -> str:
    """
    title: Serialize a flow to YAML and optionally write it.
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
    yaml = _yaml_module()
    data = flow.model_dump(mode="json")
    output = yaml.safe_dump(data, sort_keys=False)
    if path is not None:
        Path(path).write_text(output, encoding="utf-8")
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
    return text.endswith((".yaml", ".yml")) or "/" in text or "\\" in text
