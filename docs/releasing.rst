Release preparation
===================

The library is alpha and uses independent distribution versions. Repository
baselines are separately tagged with ``specs-*`` and ``imp-*``. The Python distribution
is ``python-traceprint``; its import is ``traceprint`` and license is MIT.

PyPI account setup
------------------

Verify your account email, enable two-factor authentication and save recovery
codes. PyPI requires two-factor authentication; its
`account help <https://pypi.org/help/#twofa>`_ explains setup.

For the initial release, open
`Publishing <https://pypi.org/manage/account/publishing/>`_ in your PyPI account
and add a pending GitHub Trusted Publisher using:

.. list-table::
   :header-rows: 1

   * - Field
     - Planned value
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

The publishing workflow is ``.github/workflows/release.yml`` and the GitHub
environment is ``pypi``. It runs on a published GitHub release, verifies the
annotated tag and source, builds/checks the artifacts, then uploads with OIDC. The existing ``ci.yml`` verifies code; it does not publish. Trusted
Publishing uses short-lived OIDC credentials, so a stored PyPI API token is not
needed. The first authorized upload creates the project. A pending publisher
does not reserve the name; recheck availability before publication. See PyPI's
`new-project instructions <https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/>`_.

Before publishing
-----------------

Follow the local library release policy and Macrostates review/closure gates.
Finalize the clean source history and applicable repository baselines, decide
the public API version deliberately and update the independent declaration in
``.macrostates/implementation/deliverables.yaml``. Verify that the chosen version
has not already been uploaded. Record immutable source provenance.

Run tests on supported platforms and Python versions, lint, formatting, type
checks, strict documentation builds, source and wheel builds, metadata validation
and isolated installed-wheel checks. Update the changelog for the actual release.
Only the later authorized publishing step should create tags or upload packages;
an ordinary build never does so.
