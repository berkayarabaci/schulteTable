from dataclasses import dataclass
from enum import Enum


class GameMode(str, Enum):
    CLASSIC = "classic"
    COUNTDOWN = "countdown"
    REVERSE = "reverse"
    LIVES = "lives"


@dataclass(frozen=True)
class GameConfig:
    grid_size: int
    mode: GameMode
    level_number: int | None = None
    time_limit: float | None = None
    lives: int | None = None
    target_time: float | None = None

    @property
    def max_number(self) -> int:
        return self.grid_size * self.grid_size

    @property
    def title(self) -> str:
        mode_name = self.mode.value.capitalize()
        if self.level_number is not None:
            return f"Level {self.level_number} - {mode_name}"
        return f"{mode_name} {self.grid_size} x {self.grid_size}"