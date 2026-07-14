import pathlib

root = pathlib.Path(__file__).parent
src = (root / "src/ui/styles.py").read_text(encoding="utf-8")
pairs = [
    ("APP_STYLESHEET", "GLOBAL_STYLESHEET"),
    ("HELP_HTML", "USER_GUIDE_HTML"),
    ("#centralRoot", "#workbenchRoot"),
    ("#customTitleBar", "#framelessChrome"),
    ("#titleBarName", "#chromeCaption"),
    ("#menuTextBtn", "#menuLinkBtn"),
    ("#titleBtn_", "#chromeBtn_"),
    ("#heroFrame", "#bannerStrip"),
    ("#appSubtitle", "#bannerCaption"),
    ("#glassCard", "#frostPanel"),
    ("#cardAccent", "#sectionBar"),
    ("#cardTitle", "#sectionTitle"),
    ("#cardHint", "#sectionHint"),
    ("#cardDivider", "#sectionRule"),
    ("#fileList", "#documentQueue"),
    ("#addFileBtn", "#importButton"),
    ("#neutralBtn", "#mutedButton"),
    ("#dangerButton", "#warnButton"),
    ("#primaryButton", "#accentButton"),
    ("#iconButton", "#glyphButton"),
    ("#fieldLabel", "#formCaption"),
    ("#sliderValue", "#dimensionValue"),
    ("#gradientSlider", "#violetSlider"),
    ("#previewPanel", "#scrollPreview"),
    ("#previewScroll", "#previewViewport"),
    ("#previewContainer", "#previewCanvas"),
    ("#previewPlaceholder", "#previewStage"),
    ('[hasPaper="true"]', '[showingDocument="true"]'),
    ("#statusBarWidget", "#footnoteBar"),
    ('from src.ui.styles import APP_STYLESHEET, HELP_HTML', ""),
]
for old, new in pairs:
    src = src.replace(old, new)
# remove HELP_HTML block at end - we'll import from help_content
cut = src.find("\nUSER_GUIDE_HTML = ")
if cut != -1:
    src = src[:cut] + "\n"
header = '"""全局 QSS 主题。"""\n\n'
(root / "fapiao_tool/interface/visual_theme.py").write_text(header + src, encoding="utf-8")
