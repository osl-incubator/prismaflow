"""
title: Command-line interface for prisma-flow.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from pydantic import ValidationError as PydanticValidationError

from prismaflow.exceptions import OptionalDependencyError, PrismaFlowError
from prismaflow.models import PrismaFlow

RenderFormat = str


def main(argv: Sequence[str] | None = None) -> int:
    """
    title: Run the prisma-flow command-line interface.
    parameters:
      argv:
        type: Sequence[str] | None
        description: Value for argv.
    returns:
      type: int
      description: Return value.
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            return _validate_command(args)
        if args.command == "render":
            return _render_command(args)
    except PydanticValidationError as exc:
        print("Input model validation failed:", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 2
    except OptionalDependencyError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except PrismaFlowError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    parser.print_help(sys.stderr)
    return 2


def build_parser() -> argparse.ArgumentParser:
    """
    title: Build the CLI argument parser.
    returns:
      type: argparse.ArgumentParser
      description: Return value.
    """
    parser = argparse.ArgumentParser(
        prog="prisma-flow",
        description="Generate PRISMA-style flow diagrams without system dependencies.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="validate a PRISMA flow file")
    validate.add_argument("input", help="input JSON/YAML file")
    validate.add_argument(
        "--strict-included",
        action="store_true",
        help="treat included-study reconciliation warnings as errors",
    )

    render = subparsers.add_parser("render", help="render a PRISMA flow file")
    render.add_argument("input", help="input JSON/YAML file")
    render.add_argument(
        "-f",
        "--format",
        choices=["svg", "html", "mermaid", "png", "json", "yaml"],
        help="output format; inferred from --output when omitted",
    )
    render.add_argument("-o", "--output", help="output path")
    render.add_argument(
        "--allow-invalid",
        action="store_true",
        help="render even when PRISMA count validation has errors",
    )
    return parser


def _validate_command(args: argparse.Namespace) -> int:
    """
    title: _validate_command.
    parameters:
      args:
        type: argparse.Namespace
        description: Value for args.
    returns:
      type: int
      description: Return value.
    """
    flow = _load_flow(args.input)
    report = flow.validate(strict_included=args.strict_included)
    print(report.format_text())
    return 0 if report.ok else 1


def _render_command(args: argparse.Namespace) -> int:
    """
    title: _render_command.
    parameters:
      args:
        type: argparse.Namespace
        description: Value for args.
    returns:
      type: int
      description: Return value.
    """
    flow = _load_flow(args.input)
    report = flow.validate()
    if report.has_errors and not args.allow_invalid:
        print(report.format_text(), file=sys.stderr)
        return 1
    if report.has_warnings:
        print(report.format_text(), file=sys.stderr)

    output_format = args.format or _infer_format(args.output)
    rendered = _render(flow, output_format, args.output)
    if args.output is None and isinstance(rendered, str):
        print(rendered, end="")
    return 0


def _load_flow(path: str | Path) -> PrismaFlow:
    """
    title: _load_flow.
    parameters:
      path:
        type: str | Path
        description: Value for path.
    returns:
      type: PrismaFlow
      description: Return value.
    """
    suffix = Path(path).suffix.lower()
    if suffix in {".yaml", ".yml"}:
        return PrismaFlow.from_yaml(path)
    return PrismaFlow.from_json(path)


def _infer_format(output: str | None) -> RenderFormat:
    """
    title: _infer_format.
    parameters:
      output:
        type: str | None
        description: Value for output.
    returns:
      type: RenderFormat
      description: Return value.
    """
    if not output:
        return "svg"
    suffix = Path(output).suffix.lower().lstrip(".")
    if suffix == "mmd":
        return "mermaid"
    if suffix in {"svg", "html", "png", "json", "yaml", "yml"}:
        return "yaml" if suffix == "yml" else suffix
    return "svg"


def _render(
    flow: PrismaFlow,
    output_format: RenderFormat,
    output: str | None,
) -> str | bytes:
    """
    title: _render.
    parameters:
      flow:
        type: PrismaFlow
        description: Value for flow.
      output_format:
        type: RenderFormat
        description: Value for output_format.
      output:
        type: str | None
        description: Value for output.
    returns:
      type: str | bytes
      description: Return value.
    """
    if output_format == "svg":
        return flow.to_svg(output)
    if output_format == "html":
        return flow.to_html(output)
    if output_format == "mermaid":
        return flow.to_mermaid(output)
    if output_format == "png":
        return flow.to_png(output)
    if output_format == "json":
        return flow.to_json(output)
    if output_format == "yaml":
        return flow.to_yaml(output)
    raise PrismaFlowError(f"Unsupported output format: {output_format}")


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
