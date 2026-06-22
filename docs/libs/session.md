# session — 账户与会话管理

## 数据结构

### `Account`

| 属性 | 类型 | 说明 |
|------|------|------|
| `.name` | str | 账户名 |
| `.token` | str | 认证令牌 |
| `.auth_type` | str | 认证类型（`"token"`） |

### 持久化

- 令牌文件：`./config/<plugin>/sessions/<name>.token`
- 元数据：`./config/<plugin>/sessions.json`

默认 `<plugin>` 为 `sessions`（即 `./config/sessions/`），插件可在 `init(cfg_folder=...)` 中重定向。

```json
{
  "bindings": { "MyPlugin": ["MyAccount"] },
  "accounts": { "Akatsuki": { "auth_type": "token" } }
}
```

## API

- `init(cfg_folder=None)` — 扫描 sessions 目录和 JSON 初始化，`cfg_folder` 指定基础路径
- `get_account(name)` — 获取 Account
- `list_accounts()` — 返回 `{name: Account}` dict
- `add_token_account(name, token)` — 添加 token 账户
- `remove_account(name)` — 删除账户
- `add_binding(plugin_id, account_name)` — 添加绑定
- `remove_binding(plugin_id, account_name)` — 移除绑定
- `remove_plugin(plugin_id)` — 移除插件的所有绑定
- `get_bindings(plugin_id)` — 返回绑定列表或 None（无绑定 = 全部）
- `list_bindings()` — 返回完整 bindings dict

## 旧格式迁移

读取时自动将旧 `listeners` 字段（单值字符串）迁移为 `bindings`（列表），写入后持久化新格式。
