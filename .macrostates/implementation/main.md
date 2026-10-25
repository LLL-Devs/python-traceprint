# Implementation

Project phase: active

Traceprint is an MIT-licensed Python library for readable print and logging
output. The public distribution is python-traceprint and imports remain traceprint.
The release candidate uses specs-1.1.0 and imp-1.1.0; the independent library
version is 0.1.3, with an alpha API. deliverables.yaml owns its version and tagged
source. Reviewed integration finalizes these declarations.
Publication is proven by external release files, not by a declaration alone.

## Architecture

The authoritative product contract is the local
[Traceprint specification package](../specs/900_traceprint/README.md), including
its interface, formatting, stream, context, logging and acceptance owners.
Sphinx documentation is a product derived from the library, not a competing
specification. The [specification reconstruction review](specification-review.md)
records source coverage and observed alpha boundaries separately.

src/traceprint/tracer.py owns formatting, labels, depth, explicit stream interception
and logging integration. Metadata is added once per nonblank line while partial
writes appear immediately. Indentation is independent of ANSI colors. Timestamps
are UTC; durations use perf_counter. File output strips terminal escapes.

Importing traceprint never installs process streams. Callers install/uninstall
explicitly and own file-handler cleanup. Context is shared mutable tracer state,
not isolated by thread or async task. The decorator wraps synchronous calls.

hatch_build.py validates the independent version declaration without Git, network
or installed specs. Source and wheel artifacts include MIT licensing; the wheel
includes py.typed and has no runtime dependencies. docs/ contains Sphinx autodoc,
usage and release guides. CI checks Linux Python 3.12–3.15 and Windows/macOS 3.12,
quality, docs and artifacts; Pages deploys docs, and release.yml publishes via OIDC.
The dev group requires certifi >=2026.10.19 and uv configuration requires
uv >=0.13.4. Workflows bootstrap pip 26.2.2 through the advisory's hash-verified
wheel before installing uv 0.13.4, sync locked dependencies and use the patched
v1.14.3 publishing action. CONTRIBUTING.md describes environment recovery.

## Verification and provenance

Use the commands in CONTRIBUTING.md. Macrostates CLI 0.5.0 checks package metadata
and locked upstream integrity. Semantic review, tests, artifact checks and remote
CI supply separate evidence. Initial baseline review and release provenance
are recorded in workflows/history/2026-10-14__16CBH1__initial-publication.md.
