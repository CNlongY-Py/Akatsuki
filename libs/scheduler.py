import threading
import time
import uuid

from libs import events, logger

_log = logger.get_logger("Scheduler")
_tasks: dict[str, dict] = {}
_thread: threading.Thread | None = None
_stop = threading.Event()


class _Task:
    def __init__(self, event, interval, extras, repeat):
        self.id = uuid.uuid4().hex[:8]
        self.event = event
        self.interval = interval
        self.extras = extras
        self.repeat = repeat
        self.next_tm = time.monotonic() + interval


_tasks_lock = threading.Lock()
_queue: list[_Task] = []


def _loop():
    while not _stop.is_set():
        now = time.monotonic()
        due = []
        with _tasks_lock:
            remaining = []
            for t in _queue:
                if now >= t.next_tm:
                    due.append(t)
                    if t.repeat:
                        t.next_tm = now + t.interval
                        remaining.append(t)
                else:
                    remaining.append(t)
            _queue[:] = remaining

        for t in due:
            try:
                events.call_event(t.event, **t.extras)
            except Exception:
                _log.error(f"scheduled event '{t.event}' failed")

        wait = 1.0
        with _tasks_lock:
            if _queue:
                wait = min(wait, max(0, _queue[0].next_tm - time.monotonic()))
        _stop.wait(wait)


def start():
    global _thread
    if _thread and _thread.is_alive():
        return
    _stop.clear()
    _thread = threading.Thread(target=_loop, daemon=True)
    _thread.start()
    _log.debug("scheduler started")


def stop():
    _stop.set()
    _log.debug("scheduler stopped")


def delay(event, seconds, **extras):
    t = _Task(event, seconds, extras, repeat=False)
    with _tasks_lock:
        _queue.append(t)
        _queue.sort(key=lambda x: x.next_tm)
    _log.debug(f"delay '{event}' in {seconds}s [id={t.id}]")
    return t.id


def interval(event, seconds, **extras):
    t = _Task(event, seconds, extras, repeat=True)
    with _tasks_lock:
        _queue.append(t)
        _queue.sort(key=lambda x: x.next_tm)
    _log.debug(f"interval '{event}' every {seconds}s [id={t.id}]")
    return t.id


def cancel(task_id):
    with _tasks_lock:
        before = len(_queue)
        _queue[:] = [t for t in _queue if t.id != task_id]
    if len(_queue) < before:
        _log.debug(f"cancelled task {task_id}")
