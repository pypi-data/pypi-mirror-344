import copy
from collections.abc import Mapping
from pathlib import Path
from collections import abc
import yaml

class ConfigData:

    """

    Config Data class will convert dict to object so key can access via object attribute.

    Used for converting config yml file to python object.

    Example:
        config = ConfigData({"debug" : True})

        print(config.debug)

    """

    def __init__(self, mapping):
        self.__data = dict(mapping)

    @property
    def data(self):
        return self.__data

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        """Retrieve attributes dynamically"""
        if name in self.__data:
            value = self.__data[name]
            if isinstance(value, Mapping):
                # Return same object for updates to work
                nested_obj = ConfigData(value)
                super().__setattr__(name, nested_obj)  # Store as attribute
                return nested_obj
            elif isinstance(value, list):
                return [ConfigData.build(item) for item in value]
            return value
        return None

    def __setattr__(self, key, value):
        if key == "_ConfigData__data":
            super().__setattr__(key, value)
        else:
            if key in self.__data and isinstance(self.data[key], (abc.Mapping, abc.MutableSequence)):
                self.__data[key] = ConfigData.build(value)
            else:
                self.__data[key] =  value

    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj

def load_yml(file_path: Path) -> ConfigData:
    with open(file_path, "r") as fp:
        config = yaml.safe_load(fp)
    return ConfigData.build(config)

