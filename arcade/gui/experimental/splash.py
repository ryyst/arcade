"""
An experimental splash screen for arcade.

This is a simple splash screen that shows the arcade logo for a few seconds before the actual game starts.

If arcade is properly installed, you can run this script with:
python -m arcade.gui.experimental.splash
"""

import arcade
from arcade import View
from arcade.gui import UIAnchorLayout, UIBoxLayout, UIImage, UILabel, UIView


class ArcadeSplash(UIView):
    """This view shows an arcade splash screen before the actual game starts.

    params:
    - duration: int = 3
        The duration of the splash screen in seconds.
    - next_view: UIView = None
    """

    def __init__(self, view: View, duration: int = 3):
        super().__init__()
        self.view = view
        self.duration = duration
        self._time = 0

        anchor = self.ui.add(UIAnchorLayout())
        box = anchor.add(UIBoxLayout(space_between=20))
        self._logo = box.add(
            UIImage(texture=arcade.load_texture(":system:/logo.png"), width=400, height=400)
        )
        self._logo.alpha = 0
        box.add(UILabel("Python Arcade", text_color=(0, 0, 0, 255), font_size=40, bold=True))

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE_SMOKE)
        self._time = 0

    def on_update(self, delta_time: float):
        self._time += delta_time
        if self._time >= self.duration:
            self.window.show_view(self.view)

        # fade in arcade logo
        self._logo.alpha = min(255, int(255 * self._time / self.duration))


if __name__ == "__main__":
    window = arcade.Window()
    window.show_view(ArcadeSplash(View()))
    arcade.run()
