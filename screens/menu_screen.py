from kivy.app import App
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from ui.widgets import AppButton, ColorPalette


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = FloatLayout()

        title = Label(
            text="Schulte Table",
            font_size=dp(42),
            bold=True,
            color=ColorPalette.TEXT,
            size_hint=(1, None),
            height=dp(70),
            pos_hint={"center_x": 0.5, "top": 0.92},
        )
        root.add_widget(title)

        subtitle = Label(
            text="Focus. Speed. Memory.",
            font_size=dp(18),
            color=ColorPalette.MUTED_TEXT,
            size_hint=(1, None),
            height=dp(35),
            pos_hint={"center_x": 0.5, "top": 0.82},
        )
        root.add_widget(subtitle)

        play_button = AppButton(
            text="Play Modes",
            font_size=dp(23),
            background_color=ColorPalette.BLUE,
            size_hint=(0.76, None),
            height=dp(60),
            pos_hint={"center_x": 0.5, "top": 0.62},
        )
        play_button.bind(on_press=self.go_to_modes)
        root.add_widget(play_button)

        levels_button = AppButton(
            text="Levels",
            font_size=dp(23),
            background_color=ColorPalette.PURPLE,
            size_hint=(0.76, None),
            height=dp(60),
            pos_hint={"center_x": 0.5, "top": 0.50},
        )
        levels_button.bind(on_press=self.go_to_levels)
        root.add_widget(levels_button)

        daily_button = AppButton(
            text="Daily Quest - Coming Soon",
            font_size=dp(20),
            background_color=ColorPalette.DARK_BUTTON,
            size_hint=(0.76, None),
            height=dp(58),
            pos_hint={"center_x": 0.5, "top": 0.38},
        )
        root.add_widget(daily_button)

        login_button = AppButton(
            text="Google Sign-In - Coming Soon",
            font_size=dp(19),
            background_color=ColorPalette.DARK_BUTTON,
            size_hint=(0.76, None),
            height=dp(58),
            pos_hint={"center_x": 0.5, "top": 0.26},
        )
        root.add_widget(login_button)

        footer = Label(
            text="Online features will be added after offline systems are stable",
            font_size=dp(13),
            color=(0.55, 0.58, 0.66, 1),
            size_hint=(1, None),
            height=dp(35),
            pos_hint={"center_x": 0.5, "y": 0.04},
        )
        root.add_widget(footer)

        self.add_widget(root)

    def go_to_modes(self, button):
        button.animate_tap()
        App.get_running_app().root.current = "modes"

    def go_to_levels(self, button):
        button.animate_tap()
        App.get_running_app().root.current = "levels"