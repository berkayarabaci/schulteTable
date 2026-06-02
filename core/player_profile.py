from dataclasses import dataclass, field


@dataclass
class LevelProgress:
    level_number: int
    stars: int = 0
    best_time: float | None = None
    best_mistakes: int | None = None


@dataclass
class PlayerProfile:
    name: str = "Player"
    xp: int = 0
    coins: int = 0
    total_games_played: int = 0
    total_completed_levels: int = 0
    highest_unlocked_level: int = 1
    completed_levels: list[int] = field(default_factory=list)
    level_progress: dict[str, LevelProgress] = field(default_factory=dict)
    best_mode_scores: dict[str, dict] = field(default_factory=dict)

    @property
    def player_level(self) -> int:
        """
        Simple XP level formula.
        Level 1: 0 XP
        Level 2: 100 XP
        Level 3: 200 XP
        etc.
        """
        return max(1, self.xp // 100 + 1)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "xp": self.xp,
            "coins": self.coins,
            "player_level": self.player_level,
            "total_games_played": self.total_games_played,
            "total_completed_levels": self.total_completed_levels,
            "highest_unlocked_level": self.highest_unlocked_level,
            "completed_levels": self.completed_levels,
            "level_progress": {
                key: {
                    "level_number": value.level_number,
                    "stars": value.stars,
                    "best_time": value.best_time,
                    "best_mistakes": value.best_mistakes,
                }
                for key, value in self.level_progress.items()
            },
            "best_mode_scores": self.best_mode_scores,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PlayerProfile":
        level_progress = {}

        for key, value in data.get("level_progress", {}).items():
            level_progress[key] = LevelProgress(
                level_number=value["level_number"],
                stars=value.get("stars", 0),
                best_time=value.get("best_time"),
                best_mistakes=value.get("best_mistakes"),
            )

        return cls(
            name=data.get("name", "Player"),
            xp=data.get("xp", 0),
            coins=data.get("coins", 0),
            total_games_played=data.get("total_games_played", 0),
            total_completed_levels=data.get("total_completed_levels", 0),
            highest_unlocked_level=data.get("highest_unlocked_level", 1),
            completed_levels=data.get("completed_levels", []),
            level_progress=level_progress,
            best_mode_scores=data.get("best_mode_scores", {}),
        )