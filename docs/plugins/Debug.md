# Debug — 日志等级切换

内置插件，按模块名控制日志输出等级。

## META

```python
META = {"name": "Debug", "version": "1.0.0", "author": "CNlongY", "description": "Toggle log levels per logger"}
```

## 命令

| 命令 | 作用 |
|------|------|
| `/debug` | 列出所有 logger 的等级/启用状态 |
| `/debug DEBUG\|INFO\|WARNING\|ERROR` | 设置全部 logger 等级 |
| `/debug toggle` | 全部 DEBUG ↔ INFO 切换 |
| `/debug <name> DEBUG\|INFO\|...` | 设置指定 logger 等级 |
| `/debug <name> on\|off` | 启用/禁用指定 logger |

## 补全

`_DebugCompleter`：先补全 logger 名称，再补全等级/状态值。
