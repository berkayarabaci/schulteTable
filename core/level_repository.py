from core.game_config import GameConfig, GameMode


class LevelRepository:
    """
    Stores level definitions.
    Later we can replace this with a remote Firebase-backed repository.
    """

    def get_levels(self) -> list[GameConfig]:
        return [
            GameConfig(level_number=1, grid_size=3, mode=GameMode.CLASSIC, target_time=10),
            GameConfig(level_number=2, grid_size=3, mode=GameMode.COUNTDOWN, time_limit=20),
            GameConfig(level_number=3, grid_size=3, mode=GameMode.LIVES, lives=3),

            GameConfig(level_number=4, grid_size=4, mode=GameMode.CLASSIC, target_time=22),
            GameConfig(level_number=5, grid_size=4, mode=GameMode.REVERSE, target_time=25),
            GameConfig(level_number=6, grid_size=4, mode=GameMode.COUNTDOWN, time_limit=35),

            GameConfig(level_number=7, grid_size=5, mode=GameMode.CLASSIC, target_time=45),
            GameConfig(level_number=8, grid_size=5, mode=GameMode.LIVES, lives=3),
            GameConfig(level_number=9, grid_size=5, mode=GameMode.REVERSE, target_time=50),

            GameConfig(level_number=10, grid_size=6, mode=GameMode.COUNTDOWN, time_limit=75),
        ]

    def get_level(self, level_number: int) -> GameConfig:
        for level in self.get_levels():
            if level.level_number == level_number:
                return level

        raise ValueError(f"Level {level_number} does not exist.")