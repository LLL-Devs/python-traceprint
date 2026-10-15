# Traceprint specification package

This package is the authoritative behavioral contract for Traceprint: a Python
library for readable print and logging traces with timing, labels, nesting depth
and explicit stream interception. Its normal-path requirements describe the
existing alpha library closely enough to implement it without reading its source.

Use this package together with its declared Python-library, Repository, Process
and Meta dependencies. `docs/` is generated/user-facing product documentation;
it is not an alternative requirement owner. Source code, tests and examples are
evidence used to check conformance, not a replacement for the requirements here.

The reconstruction target is equivalent public behavior, signatures, outputs and
artifact contracts, not byte-identical source or mandatory private attribute names.
Do not silently add features or repair alpha limitations while reconstructing it.

## Scope

- Traceprint's public purpose and non-goals.
- Exact public interfaces, configuration defaults and state.
- Timing, labels, indentation, ANSI colors and line-fragment output.
- Stream installation, restoration, filtering and file mirroring.
- Manual contexts, spans and synchronous decorators.
- Logging handlers and the verbosity-gated logger mixin.
- Independent build metadata, artifact contents and release provenance.
- Concrete acceptance scenarios and example behavior.

Generic Python library rules belong in `python-library-1`.

## Vocabulary

- **Tracer**: an object that formats text output with trace metadata.
- **Span**: a labeled depth context.
- **Transition**: an optional entry or exit line for a span or decorated
  function.
- **Interception**: replacing a process stream such as `sys.stdout` with a
  tracer by explicit caller request.
- **Depth**: the nonnegative nesting level used for filtering, indentation and
  palette selection; initially zero.
- **Sink**: the underlying text stream that receives tracer output.
- **Fragment**: one string supplied to `write`; a single `print` call may supply
  several fragments.
- **Line state**: whether the next nonblank fragment continues an existing output
  line instead of receiving metadata; it survives writes/flushes until a visible
  CR/LF ending. Enabled whitespace and disabled raw writes have the distinct
  effects specified in [Writes](004_interception.md#writing-fragments).
- **Metadata**: formatted timestamp, timing and label text around a message.
- **Mirror**: an attached file handler receiving already-formatted stream writes.

## Reading order

1. [Project](001_project.md)
2. [API](002_api.md)
3. [Formatting and colors](003_formatting.md)
4. [Writes and interception](004_interception.md)
5. [Contexts and decorators](005_contexts.md)
6. [Logging and file output](006_logging.md)
7. [Library versions and releases](007_release.md)
8. [Acceptance scenarios](008_acceptance.md)

Core filenames use consecutive three-digit prefixes matching this reading
order. README.md remains the unnumbered package entrypoint; conditional annexes
use the annex naming convention.

## Conditional reading

Read [alpha compatibility observations](annex_observed-compatibility.md) when
matching unusual behavior of the published alpha implementation, exercising
unsupported state changes, or deciding whether a future correction changes
compatibility. Those observations are not approvals to turn accidents into
permanent product requirements. The implementation review records the evidence
and unresolved design choices separately.

