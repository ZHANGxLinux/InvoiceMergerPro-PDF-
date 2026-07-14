import pathlib

root = pathlib.Path(__file__).parent
src = (root / "src/ui/widgets.py").read_text(encoding="utf-8")
pairs = [
    ("GlassCard", "FrostPanel"),
    ("CardHeader", "SectionHeading"),
    ("GradientLabel", "ChromaticTitle"),
    ("AppLogoWidget", "BrandMark"),
    ("InteractiveButton", "PulseButton"),
    ("IconButton", "GlyphButton"),
    ("TitleBarButton", "ChromeButton"),
    ("CustomTitleBar", "FramelessChrome"),
    ("FileListDelegate", "QueueItemRenderer"),
    ("EmptyFilePlaceholder", "QueueEmptyHint"),
    ("FileListPanel", "DocumentQueue"),
    ("ValueSlider", "GridDimensionSlider"),
    ("PreviewPanel", "ScrollPreviewPane"),
    ("StatusBarWidget", "FootnoteBar"),
    ('setObjectName("glassCard")', 'setObjectName("frostPanel")'),
    ('setObjectName("gradientTitle")', 'setObjectName("chromaticTitle")'),
    ('setObjectName("customTitleBar")', 'setObjectName("framelessChrome")'),
    ('setObjectName("titleBarName")', 'setObjectName("chromeCaption")'),
    ('setObjectName("menuTextBtn")', 'setObjectName("menuLinkBtn")'),
    ('setObjectName(f"titleBtn_{role}")', 'setObjectName(f"chromeBtn_{role}")'),
    ('objectName() == "primaryButton"', 'objectName() == "accentButton"'),
    ('setObjectName("primaryButton")', 'setObjectName("accentButton")'),
    ('setObjectName("addFileBtn")', 'setObjectName("importButton")'),
    ('setObjectName("neutralBtn")', 'setObjectName("mutedButton")'),
    ('setObjectName("dangerButton")', 'setObjectName("warnButton")'),
    ('setObjectName("iconButton")', 'setObjectName("glyphButton")'),
    ('setObjectName("fileList")', 'setObjectName("documentQueue")'),
    ('setObjectName("fieldLabel")', 'setObjectName("formCaption")'),
    ('setObjectName("sliderValue")', 'setObjectName("dimensionValue")'),
    ('setObjectName("gradientSlider")', 'setObjectName("violetSlider")'),
    ('setObjectName("previewPanel")', 'setObjectName("scrollPreview")'),
    ('setObjectName("previewScroll")', 'setObjectName("previewViewport")'),
    ('setObjectName("previewContainer")', 'setObjectName("previewCanvas")'),
    ('setObjectName("previewPlaceholder")', 'setObjectName("previewStage")'),
    ('setProperty("hasPaper", False)', 'setProperty("showingDocument", False)'),
    ('setProperty("hasPaper", True)', 'setProperty("showingDocument", True)'),
    ('setObjectName("statusBarWidget")', 'setObjectName("footnoteBar")'),
    ('setObjectName("cardAccent")', 'setObjectName("sectionBar")'),
    ('setObjectName("cardTitle")', 'setObjectName("sectionTitle")'),
    ('setObjectName("cardHint")', 'setObjectName("sectionHint")'),
    ('setObjectName("cardDivider")', 'setObjectName("sectionRule")'),
    ("def set_has_content", "def show_placeholder"),
    ("def set_preview_pixmap", "def apply_preview_image"),
    ("def update_placeholder", "def refresh_empty_hint"),
    ("def connect_changed", "def on_value_changed"),
    ("self._has_content", "self._document_visible"),
]
for old, new in pairs:
    src = src.replace(old, new)
header = '"""可复用界面控件。"""\n\nfrom __future__ import annotations\n\n'
out = root / "fapiao_tool/interface/controls/panels.py"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(header + src, encoding="utf-8")
