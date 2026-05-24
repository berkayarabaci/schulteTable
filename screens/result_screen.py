from kivy.animation import Animation
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from core.game_config import GameConfig
from core.storage import LocalStorage
from ui.widgets import AppButton, ColorPalette


class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.last_config: GameConfig | None = None
        self.storage = LocalStorage()

        root = FloatLayout()

        self.title = Label(
            text="Finished!",
            font_size=dp(42),
            bold=True,
            color=ColorPalette.TEXT,
            size_hint=(1, None),
            height=dp(70),
            pos_hint={"center_x": 0.5, "top": 0.88},
        )
        root.add_widget(self.title)

        self.result_label = Label(
            text="",
            font_size=dp(22),
            color=ColorPalette.MUTED_TEXT,
            halign="center",
            size_hint=(0.9, None),
            height=dp(200),
            pos_hint={"center_x": 0.5, "center_y": 0.57},
        )
        root.add_widget(self.result_label)

        self.play_again_button = AppButton(
            text="Play Again",
            font_size=dp(22),
            background_color=ColorPalette.BLUE,
            size_hint=(0.76, None),
            height=dp(58),
            pos_hint={"center_x": 0.5, "y": 0.22},
        )
        self.play_again_button.bind(on_press=self.play_again)
        root.add_widget(self.play_again_button)

        self.menu_button = AppButton(
            text="Back to Menu",
            font_size=dp(20),
            background_color=ColorPalette.DARK_BUTTON,
            size_hint=(0.76, None),
            height=dp(55),
            pos_hint={"center_x": 0.5, "y": 0.11},
        )
        self.menu_button.bind(on_press=self.go_to_menu)
        root.add_widget(self.menu_button)

        self.add_widget(root)

    def show_result(
        self,
        config: GameConfig,
        elapsed_time: float,
        mistakes: int,
        success: bool,
    ):
        self.last_config = config

        if success and config.level_number is not None:
            self.storage.complete_level(
                level_number=config.level_number,
                elapsed_time=elapsed_time,
                mistakes=mistakes,
            )

        total_numbers = config.max_number
        average_time = elapsed_time / total_numbers if total_numbers else 0

        self.title.text = "Completed!" if success else "Failed!"
        self.title.color = ColorPalette.GREEN if success else ColorPalette.RED

        status_text = "Success" if success else "Try Again"

        self.result_label.text = (
            f"{status_text}\n\n"
            f"Mode: {config.mode.value.capitalize()}\n"
            f"Grid: {config.grid_size} x {config.grid_size}\n"
            f"Time: {elapsed_time:.1f} seconds\n"
            f"Mistakes: {mistakes}\n"
            f"Average: {average_time:.2f}s per number"
        )

        self.animate_widgets()

    def animate_widgets(self):
        widgets = [
            self.title,
            self.result_label,
            self.play_again_button,
            self.menu_button,
        ]

        for index, widget in enumerate(widgets):
            widget.opacity = 0
            Animation(opacity=1, duration=0.25 + index * 0.12).start(widget)

    def play_again(self, button):
        button.animate_tap()

        if self.last_config is None:
            App.get_running_app().root.current = "menu"
            return

        app = App.get_running_app()
        app.game_screen.start_new_game(self.last_config)
        app.root.current = "game"

    def go_to_menu(self, button):
        button.animate_tap()
        App.get_running_app().root.current = "menu"