from kivy.app import App
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from core.storage import LocalStorage
from ui.widgets import AppButton, ColorPalette


class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.storage = LocalStorage()
        self.root_layout = FloatLayout()
        self.add_widget(self.root_layout)

    def on_pre_enter(self, *args):
        self.build_profile()

    def build_profile(self):
        self.root_layout.clear_widgets()

        profile = self.storage.load_profile()

        title = Label(
            text="Profile",
            font_size=dp(38),
            bold=True,
            color=ColorPalette.TEXT,
            size_hint=(1, None),
            height=dp(60),
            pos_hint={"center_x": 0.5, "top": 0.96},
        )
        self.root_layout.add_widget(title)

        name_label = Label(
            text=profile.name,
            font_size=dp(26),
            bold=True,
            color=ColorPalette.TEXT,
            size_hint=(1, None),
            height=dp(45),
            pos_hint={"center_x": 0.5, "top": 0.86},
        )
        self.root_layout.add_widget(name_label)

        xp_to_next_level = self.get_xp_to_next_level(profile.xp)

        stats_grid = GridLayout(
            cols=2,
            spacing=dp(12),
            size_hint=(0.86, None),
            height=dp(300),
            pos_hint={"center_x": 0.5, "top": 0.75},
        )

        stats = [
            ("Player Level", str(profile.player_level)),
            ("XP", str(profile.xp)),
            ("Next Level In", f"{xp_to_next_level} XP"),
            ("Coins", str(profile.coins)),
            ("Games Played", str(profile.total_games_played)),
            ("Levels Completed", str(profile.total_completed_levels)),
            ("Unlocked Level", str(profile.highest_unlocked_level)),
            ("Total Stars", str(self.get_total_stars(profile))),
        ]

        for label, value in stats:
            stats_grid.add_widget(
                self.create_stat_card(label=label, value=value)
            )

        self.root_layout.add_widget(stats_grid)

        leaderboard_button = AppButton(
            text="Local Leaderboards",
            font_size=dp(21),
            background_color=ColorPalette.PURPLE,
            size_hint=(0.76, None),
            height=dp(58),
            pos_hint={"center_x": 0.5, "y": 0.18},
        )
        leaderboard_button.bind(on_press=self.go_to_leaderboard)
        self.root_layout.add_widget(leaderboard_button)

        back_button = AppButton(
            text="Back",
            font_size=dp(19),
            background_color=ColorPalette.DARK_BUTTON,
            size_hint=(0.76, None),
            height=dp(55),
            pos_hint={"center_x": 0.5, "y": 0.07},
        )
        back_button.bind(on_press=self.go_back)
        self.root_layout.add_widget(back_button)

    def create_stat_card(self, label: str, value: str) -> FloatLayout:
        card = FloatLayout()

        value_label = Label(
            text=value,
            font_size=dp(24),
            bold=True,
            color=ColorPalette.TEXT,
            size_hint=(1, None),
            height=dp(35),
            pos_hint={"center_x": 0.5, "top": 0.78},
        )
        card.add_widget(value_label)

        title_label = Label(
            text=label,
            font_size=dp(13),
            color=ColorPalette.MUTED_TEXT,
            size_hint=(1, None),
            height=dp(30),
            pos_hint={"center_x": 0.5, "top": 0.38},
        )
        card.add_widget(title_label)

        return card

    def get_xp_to_next_level(self, xp: int) -> int:
        next_level_xp = ((xp // 100) + 1) * 100
        return max(0, next_level_xp - xp)

    def get_total_stars(self, profile) -> int:
        return sum(progress.stars for progress in profile.level_progress.values())

    def go_to_leaderboard(self, button):
        button.animate_tap()
        App.get_running_app().root.current = "leaderboard"

    def go_back(self, button):
        button.animate_tap()
        App.get_running_app().root.current = "menu"