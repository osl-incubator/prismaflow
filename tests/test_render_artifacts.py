from pathlib import Path

from prismaflow import PrismaFlow

ARTIFACTS_DIR = Path("tmp/test-outputs")


def test_render_outputs_are_saved_for_manual_review() -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    flow = PrismaFlow.from_json("examples/basic_new_review.json")

    svg_path = ARTIFACTS_DIR / "basic_new_review.svg"
    html_path = ARTIFACTS_DIR / "basic_new_review.html"
    mermaid_path = ARTIFACTS_DIR / "basic_new_review.mmd"
    json_path = ARTIFACTS_DIR / "basic_new_review.json"
    png_path = ARTIFACTS_DIR / "basic_new_review.png"

    svg = flow.to_svg(svg_path)
    html = flow.to_html(html_path)
    mermaid = flow.to_mermaid(mermaid_path)
    json_output = flow.to_json(json_path)
    png = flow.to_png(png_path)

    assert svg_path.read_text(encoding="utf-8") == svg
    assert html_path.read_text(encoding="utf-8") == html
    assert mermaid_path.read_text(encoding="utf-8") == mermaid
    assert json_path.read_text(encoding="utf-8") == json_output + "\n"
    assert png_path.read_bytes() == png
