import random

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from core.game_config import GameConfig, GameMode
from core.game_modes import GameRules
from ui.widgets import AppButton, ColorPalette


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.config = GameConfig(grid_size=5, mode=GameMode.CLASSIC)
        self.rules = GameRules(self.config)

        self.elapsed_time = 0
        self.timer_event = None
        self.has_started = False

        self.root_layout = FloatLayout()
        self.add_widget(self.root_layout)

        self.header = Label(
            text="Schulte Table",
            font_size=dp(27),
            bold=True,
            color=ColorPalette.TEXT,
            size_hint=(1, None),
            height=dp(45),
            pos_hint={"center_x": 0.5, "top": 0.98},
        )
        self.root_layout.add_widget(self.header)

        self.info_label = Label(
            text="Tap 1 to start",
            font_size=dp(17),
            color=ColorPalette.MUTED_TEXT,
            size_hint=(1, None),
            height=dp(38),
            pos_hint={"center_x": 0.5, "top": 0.92},
        )
        self.root_layout.add_widget(self.info_label)

        self.grid = GridLayout(
            cols=self.config.grid_size,
            spacing=dp(7),
            size_hint=(0.92, 0.64),
            pos_hint={"center_x": 0.5, "center_y": 0.52},
        )
        self.root_layout.add_widget(self.grid)

        self.menu_button = AppButton(
            text="Menu",
            font_size=dp(17),
            background_color=ColorPalette.DARK_BUTTON,
            size_hint=(0.32, None),
            height=dp(50),
            pos_hint={"x": 0.06, "y": 0.05},
        )
        self.menu_button.bind(on_press=self.go_to_menu)
        self.root_layout.add_widget(self.menu_button)

        self.restart_button = AppButton(
            text="Restart",
            font_size=dp(17),
            background_color=ColorPalette.BLUE,
            size_hint=(0.56, None),
            height=dp(50),
            pos_hint={"right": 0.94, "y": 0.05},
        )
        self.restart_button.bind(on_press=self.restart_game)
        self.root_layout.add_widget(self.restart_button)

    def start_new_game(self, config: GameConfig):
        self.config = config
        self.rules = GameRules(config)
        self.header.text = config.title
        self.restart_game()

    def restart_game(self, *args):
        self.elapsed_time = 0
        self.has_started = False
        self.rules = GameRules(self.config)

        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None

        self.info_label.text = self.rules.get_start_message()
        self.info_label.color = ColorPalette.MUTED_TEXT

        self.grid.clear_widgets()
        self.grid.cols = self.config.grid_size

        numbers = list(range(1, self.config.max_number + 1))
        random.shuffle(numbers)

        font_size = self.get_cell_font_size()

        for number in numbers:
            button = AppButton(
                text=str(number),
                font_size=font_size,
                background_color=random.choice(ColorPalette.CELL_COLORS),
            )
            button.opacity = 0
            button.bind(on_press=self.check_number)
            self.grid.add_widget(button)

            Animation(opacity=1, duration=0.22).start(button)

    def get_cell_font_size(self):
        if self.config.grid_size <= 3:
            return dp(34)
        if self.config.grid_size == 4:
            return dp(30)
        if self.config.grid_size == 5:
            return dp(25)
        return dp(21)

    def start_timer(self):
        if self.timer_event is None:
            self.timer_event = Clock.schedule_interval(self.update_timer, 0.1)

    def update_timer(self, dt):
        self.elapsed_time += dt

        if self.config.mode == GameMode.COUNTDOWN and self.config.time_limit is not None:
            if self.elapsed_time >= self.config.time_limit:
                self.finish_game(success=False)
                return

        self.update_info_label()

    def update_info_label(self):
        self.info_label.text = self.rules.get_status_text(self.elapsed_time)

    def check_number(self, button):
        if not button.text:
            return

        selected_number = int(button.text)

        if self.rules.is_correct(selected_number):
            if not self.has_started:
                self.has_started = True
                self.start_timer()

            button.animate_tap()
            self.correct_animation(button)
            self.rules.register_correct_tap()

            if self.rules.completed:
                self.finish_game(success=True)
            else:
                self.info_label.color = ColorPalette.MUTED_TEXT
                self.update_info_label()
        else:
            self.rules.register_wrong_tap()
            self.wrong_animation(button)

            if self.rules.has_lost():
                self.finish_game(success=False)
            else:
                self.info_label.text = f"Wrong! Find {self.rules.expected_number}"
                self.info_label.color = (1, 0.45, 0.45, 1)

    def correct_animation(self, button):
        button.disabled = True

        animation = Animation(
            opacity=0.15,
            background_color=(0.20, 0.22, 0.28, 1),
            duration=0.18,
        )
        animation.bind(on_complete=lambda *_: setattr(button, "text", ""))
        animation.start(button)

    def wrong_animation(self, button):
        original_color = button.background_color

        animation = (
            Animation(background_color=(1, 0.12, 0.12, 1), duration=0.08)
            + Animation(background_color=original_color, duration=0.12)
        )
        animation.start(button)

    def finish_game(self, success: bool):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None

        app = App.get_running_app()
        app.result_screen.show_result(
            config=self.config,
            elapsed_time=self.elapsed_time,
            mistakes=self.rules.mistakes,
            success=success,
        )
        app.root.current = "result"

    def go_to_menu(self, button):
        button.animate_tap()

        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None

        App.get_running_app().root.current = "menu"