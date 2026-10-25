# Changelog

## Unreleased

- Adopt Macrostates Process 6.0.0 and CLI 0.6.0. New documents use neutral
  technical summaries and role attribution under the public document contract.
- Prepare library 0.1.4 against the new repository baselines. Runtime behavior,
  public imports and the standard-library-only dependency policy are unchanged.

## 0.1.3 — 2026-10-25

- Mitigate the eMudhra/emSign CA incident in development and CI: require patched
  uv and certifi, bootstrap pip from the advisory's hash-verified wheel, and
  update the publishing action to its security release. Document recovery for
  existing environments.

- Expand the authoritative Macrostates specifications with detailed behavior,
  acceptance scenarios and consistent reading-order filenames.
- Refresh maintainer release guidance and remove conversation-specific setup notes
  from project documentation and process records.

## 0.1.2 — 2026-10-14

First standalone public alpha release.

- Adopt the MIT license and the `python-traceprint` distribution name; imports
  remain `traceprint`.
- Add one trace prefix per nonblank output line, preserving multi-argument
  `print()` calls and immediate partial writes.
- Preserve nesting indentation when ANSI colors are disabled.
- Add a usage guide, generated API reference, contribution instructions and
  PyPI release-preparation guidance.
- Prepare GitHub Actions tests, quality checks, documentation and artifact checks.
- Update published Macrostates packages and CLI 0.5.0, with explicit provenance
  and independent library development-version metadata.
- Remove unrelated project references from current repository content.
- Use empty `BaseEstimator` and `TransformerMixin` stand-ins in the transformer
  example, avoiding a scikit-learn dependency.

The API remains alpha; distribution naming is `python-traceprint`, imports are
`traceprint`, and the license is MIT.
