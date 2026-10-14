from __future__ import annotations

import io
import logging
import sys
from pathlib import Path

import pytest

from traceprint import Tracer, TracerFileHandler, TracerHandler
from traceprint.tracer import ANSI_ESCAPE_PATTERN


@pytest.mark.parametrize("stdout,stderr", [(True, False), (False, True), (True, True)])
def test_install_is_idempotent_and_restores_streams(stdout: bool, stderr: bool) -> None:
    original_stdout, original_stderr = sys.stdout, sys.stderr
    stream = io.StringIO()
    tracer = Tracer(stream=stream, use_colors=False)
    try:
        tracer.install(stdout=stdout, stderr=stderr)
        tracer.install(stdout=stdout, stderr=stderr)
        if stdout:
            print("stdout message")
        if stderr:
            print("stderr message", file=sys.stderr)
    finally:
        tracer.uninstall()
    tracer.uninstall()
    assert sys.stdout is original_stdout
    assert sys.stderr is original_stderr
    assert "message" in stream.getvalue()


def test_logging_formats_arguments_and_exception() -> None:
    stream = io.StringIO()
    handler = TracerHandler(tracer_instance=Tracer(stream=stream, use_colors=False))
    logger = logging.Logger("traceprint-test")
    logger.addHandler(handler)
    try:
        raise ValueError("failure context")
    except ValueError:
        logger.exception("operation %s failed", "load")
    assert "operation load failed" in stream.getvalue()
    assert "ValueError: failure context" in stream.getvalue()
    handler.close()


@pytest.mark.parametrize("mirror", [False, True])
@pytest.mark.parametrize(
    "message",
    ["\x1b[31mred\x1b[0m", "\x1b]8;;https://example.com\x1b\\red\x1b]8;;\x1b\\"],
)
def test_file_output_strips_ansi(tmp_path: Path, mirror: bool, message: str) -> None:
    path = tmp_path / "trace.log"
    tracer = Tracer(stream=io.StringIO(), use_colors=True)
    handler = TracerFileHandler(path, tracer_instance=tracer)
    try:
        if mirror:
            tracer.add_file_handler(handler)
            tracer.write(message + "\n")
            tracer.flush()
        else:
            handler.handle(
                logging.LogRecord("test", logging.INFO, "", 0, message, (), None)
            )
        output = path.read_text()
        assert "red" in output
        assert "\x1b" not in output
        assert tracer.use_colors is True
    finally:
        tracer.remove_file_handler(handler)
        handler.close()
    assert handler.stream is None


def test_mirrored_print_preserves_fragments_and_indentation(tmp_path: Path) -> None:
    stream = io.StringIO()
    tracer = Tracer(
        stream=stream,
        use_colors=True,
        use_tabulation=True,
        output_format="[{label_full}] {original_message}",
    )
    path = tmp_path / "trace.log"
    handler = TracerFileHandler(path)
    tracer.add_file_handler(handler)
    try:
        tracer.install()
        with tracer.span("load"):
            print("hello", "world")
        tracer.flush()
        assert path.read_text() == "[load/>]     hello world\n"
        assert path.read_text() == ANSI_ESCAPE_PATTERN.sub("", stream.getvalue())
    finally:
        tracer.uninstall()
        tracer.remove_file_handler(handler)
        handler.close()
