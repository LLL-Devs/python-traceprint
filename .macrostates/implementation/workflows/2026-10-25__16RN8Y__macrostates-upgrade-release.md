# Macrostates upgrade and library release

- Project phase: active
- Workflow type: Specification update; Implementation update; Release preparation; Integration preparation
- Status: in_progress
- Delivery state: implementing
- Change depth: systemic
- Branch: release/macrostates-0.1.4
- Requested by: Definer
- Implementer: AI-assisted implementation
- Started at: 2026-10-25 11:17 UTC
- Last updated at: 2026-10-25 11:17 UTC

## Technical objective and scope

Adopt the latest published releases of the selected Macrostates packages and
compatible CLI, validate the effective contract, and prepare python-traceprint
0.1.4 for reviewed integration and publication. Release-branch creation, remote
publication and library release are authorized. Explicit workflow closure remains
a separate acceptance gate.

## Acceptance criteria

Canonical tagged package snapshots and their integrity lock agree; the pinned
CLI supports the selected policies; new documents follow Process 6's public
contract; required local and hosted checks pass; exact annotated baseline and
library tags bind the integrated source; published files match version 0.1.4.
Runtime behavior and the alpha API remain equivalent.

## Work done and evidence

Verified a clean starting tree and refreshed origin/main at
`76d2f86` (full source identity is captured by the work origin record). Established the release branch before authoring files.
Upstream tags select Process 6.0.0 and CLI 0.6.0; Meta 3.0.0, Repository-1 4.0.0,
Python-1 2.1.1 and Python-library-1 2.0.0 are already current. PyPI confirms CLI
0.6.0 is available and library 0.1.4 is unused.

Process 6 replaces personal/conversational attribution with neutral technical
content and role attribution in new retained documents. Existing historical
records are outside this update's cleanup scope and retain their byte bindings.
The new required development contract has major specification and implementation
impact, independently of the library's patch release identity.

## Remaining work

Bind the release plan, prepare candidate artifacts and obtain explicit closure
before proposal submission.
Hosted review/integration, tag publication and package upload follow local closure.

## Blockers and unresolved questions

None identified during initial inspection. Workflow closure is not yet authorized.

## Suggested next step

Capture origin and install the published Process snapshot and CLI.

## Local validation

Process 6.0.0 was imported through CLI 0.6.0 and verified against the upstream
annotated tag. All other upstream selections are already the latest published
releases. The scoped local package is 1.1.1 for its tooling-pin update; the
composed contract has major impact because document attribution and authoring
permissions change. No implementation gap or runtime/API change was found.

On Linux Python 3.12.15, all 41 tests pass. Ruff lint/format, Pyright, strict
Sphinx HTML, Macrostates check and change-check pass. Artifact checks and hosted
platform checks remain pending. New retained records use role attribution and
neutral technical evidence; existing historical bytes are preserved.
