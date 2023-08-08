from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    """deals with ,movie app generic data"""

    @abstractmethod
    def get_all_users(self) -> dict:

        pass

    @abstractmethod
    def get_user_movies(self, user_id) -> dict:
        pass
