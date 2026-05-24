from kivy.app import App
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen

from core.level_repository import LevelRepository
from core.storage import LocalStorage
from ui.widgets import AppButton, ColorPalette


class LevelsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.level_repository = LevelRepository()
        self.storage = LocalStorage()

        self.root_layout = FloatLayout()
        self.add_widget(self.root_layout)

    def on_pre_enter(self, *args):
        self.build_level_list()

    def build_level_list(self):
        self.root_layout.clear_widgets()

        title = Label(
            text="Levels",
            font_size=dp(36),
            bold=True,
            color=ColorPalette.TEXT,
            size_hint=(1, None),
            height=dp(60),
            pos_hint={"center_x": 0.5, "top": 0.96},
        )
        self.root_layout.add_widget(title)

        progress = self.storage.load()
        highest_unlocked = progress.get("highest_unlocked_level", 1)
        completed_levels = set(progress.get("completed_levels", []))

        scroll = ScrollView(
            size_hint=(0.9, 0.72),
            pos_hint={"center_x": 0.5, "top": 0.84},
        )

        levels = self.level_repository.get_levels()

        grid = GridLayout(
            cols=1,
            spacing=dp(10),
            size_hint_y=None,
        )
        grid.bind(minimum_height=grid.setter("height"))

        for level in levels:
            is_unlocked = level.level_number <= highest_unlocked
            is_completed = level.level_number in completed_levels

            if is_completed:
                prefix = "✓"
                color = ColorPalette.GREEN
            elif is_unlocked:
                prefix = "▶"
                color = ColorPalette.BLUE
            else:
                prefix = "🔒"
                color = ColorPalette.DARK_BUTTON

            button = AppButton(
                text=f"{prefix} Level {level.level_number}: {level.mode.value.capitalize()} {level.grid_size}x{level.grid_size}",
                font_size=dp(17),
                background_color=color,
                size_hint_y=None,
                height=dp(56),
                disabled=not is_unlocked,
            )

            if is_unlocked:
                button.bind(
                    on_press=lambda instance, selected_level=level: self.start_level(
                        instance,
                        selected_level,
                    )
                )

            grid.add_widget(button)

        scroll.add_widget(grid)
        self.root_layout.add_widget(scroll)

        back_button = AppButton(
            text="Back",
            font_size=dp(18),
            background_color=ColorPalette.DARK_BUTTON,
            size_hint=(0.76, None),
            height=dp(55),
            pos_hint={"center_x": 0.5, "y": 0.05},
        )
        back_button.bind(on_press=self.go_back)
        self.root_layout.add_widget(back_button)

    def start_level(self, button, level):
        button.animate_tap()
        app = App.get_running_app()
        app.game_screen.start_new_game(level)
        app.root.current = "game"

    def go_back(self, button):
        button.animate_tap()
        App.get_running_app().root.current = "menu"