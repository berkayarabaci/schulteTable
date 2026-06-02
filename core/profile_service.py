from core.player_profile import PlayerProfile
from core.storage import LocalStorage


class ProfileService:
    """
    Handles profile-related actions.

    The UI should not directly know how to rename, reset,
    or update the player profile.
    """

    def __init__(self, storage: LocalStorage):
        self.storage = storage

    def get_profile(self) -> PlayerProfile:
        return self.storage.load_profile()

    def update_player_name(self, new_name: str) -> PlayerProfile:
        clean_name = new_name.strip()

        if not clean_name:
            clean_name = "Player"

        if len(clean_name) > 20:
            clean_name = clean_name[:20]

        profile = self.storage.load_profile()
        profile.name = clean_name
        self.storage.save_profile(profile)

        return profile

    def reset_progress(self) -> PlayerProfile:
        profile = PlayerProfile()
        self.storage.save_profile(profile)
        return profile