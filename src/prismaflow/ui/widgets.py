"""
title: Jupyter widget helpers for interactive PRISMA flow creation.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from importlib import import_module
from pathlib import Path
from typing import Any, Literal, cast

from prismaflow.enums import PrismaTemplate
from prismaflow.exceptions import OptionalDependencyError
from prismaflow.models import FlowMetadata, PrismaFlow, new_review

FieldKind = Literal[
    "dict",
    "int",
    "metadata",
    "optional_int",
    "optional_str",
    "template",
]
DisplayFunction = Callable[[Any], None]
WidgetMap = dict[str, Any]
LatestFlow = dict[str, PrismaFlow | None]


@dataclass(frozen=True)
class WidgetField:
    """
    title: Field metadata for a `new_review` widget input.
    attributes:
      name:
        type: str
        description: Keyword argument name accepted by `new_review`.
      label:
        type: str
        description: Human-readable widget label.
      kind:
        type: FieldKind
        description: Widget/parser kind.
      group:
        type: str
        description: UI section label.
      default:
        type: object
        description: Default value used when no initial keyword is provided.
    """

    name: str
    label: str
    kind: FieldKind
    group: str
    default: object = None


GENERAL_FIELDS = (
    WidgetField("title", "Title", "optional_str", "General"),
    WidgetField("template", "Template", "template", "General"),
    WidgetField("metadata", "Metadata JSON", "metadata", "General"),
)
IDENTIFICATION_FIELDS = (
    WidgetField(
        "records_identified_databases",
        "Records identified databases",
        "int",
        "Identification",
        0,
    ),
    WidgetField(
        "records_identified_registers",
        "Records identified registers",
        "int",
        "Identification",
        0,
    ),
    WidgetField(
        "database_specific_results",
        "Database-specific results",
        "optional_str",
        "Identification",
    ),
    WidgetField(
        "register_specific_results",
        "Register-specific results",
        "optional_str",
        "Identification",
    ),
    WidgetField(
        "previous_studies", "Previous studies", "optional_int", "Identification"
    ),
    WidgetField(
        "previous_reports", "Previous reports", "optional_int", "Identification"
    ),
)
SCREENING_FIELDS = (
    WidgetField(
        "records_removed_duplicates",
        "Records removed duplicates",
        "int",
        "Screening",
        0,
    ),
    WidgetField(
        "records_removed_automation",
        "Records removed automation",
        "int",
        "Screening",
        0,
    ),
    WidgetField(
        "records_removed_other",
        "Records removed other",
        "int",
        "Screening",
        0,
    ),
    WidgetField("records_screened", "Records screened", "int", "Screening", 0),
    WidgetField("records_excluded", "Records excluded", "int", "Screening", 0),
)
ELIGIBILITY_FIELDS = (
    WidgetField("reports_sought", "Reports sought", "int", "Eligibility", 0),
    WidgetField(
        "reports_not_retrieved",
        "Reports not retrieved",
        "int",
        "Eligibility",
        0,
    ),
    WidgetField("reports_assessed", "Reports assessed", "int", "Eligibility", 0),
    WidgetField(
        "reports_excluded",
        "Reports excluded JSON",
        "dict",
        "Eligibility",
    ),
)
INCLUDED_FIELDS = (
    WidgetField("studies_included", "Studies included", "int", "Included", 0),
    WidgetField("reports_included", "Reports included", "optional_int", "Included"),
    WidgetField("total_studies", "Total studies", "optional_int", "Included"),
    WidgetField("total_reports", "Total reports", "optional_int", "Included"),
)
OTHER_METHOD_FIELDS = (
    WidgetField("website_results", "Website results", "int", "Other methods", 0),
    WidgetField(
        "organisation_results",
        "Organisation results",
        "int",
        "Other methods",
        0,
    ),
    WidgetField("citations_results", "Citation results", "int", "Other methods", 0),
    WidgetField(
        "other_sought_reports",
        "Other sought reports",
        "int",
        "Other methods",
        0,
    ),
    WidgetField(
        "other_notretrieved_reports",
        "Other not retrieved reports",
        "int",
        "Other methods",
        0,
    ),
    WidgetField("other_assessed", "Other assessed", "int", "Other methods", 0),
    WidgetField("other_excluded", "Other excluded JSON", "dict", "Other methods"),
)
NEW_REVIEW_FIELDS = (
    *GENERAL_FIELDS,
    *IDENTIFICATION_FIELDS,
    *SCREENING_FIELDS,
    *ELIGIBILITY_FIELDS,
    *INCLUDED_FIELDS,
    *OTHER_METHOD_FIELDS,
)
NEW_REVIEW_FIELD_NAMES = {field.name for field in NEW_REVIEW_FIELDS}
GROUP_NAMES = (
    "General",
    "Identification",
    "Screening",
    "Eligibility",
    "Included",
    "Other methods",
)


def load(
    *,
    display_widget: bool = True,
    svg_path: str | Path = "prisma-flow.svg",
    png_path: str | Path = "prisma-flow.png",
    **kwargs: object,
) -> Any:
    """
    title: Create and optionally display a Jupyter widget for `new_review`.
    parameters:
      display_widget:
        type: bool
        description: Whether to display the widget in the active notebook cell.
      svg_path:
        type: str | Path
        description: Initial path used by the Save SVG button.
      png_path:
        type: str | Path
        description: Initial path used by the Save PNG button.
      kwargs:
        type: object
        description: Initial values for parameters accepted by `new_review`.
        variadic: keyword
    returns:
      type: Any
      description: The root ipywidgets container.
    """
    _validate_initial_kwargs(kwargs)
    widgets = _load_ipywidgets()
    display, svg_display = _load_ipython_display()

    style = {"description_width": "220px"}
    layout = widgets.Layout(width="100%")
    inputs = _build_input_widgets(
        widgets,
        kwargs,
        style=style,
        layout=layout,
    )
    svg_path_widget = widgets.Text(
        value=str(svg_path),
        description="SVG path",
        style=style,
        layout=layout,
    )
    png_path_widget = widgets.Text(
        value=str(png_path),
        description="PNG path",
        style=style,
        layout=layout,
    )
    output = widgets.Output()
    latest: LatestFlow = {"flow": None}

    generate_button = widgets.Button(
        description="Generate image",
        button_style="primary",
        icon="picture-o",
    )
    save_svg_button = widgets.Button(
        description="Save SVG",
        icon="save",
    )
    save_png_button = widgets.Button(
        description="Save PNG",
        icon="save",
    )

    def on_generate(_button: object) -> None:
        """
        title: Generate and display the current PRISMA flow SVG.
        parameters:
          _button:
            type: object
            description: Button click event object.
        """
        _generate_into_output(
            inputs,
            output,
            display,
            svg_display,
            latest,
        )

    def on_save_svg(_button: object) -> None:
        """
        title: Save the current PRISMA flow as SVG.
        parameters:
          _button:
            type: object
            description: Button click event object.
        """
        _save_current_flow(
            inputs,
            output,
            display,
            svg_display,
            latest,
            path=svg_path_widget.value,
            format_name="SVG",
        )

    def on_save_png(_button: object) -> None:
        """
        title: Save the current PRISMA flow as PNG.
        parameters:
          _button:
            type: object
            description: Button click event object.
        """
        _save_current_flow(
            inputs,
            output,
            display,
            svg_display,
            latest,
            path=png_path_widget.value,
            format_name="PNG",
        )

    generate_button.on_click(on_generate)
    save_svg_button.on_click(on_save_svg)
    save_png_button.on_click(on_save_png)

    controls = widgets.HBox([generate_button, save_svg_button, save_png_button])
    sections = _build_sections(widgets, inputs)
    output_section = widgets.Accordion(
        children=[widgets.VBox([svg_path_widget, png_path_widget])]
    )
    output_section.set_title(0, "Output paths")
    container = widgets.VBox(
        [
            widgets.HTML(
                "<h3>prisma-flow widget</h3>"
                "<p>Enter PRISMA new-review counts, generate an inline SVG "
                "preview, or save SVG/PNG files.</p>"
            ),
            *sections,
            output_section,
            controls,
            output,
        ]
    )

    container.prisma_flow_fields = inputs
    container.prisma_flow_output = output
    container.prisma_flow_build_kwargs = lambda: collect_new_review_kwargs(inputs)
    container.prisma_flow_build_flow = lambda: build_flow_from_widgets(inputs)
    container.prisma_flow_latest = latest
    container.prisma_flow_buttons = {
        "generate": generate_button,
        "save_svg": save_svg_button,
        "save_png": save_png_button,
    }
    container.prisma_flow_paths = {"svg": svg_path_widget, "png": png_path_widget}

    if display_widget:
        display(container)
    return container


def collect_new_review_kwargs(inputs: Mapping[str, Any]) -> dict[str, object]:
    """
    title: Collect parsed `new_review` keyword arguments from widget inputs.
    parameters:
      inputs:
        type: Mapping[str, Any]
        description: Mapping of parameter names to input widgets.
    returns:
      type: dict[str, object]
      description: Parsed keyword arguments for `new_review`.
    """
    values: dict[str, object] = {}
    for field in NEW_REVIEW_FIELDS:
        widget = inputs[field.name]
        values[field.name] = _parse_widget_value(field, widget.value)
    return values


def build_flow_from_widgets(inputs: Mapping[str, Any]) -> PrismaFlow:
    """
    title: Build a `PrismaFlow` from widget inputs.
    parameters:
      inputs:
        type: Mapping[str, Any]
        description: Mapping of parameter names to input widgets.
    returns:
      type: PrismaFlow
      description: Generated flow model.
    """
    kwargs = collect_new_review_kwargs(inputs)
    return new_review(**cast(Any, kwargs))


def _load_ipywidgets() -> Any:
    """
    title: Import ipywidgets or raise an optional dependency error.
    returns:
      type: Any
      description: Imported ipywidgets module.
    """
    try:
        return import_module("ipywidgets")
    except ImportError as exc:
        raise OptionalDependencyError(
            "Jupyter widgets require the optional ui dependencies.\n\n"
            "Install them with:\n\n"
            '  pip install "prisma-flow[ui]"'
        ) from exc


def _load_ipython_display() -> tuple[DisplayFunction, Any]:
    """
    title: Import IPython display helpers for notebook output.
    returns:
      type: tuple[DisplayFunction, Any]
      description: Display function and SVG display class.
    """
    try:
        display_module = cast(Any, import_module("IPython.display"))
    except ImportError as exc:
        raise OptionalDependencyError(
            "Jupyter widget display requires IPython display support.\n\n"
            "Install the optional UI extra with:\n\n"
            '  pip install "prisma-flow[ui]"'
        ) from exc
    return (
        cast(DisplayFunction, display_module.display),
        display_module.SVG,
    )


def _validate_initial_kwargs(kwargs: Mapping[str, object]) -> None:
    """
    title: Reject keyword arguments not accepted by `new_review`.
    parameters:
      kwargs:
        type: Mapping[str, object]
        description: Initial keyword arguments passed to `load`.
    """
    unknown = sorted(set(kwargs) - NEW_REVIEW_FIELD_NAMES)
    if unknown:
        names = ", ".join(unknown)
        raise TypeError(f"load() got unexpected keyword argument(s): {names}")


def _build_input_widgets(
    widgets: Any,
    initial_values: Mapping[str, object],
    *,
    style: Mapping[str, str],
    layout: Any,
) -> WidgetMap:
    """
    title: Build all input widgets for `new_review` parameters.
    parameters:
      widgets:
        type: Any
        description: Imported ipywidgets module.
      initial_values:
        type: Mapping[str, object]
        description: Initial widget values keyed by parameter name.
      style:
        type: Mapping[str, str]
        description: Shared widget style mapping.
      layout:
        type: Any
        description: Shared widget layout object.
    returns:
      type: WidgetMap
      description: Mapping of field names to widgets.
    """
    inputs: WidgetMap = {}
    for field in NEW_REVIEW_FIELDS:
        initial = initial_values.get(field.name, field.default)
        inputs[field.name] = _create_input_widget(
            widgets,
            field,
            initial,
            style=style,
            layout=layout,
        )
    return inputs


def _create_input_widget(
    widgets: Any,
    field: WidgetField,
    value: object,
    *,
    style: Mapping[str, str],
    layout: Any,
) -> Any:
    """
    title: Create one input widget for a `new_review` field.
    parameters:
      widgets:
        type: Any
        description: Imported ipywidgets module.
      field:
        type: WidgetField
        description: Field metadata.
      value:
        type: object
        description: Initial value.
      style:
        type: Mapping[str, str]
        description: Widget style mapping.
      layout:
        type: Any
        description: Widget layout object.
    returns:
      type: Any
      description: Created ipywidgets widget.
    """
    if field.kind == "int":
        return widgets.IntText(
            value=_coerce_initial_int(field.name, value),
            description=field.label,
            style=style,
            layout=layout,
        )
    if field.kind == "optional_int":
        return widgets.Text(
            value="" if value is None else str(value),
            description=field.label,
            placeholder="empty = unset",
            style=style,
            layout=layout,
        )
    if field.kind == "optional_str":
        return widgets.Text(
            value="" if value is None else str(value),
            description=field.label,
            placeholder="empty = unset",
            style=style,
            layout=layout,
        )
    if field.kind == "dict":
        return widgets.Textarea(
            value=_json_text(value),
            description=field.label,
            placeholder='{"Reason": 1}',
            style=style,
            layout=layout,
        )
    if field.kind == "metadata":
        return widgets.Textarea(
            value=_metadata_json_text(value),
            description=field.label,
            placeholder='{"review_id": "review-1"}',
            style=style,
            layout=layout,
        )
    return widgets.Dropdown(
        value=_template_value(value),
        options=[(template.value, template.value) for template in PrismaTemplate],
        description=field.label,
        style=style,
        layout=layout,
    )


def _build_sections(widgets: Any, inputs: Mapping[str, Any]) -> list[Any]:
    """
    title: Group input widgets into accordion sections.
    parameters:
      widgets:
        type: Any
        description: Imported ipywidgets module.
      inputs:
        type: Mapping[str, Any]
        description: Mapping of parameter names to widgets.
    returns:
      type: list[Any]
      description: List containing one accordion widget.
    """
    children: list[Any] = []
    for group in GROUP_NAMES:
        group_widgets = [
            inputs[field.name] for field in NEW_REVIEW_FIELDS if field.group == group
        ]
        children.append(widgets.VBox(group_widgets))
    accordion = widgets.Accordion(children=children)
    for index, group in enumerate(GROUP_NAMES):
        accordion.set_title(index, group)
    return [accordion]


def _parse_widget_value(field: WidgetField, value: object) -> object:
    """
    title: Parse a raw widget value for a `new_review` field.
    parameters:
      field:
        type: WidgetField
        description: Field metadata.
      value:
        type: object
        description: Raw widget value.
    returns:
      type: object
      description: Parsed value for `new_review`.
    """
    if field.kind == "int":
        return _parse_required_int(field.name, value)
    if field.kind == "optional_int":
        return _parse_optional_int(field.name, value)
    if field.kind == "optional_str":
        text = str(value).strip()
        return None if text == "" else str(value)
    if field.kind == "dict":
        return _parse_dict(field.name, value)
    if field.kind == "metadata":
        return _parse_metadata(field.name, value)
    return PrismaTemplate(str(value))


def _parse_required_int(name: str, value: object) -> int:
    """
    title: Parse a required integer field.
    parameters:
      name:
        type: str
        description: Field name.
      value:
        type: object
        description: Raw field value.
    returns:
      type: int
      description: Parsed integer.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    return value


def _parse_optional_int(name: str, value: object) -> int | None:
    """
    title: Parse an optional integer text field.
    parameters:
      name:
        type: str
        description: Field name.
      value:
        type: object
        description: Raw field value.
    returns:
      type: int | None
      description: Parsed integer or None.
    """
    text = str(value).strip()
    if text == "":
        return None
    try:
        parsed = int(text)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer or empty") from exc
    return parsed


def _parse_dict(name: str, value: object) -> dict[str, int] | None:
    """
    title: Parse a JSON object field as an exclusion-count mapping.
    parameters:
      name:
        type: str
        description: Field name.
      value:
        type: object
        description: Raw text value.
    returns:
      type: dict[str, int] | None
      description: Parsed mapping or None.
    """
    text = str(value).strip()
    if text == "":
        return None
    payload = _parse_json_text(name, text)
    if payload is None:
        return None
    if not isinstance(payload, dict):
        raise ValueError(f"{name} must be a JSON object")
    parsed: dict[str, int] = {}
    for key, count in payload.items():
        if not isinstance(key, str) or not key.strip():
            raise ValueError(f"{name} keys must be non-empty strings")
        if isinstance(count, bool) or not isinstance(count, int):
            raise ValueError(f"{name} values must be integers")
        parsed[key] = count
    return parsed


def _parse_metadata(name: str, value: object) -> FlowMetadata | None:
    """
    title: Parse metadata JSON into a `FlowMetadata` model.
    parameters:
      name:
        type: str
        description: Field name.
      value:
        type: object
        description: Raw text value.
    returns:
      type: FlowMetadata | None
      description: Parsed metadata model or None.
    """
    text = str(value).strip()
    if text == "":
        return None
    payload = _parse_json_text(name, text)
    if payload is None:
        return None
    if not isinstance(payload, dict):
        raise ValueError(f"{name} must be a JSON object")
    return FlowMetadata.model_validate(payload)


def _parse_json_text(name: str, text: str) -> object:
    """
    title: Parse JSON text and wrap parser errors with field context.
    parameters:
      name:
        type: str
        description: Field name.
      text:
        type: str
        description: JSON text.
    returns:
      type: object
      description: Parsed JSON payload.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{name} must contain valid JSON: {exc.msg}") from exc


def _coerce_initial_int(name: str, value: object) -> int:
    """
    title: Coerce an initial value for an integer widget.
    parameters:
      name:
        type: str
        description: Field name.
      value:
        type: object
        description: Initial value.
    returns:
      type: int
      description: Integer widget value.
    """
    if value is None:
        return 0
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} initial value must be an integer")
    return value


def _json_text(value: object) -> str:
    """
    title: Serialize a JSON-compatible initial value for a textarea.
    parameters:
      value:
        type: object
        description: Initial value.
    returns:
      type: str
      description: Textarea text.
    """
    if value is None:
        return ""
    return json.dumps(value, indent=2, sort_keys=True)


def _metadata_json_text(value: object) -> str:
    """
    title: Serialize an initial metadata value for a textarea.
    parameters:
      value:
        type: object
        description: Initial value.
    returns:
      type: str
      description: Textarea text.
    """
    if value is None:
        return ""
    if isinstance(value, FlowMetadata):
        return json.dumps(value.model_dump(mode="json"), indent=2, sort_keys=True)
    return json.dumps(value, indent=2, sort_keys=True)


def _template_value(value: object) -> str:
    """
    title: Return the template dropdown value for an initial value.
    parameters:
      value:
        type: object
        description: Initial value.
    returns:
      type: str
      description: Template string value.
    """
    if value is None:
        return PrismaTemplate.PRISMA_2020_NEW_DATABASES_REGISTERS.value
    if isinstance(value, PrismaTemplate):
        return value.value
    return PrismaTemplate(str(value)).value


def _generate_into_output(
    inputs: Mapping[str, Any],
    output: Any,
    display: DisplayFunction,
    svg_display: Any,
    latest: LatestFlow,
) -> PrismaFlow | None:
    """
    title: Build and render the current flow in an output widget.
    parameters:
      inputs:
        type: Mapping[str, Any]
        description: Mapping of parameter names to widgets.
      output:
        type: Any
        description: Output widget.
      display:
        type: DisplayFunction
        description: IPython display function.
      svg_display:
        type: Any
        description: IPython SVG display class.
      latest:
        type: LatestFlow
        description: Mutable latest-flow cache.
    returns:
      type: PrismaFlow | None
      description: Generated flow, or None when generation failed.
    """
    try:
        flow = build_flow_from_widgets(inputs)
    except Exception as exc:
        latest["flow"] = None
        _show_error(output, exc)
        return None

    latest["flow"] = flow
    _show_flow(output, display, svg_display, flow)
    return flow


def _save_current_flow(
    inputs: Mapping[str, Any],
    output: Any,
    display: DisplayFunction,
    svg_display: Any,
    latest: LatestFlow,
    *,
    path: object,
    format_name: Literal["PNG", "SVG"],
) -> None:
    """
    title: Save the current flow to SVG or PNG.
    parameters:
      inputs:
        type: Mapping[str, Any]
        description: Mapping of parameter names to widgets.
      output:
        type: Any
        description: Output widget.
      display:
        type: DisplayFunction
        description: IPython display function.
      svg_display:
        type: Any
        description: IPython SVG display class.
      latest:
        type: LatestFlow
        description: Mutable latest-flow cache.
      path:
        type: object
        description: Destination path value.
      format_name:
        type: Literal[PNG, SVG]
        description: Output format name.
    """
    destination = str(path).strip()
    if destination == "":
        _show_error(output, ValueError(f"{format_name} path cannot be empty"))
        return

    flow = _generate_into_output(inputs, output, display, svg_display, latest)
    if flow is None:
        return

    try:
        if format_name == "SVG":
            flow.to_svg(Path(destination))
        else:
            flow.to_png(Path(destination))
    except Exception as exc:
        _show_error(output, exc)
        return
    with output:
        print(f"Saved {format_name} to {destination}")


def _show_flow(
    output: Any,
    display: DisplayFunction,
    svg_display: Any,
    flow: PrismaFlow,
) -> None:
    """
    title: Display a flow validation report and SVG preview.
    parameters:
      output:
        type: Any
        description: Output widget.
      display:
        type: DisplayFunction
        description: IPython display function.
      svg_display:
        type: Any
        description: IPython SVG display class.
      flow:
        type: PrismaFlow
        description: Flow to display.
    """
    report = flow.validate()
    with output:
        output.clear_output(wait=True)
        print(report.format_text())
        print()
        display(svg_display(data=flow.to_svg()))


def _show_error(output: Any, error: Exception) -> None:
    """
    title: Display an error message in the output area.
    parameters:
      output:
        type: Any
        description: Output widget.
      error:
        type: Exception
        description: Error to display.
    """
    with output:
        output.clear_output(wait=True)
        print(f"Error: {error}")
