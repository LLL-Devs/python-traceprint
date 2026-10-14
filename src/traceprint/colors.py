"""ANSI color helpers used by traceprint."""

from __future__ import annotations

RESET = "\033[0m"
DARK_GREY = "\033[90m"


def hex_to_ansi(hexstr: str) -> str:
    """Convert a ``#RRGGBB`` value to an ANSI truecolor foreground sequence."""
    value = hexstr.removeprefix("#")
    if len(value) != 6:
        raise ValueError(f"Expected #RRGGBB color, got {hexstr!r}")

    try:
        red, green, blue = (int(value[index : index + 2], 16) for index in (0, 2, 4))
    except ValueError as exc:
        raise ValueError(f"Expected #RRGGBB color, got {hexstr!r}") from exc

    return f"\033[38;2;{red};{green};{blue}m"


DEFAULT_COLORS = [
    hex_to_ansi("#52C97F"),
    hex_to_ansi("#68BCCD"),
    hex_to_ansi("#7D7FD2"),
    hex_to_ansi("#C891D8"),
    hex_to_ansi("#DDA5BE"),
    hex_to_ansi("#E4C9B9"),
    hex_to_ansi("#E5EACC"),
    hex_to_ansi("#E0F2DF"),
]
