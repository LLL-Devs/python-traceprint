# API

Traceprint's public API should be small and explicit.

## Public imports

The package root should expose:

- `Tracer`;
- `tracer`;
- `trace`;
- `TracerHandler`;
- `TracerFileHandler`;
- `LoggerMixin`.

## Global tracer

The package may provide a global `tracer` instance for convenience. The global
instance must not intercept process streams merely because the package was
imported.

## Environment variables

`TRACEPRINT_INITIAL_LABELS` may seed the global tracer's label stack with
slash-separated labels at import time.

Environment-variable behavior should stay limited and documented because it is
part of the process-level API.

