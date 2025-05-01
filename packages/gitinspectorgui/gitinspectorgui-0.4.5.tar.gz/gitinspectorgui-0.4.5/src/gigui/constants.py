import os
import sys

if sys.platform == "darwin":
    # macOS, Macbook Pro 16
    MAX_COL_HEIGHT = 532  # height of options column
    WINDOW_SIZE_Y = 800  # height of GUI window
    WINDOW_SIZE_X = 660  # width of GUI window
else:
    # Windows, Linux
    MAX_COL_HEIGHT = 526  # height op settings column
    WINDOW_SIZE_Y = 740  # height of window
    WINDOW_SIZE_X = 670  # width of window

WINDOW_HEIGHT_CORR = 45  # height correction: height of command buttons + title bar
INIT_COL_PERCENT = 75  # ratio of other layout vs multiline, default 4 : 1
ENABLED_COLOR = ("white", "#082567")
DISABLED_COLOR = ("grey", "#082567")
INVALID_INPUT_COLOR = "#FD9292"
VALID_INPUT_COLOR = "#FFFFFF"
OPTION_TITLE_WIDTH = 13  # width of the column of text items before the option lines

# GUI option settings
REPO_HINT = "<repo-name>"
PARENT_HINT = "<repo-parent-folder>"

# GUI and CLI defaults
DEFAULT_FILE_BASE = "gitinspect"
SUBDIR_NESTING_DEPTH = 5
DEFAULT_N_FILES = 5
DEFAULT_COPY_MOVE = 1
DEFAULT_VERBOSITY = 0
DEFAULT_EXTENSIONS = [
    "c",
    "cc",
    "cif",
    "cpp",
    "glsl",
    "h",
    "hh",
    "hpp",
    "java",
    "js",
    "py",
    "rb",
    "sql",
    "ts",
]

# Output options
NONE = "none"
AUTO = "auto"
DYNAMIC_BLAME_HISTORY = "dynamic-blame-history"
VIEW_OPTIONS = [AUTO, DYNAMIC_BLAME_HISTORY, NONE]
HTML = "html"
EXCEL = "excel"
FILE_FORMATS = [HTML, EXCEL]

# Output settings web browser
MAX_BROWSER_TABS = 20
PORT_VALUE = 8080

# Output settings Excel
ABBREV_CNT = 30

# Constants for CLI arguments, GUI options and settings
PREFIX = "prefix"
POSTFIX = "postfix"
NOFIX = "nofix"
FIX_TYPE = [PREFIX, POSTFIX, NOFIX]

REMOVE = "remove"
HIDE = "hide"
SHOW = "show"
BLAME_EXCLUSION_CHOICES = [HIDE, SHOW, REMOVE]
BLAME_EXCLUSIONS_DEFAULT = HIDE

MAX_THREAD_WORKERS = 6
GIT_LOG_CHUNK_SIZE = 100  # no errors for 400 for website/main repo (394 files)
BLAME_CHUNK_SIZE = (
    20  # 80 will lead to "too many open files" error for website/main repo
)

LIMIT_CORE_WORKERS = 16
# 1 if os.cpu_count() is None, copied from ProcessPoolExecutor in concurrent.futures
CPU_COUNT = os.cpu_count() or 1
MAX_CORE_WORKERS = min(CPU_COUNT, LIMIT_CORE_WORKERS)


# Debugging
DEBUG_SHOW_MAIN_EVENT_LOOP = False
DEBUG_MULTIPROCESSING = False
ALLOW_GITPYTHON_DEBUG = True
DEBUG_WERKZEUG_SERVER = False
