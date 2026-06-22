import shutil

from prompt_toolkit.layout.containers import FloatContainer
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.layout.containers import VSplit
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.containers import Float
from prompt_toolkit.layout import CompletionsMenu
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.widgets import Label
from prompt_toolkit.buffer import Buffer
from prompt_toolkit import Application
from libs import completer
from libs import kbcontrol
from libs import handle

output_buffer = Buffer(name="output")
_input_completer = completer.get_completer()
input_area = TextArea(
    name="input_area", height=1, style="bg:#111111", multiline=False,
    focus_on_click=True, wrap_lines=True,
    accept_handler=handle.on_input,
    completer=_input_completer,
    auto_suggest=completer.CompleterAutoSuggest(_input_completer),
)

completer.on_rebuild(lambda c: (setattr(input_area, "completer", c), setattr(input_area, "auto_suggest", completer.CompleterAutoSuggest(c))))

root_container = HSplit([
    Window(BufferControl(output_buffer), wrap_lines=True),
    VSplit([
        Label("> ", width=2, style="bg:#111111"),
        input_area,
    ])
])

float_container = [
    Float(CompletionsMenu(max_height=max(3, shutil.get_terminal_size().lines * 30 // 100)), bottom=1, right=0)
]
main_container = FloatContainer(root_container, float_container)

layout = Layout(main_container, focused_element=input_area)

app = Application(layout=layout, key_bindings=kbcontrol.kb, full_screen=True, mouse_support=True)


def app_start():
    with patch_stdout():
        app.run()


def app_refresh():
    app.invalidate()


def app_exit():
    app.exit()


def get_app():
    return app


register_command = completer.register_command
register_commands = completer.register_commands
