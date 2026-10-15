# Observed alpha compatibility

Read this annex when reproducing unusual observable behavior of the 0.1.2 alpha
or assessing a possible fix. It is a descriptive compatibility profile, not a
decision that every edge must become permanent intended behavior. Normal supported
use is defined by the core documents. Unsupported mutation/input cases below
have no stronger correctness guarantees than the recorded observations.

Reconstructing that specific alpha may require these details; changing them is
a separate explicit compatibility/design decision. Do not silently repair them
in a reproduction task or introduce new requirements solely to preserve a defect.
Private field/helper names are not mandatory. Review evidence and potential
follow-up work belong in implementation records.

## Transition filtering

`trace(force=True)` can request a transition write when the captured entry depth
is filtered, but `write` filters it again at the actual current depth. With a
stable filter rejecting that depth, force produces no transition. The decorator
reuses the entry filter decision at exit; changing filters/depth during the call
can therefore make its precheck and write-level decision differ. This is not a
general force-through-filter feature.

## Context mutation edges

Contexts assume stable enabled/locked flags and a balanced label stack. The alpha
does not remember whether a particular span actually pushed before popping:

- Disable inside an entered span: exit does no work and can leave its labels/depth
  in place. Enter disabled then enable inside: exit may decrement/pop a context
  that was never entered, potentially raising `IndexError`.
- Enter locked, unlock before exiting: exit can remove a parent's label or pop
  an empty stack. Enter unlocked then lock: exit can leave the entered context.
- A decorator checks enabled only at call entry. If the body disables its target,
  its `finally` still pops when unlocked; attempted exits then follow raw disabled
  writing. Changing lock state can create the same imbalance as spans.
- Manually corrupting depth/labels or unbalancing nested operations can produce
  ordinary `IndexError`, wrong palette/indent selection or altered label text.

These are unsupported lifecycle changes, not exception-cleanup promises. Normal
body exceptions with stable state remain covered by core acceptance cases.

## Stream and installation edges

The alpha resolves sink values with `stream or sys.stdout`, while explicitness
uses `stream is not None`. A custom falsey stream can therefore select stdout
while still preventing later implicit sink refresh. The same initial truthiness
selection exists for the reserved error-stream value.

`error_stream` is stored but does not route intercepted stderr independently.
Multiple tracers can capture one another and uninstall out of order; no ownership
stack prevents restoring a tracer that another operation removed. Uninstall also
restores its captured object if external code replaced the stream afterward.

A later `install(stdout=False, stderr=True)` with a new stderr capture and an
implicit sink chooses stderr even if stdout was already installed in an earlier
call. Both intercepted streams then share that sink. Colors and partial-line
state are not reset when the sink changes.

## Configuration and mutable state

The alpha's remaining-key configuration uses existing-attribute lookup plus
assignment, not a public-key whitelist. Private attributes and even method names
can therefore be assigned; read-only properties fail normally. Such changes are
outside the supported public configuration contract. There is no transaction or
rollback after a later invalid key.

Palettes are shared mutable lists. Mutating the exported default palette affects
tracers using it. Replacing/mutating an active palette to empty can cause a division
or indexing failure even with colors off, because line-color selection precedes
the color-output branches. Constructor/configuration empty-list fallback does
not protect against later direct mutation.

## Format and color edges

Metadata/message separation uses `text.find(message)`, not placeholder position.
If the message occurs earlier in metadata, the color/indent boundary follows that
earlier substring. An empty message matches at offset zero. Repeated placeholders
are not independently colored or indented.

The color converter relies on Python `int(pair, 16)` after a length check, without
hex-digit/range validation. Some signed/whitespace-containing pairs therefore
parse even though they are not conventional RGB input. Normal six-hex-digit input
and actual conversion failures remain specified in the core.

## Fragment edges

With format `"[{original_message}]"`, `print("a", "b", file=target)` yields
`"[a] b\n"`, not `"[a b]\n"`: suffixes belong to the first nonblank fragment.
Writing `"  "` followed by `"text\n"` with format `F` yields `"  [] text\n"`.
Blank/whitespace fragments do not start prefix state.

Python's `splitlines` also separates vertical tab, form feed and several Unicode
separators, but the alpha only extracts/resets CR/LF endings. With format F,
`write("a\u2028b\n")` produces `"[] a\u2028b\n"` with one prefix. No complete
Unicode terminal-line interpretation is implied.

Interleaved intercepted stdout/stderr share the same partial-line state. A
partially successful sink/mirror write that then raises can leave output present
without committing the corresponding line-state update. Direct operations do not
repair that situation automatically.

## File and shared-logger edges

Direct file logging bypasses tracer enabled/filter state, whereas mirrored stream
output obeys it. File emission temporarily mutates the shared tracer's color flag.
Direct mirroring does not acquire the logging handler's `handle` lock or enforce
its level/filter. These routes are not isolated concurrent pipelines.

Closing a file handler does not permanently prevent reopening. Reopening a closed
`"w"` handler truncates by ordinary file-mode semantics. Duplicate mirror attachments
duplicate output. Mixin passthrough clears shared class-logger handlers without
closing them, and a later instance may alter another instance's logger level.
Neither mixin flags nor direct `.logger` calls provide per-instance logger isolation.
