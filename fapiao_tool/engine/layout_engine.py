"""PDF 排版与合并核心引擎。"""

from __future__ import annotations

import io
import os
import tempfile
from typing import Callable, Iterable, List, Optional, Tuple

import fitz
from PIL import Image

from fapiao_tool.config import (
    CELL_PADDING_RATIO,
    IMAGE_EXPORT_DPI,
    ORIENTATION_LANDSCAPE,
    PREVIEW_RENDER_SCALE,
)


ProgressFn = Optional[Callable[[int, str], None]]


class LayoutEngine:
    """负责素材预处理、网格排版、预览图与最终 PDF 输出。"""

    def __init__(self) -> None:
        self._scratch_paths: List[str] = []

    # ------------------------------------------------------------------ 资源清理

    def release_scratch_files(self) -> None:
        for path in self._scratch_paths:
            try:
                os.unlink(path)
            except OSError:
                pass
        self._scratch_paths.clear()

    def _reserve_temp_pdf(self) -> str:
        handle = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        handle.close()
        self._scratch_paths.append(handle.name)
        return handle.name

    # ------------------------------------------------------------------ 素材转换

    def raster_to_single_page_pdf(self, image_path: str) -> str:
        target = self._reserve_temp_pdf()
        with Image.open(image_path) as frame:
            if frame.mode in ("RGBA", "LA") or (
                frame.mode == "P" and "transparency" in frame.info
            ):
                canvas = Image.new("RGB", frame.size, (255, 255, 255))
                if frame.mode == "P":
                    frame = frame.convert("RGBA")
                mask = frame.split()[3] if frame.mode == "RGBA" else None
                canvas.paste(frame, mask=mask)
                frame = canvas
            elif frame.mode != "RGB":
                frame = frame.convert("RGB")
            frame.save(target, "PDF", resolution=IMAGE_EXPORT_DPI)
        return target

    def extract_pdf_first_page(self, pdf_path: str) -> str:
        target = self._reserve_temp_pdf()
        reader = fitz.open(pdf_path)
        if reader.page_count == 0:
            reader.close()
            raise ValueError("PDF 文件为空")
        writer = fitz.open()
        writer.insert_pdf(reader, from_page=0, to_page=0)
        writer.save(target)
        writer.close()
        reader.close()
        return target

    def normalize_inputs(self, paths: Iterable[str]) -> List[str]:
        normalized: List[str] = []
        for path in paths:
            if path.lower().endswith(".pdf"):
                normalized.append(self.extract_pdf_first_page(path))
            else:
                normalized.append(self.raster_to_single_page_pdf(path))
        return normalized

    # ------------------------------------------------------------------ 页面几何

    @staticmethod
    def resolve_page_size(orientation: str) -> Tuple[float, float]:
        width, height = fitz.paper_size("a4")
        if orientation == ORIENTATION_LANDSCAPE:
            return height, width
        return width, height

    def compose_page(
        self,
        canvas: fitz.Page,
        slot_pdfs: List[str],
        page_width: float,
        page_height: float,
        row_count: int,
        col_count: int,
    ) -> None:
        cell_w = page_width / col_count
        cell_h = page_height / row_count

        for index, slot_pdf in enumerate(slot_pdfs):
            row, col = divmod(index, col_count)
            origin_x = col * cell_w
            origin_y = page_height - (row + 1) * cell_h

            with fitz.open(slot_pdf) as slot_doc:
                if slot_doc.page_count == 0:
                    continue
                bounds = slot_doc[0].rect
                fit_scale = min(
                    (cell_w * CELL_PADDING_RATIO) / bounds.width,
                    (cell_h * CELL_PADDING_RATIO) / bounds.height,
                )
                draw_w = bounds.width * fit_scale
                draw_h = bounds.height * fit_scale
                draw_x = origin_x + (cell_w - draw_w) / 2
                draw_y = origin_y + (cell_h - draw_h) / 2
                canvas.show_pdf_page(
                    fitz.Rect(draw_x, draw_y, draw_x + draw_w, draw_y + draw_h),
                    slot_doc,
                    0,
                )

    # ------------------------------------------------------------------ 对外能力

    def build_merged_document(
        self,
        paths: Iterable[str],
        *,
        row_count: int = 3,
        col_count: int = 2,
        orientation: str = "纵向",
        on_progress: ProgressFn = None,
    ) -> fitz.Document:
        source_list = list(paths)
        if not source_list:
            raise ValueError("没有可处理的文件")

        prepared = []
        total = len(source_list)
        for index, path in enumerate(source_list):
            if path.lower().endswith(".pdf"):
                prepared.append(self.extract_pdf_first_page(path))
            else:
                prepared.append(self.raster_to_single_page_pdf(path))
            if on_progress:
                on_progress(int((index + 1) / total * 50), f"正在处理文件: {index + 1}/{total}")

        page_w, page_h = self.resolve_page_size(orientation)
        slots_per_sheet = row_count * col_count
        output = fitz.open()

        for sheet_start in range(0, len(prepared), slots_per_sheet):
            batch = prepared[sheet_start : sheet_start + slots_per_sheet]
            sheet = output.new_page(width=page_w, height=page_h)
            try:
                self.compose_page(sheet, batch, page_w, page_h, row_count, col_count)
            except Exception as exc:
                raise RuntimeError(f"排版失败：{exc}") from exc

            if on_progress:
                for offset in range(len(batch)):
                    done = sheet_start + offset + 1
                    pct = 50 + int(done / len(prepared) * 50)
                    on_progress(pct, f"正在合并: {done}/{len(prepared)}")

        return output

    def render_preview_bytes(
        self,
        paths: Iterable[str],
        *,
        row_count: int = 3,
        col_count: int = 2,
        orientation: str = "纵向",
    ) -> Optional[bytes]:
        source_list = list(paths)
        if not source_list:
            return None

        prepared = self.normalize_inputs(source_list)
        page_w, page_h = self.resolve_page_size(orientation)
        slots_per_sheet = row_count * col_count

        draft = fitz.open()
        for sheet_start in range(0, len(prepared), slots_per_sheet):
            batch = prepared[sheet_start : sheet_start + slots_per_sheet]
            sheet = draft.new_page(width=page_w, height=page_h)
            try:
                self.compose_page(sheet, batch, page_w, page_h, row_count, col_count)
            except Exception:
                continue

        if draft.page_count == 0:
            draft.close()
            return None

        matrix = fitz.Matrix(PREVIEW_RENDER_SCALE, PREVIEW_RENDER_SCALE)
        frames = []
        for page_index in range(draft.page_count):
            pixmap = draft[page_index].get_pixmap(matrix=matrix, alpha=False)
            frames.append(
                Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
            )
        draft.close()

        gutter = int(12 * PREVIEW_RENDER_SCALE)
        stack_height = sum(img.height for img in frames) + gutter * (len(frames) - 1)
        stack_width = max(img.width for img in frames)
        montage = Image.new("RGB", (stack_width, stack_height), (240, 242, 245))

        cursor_y = 0
        for frame in frames:
            montage.paste(frame, ((stack_width - frame.width) // 2, cursor_y))
            cursor_y += frame.height + gutter

        buffer = io.BytesIO()
        montage.save(buffer, format="PNG")
        return buffer.getvalue()
