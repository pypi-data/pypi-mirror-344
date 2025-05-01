from collections.abc import Callable
from typing import Any

import yaml

from collection_sync import ReadWriteCollection
from collection_sync.collections.list import List
from collection_sync.util import identity_func


class YamlList(ReadWriteCollection):
    def __init__(self, file: str):
        self.file = file
        with open(file) as f:
            data: list[dict] = yaml.safe_load(f)
        self.data_list_collection = List(data)

    def write_to_file(self):
        with open(self.file, 'w') as f:
            yaml.dump(self.data, f, allow_unicode=True)

    def __iter__(self):
        return iter(self.data_list_collection)

    def create(self, create_data: dict):
        self.data_list_collection.create(create_data)
        self.write_to_file()

    def delete_by_key(self, key: Any, key_func: Callable = identity_func):
        self.data_list_collection.delete_by_key(key, key_func)
        self.write_to_file()
