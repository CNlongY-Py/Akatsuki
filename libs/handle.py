from prompt_toolkit.application import get_app
from libs import logger
from libs import events
from libs import command


def exit_app():
    get_app().exit()


def on_input(string):
    if string.text:
        log = logger.get_logger("Input")
        text = string.text.strip()
        log.info(text)
        if not command.dispatch(text):
            events.call_event("user_input", data=text)
