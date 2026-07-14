"""主窗口与工作台逻辑。"""

from __future__ import annotations

import logging
import os
import sys
import traceback
from typing import List, Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence, QPixmap, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QFrame,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QMenu,
    QMessageBox,
    QProgressBar,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from fapiao_tool import __app_name__, __version__
from fapiao_tool.config import (
    APP_TITLE,
    DEFAULT_COL_COUNT,
    DEFAULT_ROW_COUNT,
    GRID_MAX,
    GRID_MIN,
    LOG_FILENAME,
    ORIENTATION_LANDSCAPE,
    ORIENTATION_PORTRAIT,
    PDF_SAVE_FILTER,
    SUPPORTED_OPEN_FILTER,
    WINDOW_DEFAULT_HEIGHT,
    WINDOW_DEFAULT_WIDTH,
    WINDOW_MIN_HEIGHT,
    WINDOW_MIN_WIDTH,
)
from fapiao_tool.interface.async_jobs import ExportRenderJob, PreviewRenderJob
from fapiao_tool.interface.controls import (
    DocumentQueue,
    FootnoteBar,
    FramelessChrome,
    FrostPanel,
    GlyphButton,
    GridDimensionSlider,
    PulseButton,
    ScrollPreviewPane,
    SectionHeading,
    ChromaticTitle,
)
from fapiao_tool.interface.help_content import USER_GUIDE_HTML
from fapiao_tool.interface.visual_theme import GLOBAL_STYLESHEET


def _configure_logging() -> None:
    logging.basicConfig(
        filename=LOG_FILENAME,
        level=logging.ERROR,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


class WorkbenchWindow(QMainWindow):
    """发票合并主界面。"""

    def __init__(self) -> None:
        super().__init__()
        self._paths: List[str] = []
        self._preview_job: Optional[PreviewRenderJob] = None
        self._export_job: Optional[ExportRenderJob] = None

        self._assemble_layout()
        self._bind_shortcuts()
        self._document_queue.refresh_empty_hint()

    # ------------------------------------------------------------------ 布局

    def _make_section(self, title: str, hint: str = "", accessory: QWidget | None = None):
        panel = FrostPanel()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(14)
        layout.addWidget(SectionHeading(title, hint, accessory))
        rule = QFrame()
        rule.setObjectName("sectionRule")
        rule.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(rule)
        return panel, layout

    def _assemble_layout(self) -> None:
        self.setWindowTitle(APP_TITLE)
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.resize(WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)

        shell = QWidget()
        shell.setObjectName("workbenchRoot")
        self.setCentralWidget(shell)
        shell_layout = QVBoxLayout(shell)
        shell_layout.setContentsMargins(0, 0, 0, 0)
        shell_layout.setSpacing(0)

        self._chrome = FramelessChrome(self)
        shell_layout.addWidget(self._chrome)
        self._wire_menus()

        banner = QFrame()
        banner.setObjectName("bannerStrip")
        banner_layout = QVBoxLayout(banner)
        banner_layout.setContentsMargins(28, 22, 28, 22)
        banner_layout.setSpacing(6)
        banner_layout.addWidget(ChromaticTitle(APP_TITLE))
        caption = QLabel(
            '批量导入 · <span style="color:#22b8cf;">智能排版</span> · 一键合并 PDF 发票'
        )
        caption.setObjectName("bannerCaption")
        caption.setTextFormat(Qt.TextFormat.RichText)
        banner_layout.addWidget(caption)
        shell_layout.addWidget(banner)

        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(24, 20, 24, 20)
        body_layout.setSpacing(20)

        queue_panel, queue_layout = self._make_section(
            "文件列表", "支持 PDF、JPG、PNG 等格式"
        )
        self._document_queue = DocumentQueue()
        self._document_queue.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        queue_layout.addWidget(self._document_queue, 1)

        queue_actions = QHBoxLayout()
        queue_actions.setSpacing(8)
        btn_import = PulseButton("添加文件")
        btn_import.setObjectName("importButton")
        btn_remove = PulseButton("移除选中")
        btn_remove.setObjectName("mutedButton")
        btn_clear = PulseButton("清空全部")
        btn_clear.setObjectName("warnButton")
        queue_actions.addWidget(btn_import)
        queue_actions.addWidget(btn_remove)
        queue_actions.addWidget(btn_clear)
        queue_layout.addLayout(queue_actions)

        layout_panel, layout_form = self._make_section("排版设置", "调整页面方向与每页布局")

        orient_caption = QLabel("页面方向")
        orient_caption.setObjectName("formCaption")
        layout_form.addWidget(orient_caption)
        self._orientation_box = QComboBox()
        self._orientation_box.addItems([ORIENTATION_PORTRAIT, ORIENTATION_LANDSCAPE])
        layout_form.addWidget(self._orientation_box)

        grid_caption = QLabel("每页文件数")
        grid_caption.setObjectName("formCaption")
        layout_form.addWidget(grid_caption)
        self._row_slider = GridDimensionSlider("行数", GRID_MIN, GRID_MAX, DEFAULT_ROW_COUNT)
        self._col_slider = GridDimensionSlider("列数", GRID_MIN, GRID_MAX, DEFAULT_COL_COUNT)
        layout_form.addWidget(self._row_slider)
        layout_form.addWidget(self._col_slider)

        layout_form.addSpacing(12)
        self._export_btn = PulseButton("PDF  合并并导出")
        self._export_btn.setObjectName("accentButton")
        layout_form.addWidget(self._export_btn)
        layout_form.addStretch()

        btn_refresh = GlyphButton("↻", "刷新预览")
        btn_refresh.clicked.connect(self._schedule_preview)
        preview_panel, preview_layout = self._make_section(
            "实时预览", "调整设置后自动更新预览", btn_refresh
        )

        self._progress = QProgressBar()
        self._progress.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._progress.setTextVisible(True)
        self._progress.setValue(0)
        self._progress.setFormat("等待添加文件")
        preview_layout.addWidget(self._progress)

        self._preview_pane = ScrollPreviewPane()
        preview_layout.addWidget(self._preview_pane, 1)

        body_layout.addWidget(queue_panel, 2)
        body_layout.addWidget(layout_panel, 1)
        body_layout.addWidget(preview_panel, 3)
        shell_layout.addWidget(body, 1)

        self._footnote = FootnoteBar()
        shell_layout.addWidget(self._footnote)

        btn_import.clicked.connect(self._pick_documents)
        btn_remove.clicked.connect(self._drop_selected)
        btn_clear.clicked.connect(self._clear_queue)
        self._export_btn.clicked.connect(self._export_combined_pdf)
        self._orientation_box.currentIndexChanged.connect(self._schedule_preview)
        self._row_slider.on_value_changed(self._schedule_preview)
        self._col_slider.on_value_changed(self._schedule_preview)

    def _wire_menus(self) -> None:
        file_menu = QMenu(self)
        for label, slot, key in (
            ("添加文件", self._pick_documents, "Ctrl+O"),
            ("移除选中", self._drop_selected, "Delete"),
            ("清空列表", self._clear_queue, "Ctrl+Shift+Delete"),
        ):
            action = QAction(label, self)
            action.setShortcut(key)
            action.triggered.connect(slot)
            file_menu.addAction(action)
        file_menu.addSeparator()
        merge_action = QAction("合并文件", self)
        merge_action.setShortcut("Ctrl+M")
        merge_action.triggered.connect(self._export_combined_pdf)
        file_menu.addAction(merge_action)
        file_menu.addSeparator()
        quit_action = QAction("退出", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        help_menu = QMenu(self)
        guide_action = QAction("使用说明", self)
        guide_action.setShortcut("F1")
        guide_action.triggered.connect(self._open_user_guide)
        help_menu.addAction(guide_action)
        about_action = QAction("关于", self)
        about_action.triggered.connect(self._open_about_dialog)
        help_menu.addAction(about_action)

        self._chrome.file_btn.setMenu(file_menu)
        self._chrome.help_btn.setMenu(help_menu)

    def _bind_shortcuts(self) -> None:
        QShortcut(QKeySequence("F1"), self, self._open_user_guide)

    # ------------------------------------------------------------------ 状态

    def _write_log(self, message: str, with_trace: bool = False) -> None:
        if with_trace:
            logging.error("%s\n%s", message, traceback.format_exc())
        else:
            logging.error(message)

    def _update_footnote(self, text: str, tone: str = "ready") -> None:
        self._footnote.set_text(text)
        self._footnote.set_state(tone)

    def _sync_progress_label(self) -> None:
        count = len(self._paths)
        if count == 0:
            self._progress.setValue(0)
            self._progress.setFormat("等待添加文件")
            self._update_footnote("就绪 · 请添加待合并的文件")
        else:
            self._progress.setValue(100)
            self._progress.setFormat(f"已选择 {count} 个文件")
            self._update_footnote(f"已加载 {count} 个文件")

    # ------------------------------------------------------------------ 对话框

    def _open_user_guide(self) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle("使用说明")
        dialog.setMinimumSize(560, 520)
        dialog.resize(600, 560)
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        browser = QTextBrowser()
        browser.setHtml(USER_GUIDE_HTML)
        layout.addWidget(browser)
        close = PulseButton("关闭")
        close.setObjectName("accentButton")
        close.setFixedWidth(100)
        close.clicked.connect(dialog.accept)
        row = QHBoxLayout()
        row.addStretch()
        row.addWidget(close)
        layout.addLayout(row)
        dialog.exec()

    def _open_about_dialog(self) -> None:
        QMessageBox.about(
            self,
            "关于",
            f"{__app_name__}\n\n"
            f"版本：{__version__}\n\n"
            "将多张发票 PDF 或图片按自定义网格排版，合并导出为单个 PDF。\n\n"
            "技术栈：PySide6 · PyMuPDF · Pillow\n\n"
            "支持 Windows / macOS / Linux。",
        )

    # ------------------------------------------------------------------ 文件队列

    def _pick_documents(self) -> None:
        chosen, _ = QFileDialog.getOpenFileNames(
            self, "选择文件", "", SUPPORTED_OPEN_FILTER
        )
        for path in chosen:
            if path not in self._paths:
                self._paths.append(path)
                self._document_queue.addItem(os.path.basename(path))
        self._document_queue.refresh_empty_hint()
        if chosen:
            self._schedule_preview()
        self._sync_progress_label()

    def _drop_selected(self) -> None:
        for item in self._document_queue.selectedItems():
            index = self._document_queue.row(item)
            self._document_queue.takeItem(index)
            self._paths.pop(index)
        self._document_queue.refresh_empty_hint()
        self._schedule_preview()
        self._sync_progress_label()

    def _clear_queue(self) -> None:
        self._paths.clear()
        self._document_queue.clear()
        self._document_queue.refresh_empty_hint()
        self._schedule_preview()
        self._sync_progress_label()

    # ------------------------------------------------------------------ 预览

    def _current_layout(self):
        return (
            self._row_slider.value(),
            self._col_slider.value(),
            self._orientation_box.currentText(),
        )

    def _schedule_preview(self) -> None:
        if not self._paths:
            self._preview_pane.show_placeholder(False)
            return

        if self._preview_job and self._preview_job.isRunning():
            self._preview_job.quit()
            self._preview_job.wait()

        self._progress.setValue(0)
        self._progress.setFormat("正在生成预览...")
        self._update_footnote("正在生成预览...", "busy")

        rows, cols, orientation = self._current_layout()
        self._preview_job = PreviewRenderJob(self._paths, rows, cols, orientation)
        self._preview_job.finished_image.connect(self._on_preview_ready)
        self._preview_job.failed.connect(self._on_preview_failed)
        self._preview_job.finished.connect(self._on_preview_done)
        self._preview_job.start()

    def _on_preview_ready(self, payload: bytes) -> None:
        image = QPixmap()
        image.loadFromData(payload)
        self._preview_pane.apply_preview_image(image)

    def _on_preview_failed(self, message: str) -> None:
        self._write_log(message)
        QMessageBox.warning(self, "警告", message)
        self._preview_pane.show_placeholder(False)
        self._progress.setValue(0)
        self._progress.setFormat("预览生成失败")
        self._update_footnote("预览失败", "error")

    def _on_preview_done(self) -> None:
        self._progress.setValue(100)
        self._progress.setFormat("预览完成")
        self._update_footnote(f"预览就绪 · {len(self._paths)} 个文件", "success")

    # ------------------------------------------------------------------ 导出

    def _export_combined_pdf(self) -> None:
        if not self._paths:
            QMessageBox.warning(self, "警告", "请先添加文件！")
            return

        destination, _ = QFileDialog.getSaveFileName(
            self, "保存合并后的 PDF", "", PDF_SAVE_FILTER
        )
        if not destination:
            return

        if self._export_job and self._export_job.isRunning():
            self._export_job.quit()
            self._export_job.wait()

        self._progress.setValue(0)
        self._progress.setFormat("正在处理文件...")
        self._update_footnote("正在合并文件...", "busy")
        self._export_btn.setEnabled(False)

        rows, cols, orientation = self._current_layout()
        self._export_job = ExportRenderJob(
            self._paths, rows, cols, orientation, destination
        )
        self._export_job.progress.connect(self._on_export_progress)
        self._export_job.succeeded.connect(self._on_export_success)
        self._export_job.failed.connect(self._on_export_failed)
        self._export_job.finished.connect(lambda: self._export_btn.setEnabled(True))
        self._export_job.start()

    def _on_export_progress(self, value: int, label: str) -> None:
        self._progress.setValue(value)
        self._progress.setFormat(label)

    def _on_export_success(self, destination: str) -> None:
        QMessageBox.information(self, "成功", "文件合并完成！")
        self._progress.setValue(100)
        self._progress.setFormat("合并完成")
        self._update_footnote(f"合并完成 · {os.path.basename(destination)}", "success")

    def _on_export_failed(self, message: str) -> None:
        self._write_log(message)
        QMessageBox.critical(self, "错误", message)
        self._progress.setValue(0)
        self._progress.setFormat("合并失败")
        self._update_footnote("合并失败", "error")


def launch() -> None:
    _configure_logging()
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(GLOBAL_STYLESHEET)
    WorkbenchWindow().show()
    sys.exit(app.exec())
