from pathlib import Path

from saved_instance.db.shelve_repo import ShelveRepo
from saved_instance.simple_storage import SimpleStorage


def test_get():
    shelve_repo = ShelveRepo()
    simple_storage = SimpleStorage(shelve_repo)
    res = simple_storage.get("is_on")
    assert res is True

    res = simple_storage["is_on"]
    assert res is True

def test_set():
    simple_storage = SimpleStorage()

    res = simple_storage.set("is_on", False)

    assert res is False

def test_get_set():
    shelve_repo = ShelveRepo(Path("saved_instance_global"))
    simple_storage = SimpleStorage(shelve_repo)
    # simple_storage["dict_data"] = {"1": 1}
    # simple_storage["dict_data"]["2"]["3"]["4"] = 5
    # simple_storage.sync()
    print(simple_storage["dict_data"])
    # simple_storage["list_data"] = [1, 2]
    # simple_storage["list_data"].append(3)
    # simple_storage.sync()
    # print(simple_storage["list_data"])