# python-traceprint

Readable print and logging output with timestamps, elapsed time, labels, nesting
depth and optional terminal colors. Requires Python 3.12 or later and has no
runtime dependencies. The API is alpha.

The distribution is named **python-traceprint**; Python code imports **traceprint**.
Importing it does not replace process streams. Install a tracer explicitly when
you want to format ordinary `print()` calls.

## Installation

Use pip >=26.2.2 or uv >=0.13.4. If your tools predate the October 2026
eMudhra/emSign incident, follow the
[certificate recovery steps](CONTRIBUTING.md#certificate-security-and-existing-environments)
before installing packages.

From a local checkout:

```bash
python -m pip install .
```

Install the public distribution from PyPI:

```bash
python -m pip install python-traceprint
```

The first public release is `0.1.2`; the API remains alpha.

[Documentation](https://lll-devs.github.io/python-traceprint/) ·
[PyPI](https://pypi.org/project/python-traceprint/)

## Quick start

```python
from traceprint import Tracer

tracer = Tracer(use_colors=False, use_tabulation=True)
tracer.install()
try:
    with tracer.span("load"):
        print("loaded", 42, "records")
finally:
    tracer.uninstall()
```

Each nonblank line gets one prefix, even when `print()` writes several arguments.
Partial writes appear immediately. Nesting adds labels and, when enabled,
indentation. Timestamps use UTC; elapsed times use a monotonic performance clock.

To avoid replacing `sys.stdout`, pass a tracer directly to `print()`:

```python
from traceprint import Tracer, trace

tracer = Tracer()


@trace(tracer_instance=tracer, label="work")
def work() -> None:
    print("doing the thing", file=tracer)


work()
```

Python logging can use the same formatting:

```python
import logging

from traceprint import Tracer, TracerHandler

tracer = Tracer()
handler = TracerHandler(tracer_instance=tracer)
logger = logging.getLogger("example")
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.propagate = False
logger.info("ready")
logger.removeHandler(handler)
handler.close()
```

Tracer labels and stream installation are shared mutable state. Use this library
for scripts and development output; it does not provide isolated thread or async
task contexts or distributed tracing.

## Documentation and examples

- [Usage guide](docs/usage.rst): configuration, spans, decorators, logging and files.
- [API reference](docs/api.rst): generated signatures and public methods.
- [Contributing](CONTRIBUTING.md): setup, checks and building HTML documentation.
- [Changelog](CHANGELOG.md): changes awaiting release.
- [Maintainer releases](docs/releasing.rst): versioning, validation and publishing.
- [Transformer example](examples/sklearn_style_transformer.py): a scikit-learn-style
  transformer with empty stand-in base classes; scikit-learn is not required.
- [Main-loop example](examples/main_loop.py): logging and nested labels.

Build the searchable HTML documentation locally:

```bash
uv sync --dev
uv run sphinx-build -W --keep-going -b html docs docs/_build/html
```

Open `docs/_build/html/index.html` in a browser, or use the published
[documentation site](https://lll-devs.github.io/python-traceprint/).

## Development

```bash
uv sync --dev
uv run macrostates check
uv run macrostates change-check
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv build
```

The canonical repository is
[LLL-Devs/python-traceprint](https://github.com/LLL-Devs/python-traceprint).
Specifications and implementation records live under `.macrostates/`. The
development environment pins Macrostates CLI 0.6.0. The distribution version has
its own authority in `.macrostates/implementation/deliverables.yaml`, independent
of the initial `specs-1.0.0` and `imp-1.0.0` repository baselines. See the
[release policy](.macrostates/specs/900_traceprint/007_release.md).

The local GitHub Actions workflow checks tests across Python 3.12–3.15 on Linux
and Python 3.12 on Windows and macOS, plus lint, types, documentation and package
builds. Documentation is built and deployed by the GitHub Pages workflow.

## License

[MIT](LICENSE), copyright © 2026 Lucas Lopez. Vendored Macrostates specifications
retain their upstream licenses.
