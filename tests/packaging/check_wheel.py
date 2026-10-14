"""Check a wheel from an isolated environment, including both shipped examples."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import venv
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def check(dist: Path) -> None:
    wheels = list(dist.resolve().glob("python_traceprint-*.whl"))
    if len(wheels) != 1:
        raise ValueError(f"Expected one python-traceprint wheel, found {wheels}")
    declaration = yaml.safe_load(
        (ROOT / ".macrostates/implementation/deliverables.yaml").read_text()
    )
    expected_version = declaration["deliverables"]["traceprint"]["version"]
    with tempfile.TemporaryDirectory() as directory:
        isolated = Path(directory)
        environment = isolated / "venv"
        venv.create(environment, with_pip=True)
        python = environment / (
            "Scripts/python.exe" if os.name == "nt" else "bin/python"
        )
        env = dict(os.environ)
        env.pop("PYTHONPATH", None)
        subprocess.run(
            [
                str(python),
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                "--no-cache-dir",
                "--no-index",
                "--no-deps",
                str(wheels[0]),
            ],
            cwd=isolated,
            env=env,
            check=True,
        )
        subprocess.run(
            [
                str(python),
                "-c",
                """
import io
import sys
from importlib.metadata import distribution
from pathlib import Path
import traceprint

dist = distribution('python-traceprint')
assert dist.metadata['Name'] == 'python-traceprint'
assert dist.version == sys.argv[1]
assert not dist.metadata.get_all('Requires-Dist')
assert dist.metadata['License-Expression'] == 'MIT'
assert dist.metadata['License-File'] == 'LICENSE'
assert dist.read_text('licenses/LICENSE').startswith('MIT License')
assert Path(traceprint.__file__).with_name('py.typed').is_file()
stream = io.StringIO()
target = traceprint.Tracer(stream=stream, use_colors=False,
                          output_format='[trace] {original_message}')
print('hello', 'world', file=target)
assert stream.getvalue() == '[trace] hello world\\n'
print(f'Installed {dist.metadata["Name"]} {dist.version}; wheel checks passed')
""",
                expected_version,
            ],
            cwd=isolated,
            env=env,
            check=True,
        )
        for name in ("sklearn_style_transformer.py", "main_loop.py"):
            subprocess.run(
                [str(python), str(ROOT / "examples" / name)],
                cwd=isolated,
                env=env,
                check=True,
            )


if __name__ == "__main__":
    check(Path(sys.argv[1] if len(sys.argv) > 1 else "dist"))
