import os
import threading
import time

from libs import uicontrol
from libs import render
from libs import config

_MAX_LINES = 1000
loggers = {}
_level_map = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}
_print_lock = threading.Lock()

os.makedirs("./logs", exist_ok=True)
with open("./logs/latest.log", "w", encoding="utf-8") as f:
    pass

logger_cfg = config.cfg("core/logger.json")
time_cfg = config.cfg("core/render.json")
_time_format = time_cfg.get("settings", {}).get("time_format", "%Y-%m-%d %H:%M:%S")


class Logger:
    def __init__(self, name):
        self.name = name
        self.disabled = False
        self.level = logger_cfg.get("LEVEL") or "INFO"
        self.log_level = logger_cfg.get("LOG_LEVEL") or self.level
        self.formats = logger_cfg.get("FORMATS", "/TIME/[/LEVEL/]</NAME/>:/TEXT/")

    def set_level(self, level):
        self.level = level.upper()

    def _make_template(self, text, level):
        return {
            "/NAME/": self.name,
            "/TEXT/": text,
            "/LEVEL/": level,
            "/TIME/": time.strftime(_time_format),
            "/LINE/": str(get_line()),
        }

    def debug(self, *args):
        self._log("DEBUG", " ".join(args))

    def info(self, *args):
        self._log("INFO", " ".join(args))

    def warning(self, *args):
        self._log("WARNING", " ".join(args))

    def error(self, *args):
        self._log("ERROR", " ".join(args))

    def write(self, text, level):
        if _level_map[level] >= _level_map[self.log_level] and not self.disabled:
            log_dir = "./logs"
            os.makedirs(log_dir, exist_ok=True)
            with open(os.path.join(log_dir, f"{time.strftime('%Y-%m-%d')}.log"), "a+", encoding="utf-8") as f:
                f.write(text + "\n")
            with open(os.path.join(log_dir, "latest.log"), "a+", encoding="utf-8") as f:
                f.write(text + "\n")

    def _log(self, level, text):
        if _level_map[level] >= _level_map[self.level] and not self.disabled:
            template = self._make_template(text, level)
            rendered = render.shader(self.formats, template)
            raw_print(rendered)
            self.write(rendered, level)


def raw_print(text, new_line=True):
    with _print_lock:
        buffer = uicontrol.output_buffer
        buffer.cursor_position = len(buffer.text)
        buffer.insert_text(text)
        if new_line:
            buffer.newline()
        _trim_buffer()
        uicontrol.app_refresh()


def get_logger(name):
    if name in loggers:
        return loggers[name]
    loggers[name] = Logger(name)
    return loggers[name]


def get_line():
    return uicontrol.output_buffer.text.count("\n") + 1


def _trim_buffer():
    buffer = uicontrol.output_buffer
    line_count = buffer.text.count("\n")
    if line_count > _MAX_LINES:
        excess = line_count - _MAX_LINES
        i = 0
        for _ in range(excess):
            i = buffer.text.index("\n", i) + 1
        buffer.text = buffer.text[i:]
