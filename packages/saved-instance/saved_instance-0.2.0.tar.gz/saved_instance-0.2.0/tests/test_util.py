import os
from pathlib import Path
from saved_instance.utils import get_app_storage, search_user_defined_config_file, get_config_data
from saved_instance.config import load_yml, ConfigData, set_config


def test_get_app_storage():
    path = get_app_storage("test", ".test")
    assert str(Path(".local", "share")) in str(path)


def test_search_user_defined_config_file():
    os.chdir("temp")
    search_user_defined_config_file()

def test_config_load():
    config_data:ConfigData = load_yml(Path("../", ".config_svd.yml"))
    print(config_data.project.name)

def test_get_config_data():
    set_config(True)
    config: ConfigData = get_config_data()
    print(config.storage.path)