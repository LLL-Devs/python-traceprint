# Interception

Traceprint may replace process streams only when the caller explicitly requests
that behavior.

## Installation

`Tracer.install()` should install a tracer as `sys.stdout` and optionally as
`sys.stderr`.

`Tracer.uninstall()` should restore streams previously captured by that tracer.

Installation and cleanup should be safe enough for tests, CLIs, and short-lived
scripts.

## Formatting

Formatted output should preserve the original message text and add metadata
around it. Color should be optional and disabled by default when the output
stream is not a TTY.

File output should not include ANSI escape sequences unless a future explicit
option requests it.

