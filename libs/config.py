import json
import os


class cfg:
    def __init__(self, path):
        path = "./config/" + path
        self.path = path
        if os.path.exists(path):
            if os.path.isdir(path):
                self.folder = path
                self.file = None
            else:
                self.file = path
                self.folder = os.path.dirname(path)
        else:
            if path.endswith("/") or path.endswith("\\"):
                os.mkdir(path)
                self.folder = path
                self.file = None
            else:
                self.file = path
                self.folder = os.path.dirname(path)

    def _read(self):
        if not self.file or not os.path.isfile(self.file):
            return {}
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                content = f.read()
                if not content.strip():
                    return {}
                return json.loads(content)
        except (json.JSONDecodeError, OSError):
            return {}

    def _write(self, data):
        if not self.file:
            return
        try:
            with open(self.file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError:
            pass

    def set(self, key, value):
        if self.file:
            data = self._read()
            data[key] = value
            self._write(data)

    def get(self, key="", default=None):
        if self.file:
            data = self._read()
            if key:
                return data.get(key, default)
            return data

    def delete(self, key):
        if self.file:
            data = self._read()
            if key in data:
                del data[key]
            self._write(data)
