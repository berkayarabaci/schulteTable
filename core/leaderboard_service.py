from core.player_profile import PlayerProfile


class LeaderboardService:
    """
    Responsible only for preparing leaderboard data from profile data.
    UI screens should not know how scores are sorted/formatted internally.
    """

    def get_best_mode_scores(self, profile: PlayerProfile) -> list[dict]:
        scores = []

        for mode_key, score in profile.best_mode_scores.items():
            scores.append(
                {
                    "mode_key": mode_key,
                    "display_name": self._format_mode_name(mode_key),
                    "time": score.get("time"),
                    "mistakes": score.get("mistakes"),
                }
            )

        return sorted(
            scores,
            key=lambda item: (
                item["display_name"],
                item["time"] if item["time"] is not None else 999999,
            ),
        )

    def get_best_level_scores(self, profile: PlayerProfile) -> list[dict]:
        scores = []

        for level_key, progress in profile.level_progress.items():
            scores.append(
                {
                    "level_key": level_key,
                    "level_number": progress.level_number,
                    "stars": progress.stars,
                    "best_time": progress.best_time,
                    "best_mistakes": progress.best_mistakes,
                }
            )

        return sorted(scores, key=lambda item: item["level_number"])

    def _format_mode_name(self, mode_key: str) -> str:
        parts = mode_key.split("_")

        if len(parts) < 2:
            return mode_key.replace("_", " ").title()

        mode = parts[0].capitalize()
        grid = parts[1]

        return f"{mode} {grid}"