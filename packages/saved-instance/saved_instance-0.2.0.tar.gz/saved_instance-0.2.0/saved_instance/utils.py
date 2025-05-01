from pathlib import Path
from platformdirs import user_data_path
from saved_instance.config import APP_DIR_NAME, ConfigData, get_config, load_yml, APP_NAME, DEFAULT_STORAGE_NAME


def get_app_storage(app_name: str, file_name: str) -> Path:
    data_dir = user_data_path(APP_DIR_NAME, ensure_exists=True)
    data_path = data_dir / app_name
    try:
        data_path.mkdir(parents=True, exist_ok=True)
        test_file = data_dir / ".write_test"
        test_file.touch()
        test_file.unlink()
        return data_path / file_name
    except (PermissionError, OSError):
        """ 
        create resource folder in current directory if permission error occurred.
        fall back strategy
        """
        fall_back_dir = Path.cwd() / "resource"
        print(f"WARNING: Using fall back location {fall_back_dir} "
              f"due to permission issue"
              )
        return fall_back_dir / file_name

def search_user_defined_config_file():
    file_to_search = ".config_svd.yml"
    current_dir = Path.cwd()
    return file_search(current_dir, file_to_search)

def file_search(path: Path, file_name: str):
    file_path: Path = path / file_name
    if path == path.parent:
        return None
    elif file_path.exists():
        return file_path
    else:
        return file_search(path.parent, file_name)

def get_config_data() -> ConfigData:
    if get_config():
        config_file_path: Path = search_user_defined_config_file()
        config_data: ConfigData = load_yml(config_file_path)
        app_path = get_app_storage(config_data.project.name, config_data.storage.name)
        if config_data.storage.path == "Default":
            config_data.storage.path = app_path
        return config_data
    else:
        default_data = {
            "project" : {
                "name": APP_NAME
            },
            "storage": {
                "name": DEFAULT_STORAGE_NAME,
                "path": get_app_storage(APP_NAME, DEFAULT_STORAGE_NAME)
            }
        }
        return ConfigData(default_data)


