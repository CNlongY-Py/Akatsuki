# uicontrol — UI 布局

## 布局

```
┌─────────────────────────────┐
│  output_buffer (可滚动)      │
├─────────────────────────────┤
│ > input_area                 │
└─────────────────────────────┘
```

- `output_buffer` — `Buffer(name="output")`，显示日志
- `input_area` — `TextArea`，单行输入，带 completer + auto_suggest
- `CompletionsMenu` — 浮动在底部，高度为终端行数的 30%（最少 3 行）

## API

- `app_start()` — 启动 full-screen Application
- `app_refresh()` — 刷新 UI
- `app_exit()` — 退出应用
- `get_app()` — 返回 Application 实例
- `register_command` / `register_commands` — 委托给 `completer`

## 重建回调

`completer.on_rebuild` 注册一个回调，在补全器重建时同时更新 `input_area.completer` 和 `input_area.auto_suggest`。
