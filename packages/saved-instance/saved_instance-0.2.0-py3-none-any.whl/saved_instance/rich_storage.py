import collections
from .base_storage import BaseStorage
from .db import BaseRepo


class ProxyList(collections.UserList):
    """
    Proxy List class is list and subclass of list.
    helping to track nested list changes in RichStorage Class
    __init__,__getitem__, __setitem__, append are override methods.
    __getitem__ method to keep track of parent list data for nested list.
    __setitem__ method to store latest changes of nested list data.
    """
    def __init__(self, *args, parent_key=None,parent_obj=None,root_parent_key=None, repo_write_function=None, **kwargs):
        self.repo_write_callback = repo_write_function
        self.parent_key = parent_key
        self.parent_obj = parent_obj
        self.root_parent = root_parent_key
        temp = []
        for item in args[0]:
            if isinstance(item, dict):
                temp.append(ProxyMapping(item, root_parent_key=self.root_parent, repo_write_function=self.repo_write_callback))
            else:
                temp.append(item)
        super().__init__(temp)

    def __getitem__(self, item):
        val = super().__getitem__(item)
        if isinstance(val, ProxyMapping):
            val.parent_obj = self.parent_obj
            val.parent_key = self.parent_key
            val.repo_write_callback = self.repo_write_callback
        return val

    def append(self, item):
        if isinstance(item, collections.abc.MutableMapping):
            item = ProxyMapping(item, repo_write_function=self.repo_write_callback)
        if isinstance(item, list):
            item = ProxyList(item, repo_write_function=self.repo_write_callback)
        super().append(item)
        if self.root_parent is not None and self.repo_write_callback and self.parent_obj:
            self.repo_write_callback(self.root_parent, self.parent_obj)
            del self.parent_obj
            return None
        elif self.root_parent and self.repo_write_callback:
            self.repo_write_callback(self.root_parent, self)
            del self
            return None
        return None

    def __setitem__(self, index, value):
        if isinstance(value, collections.abc.MutableMapping):
            value = ProxyMapping(value, repo_write_function=self.repo_write_callback)
        if isinstance(value, list):
            value = ProxyList(value, repo_write_function=self.repo_write_callback)
        super().__setitem__(index, value)
        if self.root_parent is not None and self.repo_write_callback and self.parent_obj:
            self.repo_write_callback(self.root_parent, self.parent_obj)
            del self.parent_obj
            return None
        elif self.root_parent and self.repo_write_callback:
            self.repo_write_callback(self.root_parent, self)
            del self
            return None
        return None


class ProxyMapping(collections.UserDict):
    """
    Proxy Mapping class is dictionary and subclass of dict.

    helping to track nested dictionary changes in RichStorage Class

    __init__,__getitem__, __setitem__ are override methods.

    __getitem__ method to keep track of parent dictionary data for nested dictionary.

    __setitem__ method to store latest changes of nested dictionary data.

    """
    def __init__(self, *args, parent_key=None,parent_obj=None,root_parent_key=None, repo_write_function=None, **kwargs):
        self.repo_write_callback = repo_write_function
        self.parent_key = parent_key
        self.parent_obj = parent_obj
        self.root_parent = root_parent_key
        super().__init__(*args, **kwargs)

    def __getitem__(self, item):
        val = super().__getitem__(item)
        if isinstance(val, ProxyMapping):
            if self.parent_obj is None:
                val.parent_obj = self
            else:
                val.parent_obj = self.parent_obj
            val.parent_key = item
            val.root_parent = self.root_parent
            val.repo_write_callback = self.repo_write_callback
            return val
        if isinstance(val, ProxyList):
            if self.parent_obj is None:
                val.parent_obj = self
            else:
                val.parent_obj = self.parent_obj
            val.parent_key = item
            val.root_parent = self.root_parent
            val.repo_write_callback = self.repo_write_callback
            return val
        else: return val


    def __setitem__(self, key, value):
        if isinstance(value, collections.abc.MutableMapping):
            value = ProxyMapping(value, root_parent_key=self.root_parent, repo_write_function=self.repo_write_callback)
        if isinstance(value, list):
            value = ProxyList(value, root_parent_key=self.root_parent,repo_write_function=self.repo_write_callback, parent_obj=self.parent_obj)
        super().__setitem__(key, value)
        if self.root_parent is not None and self.repo_write_callback and self.parent_obj:
            self.repo_write_callback(self.root_parent, self.parent_obj)
            del self.parent_obj


class RichStorage(BaseStorage):

    """
    RichStorage implementation of BaseStorage.

    this class requires BaseRepo type object as parameter.

    This is initialized with a dictionary like object

    """

    def __init__(self, db_repo: BaseRepo):
        self.db_repo: BaseRepo = db_repo

    def get(self, key: str):
        value = self.db_repo.read(key)
        return value

    def _set(self, key: str, value):
        self.db_repo.write(key, value)
        return value

    def set(self, key, value):
        if isinstance(value, collections.abc.MutableMapping):
            proxy_dict = ProxyMapping(value, repo_write_function=self._set, root_parent_key=key)
            self._set(key, proxy_dict)
            del proxy_dict
        elif isinstance(value, list):
            proxy_list = ProxyList(value,  repo_write_function=self._set, root_parent_key=key)
            self._set(key, proxy_list)
        else:
            self._set(key, value)

    def remove(self, key: str) -> None:
        self.db_repo.delete(key)

    def _get_all(self):
        yield from self.db_repo.read_all()

    def _len(self):
        return self.db_repo.count()

# class RichStorageCache(BaseStorage):
#
#     def __init__(self, db_repo: BaseRepo):
#         self.db_repo: BaseRepo = db_repo
#         self.cache: dict = {}
#
#     def get(self, key: str):
#         try:
#             value = self.cache[key]
#         except KeyError:
#             value = self.db_repo.read(key)
#             self.cache[key] =  value
#         return value
#
#     def set(self, key: str, value):
#         value = self.db_repo.write(key, value)
#         self.cache[key] = value
#         self.sync()
#         return value
#
#     def sync(self):
#         for key, item in self.cache.items():
#             self[key] = item
#         self.cache = {}
#
#     def remove(self, key: str) -> None:
#         self.db_repo.delete(key)
#         del self.cache[key]
#
#     def _get_all(self):
#         yield from self.cache.keys()
#
#     def _len(self):
#         return len(self.cache)
#
#
# class RichStorageThreadSafe(BaseStorage):
#
#     def __init__(self, db_repo: BaseRepo):
#         self.db_repo: BaseRepo = db_repo
#
#     def get(self, key: str):
#         value = self.db_repo.read(key)
#         return value
#
#     def set(self, key: str, value):
#         value = self.db_repo.write(key, value)
#         return value
#
#     def remove(self, key: str) -> None:
#         self.db_repo.delete(key)
#
#     def _get_all(self):
#         yield from self.db_repo.read_all()
#
#     def _len(self):
#         return self.db_repo.count()