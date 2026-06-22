# 插件开发教程

插件是扩展框架功能的模块。

## 文件结构

单文件插件直接在 `plugins/` 下创建 `.py` 文件：

```
plugins/
├── MyPlugin.py       # 单文件插件
└── MyPackage/        # 包插件
    ├── __init__.py
    └── ...
```

## 基础模板

```python
# plugins/MyPlugin.py
from libs import command, events, logger

META = {
    "name": "MyPlugin",
    "version": "1.0.0",
    "author": "yourname",
    "description": "What this plugin does",
}

_LOG = logger.get_logger("MyPlugin")


@events.on_event("init_plugins")
def _on_start():
    _LOG.info("MyPlugin loaded")
```

## 注册命令

```python
@command.register("/hello")
def _cmd_hello(*args):
    _LOG.info(f"Hello, {' '.join(args) if args else 'world'}!")
```

多级命令：

```python
@command.register(["/mycmd", "sub"])
def _cmd_sub(*args):
    _LOG.info(f"sub: {args}")
```

## 添加 Tab 补全

### 简单动态补全

`dynamic` 参数接受可调用对象（返回列表或字符串列表）：

```python
@command.register(["/greet"], dynamic=lambda: ["hello", "bye"])
def _cmd_greet(*args):
    _LOG.info(f"{args}")
```

### 自定义 Completer

```python
from prompt_toolkit.completion import Completer, Completion

class _MyCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        idx = text.rfind(" ")
        word = text[idx + 1:] if idx >= 0 else text
        items = ["apple", "banana", "cherry"]
        for item in items:
            if item.lower().startswith(word.lower()):
                yield Completion(item, start_position=-len(word))

@command.register(["/fruit"], dynamic=_MyCompleter())
def _cmd_fruit(*args):
    _LOG.info(f"fruit: {args}")
```

### 分步补全（子命令 + 参数）

```python
class _MyCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        idx = text.rfind(" ")
        word = text[idx + 1:] if idx >= 0 else text
        parts = text.split()

        # 还没输入参数：补全子命令
        if len(parts) <= 1 and not text.endswith(" "):
            for item in ("add", "remove", "list"):
                if item.lower().startswith(word.lower()):
                    yield Completion(item, start_position=-len(word))
            return

        # 已输入子命令：补全参数
        cmd = parts[0]
        if cmd == "add":
            items = ["user1", "user2", "user3"]
        elif cmd == "remove":
            items = ["user1", "user2"]
        else:
            return
        for item in items:
            if item.lower().startswith(word.lower()):
                yield Completion(item, start_position=-len(word))
```

## 用法提示（AutoSuggest）

注册后输入命令时会在光标后显示提示文字：

```python
from libs import completer

completer.register_hint(["/fruit"], "<name>")
completer.register_hint(["/mycmd", "sub"], "<arg>")
```

效果：输入 `/fruit ` 后显示 `<name>`，输入 `/mycmd sub ` 后显示 `<arg>`。

## 订阅事件

### 启动事件

```python
@events.on_event("init_plugins")
def _on_start():
    # 应用启动时执行
    pass
```

### 用户输入事件

```python
@events.on_event("user_input")
def _on_input(payload):
    text = payload.data
    _LOG.info(f"user typed: {text}")
```

### 带绑定过滤的事件

```python
@events.on_event("custom.event.name")
def _on_message(payload):
    _LOG.info(f"{payload.data}")
```

Payload 属性：

| 属性 | 说明 |
|------|------|
| `payload.log` | 按插件名自动创建的 logger |
| `payload.data` | 事件数据 |
| `payload.account` | 来源账户名 |
| `payload.client` | 客户端实例 |
| `payload.config` | `config.cfg("name/")` 实例 |

## META 和包配置

### 单文件插件

```python
META = {
    "name": "MyPlugin",
    "version": "1.0.0",
    "author": "yourname",
    "description": "What this plugin does",
}
```

系统使用 `META["name"]` 作为 logger 名称和绑定查找的标识。

### 包插件

`plugins/MyPackage/meta.json`:

```json
{
    "name": "MyPackage",
    "version": "1.0.0",
    "author": "yourname",
    "description": "What this plugin does"
}
```

## 配置文件

插件专属配置目录通过 `payload.config` 自动创建：

```python
@events.on_event("init_plugins")
def _on_start():
    # config.cfg("MyPlugin/")  -> ./config/MyPlugin/
    pass

# 在命令中直接使用 config
from libs import config
_CFG = config.cfg("MyPlugin/settings.json")

def save_setting(key, value):
    _CFG.set(key, value)
```

## 事件派发

如果你的插件触发事件让其他插件响应：

```python
from libs import events

# 触发时传递 data, account, client
# events.call_event("myplugin.custom_event", data, account, client)
```

其他插件通过 `@events.on_event("myplugin.custom_event")` 订阅。

## 完整示例

```python
# plugins/Echo.py
from prompt_toolkit.completion import Completer, Completion
from libs import command, completer, events, logger

META = {
    "name": "Echo",
    "version": "1.0.0",
    "author": "yourname",
    "description": "Echo input back to the user",
}

_LOG = logger.get_logger("Echo")


class _EchoCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        idx = text.rfind(" ")
        word = text[idx + 1:] if idx >= 0 else text
        items = ["hello", "world"]
        for item in items:
            if item.lower().startswith(word.lower()):
                yield Completion(item, start_position=-len(word))


completer.register_hint(["/echo"], "<word>")


@command.register(["/echo"], dynamic=_EchoCompleter())
def _cmd_echo(*args):
    _LOG.info(" ".join(args) if args else "echo!")


@events.on_event("init_plugins")
def _start():
    _LOG.info("Echo ready")
```

用 `/plugin load Echo` 加载后用 `/echo hello world` 测试。
