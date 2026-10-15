# Acceptance scenarios

These cases are concrete conformance requirements for supported usage. They
describe inputs and externally visible results without requiring existing source
or test files. Use the compatibility annex for baseline-only edge observations.

Unless overridden, each case uses a fresh `io.StringIO` sink, an enabled/unlocked
tracer, colors/tabulation/transitions off, no filter, no environment labels and
this format (called `F` below):

```text
[{label_full}] {original_message}
```

Use actual ANSI sequences when comparing colored strings; display escapes with
`repr` rather than interpreting them. For timing tests, control the performance
clock and UTC datetime. Use temporary files and restore process/logger state in
`finally` so cases do not depend on one another.

## API and initialization

| ID | Operation | Required result |
| --- | --- | --- |
| API-01 | Import `traceprint` with empty environment labels. | Exactly the nine root `__all__` names in [API](002_api.md); stdout/stderr identities and root logging configuration unchanged. |
| API-02 | Construct with defaults and a non-TTY sink. | Depth 0, labels empty, enabled true, colors false, tabulation/transitions false; no stream installation. |
| API-03 | Construct with a TTY sink, then explicit `use_colors=False` in another instance. | Automatic detection gives true in the first; explicit false wins in the second. |
| API-04 | Fresh import with `TRACEPRINT_INITIAL_LABELS=" / job // load / "`. | Global depth 2 and labels `["job", "load"]`; new explicit instances remain at zero/empty; no interception. |
| API-05 | Supply a custom palette, or an empty list. | Nonempty palette is retained by reference; empty list selects the shared default palette. |
| API-06 | `configure(use_colors=None, filter_levels=[0])` after a sink's TTY status changes. | Redetect colors and retain the requested filter. |
| API-07 | `configure(use_tabulation=True, unknown=1)`. | Raise `AttributeError("Tracer has no attribute unknown")`; the earlier tabulation update remains true. |
| API-08 | Inspect/call the public constructors and methods. | Argument positions, keyword-only boundaries and defaults match [API](002_api.md). `enabled` has no setter. |

## Formatting

**FMT-01 — default text and clocks.** Construction reads performance time 100.0.
With UTC datetime `2026-10-14 12:00:00`, format `"hello"` at time 101.25:

```text
[2026-10-14 12:00:00][1.250s][+1.250s][] hello
```

The result has no newline and is not written to the sink. Format `"next"` at
101.5 with the same UTC datetime and obtain cumulative `1.500s`, elapsed
`+0.250s`. A direct formatting call affects the next write's elapsed time.

**FMT-02 — labels.** With labels `["outer", "inner"]`, format
`"{label}|{label_full}|{original_message}"`:

| Message | Result |
| --- | --- |
| `"inside"` | `inner/>|outer/inner/>|inside` |
| `"> enter"` | `inner|outer/inner|> enter` |
| `"< exit"` | `inner|outer/inner|< exit` |
| `" > spaced"` | `inner/>|outer/inner/>| > spaced` |

**FMT-03 — indentation.** At depth 1 with format
`"[trace] {original_message}"` and tabulation on, stripping ANSI from a colored
result must equal its plain result:

| Metadata color | Plain result for `"message"` |
| --- | --- |
| Default dark grey | `[trace]     message` |
| `None` | `    [trace] message` |

**FMT-04 — exact ANSI composition.** At depth zero with default metacolor and
format `"[trace] {original_message}"`, formatting `"hello"` with colors on yields:

```python
"\x1b[90m[trace] \x1b[0m\x1b[38;2;82;201;127mhello\x1b[0m"
```

For `metacolor=None`, use the same depth color around the entire `[trace] hello`
text and one trailing reset. The default palette repeats at depth 8.

**FMT-05 — format selection.** A format `"fixed"` with tabulation at depth 1
returns `"    fixed"` without colors; with default metacolor and colors, returns
dark-grey + that whole string + reset. A missing format field raises standard
`KeyError`; the last-format clock has already advanced.

**FMT-06 — UTC and conversion.** `%z` must format as `+0000`.
`hex_to_ansi("#52C97F")` and `hex_to_ansi("52c97f")` both return the depth-zero
sequence above. `"#123"` and `"#GG0000"` raise the specified `ValueError`.

## Fragment output, filters and streams

| ID | Operation | Required sink text/effect |
| --- | --- | --- |
| IO-01 | `print("hello", "world", file=target)`. | `"[] hello world\n"`, one prefix. |
| IO-02 | Then `print("one", "two", sep="/", end="!", file=target, flush=True)`. | Append `"[] one/two!"`; flushing adds nothing. |
| IO-03 | `write("first")`, inspect, flush, then `write(" part\nnext\n\nlast")`. | Initially `"[] first"` immediately; finally `"[] first part\n[] next\n\n[] last"`. Return 5 and 16. |
| IO-04 | `write("first" + ending + "next" + ending)` for each of LF, CR, CRLF. | `"[] first" + ending + "[] next" + ending`; retain the exact endings. |
| IO-05 | Write whitespace-only/empty chunks. | No metadata; an enabled empty write emits nothing; whitespace does not advance timing. |
| IO-06 | Allow depth 0, enter `span("hidden")`, write `"hidden"`, exit and write `"visible\n"`. | Only `"[] visible\n"`; filtered text neither advances clocks nor starts a line. |
| IO-07 | Write `"shown"` at depth 0, hide a nested newline with filter `[0]`, return and write `" continuation\n"`. | `"[] shown continuation\n"`; a suppressed newline does not end a visible line. |
| IO-08 | Repeat allowed/hidden writes with a range, list and predicate `lambda depth: depth == 0`. | Equivalent allowed-depth output; predicate receives current depth. |
| IO-09 | Disable, write `"raw"`, enable and write `" continuation\nnext\n"`. | `"raw continuation\n[] next\n"`. Disabled raw output bypasses filters/mirrors. |
| IO-10 | Write a colored multi-fragment line at depth 1 and mirror it. | Console continuation has depth color without a second prefix/indent; file equals console text after escape stripping. |
| IO-11 | Attach the same mirror twice, then remove it once. | Two callbacks per enabled write/flush before removal, one afterward; absent removal is harmless. |
| IO-12 | Inject a sink or direct mirror failure. | Direct operation raises; already-written effects are retained and there is no automatic retry. |

**IO-13 — installation and identity.** Save original stdout/stderr. With an
explicit sink, test stdout-only, stderr-only and both installation combinations,
repeat the install, print through installed streams, then uninstall twice. Each
requested stream must route through the explicit sink; final process stream
objects must be the original identities.

**IO-14 — implicit routing.** In a fresh tracer without a supplied sink,
stderr-only installation uses the captured stderr; installing both in one call
uses captured stdout for both. `error_stream` does not create an alternate route.
TTY detection changes only on explicit detection/configuration, not installation.

**IO-15 — configuration of installation.** Install stdout, then
`configure(intercept_stderr=True)`; the omitted stdout flag stays installed.
`configure(intercept_stdout=False, intercept_stderr=False)` restores both.
Timing, labels and partial-line state survive these operations.

## Context operations

**CTX-01 — nesting.** `push()` gives depth 1, labels `["level1"]`; `push("")`
gives depth 2, labels `["level1", "level2"]`. Two pops restore zero/empty; an
extra pop stays zero/empty. `pop("other")` names its transition without selecting
a different stack entry.

**CTX-02 — transition context.** For format `F` and transitions on, compare:

| Operation | Exact output |
| --- | --- |
| `push("outer"); write("inside\n"); pop()` | `"[outer] > outer\n[outer/>] inside\n[] < outer\n"` |
| `with span("outer"): write("inside\n")` | `"[] > outer\n[outer/>] inside\n[] < outer\n"` |
| Same span, body raises `ValueError`. | Entry as above, then `"[] < outer [failed: ValueError]\n"`; original error propagates and prior context is restored. |

**CTX-03 — lock/disable.** Under a stable lock, manual operations and spans
retain depth/labels; allowed explicitly named transitions may still print. Under
stable disabled state they do nothing. Unlock/enable restores normal tracking
without resetting preexisting context.

**CTX-04 — returned span.** `with target.span("load") as context` exposes
`context.tracer is target` and `context.label == "load"`; the target's depth is
increased inside, restored outside. An empty span label is stored literally,
unlike generated manual labels.

**CTX-05 — decorated function.** Decorating `run` with a target and transitions
on, where its body writes `"inside\n"`, produces:

```text
[] > run()
[run/>] inside
[] < run()
```

The function's arguments, return object, name/docstring and `__wrapped__` metadata
are preserved. On a body exception, the exit still prints without a failure suffix,
context is restored and the exception propagates. A truthy explicit label replaces
`run`; an empty label falls back to it. With a disabled target, only the function
is invoked. Coroutine/generator execution is not traced after object creation.

## Logging and files

| ID | Operation | Required result |
| --- | --- | --- |
| LOG-01 | Emit `logger.info("value=%s", 42)` through a `TracerHandler` with standard formatter `"%(levelname)s: %(message)s"`. | Tracer receives `"INFO: value=42\n"`, rendered normally with one metadata prefix. |
| LOG-02 | Emit `logger.exception("operation %s failed", "load")` inside a `ValueError` handler. | Include substituted message and `ValueError` exception text; multiline tracer rules apply. |
| LOG-03 | Use a file handler with default mode/encoding and a nested path. | Parent directories exist; file opens on construction, appends UTF-8 text and flushes after emission. |
| LOG-04 | Emit directly to a file while the tracer is disabled, has filter `[]` and colors on. | A trace-formatted ANSI-free file record is produced; console/mirrors are untouched; colors are restored true. |
| LOG-05 | Directly write `"\x1b[31mred\x1b[0m"` or an OSC hyperlink containing `red` to a file handler. | File contains `"red"`; no matched terminal escapes, extra prefix or newline. |
| LOG-06 | Mirror an installed multi-argument print under `span("load")`, tabulation on. | File text is `"[load/>]     hello world\n"`; identical to stripped console output. |
| LOG-07 | Close an append-mode file handler and write again. | Stream becomes `None` on close, then reopens and preserves preceding append-mode contents. In `"w"` mode, reopening truncates. |
| LOG-08 | Inject an ordinary exception in handler emission, or in direct file writing. | Emission uses standard `handleError`; direct writing propagates. Temporary color changes are always restored. |
| LOG-09 | Construct a lazy mixin instance; access `.logger` or `.log`. | First access initializes the concrete class-named logger at its configured level; repeated access does not reset it. |
| LOG-10 | Set `verbose=False`, call proxy methods, then use `.logger` directly. | Proxy submits no records; direct standard logger calls bypass the gate. Turning verbosity on affects the next proxy call. |
| LOG-11 | Construct with passthrough and a root formatter. | Class logger handlers are replaced by one global-target tracer handler carrying the first root formatter; propagation is false. Removed handlers are not closed. |
| LOG-12 | Initialize two instances of the same class with different logging levels. | Both refer to the same standard logger; second initialization sets its level; each proxy still uses its owner's verbosity. |

## Artifacts and build validation

**BUILD-01 — independent metadata.** A valid independent declaration can use
`version="3.2.0.dev0"`, `status="development"` and matching-contract baseline
references such as `specs-1.0.0`/`imp-1.0.1`. The build hook returns that exact
version; baseline numbers do not replace it. A directory containing just the
hook inputs works without Git, installed specs or a baseline release file.

**BUILD-02 — validation failures.** Reject schemas `True`, `2` or `"1"`, missing
deliverable mappings, non-independent strategy, a non-string/noncanonical/invalid
PEP 440 version, unknown status, a stable version with development status, invalid
baseline prefixes and mismatched baseline Major.Minor. Missing declaration raises
the filesystem error. Exact validation order/messages are in [Release](007_release.md).

**BUILD-03 — installed perspective.** Build source and wheel, install the wheel
outside the checkout without runtime dependencies, and verify importable root
API, distribution name/version/MIT metadata, license payload and `py.typed`.
Rebuild an extracted source distribution without Git/installed specs and verify
the same declared version. No build may edit release declarations or publish.

**BUILD-04 — repository products.** Strict Sphinx HTML generation must include
all root symbols with signatures and public methods/properties. CI checks the
six runtime matrix entries and quality described in [Release](007_release.md).
Publishing validates annotated source/baseline provenance and separates the
artifact build from credential-bearing upload.

## Runnable example behavior

**EX-01 — transformer.** `examples/sklearn_style_transformer.py` provides empty
`BaseEstimator` and `TransformerMixin` stand-ins; no scikit-learn dependency.
`SampleNameTransformer` inherits `LoggerMixin, TransformerMixin, BaseEstimator`,
uses INFO/global passthrough/lazy logging and accepts `verbose=True` by default.
Its `seen_count_` starts `None`; `fit(rows)` records row count, logs
`"fitted on %s rows"` and returns the same instance. `transform(rows)` logs
`"normalizing sample names"` and returns new dictionaries retaining each row's
fields but setting `sample_name` to `str(value).strip().lower()`. Original rows
are untouched. `fit_transform` chains the two operations. Their trace labels
are `SampleNameTransformer.fit` and `SampleNameTransformer.transform`.

The sample inputs `S1 / " Control "` and `S2 / " Treatment "` become the same
IDs with names `control` and `treatment`. Its main configures root INFO logging
with `"%(levelname)s - %(message)s"` and a tracer handler, explicitly installs
the global tracer, prints results and uninstalls in `finally`.

**EX-02 — main loop.** `examples/main_loop.py` uses the same root logging setup,
automatic colors, transitions/tabulation off and no depth filter. It logs start,
pushes `loop`, pushes `item_1`/`item_2`/`item_3` around inputs alpha/beta/gamma,
prints `input: VALUE`, logs `"processing %s"`, prints `output: UPPERCASE`, then
unwinds each item and loop in `finally`. It logs finish, prints
`['ALPHA', 'BETA', 'GAMMA']` using ordinary Python list representation and
uninstalls in `finally`. The processing function returns `item.upper()`.
