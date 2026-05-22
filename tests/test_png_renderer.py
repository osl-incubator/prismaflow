import struct
import zlib

import pytest

import prismaflow.renderers.png as png_module
from prismaflow import PrismaFlow
from prismaflow.exceptions import OptionalDependencyError
from prismaflow.renderers.png import PNGRenderer, _preferred_font_family


def test_png_renderer_outputs_png_bytes() -> None:
    flow = PrismaFlow.from_json("examples/basic_new_review.json")

    png = flow.to_png()

    assert png.startswith(b"\x89PNG\r\n\x1a\n")


def test_png_renderer_outputs_visible_diagram_pixels() -> None:
    flow = PrismaFlow.from_json("examples/basic_new_review.json")

    png = flow.to_png()
    pixels = _rgba_pixels(png)

    assert any(pixel[:3] == (255, 255, 255) and pixel[3] == 255 for pixel in pixels)
    assert sum(1 for pixel in pixels if pixel[:3] != (255, 255, 255)) > 1000


def test_png_renderer_writes_png_file(tmp_path) -> None:  # type: ignore[no-untyped-def]
    output = tmp_path / "prisma.png"
    flow = PrismaFlow.from_json("examples/basic_new_review.json")

    png = flow.to_png(output)

    assert output.read_bytes() == png


def test_png_renderer_reports_missing_optional_dependency(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    def missing_import(name: str) -> object:
        raise ImportError(name)

    monkeypatch.setattr(png_module, "import_module", missing_import)
    flow = PrismaFlow.from_json("examples/basic_new_review.json")

    with pytest.raises(OptionalDependencyError, match="prisma-flow\\[png\\]"):
        PNGRenderer().render(flow.to_layout())


def test_png_renderer_rejects_non_positive_scale() -> None:
    with pytest.raises(ValueError, match="greater than zero"):
        PNGRenderer(scale=0)


def test_png_renderer_prefers_available_notebook_fonts() -> None:
    assert _preferred_font_family(["FreeSans", "Other Sans"]) == "FreeSans"
    assert _preferred_font_family(["Other Sans"]) == "Other Sans"
    assert _preferred_font_family([]) is None


def _rgba_pixels(png: bytes) -> list[tuple[int, int, int, int]]:
    assert png.startswith(b"\x89PNG\r\n\x1a\n")
    offset = 8
    width = 0
    height = 0
    compressed = bytearray()
    while offset < len(png):
        length = struct.unpack(">I", png[offset : offset + 4])[0]
        chunk_type = png[offset + 4 : offset + 8]
        chunk_data = png[offset + 8 : offset + 8 + length]
        offset += 12 + length
        if chunk_type == b"IHDR":
            width, height, bit_depth, color_type = struct.unpack(
                ">IIBB",
                chunk_data[:10],
            )
            assert bit_depth == 8
            assert color_type == 6
        elif chunk_type == b"IDAT":
            compressed.extend(chunk_data)
        elif chunk_type == b"IEND":
            break

    raw = zlib.decompress(bytes(compressed))
    stride = width * 4
    previous = [0] * stride
    rows: list[bytes] = []
    position = 0
    for _ in range(height):
        filter_type = raw[position]
        position += 1
        current = list(raw[position : position + stride])
        position += stride
        _unfilter_row(current, previous, filter_type)
        rows.append(bytes(current))
        previous = current

    return [
        (row[index], row[index + 1], row[index + 2], row[index + 3])
        for row in rows
        for index in range(0, stride, 4)
    ]


def _unfilter_row(current: list[int], previous: list[int], filter_type: int) -> None:
    bytes_per_pixel = 4
    for index, value in enumerate(current):
        left = current[index - bytes_per_pixel] if index >= bytes_per_pixel else 0
        up = previous[index]
        upper_left = (
            previous[index - bytes_per_pixel] if index >= bytes_per_pixel else 0
        )
        if filter_type == 1:
            current[index] = (value + left) & 0xFF
        elif filter_type == 2:
            current[index] = (value + up) & 0xFF
        elif filter_type == 3:
            current[index] = (value + ((left + up) // 2)) & 0xFF
        elif filter_type == 4:
            current[index] = (value + _paeth(left, up, upper_left)) & 0xFF
        else:
            assert filter_type == 0


def _paeth(left: int, up: int, upper_left: int) -> int:
    estimate = left + up - upper_left
    left_distance = abs(estimate - left)
    up_distance = abs(estimate - up)
    upper_left_distance = abs(estimate - upper_left)
    if left_distance <= up_distance and left_distance <= upper_left_distance:
        return left
    if up_distance <= upper_left_distance:
        return up
    return upper_left
