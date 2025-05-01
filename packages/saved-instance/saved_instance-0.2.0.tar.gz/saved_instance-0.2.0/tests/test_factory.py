from saved_instance import SimpleStorage, simple_storage, SecureStorage, secure_storage, rich_storage


def test_simple_storage_factory():
    ss: SimpleStorage = simple_storage()
    print(ss.get("is_on"))


def test_secure_storage_factory():
    se: SecureStorage = secure_storage()
    se["msg"] = "he"
    print(se["msg"])

def test_rich_storage_factory():
    rs = rich_storage()
    print("a")
