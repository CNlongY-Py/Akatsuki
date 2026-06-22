# scheduler — 计划任务

通过事件系统实现的轻量级定时调度器，支持延迟执行和循环执行。

## API

### `start()`

启动调度器后台线程。由 `app.py` 在加载插件前自动调用。

### `stop()`

停止调度器。

### `delay(event, seconds, **extras)`

延迟 `seconds` 秒后触发一次 `event`。返回 task_id 用于取消。

```python
scheduler.delay("my_event", seconds=10, data="hello")
```

### `interval(event, seconds, **extras)`

每 `seconds` 秒循环触发 `event`。返回 task_id 用于取消。

```python
scheduler.interval("tick", seconds=5)
```

### `cancel(task_id)`

取消指定任务。

## 事件

调度器通过 `events.call_event(event, **extras)` 触发事件，handler 接收 `payload` 参数：

```python
@events.on_event("tick")
def on_tick(payload):
    payload.log.info("tick")
```

## 说明

- 后台守护线程运行，精度约 1 秒
- 任务按触发时间排序，每次循环检查到期的任务
- 重复任务触发后自动重排
- 任务 handler 异常不会影响调度器
