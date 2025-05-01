import pickle
from pathlib import Path
from cryptography.fernet import Fernet

from saved_instance.db.shelve_repo import ShelveRepo
from saved_instance.secure_storage import SecureStorage


def test_secure_storage():
    key = "X3EsCRrNgp9zH2nUud7aiHtJUau87BFBFhi7XgfzpPE="
    repo: ShelveRepo = ShelveRepo(Path("TestProject"))
    fernet = Fernet(key)
    ss = SecureStorage(repo, fernet, auto_decrypt=True)
    ss["1"] = [1]
    ss["1"].append(2)
    ss.disable_auto_decrypt()
    print(ss["1"])
    print(ss.decrypt("2"))