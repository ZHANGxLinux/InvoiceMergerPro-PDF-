"""可复用界面控件。"""

from __future__ import annotations

import random
from PySide6.QtWidgets import (
    QFrame, QPushButton, QLabel, QWidget, QHBoxLayout, QVBoxLayout,
    QSlider, QStyledItemDelegate, QStyle, QListWidget, QStyleOptionViewItem,
    QGraphicsDropShadowEffect, QGraphicsOpacityEffect, QSizePolicy,
    QStyleOptionButton, QScrollArea,
)
from PySide6.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, Property, QTimer, QRect, QSize, QPoint, QEvent,
)
from PySide6.QtGui import (
    QPainter, QLinearGradient, QPen, QBrush, QColor, QFont, QPainterPath,
    QRadialGradient, QPixmap, QFontMetrics,
)


ANIM_MS = 220
EASE = QEasingCurve.Type.OutCubic


class GlowShadowMixin:
    def _setup_glow(self, blur=28, offset_y=6, color=QColor(0, 0, 0, 80)):
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(blur)
        self._shadow.setOffset(0, offset_y)
        self._shadow.setColor(color)
        self.setGraphicsEffect(self._shadow)
        self._shadow_anim = None

    def _animate_shadow(self, blur, offset_y, duration=ANIM_MS):
        if self._shadow_anim and self._shadow_anim.state() == QPropertyAnimation.Running:
            self._shadow_anim.stop()
        self._shadow_anim = QPropertyAnimation(self._shadow, b"blurRadius", self)
        self._shadow_anim.setDuration(duration)
        self._shadow_anim.setEasingCurve(EASE)
        self._shadow_anim.setEndValue(blur)
        self._shadow_anim.start()

        off_anim = QPropertyAnimation(self._shadow, b"offset", self)
        off_anim.setDuration(duration)
        off_anim.setEasingCurve(EASE)
        off_anim.setEndValue(QPoint(0, offset_y))
        off_anim.start()


class FrostPanel(QFrame, GlowShadowMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("frostPanel")
        self._lifted = False
        self._setup_glow(blur=24, offset_y=4, color=QColor(0, 0, 0, 100))
        self.setAttribute(Qt.WA_Hover, True)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, False)
        painter.setOpacity(0.035)
        rng = random.Random(42)
        for _ in range(180):
            x = rng.randint(0, max(1, self.width()))
            y = rng.randint(0, max(1, self.height()))
            c = rng.randint(160, 220)
            painter.setPen(QColor(c, c, c, 40))
            painter.drawPoint(x, y)

    def enterEvent(self, event):
        self._lifted = True
        self._animate_shadow(36, 2)
        self.setProperty("hovered", True)
        self.style().unpolish(self)
        self.style().polish(self)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._lifted = False
        self._animate_shadow(24, 4)
        self.setProperty("hovered", False)
        self.style().unpolish(self)
        self.style().polish(self)
        super().leaveEvent(event)


class SectionHeading(QWidget):
    def __init__(self, title, hint="", extra_widget=None, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        accent = QFrame()
        accent.setObjectName("sectionBar")
        accent.setFixedSize(3, 18)

        text_col = QVBoxLayout()
        text_col.setSpacing(2)
        title_lbl = QLabel(title)
        title_lbl.setObjectName("sectionTitle")
        text_col.addWidget(title_lbl)
        if hint:
            hint_lbl = QLabel(hint)
            hint_lbl.setObjectName("sectionHint")
            text_col.addWidget(hint_lbl)

        layout.addWidget(accent, 0, Qt.AlignTop)
        layout.addLayout(text_col, 1)
        if extra_widget:
            layout.addWidget(extra_widget, 0, Qt.AlignTop | Qt.AlignRight)


class ChromaticTitle(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setObjectName("chromaticTitle")
        self._font = QFont("Segoe UI", 18, QFont.Bold)
        self._font.setFamilies(["Segoe UI", "Microsoft YaHei UI"])
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(self._text_height() + 6)

    def _text_height(self):
        return QFontMetrics(self._font).height()

    def _text_width(self):
        return QFontMetrics(self._font).horizontalAdvance(self.text())

    def sizeHint(self):
        return QSize(self._text_width() + 4, self._text_height() + 10)

    def minimumSizeHint(self):
        return QSize(self._text_width() + 4, self._text_height() + 6)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        grad = QLinearGradient(0, 0, max(1, self.width()), 0)
        grad.setColorAt(0.0, QColor("#9061ff"))
        grad.setColorAt(0.5, QColor("#635bff"))
        grad.setColorAt(1.0, QColor("#22b8cf"))
        painter.setPen(QPen(QBrush(grad), 0))
        painter.setFont(self._font)
        painter.drawText(self.rect(), Qt.AlignLeft | Qt.AlignVCenter, self.text())


class BrandMark(QWidget):
    def __init__(self, size=28, parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        grad = QLinearGradient(0, 0, self.width(), self.height())
        grad.setColorAt(0, QColor("#635bff"))
        grad.setColorAt(1, QColor("#9061ff"))
        path = QPainterPath()
        r = self.width() / 2
        path.addRoundedRect(0, 0, self.width(), self.height(), 7, 7)
        p.fillPath(path, grad)
        p.setPen(QPen(QColor(255, 255, 255, 180), 1.2))
        p.drawLine(int(r * 0.55), int(r * 0.5), int(r * 1.45), int(r * 0.5))
        p.drawLine(int(r * 0.55), int(r * 0.85), int(r * 1.45), int(r * 0.85))
        p.drawLine(int(r * 0.55), int(r * 1.2), int(r * 1.15), int(r * 1.2))


class PulseButton(QPushButton, GlowShadowMixin):
    def __init__(self, text="", object_name="", parent=None):
        super().__init__(text, parent)
        if object_name:
            self.setObjectName(object_name)
        self.setCursor(Qt.PointingHandCursor)
        self._scale = 1.0
        self._scale_anim = None
        self._setup_glow(blur=0, offset_y=0, color=QColor(99, 91, 255, 60))
        self._shadow.setEnabled(False)

    def _get_scale(self):
        return self._scale

    def _set_scale(self, value):
        self._scale = value
        self.update()

    scaleFactor = Property(float, _get_scale, _set_scale)

    def enterEvent(self, event):
        self._shadow.setEnabled(True)
        self._animate_shadow(18, 0)
        self._run_scale(1.0, 1.03 if self.objectName() == "accentButton" else 1.02)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._shadow.setEnabled(False)
        self._run_scale(self._scale, 1.0)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self._run_scale(self._scale, 0.97, 80)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        target = 1.03 if self.objectName() == "accentButton" and self.underMouse() else 1.0
        if self.objectName() == "accentButton" and self.underMouse():
            target = 1.03
        elif self.underMouse():
            target = 1.02
        self._run_scale(self._scale, target, 120)
        super().mouseReleaseEvent(event)

    def _run_scale(self, start, end, duration=ANIM_MS):
        if self._scale_anim and self._scale_anim.state() == QPropertyAnimation.Running:
            self._scale_anim.stop()
        self._scale_anim = QPropertyAnimation(self, b"scaleFactor", self)
        self._scale_anim.setDuration(duration)
        self._scale_anim.setEasingCurve(EASE)
        self._scale_anim.setStartValue(start)
        self._scale_anim.setEndValue(end)
        self._scale_anim.start()

    def paintEvent(self, event):
        if abs(self._scale - 1.0) < 0.001:
            super().paintEvent(event)
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.translate(self.width() / 2, self.height() / 2)
        p.scale(self._scale, self._scale)
        p.translate(-self.width() / 2, -self.height() / 2)
        opt = QStyleOptionButton()
        self.initStyleOption(opt)
        self.style().drawControl(QStyle.ControlElement.CE_PushButton, opt, p, self)


class GlyphButton(QPushButton):
    def __init__(self, icon_char, tooltip="", parent=None):
        super().__init__(icon_char, parent)
        self.setObjectName("glyphButton")
        self.setFixedSize(28, 28)
        self.setCursor(Qt.PointingHandCursor)
        if tooltip:
            self.setToolTip(tooltip)


class ChromeButton(QPushButton):
    def __init__(self, text, role="normal", parent=None):
        super().__init__(text, parent)
        self.setObjectName(f"chromeBtn_{role}")
        self.setFixedSize(36, 28)
        self.setCursor(Qt.PointingHandCursor)


class FramelessChrome(QWidget):
    def __init__(self, window, parent=None):
        super().__init__(parent)
        self._window = window
        self._drag_pos = None
        self.setObjectName("framelessChrome")
        self.setFixedHeight(44)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 0, 8, 0)
        layout.setSpacing(10)

        self.logo = BrandMark(26)
        self.title = QLabel("发票合并助手")
        self.title.setObjectName("chromeCaption")
        self.title.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        title_w = self.title.fontMetrics().horizontalAdvance("发票合并助手") + 8
        self.title.setMinimumWidth(title_w)

        layout.addWidget(self.logo)
        layout.addWidget(self.title)
        layout.addSpacing(16)

        self.file_btn = QPushButton("文件")
        self.file_btn.setObjectName("menuLinkBtn")
        self.help_btn = QPushButton("帮助")
        self.help_btn.setObjectName("menuLinkBtn")
        layout.addWidget(self.file_btn)
        layout.addWidget(self.help_btn)
        layout.addStretch()

        self.min_btn = ChromeButton("—", "min")
        self.max_btn = ChromeButton("□", "max")
        self.close_btn = ChromeButton("×", "close")
        layout.addWidget(self.min_btn)
        layout.addWidget(self.max_btn)
        layout.addWidget(self.close_btn)

        self.min_btn.clicked.connect(self._window.showMinimized)
        self.max_btn.clicked.connect(self._toggle_maximize)
        self.close_btn.clicked.connect(self._window.close)

    def _toggle_maximize(self):
        if self._window.isMaximized():
            self._window.showNormal()
            self.max_btn.setText("□")
        else:
            self._window.showMaximized()
            self.max_btn.setText("❐")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self._window.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() & Qt.LeftButton:
            if self._window.isMaximized():
                self._window.showNormal()
                self.max_btn.setText("□")
            self._window.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        self._toggle_maximize()


class QueueItemRenderer(QStyledItemDelegate):
    def paint(self, painter, option, index):
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)
        rect = option.rect.adjusted(4, 2, 4, 2)
        is_selected = option.state & QStyle.State_Selected
        is_hover = option.state & QStyle.State_MouseOver

        if is_selected or is_hover:
            bg = QLinearGradient(rect.topLeft(), rect.bottomRight())
            if is_selected:
                bg.setColorAt(0, QColor(99, 91, 255, 55))
                bg.setColorAt(1, QColor(34, 184, 207, 25))
            else:
                bg.setColorAt(0, QColor(255, 255, 255, 12))
                bg.setColorAt(1, QColor(99, 91, 255, 18))
            path = QPainterPath()
            path.addRoundedRect(rect, 6, 6)
            painter.fillPath(path, bg)

        if is_selected:
            bar = QRect(rect.left(), rect.top() + 4, 3, rect.height() - 8)
            bar_grad = QLinearGradient(bar.topLeft(), bar.bottomLeft())
            bar_grad.setColorAt(0, QColor("#635bff"))
            bar_grad.setColorAt(1, QColor("#9061ff"))
            painter.fillRect(bar, bar_grad)

        text_rect = rect.adjusted(14 if is_selected else 10, 0, -8, 0)
        painter.setPen(QColor("#e8ecf4" if is_selected else "#b8c0d0"))
        font = QFont("Segoe UI", 12)
        font.setFamilies(["Segoe UI", "Microsoft YaHei UI"])
        painter.setFont(font)
        painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft, index.data())
        painter.restore()

    def sizeHint(self, option, index):
        return QSize(option.rect.width(), 36)


class QueueEmptyHint(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self._glow = 0.4
        self._glow_dir = 1
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._pulse)
        self._timer.start(40)

    def _pulse(self):
        self._glow += 0.012 * self._glow_dir
        if self._glow >= 0.85:
            self._glow_dir = -1
        elif self._glow <= 0.35:
            self._glow_dir = 1
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        cx, cy = self.width() // 2, self.height() // 2 - 10

        glow = QRadialGradient(cx, cy, 80)
        glow.setColorAt(0, QColor(99, 91, 255, int(40 * self._glow)))
        glow.setColorAt(1, QColor(99, 91, 255, 0))
        p.setBrush(glow)
        p.setPen(Qt.NoPen)
        p.drawEllipse(cx - 80, cy - 80, 160, 160)

        pen = QPen(QColor(99, 91, 255, int(100 + 60 * self._glow)), 1.4)
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        doc = QRect(cx - 42, cy - 50, 84, 100)
        p.drawRoundedRect(doc, 6, 6)
        p.drawLine(doc.left() + 14, doc.top() + 22, doc.right() - 14, doc.top() + 22)
        p.drawLine(doc.left() + 14, doc.top() + 38, doc.right() - 14, doc.top() + 38)
        p.drawLine(doc.left() + 14, doc.top() + 54, doc.right() - 30, doc.top() + 54)

        p.setPen(QColor(100, 110, 130, 160))
        font = QFont("Segoe UI", 11)
        font.setFamilies(["Segoe UI", "Microsoft YaHei UI"])
        p.setFont(font)
        p.drawText(QRect(0, cy + 62, self.width(), 24), Qt.AlignCenter, "点击「添加文件」开始导入")


class DocumentQueue(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("documentQueue")
        self.setItemDelegate(QueueItemRenderer(self))
        self.setSpacing(2)
        self._placeholder = QueueEmptyHint(self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._placeholder.setGeometry(self.viewport().rect())

    def refresh_empty_hint(self):
        self._placeholder.setVisible(self.count() == 0)
        self._placeholder.raise_()


class GridDimensionSlider(QWidget):
    valueChanged = None

    def __init__(self, label, minimum=1, maximum=8, value=1, parent=None):
        super().__init__(parent)
        self._label_text = label
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        row = QHBoxLayout()
        lbl = QLabel(label)
        lbl.setObjectName("formCaption")
        self.value_label = QLabel(str(value))
        self.value_label.setObjectName("dimensionValue")
        self.value_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        row.addWidget(lbl)
        row.addStretch()
        row.addWidget(self.value_label)
        layout.addLayout(row)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setObjectName("violetSlider")
        self.slider.setMinimum(minimum)
        self.slider.setMaximum(maximum)
        self.slider.setValue(value)
        self.slider.valueChanged.connect(self._on_change)
        layout.addWidget(self.slider)

    def _on_change(self, v):
        self.value_label.setText(str(v))

    def value(self):
        return self.slider.value()

    def setValue(self, v):
        self.slider.setValue(v)

    def on_value_changed(self, slot):
        self.slider.valueChanged.connect(slot)


class ScrollPreviewPane(QWidget):
    """可滚动的预览面板：空状态文案居中；有内容时按宽度缩放、纵向滚动。"""

    PAD = 10

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("scrollPreview")
        self._source_pixmap = None
        self._document_visible = False

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        self.scroll = QScrollArea()
        self.scroll.setObjectName("previewViewport")
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.container = QWidget()
        self.container.setObjectName("previewCanvas")
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(self.PAD, self.PAD, self.PAD, self.PAD)
        self.container_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.image_label = QLabel("添加文件后将在此显示预览")
        self.image_label.setObjectName("previewStage")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setWordWrap(True)
        self.container_layout.addWidget(self.image_label)

        self.scroll.setWidget(self.container)
        outer.addWidget(self.scroll)

        self.scroll.viewport().installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj is self.scroll.viewport() and event.type() == QEvent.Resize:
            QTimer.singleShot(0, self._on_viewport_resize)
        return super().eventFilter(obj, event)

    def _viewport_size(self):
        return self.scroll.viewport().size()

    def _on_viewport_resize(self):
        if self._document_visible:
            self._apply_scale()
        else:
            self._layout_empty()

    def _layout_empty(self):
        vp = self._viewport_size()
        inner_w = max(80, vp.width() - self.PAD * 2)
        inner_h = max(80, vp.height() - self.PAD * 2)
        self.container.setMinimumSize(vp.width(), vp.height())
        self.container.setMaximumSize(QSize(16777215, 16777215))
        self.image_label.setPixmap(QPixmap())
        self.image_label.setText("添加文件后将在此显示预览")
        self.image_label.setProperty("showingDocument", False)
        self.image_label.style().unpolish(self.image_label)
        self.image_label.style().polish(self.image_label)
        self.image_label.setMinimumSize(inner_w, inner_h)
        self.image_label.setMaximumSize(QSize(16777215, 16777215))
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def _apply_scale(self):
        if not self._source_pixmap or self._source_pixmap.isNull():
            return
        vp = self._viewport_size()
        fit_w = max(80, vp.width() - self.PAD * 2)
        dpr = self.devicePixelRatioF()
        target_px = max(1, int(fit_w * dpr))
        src = self._source_pixmap

        # 只缩小不放大，避免二次插值导致模糊
        if src.width() > target_px:
            scaled = src.scaledToWidth(target_px, Qt.SmoothTransformation)
            scaled.setDevicePixelRatio(dpr)
        else:
            scaled = src

        logical_w = int(scaled.width() / scaled.devicePixelRatio())
        logical_h = int(scaled.height() / scaled.devicePixelRatio())

        self.container.setMinimumSize(0, 0)
        self.image_label.setText("")
        self.image_label.setProperty("showingDocument", True)
        self.image_label.style().unpolish(self.image_label)
        self.image_label.style().polish(self.image_label)
        self.image_label.setPixmap(scaled)
        self.image_label.setFixedSize(logical_w, logical_h)
        self.image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.container.adjustSize()

    def show_placeholder(self, has_content):
        self._document_visible = has_content
        if not has_content:
            self._source_pixmap = None
            self._layout_empty()

    def apply_preview_image(self, pixmap):
        self._document_visible = True
        self._source_pixmap = pixmap
        self._apply_scale()
        self.scroll.verticalScrollBar().setValue(0)
        self.scroll.horizontalScrollBar().setValue(0)

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(0, self._on_viewport_resize)


class FootnoteBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("footnoteBar")
        self.setFixedHeight(30)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(8)

        self.dot = QLabel()
        self.dot.setObjectName("statusDot")
        self.dot.setFixedSize(8, 8)
        self.text = QLabel("就绪")
        self.text.setObjectName("statusText")
        layout.addWidget(self.dot)
        layout.addWidget(self.text)
        layout.addStretch()
        self.set_state("ready")

    def set_text(self, text):
        self.text.setText(text)

    def set_state(self, state):
        colors = {
            "ready": "#34d399",
            "busy": "#22b8cf",
            "error": "#ff4757",
            "success": "#34d399",
        }
        color = colors.get(state, "#64748b")
        self.dot.setStyleSheet(
            f"background-color: {color}; border-radius: 4px;"
        )
