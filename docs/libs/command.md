# command — 命令注册与派发

## 数据结构

- `_handlers: dict[tuple, callable]` — 静态命令
- `_dynamic_handlers: dict[tuple, callable]` — 带补全器的命令
- `_dynamic_providers: dict[tuple, callable]` — 动态补全提供者
- `_custom_completers: dict[tuple, Completer]` — 自定义补全器

## API

### `register(path, handler=None, dynamic=None)`

注册命令。`path` 为字符串或列表（如 `["/cmd", "sub"]`），`dynamic` 为 `Completer` 实例或返回列表的可调用对象。

```python
@command.register("/cmd")
def handler(*args): ...

@command.register(["/cmd", "sub"], dynamic=MyCompleter())
def handler(*args): ...
```

### `unregister(path)`

移除命令。

### `dispatch(text)`

派发输入文本，最长前缀匹配。

## 内置命令

- `/exit` — 退出
- `/clear` — 清屏

## 补全器重建

`_rebuild_completer()` 将 `_handlers` / `_dynamic_providers` / `_custom_completers` 合并为嵌套字典，调用 `completer.register_commands()`。
