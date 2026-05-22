"""
title: PNG renderer.
"""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
from typing import Any, cast

from prismaflow.exceptions import OptionalDependencyError
from prismaflow.layout.engine import DiagramLayout
from prismaflow.renderers.svg import SVGRenderer

Transform = tuple[float, float, float, float, float, float]
PREFERRED_FONT_FAMILIES = (
    "DejaVu Sans",
    "Liberation Sans",
    "Arial",
    "Helvetica",
    "FreeSans",
    "Noto Sans",
    "Roboto",
    "Arimo",
)
FALLBACK_FONT_FILES = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    "/usr/local/share/fonts/DejaVuSans.ttf",
)


class PNGRenderer:
    """
    title: Render diagram layouts to PNG through the resvg backend.
    attributes:
      scale:
        description: Scale factor applied while rasterizing the SVG.
      load_system_fonts:
        description: Whether resvg should load locally available fonts.
    """

    def __init__(self, *, scale: float = 1.0, load_system_fonts: bool = True) -> None:
        """
        title: Configure PNG rasterization.
        parameters:
          scale:
            type: float
            description: Scale factor applied while rasterizing the SVG.
          load_system_fonts:
            type: bool
            description: Whether resvg should load locally available fonts.
        """
        if scale <= 0:
            raise ValueError("PNG scale must be greater than zero")
        self.scale = scale
        self.load_system_fonts = load_system_fonts

    def render(self, layout: DiagramLayout, *, path: str | Path | None = None) -> bytes:
        """
        title: Render a layout as PNG bytes and optionally write it to a file.
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
        resvg = _load_resvg()
        options = resvg.usvg.Options.default()
        if self.load_system_fonts:
            options.load_system_fonts()
            _load_fallback_fonts(options)
        font_family = _preferred_font_family(options.list_fonts())
        if font_family is None:
            raise OptionalDependencyError(
                "PNG export requires at least one TrueType/OpenType font so text "
                "can be rendered.\n\n"
                "In Google Colab, install fonts with:\n\n"
                "  !apt-get update && !apt-get install -y fonts-dejavu-core"
            )

        svg = SVGRenderer(font_family=font_family).render(layout)
        tree = resvg.usvg.Tree.from_str(svg, options)
        png = cast(
            bytes,
            resvg.render(
                tree,
                self._transform(),
                bg_color=(255, 255, 255, 255),
            ),
        )
        if path is not None:
            Path(path).write_bytes(png)
        return png

    def _transform(self) -> Transform:
        """
        title: Return the affine transform used by resvg.
        returns:
          type: Transform
          description: Return value.
        """
        return (self.scale, 0.0, 0.0, 0.0, self.scale, 0.0)


def _load_resvg() -> Any:
    """
    title: Import the required resvg backend.
    returns:
      type: Any
      description: Imported resvg module.
    """
    try:
        return import_module("resvg")
    except ImportError as exc:
        raise OptionalDependencyError(
            "PNG export requires the runtime dependency resvg.\n\n"
            "Reinstall prisma-flow with:\n\n"
            "  pip install --force-reinstall prisma-flow"
        ) from exc


def _load_fallback_fonts(options: Any) -> None:
    """
    title: Load common Linux notebook fonts when font discovery is empty.
    parameters:
      options:
        type: Any
        description: resvg usvg options object.
    """
    if options.list_fonts():
        return
    for font_file in FALLBACK_FONT_FILES:
        path = Path(font_file)
        if path.exists():
            options.load_font_file(str(path))


def _preferred_font_family(fonts: list[str]) -> str | None:
    """
    title: Pick a font family that is available to resvg.
    parameters:
      fonts:
        type: list[str]
        description: Font families loaded in resvg options.
    returns:
      type: str | None
      description: Preferred family name, or None when no fonts are loaded.
    """
    available = set(fonts)
    for family in PREFERRED_FONT_FAMILIES:
        if family in available:
            return family
    return fonts[0] if fonts else None
