import os
import sys

from prompt_toolkit.completion import Completer, Completion
from libs import command, completer, events, loader, logger

META = {
    "name": "PluginMgr",
    "version": "1.0.0",
    "author": "CNlongY",
    "description": "List, load, unload, reload plugins",
}
_LOG = logger.get_logger("PluginMgr")


def _available():
    names = []
    for entry in sorted(os.listdir("./plugins")):
        name = os.path.splitext(entry)[0]
        if name == "__init__":
            continue
        full = os.path.join("./plugins", entry)
        if entry.endswith(".py") or os.path.isfile(os.path.join(full, "__init__.py")):
            names.append(name)
    return names


def _loaded():
    return [k.split(".", 1)[1] for k in sys.modules if k.startswith("plugins.") and "." not in k.split(".", 1)[1]]


def _meta_modules():
    """Return {META_name: module_object} for all loaded plugins.* modules with META."""
    result = {}
    for mod_name in list(sys.modules):
        if mod_name.startswith("plugins."):
            mod = sys.modules[mod_name]
            meta = getattr(mod, "META", None)
            if isinstance(meta, dict) and "name" in meta:
                result[meta["name"]] = mod
    return result


def _handler_counts(name):
    hc = 0
    for ev_handlers in events.events.values():
        for h in ev_handlers:
            mod = h.__module__.rsplit(".", 1)[-1]
            mname = events._handler_name(h)
            if mod == name or mname == name:
                hc += 1
    return hc


def _cmd_counts(name):
    from libs.command import _handlers, _dynamic_handlers
    cc = 0
    for d in (_handlers, _dynamic_handlers):
        for handler in d.values():
            mod = handler.__module__.rsplit(".", 1)[-1]
            mname = events._handler_name(handler)
            if mod == name or mname == name:
                cc += 1
    return cc


class _PluginCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        idx = text.rfind(" ")
        word = text[idx + 1:] if idx >= 0 else text
        parts = text.split()

        if len(parts) <= 1 and not text.endswith(" "):
            for item in ("list", "load", "unload", "reload"):
                if item.lower().startswith(word.lower()):
                    yield Completion(item, start_position=-len(word))
            return

        cmd = parts[0]
        if cmd == "load":
            loaded = set(_loaded())
            for name in _available():
                if name not in loaded and name.lower().startswith(word.lower()):
                    yield Completion(name, start_position=-len(word))
        elif cmd in ("unload", "reload"):
            for name in _loaded():
                if name.lower().startswith(word.lower()):
                    yield Completion(name, start_position=-len(word))


completer.register_hint(["/plugin", "load"], "<name>")
completer.register_hint(["/plugin", "unload"], "<name>")
completer.register_hint(["/plugin", "reload"], "<name>")


@command.register(["/plugin"], dynamic=_PluginCompleter())
def _cmd_plugin(*args):
    def _show_all():
        loaded = set(_loaded())
        seen = set()
        for name in _available():
            seen.add(name)
            if name in loaded:
                hc = _handler_counts(name)
                cc = _cmd_counts(name)
                _LOG.info(f"{name}  loaded  ({hc} events, {cc} commands)")
            else:
                _LOG.info(f"{name}  unloaded")
        for mname in _meta_modules():
            if mname not in seen:
                hc = _handler_counts(mname)
                cc = _cmd_counts(mname)
                _LOG.info(f"{mname}  loaded  ({hc} events, {cc} commands)")
                seen.add(mname)

    if not args:
        _show_all()
        return

    cmd = args[0].lower()

    if cmd == "list":
        _show_all()
        return

    if len(args) < 2:
        _LOG.info("usage: /plugin <load|unload|reload> <name>")
        return

    name = args[1]

    if cmd == "load":
        if name in _loaded():
            _LOG.warning(f"{name} already loaded")
            return
        loader.load_plugin(name)
        if name in _loaded():
            _LOG.info(f"{name} loaded")
        else:
            _LOG.error(f"failed to load {name}")

    elif cmd == "unload":
        if name not in _loaded():
            _LOG.warning(f"{name} not loaded")
            return
        loader.unload_plugin(name)
        _LOG.info(f"{name} unloaded")

    elif cmd == "reload":
        if name not in _loaded():
            _LOG.warning(f"{name} not loaded")
            return
        loader.reload_plugin(name)
        if name in _loaded():
            _LOG.info(f"{name} reloaded")
        else:
            _LOG.error(f"failed to reload {name}")

    else:
        _LOG.warning(f"unknown subcommand '{cmd}'")
