from core.game_config import GameConfig


class ScoreService:
    """
    Responsible only for creating score keys and comparing scores.
    Later, online leaderboards can reuse this logic.
    """

    def get_mode_score_key(self, config: GameConfig) -> str:
        return f"{config.mode.value}_{config.grid_size}x{config.grid_size}"

    def is_better_time_score(
        self,
        current_best: dict | None,
        elapsed_time: float,
        mistakes: int,
    ) -> bool:
        if current_best is None:
            return True

        current_time = current_best.get("time")

        if current_time is None:
            return True

        if elapsed_time < current_time:
            return True

        if elapsed_time == current_time and mistakes < current_best.get("mistakes", 999):
            return True

        return False