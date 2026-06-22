from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion
from prompt_toolkit.completion import Completer, Completion, ThreadedCompleter
from prompt_toolkit.document import Document
from prompt_toolkit.application import get_app

_BUILTIN_CMD_DICT = {
    "/exit": None,
    "/clear": None,
}
CMD_DICT = dict(_BUILTIN_CMD_DICT)
USAGE_HINTS: dict[tuple[str, ...], str] = {}

_completer = None
_rebuild_callbacks = []


class _CmdCompleter(Completer):
    def __init__(self, options, ignore_case=True):
        self.options = options
        self.ignore_case = ignore_case

    @classmethod
    def from_nested_dict(cls, data):
        options = {}
        for key, value in data.items():
            if isinstance(value, Completer):
                options[key] = value
            elif isinstance(value, dict):
                options[key] = cls.from_nested_dict(value)
            else:
                options[key] = None
        return cls(options)

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.lstrip()
        stripped_len = len(document.text_before_cursor) - len(text)

        if " " in text:
            first_term = text.split()[0]
            completer = self.options.get(first_term)
            if completer is not None:
                remaining = text[len(first_term):].lstrip()
                move_cursor = len(text) - len(remaining) + stripped_len
                new_doc = Document(
                    remaining,
                    cursor_position=document.cursor_position - move_cursor,
                )
                yield from completer.get_completions(new_doc, complete_event)

        else:
            word = text
            for key in self.options:
                if self._match(key, word):
                    if key == word:
                        sub = self.options[key]
                        if isinstance(sub, (Completer, _CmdCompleter)):
                            for c in sub.get_completions(
                                Document("", cursor_position=0), complete_event
                            ):
                                yield Completion(
                                    key + " " + c.text,
                                    start_position=-len(word),
                                    display=c.text,
                                )
                            return
                    yield Completion(key, start_position=-len(word))

    def _match(self, key, word):
        if not word:
            return True
        if self.ignore_case:
            return key.lower().startswith(word.lower())
        return key.startswith(word)


def _rebuild():
    global _completer
    cmd_completer = _CmdCompleter.from_nested_dict(CMD_DICT)
    _completer = ThreadedCompleter(cmd_completer)
    for cb in _rebuild_callbacks:
        cb(_completer)


def get_completer():
    if _completer is None:
        _rebuild()
    return _completer


def on_rebuild(callback):
    _rebuild_callbacks.append(callback)


def register_command(path, children=None):
    parts = path if isinstance(path, list) else [path]
    d = CMD_DICT
    for part in parts[:-1]:
        if part not in d or d[part] is None:
            d[part] = {}
        d = d[part]
    d[parts[-1]] = children
    _rebuild()


def register_commands(cmd_dict):
    _merge(CMD_DICT, cmd_dict)
    _rebuild()


def clear_commands():
    CMD_DICT.clear()
    CMD_DICT.update(_BUILTIN_CMD_DICT)


def _merge(base, overlay):
    for k, v in overlay.items():
        if k in base and isinstance(base[k], dict) and isinstance(v, dict):
            _merge(base[k], v)
        else:
            base[k] = v


def refresh():
    get_app().invalidate()


def register_hint(path, hint):
    if isinstance(path, str):
        path = path.strip().split()
    USAGE_HINTS[tuple(path)] = hint.split()


class CompleterAutoSuggest(AutoSuggest):
    def __init__(self, completer):
        self._completer = completer

    def get_suggestion(self, buffer, document):
        text = document.text_before_cursor.lstrip()
        if not text:
            return None

        if text.endswith(" "):
            parts = text.rstrip().split()
            for cmd_path, hint_parts in USAGE_HINTS.items():
                if parts[:len(cmd_path)] == list(cmd_path):
                    consumed = len(parts) - len(cmd_path)
                    remaining = hint_parts[consumed:]
                    if remaining:
                        return Suggestion(" ".join(remaining))

        completions = list(self._completer.get_completions(document, None))
        if completions:
            suggestion = completions[0].text
            if suggestion.startswith(text):
                return Suggestion(suggestion[len(text):])
        return None
