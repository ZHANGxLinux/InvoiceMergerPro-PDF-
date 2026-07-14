"""应用级常量与路径配置。"""

from fapiao_tool import __app_name__, __version__

APP_TITLE = __app_name__
APP_VERSION = __version__

LOG_FILENAME = "runtime_error.log"
ERROR_LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"
ERROR_LOG_DATEFMT = "%Y-%m-%d %H:%M:%S"

SUPPORTED_OPEN_FILTER = "支持的文件 (*.pdf *.jpg *.jpeg *.png *.tif *.bmp)"
PDF_SAVE_FILTER = "PDF 文件 (*.pdf)"

DEFAULT_ROW_COUNT = 3
DEFAULT_COL_COUNT = 2
GRID_MIN = 1
GRID_MAX = 8

ORIENTATION_PORTRAIT = "纵向"
ORIENTATION_LANDSCAPE = "横向"

PREVIEW_RENDER_SCALE = 2.0
CELL_PADDING_RATIO = 0.95
IMAGE_EXPORT_DPI = 300.0

WINDOW_MIN_WIDTH = 1100
WINDOW_MIN_HEIGHT = 720
WINDOW_DEFAULT_WIDTH = 1280
WINDOW_DEFAULT_HEIGHT = 820
