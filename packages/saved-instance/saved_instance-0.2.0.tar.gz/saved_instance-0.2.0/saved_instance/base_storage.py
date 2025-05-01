from abc import ABC, abstractmethod
from collections.abc import MutableMapping

__all__ = ['BaseStorage']

class BaseStorage(ABC, MutableMapping):

    """
    Abstract class for dictionary storage.

    override the mutable mapping abstract class.

    """

    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def set(self, key: str, value):
        pass

    @abstractmethod
    def remove(self, key: str):
        pass

    @abstractmethod
    def _get_all(self):
        pass

    @abstractmethod
    def _len(self):
        pass

    def __getitem__(self, key, /):
        return self.get(key)

    def __setitem__(self, key, value, /):
        self.set(key, value)

    def __delitem__(self, key, /):
        self.remove(key)

    def __iter__(self):
        yield from self._get_all()

    def __len__(self):
        self._len()

