from prompt_toolkit.completion import Completer, Completion
from libs import completer

_handlers = {}
_dynamic_handlers = {}
_dynamic_providers = {}
_custom_completers = {}


def register(path, handler=None, dynamic=None):
    def decorator(func):
        parts = path if isinstance(path, list) else [path]
        key = tuple(parts)
        if dynamic is not None:
            _dynamic_handlers[key] = func
            if isinstance(dynamic, Completer):
                _custom_completers[key] = dynamic
            else:
                _dynamic_providers[key] = dynamic if callable(dynamic) else lambda: dynamic
        else:
            _handlers[key] = func
        _rebuild_completer()
        return func

    if handler is not None:
        return decorator(handler)
    return decorator


def unregister(path):
    parts = path if isinstance(path, list) else [path]
    key = tuple(parts)
    _handlers.pop(key, None)
    _dynamic_handlers.pop(key, None)
    _dynamic_providers.pop(key, None)
    _custom_completers.pop(key, None)
    _rebuild_completer()


def dispatch(text):
    parts = text.strip().split()
    if not parts:
        return False

    for i in range(len(parts), 0, -1):
        path = tuple(parts[:i])
        if path in _handlers:
            _handlers[path](*parts[i:])
            return True
        if path in _dynamic_handlers:
            _dynamic_handlers[path](*parts[i:])
            return True
    return False


class _DynamicWordCompleter(Completer):
    def __init__(self, provider, extra_words=None):
        self.provider = provider
        self.extra_words = extra_words or []

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        idx = text.rfind(" ")
        word = text[idx + 1:] if idx >= 0 else text
        raw = self.provider()
        words = [str(w) for w in raw] + self.extra_words
        for w in sorted(set(words)):
            if w.lower().startswith(word.lower()):
                yield Completion(w, -len(word))


def _rebuild_completer():
    cmd_dict = {}
    for path_tuple in _handlers:
        _insert_leaf(cmd_dict, path_tuple)
    for path_tuple, provider in _dynamic_providers.items():
        existing = _walk(cmd_dict, list(path_tuple))
        extra = _collect_leaf_words(existing) if isinstance(existing, dict) else []
        _insert_completer(cmd_dict, path_tuple, _DynamicWordCompleter(provider, extra))
    for path_tuple, comp in _custom_completers.items():
        _insert_completer(cmd_dict, path_tuple, comp)
    completer.clear_commands()
    completer.register_commands(cmd_dict)


def _walk(d, parts):
    for part in parts:
        if isinstance(d, dict) and part in d:
            d = d[part]
        else:
            return None
    return d


def _collect_leaf_words(d):
    words = []
    for k, v in d.items():
        words.append(k)
        if isinstance(v, dict):
            words.extend(_collect_leaf_words(v))
    return words


def _insert_leaf(d, path_tuple):
    for part in path_tuple[:-1]:
        if part not in d or not isinstance(d[part], dict):
            d[part] = {}
        d = d[part]
    d[path_tuple[-1]] = None


def _insert_completer(d, path_tuple, comp):
    for part in path_tuple[:-1]:
        if part not in d or not isinstance(d[part], dict):
            d[part] = {}
        d = d[part]
    d[path_tuple[-1]] = comp


@register("/exit")
def _cmd_exit():
    from libs import handle
    handle.exit_app()


@register("/clear")
def _cmd_clear():
    import libs.uicontrol as uicontrol
    uicontrol.output_buffer.text = ""
