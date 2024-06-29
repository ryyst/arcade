from typing import Optional

import arcade
from arcade import LBWH
from arcade.gui import UILayout, bind, UIWidget, Property, Surface
from arcade.types import AnchorPoint, Color


class UISimpleGridLayout(UILayout):
    """
    A simple grid layout that places widgets in a grid.

    The grid is defined by the number of columns and rows.
    Adding a new widget will place it in the next cell (left to right, top to bottom).

    All cells are the same size. The requested minimal size is determined by the largest widget in the grid.
    The actual cell size is determined by the size of the grid and the number of columns and rows.

    Widgets can be added to the grid using the :meth:`add` method.
    The position of a widget within its cell can be specified using the anchor parameter.

    Providing a column or row within :meth:`add` will place the widget in the specified cell,
    but will not change the index of the next widget to be added.

    The grid can be rendered with grid lines using the :meth:`with_grid_color` method.
    The lines are rendered behind the widgets, use space_between to create a gap between the widgets for the lines.
    """

    _grid_color: Optional[Color] = Property()
    _grid_width: Optional[int] = Property(0)

    def __init__(
        self,
        columns: int,
        rows: int,
        horizontal_space_between: int = 0,
        vertical_space_between: int = 0,
        size_hint=(0, 0),
    ):
        """
        Create a grid layout.

        :param columns: Number of columns in the grid.
        :param rows: Number of rows in the grid.
        :param space_between: Space between widgets.
        """
        super().__init__(size_hint=size_hint)
        self.columns = columns
        self.rows = rows
        self.horizontal_space_between = horizontal_space_between
        self.vertical_space_between = vertical_space_between
        self._index = 0

        bind(self, "_children", self._update_size_hints)
        bind(self, "_border_width", self._update_size_hints)
        bind(self, "_padding_left", self._update_size_hints)
        bind(self, "_padding_right", self._update_size_hints)
        bind(self, "_padding_top", self._update_size_hints)
        bind(self, "_padding_bottom", self._update_size_hints)

        bind(self, "_grid_color", self.trigger_render)
        bind(self, "_grid_width", self.trigger_render)

    def with_grid_color(self, color=None, width=1):
        """
        Set the color of the grid lines.
        """
        self._grid_color = color
        self._grid_width = width

        return self

    def add(self, child, *, column=None, row=None, anchor=AnchorPoint.CENTER):
        """
        Add a widget to the grid layout.

        :param child: Widget to add.
        :param column: Column to place the widget in. If None, the widget will be placed in the next cell.
        :param row: Row to place the widget in. If None, the widget will be placed in the next cell.
        :param anchor: Anchor point of the widget in the cell.
        """
        if row is None and column is None:
            column = self._index % self.columns
            row = self._index // self.columns
            self._index += 1

        super().add(child, column=column, row=row, anchor=anchor)

        self._debug_points = []

    def _update_size_hints(self):
        """
        Update the minimum size hint of the layout.

        The minimum size hint is the size of the largest widget in the layout.
        """
        min_child_sizes = [UILayout.min_size_of(child) for child in self.children]
        if not min_child_sizes:
            self.size_hint_min = (0, 0)
            return

        min_widths = max([size_hint[0] for size_hint in min_child_sizes])
        min_heights = max([size_hint[1] for size_hint in min_child_sizes])

        self.size_hint_min = (
            min_widths * self.columns + self.horizontal_space_between * (self.columns - 1),
            min_heights * self.rows + self.vertical_space_between * (self.rows - 1),
        )

    def do_layout(self):
        """
        Layout the widgets in the grid.

        The widgets are placed in the grid from left to right, top to bottom.
        """
        cell_width = (self.content_width - self.horizontal_space_between * (self.columns - 1)) / self.columns
        cell_height = (self.content_height - self.vertical_space_between * (self.rows - 1)) / self.rows

        for child, data in self._children:
            child: UIWidget
            column = data.get("column", 0)
            row = data.get("row", 0)
            anchor = data.get("anchor", AnchorPoint.CENTER)

            cell_left = self.content_rect.left + column * (cell_width + self.horizontal_space_between)
            cell_top = self.content_rect.top - row * (cell_height + self.vertical_space_between)
            cell_bottom = cell_top - cell_height

            # calculate the offset based on the anchor point
            cell = LBWH(cell_left, cell_bottom, cell_width, cell_height)
            # TODO resize child according to child size hints and cell size
            child.rect = cell.resize(width=child.width, height=child.height, anchor=anchor)

    def do_render_base(self, surface: Surface):
        """
        Render the grid lines.

        :param surface: Surface to render on.
        """
        super().do_render_base(surface)

        if self._grid_color:
            cell_width = (self.content_width - self.horizontal_space_between * (self.columns - 1)) / self.columns
            cell_height = (self.content_height - self.vertical_space_between * (self.rows - 1)) / self.rows

            # draw lines relative to 0,0
            for column in range(1, self.columns):
                x = column * (cell_width + self.horizontal_space_between)
                arcade.draw_line(x, 0, x, self.content_height, color=self._grid_color, line_width=self._grid_width)

            for row in range(1, self.rows):
                y = row * (cell_height + self.vertical_space_between)
                arcade.draw_line(0, y, self.content_width, y, color=self._grid_color, line_width=self._grid_width)
