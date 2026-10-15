# Logging and file output

## Stream logging handler

`TracerHandler` subclasses `logging.Handler`. Initialize the base handler with
the supplied level (default `logging.NOTSET`) and retain the optional tracer.
Omitting a tracer selects the global tracer at emission time.

For each `emit(record)`, use the handler's standard `format(record)` to render
the record, append a newline, then call the selected tracer's `write`. This keeps
normal logging parameter substitution, custom formatters and exception text.
Multiline records follow the tracer's ordinary chunk formatting/filtering rules.
Do not force a flush, change tracer configuration or automatically install streams.

Catch ordinary `Exception` failures during emission and call `handleError(record)`;
standard logging controls diagnostic reporting. Do not swallow `BaseException`
such as `KeyboardInterrupt`/`SystemExit`. Level/filter handling belongs to the
standard logging call path; direct `emit` itself does not recheck the handler level.

## File handler

`TracerFileHandler` is a `logging.Handler` with constructor defaults in [API](002_api.md).
Retain public attributes `filename` as a `Path`, `mode`, `encoding`, optional
`tracer`, and `stream` as the opened text file or `None` when closed.

Construction initializes the base level, creates the filename's parent directories
with parents/existing-directory support, and opens the text file immediately using
the requested mode and encoding. Default mode is append, default encoding UTF-8.
Constructor filesystem/encoding/mode errors propagate. Opening is not lazy.
Use ordinary platform text-mode newline translation; there is no custom newline
parameter or cross-platform byte-normalization layer.

There are two use routes:

1. **Logging emission:** select the configured/global tracer; reopen if closed;
   temporarily set the tracer's `use_colors` to false; call the tracer's `format`
   on the standard handler-formatted record; restore the original color value in
   `finally`; call the file handler's direct `write` with a trailing newline;
   flush the file. Catch ordinary emission errors with `handleError(record)`.
2. **Mirroring/direct write:** accept already-formatted text without adding
   metadata, indentation or newline. Reopen if closed, strip terminal escapes and
   write to the file. Do not flush automatically. Direct-write errors propagate.

Unlike stream-handler emission, file-handler emission calls `format`, not tracer
`write`. It therefore advances tracer timing but does not use its line state,
enabled flag, depth-output filter or mirror list. It does not print to the console.
Do not combine both routes for the same record unless duplicate output is wanted.

`flush` flushes an open file and is a no-op when closed. `close` closes the current
file, sets `stream = None` even if file closing raises, and invokes the base
logging handler's close after a successful file close. Close does not detach the
handler from a logger or tracer. A later write/emission reopens with the original
mode; in `"w"` mode that reopening truncates earlier contents.

## Terminal escape stripping

File output must remove ANSI escapes from both tracer-added formatting and the
original message, including color controls and OSC hyperlinks, preserving ordinary
visible text. Apply these regular-expression alternatives with Python `re.sub`
and an empty replacement:

```text
\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)
\x1b\[[0-?]*[ -/]*[@-~]
\x1b[ -/]*[@-Z\\-_]
```

The alternatives respectively match OSC ending in BEL or ESC-backslash, CSI,
and other terminal escape sequences. This specifies the existing matching profile,
not a complete terminal emulator or Unicode/control-character sanitizer. Do not
strip ANSI from console output or remove text inside a valid hyperlink.

## Logger mixin

`LoggerMixin` exposes public `verbose`, `logging_level`, `logging_passthrough`
and `lazy_init` attributes with the keyword-only defaults in [API](002_api.md).
Construction creates the verbosity proxy; initialize the underlying logger
immediately unless `lazy_init=True`.
The mixin initializer does not automatically initialize later classes in a
cooperative inheritance chain; subclasses own any additional parent setup.

First logger initialization:

1. Obtain `logging.getLogger(f"{class.__module__}.{class.__name__}")` for the
   concrete instance class and set its level to the current `logging_level`.
2. If passthrough is true, clear that logger's handlers without closing them;
   create a `TracerHandler` targeting the global tracer; if the root logger has
   handlers, copy the first root handler's formatter to it (possibly `None`);
   attach the new tracer handler and set propagation to false.
3. Cache the logger. Subsequent accesses return it without reinitialization.

Both `.logger` and `.log` properties ensure this initialization, including when
`verbose=False`. Instances of the same concrete class share the standard logger
name/handlers/level, though each has its own proxy and initialization cache. A
later instance can therefore change the shared logger's configuration.

When passthrough is false, leave existing handlers/propagation unchanged; still
set the level on first initialization. Later changes to `logging_level`,
`logging_passthrough` or `lazy_init` do not automatically reconfigure an already
initialized logger. The caller may configure the standard `.logger` directly.

The proxy reads `owner.verbose` at each call. If falsey, do not submit the record;
if truthy, forward `logger.log(level, msg, *args, **kwargs)` without extra formatting
or tracing. Convenience methods use standard DEBUG/INFO/WARNING/ERROR/CRITICAL
levels. Return `None`; standard logging level/filter rules still apply. Direct
`.logger` calls bypass the verbose gate.

## Ownership and concurrency

Adding/removing/closing handlers is the caller's responsibility. The mixin does
not globally configure logging, close replaced class-logger handlers or restore
their earlier configuration. Tracer mirrors do not use a logging handler's
level/filter path. Raw disabled tracer writes bypass mirrors, but explicit file
logging still formats its records. Temporary file-emission color changes and
tracer context/line state are shared; do not claim concurrent isolation.
