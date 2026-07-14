"""后台线程：预览渲染与 PDF 导出。"""

from __future__ import annotations

from typing import List

from PySide6.QtCore import QThread, Signal

from fapiao_tool.engine import LayoutEngine


class PreviewRenderJob(QThread):
    finished_image = Signal(bytes)
    failed = Signal(str)

    def __init__(
        self,
        paths: List[str],
        row_count: int,
        col_count: int,
        orientation: str,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._paths = paths.copy()
        self._rows = row_count
        self._cols = col_count
        self._orientation = orientation
        self._engine = LayoutEngine()

    def run(self) -> None:
        try:
            payload = self._engine.render_preview_bytes(
                self._paths,
                row_count=self._rows,
                col_count=self._cols,
                orientation=self._orientation,
            )
            if payload:
                self.finished_image.emit(payload)
        except Exception as exc:
            self.failed.emit(f"预览生成失败：{exc}")
        finally:
            self._engine.release_scratch_files()


class ExportRenderJob(QThread):
    succeeded = Signal(str)
    progress = Signal(int, str)
    failed = Signal(str)

    def __init__(
        self,
        paths: List[str],
        row_count: int,
        col_count: int,
        orientation: str,
        destination: str,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._paths = paths.copy()
        self._rows = row_count
        self._cols = col_count
        self._orientation = orientation
        self._destination = destination
        self._engine = LayoutEngine()

    def run(self) -> None:
        try:
            def report(value: int, label: str) -> None:
                self.progress.emit(value, label)

            document = self._engine.build_merged_document(
                self._paths,
                row_count=self._rows,
                col_count=self._cols,
                orientation=self._orientation,
                on_progress=report,
            )
            document.save(self._destination)
            document.close()
            self.succeeded.emit(self._destination)
        except Exception as exc:
            self.failed.emit(f"文件合并失败：{exc}")
        finally:
            self._engine.release_scratch_files()
