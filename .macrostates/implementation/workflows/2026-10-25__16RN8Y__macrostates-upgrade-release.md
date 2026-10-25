# Macrostates upgrade and library release

- Project phase: active
- Workflow type: Specification update; Implementation update; Release preparation; Integration preparation
- Status: in_progress
- Delivery state: awaiting_acceptance
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

Implementation and applicable local checks are complete. Explicit Definer
acceptance and closure remain required before proposal submission. After closure,
submit the candidate, require hosted checks/review, integrate and publish the
annotated baseline/library tags and verified distribution through the release
workflow. No remote proposal, integration or upload has occurred yet.

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

## Candidate qualification

Prepared the candidate against freshly fetched origin/main `76d2f86`. The plan proposes specs-2.0.0 / imp-2.0.0 and preserves
all earlier consumed record hashes. Library 0.1.4 has independent provenance
and tag v0.1.4. The declaration is a release candidate until reviewed integration;
its status field alone does not establish an upload.

Offline uv builds produced both artifacts, building the wheel from the source
distribution without original Git ancestry. Strict Twine, isolated installation,
metadata/license/type-marker checks and both examples pass. Structured YAML
parses; artifact inventories exclude local environments/backups/generated docs;
six generated HTML documents contain no checkout-location disclosure. Strict
Sphinx was rerun for version 0.1.4. Macrostates check/change-check and diff checks
pass. Hosted matrix tests and post-integration publication provenance remain
separate required gates.

Reviewed newly authored records and retained artifacts against Process 6's
public document contract. Necessary public upstream provenance and legal notices
remain accurate; existing historical records were not rewritten. There are no
other independently composed or vendored package contexts in the tracked project
requiring an update suggestion. Local private backup trees are outside scope.

## Candidate consistency correction

The exact candidate check rejected finalizing CHANGELOG.md after the plan's
source snapshot: CLI 0.6.0 permits release metadata and workflow updates after
planning, but requires root changelog content in the original planned tree.
Returned the change unchanged to pending state and restored the original baseline
and historical plan declarations without rewriting commits. Final release notes
remain in the new pre-plan source, which is then replanned and prepared normally.
This correction does not change impact, API, requirements or successful artifact
results. No release identities were published during the rejected preparation.
