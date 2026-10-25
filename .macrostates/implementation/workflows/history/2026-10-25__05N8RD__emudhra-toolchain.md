# eMudhra toolchain remediation

Project phase: active
Workflow type: Implementation amendment
Status: completed
Delivery state: accepted
Change depth: medium
Branch: fix/emudhra-toolchain
Requested by: Lucas Lopez (713375+lucaslopez@users.noreply.github.com) - Obtained from repository Git configuration
Implementer: Model — GPT-6; exact revision/effort not exposed; agent: Codex; source: session metadata
Started at: 2026-10-25 01:38 UTC
Last updated at: 2026-10-25 01:38 UTC

## Original request

Update this project for the eMudhra/emSign certificate security incident according
to https://discuss.python.org/t/109576.

## Scope and acceptance

Repair affected development dependencies and CI installers using the advisory's
minimum versions and verified bootstrap. Preserve the standard-library-only
runtime and public API. Document existing-environment repair and verify the
lockfile, workflows, project checks and built artifact.

## Work done

- Read the selected specifications and inspected all tracked tooling/CI entrypoints.
- No pre-existing open workflows or working-tree edits were present.
- Created the topic branch from 92072928c35016e404afb84d49ef9f1486d0e17c.
- Found certifi 2026.7.22 in uv.lock and uv 0.12.24 in all build workflows.

## Remaining work

All 41 tests, Ruff lint/format, Pyright and strict Sphinx pass on Linux Python
3.12.15. Macrostates 0.5.0 check/change-check pass. Manual assertions verify
security floors, hash bootstrap ordering, locked CI and the publisher pin.
uv 0.13.4 lock/sync upgraded certifi to 2026.10.23. The lockfile was previously
ignored; it is now tracked for reproducible locked installs.

Artifact checks and hosted matrix checks continue in the release workflow.

## Blockers and limits

No containers, conda, pixi or sigstore dependencies are tracked. Host-wide trust
stores and unrelated environments are outside this repository update.

## Suggested next step

Apply and verify the scoped security update.

## Closure authorization

The user explicitly authorized closing the open workflows once work finishes,
and preparing a PR, pushing, merging and publishing the package. Closure will be
applied after the release candidate's applicable local checks. No public API or
product specification change is needed for the toolchain repair.

## Completed local delivery

Updated at: 2026-10-25 01:41 UTC. All 41 tests, Ruff lint/format,
Pyright, strict Sphinx, Macrostates 0.5.0 check/change-check, offline source/wheel
builds, strict Twine and isolated wheel/examples checks pass. The wheel is built
from the source distribution. Candidate version 0.1.3 is unused on PyPI.

The bound release plan collects four pending records and proposes specs-1.1.0 /
imp-1.1.0. Historical origin and consumed record bytes are preserved. No runtime
or public API change was made; no additional product specification update is
needed. Baseline summary links now point to authoritative declarations.

The user's instruction authorizes closure after finishing and PR/push/merge/package
publication. Local implementation and preparation are finished; this record is
closed under that authorization. Hosted checks, reviewed integration and upload
are subsequent authorized operations whose receipts belong in GitHub/PyPI.

Remaining implementation work: none. The earlier progress lists are historical;
external CI, merge and publication are pending at closure.

- Closure authorized by: Lucas Lopez — explicit current-session instruction to close open workflows when finished and prepare PR, push, merge and publish.
