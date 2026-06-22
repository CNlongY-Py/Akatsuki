# loader — 插件加载

## API

- `load_plugins()` — 扫描 `./plugins/` 目录，逐个 `importlib.import_module("plugins.<name>")`
- `load_plugin(plugin)` — 加载单个插件
- `unload_plugin(plugin)` — 从 `sys.modules` 删除插件及其子模块
- `reload_plugin(plugin)` — unload + load
- `get_plugin(plugin)` — `importlib.import_module` 返回模块对象

## 说明

- 跳过 `__init__` 和 `.pyc`
- 包插件通过 `os.path.isfile(os.path.join(full, "__init__.py"))` 识别
- 加载失败记录 `log.error`，不阻断其他插件
- 使用 `importlib.import_module` 替代 `runpy`，使 `sys.modules` 可管理
