"""
title: Geometry primitives for diagram layout.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Anchor = Literal["top", "bottom", "left", "right"]


@dataclass(frozen=True)
class Point:
    """
    title: A point in diagram coordinates.
    attributes:
      x:
        type: float
        description: Value for x.
      y:
        type: float
        description: Value for y.
    """

    x: float
    y: float


@dataclass(frozen=True)
class Rect:
    """
    title: A rectangular diagram area.
    attributes:
      x:
        type: float
        description: Value for x.
      y:
        type: float
        description: Value for y.
      width:
        type: float
        description: Value for width.
      height:
        type: float
        description: Value for height.
    """

    x: float
    y: float
    width: float
    height: float

    @property
    def center_x(self) -> float:
        """
        title: Horizontal center coordinate.
        returns:
          type: float
          description: Return value.
        """
        return self.x + self.width / 2

    @property
    def center_y(self) -> float:
        """
        title: Vertical center coordinate.
        returns:
          type: float
          description: Return value.
        """
        return self.y + self.height / 2

    @property
    def top_center(self) -> Point:
        """
        title: Top-center anchor.
        returns:
          type: Point
          description: Return value.
        """
        return Point(self.center_x, self.y)

    @property
    def bottom_center(self) -> Point:
        """
        title: Bottom-center anchor.
        returns:
          type: Point
          description: Return value.
        """
        return Point(self.center_x, self.y + self.height)

    @property
    def left_center(self) -> Point:
        """
        title: Left-center anchor.
        returns:
          type: Point
          description: Return value.
        """
        return Point(self.x, self.center_y)

    @property
    def right_center(self) -> Point:
        """
        title: Right-center anchor.
        returns:
          type: Point
          description: Return value.
        """
        return Point(self.x + self.width, self.center_y)

    def anchor(self, name: Anchor) -> Point:
        """
        title: Return a named anchor point.
        parameters:
          name:
            type: Anchor
            description: Value for name.
        returns:
          type: Point
          description: Return value.
        """
        if name == "top":
            return self.top_center
        if name == "bottom":
            return self.bottom_center
        if name == "left":
            return self.left_center
        return self.right_center

    def overlaps(self, other: Rect, *, padding: float = 0) -> bool:
        """
        title: Return whether this rectangle overlaps another rectangle.
        parameters:
          other:
            type: Rect
            description: Value for other.
          padding:
            type: float
            description: Value for padding.
        returns:
          type: bool
          description: Return value.
        """
        return not (
            self.x + self.width + padding <= other.x
            or other.x + other.width + padding <= self.x
            or self.y + self.height + padding <= other.y
            or other.y + other.height + padding <= self.y
        )
