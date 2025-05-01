from .config_data import ConfigData, load_yml

APP_NAME = "saved_instance"
APP_DIR_NAME = "SavedInstance"
DEFAULT_STORAGE_NAME = ".global"

local_config_file_path = None
load_local_config = True

def set_config(enable=False):
    global load_local_config
    load_local_config = enable

def get_config():
    return load_local_config

