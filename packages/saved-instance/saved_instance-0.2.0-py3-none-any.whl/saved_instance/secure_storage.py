import json
import pickle
from collections import abc
from typing import Any

from cryptography.fernet import Fernet
from saved_instance.base_storage import BaseStorage
from saved_instance.db import BaseRepo


class SecureStorage(BaseStorage):

    """
    SecureStorage is implementation BaseStorage which is interface of dictionary.

    param
        db_repo: BaseRepo type object like a ShelveRepo or SqliteRepo.
        fernet: Fernet object
        auto_decrypt: True for automatically decrypt the data while retrieve. Default is False.

        if still want decrypt data even when auto decrypt is False use decrypt method.

    """

    def __init__(self, db_repo: BaseRepo, fernet: Fernet, auto_decrypt=False):
        self.db_repo: BaseRepo = db_repo
        self.fernet: Fernet = fernet
        self.auto_decrypt: bool = auto_decrypt

    def get(self, key: str):
            if self.auto_decrypt:
                _value = self.decrypt(key)
                return _value
            else:
                return self.db_repo.read(key)

    def set(self, key: str, value):
        pickle_data = pickle.dumps(value)
        _value = self.fernet.encrypt(pickle_data)
        value = self.db_repo.write(key, _value)
        return value

    def remove(self, key: str) -> None:
        self.db_repo.delete(key)

    def _get_all(self):
        yield from self.db_repo.read_all()

    def _len(self):
        return len(self.db_repo.count())

    def enable_auto_decrypt(self):
        self.auto_decrypt = True

    def disable_auto_decrypt(self):
        self.auto_decrypt = False

    def decrypt(self, key: str) -> Any:
        value = self.db_repo.read(key)
        if value is None:
            raise KeyError("Key not found")
        return pickle.loads(
            self.fernet.decrypt(value)
        )


