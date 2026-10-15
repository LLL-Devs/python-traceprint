Maintainer releases
===================

The library is alpha and uses independent distribution versions. Repository
baselines are separately tagged with ``specs-*`` and ``imp-*``. The Python distribution
is ``python-traceprint``; its import is ``traceprint`` and license is MIT.

Release preparation
-------------------

Follow the repository's
`release policy <https://github.com/LLL-Devs/python-traceprint/blob/main/.macrostates/specs/900_traceprint/007_release.md>`_
and Macrostates review/closure gates. The authoritative distribution version is
``deliverables.traceprint.version`` in
``.macrostates/implementation/deliverables.yaml``. Repository baseline changes
alone do not require another Python package release.

For a package release, assign an unused PEP 440 version according to API impact,
update the changelog, and record the exact specification/implementation baselines,
release date and immutable source tag. Preserve earlier release provenance.
Complete the reviewed integration into ``main`` before publishing.

Run the checks in ``CONTRIBUTING.md``, including supported-platform tests, lint,
formatting, types, strict documentation, source/wheel builds and isolated-wheel
checks. Validate distribution metadata with ``uv run twine check --strict dist/*``.

Publishing configuration
------------------------

``.github/workflows/release.yml`` uses GitHub-to-PyPI Trusted Publishing with OIDC.
Its publisher configuration is:

.. list-table::
   :header-rows: 1

   * - Field
     - Configured value
   * - PyPI project name
     - ``python-traceprint``
   * - GitHub owner
     - ``LLL-Devs``
   * - GitHub repository
     - ``python-traceprint``
   * - Workflow filename
     - ``release.yml``
   * - GitHub environment
     - ``pypi``

The separate ``ci.yml`` workflow validates changes. The publishing workflow has
an artifact-building job and a separate upload job in the ``pypi`` environment;
the upload uses a short-lived OIDC credential rather than a stored PyPI API token.

Publication and verification
----------------------------

Create an annotated ``v<version>`` tag for the exact integrated release commit.
The declared baseline tags must be annotated ancestors, with the specification
snapshot and implementation declaration matching the release policy. Published
tags and distribution versions are immutable.

Publishing a GitHub release for that tag triggers the workflow. Its build job
verifies tag/source provenance and closed workflows, runs tests, builds the
source and wheel artifacts, and checks metadata and isolated installation. The
upload job publishes those verified artifacts to PyPI.

Confirm that both jobs succeeded, the expected files are available on PyPI, and
their hashes match the verified build artifacts. Verify installation from PyPI
in an isolated environment. A release declaration or GitHub release page alone
does not establish a successful upload. Ordinary builds never tag or publish.
