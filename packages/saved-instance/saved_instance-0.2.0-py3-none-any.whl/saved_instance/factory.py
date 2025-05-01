import threading
from multiprocessing import Manager
from typing import TypeVar, Type
from cryptography.fernet import Fernet
from saved_instance.db.shelve_repo import ShelveRepo
from saved_instance.simple_storage import SimpleStorage
from saved_instance.base_storage import BaseStorage
from saved_instance.config import ConfigData
from saved_instance.db.sqllite_repo import SqliteRepo
from saved_instance.rich_storage import RichStorage
from saved_instance.secure_storage import SecureStorage
from saved_instance.utils import get_config_data

__all__ = ['simple_storage',
           'secure_storage',
           'rich_storage',
           'thread_safe_storage',
           'process_safe_storage'
           ]

T = TypeVar("T", bound=BaseStorage)

_thread_lock = threading.Lock()
_process_lock = None

def init_multiprocess_lock():
    global _process_lock
    if _process_lock is None:
        manager: Manager = Manager()
        _process_lock = manager.Lock()

def get_shared_lock():
    if _process_lock is None:
        init_multiprocess_lock()
    return _process_lock

def simple_storage(thread_safe=False, process_safe=False) -> SimpleStorage:
    """
    factory function for SimpleStorage class

    :return: SimpleStorage
    """
    config_data: ConfigData = get_config_data()
    if thread_safe:
        return thread_safe_storage(SimpleStorage, config_data)
    if process_safe:
        return process_safe_storage(SimpleStorage, config_data)
    repo: ShelveRepo = ShelveRepo(config_data.storage.path)
    return SimpleStorage(repo)

def secure_storage(key = None, auto_decrypt=False) -> SecureStorage:
    """
    factory function for SecureStorage class

    :param key: Secret key for encryption and decryption. Defaults to None and automatically taken from config file,
    or you can pass security key.
    :param auto_decrypt: True for automatically decrypt the data while retrieve. Default is False.
    :return: SecureStorage
    """
    config_data: ConfigData = get_config_data()
    repo: ShelveRepo = ShelveRepo(config_data.storage.path)
    if key is None:
        fernet: Fernet = Fernet(config_data.encrypt.key)
    else:
        fernet: Fernet = Fernet(key)
    return SecureStorage(repo, fernet, auto_decrypt)

def rich_storage(thread_safe=False, process_safe=False) -> RichStorage:
    """
    factory function for RichStorage class
    :return:
    """
    config_data: ConfigData = get_config_data()
    if thread_safe:
        return thread_safe_storage(RichStorage, config_data)
    if process_safe:
        return process_safe_storage(RichStorage, config_data)
    repo: SqliteRepo = SqliteRepo(config_data.storage.path, lock=None)
    return RichStorage(repo)



def thread_safe_storage(storage: Type[T], config_data: ConfigData) -> T:
    """
    factory function for storage with thread safe enable
    :param config_data: Config data object, it has config yml file data
    :param storage: BaseStorage class like with type T
    :return: storage
    """
    repo: SqliteRepo = SqliteRepo(config_data.storage.path, lock=_thread_lock)
    return storage(repo)



def process_safe_storage(storage: Type[T], config_data: ConfigData) -> T:
    """
    factory function for storage with process safe enable
    :param config_data: Config data object, it has config yml file data
    :param storage: BaseStorage class like with type T
    :return: storage
    """
    repo: SqliteRepo = SqliteRepo(config_data.storage.path, lock=get_shared_lock())
    return storage(repo)
