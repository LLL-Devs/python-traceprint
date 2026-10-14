from __future__ import annotations

import io
import sys

import pytest

from traceprint import Tracer, trace, tracer
from traceprint.tracer import ANSI_ESCAPE_PATTERN


def test_import_does_not_intercept_stdout() -> None:
    assert sys.stdout is not tracer


def test_write_formats_message_without_colors() -> None:
    stream = io.StringIO()
    tracer = Tracer(stream=stream, use_colors=False)

    tracer.write("hello\n")

    output = stream.getvalue()
    assert "hello" in output
    assert "+0." in output


def test_span_adds_label_context() -> None:
    stream = io.StringIO()
    tracer = Tracer(stream=stream, use_colors=False)

    with tracer.span("outer"):
        tracer.write("inside\n")

    assert "[outer/>]" in stream.getvalue()


def test_trace_decorator_uses_given_tracer() -> None:
    stream = io.StringIO()
    tracer = Tracer(stream=stream, use_colors=False)

    @trace(tracer_instance=tracer)
    def run() -> None:
        tracer.write("inside\n")

    run()

    assert "[run/>]" in stream.getvalue()


def test_timestamp_is_aware_utc() -> None:
    tracer = Tracer(
        stream=io.StringIO(),
        use_colors=False,
        timestamp_format="%z",
        output_format="{timestamp} {original_message}",
    )
    assert tracer.format("hello") == "+0000 hello"


def test_span_restores_context_after_exception() -> None:
    tracer = Tracer(stream=io.StringIO(), use_colors=False)
    try:
        with tracer.span("failure"):
            raise ValueError("expected")
    except ValueError:
        pass
    assert tracer.depth == 0
    assert tracer.labels == []


def test_print_formats_each_line_once() -> None:
    stream = io.StringIO()
    target = Tracer(
        stream=stream, use_colors=False, output_format="[trace] {original_message}"
    )
    print("hello", "world", file=target)
    print("one", "two", sep="/", end="!", file=target, flush=True)
    assert stream.getvalue() == "[trace] hello world\n[trace] one/two!"


def test_partial_writes_are_immediate_and_flush_keeps_line_context() -> None:
    stream = io.StringIO()
    target = Tracer(
        stream=stream, use_colors=True, output_format="[trace] {original_message}"
    )
    assert target.write("first") == 5
    assert ANSI_ESCAPE_PATTERN.sub("", stream.getvalue()) == "[trace] first"
    target.flush()
    assert target.write(" part\nnext\n\nlast") == 16
    assert ANSI_ESCAPE_PATTERN.sub("", stream.getvalue()) == (
        "[trace] first part\n[trace] next\n\n[trace] last"
    )


@pytest.mark.parametrize("use_colors", [False, True])
@pytest.mark.parametrize("metacolor", [None, "\x1b[90m"])
def test_indentation_is_independent_of_colors(
    use_colors: bool, metacolor: str | None
) -> None:
    target = Tracer(
        stream=io.StringIO(),
        use_colors=use_colors,
        use_tabulation=True,
        metacolor=metacolor,
        output_format="[trace] {original_message}",
    )
    with target.span("outer"):
        text = ANSI_ESCAPE_PATTERN.sub("", target.format("message"))
    expected = "[trace]     message" if metacolor else "    [trace] message"
    assert text == expected


def test_filtered_fragments_do_not_start_an_output_line() -> None:
    stream = io.StringIO()
    target = Tracer(
        stream=stream,
        use_colors=False,
        filter_levels=[0],
        output_format="[trace] {original_message}",
    )
    with target.span("hidden"):
        target.write("hidden")
    target.write("visible\n")
    assert stream.getvalue() == "[trace] visible\n"


def test_reenabling_midline_does_not_insert_metadata() -> None:
    stream = io.StringIO()
    target = Tracer(
        stream=stream, use_colors=False, output_format="[trace] {original_message}"
    )
    target.disable()
    target.write("raw")
    target.enable()
    target.write(" continuation\nnext\n")
    assert stream.getvalue() == "raw continuation\n[trace] next\n"


@pytest.mark.parametrize("ending", ["\n", "\r", "\r\n"])
def test_line_endings_reset_the_prefix_and_preserve_text(ending: str) -> None:
    stream = io.StringIO()
    target = Tracer(
        stream=stream, use_colors=False, output_format="[trace] {original_message}"
    )
    target.write("first" + ending + "next" + ending)
    assert stream.getvalue() == f"[trace] first{ending}[trace] next{ending}"
