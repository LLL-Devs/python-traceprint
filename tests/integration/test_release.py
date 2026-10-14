from __future__ import annotations

import runpy
from collections.abc import Callable
from pathlib import Path
from typing import cast

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
read_version = cast(
    Callable[[Path], str],
    runpy.run_path(str(ROOT / "hatch_build.py"))["distribution_version"],
)


def declaration(root: Path, **overrides: object) -> Path:
    path = root / ".macrostates/implementation/deliverables.yaml"
    path.parent.mkdir(parents=True)
    library = {
        "strategy": "independent",
        "version": "0.1.2.dev0",
        "status": "development",
        "specification": "specs-0.1.0",
        "implementation": "imp-0.1.1",
        **overrides,
    }
    path.write_text(
        yaml.safe_dump({"schema_version": 1, "deliverables": {"traceprint": library}})
    )
    return path


def test_version_works_without_git_or_installed_specs(tmp_path: Path) -> None:
    declaration(tmp_path)
    assert read_version(tmp_path) == "0.1.2.dev0"
    assert not (tmp_path / ".macrostates/specs").exists()
    assert not (tmp_path / ".macrostates/implementation/release.yaml").exists()


def test_distribution_version_is_independent_of_baseline_numbers(
    tmp_path: Path,
) -> None:
    declaration(tmp_path, version="3.2.0.dev0")
    assert read_version(tmp_path) == "3.2.0.dev0"


@pytest.mark.parametrize(
    "field,value",
    [
        ("strategy", "implementation"),
        ("version", "01.1.0.dev0"),
        ("version", "imp-0.1.1"),
        ("version", None),
        ("version", "0.1.2"),
        ("status", "unknown"),
        ("specification", "spec-0.1.0"),
        ("implementation", "0.1.1"),
        ("implementation", "imp-0.2.0"),
    ],
)
def test_invalid_declarations_fail(tmp_path: Path, field: str, value: object) -> None:
    declaration(tmp_path, **{field: value})
    with pytest.raises(ValueError):
        read_version(tmp_path)


@pytest.mark.parametrize("schema", [True, 2, "1"])
def test_invalid_schema_fails(tmp_path: Path, schema: object) -> None:
    path = declaration(tmp_path)
    data = yaml.safe_load(path.read_text())
    data["schema_version"] = schema
    path.write_text(yaml.safe_dump(data))
    with pytest.raises(ValueError):
        read_version(tmp_path)


def test_missing_declaration_fails(tmp_path: Path) -> None:
    declaration(tmp_path).unlink()
    with pytest.raises(FileNotFoundError):
        read_version(tmp_path)
