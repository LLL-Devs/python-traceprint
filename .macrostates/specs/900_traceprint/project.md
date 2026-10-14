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

