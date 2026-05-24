from core.game_config import GameConfig, GameMode


class GameRules:
    """
    Handles the rules for one game session.
    Single responsibility: decide what number is expected,
    whether taps are correct, and whether the game is over.
    """

    def __init__(self, config: GameConfig):
        self.config = config
        self.mistakes = 0
        self.remaining_lives = config.lives
        self.completed = False

        if config.mode == GameMode.REVERSE:
            self.expected_number = config.max_number
        else:
            self.expected_number = 1

    def is_correct(self, number: int) -> bool:
        return number == self.expected_number

    def register_correct_tap(self) -> None:
        if self.config.mode == GameMode.REVERSE:
            if self.expected_number <= 1:
                self.completed = True
            else:
                self.expected_number -= 1
        else:
            if self.expected_number >= self.config.max_number:
                self.completed = True
            else:
                self.expected_number += 1

    def register_wrong_tap(self) -> None:
        self.mistakes += 1

        if self.config.mode == GameMode.LIVES and self.remaining_lives is not None:
            self.remaining_lives -= 1

    def has_lost(self) -> bool:
        return (
            self.config.mode == GameMode.LIVES
            and self.remaining_lives is not None
            and self.remaining_lives <= 0
        )

    def get_start_message(self) -> str:
        if self.config.mode == GameMode.REVERSE:
            return f"Tap {self.config.max_number} to start"
        return "Tap 1 to start"

    def get_status_text(self, elapsed_time: float) -> str:
        parts = [
            f"Next: {self.expected_number}",
            f"Time: {elapsed_time:.1f}s",
            f"Mistakes: {self.mistakes}",
        ]

        if self.config.mode == GameMode.LIVES:
            parts.append(f"Lives: {self.remaining_lives}")

        if self.config.mode == GameMode.COUNTDOWN and self.config.time_limit is not None:
            remaining = max(0, self.config.time_limit - elapsed_time)
            parts.append(f"Left: {remaining:.1f}s")

        return "   ".join(parts)