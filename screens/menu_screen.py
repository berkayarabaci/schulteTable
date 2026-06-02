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
            pos_hint={"center_x": 0.5, "top": 0.95},
        )
        root.add_widget(title)

        subtitle = Label(
            text="Focus. Speed. Memory.",
            font_size=dp(18),
            color=ColorPalette.MUTED_TEXT,
            size_hint=(1, None),
            height=dp(35),
            pos_hint={"center_x": 0.5, "top": 0.86},
        )
        root.add_widget(subtitle)

        play_button = AppButton(
            text="Play Modes",
            font_size=dp(22),
            background_color=ColorPalette.BLUE,
            size_hint=(0.76, None),
            height=dp(54),
            pos_hint={"center_x": 0.5, "top": 0.70},
        )
        play_button.bind(on_press=self.go_to_modes)
        root.add_widget(play_button)

        levels_button = AppButton(
            text="Levels",
            font_size=dp(22),
            background_color=ColorPalette.PURPLE,
            size_hint=(0.76, None),
            height=dp(54),
            pos_hint={"center_x": 0.5, "top": 0.60},
        )
        levels_button.bind(on_press=self.go_to_levels)
        root.add_widget(levels_button)

        profile_button = AppButton(
            text="Profile",
            font_size=dp(22),
            background_color=ColorPalette.GREEN,
            size_hint=(0.76, None),
            height=dp(54),
            pos_hint={"center_x": 0.5, "top": 0.50},
        )
        profile_button.bind(on_press=self.go_to_profile)
        root.add_widget(profile_button)

        settings_button = AppButton(
            text="Settings",
            font_size=dp(21),
            background_color=ColorPalette.ORANGE,
            size_hint=(0.76, None),
            height=dp(54),
            pos_hint={"center_x": 0.5, "top": 0.40},
        )
        settings_button.bind(on_press=self.go_to_settings)
        root.add_widget(settings_button)

        daily_button = AppButton(
            text="Daily Quest - Coming Soon",
            font_size=dp(18),
            background_color=ColorPalette.DARK_BUTTON,
            size_hint=(0.76, None),
            height=dp(52),
            pos_hint={"center_x": 0.5, "top": 0.30},
        )
        root.add_widget(daily_button)

        login_button = AppButton(
            text="Google Sign-In - Coming Soon",
            font_size=dp(17),
            background_color=ColorPalette.DARK_BUTTON,
            size_hint=(0.76, None),
            height=dp(52),
            pos_hint={"center_x": 0.5, "top": 0.20},
        )
        root.add_widget(login_button)

        footer = Label(
            text="Offline progress saves locally on this device",
            font_size=dp(13),
            color=(0.55, 0.58, 0.66, 1),
            size_hint=(1, None),
            height=dp(35),
            pos_hint={"center_x": 0.5, "y": 0.03},
        )
        root.add_widget(footer)

        self.add_widget(root)

    def go_to_modes(self, button):
        button.animate_tap()
        App.get_running_app().root.current = "modes"

    def go_to_levels(self, button):
        button.animate_tap()
        App.get_running_app().root.current = "levels"

    def go_to_profile(self, button):
        button.animate_tap()
        App.get_running_app().root.current = "profile"

    def go_to_settings(self, button):
        button.animate_tap()
        App.get_running_app().root.current = "settings"