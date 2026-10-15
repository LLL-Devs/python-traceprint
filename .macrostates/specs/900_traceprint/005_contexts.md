# Contexts and decorators

## Common context rules

Depth starts at zero and labels form a stack in outer-to-inner order. A normal
entry adds one depth and one label; a normal exit removes one of each. Filtering
affects output, not this tracking. Locked tracers retain their existing depth and
labels while still being able to print allowed transitions/messages.

Enable/disable and lock/unlock are setters, not counters or context managers.
They do not reset labels, clocks, mirrors or line state. Disabled manual operations
and spans do not track depth. Keep these flags stable inside active spans/decorated
calls and balance manual operations. Behavior outside those conditions is recorded
in [compatibility observations](annex_observed-compatibility.md#context-mutation-edges).

Transition strings below are supplied to `write` with a trailing newline and
are therefore subject to filtering, current line state and ordinary formatting.
Transition output is optional; no transitions are printed by default.

## Manual push and pop

`push(label=None)`:

1. If disabled, return without any effect.
2. If unlocked, increment depth and append the supplied truthy label, otherwise
   append `"level" + str(new_depth)`. Thus `None` and `""` generate `levelN` labels.
3. If the supplied label itself is truthy, transitions are enabled and the new
   current depth is allowed, write `"> LABEL\n"`.

Generated labels do not trigger a transition when no truthy label was supplied.
When locked, an explicitly labeled transition can still be written at the existing
depth; the label stack is unchanged.

`pop(label=None)`:

1. If disabled, return without any effect.
2. If unlocked and depth is above zero, decrement depth and remove the final
   stored label. At depth zero, do not decrement or remove anything.
3. Select the supplied truthy label, otherwise the removed label. If that selected
   value is truthy, transitions are enabled and the resulting depth is allowed,
   write `"< LABEL\n"`.

An explicit pop label names the transition, not a stack entry to search/remove.
At depth zero or while locked, `pop("name")` may still print an exit transition.
With no selected label, print nothing. Manual push transitions use the entered
context; manual pop transitions use the parent context after removal.

## Spans

`span(label)` constructs a synchronous context manager without changing state.
The returned object exposes its target as `.tracer` and exact label as `.label`.
Entering returns that context object, so `with target.span("load") as context`
binds the span, not the tracer.

On entry when enabled:

1. If transitions are enabled and the parent depth is allowed, write `"> LABEL\n"`.
2. If unlocked, increment depth and append the exact supplied label, including an
   empty string. Unlike manual `push`, spans do not generate a replacement label.

On exit when enabled:

1. If unlocked, decrement depth and remove the final label.
2. If transitions are enabled and the resulting parent depth is allowed, write
   `"< LABEL\n"` on ordinary exit, or
   `"< LABEL [failed: EXCEPTION_CLASS_NAME]\n"` when exiting with an exception.

Return `None` from exit; do not suppress the body's exception. On normal supported
use, cleanup restores the prior depth/labels even when the body raises. Disabled
entry/exit performs no context/transition work; locked entry/exit performs no
depth mutation. Spans do not install/uninstall streams or flush/close sinks.

## Function decorator

Support all these forms, preserving the function's metadata with `functools.wraps`:

```python
@trace
def work(): ...


@trace(label="load")
def load(): ...


@trace(tracer_instance=target)
def run(): ...
```

Select the supplied tracer or global `tracer` when the decorator is created;
do not select a new tracer on each call. The optional first positional function
supports the bare form; when it is `None`, return a decorator awaiting a function.
A truthy explicit label wins; otherwise use `function.__name__`.

On each wrapped call:

1. If the target is disabled, directly call the function with the original
   arguments and return its result. No transitions or context mutation occur.
2. Capture whether the entry depth is filtered. If transitions are enabled and
   either entry depth is allowed or `force=True`, attempt
   `"> LABEL()\n"` at the parent depth.
3. If unlocked, increment depth and append the selected label.
4. Call the function with unchanged positional/keyword arguments. Return its
   result unchanged; let its exceptions propagate.
5. In `finally`, if unlocked, decrement depth and remove the last label. If
   transitions are enabled and either the captured entry depth was allowed or
   `force=True`, attempt `"< LABEL()\n"` at the resulting parent depth.

The decorator's exit has no span-style `[failed: ...]` suffix. Capture the entry
filter decision once for both transition attempts; each actual `write` still
applies the current depth filter. `force` is not a bypass of write-level filtering.
That alpha compatibility boundary is discussed in the
[annex](annex_observed-compatibility.md#transition-filtering).

The wrapper traces synchronous function invocation only. For an async function
or generator, it surrounds creation of the coroutine/generator object, not later
execution, awaits or iteration. Do not add special async/generator tracing while
replicating this library.

## Failure boundaries

Context tracking is not transactional with output. A transition write can fail
before body execution or during exit, using the direct stream failure behavior.
Entry/exit may therefore fail independently of the body. Normal exception cleanup
guarantees assume a writable sink, balanced context and stable enabled/locked state;
no recovery for externally corrupted stacks or flag changes is required.
