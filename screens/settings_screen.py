from kivy.app import App
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from core.profile_service import ProfileService
from core.storage import LocalStorage
from ui.widgets import AppButton, ColorPalette


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.storage = LocalStorage()
        self.profile_service = ProfileService(self.storage)

        self.root_layout = FloatLayout()
        self.add_widget(self.root_layout)

        self.name_input = None
        self.status_label = None

    def on_pre_enter(self, *args):
        self.build_settings()

    def build_settings(self):
        self.root_layout.clear_widgets()

        profile = self.profile_service.get_profile()

        title = Label(
            text="Settings",
            font_size=dp(38),
            bold=True,
            color=ColorPalette.TEXT,
            size_hint=(1, None),
            height=dp(60),
            pos_hint={"center_x": 0.5, "top": 0.96},
        )
        self.root_layout.add_widget(title)

        name_label = Label(
            text="Player Name",
            font_size=dp(20),
            bold=True,
            color=ColorPalette.TEXT,
            size_hint=(0.8, None),
            height=dp(35),
            pos_hint={"center_x": 0.5, "top": 0.82},
        )
        self.root_layout.add_widget(name_label)

        self.name_input = TextInput(
            text=profile.name,
            multiline=False,
            font_size=dp(22),
            foreground_color=ColorPalette.TEXT,
            background_color=(0.14, 0.16, 0.22, 1),
            cursor_color=ColorPalette.TEXT,
            padding=[dp(14), dp(12), dp(14), dp(12)],
            size_hint=(0.78, None),
            height=dp(56),
            pos_hint={"center_x": 0.5, "top": 0.75},
        )
        self.root_layout.add_widget(self.name_input)

        save_name_button = AppButton(
            text="Save Name",
            font_size=dp(20),
            background_color=ColorPalette.BLUE,
            size_hint=(0.78, None),
            height=dp(56),
            pos_hint={"center_x": 0.5, "top": 0.64},
        )
        save_name_button.bind(on_press=self.save_name)
        self.root_layout.add_widget(save_name_button)

        future_settings_label = Label(
            text="Coming Soon\nSound • Vibration • Themes • Animation Settings",
            font_size=dp(17),
            color=ColorPalette.MUTED_TEXT,
            halign="center",
            valign="middle",
            size_hint=(0.86, None),
            height=dp(90),
            pos_hint={"center_x": 0.5, "top": 0.50},
        )
        self.root_layout.add_widget(future_settings_label)

        reset_button = AppButton(
            text="Reset Progress",
            font_size=dp(20),
            background_color=ColorPalette.RED,
            size_hint=(0.78, None),
            height=dp(56),
            pos_hint={"center_x": 0.5, "top": 0.34},
        )
        reset_button.bind(on_press=self.reset_progress)
        self.root_layout.add_widget(reset_button)

        self.status_label = Label(
            text="Progress is saved locally on this device.",
            font_size=dp(14),
            color=ColorPalette.MUTED_TEXT,
            size_hint=(0.9, None),
            height=dp(45),
            pos_hint={"center_x": 0.5, "top": 0.23},
        )
        self.root_layout.add_widget(self.status_label)

        back_button = AppButton(
            text="Back",
            font_size=dp(19),
            background_color=ColorPalette.DARK_BUTTON,
            size_hint=(0.76, None),
            height=dp(55),
            pos_hint={"center_x": 0.5, "y": 0.06},
        )
        back_button.bind(on_press=self.go_back)
        self.root_layout.add_widget(back_button)

    def save_name(self, button):
        button.animate_tap()

        new_name = self.name_input.text if self.name_input else "Player"
        profile = self.profile_service.update_player_name(new_name)

        if self.status_label:
            self.status_label.text = f"Saved name: {profile.name}"
            self.status_label.color = ColorPalette.GREEN

    def reset_progress(self, button):
        button.animate_tap()

        self.profile_service.reset_progress()

        if self.name_input:
            self.name_input.text = "Player"

        if self.status_label:
            self.status_label.text = "Progress reset successfully."
            self.status_label.color = ColorPalette.RED

    def go_back(self, button):
        button.animate_tap()
        App.get_running_app().root.current = "menu"