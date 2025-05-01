from typing import override, overload

from .base_storage import BaseStorage
from .db import BaseRepo

class SimpleStorage(BaseStorage):

    """
    SimpleStorage is implementation BaseStorage which is interface of dictionary.

    param
        db_repo: BaseRepo type object like a ShelveRepo or SqliteRepo.

    """

    def __init__(self, db_repo: BaseRepo):
        self.db_repo: BaseRepo = db_repo

    def get(self, key: str):
        value = self.db_repo.read(key)
        return value

    def set(self, key: str, value):
        value = self.db_repo.write(key, value)
        return value

    def remove(self, key: str) -> None:
        self.db_repo.delete(key)

    def _get_all(self):
        yield from self.db_repo.read_all()

    def _len(self):
        return len(self.db_repo.count())


