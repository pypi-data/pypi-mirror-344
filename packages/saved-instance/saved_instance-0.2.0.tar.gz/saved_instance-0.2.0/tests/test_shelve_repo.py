from pathlib import Path
from saved_instance.db.shelve_repo import ShelveRepo


def test_set():
    shelve_repo = ShelveRepo(Path("saved_instance_global"))
    res = shelve_repo.write("is_on", True)
    assert res is True
    shelve_repo.write("dict_data", {"res": "res", "b": {"1":1}})
    shelve_repo.write("list_data", [1])


def test_get():
    shelve_repo = ShelveRepo(Path("saved_instance_global"))
    res_get = shelve_repo.read("dict_data")
    res_get["res"] = "hey"
    print(shelve_repo.read("dict_data"))