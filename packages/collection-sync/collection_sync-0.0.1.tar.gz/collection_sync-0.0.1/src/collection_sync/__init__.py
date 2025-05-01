__version__ = '0.0.1'

import abc
from collections.abc import Callable
from collections.abc import Iterable
from typing import Any

from collection_sync.util import identity_func


class ReadCollection(Iterable):
    def cache_items(self, key_func: Callable):
        self._cache = {key_func(item): item for item in self}  # pylint: disable=attribute-defined-outside-init

    def delete_cache(self):
        self._cache = None  # pylint: disable=attribute-defined-outside-init

    def contains_key(self, key: Any, key_func: Callable = identity_func) -> bool:
        try:
            self.get_by_key(key, key_func)
        except KeyError:
            return False
        return True

    def get_by_key(self, key: Any, key_func: Callable = identity_func):
        if hasattr(self, '_cache') and self._cache is not None:
            return self._cache[key]
        for x in self:
            if key_func(x) == key:
                return x
        raise KeyError(f'Key {key} not found')


class WriteCollection(abc.ABC):
    @abc.abstractmethod
    def create(self, create_data: Any): ...

    @abc.abstractmethod
    def delete_by_key(self, key: Any, key_func: Callable = identity_func): ...


class ReadWriteCollection(ReadCollection, WriteCollection):
    ...


def sync_collections(
    source: ReadCollection,
    destination: ReadWriteCollection,
    *,
    source_key: Callable = identity_func,
    destination_key: Callable = identity_func,
    source_destination_transform: Callable = identity_func,
    delete_missing: bool = False,
    cache_before_source: bool = True,
    cache_before_destination: bool = True,
    delete_cache_after_source: bool = False,
    delete_cache_after_destination: bool = False,
    dry_run: bool = False,
) -> None:
    """
    delete_missing: bool
        If there are items in the destination that don't exist in the
        source and this is True, delete them. Otherwise, leave them alone.
    """
    if cache_before_source:
        source.cache_items(key_func=source_key)
    if cache_before_destination:
        destination.cache_items(key_func=destination_key)

    for item in source:
        key = source_key(item)
        if not destination.contains_key(key, key_func=destination_key):
            create_data = source_destination_transform(item)
            print(f'CREATE: {create_data}')
            if dry_run:
                continue
            destination.create(create_data)

    if delete_missing:
        for item in destination:
            key = destination_key(item)
            if not source.contains_key(key, key_func=source_key):
                print(f'DELETE {key}')
                if dry_run:
                    continue
                destination.delete_by_key(key, key_func=destination_key)

    if delete_cache_after_source:
        source.delete_cache()
    if delete_cache_after_destination:
        destination.delete_cache()
