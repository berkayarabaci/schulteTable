import json
from pathlib import Path

from core.game_config import GameConfig
from core.player_profile import LevelProgress, PlayerProfile
from core.reward_service import RewardResult
from core.score_service import ScoreService


class LocalStorage:
    """
    Handles local save/load only.
    Later we can create FirebaseStorage with similar methods.
    """

    def __init__(self, filename: str = "progress.json"):
        self.path = Path(filename)
        self.score_service = ScoreService()

    def load_profile(self) -> PlayerProfile:
        if not self.path.exists():
            return PlayerProfile()

        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            return PlayerProfile.from_dict(data)
        except (json.JSONDecodeError, KeyError, TypeError):
            return PlayerProfile()

    def save_profile(self, profile: PlayerProfile) -> None:
        self.path.write_text(
            json.dumps(profile.to_dict(), indent=2),
            encoding="utf-8",
        )

    def register_game_result(
        self,
        config: GameConfig,
        elapsed_time: float,
        mistakes: int,
        success: bool,
        reward: RewardResult,
    ) -> PlayerProfile:
        profile = self.load_profile()

        profile.total_games_played += 1
        profile.xp += reward.xp
        profile.coins += reward.coins

        self._update_mode_score(
            profile=profile,
            config=config,
            elapsed_time=elapsed_time,
            mistakes=mistakes,
            success=success,
        )

        if success and config.level_number is not None:
            self._update_level_progress(
                profile=profile,
                config=config,
                elapsed_time=elapsed_time,
                mistakes=mistakes,
                reward=reward,
            )

        self.save_profile(profile)
        return profile

    def _update_mode_score(
        self,
        profile: PlayerProfile,
        config: GameConfig,
        elapsed_time: float,
        mistakes: int,
        success: bool,
    ) -> None:
        if not success:
            return

        score_key = self.score_service.get_mode_score_key(config)
        current_best = profile.best_mode_scores.get(score_key)

        if self.score_service.is_better_time_score(
            current_best=current_best,
            elapsed_time=elapsed_time,
            mistakes=mistakes,
        ):
            profile.best_mode_scores[score_key] = {
                "time": round(elapsed_time, 2),
                "mistakes": mistakes,
            }

    def _update_level_progress(
        self,
        profile: PlayerProfile,
        config: GameConfig,
        elapsed_time: float,
        mistakes: int,
        reward: RewardResult,
    ) -> None:
        level_number = config.level_number
        if level_number is None:
            return

        level_key = f"level_{level_number}"

        was_already_completed = level_number in profile.completed_levels

        if not was_already_completed:
            profile.completed_levels.append(level_number)
            profile.completed_levels.sort()
            profile.total_completed_levels += 1

        profile.highest_unlocked_level = max(
            profile.highest_unlocked_level,
            level_number + 1,
        )

        previous = profile.level_progress.get(level_key)

        if previous is None:
            profile.level_progress[level_key] = LevelProgress(
                level_number=level_number,
                stars=reward.stars,
                best_time=round(elapsed_time, 2),
                best_mistakes=mistakes,
            )
            return

        previous.stars = max(previous.stars, reward.stars)

        if previous.best_time is None or elapsed_time < previous.best_time:
            previous.best_time = round(elapsed_time, 2)
            previous.best_mistakes = mistakes
        elif elapsed_time == previous.best_time:
            if previous.best_mistakes is None or mistakes < previous.best_mistakes:
                previous.best_mistakes = mistakes

    # Backward-compatible method for current LevelsScreen
    def load(self) -> dict:
        return self.load_profile().to_dict()

    # Backward-compatible method for old ResultScreen code
    def complete_level(self, level_number: int, elapsed_time: float, mistakes: int) -> None:
        profile = self.load_profile()

        if level_number not in profile.completed_levels:
            profile.completed_levels.append(level_number)
            profile.completed_levels.sort()
            profile.total_completed_levels += 1

        profile.highest_unlocked_level = max(
            profile.highest_unlocked_level,
            level_number + 1,
        )

        self.save_profile(profile)