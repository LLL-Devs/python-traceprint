# Traceprint specification package

This package describes Traceprint specifically: a Python library for readable
print and logging traces with timing, labels, nesting depth, and explicit stream
interception.

## Scope

- Traceprint's public purpose and non-goals.
- Public API expectations.
- Stream interception behavior.
- Logging integration behavior.
- Independent library version and release expectations.

Generic Python library rules belong in `python-library-1`.

## Vocabulary

- **Tracer**: an object that formats text output with trace metadata.
- **Span**: a labeled depth context.
- **Transition**: an optional entry or exit line for a span or decorated
  function.
- **Interception**: replacing a process stream such as `sys.stdout` with a
  tracer by explicit caller request.

## Reading order

1. [Project](project.md)
2. [API](api.md)
3. [Interception](interception.md)
4. [Library versions and releases](release.md)

