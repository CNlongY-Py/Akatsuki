from prompt_toolkit.completion import Completer, Completion
from libs import command, config, logger

META = {
    "name": "Debug",
    "version": "1.0.0",
    "author": "CNlongY",
    "description": "Toggle log levels per logger",
}
_LOG = logger.get_logger("Debug")
_CFG = config.cfg("core/logger.json")


def _set_level(level):
    for l in logger.loggers.values():
        l.set_level(level)
    _CFG.set("LEVEL", level)
    _LOG.info(f"log level set to {level}")


class _DebugCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        idx = text.rfind(" ")
        word = text[idx + 1:] if idx >= 0 else text
        parts = text.split()
        if len(parts) <= 1:
            items = ["DEBUG", "INFO", "WARNING", "ERROR", "toggle", *logger.loggers.keys()]
        else:
            items = ["DEBUG", "INFO", "WARNING", "ERROR", "on", "off"]
        for item in items:
            if item.lower().startswith(word.lower()):
                yield Completion(item, start_position=-len(word))


@command.register(["/debug"], dynamic=_DebugCompleter())
def _cmd_debug(*args):
    if not args:
        info = []
        for l in logger.loggers.values():
            s = f"{l.name}={l.level}"
            if l.disabled:
                s += "(disabled)"
            info.append(s)
        _LOG.info(f"levels: {', '.join(sorted(info))}")
        return

    arg = args[0].upper()

    if arg == "TOGGLE":
        for l in logger.loggers.values():
            if l.level == "DEBUG":
                _set_level("INFO")
                return
        _set_level("DEBUG")
        return

    if arg in ("DEBUG", "INFO", "WARNING", "ERROR"):
        _set_level(arg)
        return

    # specific logger
    name = args[0]
    logger_obj = logger.loggers.get(name)
    if not logger_obj:
        for k, v in logger.loggers.items():
            if k.lower() == name.lower():
                logger_obj = v
                break
    if not logger_obj:
        _LOG.warning(f"unknown: '{args[0]}'")
        return

    if len(args) == 1:
        _LOG.info(f"{logger_obj.name}={logger_obj.level}" + (" (disabled)" if logger_obj.disabled else ""))
        return

    second = args[1].upper()
    if second == "ON":
        logger_obj.disabled = False
        _LOG.info(f"{logger_obj.name} enabled")
    elif second == "OFF":
        logger_obj.disabled = True
        _LOG.info(f"{logger_obj.name} disabled")
    elif second in ("DEBUG", "INFO", "WARNING", "ERROR"):
        logger_obj.set_level(second)
        _LOG.info(f"{logger_obj.name} set to {second}")
    else:
        _LOG.warning(f"unknown option '{args[1]}'")
