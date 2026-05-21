"""
title: Text wrapping helpers for renderers.
"""

from __future__ import annotations

import textwrap


def wrap_text(text: str, *, max_chars: int = 34) -> list[str]:
    """
    title: Wrap text while preserving explicit line breaks.
    parameters:
      text:
        type: str
        description: Value for text.
      max_chars:
        type: int
        description: Value for max_chars.
    returns:
      type: list[str]
      description: Return value.
    """
    lines: list[str] = []
    for raw_line in text.splitlines() or [""]:
        if not raw_line:
            lines.append("")
            continue
        wrapped = textwrap.wrap(
            raw_line,
            width=max_chars,
            break_long_words=False,
            break_on_hyphens=False,
        )
        lines.extend(wrapped or [raw_line])
    return lines
