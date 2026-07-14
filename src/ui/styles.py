APP_STYLESHEET = """
/* ── 全局基调 ── */
QMainWindow, QDialog {
    background-color: #0c1018;
}

QWidget {
    color: #b8c0d0;
    font-family: "Segoe UI", "Microsoft YaHei UI", sans-serif;
    font-size: 12px;
}

#centralRoot {
    background-color: #0c1018;
}

/* ── 自定义标题栏 ── */
#customTitleBar {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(18, 22, 34, 0.95), stop:1 rgba(12, 16, 24, 0.98));
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

#titleBarName {
    font-size: 13px;
    font-weight: 600;
    color: #f0f2f8;
    letter-spacing: 0.3px;
}

#menuTextBtn {
    background: transparent;
    border: none;
    color: #8892a4;
    font-size: 12px;
    font-weight: 500;
    padding: 6px 12px;
    border-radius: 0px;
    border-bottom: 2px solid transparent;
}

#menuTextBtn:hover {
    color: #c8d0e0;
    border-bottom: 2px solid #635bff;
    background: transparent;
}

#menuTextBtn:pressed {
    color: #9061ff;
}

#titleBtn_normal, #titleBtn_min, #titleBtn_max {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 6px;
    color: #8892a4;
    font-size: 12px;
    font-weight: 400;
    padding: 0;
    margin-left: 4px;
}

#titleBtn_normal:hover, #titleBtn_min:hover, #titleBtn_max:hover {
    background: rgba(255, 255, 255, 0.10);
    border-color: rgba(255, 255, 255, 0.14);
    color: #e0e4ec;
}

#titleBtn_close {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 6px;
    color: #8892a4;
    font-size: 14px;
    padding: 0;
    margin-left: 4px;
}

#titleBtn_close:hover {
    background: rgba(255, 71, 87, 0.85);
    border-color: rgba(255, 71, 87, 0.6);
    color: #ffffff;
}

/* ── 头部 Hero 区域 ── */
#heroFrame {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(99, 91, 255, 0.08), stop:0.5 rgba(18, 24, 38, 0.6), stop:1 rgba(34, 184, 207, 0.06));
    border-bottom: 1px solid qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(99, 91, 255, 0.0), stop:0.3 rgba(99, 91, 255, 0.25),
        stop:0.7 rgba(34, 184, 207, 0.25), stop:1 rgba(34, 184, 207, 0.0));
}

#appSubtitle {
    font-size: 11px;
    color: #6b7588;
    letter-spacing: 0.8px;
}

#subtitleAccent {
    color: #22b8cf;
}

/* ── 磨砂玻璃卡片 ── */
#glassCard {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(22, 28, 42, 0.72), stop:1 rgba(14, 18, 28, 0.85));
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 14px;
}

#glassCard[hovered="true"] {
    border-color: rgba(99, 91, 255, 0.22);
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(26, 32, 50, 0.78), stop:1 rgba(16, 20, 32, 0.88));
}

#cardAccent {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #635bff, stop:1 #9061ff);
    border-radius: 2px;
}

#cardTitle {
    font-size: 14px;
    font-weight: 600;
    color: #f0f2f8;
}

#cardHint {
    font-size: 11px;
    color: #5c6478;
}

#cardDivider {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(99, 91, 255, 0.0), stop:0.5 rgba(255, 255, 255, 0.08), stop:1 rgba(34, 184, 207, 0.0));
    max-height: 1px;
    min-height: 1px;
    border: none;
}

/* ── 文件列表 ── */
#fileList {
    background: rgba(8, 11, 18, 0.55);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    padding: 4px;
    outline: none;
}

#fileList::item {
    border: none;
    background: transparent;
}

/* ── 按钮体系 ── */
QPushButton {
    background: rgba(255, 255, 255, 0.05);
    color: #c0c8d8;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 8px 14px;
    font-weight: 500;
    font-size: 12px;
    min-height: 16px;
}

QPushButton:hover {
    background: rgba(255, 255, 255, 0.09);
    border-color: rgba(255, 255, 255, 0.14);
    color: #e4e8f0;
}

QPushButton:pressed {
    background: rgba(255, 255, 255, 0.04);
}

QPushButton:disabled {
    background: rgba(255, 255, 255, 0.02);
    color: #4a5264;
    border-color: rgba(255, 255, 255, 0.04);
}

QPushButton#addFileBtn {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(255, 255, 255, 0.10), stop:1 rgba(255, 255, 255, 0.05));
    border: 1px solid rgba(255, 255, 255, 0.12);
    color: #dce2ee;
}

QPushButton#addFileBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(255, 255, 255, 0.16), stop:1 rgba(255, 255, 255, 0.08));
    border-color: rgba(99, 91, 255, 0.35);
}

QPushButton#neutralBtn {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.07);
    color: #98a0b4;
}

QPushButton#neutralBtn:hover {
    background: rgba(255, 255, 255, 0.08);
    color: #c8d0e0;
}

QPushButton#dangerButton {
    background: transparent;
    color: #ff6b7a;
    border: 1px solid rgba(255, 71, 87, 0.35);
}

QPushButton#dangerButton:hover {
    background: rgba(255, 71, 87, 0.12);
    border-color: rgba(255, 71, 87, 0.55);
    color: #ff8a96;
}

QPushButton#primaryButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #9061ff, stop:1 #635bff);
    color: #ffffff;
    border: 1px solid rgba(144, 97, 255, 0.4);
    font-weight: 600;
    font-size: 13px;
    padding: 14px 22px;
    min-height: 24px;
    border-radius: 8px;
}

QPushButton#primaryButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #a478ff, stop:1 #7b72ff);
    border-color: rgba(144, 97, 255, 0.6);
}

QPushButton#primaryButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #7a4ef0, stop:1 #5548e8);
}

QPushButton#primaryButton:disabled {
    background: rgba(255, 255, 255, 0.04);
    color: #4a5264;
    border-color: rgba(255, 255, 255, 0.06);
}

#iconButton {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 6px;
    color: #8892a4;
    font-size: 13px;
    padding: 0;
}

#iconButton:hover {
    background: rgba(99, 91, 255, 0.15);
    border-color: rgba(99, 91, 255, 0.35);
    color: #c8b8ff;
}

/* ── 表单控件 ── */
QLabel#fieldLabel {
    color: #6b7588;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.3px;
}

#sliderValue {
    color: #9061ff;
    font-size: 14px;
    font-weight: 600;
    min-width: 20px;
}

QComboBox {
    background: rgba(8, 11, 18, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 8px;
    padding: 9px 14px;
    color: #dce2ee;
    min-height: 18px;
    font-size: 12px;
}

QComboBox:hover {
    border-color: rgba(99, 91, 255, 0.45);
    background: rgba(12, 16, 26, 0.85);
}

QComboBox:focus {
    border-color: rgba(99, 91, 255, 0.6);
}

QComboBox::drop-down {
    border: none;
    width: 30px;
    background: transparent;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #6b7588;
    margin-right: 10px;
}

QComboBox:hover::down-arrow {
    border-top-color: #9061ff;
}

QComboBox QAbstractItemView {
    background: rgba(18, 24, 38, 0.96);
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 8px;
    padding: 4px;
    color: #c0c8d8;
    selection-background-color: rgba(99, 91, 255, 0.35);
    selection-color: #f0f2f8;
    outline: none;
}

QComboBox QAbstractItemView::item {
    padding: 8px 12px;
    border-radius: 6px;
    min-height: 24px;
}

QComboBox QAbstractItemView::item:hover {
    background: rgba(99, 91, 255, 0.18);
}

QSlider#gradientSlider::groove:horizontal {
    background: rgba(255, 255, 255, 0.06);
    height: 6px;
    border-radius: 3px;
}

QSlider#gradientSlider::sub-page:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #635bff, stop:1 #9061ff);
    height: 6px;
    border-radius: 3px;
}

QSlider#gradientSlider::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #a478ff, stop:1 #635bff);
    width: 16px;
    height: 16px;
    margin: -5px 0;
    border-radius: 8px;
    border: 2px solid rgba(255, 255, 255, 0.25);
}

QSlider#gradientSlider::handle:horizontal:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #b890ff, stop:1 #7b72ff);
    border-color: rgba(255, 255, 255, 0.4);
}

/* ── 预览区域 ── */
#previewPanel {
    background: transparent;
}

#previewScroll {
    background: rgba(8, 11, 18, 0.45);
    border: 1px solid rgba(34, 184, 207, 0.15);
    border-radius: 8px;
}

#previewContainer {
    background: transparent;
}

#previewPlaceholder {
    background: transparent;
    color: #4a5264;
    font-size: 12px;
    border: 1px dashed rgba(255, 255, 255, 0.06);
    border-radius: 8px;
}

#previewPlaceholder[hasPaper="true"] {
    background: rgba(255, 255, 255, 0.97);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 6px;
}

/* ── 进度条 ── */
QProgressBar {
    background: rgba(8, 11, 18, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 8px;
    text-align: center;
    color: #6b7588;
    font-size: 11px;
    min-height: 22px;
    max-height: 22px;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #635bff, stop:1 #22b8cf);
    border-radius: 6px;
    margin: 2px;
}

/* ── 滚动条 ── */
QScrollArea {
    background: transparent;
    border: none;
}

QScrollBar:vertical {
    background: transparent;
    width: 8px;
    border-radius: 4px;
    margin: 2px;
}

QScrollBar::handle:vertical {
    background: rgba(255, 255, 255, 0.12);
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(99, 91, 255, 0.45);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background: transparent;
    height: 8px;
}

QScrollBar::handle:horizontal {
    background: rgba(255, 255, 255, 0.12);
    border-radius: 4px;
}

/* ── 底部状态栏 ── */
#statusBarWidget {
    background: rgba(10, 14, 22, 0.85);
    border-top: 1px solid qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(99, 91, 255, 0.0), stop:0.5 rgba(255, 255, 255, 0.06), stop:1 rgba(34, 184, 207, 0.0));
}

#statusText {
    color: #5c6478;
    font-size: 11px;
}

/* ── 下拉菜单（标题栏触发） ── */
QMenu {
    background: rgba(18, 24, 38, 0.97);
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 8px;
    padding: 6px;
}

QMenu::item {
    padding: 8px 32px 8px 16px;
    border-radius: 6px;
    color: #b8c0d0;
    font-size: 12px;
}

QMenu::item:selected {
    background: rgba(99, 91, 255, 0.22);
    color: #f0f2f8;
}

QMenu::separator {
    height: 1px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(255,255,255,0.0), stop:0.5 rgba(255,255,255,0.08), stop:1 rgba(255,255,255,0.0));
    margin: 4px 8px;
}

/* ── 对话框 ── */
QDialog {
    border: 1px solid rgba(255, 255, 255, 0.08);
}

QTextBrowser {
    background: rgba(8, 11, 18, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 8px;
    color: #b8c0d0;
    padding: 8px;
}

QMessageBox {
    background-color: #12182a;
}

QMessageBox QLabel {
    color: #b8c0d0;
    font-size: 12px;
}

QFileDialog {
    background-color: #12182a;
}
"""

HELP_HTML = """
<body style="background:#0c1018; color:#b8c0d0; font-family:'Segoe UI','Microsoft YaHei UI',sans-serif; font-size:12px; line-height:1.6;">
<h2 style="color:#9061ff; margin-top:0; font-size:16px;">发票合并助手 · 使用说明</h2>

<h3 style="color:#dce2ee; font-size:13px;">功能概述</h3>
<p>本工具用于将多张发票 PDF 或图片合并为<strong style="color:#f0f2f8;">一个 PDF 文件</strong>。支持自定义每页排列方式（行数 × 列数），并在合并前提供<strong style="color:#22b8cf;">实时预览</strong>。</p>

<h3 style="color:#dce2ee; font-size:13px;">界面说明</h3>
<ul>
<li><strong style="color:#c8d0e0;">文件列表</strong>：显示已添加的文件，支持多选后批量移除。</li>
<li><strong style="color:#c8d0e0;">排版设置</strong>：配置页面方向、每页行数/列数，以及合并导出按钮。</li>
<li><strong style="color:#c8d0e0;">实时预览</strong>：添加文件或修改排版参数后自动刷新，预览第一页的排版效果。</li>
<li><strong style="color:#c8d0e0;">底部状态栏</strong>：显示当前操作状态（就绪、预览中、合并中等）。</li>
</ul>

<h3 style="color:#dce2ee; font-size:13px;">使用步骤</h3>
<ol>
<li>点击<strong>「添加文件」</strong>，选择一个或多个待合并文件。</li>
<li>在<strong>排版设置</strong>中调整页面方向与行数、列数，右侧预览区会同步更新。</li>
<li>确认预览无误后，点击<strong>「合并并导出 PDF」</strong>，选择保存路径即可。</li>
</ol>

<h3 style="color:#dce2ee; font-size:13px;">快捷键</h3>
<table cellpadding="4" style="color:#98a0b4;">
<tr><td><strong style="color:#9061ff;">Ctrl+O</strong></td><td>添加文件</td></tr>
<tr><td><strong style="color:#9061ff;">Delete</strong></td><td>移除选中文件</td></tr>
<tr><td><strong style="color:#9061ff;">Ctrl+M</strong></td><td>合并并导出 PDF</td></tr>
<tr><td><strong style="color:#9061ff;">F1</strong></td><td>打开使用说明</td></tr>
</table>
</body>
"""
