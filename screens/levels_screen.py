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

        profile = self.storage.load_profile()
        highest_unlocked = profile.highest_unlocked_level

        progress_label = Label(
            text=(
                f"{profile.name} | Level {profile.player_level} | "
                f"XP: {profile.xp} | Coins: {profile.coins}"
            ),
            font_size=dp(14),
            color=ColorPalette.MUTED_TEXT,
            size_hint=(1, None),
            height=dp(30),
            pos_hint={"center_x": 0.5, "top": 0.89},
        )
        self.root_layout.add_widget(progress_label)

        scroll = ScrollView(
            size_hint=(0.9, 0.68),
            pos_hint={"center_x": 0.5, "top": 0.82},
        )

        levels = self.level_repository.get_levels()

        grid = GridLayout(
            cols=1,
            spacing=dp(10),
            size_hint_y=None,
        )
        grid.bind(minimum_height=grid.setter("height"))

        for level in levels:
            level_key = f"level_{level.level_number}"
            level_progress = profile.level_progress.get(level_key)

            is_unlocked = level.level_number <= highest_unlocked

            stars = level_progress.stars if level_progress else 0
            stars_text = "★" * stars + "☆" * (3 - stars)

            best_text = ""
            if level_progress and level_progress.best_time is not None:
                best_text = f" | Best: {level_progress.best_time:.1f}s"

            if stars > 0:
                prefix = stars_text
                color = ColorPalette.GREEN
            elif is_unlocked:
                prefix = "▶"
                color = ColorPalette.BLUE
            else:
                prefix = "🔒"
                color = ColorPalette.DARK_BUTTON

            button = AppButton(
                text=(
                    f"{prefix}  Level {level.level_number}: "
                    f"{level.mode.value.capitalize()} {level.grid_size}x{level.grid_size}"
                    f"{best_text}"
                ),
                font_size=dp(14),
                background_color=color,
                size_hint_y=None,
                height=dp(60),
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