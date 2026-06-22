# logger — 日志系统

## 配置

`config/core/logger.json`:

```json
{
  "LEVEL": "DEBUG",
  "LOG_LEVEL": "DEBUG",
  "FORMATS": "/TIME/[/LEVEL/]</NAME/>:/TEXT/"
}
```

- `LEVEL` — 控制台最低等级
- `LOG_LEVEL` — 文件日志最低等级
- `FORMATS` — 输出模板，运行时替换

## 等级

| 等级 | 值 |
|------|-----|
| DEBUG | 0 |
| INFO | 1 |
| WARNING | 2 |
| ERROR | 3 |

## API

- `get_logger(name)` — 获取/创建 Logger 实例
- `set_level(level)` — 设置控制台等级
- `set_log_level(level)` — 设置文件日志等级
- `enable(name, enabled)` — 启用/禁用指定 logger
- `list_loggers()` — 返回 `{name: {"enabled": bool, "level": str}}`
- `set_logger_level(name, level)` — 设置指定 logger 等级
- `raw_print(text)` — 线程安全输出到 output_buffer

## 日志文件

写入 `./logs/` 目录：
- `YYYY-MM-DD.log` — 按日期归档
- `latest.log` — 本次运行日志，每次启动自动清空

## 线程安全

`raw_print` 使用 `_print_lock` 防止多线程同时写入 buffer。
