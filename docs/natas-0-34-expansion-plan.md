# Natas 0-34 Expansion Plan

## Scope

CEI Labs Natas will provide Start Here plus 35 original web-security
transitions, `natas-00` through `natas-34`: 36 CTFd challenges. This supersedes
the former 0-14 subset. The implementation is a clean-room rebuild guided by
publicly known web-security concepts and must not copy OverTheWire source,
passwords, flags, exact requests, page layouts, or third-party walkthrough
prose.

The current target is one per-team `target-attacker` pair. Expansion keeps that
model: one target container with level endpoints on ports `8000-8034`, one
attacker container, and one `instance_group: natas`. No additional public
services are introduced.

## Architecture Contract

| Item | Current | Expanded contract |
| --- | --- | --- |
| Playable levels | 0-14 | 0-34 |
| CTFd challenges | 16 | 36: Start Here plus 35 levels |
| Target endpoints | 8000-8014 | 8000-8034 |
| Web identities | `natas0`-`natas14` | `natas0`-`natas34` |
| Dynamic secret keys | `natas1`-`natas14`, terminal | `natas1`-`natas34`, one terminal key |
| Shared range | one target + one attacker per team | unchanged |

- Define `FIRST_LEVEL`, `LAST_LEVEL`, and `PORT_BASE` once; derive users,
  webpass files, vhosts, banners, themes, audit loops, and generated challenge
  metadata from them.
- Every level receives only its next-level material. Runtime secrets never
  enter web-process environments, served trees, image layers, logs, or shared
  session/database stores.
- Database-backed levels use a separate local-only schema and least-privilege
  identity per level. Credentials live in owner-only runtime files and are not
  Dockerfile literals.
- Stateful levels namespace sessions, mutable artifacts, and completion tokens
  by team/instance. Reset removes all mutable state.
- High-risk upstream concepts are modeled behaviorally: no real shell command
  execution, unsafe native deserialization, arbitrary file inclusion, real
  process spawning, or learner-controlled interpreter execution is permitted.

## Clean-Room Curriculum Matrix

| Levels | Original CEI Labs concept | Safe mechanism | Core isolation gate |
| --- | --- | --- | --- |
| 15-16 | Boolean response-oracle query validation | Isolated SQLite lookup with two stable outcomes. | Disposable DB; no stacked statements/extensions; server-side completion validation. |
| 16-17 | Denylist failure in command-like search | Custom evaluator over in-memory training data, not a shell. | No subprocess, filesystem secret, inherited environment, or egress. |
| 17-18 | Timing response oracle | Application-layer deterministic delay with capped concurrency/jitter. | Per-instance worker/quota; no shared timing process. |
| 18-19 | Predictable numeric session state | Challenge-only bounded session store with one local privileged state. | Per-instance namespace, strict cookie scope, rate limit. |
| 19-20 | Encoded weak session token | Strict custom token codec over bounded session state. | No framework serialization or object decoding. |
| 20-21 | Delimiter-injected session record | Private, ephemeral custom record parser with a two-request state transition. | No path control/log reuse; reset state. |
| 21-22 | Cross-application session trust | Two internal app routes with deliberately shared challenge session state. | Distinct local hostnames, keys, storage, and cookie scope outside the lab. |
| 22-23 | Redirect/execution mismatch | Route emits a redirect and controlled body marker; secure comparator terminates. | No external redirects, no-store response, generated local token only. |
| 23-24 | Numeric-prefix coercion | Pinned toy parser with insecure and strict comparators. | No real authentication; runtime semantics unit-tested. |
| 24-25 | Parameter shape/type confusion | Controlled request parser and in-memory comparison model. | Depth/count caps; no debug errors or shared middleware state. |
| 25-26 | File/log data-flow weakness | Synthetic resolver/audit fixture interpreter with inert markers. | No native include/eval/shell, host mounts, served writable directory, or external path resolution. |
| 26-27 | Unsafe serialized-state concept | JSON project parser and virtual export sink, never native object deserialization. | Size/depth caps; virtual sink only; no object hooks/filesystem writes. |
| 27-28 | Identity normalization ambiguity | Custom bounded account-store comparison model. | Per-instance namespace; no real account/DB collision. |
| 28-29 | ECB integrity failure concept | Deterministic visual block/token assembler and miniature allowlisted query model. | No real encryption oracle, DB, shared key, or raw input logging. |
| 29-30 | Filename-to-command interpretation | Parser emulator and fixed virtual command catalog. | No Perl `open`, shell, subprocess, or writable executable directory. |
| 30-31 | Repeated-parameter type propagation | Fixed form parser and mock quote/query model. | No real DBI/database; pinned parser behavior; request limits. |
| 31-32 | Legacy multipart/input ambiguity | Modern app simulation of assigned training-artifact selection. | Allowlisted virtual artifacts only; no host paths or process calls. |
| 32-33 | Legacy command-execution reasoning | Command emulator with fixed safe output catalog. | No real RCE; a real historical interpreter is prohibited in the shared target. |
| 33-34 | Upload/archive metadata trust boundary | Simulated upload registry and benign metadata lifecycle event. | No executable uploads, PHAR/native deserialization, magic methods, include, or writable web root. |
| 34 terminal | Completion/debrief | Static completion view or server-side terminal marker. | No next credential or secret-bearing terminal service. |

## Implementation Sequence

1. **0-14 repair foundation:** dynamic materials, spoiler correction, strict
   secret schema, 0-14 runtime audit, and passing 12/13 RCE isolation audit.
2. **Range foundation:** constants, 35 identities/vhosts/endpoints/webpass
   chain, secret-sink inventory, generator/stage/inventory/docs expansion,
   placeholder authenticated endpoints, and generated contracts. The stage
   count changes from 16 to 36 only in this PR.
3. **Batch A:** original levels 15-19 plus intended/negative runtime cases.
4. **Batch B:** levels 20-24 plus state/session and parser isolation tests.
5. **Batch C:** levels 25-29 after file/log/data-flow containment review.
6. **Batch D:** levels 30-34, terminal behavior, full 0-34 audit, two-team
   secret uniqueness, immutable image validation, and deployment rehearsal.

Each level requires: original scenario and source, dynamic sink inventory,
three progressive hints, instructor writeup, positive solve, negative isolation
test, deterministic reset, and no public/outbound dependency. Full 0-34 audit
must exercise every intended endpoint from an attacker-equivalent client and
redact secret values in failures.

## References

- [OverTheWire Natas](https://overthewire.org/wargames/natas/): public
  progression and level model.
- [CertCube Natas reference](https://blog.certcube.com/overthewire-natas/):
  concept discovery reference only. It is not copied into CEI Labs materials.
