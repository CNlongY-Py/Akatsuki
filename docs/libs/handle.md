# handle — 输入处理

## API

- `exit_app()` — 退出 prompt_toolkit 应用
- `on_input(string)` — 输入接受回调：记录日志、派发命令、未匹配时触发 `user_input` 事件

## 流程

```
输入 → on_input → log.info(text) → command.dispatch(text)
                                        ↓ 未匹配
                                   events.call_event("user_input", text)
```
