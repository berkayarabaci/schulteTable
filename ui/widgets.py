from kivy.animation import Animation
from kivy.metrics import dp
from kivy.uix.button import Button


class AppButton(Button):
    """
    Reusable styled button.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""
        self.color = (1, 1, 1, 1)
        self.bold = True
        self.font_size = kwargs.get("font_size", dp(20))

    def animate_tap(self):
        animation = (
            Animation(opacity=0.65, duration=0.06)
            + Animation(opacity=1, duration=0.08)
        )
        animation.start(self)


class ColorPalette:
    BACKGROUND = (0.06, 0.07, 0.10, 1)
    CARD = (0.12, 0.14, 0.20, 1)
    TEXT = (1, 1, 1, 1)
    MUTED_TEXT = (0.72, 0.76, 0.86, 1)
    BLUE = (0.18, 0.52, 0.95, 1)
    GREEN = (0.22, 0.67, 0.48, 1)
    PURPLE = (0.55, 0.35, 0.95, 1)
    ORANGE = (0.95, 0.48, 0.22, 1)
    RED = (0.90, 0.28, 0.42, 1)
    DARK_BUTTON = (0.22, 0.24, 0.30, 1)

    CELL_COLORS = [
        BLUE,
        GREEN,
        PURPLE,
        ORANGE,
        RED,
    ]