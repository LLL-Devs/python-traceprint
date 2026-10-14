"""Trace-friendly stdout and logging helpers."""

from __future__ import annotations

import functools
import logging
import os
import re
import sys
import time
from collections.abc import Callable, Iterable
from contextlib import AbstractContextManager
from datetime import UTC, datetime
from pathlib import Path
from types import TracebackType
from typing import IO, Any, TextIO

from traceprint.colors import DARK_GREY, DEFAULT_COLORS, RESET

ANSI_ESCAPE_PATTERN = re.compile(
    r"\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)"  # OSC, including hyperlinks
    r"|\x1b\[[0-?]*[ -/]*[@-~]"  # CSI, including colors and cursor controls
    r"|\x1b[ -/]*[@-Z\\-_]"  # Other terminal escape sequences
)
DEFAULT_OUTPUT_FORMAT = (
    "[{timestamp}][{cumulative}][{elapsed}][{label_full}] {original_message}"
)

DepthFilter = range | Iterable[int] | Callable[[int], bool] | None


class Tracer:
    """Format text output with timing, labels, nesting, and optional colors."""

    def __init__(
        self,
        *,
        use_colors: bool | None = None,
        use_tabulation: bool = False,
        color_scheme: list[str] | None = None,
        metacolor: str | None = DARK_GREY,
        print_transitions: bool = False,
        filter_levels: DepthFilter = None,
        start_enabled: bool = True,
        output_format: str = DEFAULT_OUTPUT_FORMAT,
        timestamp_format: str = "%Y-%m-%d %H:%M:%S",
        stream: TextIO | None = None,
        error_stream: TextIO | None = None,
        intercept_stdout: bool = False,
        intercept_stderr: bool = False,
    ) -> None:
        self._stream = stream or sys.stdout
        self._stream_explicit = stream is not None
        self._error_stream = error_stream or sys.stderr
        self._error_stream_explicit = error_stream is not None
        self._orig_stdout: TextIO | None = None
        self._orig_stderr: TextIO | None = None
        self._intercept_stdout = False
        self._intercept_stderr = False

        if use_colors is None:
            use_colors = self._stream.isatty()
        self.use_colors = use_colors
        self.use_tabulation = use_tabulation
        self.color_scheme = color_scheme or DEFAULT_COLORS
        self.metacolor = metacolor
        self.print_transitions = print_transitions
        self.filter_levels = filter_levels
        self.output_format = output_format
        self.timestamp_format = timestamp_format

        self.depth = 0
        self.labels: list[str] = []
        self._last_time = time.perf_counter()
        self._start_time = self._last_time
        self._locked = False
        self._enabled = start_enabled
        self._line_started = False
        self._file_handlers: list[TracerFileHandler] = []

        if intercept_stdout or intercept_stderr:
            self.install(stdout=intercept_stdout, stderr=intercept_stderr)

    @property
    def enabled(self) -> bool:
        """Return whether formatting is currently enabled."""
        return self._enabled

    def install(self, *, stdout: bool = True, stderr: bool = False) -> None:
        """Install this tracer as ``sys.stdout`` and optionally ``sys.stderr``."""
        if stdout and not self._intercept_stdout:
            self._orig_stdout = sys.stdout
            if not self._stream_explicit:
                self._stream = sys.stdout
            sys.stdout = self
            self._intercept_stdout = True
        if stderr and not self._intercept_stderr:
            self._orig_stderr = sys.stderr
            if not stdout and not self._stream_explicit:
                self._stream = sys.stderr
            sys.stderr = self
            self._intercept_stderr = True

    def uninstall(self) -> None:
        """Restore streams captured by :meth:`install`."""
        if self._intercept_stdout and self._orig_stdout is not None:
            sys.stdout = self._orig_stdout
        if self._intercept_stderr and self._orig_stderr is not None:
            sys.stderr = self._orig_stderr
        self._intercept_stdout = False
        self._intercept_stderr = False
        self._orig_stdout = None
        self._orig_stderr = None

    def enable(self) -> None:
        """Enable formatted output and depth tracking."""
        self._enabled = True

    def disable(self) -> None:
        """Disable formatted output and forward text to the underlying stream."""
        self._enabled = False

    def lock(self) -> None:
        """Prevent further depth changes."""
        self._locked = True

    def unlock(self) -> None:
        """Allow depth changes."""
        self._locked = False

    def configure(self, **kwargs: Any) -> None:
        """Update tracer configuration after initialization."""
        if "intercept_stdout" in kwargs or "intercept_stderr" in kwargs:
            stdout = bool(kwargs.pop("intercept_stdout", self._intercept_stdout))
            stderr = bool(kwargs.pop("intercept_stderr", self._intercept_stderr))
            self.uninstall()
            self.install(stdout=stdout, stderr=stderr)

        if "use_colors" in kwargs:
            value = kwargs.pop("use_colors")
            self.use_colors = self._stream.isatty() if value is None else bool(value)

        if "color_scheme" in kwargs:
            value = kwargs.pop("color_scheme")
            self.color_scheme = value or DEFAULT_COLORS

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"Tracer has no attribute {key}")

    def add_file_handler(self, handler: TracerFileHandler) -> None:
        """Mirror formatted stream writes to a file handler."""
        self._file_handlers.append(handler)

    def remove_file_handler(self, handler: TracerFileHandler) -> None:
        """Stop mirroring formatted stream writes to a file handler."""
        if handler in self._file_handlers:
            self._file_handlers.remove(handler)

    def format(self, message: str) -> str:
        """Format a single message without writing it."""
        now = time.perf_counter()
        elapsed = now - self._last_time
        cumulative = now - self._start_time
        self._last_time = now

        label_full = "/".join(self.labels) if self.labels else ""
        label = self.labels[-1] if self.labels else ""
        if label_full and not (message.startswith(">") or message.startswith("<")):
            label_full = f"{label_full}/>"
            label = f"{label}/>"

        text = self.output_format.format(
            timestamp=datetime.now(UTC).strftime(self.timestamp_format),
            cumulative=f"{cumulative:.3f}s",
            elapsed=f"+{elapsed:.3f}s",
            label=label,
            label_full=label_full,
            original_message=message,
        )

        indent = ("    " * self.depth) if self.use_tabulation else ""
        line_color = self.color_scheme[self.depth % len(self.color_scheme)]
        if not self.metacolor:
            if not self.use_colors:
                return indent + text
            return f"{line_color}{indent}{text}{RESET}"

        split_index = text.find(message)
        if split_index == -1:
            if not self.use_colors:
                return indent + text
            return f"{self.metacolor}{indent}{text}{RESET}"

        meta_part = text[:split_index]
        msg_part = text[split_index:]
        if not self.use_colors:
            return meta_part + indent + msg_part
        return (
            f"{self.metacolor}{meta_part}{RESET}{line_color}{indent}{msg_part}{RESET}"
        )

    def write(self, data: str) -> int:
        """Write immediately, adding metadata once per nonblank output line."""
        if not self._enabled:
            self._stream.write(data)
            if data:
                self._line_started = not data.endswith(("\n", "\r"))
            return len(data)

        for chunk in data.splitlines(keepends=True):
            if self._filter_out():
                continue
            message = chunk.rstrip("\r\n")
            ending = chunk[len(message) :]
            if message.strip():
                if not self._line_started:
                    formatted = self.format(message)
                elif self.use_colors:
                    color = self.color_scheme[self.depth % len(self.color_scheme)]
                    formatted = f"{color}{message}{RESET}"
                else:
                    formatted = message
                self._write_raw(formatted + ending)
                self._line_started = True
            else:
                self._write_raw(chunk)
            if ending:
                self._line_started = False
        return len(data)

    def flush(self) -> None:
        """Flush the underlying stream and attached file handlers."""
        self._stream.flush()
        for handler in self._file_handlers:
            handler.flush()

    def push(self, label: str | None = None) -> None:
        """Increase depth and optionally record a label."""
        if not self._enabled:
            return
        if not self._locked:
            self.depth += 1
            self.labels.append(label or f"level{self.depth}")
        if label and self.print_transitions and not self._filter_out():
            self.write(f"> {label}\n")

    def pop(self, label: str | None = None) -> None:
        """Decrease depth and remove the most recent label."""
        if not self._enabled:
            return
        popped = None
        if not self._locked and self.depth > 0:
            self.depth -= 1
            popped = self.labels.pop()
        transition_label = label or popped
        if transition_label and self.print_transitions and not self._filter_out():
            self.write(f"< {transition_label}\n")

    def span(self, label: str) -> Span:
        """Create a context-managed labeled span."""
        return Span(self, label)

    def _filter_out(self) -> bool:
        if self.filter_levels is None:
            return False
        if isinstance(self.filter_levels, range):
            return self.depth not in self.filter_levels
        if callable(self.filter_levels):
            return not self.filter_levels(self.depth)
        return self.depth not in self.filter_levels

    def _write_raw(self, data: str) -> None:
        self._stream.write(data)
        for handler in self._file_handlers:
            handler.write(data)


class Span(AbstractContextManager["Span"]):
    """Context manager for tracer labels and depth."""

    def __init__(self, tracer_instance: Tracer, label: str) -> None:
        self.tracer = tracer_instance
        self.label = label

    def __enter__(self) -> Span:
        if self.tracer.enabled:
            if self.tracer.print_transitions and not self.tracer._filter_out():
                self.tracer.write(f"> {self.label}\n")
            if not self.tracer._locked:
                self.tracer.depth += 1
                self.tracer.labels.append(self.label)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        if self.tracer.enabled:
            if not self.tracer._locked:
                self.tracer.depth -= 1
                self.tracer.labels.pop()
            if self.tracer.print_transitions and not self.tracer._filter_out():
                suffix = f" [failed: {exc_type.__name__}]" if exc_type else ""
                self.tracer.write(f"< {self.label}{suffix}\n")
        return None


def trace(
    _func: Callable[..., Any] | None = None,
    *,
    label: str | None = None,
    force: bool = False,
    tracer_instance: Tracer | None = None,
) -> Callable[..., Any]:
    """Decorate a function so calls are reflected in tracer depth and labels."""

    target = tracer_instance or tracer

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not target.enabled:
                return func(*args, **kwargs)

            entry_label = label or func.__name__
            filtered = target._filter_out()
            if target.print_transitions and (not filtered or force):
                target.write(f"> {entry_label}()\n")
            if not target._locked:
                target.depth += 1
                target.labels.append(entry_label)
            try:
                return func(*args, **kwargs)
            finally:
                if not target._locked:
                    target.depth -= 1
                    target.labels.pop()
                if target.print_transitions and (not filtered or force):
                    target.write(f"< {entry_label}()\n")

        return wrapper

    if _func is None:
        return decorator
    return decorator(_func)


class TracerHandler(logging.Handler):
    """A logging handler that writes records through a tracer."""

    def __init__(
        self,
        level: int = logging.NOTSET,
        *,
        tracer_instance: Tracer | None = None,
    ) -> None:
        super().__init__(level=level)
        self.tracer = tracer_instance

    def emit(self, record: logging.LogRecord) -> None:
        try:
            target = self.tracer or tracer
            target.write(self.format(record) + "\n")
        except Exception:
            self.handleError(record)


class TracerFileHandler(logging.Handler):
    """A logging handler that writes trace-formatted records to a file."""

    def __init__(
        self,
        filename: str | os.PathLike[str],
        mode: str = "a",
        level: int = logging.NOTSET,
        encoding: str = "utf-8",
        *,
        tracer_instance: Tracer | None = None,
    ) -> None:
        super().__init__(level=level)
        self.filename = Path(filename)
        self.mode = mode
        self.encoding = encoding
        self.tracer = tracer_instance
        self.stream: IO[str] | None = None
        self._open_file()

    def emit(self, record: logging.LogRecord) -> None:
        try:
            if self.stream is None:
                self._open_file()
            if self.stream is None:
                return

            target = self.tracer or tracer
            original_use_colors = target.use_colors
            target.use_colors = False
            try:
                full_msg = target.format(self.format(record))
            finally:
                target.use_colors = original_use_colors

            self.write(full_msg + "\n")
            self.stream.flush()
        except Exception:
            self.handleError(record)

    def write(self, data: str) -> None:
        """Write already-formatted tracer output directly to the file."""
        if self.stream is None:
            self._open_file()
        if self.stream is not None:
            self.stream.write(ANSI_ESCAPE_PATTERN.sub("", data))

    def flush(self) -> None:
        if self.stream is not None:
            self.stream.flush()

    def close(self) -> None:
        """Close the file and release the standard logging handler."""
        if self.stream is not None:
            try:
                self.stream.close()
            finally:
                self.stream = None
        super().close()

    def _open_file(self) -> None:
        self.filename.parent.mkdir(parents=True, exist_ok=True)
        self.stream = self.filename.open(self.mode, encoding=self.encoding)


class _LoggerProxy:
    def __init__(self, owner: LoggerMixin) -> None:
        self._owner = owner

    def log(self, level: int, msg: object, *args: Any, **kwargs: Any) -> None:
        if self._owner.verbose:
            self._owner.logger.log(level, msg, *args, **kwargs)

    def debug(self, msg: object, *args: Any, **kwargs: Any) -> None:
        self.log(logging.DEBUG, msg, *args, **kwargs)

    def info(self, msg: object, *args: Any, **kwargs: Any) -> None:
        self.log(logging.INFO, msg, *args, **kwargs)

    def warning(self, msg: object, *args: Any, **kwargs: Any) -> None:
        self.log(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg: object, *args: Any, **kwargs: Any) -> None:
        self.log(logging.ERROR, msg, *args, **kwargs)

    def critical(self, msg: object, *args: Any, **kwargs: Any) -> None:
        self.log(logging.CRITICAL, msg, *args, **kwargs)


class LoggerMixin:
    """Mixin that provides an instance logger exposed as ``self.log``."""

    def __init__(
        self,
        *,
        verbose: bool = True,
        logging_level: int = logging.INFO,
        logging_passthrough: bool = False,
        lazy_init: bool = False,
    ) -> None:
        self.verbose = verbose
        self.logging_level = logging_level
        self.logging_passthrough = logging_passthrough
        self.lazy_init = lazy_init
        self._logger: logging.Logger | None = None
        self._log_proxy = _LoggerProxy(self)
        if not self.lazy_init:
            self._ensure_logger()

    @property
    def logger(self) -> logging.Logger:
        """Return the shared class-named standard logger."""
        self._ensure_logger()
        assert self._logger is not None
        return self._logger

    @property
    def log(self) -> _LoggerProxy:
        """Return the logging proxy gated by this instance's verbose flag."""
        self._ensure_logger()
        return self._log_proxy

    def _ensure_logger(self) -> None:
        if self._logger is not None:
            return

        self._logger = logging.getLogger(
            f"{self.__class__.__module__}.{self.__class__.__name__}"
        )
        self._logger.setLevel(self.logging_level)

        if self.logging_passthrough:
            self._logger.handlers.clear()
            tracer_handler = TracerHandler()
            root_logger = logging.getLogger()
            if root_logger.handlers:
                tracer_handler.setFormatter(root_logger.handlers[0].formatter)
            self._logger.addHandler(tracer_handler)
            self._logger.propagate = False


tracer = Tracer()

_initial_labels = os.environ.get("TRACEPRINT_INITIAL_LABELS", "").strip()
if _initial_labels:
    for _label in _initial_labels.split("/"):
        if stripped := _label.strip():
            tracer.push(stripped)
