from kivy.app import App
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen

from core.leaderboard_service import LeaderboardService
from core.storage import LocalStorage
from ui.widgets import AppButton, ColorPalette


class LeaderboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.storage = LocalStorage()
        self.leaderboard_service = LeaderboardService()

        self.root_layout = FloatLayout()
        self.add_widget(self.root_layout)

    def on_pre_enter(self, *args):
        self.build_leaderboard()

    def build_leaderboard(self):
        self.root_layout.clear_widgets()

        profile = self.storage.load_profile()

        title = Label(
            text="Local Leaderboards",
            font_size=dp(32),
            bold=True,
            color=ColorPalette.TEXT,
            size_hint=(1, None),
            height=dp(60),
            pos_hint={"center_x": 0.5, "top": 0.96},
        )
        self.root_layout.add_widget(title)

        scroll = ScrollView(
            size_hint=(0.9, 0.74),
            pos_hint={"center_x": 0.5, "top": 0.84},
        )

        content = GridLayout(
            cols=1,
            spacing=dp(14),
            size_hint_y=None,
        )
        content.bind(minimum_height=content.setter("height"))

        self.add_section_title(content, "Best Mode Scores")
        mode_scores = self.leaderboard_service.get_best_mode_scores(profile)

        if mode_scores:
            for score in mode_scores:
                self.add_score_row(
                    content,
                    title=score["display_name"],
                    detail=f"Best: {score['time']:.1f}s | Mistakes: {score['mistakes']}",
                    color=ColorPalette.BLUE,
                )
        else:
            self.add_empty_row(content, "No mode scores yet.")

        self.add_section_title(content, "Best Level Scores")
        level_scores = self.leaderboard_service.get_best_level_scores(profile)

        if level_scores:
            for score in level_scores:
                stars_text = "★" * score["stars"] + "☆" * (3 - score["stars"])
                self.add_score_row(
                    content,
                    title=f"Level {score['level_number']}   {stars_text}",
                    detail=(
                        f"Best: {score['best_time']:.1f}s | "
                        f"Mistakes: {score['best_mistakes']}"
                    ),
                    color=ColorPalette.GREEN,
                )
        else:
            self.add_empty_row(content, "No level scores yet.")

        scroll.add_widget(content)
        self.root_layout.add_widget(scroll)

        back_button = AppButton(
            text="Back",
            font_size=dp(19),
            background_color=ColorPalette.DARK_BUTTON,
            size_hint=(0.76, None),
            height=dp(55),
            pos_hint={"center_x": 0.5, "y": 0.05},
        )
        back_button.bind(on_press=self.go_back)
        self.root_layout.add_widget(back_button)

    def add_section_title(self, content: GridLayout, text: str) -> None:
        label = Label(
            text=text,
            font_size=dp(22),
            bold=True,
            color=ColorPalette.TEXT,
            size_hint_y=None,
            height=dp(42),
        )
        content.add_widget(label)

    def add_score_row(
        self,
        content: GridLayout,
        title: str,
        detail: str,
        color,
    ) -> None:
        row = AppButton(
            text=f"{title}\n{detail}",
            font_size=dp(15),
            background_color=color,
            size_hint_y=None,
            height=dp(68),
        )
        content.add_widget(row)

    def add_empty_row(self, content: GridLayout, text: str) -> None:
        row = Label(
            text=text,
            font_size=dp(16),
            color=ColorPalette.MUTED_TEXT,
            size_hint_y=None,
            height=dp(50),
        )
        content.add_widget(row)

    def go_back(self, button):
        button.animate_tap()
        App.get_running_app().root.current = "profile"