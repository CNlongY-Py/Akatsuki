# events — 事件系统

## 全局

- `events: dict[str, list[callable]]` — 事件名到 handler 列表的映射

## 类

### `EventPayload`

Handler 接收的参数对象，属性：

| 属性 | 类型 | 说明 |
|------|------|------|
| `.log` | Logger | 按插件名自动创建的 logger |
| `.data` | any | 事件数据 |
| `.account` | str | 来源账户名 |
| `.client` | SolarNetworkClient | WS/HTTP 客户端实例 |
| `.config` | cfg | `./config/<name>/` 配置 |

## API

### `on_event(event, func=None)`

装饰器/函数式注册事件 handler。

```python
@events.on_event("custom.event.name")
def handler(payload): ...

@events.on_event("init_plugins")
def on_start(): ...
```

### `call_event(event, *args)`

派发事件。3 参数时创建 `EventPayload`（log, data, account, client, config）并检查绑定过滤；无参数时直接调用 handler。

### `reg_event(event, name=None)`

类装饰器，`name` 可选覆盖事件名。

## 绑定过滤

`call_event` 中调用 `session.get_bindings(name)`：
- `None` — 所有账户
- `[...]` — 只处理列表中的账户
- `[]` — 不处理任何账户

## 插件名解析

`_plugin_name(mod)` 按优先级：
1. 模块的 `META["name"]`
2. 包目录的 `meta.json` 中的 `name`
3. 模块名（`mod.__name__.rsplit(".", 1)[-1]`）
