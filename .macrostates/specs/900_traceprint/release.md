# Library versions and releases

## Distribution identity and license

The published Python distribution name is `python-traceprint`; its Python import
package and supported imports remain `traceprint`. Distribution metadata must use
the MIT SPDX expression and include the root MIT license in source and wheel
artifacts. Selecting this name does not claim a PyPI registration or upload.

Traceprint's Python distribution version is independent of the Macrostates
repository baselines. Its single editable authority is
`deliverables.traceprint.version` in
`.macrostates/implementation/deliverables.yaml`, read by `hatch_build.py`.
The declaration identifies the independent strategy, PEP 440 version scheme,
development/candidate/released status and applicable baseline references.

## Compatibility and development

The supported package-root imports remain the public surface described in
[API](api.md). The API is alpha; breaking changes must be described explicitly.
Once stable, incompatible public behavior changes increment the distribution
Major version, compatible additions increment Minor, and fixes increment Patch.
Repository tooling or specification-baseline changes alone do not imply an API
Major change or publication of the library.

An ordinary development build uses an explicit PEP 440 prerelease version and
`status: development`. Do not use a raw Macrostates branch
identity as a Python version or silently rebuild changed source as a stable
published distribution. Builds validate the tracked declaration without Git,
network, installed specifications or local settings and never update it.

## Release preparation

Assign a distribution version deliberately during authorized library release
preparation, using its public API impact. Macrostates baseline finalization does
not assign or publish the library's version. The default numeric `imp-*` version
policy is replaced by this independent distribution policy for Traceprint.

Before publication, complete Process and Repository review/closure gates, verify
required compatibility tests, lint, type checks, source/wheel builds and installed
artifact imports, and confirm that the distribution version has not been used.
Record the exact finalized `specs-*` and `imp-*` references, release date and
immutable source tag or post-commit source receipt. Preserve previous release
provenance and do not advance versions, create tags or upload artifacts during an
ordinary build. A candidate declaration is not evidence of publication.

## Initial standalone publication

The definer explicitly authorized a fresh public history with a private backup
of earlier development. The public project starts from one reviewed initial
snapshot, without importing or rewriting the private Git ancestry. Original
work origins, pending changes and closed workflow records are retained in the
private archive; they are not represented as ancestors of the public repository.

For this one-time bootstrap, use a reviewed native Git equivalent: audit the
source, verify the unchanged upstream package lock, review behavior and artifacts,
record the initial baseline decision and closed preparation in implementation
history, submit the exact initial commit on a release branch, require successful
CI, then create the primary ref at that accepted commit. Do not fabricate a CLI
release plan referring to nonexistent public ancestors. This scoped rule overrides
ordinary existing-baseline planning for the initial snapshot only; subsequent
baseline changes use Process's normal change-record/release-plan procedure.

The initial baselines are specs-1.0.0 and imp-1.0.0, reflecting the highest major
contract impact of the accepted specification/tooling and distribution-identity
changes. The library remains independently versioned at 0.1.2, with an alpha API.
Released declaration status identifies the finalized source/version assignment;
publication itself is evidenced externally by the GitHub release and PyPI files.

Create immutable annotated specs-1.0.0, imp-1.0.0 and v0.1.2 tags on the accepted
initial commit. The tracked deliverable identifies v0.1.2 rather than embedding
its own future commit hash. Validate tag type, exact declarations, primary ancestry,
artifact metadata and complete compatibility checks before upload. The initial
bootstrap is verified by tests/packaging/check_release.py plus Macrostates check
and change-check. Later releases with a Process release plan also run CLI
release-check --publication. Keep publication credentials in a separate OIDC job.
