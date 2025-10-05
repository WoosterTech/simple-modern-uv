import logging
import sys
from collections.abc import Mapping
from dataclasses import dataclass, field
from importlib.util import find_spec
from types import TracebackType
from typing import TYPE_CHECKING, TypeAlias, cast, final

from .settings import settings

if TYPE_CHECKING:
    from rich.console import Console
    from rich.theme import Theme

# ---- Custom TRACE level ----------------------------------------------------
TRACE_LEVEL_NUM = 5
logging.addLevelName(TRACE_LEVEL_NUM, "TRACE")

_SysExcInfoType: TypeAlias = (
    tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None]
)
_ExcInfoType: TypeAlias = None | bool | _SysExcInfoType | BaseException
_ArgsType: TypeAlias = tuple[object, ...] | Mapping[str, object]


def trace(
    self: logging.Logger,
    msg: str,
    *args: object,
    exc_info: _ExcInfoType = None,
    stack_info: bool = False,
    stacklevel: int = 1,
    extra: Mapping[str, object] | None = None,
) -> None:
    """
    Log a message with severity 'TRACE'.

    This method logs a message at the TRACE level, which is typically used for
    very detailed diagnostic information that is only of interest when diagnosing
    problems.

    Args:
        msg (str): The message format string.
        *args: Variable length argument list for message formatting.
        **kwargs: Arbitrary keyword arguments passed to the underlying logging method.

    Note:
        The message is only processed if the logger's effective level allows
        TRACE level messages.
    """
    if self.isEnabledFor(TRACE_LEVEL_NUM):
        self._log(TRACE_LEVEL_NUM, msg, args, exc_info, extra, stack_info, stacklevel)


logging.Logger.trace = trace  # pyright: ignore[reportAttributeAccessIssue]

if TYPE_CHECKING:

    @final
    class MyLogger(logging.Logger):
        trace = trace


@dataclass
class GlobalConsole:
    console: "Console | None" = None
    theme: "Theme | None" = None
    _configured: bool = field(default=False, init=False, repr=False)
    rich: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        if self.console is not None:
            self.configure()

    def enforce_imports(self) -> None:
        if not find_spec("rich"):
            raise ImportError("Rich is required for rich logging. Please install it.")

        self.rich = True

    def configure(self, theme: "Theme | None" = None) -> None:
        if self._configured:
            return

        self.enforce_imports()
        from rich.console import Console

        if theme is not None:
            self.theme = theme
        self.console = Console(stderr=True, force_terminal=True, theme=self.theme)
        self._configured = True

    @property
    def is_configured(self) -> bool:
        return self._configured


_console = GlobalConsole()
_configured = False


# ---- Core setup ------------------------------------------------------------
def setup_logging(rich_tracebacks: bool = True) -> None:
    """
    Set up application-wide logging.
    Defaults come from settings (DEBUG → DEBUG level).
    LOG_LEVEL env var still overrides.
    """
    global _configured

    # Resolve level: LOG_LEVEL env > settings.default_log_level
    level_name = settings.log_level.upper() if settings.log_level else None
    level: int = (
        getattr(logging, level_name, settings.default_log_level)
        if level_name
        else settings.default_log_level
    )

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()

    try:
        global _console

        if _console.is_configured:
            return

        from rich.logging import RichHandler
        from rich.theme import Theme

        console_theme = Theme({"logging.level.trace": "dim"})
        _console.configure(theme=console_theme)

        handler = RichHandler(
            rich_tracebacks=rich_tracebacks,
            markup=True,
            show_time=True,
            show_level=True,
            show_path=False,
            tracebacks_show_locals=True,
            console=_console.console,
        )
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)

    except ImportError:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)

    root.addHandler(handler)

    if _console.rich:
        from rich.traceback import install

        _ = install(show_locals=True, console=_console.console)

    _configured = True


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.

    Args:
        name (str): The name of the logger to retrieve.

    Returns:
        logging.Logger: The logger instance with the specified name.
    """
    if not _configured:
        setup_logging()

    return cast("MyLogger", logging.getLogger(name))


# ---- Utility for custom levels --------------------------------------------
def add_log_level(name: str, level_num: int) -> None:
    if hasattr(logging, name.lower()):
        raise ValueError(f"Logging already has a '{name}' method.")

    name = name.strip().upper()
    if " " in name:
        raise ValueError("Log level name must not contain spaces.")

    logging.addLevelName(level_num, name)

    def log_for_level(
        self: logging.Logger,
        msg: str,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ):
        if self.isEnabledFor(level_num):
            self._log(
                level_num,
                msg,
                args,
                exc_info=exc_info,
                stack_info=stack_info,
                stacklevel=stacklevel,
                extra=extra,
            )

    setattr(logging.Logger, name.lower(), log_for_level)
