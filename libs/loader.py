import importlib
import os
import sys
import traceback

from libs import logger

_log = logger.get_logger("loader")


def load_plugins():
    for entry in sorted(os.listdir("./plugins")):
        full = os.path.join("./plugins", entry)
        name = os.path.splitext(entry)[0]
        try:
            if name == "__init__":
                continue
            if entry.endswith(".py") or os.path.isfile(os.path.join(full, "__init__.py")):
                _log.debug(f"loading {entry} ...")
                importlib.import_module("plugins." + name)
                _log.debug(f"loaded {entry}")
        except Exception:
            _log.error(f"failed to load {entry}\n{traceback.format_exc()}")


def load_plugin(plugin):
    try:
        importlib.import_module("plugins." + plugin)
    except Exception:
        _log.error(f"failed to load {plugin}\n{traceback.format_exc()}")


def unload_plugin(plugin):
    prefix = "plugins." + plugin
    keys = [k for k in list(sys.modules) if k == prefix or k.startswith(prefix + ".")]
    for k in keys:
        del sys.modules[k]


def reload_plugin(plugin):
    unload_plugin(plugin)
    load_plugin(plugin)


def get_plugin(plugin):
    return importlib.import_module("plugins." + plugin)
