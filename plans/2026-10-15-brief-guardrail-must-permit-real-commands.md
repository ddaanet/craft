## Brief: verify a guardrail with a command the system really issues, expecting ALLOW

2026-10-15. Written from a session in `/Users/david/code/ghmem`. My human
partner agreed the fact belongs in a skill rather than in shared memory, and the
session proposed `craft:test-discipline`. That proposal is input, not a
decision: verify it against the shipped skill and get a ruling before editing.

### The fact

The source is `memory/ddaanet/guardrail-must-permit-real-commands.md` in the
shared ddaanet tier, mounted in this repo too (`/gitlore:merge` if it is
missing). In short: a containment allowlist must permit the contained system's
primary operation, and that has to be checked against a real command string, not
a synthetic probe or reasoning about the pattern. ghmem's `ghmem-only` hook was
a character allowlist with no space or quote in its class, while `ghmem route`
requires a quoted, multi-word note on every verdict. So the hook blocked the
only operation the triage agent exists to perform. It had been signed off on a
provoke-and-check dispatch, which proved the hook was attached but never that it
allowed the work. The failure was silent in the worst direction: routes with
notes filling the corpus were proof that enforcement was off, and they read as
success.

### Why test-discipline

The memory already names its principle: green for the wrong reason, applied to a
guardrail. A guard has two failure directions, and the skill's red-step
discipline covers only "the test fails when it should". The missing check is the
positive control: an ALLOW case built from a command the real system issues,
beside every BLOCK case. The fact is not about plugins. Any allowlist, sandbox
rule or permission pattern has the same failure, so plugin-craft would hide it
behind a hook-specific trigger.

Check first whether the skill already carries a positive-control rule. If it
does, the fact reduces to one example sentence.

### Plan to remove the memory

In the same change that lands the skill text: delete
`memory/ddaanet/guardrail-must-permit-real-commands.md` and its line in the root
`memory/MEMORY.md`, then commit through the gitlore memory gate with a
**Remove** paragraph and `/gitlore:push`.

### Constraints

- `/Users/david/code/ghmem` is another repo: read-only from here.
