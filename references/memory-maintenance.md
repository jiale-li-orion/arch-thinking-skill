# Maintain architecture memory without creating a documentation project

Architecture memory exists to reduce repeated exploration and improve decisions. A note earns its place when it changes where an agent searches, what it expects to happen, what it checks before changing code, or how it diagnoses failure.

## Ownership

- README owns navigation and task-to-document routing.
- AGENTS owns stable maintenance and re-read rules.
- ARCHITECTURE owns the global model.
- STATE owns current understanding and unresolved questions.
- flows/<name>.md owns one important cross-module lifecycle.
- Existing ADRs and run records own durable decisions and concrete executions.

If a repository already has equivalent authoritative documents, extend those instead of creating parallel copies.

## Evidence and confidence

Keep observed facts, inferred mechanisms, and unknowns distinct. Attach evidence close to important claims. Use repository-relative paths, exact symbols or distinctive strings, and optionally the commit where the source was checked.

Run scripts/arch_memory.py check after meaningful memory edits. Missing paths or symbols are errors. Uncommitted source changes and changes after the recorded revision are re-read warnings, not proof that the note is wrong.

## Invalidation rules

Revisit affected memory when an entry point, call edge, payload shape or public contract changes; an authoritative state field gains another writer or moves owner; persistence, retry, timeout, cancellation or recovery behavior changes; a cited file or symbol disappears; or a real incident contradicts the documented lifecycle.

Confirm the semantic impact before rewriting the model. A rename may only require a citation update; a new state writer may change the system explanation.

## Update and pruning

Update the authoritative owner first, then dependent notes only where conclusions or navigation changed. Do not copy the entire STATE into ARCHITECTURE or duplicate a flow in multiple notes.

Delete or merge a note when it no longer changes a future search, explanation, decision, or verification. Use Git history for chronology. Keep snapshots only when they preserve otherwise-lost provenance or explain a meaningful regression.
