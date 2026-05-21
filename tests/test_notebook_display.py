from prismaflow import PrismaFlow


def test_repr_svg_returns_inline_svg() -> None:
    flow = PrismaFlow.from_json("examples/basic_new_review.json")

    svg = flow._repr_svg_()

    assert svg.startswith('<?xml version="1.0"')
    assert "<svg" in svg
    assert "PRISMA-style flow diagram" in svg


def test_repr_mimebundle_returns_svg_bundle() -> None:
    flow = PrismaFlow.from_json("examples/basic_new_review.json")

    data, metadata = flow._repr_mimebundle_()

    assert metadata == {}
    assert set(data) == {"image/svg+xml"}
    assert data["image/svg+xml"].startswith('<?xml version="1.0"')


def test_repr_mimebundle_respects_frontend_filters() -> None:
    flow = PrismaFlow.from_json("examples/basic_new_review.json")

    assert flow._repr_mimebundle_(include={"text/plain"}) == ({}, {})
    assert flow._repr_mimebundle_(exclude={"image/svg+xml"}) == ({}, {})
