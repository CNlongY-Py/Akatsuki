# render — 模板渲染

## 配置

`config/core/render.json`:

```json
{
  "settings": {
    "time_format": "%Y-%m-%d %H:%M:%S"
  }
}
```

## API

### `shader(text, template=None)`

将 `text` 中的占位符替换为模板值。

默认模板：
- `/TIME/` → `time.strftime(time_format)`

自定义模板：
```python
render.shader("Hello /NAME/", {"/NAME/": "World"})
```
