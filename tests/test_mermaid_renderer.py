from prismaflow import PrismaFlow


def test_mermaid_renderer_outputs_text_only() -> None:
    flow = PrismaFlow.from_json("examples/basic_new_review.json")
    mermaid = flow.to_mermaid()
    assert mermaid.startswith("flowchart TD")
    assert "Records identified from*:<br/>" in mermaid
    assert "Identification of studies via databases and registers" not in mermaid
    assert "A --> B" in mermaid
