from dataclasses import dataclass

from core.game_config import GameConfig


@dataclass(frozen=True)
class RewardResult:
    xp: int
    coins: int
    stars: int
    messages: list[str]


class RewardService:
    """
    Responsible only for calculating rewards.
    This follows Single Responsibility.
    """

    BASE_LEVEL_XP = 50
    TARGET_TIME_BONUS_XP = 25
    NO_MISTAKE_BONUS_XP = 20

    BASE_LEVEL_COINS = 10
    TARGET_TIME_BONUS_COINS = 5
    NO_MISTAKE_BONUS_COINS = 5

    def calculate_rewards(
        self,
        config: GameConfig,
        elapsed_time: float,
        mistakes: int,
        success: bool,
    ) -> RewardResult:
        if not success:
            return RewardResult(
                xp=5,
                coins=0,
                stars=0,
                messages=["Try again reward: +5 XP"],
            )

        xp = self.BASE_LEVEL_XP
        coins = self.BASE_LEVEL_COINS
        stars = 1
        messages = ["Level complete: +50 XP, +10 coins"]

        if config.target_time is not None and elapsed_time <= config.target_time:
            xp += self.TARGET_TIME_BONUS_XP
            coins += self.TARGET_TIME_BONUS_COINS
            stars += 1
            messages.append("Target time bonus: +25 XP, +5 coins")

        if mistakes == 0:
            xp += self.NO_MISTAKE_BONUS_XP
            coins += self.NO_MISTAKE_BONUS_COINS
            stars += 1
            messages.append("Perfect bonus: +20 XP, +5 coins")

        stars = min(stars, 3)

        return RewardResult(
            xp=xp,
            coins=coins,
            stars=stars,
            messages=messages,
        )