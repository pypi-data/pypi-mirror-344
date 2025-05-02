import json
import os
from typing import Any

class Jsonix:
    def __init__(self, path: str):
        self.path = path
        self.data = self._load()
        if not os.path.exists(self.path):
            self._save()

    @classmethod
    def register(cls, path: str):
        return cls(path)

    def _load(self) -> dict:
        if os.path.exists(self.path):
            with open(self.path, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def _save(self):
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def _get_nested(self, path_list: list[str], create_missing=True) -> dict:
        current = self.data
        for key in path_list:
            if create_missing and (key not in current or not isinstance(current[key], dict)):
                current[key] = {}
            current = current.get(key, {})
        return current

    def add(self, path: str, data: Any):
        keys = path.split(',')
        *parents, last = keys
        current = self.data
        for key in parents:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]
        if isinstance(current.get(last), dict) and isinstance(data, dict):
            current[last].update(data)
        else:
            current[last] = data
        self._save()

    def remove(self, path: str):
        keys = path.split(',')
        *parents, last = keys
        current = self.data
        for key in parents:
            current = current.get(key)
            if current is None or not isinstance(current, dict):
                return  # path doesn't exist
        if last in current:
            del current[last]
            self._save()

    def get(self, path: str) -> Any:
        keys = path.split(',')
        current = self.data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        return current

    def change(self, path: str, data: Any):
        keys = path.split(',')
        *parents, last = keys
        current = self._get_nested(parents, create_missing=False)
        if isinstance(current, dict) and last in current:
            current[last] = data
            self._save()

    def show(self) -> dict:
        return self.data

    def clear(self):
        self.data = {}
        self._save()

jsonix = Jsonix
