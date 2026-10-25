# Contributing

Use Python 3.12 or later and [uv](https://docs.astral.sh/uv/) 0.13.4 or later.
Before installing dependencies, follow the certificate recovery steps below if
your tools predate the October 2026 eMudhra/emSign incident. From a checkout:

```bash
uv sync --locked --dev
```

Develop on a topic branch. Before implementation changes, read
[the specification entrypoint](.macrostates/specs/main.md), follow its reading
order and record the work under `.macrostates/implementation/`. Macrostates owns
review, provenance and closure rules; upstream specification packages must stay
unmodified. Keep changes focused and add regression tests for behavior fixes.

## Certificate security and existing environments

The [Python security advisory](https://discuss.python.org/t/109576) requires
pip >=26.2.2, uv >=0.13.4 and certifi >=2026.10.19. Updating certifi or the OS
trust store alone does not repair pip's vendored certificate bundle.

In each Python environment that has pip, bootstrap the advisory's exact wheel
and SHA-256 before fetching anything from an index:

```bash
python -m pip --disable-pip-version-check install --no-index --no-deps --no-cache-dir "pip @ https://files.pythonhosted.org/packages/3f/06/3e4420302363fbb71be3c7f35ce042f54bfca330e3e66b3a2e3c4cca579f/pip-26.2.2-py3-none-any.whl#sha256=fd7f4dfa8190e014013b9f08f3e973f4e4c26ffd179a204895533a7254813a70"
python -m pip install --upgrade "certifi>=2026.10.19" "uv>=0.13.4"
```

Run these commands with that environment's Python, including newly created
pip-seeded virtual environments. For a standalone uv installation, first update
the OS certificate store using your platform's security updates, then run
`UV_SYSTEM_CERTS=true uv self update` (POSIX shell). Verify `uv --version` before
running `uv sync --locked --dev` to repair this checkout's `.venv`; uv normally
creates it without pip. On macOS python.org installations, also update certifi
using each framework installation's Python as described in the advisory.

The committed `uv.lock` makes CI and contributor installs reproducible.
The lockfile and dev dependency floor keep certifi patched for development;
`tool.uv.required-version` rejects older uv. CI bootstraps patched pip before
installing its pinned uv, uses locked dependencies, and pins the patched
publishing action, whose container has its own dependency bundle. Rebuild any
external container images with `--pull --no-cache` after updating their system
certificates and Python tools. This repository has no container build definition.
Traceprint's runtime remains standard-library-only; these repository changes do
not update other virtual environments or the host's certificate store.

## Checks

```bash
uv run macrostates check
uv run macrostates change-check
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run sphinx-build -W --keep-going -b html docs docs/_build/html
uv build
uv run python tests/packaging/check_wheel.py dist
uv run python examples/sklearn_style_transformer.py
uv run python examples/main_loop.py
```

The wheel check installs the built distribution into a temporary isolated
environment and checks imports, metadata, type markers and both examples.
GitHub Actions runs runtime checks across the supported Python versions and
operating systems; an individual local run covers its own Python and platform.

## Documentation

Edit the usage guide for examples and configuration guidance. The Sphinx API
reference reads the public signatures and docstrings from the installed package,
so update those when behavior changes. Add changes under `Unreleased` in
[CHANGELOG.md](CHANGELOG.md). Build HTML using the command above and open
`docs/_build/html/index.html`; generated output is ignored by Git.

## Proposing a change

Describe the concrete problem, resulting behavior and checks performed in the
pull request. For a public API change, explain compatibility impact and update
the relevant local specifications deliberately. Workflow review and closure must
finish before integration. Release versions, tags, publishing and history changes
require their own authorized release work; ordinary builds do not perform them.
