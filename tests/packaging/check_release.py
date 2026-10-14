"""Verify immutable release provenance, including the initial native bootstrap."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def check(tag: str) -> None:
    declaration = yaml.safe_load(
        (ROOT / ".macrostates/implementation/deliverables.yaml").read_text()
    )["deliverables"]["traceprint"]
    release = yaml.safe_load(
        (ROOT / ".macrostates/implementation/release.yaml").read_text()
    )
    composition = yaml.safe_load(
        (ROOT / ".macrostates/specs/composition.yaml").read_text()
    )
    assert tag == f"v{declaration['version']}", "Release tag and version differ"
    assert declaration["source"]["tag"] == tag
    assert declaration["status"] == "released"
    assert declaration["implementation"] == release["version"]
    assert declaration["specification"] == release["specification"]
    assert composition["project"]["version"] == release["specification"]
    head = git("rev-parse", "HEAD")
    for name in (tag, release["version"], release["specification"]):
        assert git("cat-file", "-t", f"refs/tags/{name}") == "tag"
        tagged = git("rev-parse", f"refs/tags/{name}^{{commit}}")
        git("merge-base", "--is-ancestor", tagged, head)
        if name == tag:
            assert tagged == head
        elif name.startswith("specs-"):
            assert not git("diff", tagged, head, "--", ".macrostates/specs")
        else:
            previous = yaml.safe_load(
                git("show", f"{tagged}:.macrostates/implementation/release.yaml")
            )
            assert previous == release
    git("merge-base", "--is-ancestor", head, "origin/main")
    for path in (ROOT / ".macrostates/implementation/workflows").rglob("*.md"):
        assert "Status: in_progress" not in path.read_text(), path
    if (ROOT / ".macrostates/implementation/release-plan.yaml").exists():
        subprocess.run(
            [sys.executable, "-m", "macrostates", "release-check", "--publication"],
            cwd=ROOT,
            check=True,
        )
    else:
        assert declaration["version"] == "0.1.2", "Missing ordinary release plan"
        assert release["version"] == "imp-1.0.0"
        assert release["specification"] == "specs-1.0.0"
    print(f"Verified {tag}, baseline tags, closed records and integrated source {head}")


if __name__ == "__main__":
    check(sys.argv[1])
