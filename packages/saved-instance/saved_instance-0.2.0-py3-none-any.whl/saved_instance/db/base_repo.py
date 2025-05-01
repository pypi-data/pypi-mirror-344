from abc import ABC, abstractmethod

__all__ = ['BaseRepo']

class BaseRepo(ABC):

    """
    Abstract class for data source repo.
    """

    @abstractmethod
    def read(self, key):
        pass

    @abstractmethod
    def write(self, key, value):
        pass

    @abstractmethod
    def delete(self, key):
        pass

    @abstractmethod
    def read_all(self):
        pass

    @abstractmethod
    def count(self):
        pass