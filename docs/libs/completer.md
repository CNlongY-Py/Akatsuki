# completer — Tab 补全与 AutoSuggest

## 数据结构

- `CMD_DICT: dict` — 嵌套命令字典，叶节点为 `None`（静态）或 `Completer` 实例
- `USAGE_HINTS: dict[tuple[str,...], list[str]]` — 用法提示，注册后显示在自动建议中
- `_completer: ThreadedCompleter` — 当前生效的补全器
- `_rebuild_callbacks: list[callable]` — 重建回调（UI 更新 completer + auto_suggest）

## 类

### `_CmdCompleter(Completer)`

- `from_nested_dict(data)` — 从嵌套字典构建树状补全器
- `get_completions()` — 空格后委托给子补全器，否则匹配当前单词前缀
- 子补全器显示 `key + " " + completion.text`，光标位于子补全文本后

### `CompleterAutoSuggest(AutoSuggest)`

- `get_suggestion()` — 先查 `USAGE_HINTS` 匹配补全路径，取第一个 completion 的文本

## API

- `register_command(path, children=None)` — 手动注册命令路径
- `register_commands(cmd_dict)` — 合并嵌套字典
- `clear_commands()` — 重置为仅内置命令
- `register_hint(path, hint)` — 注册用法提示
- `get_completer()` — 获取当前 `ThreadedCompleter`
- `on_rebuild(callback)` — 注册重建回调
- `refresh()` — 刷新 UI
