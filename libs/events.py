import json
import os
import sys

from libs import config
from libs import logger
from libs import session

_log = logger.get_logger("events")
events = {}


class EventPayload:
    __slots__ = ("log", "cfg", "__dict__")

    def __init__(self, log, cfg):
        self.log = log
        self.cfg = cfg


def _plugin_name(mod):
    meta = getattr(mod, "META", None)
    if isinstance(meta, dict) and "name" in meta:
        return meta["name"]
    f = getattr(mod, "__file__", None)
    if f:
        d = os.path.dirname(f)
        mp = os.path.join(d, "meta.json")
        if os.path.isfile(mp):
            try:
                with open(mp) as fh:
                    data = json.load(fh)
                if "name" in data:
                    return data["name"]
            except (json.JSONDecodeError, OSError):
                pass
    return mod.__name__.rsplit(".", 1)[-1]


def _handler_name(handler):
    mod = sys.modules.get(handler.__module__)
    if mod is None:
        return handler.__module__.rsplit(".", 1)[-1]
    return _plugin_name(mod)


def on_event(event, func=None):
    if func is None:
        def decorator(f):
            if event not in events:
                events[event] = []
            events[event].append(f)
            _log.debug(f"registered handler {f.__name__} for '{event}'")
            return f
        return decorator
    if event not in events:
        events[event] = []
    events[event].append(func)
    _log.debug(f"registered handler {func.__name__} for '{event}'")


def call_event(event, **extras):
    if event not in events:
        return
    _log.debug(f"dispatching '{event}' to {len(events[event])} handlers")
    for handler in events[event]:
        name = _handler_name(handler)
        log = logger.get_logger(name)
        cfg_obj = config.cfg(name + "/")
        payload = EventPayload(log, cfg_obj)
        for k, v in extras.items():
            setattr(payload, k, v)
        bindings = session.get_bindings(name)
        if bindings is not None and extras.get("account") not in bindings:
            continue
        handler(payload)


def reg_event(event, name=None):
    def decorator(func):
        event_name = name if name else func.__name__
        on_event(event_name, func)
        return func
    return decorator
