# Interception

Traceprint may replace process streams only when the caller explicitly requests
that behavior. The same object also works as `print(..., file=target)` or through
direct `write` calls without installation. Writes have immediate effects; no
complete-line buffering is permitted merely to join `print` arguments.

## Installation

`install(*, stdout=True, stderr=False)` handles stdout first, then stderr:

- For a requested stream not already intercepted by this tracer, capture its
  current process object and replace it with the tracer. Mark that stream installed.
- If stdout is newly installed and no explicit sink was supplied at construction,
  choose the captured stdout as the sink.
- If stderr is newly installed, this call's `stdout` argument is false and no
  explicit sink was supplied, choose the captured stderr as the sink.
- Otherwise retain the sink. An explicit constructor sink wins in every case.

This makes repeated requests for an already-installed stream idempotent without
recapturing the tracer itself. A false argument does not uninstall a previously
installed stream; use `uninstall` or `configure` to remove interception. With
both streams requested in the same call, both feed the selected stdout sink.
There is no separate routing through `error_stream`.

`uninstall()` restores each captured stdout/stderr object for which this tracer
has an active installation flag, then clears both flags and captures. Repeating
uninstall is a no-op. It does not close/reset the sink, clocks, labels, line state
or attached file handlers. Install/uninstall do not enable a disabled tracer.

Callers should use `try/finally` to restore streams. Normal single-tracer cleanup
must restore object identity, not just an equivalent stream. Overlapping tracer
ownership and external stream replacements are not automatically coordinated;
see [compatibility](annex_observed-compatibility.md#stream-and-installation-edges).

## Depth filtering

At the point a write chunk or transition is considered, determine whether the
current depth is allowed:

- `None`: allow every depth.
- `range`: allow exactly its members.
- Callable: call it with the current depth and allow a truthy result.
- Other iterable: allow when membership contains the current depth.

Suppressing output does not suppress context mutation. A disallowed chunk must
not reach either the sink or mirrors, call `format`, advance timing or alter
visible line state. Evaluate the write filter once per chunk, including whitespace
chunks. Context transition operations may also perform their own precheck.
Exceptions from predicates/membership propagate during direct tracer operations.
Iterable membership has ordinary Python semantics, including consumption of
one-shot iterators; prefer a reusable collection for stable membership.

## Writing fragments

`write(data: str)` returns `len(data)` on a successful call, even when all output
is filtered. It does not return the length of metadata or the underlying sink's
write result. Preserve message whitespace and original CR/LF endings.

When disabled, write `data` directly to the sink, bypassing formatting, filtering
and mirrors. For a nonempty input, set line state according to whether it ends
with CR or LF: an ending resets it; otherwise mark an existing line. An empty
disabled write still calls the sink but leaves line state unchanged.

When enabled:

1. Split `data` using `str.splitlines(keepends=True)`. An empty input creates no
   chunks and causes no sink write.
2. For each allowed chunk, remove only trailing CR/LF characters into an `ending`
   suffix, leaving `message`. Do not strip other characters from the emitted text.
3. If `message.strip()` is nonempty and no line has started, call `format(message)`.
   If a line has started, emit the original message unchanged, or surround it
   with the current depth color and `RESET` when colors are enabled. Do not
   repeat metadata or indentation on a continuation.
4. Write that result plus its ending, then mark the line started. For a whitespace-
   only chunk, write the original chunk without formatting or starting a new line.
5. Any nonempty CR/LF ending resets line state after that write.

Every enabled write reaches the sink first, followed by all mirrors in attachment
order with the same already-formatted text. Do not catch sink/mirror exceptions
in the tracer, automatically retry, or roll back effects already written. Line
state changes after the corresponding successful write operation.

Whitespace fragments are immediate too. Leading whitespace supplied separately
can precede the first metadata prefix; whitespace within a nonblank fragment
remains part of that formatted message. Blank lines have no metadata. Unicode
line separators recognized by `splitlines` but not CR/LF remain in their message
or whitespace chunk and do not reset this CR/LF line state. These unusual cases
are further illustrated in the [compatibility annex](annex_observed-compatibility.md).

Labels, timing and indentation belong to the first nonblank fragment's metadata.
Later context/configuration changes do not cause a second prefix before a newline.
Continuation coloring uses the current palette/depth at that write. A custom
format suffix follows the first fragment, not the eventual complete line.

## Flush and mirroring lifecycle

`flush()` flushes the sink, then every attached mirror in attachment order,
regardless of enabled state. It does not output pending text, add a newline,
reset line state or advance clocks. Exceptions propagate; later mirrors are not
flushed after an earlier failure.

Attaching a handler appends it without deduplication or opening/closing it.
Removing a handler removes the first equal attachment if present and otherwise
does nothing. Attaching the same handler twice yields two mirror writes/flushes;
ordinary use should attach once. The caller removes and closes owned handlers.
Handler behavior and ANSI stripping are owned by [Logging](006_logging.md).

## Formatting

Formatted output preserves message text when the configured format contains its
placeholder. Colors are optional and auto-disabled for non-TTY sinks. Exact
format fields, colors and indentation rules are in [Formatting](003_formatting.md).
File output strips terminal escape sequences as specified in [Logging](006_logging.md);
there is no current option to preserve ANSI in files.
