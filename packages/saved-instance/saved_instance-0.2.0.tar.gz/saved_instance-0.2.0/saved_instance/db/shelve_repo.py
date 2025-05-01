import shelve
from pathlib import Path
from .base_repo import BaseRepo

class ShelveRepo(BaseRepo):

    """

    ShelveRepo is implementation of Base Repo.

    :param path: path of storage file.

    shelve is used for storing the data.

    """

    def __init__(self, path: Path):
        self.db_name: Path = path

    def read(self, key):
        try:
            with shelve.open(self.db_name) as db:
                return db[key]
        except KeyError:
            return None

    def write(self, key, value):
        with shelve.open(self.db_name) as db:
            db[key] = value
        return value

    def delete(self, key):
        with shelve.open(self.db_name) as db:
            del db[key]

    def read_all(self):
        with shelve.open(self.db_name) as db:
            yield from db.keys()

    def count(self):
        with shelve.open(self.db_name) as db:
            return len(db)