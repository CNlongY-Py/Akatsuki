<p align="center">
  <img src="https://socialify.git.ci/CNlongY-Py/Re-SimpQ/image?language=1&amp;name=1&amp;owner=1&amp;theme=Light" alt="Akatsuki">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/license-GPLv3-green" alt="License">
  <img src="https://img.shields.io/badge/prompt_toolkit-powered-orange?logo=python" alt="prompt_toolkit">
</p>

<h1 align="center">⚡ Akatsuki</h1>
<p align="center"><i>基于 prompt_toolkit 的多账户终端框架 · 插件化事件驱动架构</i></p>

---

## ✨ 特性

- **事件驱动** — 基于事件的松耦合架构，插件之间通过事件通信
- **插件系统** — 热加载/卸载/重载，动态扩展功能
- **Tab 补全** — 命令自动补全 + AutoSuggest 用法提示
- **绑定过滤** — 将事件按账户路由到指定插件
- **计划任务** — 内置调度器，支持延迟/循环事件触发
- **日志系统** — 多级日志、按日期归档、latest.log 实时追踪

## 🚀 快速开始

```bash
pip install -r requirements.txt
python app.py
```

## 📦 架构

```
Akatsuki/
├── app.py                  # 入口
├── requirements.txt        # 依赖
├── libs/                   # ◈ 框架层（不依赖任何插件）
│   ├── command.py          #   命令注册与派发
│   ├── completer.py        #   Tab 补全 + AutoSuggest
│   ├── config.py           #   JSON 配置文件读写
│   ├── events.py           #   事件系统（EventPayload + 绑定过滤）
│   ├── handle.py           #   输入处理
│   ├── kbcontrol.py        #   键盘绑定
│   ├── loader.py           #   插件加载/卸载/重载
│   ├── logger.py           #   日志系统（等级控制 + 线程安全）
│   ├── render.py           #   模板渲染
│   ├── scheduler.py        #   计划任务（延迟/循环）
│   ├── session.py          #   账户与会话管理
│   └── uicontrol.py        #   UI 布局
├── plugins/                # ◈ 插件层
│   ├── Debug.py            #   🔧 日志等级切换【内置】
│   └── PluginMgr.py        #   🔧 插件管理器【内置】
├── config/
│   └── core/               #   核心配置（logger.json, render.json）
├── docs/                   #   模块文档
└── logs/                   #   日志文件（.log）
```

## ⌨️ 命令

| 命令 | 来源 | 说明 |
|------|------|------|
| `/exit` | 内置 | 退出程序 |
| `/clear` | 内置 | 清屏 |
| `/debug` | Debug | 查看/切换日志等级 |
| `/plugin` | PluginMgr | 插件生命周期管理 |

## 🔌 插件开发

```python
from libs import command, events, logger

META = {"name": "MyPlugin", "version": "1.0.0", "author": "you", "description": "..."}

@events.on_event("init_plugins")
def on_start(payload):
    payload.log.info("loaded!")

@command.register("/hello")
def hello(*args):
    payload.log.info(f"Hello, {args}!")
```

详细教程见 [`docs/tutorial.md`](docs/tutorial.md)。

## 📖 文档

各模块文档见 [`docs/`](docs/) 目录。

---

## 📄 许可证

GNU General Public License v3.0 — 详见 [LICENSE](LICENSE)。

<p align="center"><sub>Powered by CNlongY-Py · Akatsuki</sub></p>
