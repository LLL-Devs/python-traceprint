# Traceprint specification project

This file composes the specification packages that define Traceprint.

The finalized repository baselines are `specs-1.0.0` and `imp-1.0.0`.
The independent published library is `python-traceprint` 0.1.2, with an alpha API.
See [implementation](../implementation/main.md) and the
[local release policy](900_traceprint/007_release.md) for release preparation,
provenance and verification. Declarations alone do not prove a PyPI upload.

## Specification packages

This project uses:

- `meta`, version `3.0.0`, at `000_meta/`.
- `process`, version `5.1.0`, at `001_process/`.
- `repository-1`, version `4.0.0`, at `010_repository-1/`.
- `python-1`, version `2.1.1`, at `020_python-1/`.
- `python-library-1`, version `2.0.0`, at `031_python-library-1/`.
- `traceprint`, version `1.1.0`, at `900_traceprint/`.

All specifications live under `.macrostates/specs/`. The five upstream packages
are unmodified Git archive snapshots of published Macrostates release tags, selected in the
composition and verified against [composition.lock.yaml](composition.lock.yaml).
Traceprint's own package is local. Macrostates CLI 0.5.0 is pinned in the development
dependency group; `uv run macrostates check` checks selection and integrity.

## Authority

Apply this order from highest to lowest authority:

1. The definer's latest explicit instruction.
2. Traceprint-specific specifications in `900_traceprint/`.
3. Applicable directory-scoped specifications, limited to their own scope.
4. Python library specifications in `031_python-library-1/`.
5. Python language specifications in `020_python-1/`.
6. Repository specifications in `010_repository-1/`.
7. Process specifications in `001_process/`.
8. Specification package rules in `000_meta/`.

Do not resolve genuine ambiguity by silently editing a specification. Record a
reversible implementation decision, or ask when the choice materially changes
public library behavior. Installed upstream snapshots are immutable; changes
require a verified new upstream release.

## Reading order

Read package entrypoints first, then follow their internal reading orders.

1. [Meta](000_meta/README.md)
2. [Process](001_process/README.md)
3. [Repository](010_repository-1/README.md)
4. [Python](020_python-1/README.md)
5. [Python library](031_python-library-1/README.md)
6. [Traceprint](900_traceprint/README.md)
