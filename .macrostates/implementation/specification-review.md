# Traceprint specification reconstruction review

Reviewed source: public release 0.1.2, commit
`6e5d9ab13dca1f95a6f985a9d8167c9472932f68`. The specification expansion describes
this runtime without altering it. Runtime code, tests, examples, build tooling,
finalized baselines and published deliverable provenance remain unchanged.
The local package moves from 1.0.0 to 1.1.0 for compatible behavioral clarification;
its origin and pending impact are separate Process records. The release guide and
public process records receive an editorial refresh while retaining release gates,
requirement coverage and historical baseline compatibility.

## Original-to-expanded requirement map

| Original owner/requirement | Expanded owner | Preservation/clarification |
| --- | --- | --- |
| project.md: purpose, timing/labels/colors, spans/decorator/logging | 001_project.md; feature owners below | Retained; adds identity, supported text-stream scope and shared-state limits. |
| project.md: observability/nonrelated-utility non-goals | 001_project.md | Retained without adding unrelated runtime functions. Example stand-ins remain explicitly educational. |
| api.md: six main root symbols | 002_api.md; 003_formatting.md | Retained; adds three existing color exports, exact signatures/defaults and returned-object/proxy boundaries. |
| api.md: non-intercepting global tracer | 002_api.md | Required existing instance, construction state, no root logging/file effects. |
| api.md: initial environment labels | 002_api.md; 008_acceptance.md API-04 | Slash parsing, trimming, depth, import timing and explicit-instance distinction. |
| interception.md: install/uninstall and cleanup | 004_interception.md | Exact capture/sink selection, repeat behavior and ownership constraints. |
| interception.md: metadata preserves text, optional colors | 003_formatting.md; 004_interception.md | Default text preserved; existing custom-field selection made explicit; timing, labels and indentation specified. |
| interception.md: ANSI-free file output | 006_logging.md | Both file routes and exact terminal-escape matching profile. |
| release.md: independent version authority and honest builds | 007_release.md | Retained; specifies existing hook input checks, failure order/messages, artifact metadata and tooling. |
| release.md: review/closure, provenance, no implicit publication | 007_release.md | Retained; completed initial-bootstrap compatibility is stated as historical facts and bounded to its original identities. |
| README scope/vocabulary/reading order | README.md | Retained and extended; all core topics numbered consistently, affected references updated, conditional compatibility annex linked. |

## Topic reference map

All eight core topics use Meta's three-digit reading-order convention. The four
legacy topic references map to their numbered owners as follows:

| Previous filename | Current filename |
| --- | --- |
| project.md | 001_project.md |
| api.md | 002_api.md |
| interception.md | 004_interception.md |
| release.md | 007_release.md |

README.md and annex_observed-compatibility.md retain their entrypoint/conditional
roles and unnumbered filenames. The package reading order, cross-references,
project entrypoint and root README's release-policy pointer use the new paths.
Original-owner names above identify historical inputs, not active reference routes.

## Runtime source-to-owner coverage

| Source surface | Authoritative owner and acceptance |
| --- | --- |
| __init__.__all__, global tracer/environment | 002_api.md; API-01 through API-04 |
| Tracer constructor/state, enabled, enable/disable, lock/unlock, configure | 002_api.md; API-02/03/05–08, IO-09/15, CTX-03 |
| Tracer.format; colors constants/converter | 003_formatting.md; FMT-01 through FMT-06 |
| Tracer.write, filtering, raw sink/mirror path, flush | 004_interception.md; IO-01 through IO-12 |
| Tracer.install/uninstall | 004_interception.md; IO-13 through IO-15 |
| Tracer.add_file_handler/remove_file_handler | 004_interception.md; IO-10/11, LOG-06/07 |
| Tracer.push/pop/span; Span entry/exit | 005_contexts.md; CTX-01 through CTX-04 |
| trace, bare/factory forms, wrapping/return/finally | 005_contexts.md; CTX-05 |
| TracerHandler constructor/emit | 006_logging.md; LOG-01/02/08 |
| TracerFileHandler open/emit/write/flush/close and escape stripping | 006_logging.md; LOG-03 through LOG-08 |
| LoggerMixin constructor/properties/initialization; proxy log and five convenience methods | 006_logging.md; LOG-09 through LOG-12 |
| distribution_version, CustomMetadataHook.update | 007_release.md; BUILD-01/02 |
| Package artifacts and existing wheel/release verification helpers | 007_release.md; BUILD-03/04 |
| Transformer and main-loop examples | 008_acceptance.md EX-01/02 |

Private mechanism names remain implementation choices. Public signatures, return
values, state/output effects, ordering and error boundaries form the replica
contract. Product docs are derived from the authoritative feature owners and
provide supporting conformance examples. The root README's release-policy link
follows the numbered owner; the maintainer guide describes ongoing releases.

## Observed compatibility decisions

The conditional annex records published-alpha observations without promoting
defects into intended future product behavior:

- `force` requests transition attempts but never bypasses `write` filtering.
- Changing enable/lock state during active contexts can leave/corrupt the stack;
  stable-state usage remains the supported cleanup contract.
- `error_stream` is accepted/stored without independent routing; installations
  are not an ownership stack and retain colors/partial-line state across sink changes.
- Configuration permits any existing attribute, including private/method names;
  this does not make those supported configuration APIs.
- Format separation uses the first matching message substring; integer RGB parsing
  lacks additional range/digit validation; shared palette mutation can invalidate it.
- First-fragment suffixes, leading whitespace and Unicode separators have specific
  output effects; direct-output failures are not transactional.
- File emission bypasses tracer enabled/filter/line state; direct mirrors bypass
  logging level/filter/lock handling; mixin instances share class-logger configuration.

No correction is introduced in this scope. These cases are descriptive constraints
for faithfully matching the existing alpha, not new desired features or required
implementation fixes. A future design change would require explicit requirements
and compatibility classification. Supported-normal-path requirements match the
reviewed implementation; there is no new required implementation gap.

## Verification scope

Validate local package/composition versions, upstream integrity, reading order,
all project-owned link targets and anchors, public signature coverage and selected
executable acceptance cases derived from the new specification. Runtime source
and build logic remain byte-identical to the reviewed public commit. Documentation
changes are limited to the approved specification and maintainer-content refresh.
No application rebuild/release or comprehensive new runtime test suite is required
for this specification-only task. The workflow records actual validation results
and user acceptance remains separate.
