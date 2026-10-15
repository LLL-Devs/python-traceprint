# Project

Traceprint exists to make ad hoc development output easier to follow without
requiring a full observability stack.

## Responsibilities

Traceprint should provide:

- formatted text output with timestamp, elapsed time, cumulative time, labels,
  and nesting depth;
- optional ANSI colors for terminal use;
- manual spans for nested operations;
- a decorator for function-level tracing;
- Python logging handlers that route logging records through tracer formatting.

## Non-goals

Traceprint is not a replacement for structured logging, distributed tracing,
metrics, OpenTelemetry, or production observability infrastructure.

Traceprint should not include unrelated project, pipeline, placeholder, or
filesystem utility functions.

## Identity and supported use

- Distribution: `python-traceprint`; import package: `traceprint`; license: MIT.
- Python 3.12 or later; no runtime dependencies outside the Python standard library.
- Public API maturity: alpha. Repository specification versions and library
  versions are independent; a specification 1.x does not declare the library stable.
- Supported use is ordinary text streams, development scripts, short-lived CLIs
  and Python logging. Callers coordinate shared state and own stream/file cleanup.

The library is a synchronous formatter and a partial text-stream adapter. It is
not a general `TextIOBase` implementation: only `write`, `flush` and the explicitly
specified tracing operations are required. Do not infer `encoding`, `fileno`,
`isatty`, binary writes or a `close` operation on `Tracer` from stream interception.
TTY detection is delegated to the underlying sink during construction/configuration.

## Product structure

The importable package lives under `src/traceprint/`. Its root exports the API
in [API](002_api.md), `colors.py` supplies color constants/conversion, `tracer.py`
supplies tracer/context/logging behavior, and an empty `py.typed` marks typing
support. Private implementation organization may vary while these supported
interfaces and outputs remain equivalent.

The repository also provides tests, two runnable examples, `hatch_build.py`,
`pyproject.toml`, MIT licensing, README/contribution/changelog material and Sphinx
API/usage/release documentation. The latter is a product maintained according to
this package and the Python-library documentation rules. Build and release
requirements are owned by [Library versions and releases](007_release.md).

## Shared-state boundaries

A tracer owns its label stack, depth, timing, enabled/locked flags, sink,
interception captures, attached mirrors and current line state. None of these
is thread-local, task-local or isolated by `contextvars`. Intercepted stdout and
stderr share one sink and one context/line state.

Do not promise concurrent-context isolation, asynchronous coroutine/generator
execution tracing, overlapping tracer installation management or transactional
configuration. Keep enable/lock settings stable while a context is active and
balance manual push/pop operations. Unsupported mutation observations belong to
the [compatibility annex](annex_observed-compatibility.md).
