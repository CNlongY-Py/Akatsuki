# PluginMgr — 插件管理器

内置插件，管理插件的加载/卸载/重载生命周期。

## META

```python
META = {"name": "PluginMgr", "version": "1.0.0", "author": "CNlongY", "description": "List, load, unload, reload plugins"}
```

## 命令

| 命令 | 作用 |
|------|------|
| `/plugin` | 列出所有插件及状态 |
| `/plugin list` | 同上 |
| `/plugin load <name>` | 加载插件 |
| `/plugin unload <name>` | 卸载插件 |
| `/plugin reload <name>` | 重载插件 |

## 说明

- `load` 调用 `loader.load_plugin()`，通过 `importlib.import_module` 导入
- `unload` 从 `sys.modules` 删除模块及其子模块
- `reload` = unload + load
- 通过 `_meta_modules()` 扫描所有已加载 `plugins.*` 模块的 META，可识别包内子插件（如 `SubPlugin`）
- 状态显示使用 `events.events` 检查是否注册了事件 handler
- 插件计数器通过 `events._handler_name()` 匹配 META 名或模块名

## 补全

`_PluginCompleter`：先补全子命令（list/load/unload/reload），再补全插件名称（从 `./plugins/` 目录扫描）。
