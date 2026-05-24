import json
from pathlib import Path


class LocalStorage:
    """
    Handles local progress.
    Later, cloud storage can implement the same style of methods.
    """

    def __init__(self, filename: str = "progress.json"):
        self.path = Path(filename)

    def load(self) -> dict:
        if not self.path.exists():
            return {
                "highest_unlocked_level": 1,
                "completed_levels": [],
                "best_scores": {},
            }

        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {
                "highest_unlocked_level": 1,
                "completed_levels": [],
                "best_scores": {},
            }

    def save(self, data: dict) -> None:
        self.path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

    def complete_level(self, level_number: int, elapsed_time: float, mistakes: int) -> None:
        data = self.load()

        completed = set(data.get("completed_levels", []))
        completed.add(level_number)
        data["completed_levels"] = sorted(completed)

        current_highest = data.get("highest_unlocked_level", 1)
        data["highest_unlocked_level"] = max(current_highest, level_number + 1)

        score_key = f"level_{level_number}"
        best_scores = data.setdefault("best_scores", {})

        previous = best_scores.get(score_key)

        new_score = {
            "time": round(elapsed_time, 2),
            "mistakes": mistakes,
        }

        if previous is None or elapsed_time < previous["time"]:
            best_scores[score_key] = new_score

        self.save(data)