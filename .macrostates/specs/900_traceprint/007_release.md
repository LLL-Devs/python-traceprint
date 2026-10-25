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
[API](002_api.md). The API is alpha; breaking changes must be described explicitly.
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

## Build declaration and validation

The authoritative input is a YAML mapping at
`.macrostates/implementation/deliverables.yaml`. Its normal declaration contains
`schema_version: 1` and a `deliverables.traceprint` mapping with independent
strategy, `version_scheme: pep440`, version/status and exact baseline references.
Release date and immutable source provenance are added during release work.

`hatch_build.py` exposes `distribution_version(root: Path) -> str`. To reproduce
the metadata gate, validate in this order, raising `ValueError` with the indicated
message at the first failed check:

| Check | Failure message |
| --- | --- |
| Top level is a mapping and schema is exactly a Python integer, not a bool. | `Deliverables must declare schema_version: 1` |
| Schema equals 1. | `Unsupported deliverable schema` |
| `deliverables` is a mapping. | `deliverables must be a mapping` |
| `traceprint` is a mapping with strategy exactly `independent`. | `Traceprint needs an independent distribution declaration` |
| Version is a string. | `Distribution version must be a string` |
| `packaging.version.Version(value)` accepts it. | `Invalid Python distribution version`, chaining the parser exception. |
| `str(parsed_version) == value`. | `Distribution version must use canonical Python syntax` |
| Status is `development`, `candidate` or `released`. | `Invalid distribution status` |
| Development status has `parsed_version.is_prerelease == True`. | `Development builds need an explicit prerelease version` |
| Both baseline references have valid prefixes/numeric syntax. | `Invalid specification or implementation reference` |
| References have identical Major.Minor components. | `Referenced baseline contracts must match` |

Each reference uses a full match of `specs-` or `imp-` followed by
`(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)`. Their patches may differ. These
are strings, not alternative distribution-version sources. A noncanonical version
such as `01.1.0.dev0` fails instead of silently normalizing it.

Return the original validated version string. Missing/unreadable input and YAML
syntax errors propagate from their respective filesystem/parser operations.
Do not query Git, environment, network, a baseline release file or installed
specifications to obtain/fix the version. Other deliverable entries and optional
fields do not affect this lookup. The hook validates the listed fields; checking
release provenance, policy scheme declarations and actual uploads is separate.
Candidate/released statuses do not add a prerelease prohibition in this gate.

Register a custom Hatch metadata hook through
`[tool.hatch.metadata.hooks.custom]`. `CustomMetadataHook.update(metadata)` assigns
only `metadata["version"]` using that reader and the build root. Declare
`dynamic = ["version"]`; do not introduce a second editable version constant.

## Package metadata and artifacts

Use `hatchling.build` as the backend with build dependencies `hatchling>=1.27`,
`PyYAML>=6.0` and `packaging>=24.2`. Runtime dependencies remain empty.

| Metadata | Value/constraint |
| --- | --- |
| Name | `python-traceprint` |
| Description | `Readable print and logging traces with timing, labels, and nesting.` |
| Python requirement | `>=3.12` |
| License | SPDX `MIT`, root `LICENSE` included via license-files. |
| Author | Lucas Lopez; no personal email is required. |
| Keywords | `logging`, `tracing`, `stdout`, `debugging`. |
| Classifiers | Alpha development, developers, Python 3 and supported 3.12–3.15 versions, typed package. |
| Readme | Root `README.md`. |
| Repository/issues/changelog | Canonical `LLL-Devs/python-traceprint` GitHub routes. |
| Documentation | `https://lll-devs.github.io/python-traceprint/`. |

The wheel contains `traceprint` source modules, empty `py.typed`, distribution
metadata and the MIT license payload. It must import from an isolated installation
with no checkout on the path and no runtime dependency installation.

The source distribution includes `src/`, `tests/`, `examples/`, Sphinx source
under `docs/`, the metadata hook, project configuration, README, CONTRIBUTING,
CHANGELOG, LICENSE, deliverable declaration, recorded baseline release declaration
and the selected specifications. Exclude generated HTML, environments, caches,
temporary/private backups and Git objects. Rebuilding a clean extracted source
distribution must preserve its declared version without original Git ancestry.

UV cache inputs cover `pyproject.toml`, the hook, deliverable declaration, README
and source directory so changed build metadata is not hidden by a stale editable
installation. No Python dependency lockfile is required for this alpha library;
the specification integrity lock is tracked independently.

## Verification and repository products

Development tooling includes pytest, pytest-cov, Ruff, Pyright, Hatchling, PyYAML
and YAML typing support, Sphinx and Twine. Pin Macrostates CLI 0.6.0 in the dev
group for this selected composition. Existing minima are pytest 8, pytest-cov 5,
Ruff 0.6, Pyright 1.1, Sphinx 8.2 and Twine 6.1; installing current compatible
tools does not make them runtime dependencies. Ruff uses line length 88, Python
3.12 and E/F/I/UP/B/SIM rules; Pyright checks source/tests/hook in standard mode
using Python 3.12 and the local `.venv`. Pytest targets `tests` with `src` on its
path, complemented by genuinely isolated installed-wheel checks.

Sphinx imports the installed library and generates the root API reference with
signatures, public methods/properties and usage/release guidance. Use strict HTML
builds without warnings. Root repository documents link to the authoritative
specifications rather than treating `docs/` as a competing contract.

CI must cover Linux Python 3.12, 3.13, 3.14 and 3.15 plus Windows/macOS Python
3.12. Runtime jobs run tests, build wheels and check their isolated imports,
metadata, type marker and both examples. Quality checks run Macrostates integrity
and impact validation, lint/format, type checks, strict docs and source/wheel builds.
Protected primary integration requires the defined review/closure and passing
checks on the exact accepted source; configuration alone is not conformance proof.

The documentation workflow builds on main/explicit dispatch, uploads a Pages
artifact and deploys it through the `github-pages` environment. The release
workflow runs on a published GitHub release, checks out its tag with history,
verifies source/baseline provenance and closed workflows, runs tests, builds source
and wheel, performs strict Twine and isolated-wheel checks, then transfers the
artifacts to a separate publishing job. That job uses the `pypi` environment,
version-tag deployment policy and OIDC `id-token: write`; no stored API token is
required. Pin official action commits and keep build credentials separate from
publication credentials.

Release verification requires the library tag to equal `v` plus its declared
version and resolve to the exact released HEAD, with an annotated tag object.
Baseline tags must also be annotated ancestors: the specification tag's snapshot
must match current specifications, and the implementation tag's release declaration
must match the current one. The released HEAD must be integrated in `origin/main`;
there must be no open workflows, including under history. A normal Process release
plan requires CLI publication checks. The initial-snapshot exception below is
bounded to its declared version/baselines and must not silently become a general
bypass for later releases.

## Initial standalone publication

The immutable first release, v0.1.2, identifies the reviewed public root commit
6e5d9ab13dca1f95a6f985a9d8167c9472932f68. Its annotated baseline tags are
specs-1.0.0 and imp-1.0.0. The initial contract adoption and distribution identity
established those baselines; the independent Python API remains alpha.

That snapshot was established through a native bootstrap review because no
earlier public commit existed for a normal Process release plan. This completed
exception is limited to v0.1.2 and those baseline tags. It grants no exception
to later planning, review, closure, provenance or publication requirements.
Subsequent baseline releases use Process's normal change-record/release-plan
procedure and CLI release-check --publication.

tests/packaging/check_release.py retains compatibility for verifying the original
tagged snapshot. Its review evidence is recorded in the initial-publication
workflow history; GitHub release artifacts and PyPI files evidence publication.
