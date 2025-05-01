import pickle
import sqlite3
from pathlib import Path

from saved_instance.db import BaseRepo

class SqliteRepo(BaseRepo):

    """

    SqliteRepo is implementation of Base Repo.

    param
        path: path of storage file.
        lock: accept thread or process lock, default is None.

    sqlite is used for storing the data.

    """

    def __init__(self, path: Path, lock=None):
        self.path: Path = path.with_suffix(".svd")
        self.lock = lock
        self.__init_db()

    def __init_db(self):
        with sqlite3.connect(self.path, timeout=5) as conn:
            conn.execute('''
            CREATE TABLE IF NOT EXISTS store (
                key TEXT PRIMARY KEY,
                value Text
            )
            ''')

    def read(self, key):
        with sqlite3.connect(self.path) as conn:
            cur = conn.execute('SELECT value FROM store WHERE key = ?', (key,))
            row = cur.fetchone()
            if row:
                return pickle.loads(row[0])
            else:
                return None

    def write(self, key: str, _value):
        value = pickle.dumps(_value)
        if self.lock is None:
            self._write(key, value)
        else:
            with self.lock:
                self._write(key, value)
        return _value

    def _write(self, key: str, value):
        with sqlite3.connect(self.path, timeout=5) as conn:
            conn.execute('REPLACE INTO store (key, value) VALUES (?, ?)',
                         (key, value))
    def delete(self, key):
        if self.lock is None:
            self._delete(key)
        else:
            with self.lock:
                self._delete(key)

    def _delete(self, key):
        with sqlite3.connect(self.path) as conn:
            conn.execute('DELETE FROM store WHERE key = ?', (key,))

    def read_all(self):
        with sqlite3.connect(self.path) as conn:
            cur = conn.execute('SELECT key, value FROM store')
            for key, value in cur:
                yield key

    def count(self):
        with sqlite3.connect(self.path) as conn:
            cur = conn.execute('SELECT COUNT(*) from store')
            return cur.fetchone()[0]