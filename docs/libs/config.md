# config — JSON 配置文件读写

## 类

### `cfg(path)`

`path` 相对于 `./config/`。以 `/` 结尾视为目录，自动创建；否则视为文件。

```python
c = config.cfg("core/logger.json")   # ./config/core/logger.json
d = config.cfg("myplugin/")          # ./config/myplugin/ 目录
```

## 方法

- `.set(key, value)` — 写入 JSON
- `.get(key="", default=None)` — 读取，无 key 返回整个 dict
- `.delete(key)` — 删除 key

文件使用 `utf-8`、`indent=2` 序列化。
