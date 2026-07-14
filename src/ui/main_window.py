import sys
import os
import logging
import traceback
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFileDialog, QComboBox, QMessageBox, QScrollArea, QProgressBar,
    QFrame, QDialog, QTextBrowser, QMenu, QListWidget,
)
from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtGui import QPixmap, QAction, QShortcut, QKeySequence
from src.core.pdf_merger import PDFMergerCore
from src.ui.styles import APP_STYLESHEET, HELP_HTML
from src.ui.widgets import (
    GlassCard, CardHeader, GradientLabel, CustomTitleBar,
    InteractiveButton, IconButton, FileListPanel, ValueSlider,
    PreviewPanel, StatusBarWidget,
)


log_file = 'pdf_merger_error.log'
logging.basicConfig(
    filename=log_file,
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class PreviewWorker(QThread):
    preview_ready = Signal(bytes)
    progress_updated = Signal(int, str)
    error_occurred = Signal(str)

    def __init__(self, files, rows, cols, orientation):
        super().__init__()
        self.files = files.copy()
        self.rows = rows
        self.cols = cols
        self.orientation = orientation
        self.core = PDFMergerCore()

    def run(self):
        try:
            img_data = self.core.generate_preview_image(
                self.files,
                rows=self.rows,
                cols=self.cols,
                orientation=self.orientation
            )
            if img_data:
                self.preview_ready.emit(img_data)
        except Exception as e:
            self.error_occurred.emit(f'预览生成失败：{str(e)}')
        finally:
            self.core.cleanup_temp_files()


class MergeWorker(QThread):
    merge_completed = Signal(str)
    progress_updated = Signal(int, str)
    error_occurred = Signal(str)

    def __init__(self, files, rows, cols, orientation, output_file):
        super().__init__()
        self.files = files.copy()
        self.rows = rows
        self.cols = cols
        self.orientation = orientation
        self.output_file = output_file
        self.core = PDFMergerCore()

    def run(self):
        try:
            def progress_callback(value, text):
                self.progress_updated.emit(value, text)

            output_doc = self.core.merge_files(
                self.files,
                rows=self.rows,
                cols=self.cols,
                orientation=self.orientation,
                progress_callback=progress_callback
            )

            output_doc.save(self.output_file)
            output_doc.close()
            self.merge_completed.emit(self.output_file)
        except Exception as e:
            self.error_occurred.emit(f'文件合并失败：{str(e)}')
        finally:
            self.core.cleanup_temp_files()


class PDFMergerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.files = []
        self.preview_worker = None
        self.merge_worker = None
        self.initUI()
        self.setup_shortcuts()

    def log_error(self, error_msg, exc_info=None):
        if exc_info:
            logging.error(f"{error_msg}\n{traceback.format_exc()}")
        else:
            logging.error(error_msg)

    def _build_card(self, title, hint="", extra=None):
        card = GlassCard()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(14)
        layout.addWidget(CardHeader(title, hint, extra))
        divider = QFrame()
        divider.setObjectName("cardDivider")
        divider.setFrameShape(QFrame.HLine)
        layout.addWidget(divider)
        return card, layout

    def initUI(self):
        self.setWindowTitle('发票合并助手')
        self.setMinimumSize(1100, 720)
        self.resize(1280, 820)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        root = QWidget()
        root.setObjectName("centralRoot")
        self.setCentralWidget(root)
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.title_bar = CustomTitleBar(self)
        root_layout.addWidget(self.title_bar)
        self.setup_title_menus()

        hero = QFrame()
        hero.setObjectName("heroFrame")
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(28, 22, 28, 22)
        hero_layout.setSpacing(6)
        hero_layout.addWidget(GradientLabel('发票合并助手'))
        subtitle = QLabel(
            '批量导入 · <span style="color:#22b8cf;">智能排版</span> · 一键合并 PDF 发票'
        )
        subtitle.setObjectName("appSubtitle")
        subtitle.setTextFormat(Qt.RichText)
        hero_layout.addWidget(subtitle)
        root_layout.addWidget(hero)

        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(24, 20, 24, 20)
        content_layout.setSpacing(20)

        files_card, files_layout = self._build_card(
            '文件列表', '支持 PDF、JPG、PNG 等格式'
        )
        self.file_list = FileListPanel()
        self.file_list.setSelectionMode(QListWidget.ExtendedSelection)
        files_layout.addWidget(self.file_list, 1)

        file_btn_layout = QHBoxLayout()
        file_btn_layout.setSpacing(8)
        add_button = InteractiveButton('添加文件')
        add_button.setObjectName("addFileBtn")
        remove_button = InteractiveButton('移除选中')
        remove_button.setObjectName("neutralBtn")
        remove_all_button = InteractiveButton('清空全部')
        remove_all_button.setObjectName("dangerButton")
        file_btn_layout.addWidget(add_button)
        file_btn_layout.addWidget(remove_button)
        file_btn_layout.addWidget(remove_all_button)
        files_layout.addLayout(file_btn_layout)

        settings_card, settings_layout = self._build_card(
            '排版设置', '调整页面方向与每页布局'
        )

        orient_label = QLabel('页面方向')
        orient_label.setObjectName("fieldLabel")
        settings_layout.addWidget(orient_label)
        self.orientation = QComboBox()
        self.orientation.addItems(['纵向', '横向'])
        settings_layout.addWidget(self.orientation)

        grid_label = QLabel('每页文件数')
        grid_label.setObjectName("fieldLabel")
        settings_layout.addWidget(grid_label)

        self.rows_slider = ValueSlider('行数', minimum=1, maximum=8, value=3)
        self.cols_slider = ValueSlider('列数', minimum=1, maximum=8, value=2)
        settings_layout.addWidget(self.rows_slider)
        settings_layout.addWidget(self.cols_slider)

        settings_layout.addSpacing(12)
        self.merge_button = InteractiveButton('PDF  合并并导出')
        self.merge_button.setObjectName("primaryButton")
        settings_layout.addWidget(self.merge_button)
        settings_layout.addStretch()

        refresh_btn = IconButton('↻', '刷新预览')
        refresh_btn.clicked.connect(self.update_preview)
        preview_card, preview_layout = self._build_card(
            '实时预览', '调整设置后自动更新预览', refresh_btn
        )

        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("等待添加文件")
        preview_layout.addWidget(self.progress_bar)

        self.preview_panel = PreviewPanel()
        preview_layout.addWidget(self.preview_panel, 1)

        content_layout.addWidget(files_card, 2)
        content_layout.addWidget(settings_card, 1)
        content_layout.addWidget(preview_card, 3)
        root_layout.addWidget(content, 1)

        self.status_bar = StatusBarWidget()
        root_layout.addWidget(self.status_bar)

        add_button.clicked.connect(self.add_files)
        remove_button.clicked.connect(self.remove_files)
        remove_all_button.clicked.connect(self.remove_all_files)
        self.merge_button.clicked.connect(self.merge_files)
        self.orientation.currentIndexChanged.connect(self.update_preview)
        self.rows_slider.connect_changed(self.update_preview)
        self.cols_slider.connect_changed(self.update_preview)

        self.file_list.update_placeholder()

    def setup_title_menus(self):
        file_menu = QMenu(self)

        add_action = QAction('添加文件', self)
        add_action.setShortcut('Ctrl+O')
        add_action.triggered.connect(self.add_files)
        file_menu.addAction(add_action)

        remove_action = QAction('移除选中', self)
        remove_action.setShortcut('Delete')
        remove_action.triggered.connect(self.remove_files)
        file_menu.addAction(remove_action)

        clear_action = QAction('清空列表', self)
        clear_action.setShortcut('Ctrl+Shift+Delete')
        clear_action.triggered.connect(self.remove_all_files)
        file_menu.addAction(clear_action)

        file_menu.addSeparator()

        merge_action = QAction('合并文件', self)
        merge_action.setShortcut('Ctrl+M')
        merge_action.triggered.connect(self.merge_files)
        file_menu.addAction(merge_action)

        file_menu.addSeparator()

        quit_action = QAction('退出', self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        help_menu = QMenu(self)

        guide_action = QAction('使用说明', self)
        guide_action.setShortcut('F1')
        guide_action.triggered.connect(self.show_help)
        help_menu.addAction(guide_action)

        about_action = QAction('关于', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        self.title_bar.file_btn.setMenu(file_menu)
        self.title_bar.help_btn.setMenu(help_menu)

    def setup_shortcuts(self):
        QShortcut(QKeySequence('F1'), self, self.show_help)

    def _set_status(self, text, state='ready'):
        self.status_bar.set_text(text)
        self.status_bar.set_state(state)

    def show_help(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('使用说明')
        dialog.setMinimumSize(560, 520)
        dialog.resize(600, 560)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        browser = QTextBrowser()
        browser.setOpenExternalLinks(False)
        browser.setHtml(HELP_HTML)
        layout.addWidget(browser)

        close_btn = InteractiveButton('关闭')
        close_btn.setObjectName("primaryButton")
        close_btn.setFixedWidth(100)
        close_btn.clicked.connect(dialog.accept)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

        dialog.exec()

    def show_about(self):
        QMessageBox.about(
            self,
            '关于',
            '发票合并助手\n\n'
            '版本：1.2\n\n'
            '将多张发票 PDF 或图片按自定义网格排版，合并导出为单个 PDF。\n\n'
            '技术栈：\n'
            '· 界面：PySide6 (Qt Fusion)\n'
            '· PDF 处理：PyMuPDF (fitz)\n'
            '· 图片转换：Pillow\n\n'
            '跨平台桌面应用，支持 Windows / macOS / Linux。'
        )

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "选择文件",
            "",
            "支持的文件 (*.pdf *.jpg *.jpeg *.png *.tif *.bmp)"
        )
        for file in files:
            if file not in self.files:
                self.files.append(file)
                self.file_list.addItem(os.path.basename(file))
        self.file_list.update_placeholder()
        if files:
            self.update_preview()
        self.update_progress_bar()

    def remove_files(self):
        for item in self.file_list.selectedItems():
            idx = self.file_list.row(item)
            self.file_list.takeItem(idx)
            self.files.pop(idx)
        self.file_list.update_placeholder()
        self.update_preview()
        self.update_progress_bar()

    def remove_all_files(self):
        self.files.clear()
        self.file_list.clear()
        self.file_list.update_placeholder()
        self.update_preview()
        self.update_progress_bar()

    def update_progress_bar(self):
        total_files = len(self.files)
        if total_files == 0:
            self.progress_bar.setValue(0)
            self.progress_bar.setFormat("等待添加文件")
            self._set_status('就绪 · 请添加待合并的文件', 'ready')
        else:
            self.progress_bar.setValue(100)
            self.progress_bar.setFormat(f"已选择 {total_files} 个文件")
            self._set_status(f'已加载 {total_files} 个文件', 'ready')

    def update_preview(self):
        if not self.files:
            self.preview_panel.set_has_content(False)
            return

        if self.preview_worker and self.preview_worker.isRunning():
            self.preview_worker.quit()
            self.preview_worker.wait()

        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("正在生成预览...")
        self._set_status('正在生成预览...', 'busy')

        self.preview_worker = PreviewWorker(
            self.files,
            rows=self.rows_slider.value(),
            cols=self.cols_slider.value(),
            orientation=self.orientation.currentText()
        )
        self.preview_worker.preview_ready.connect(self.on_preview_ready)
        self.preview_worker.error_occurred.connect(self.on_preview_error)
        self.preview_worker.finished.connect(self.on_preview_finished)
        self.preview_worker.start()

    def on_preview_ready(self, img_data):
        qimg = QPixmap()
        qimg.loadFromData(img_data)
        self.preview_panel.set_preview_pixmap(qimg)

    def on_preview_error(self, error_msg):
        self.log_error(error_msg)
        QMessageBox.warning(self, '警告', error_msg)
        self.preview_panel.set_has_content(False)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("预览生成失败")
        self._set_status('预览失败', 'error')

    def on_preview_finished(self):
        self.progress_bar.setValue(100)
        self.progress_bar.setFormat("预览完成")
        self._set_status(f'预览就绪 · {len(self.files)} 个文件', 'success')

    def merge_files(self):
        if not self.files:
            QMessageBox.warning(self, '警告', '请先添加文件！')
            return

        output_file, _ = QFileDialog.getSaveFileName(
            self,
            "保存合并后的PDF",
            "",
            "PDF文件 (*.pdf)"
        )

        if not output_file:
            return

        if self.merge_worker and self.merge_worker.isRunning():
            self.merge_worker.quit()
            self.merge_worker.wait()

        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("正在处理文件...")
        self._set_status('正在合并文件...', 'busy')
        self.merge_button.setEnabled(False)

        self.merge_worker = MergeWorker(
            self.files,
            rows=self.rows_slider.value(),
            cols=self.cols_slider.value(),
            orientation=self.orientation.currentText(),
            output_file=output_file
        )
        self.merge_worker.merge_completed.connect(self.on_merge_completed)
        self.merge_worker.progress_updated.connect(self.on_merge_progress)
        self.merge_worker.error_occurred.connect(self.on_merge_error)
        self.merge_worker.finished.connect(self.on_merge_finished)
        self.merge_worker.start()

    def on_merge_progress(self, value, text):
        self.progress_bar.setValue(value)
        self.progress_bar.setFormat(text)

    def on_merge_completed(self, output_file):
        QMessageBox.information(self, '成功', '文件合并完成！')
        self.progress_bar.setValue(100)
        self.progress_bar.setFormat("合并完成")
        self._set_status(f'合并完成 · {os.path.basename(output_file)}', 'success')

    def on_merge_error(self, error_msg):
        self.log_error(error_msg)
        QMessageBox.critical(self, '错误', error_msg)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("合并失败")
        self._set_status('合并失败', 'error')

    def on_merge_finished(self):
        self.merge_button.setEnabled(True)


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(APP_STYLESHEET)

    merger = PDFMergerWindow()
    merger.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
