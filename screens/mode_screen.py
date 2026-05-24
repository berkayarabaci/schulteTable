from kivy.app import App
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from core.game_config import GameConfig, GameMode
from ui.widgets import AppButton, ColorPalette


class ModeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = FloatLayout()

        title = Label(
            text="Game Modes",
            font_size=dp(36),
            bold=True,
            color=ColorPalette.TEXT,
            size_hint=(1, None),
            height=dp(60),
            pos_hint={"center_x": 0.5, "top": 0.94},
        )
        root.add_widget(title)

        grid = GridLayout(
            cols=1,
            spacing=dp(12),
            size_hint=(0.82, None),
            height=dp(350),
            pos_hint={"center_x": 0.5, "top": 0.80},
        )

        modes = [
            ("Classic 5 x 5", GameConfig(grid_size=5, mode=GameMode.CLASSIC), ColorPalette.BLUE),
            ("Countdown 5 x 5", GameConfig(grid_size=5, mode=GameMode.COUNTDOWN, time_limit=45), ColorPalette.ORANGE),
            ("Reverse 5 x 5", GameConfig(grid_size=5, mode=GameMode.REVERSE), ColorPalette.PURPLE),
            ("3 Lives 5 x 5", GameConfig(grid_size=5, mode=GameMode.LIVES, lives=3), ColorPalette.RED),
        ]

        for text, config, color in modes:
            button = AppButton(
                text=text,
                font_size=dp(21),
                background_color=color,
            )
            button.bind(on_press=lambda instance, c=config: self.start_game(instance, c))
            grid.add_widget(button)

        root.add_widget(grid)

        back_button = AppButton(
            text="Back",
            font_size=dp(18),
            background_color=ColorPalette.DARK_BUTTON,
            size_hint=(0.76, None),
            height=dp(55),
            pos_hint={"center_x": 0.5, "y": 0.07},
        )
        back_button.bind(on_press=self.go_back)
        root.add_widget(back_button)

        self.add_widget(root)

    def start_game(self, button, config: GameConfig):
        button.animate_tap()
        app = App.get_running_app()
        app.game_screen.start_new_game(config)
        app.root.current = "game"

    def go_back(self, button):
        button.animate_tap()
        App.get_running_app().root.current = "menu"