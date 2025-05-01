import subprocess
from collections.abc import Callable
from typing import Literal

from collection_sync import ReadWriteCollection
from collection_sync.util import identity_func


class IPRoute(ReadWriteCollection):
    def __init__(
        self,
        dev: str | None = None,
        table: str | None = None,
    ):
        self.dev = dev
        self.table = table

    def __iter__(self):
        cmd = 'ip route show'
        if self.dev:
            cmd += f' dev {self.dev}'
        if self.table:
            cmd += f' table {self.table}'
        for line in subprocess.check_output(cmd, shell=True, text=True).splitlines():
            yield line.strip()

    def add(self, item: str) -> None:
        subprocess.run(self.build_cmd('add', item, self.dev, self.table), shell=True, check=True)

    def add_batch(self, items: list[str]) -> None:
        cmd = '; '.join(self.build_cmd('add', item, self.dev, self.table) for item in items)
        subprocess.check_call(cmd, shell=True)

    def delete_by_key(self, key: str, key_func: Callable = identity_func) -> None:
        for item in self:
            if key_func(item) == key:
                subprocess.run(self.build_cmd('del', item, self.dev, self.table), shell=True, check=True)
                break

    def delete_by_key_batch(self, keys: list[str], key_func: Callable = identity_func) -> None:
        _keys_set = set(keys)
        _items = [item for item in self if key_func(item) in _keys_set]
        cmd = '; '.join(self.build_cmd('del', item, self.dev, self.table) for item in _items)
        subprocess.check_call(cmd, shell=True)

    @staticmethod
    def build_cmd(
        action: Literal['add', 'del'],
        route: str,
        dev: str | None = None,
        table: str | None = None,
    ) -> str:
        cmd = f'ip route {action} {route}'
        if dev:
            cmd += f' dev {dev}'
        if table:
            cmd += f' table {table}'
        return cmd
