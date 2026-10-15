# Formatting and colors

## Format fields

The exact default output format is:

```text
[{timestamp}][{cumulative}][{elapsed}][{label_full}] {original_message}
```

Use Python string formatting with these named values, all strings:

| Field | Value |
| --- | --- |
| `timestamp` | Current aware UTC datetime formatted with `timestamp_format`. |
| `cumulative` | Performance-clock seconds since construction, `f"{seconds:.3f}s"`. |
| `elapsed` | Seconds since the previous `format` call, `f"+{seconds:.3f}s"`. |
| `label` | The final label, or empty; append `/>` for regular labeled messages. |
| `label_full` | The slash-joined label stack, or empty; same regular-message suffix. |
| `original_message` | The input string without further stripping or interpolation. |

At each `format` call, read the performance clock, compute elapsed from the last
format time and cumulative from the start time, then set last-format time to the
new value. Obtain the UTC timestamp separately. Formatting advances timing even
when called directly, when the tracer is disabled, or when a later formatting
operation raises. Continuation fragments, blank writes, filtered writes and
flushes do not call `format` and do not advance timing.

Clocks measure tracer age and gaps between formatted messages, not exclusive
span duration. Timing text has three fractional digits and an `s` suffix, with
an explicit `+` before elapsed text. The default timestamp uses
`%Y-%m-%d %H:%M:%S`; `%z` yields `+0000`.

Compute the raw full label by joining labels with `/` and the short label from
the final entry. If the full label is nonempty and the message does not start
with literal `>` or `<`, append `/>` to both values. Otherwise keep them raw.
This rule examines the first character without stripping leading whitespace;
it is not a special transition object. Label strings are not escaped.

Custom formats may select, omit, repeat or reorder fields. Preserve message text
when the format includes `original_message`; do not force it into a format that
omits it. Unknown fields, incompatible format syntax and invalid timestamp formats
use the standard formatting/datetime exception behavior; there is no silent fallback.
For incremental writes, metadata/custom suffixes are applied to the first
nonblank fragment only; see [Writes](004_interception.md#writing-fragments).

## Color values

`RESET` is `"\x1b[0m"`; `DARK_GREY` is `"\x1b[90m"`. `DEFAULT_COLORS` is an
ordered mutable list of truecolor foreground sequences generated from:

| Depth modulo 8 | RGB hex | Red, green, blue |
| --- | --- | --- |
| 0 | `#52C97F` | 82, 201, 127 |
| 1 | `#68BCCD` | 104, 188, 205 |
| 2 | `#7D7FD2` | 125, 127, 210 |
| 3 | `#C891D8` | 200, 145, 216 |
| 4 | `#DDA5BE` | 221, 165, 190 |
| 5 | `#E4C9B9` | 228, 201, 185 |
| 6 | `#E5EACC` | 229, 234, 204 |
| 7 | `#E0F2DF` | 224, 242, 223 |

The sequence for channels `r`, `g`, `b` is exactly
`"\x1b[38;2;{r};{g};{b}m"`, with decimal channel values. Select the current
line color at index `depth % len(color_scheme)`; custom palettes cycle by their
own length. No terminal capability negotiation beyond TTY color detection is
required. A caller can explicitly request ANSI output to a non-TTY sink.

The supporting module `traceprint.colors` also exposes
`hex_to_ansi(hexstr: str) -> str`, although it is not a root export. For normal
hex input, remove a single leading `#`, require six remaining characters, parse
each pair using base-16 integer conversion and generate the sequence above.
Bad length or pair-conversion failure raises
`ValueError(f"Expected #RRGGBB color, got {hexstr!r}")`; conversion failure chains
the original `ValueError`. No additional clamping is performed. Malformed inputs
accepted by Python's integer parser are discussed in the
[compatibility annex](annex_observed-compatibility.md#format-and-color-edges).

## Color and indentation composition

After formatting fields into `text`, compute `indent` as four literal spaces
times depth when tabulation is enabled, otherwise the empty string. Indentation
must have the same placement whether colors are enabled or disabled.

1. If `metacolor` is falsey, prepend `indent` to the entire `text`. When colors
   are enabled, surround that complete result with the selected line color and
   `RESET`; otherwise return it directly.
2. If `metacolor` is truthy, find the first occurrence of the input message in
   the formatted `text`. Split into `meta_part` before that occurrence and
   `message_part` from that occurrence through the end. With colors disabled,
   return `meta_part + indent + message_part`. With colors enabled, return:

   ```text
   metacolor + meta_part + RESET + line_color + indent + message_part + RESET
   ```

3. If the message does not occur in `text`, prepend `indent` to the whole text.
   With colors enabled use `metacolor + indent + text + RESET`; with colors
   disabled use `indent + text`.

This describes string concatenation, not literal names in emitted output. Do not
strip caller-supplied ANSI from console output. An empty `meta_part` still has
its metadata color/reset framing when colors are enabled. `format` adds no
newline of its own and does not update the fragment line state.

The first-substring rule is a compatibility detail of the existing formatter;
it is not a promise of placeholder-aware parsing. See the
[compatibility annex](annex_observed-compatibility.md#format-and-color-edges)
when a custom format repeats a message or includes it in metadata.
