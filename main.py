from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import FadeTransition, ScreenManager

from screens.game_screen import GameScreen
from screens.levels_screen import LevelsScreen
from screens.menu_screen import MenuScreen
from screens.mode_screen import ModeScreen
from screens.result_screen import ResultScreen
from ui.widgets import ColorPalette


class SchulteApp(App):
    def build(self):
        self.title = "Schulte Table"
        Window.clearcolor = ColorPalette.BACKGROUND

        manager = ScreenManager(
            transition=FadeTransition(duration=0.25)
        )

        self.menu_screen = MenuScreen(name="menu")
        self.mode_screen = ModeScreen(name="modes")
        self.levels_screen = LevelsScreen(name="levels")
        self.game_screen = GameScreen(name="game")
        self.result_screen = ResultScreen(name="result")

        manager.add_widget(self.menu_screen)
        manager.add_widget(self.mode_screen)
        manager.add_widget(self.levels_screen)
        manager.add_widget(self.game_screen)
        manager.add_widget(self.result_screen)

        return manager


if __name__ == "__main__":
    SchulteApp().run()