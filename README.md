# 发票合并助手

将多张发票 PDF 或图片按自定义网格排版，合并导出为单个 PDF 的跨平台桌面工具。

<img width="2832" height="1826" alt="image" src="https://github.com/user-attachments/assets/832aee0b-b692-412d-bb20-1590e3a7ef29" />

<img width="2832" height="1826" alt="image" src="https://github.com/user-attachments/assets/fef4c3e0-0c8f-4c80-b155-beeca9bd5012" />


## 快速开始

```bash
pip install -r requirements.txt
python run.py
```

## 项目结构

```
├── run.py                      # 程序入口
├── fapiao_tool/                # 主包
│   ├── config.py               # 常量与默认配置
│   ├── engine/
│   │   └── layout_engine.py    # PDF 排版合并引擎
│   └── interface/
│       ├── workbench.py        # 主窗口与交互逻辑
│       ├── async_jobs.py       # 后台预览/导出任务
│       ├── visual_theme.py     # 全局 QSS 主题
│       ├── help_content.py     # 内置帮助文档
│       └── controls/
│           └── panels.py       # 自定义 UI 组件
├── docs/
│   └── 项目说明.md             # 详细说明文档
└── requirements.txt
```

## 主要能力

- 批量导入 PDF / 图片并合并为单个 PDF
- 自定义每页行数、列数与页面方向
- 高清多页滚动预览
- 深色商务风界面

## 打包（Windows）

```bash
pyinstaller build.spec
```

## 依赖

- PySide6
- PyMuPDF
- Pillow

## 日志

运行异常时写入项目目录下的 `runtime_error.log`。
