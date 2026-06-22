from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import get_app
from libs import handle

kb = KeyBindings()


@Condition
def _suggestion_available():
    app = get_app()
    return (
        app.current_buffer.suggestion is not None
        and len(app.current_buffer.suggestion.text) > 0
        and app.current_buffer.document.is_cursor_at_the_end
    )


@kb.add("right", filter=_suggestion_available)
def _(event):
    b = event.current_buffer
    if b.suggestion:
        b.insert_text(b.suggestion.text)


@kb.add("c-q")
def exit_(event):
    handle.exit_app()
