"""Supply the declared library version without Git or installed specifications."""

import re
from pathlib import Path
from typing import Any

import yaml
from hatchling.metadata.plugin.interface import MetadataHookInterface
from packaging.version import InvalidVersion, Version

_VERSION = r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"


def distribution_version(root: Path) -> str:
    """Validate the independent distribution declaration; never invent a version."""
    declaration = yaml.safe_load(
        (root / ".macrostates/implementation/deliverables.yaml").read_text()
    )
    if (
        not isinstance(declaration, dict)
        or type(declaration.get("schema_version")) is not int
    ):
        raise ValueError("Deliverables must declare schema_version: 1")
    if declaration["schema_version"] != 1:
        raise ValueError("Unsupported deliverable schema")
    deliverables = declaration.get("deliverables")
    if not isinstance(deliverables, dict):
        raise ValueError("deliverables must be a mapping")
    library = deliverables.get("traceprint")
    if not isinstance(library, dict) or library.get("strategy") != "independent":
        raise ValueError("Traceprint needs an independent distribution declaration")
    value = library.get("version")
    if not isinstance(value, str):
        raise ValueError("Distribution version must be a string")
    try:
        parsed = Version(value)
    except InvalidVersion as exc:
        raise ValueError("Invalid Python distribution version") from exc
    if str(parsed) != value:
        raise ValueError("Distribution version must use canonical Python syntax")
    status = library.get("status")
    if status not in ("development", "candidate", "released"):
        raise ValueError("Invalid distribution status")
    if status == "development" and not parsed.is_prerelease:
        raise ValueError("Development builds need an explicit prerelease version")
    specification = library.get("specification")
    implementation = library.get("implementation")
    for baseline, prefix in [(specification, "specs-"), (implementation, "imp-")]:
        if not isinstance(baseline, str) or not re.fullmatch(
            prefix + _VERSION, baseline
        ):
            raise ValueError("Invalid specification or implementation reference")
    assert isinstance(specification, str) and isinstance(implementation, str)
    if (
        specification.removeprefix("specs-").split(".")[:2]
        != implementation.removeprefix("imp-").split(".")[:2]
    ):
        raise ValueError("Referenced baseline contracts must match")
    return value


class CustomMetadataHook(MetadataHookInterface):
    def update(self, metadata: dict[str, Any]) -> None:
        metadata["version"] = distribution_version(Path(self.root))
