"""
Creating a hidden password field

This example demonstrates how to create a custom text input
which hides the contents behind a custom character, as often
required for login screens

If arcade and Python are properly installed, you can run this example with:
python -m arcade.gui.examples.exp_simple_grid
"""

from __future__ import annotations

import arcade
from arcade.gui import UIManager, UIDummy
from arcade.gui.experimental.simplegrid import UISimpleGridLayout
from arcade.gui.widgets.layout import UIAnchorLayout
from arcade.types import AnchorPoint


class MyView(arcade.gui.UIView):
    def __init__(self):
        super().__init__()
        self.ui = UIManager()
        anchor = self.ui.add(UIAnchorLayout())

        self.grid = anchor.add(UISimpleGridLayout(
            3,
            3,
            size_hint=(0.8, 0.8),
            horizontal_space_between=10,
        ))
        self.grid.with_border(color=arcade.color.WHITE)
        self.grid.with_grid_color(arcade.color.RED, width=1)
        self.grid.with_background(color=arcade.color.BUD_GREEN)

        self.grid.add(UIDummy(), anchor=AnchorPoint.TOP_LEFT)
        self.grid.add(UIDummy(), anchor=AnchorPoint.TOP_CENTER)
        self.grid.add(UIDummy(), anchor=AnchorPoint.TOP_RIGHT)
        self.grid.add(UIDummy(), anchor=AnchorPoint.BOTTOM_LEFT)
        self.grid.add(UIDummy(), anchor=AnchorPoint.BOTTOM_CENTER)
        self.grid.add(UIDummy(), anchor=AnchorPoint.BOTTOM_RIGHT)
        self.grid.add(UIDummy(width=50, height=50), anchor=AnchorPoint.CENTER_LEFT)
        self.grid.add(UIDummy(), anchor=AnchorPoint.CENTER)

        self.ui.add(anchor)

    def on_draw(self):
        self.clear()
        super().on_draw()


if __name__ == "__main__":
    window = arcade.Window(800, 600, "UIExample", resizable=True)
    window.show_view(MyView())
    window.run()
