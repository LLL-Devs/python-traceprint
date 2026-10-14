# Contributing

Use Python 3.12 or later and [uv](https://docs.astral.sh/uv/). From a checkout:

```bash
uv sync --dev
```

Develop on a topic branch. Before implementation changes, read
[the specification entrypoint](.macrostates/specs/main.md), follow its reading
order and record the work under `.macrostates/implementation/`. Macrostates owns
review, provenance and closure rules; upstream specification packages must stay
unmodified. Keep changes focused and add regression tests for behavior fixes.

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
