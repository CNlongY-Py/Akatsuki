from libs import config
import time

cfg = config.cfg("core/render.json")
settings = cfg.get("settings") or {}
time_format = settings.get("time_format", "%Y-%m-%d %H:%M:%S")


def shader(text, template=None):
    if template is None:
        template = {"/TIME/": time.strftime(time_format)}
    for k, v in template.items():
        text = str(text).replace(str(k), str(v))
    return text
