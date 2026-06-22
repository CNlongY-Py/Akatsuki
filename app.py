"""
Project Akatsuki
Powered by CNlongY-Py
"""
from libs import uicontrol
from libs import logger
from libs import loader
from libs import events
from libs import scheduler

logger.raw_print("""

           d8888 888               888                      888      d8b
          d88888 888               888                      888      Y8P
         d88P888 888               888                      888
        d88P 888 888  888  8888b.  888888 .d8888b  888  888 888  888 888
       d88P  888 888 .88P     "88b 888    88K      888  888 888 .88P 888
      d88P   888 888888K  .d888888 888    "Y8888b. 888  888 888888K  888
     d8888888888 888 "88b 888  888 Y88b.       X88 Y88b 888 888 "88b 888
    d88P     888 888  888 "Y888888  "Y888  88888P'  "Y88888 888  888 888
 -========================================================================-
""")
scheduler.start()
loader.load_plugins()
events.call_event("init_plugins")
uicontrol.app_start()
