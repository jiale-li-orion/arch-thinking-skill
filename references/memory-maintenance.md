# Maintain architecture memory without turning it into a documentation project

Architecture memory exists to reduce repeated exploration and improve decisions. A note earns its place when it changes where an agent searches, what it expects to happen, what it checks before changing code, or how it diagnoses failure.

## The three durable artifacts

### ARCHITECTURE.md — stable map

Keep module responsibility, entry points, dependency direction, persistence / external-service boundaries, and links to high-value flow notes. Describe relationships rather than enumerating every file. Update it when module boundaries or important dependencies change.

### STATE.md — current model

Keep the current explanation of behavior relevant to ongoing work, unresolved questions and competing explanations, evidence needed to distinguish them, the next highest-value probe, and assumptions that remain unverified.

Replace stale conclusions in place. Use Git history for chronology where available; do not append a session diary.

### flows/<name>.md — one business lifecycle

Create only when behavior is cross-module, asynchronous, failure-prone, or likely to recur. Include:
- trigger and observable outcome;
- ordered boundaries and data transformations;
- authoritative state owner and lifecycle;
- persistence and external effects;
- success acknowledgment, timeout, retry, cancellation and recovery;
- evidence references beside the claims they support;
- unresolved branches that affect the current understanding.

A flow note should help a future agent choose its next search. It should not become a second copy of the source code.

## Evidence and confidence

Keep three categories distinct:
- **Observed:** directly supported by source, configuration, logs, test output or runtime behavior.
- **Inferred:** a mechanism that explains observations but still has a discriminating check.
- **Unknown:** a question whose answer can change the implementation or diagnosis.

Attach evidence close to each important claim. Prefer repository-relative paths and symbols. When Git is available, record the commit at which evidence was checked. Run scripts/arch_memory.py check after substantial edits; missing paths or symbols indicate broken evidence, while source changes after the recorded commit indicate a note worth re-reading.

## Invalidation rules

Revisit affected memory when an entry point, call edge, payload shape or public contract changes; an authoritative state field gains another writer or moves owner; persistence, retry, timeout, cancellation or recovery behavior changes; a cited file or symbol disappears; or a real incident contradicts the documented lifecycle.

A source change is a re-read trigger, not proof that the note is wrong. Confirm whether relevant behavior changed before rewriting the model.

## Pruning rules

Delete or merge a note when it duplicates a more authoritative note, no longer changes any search or implementation decision, or only records transient task progress. Preserve an old model only when its historical difference explains a real decision or regression; use Git history when available instead of endless snapshots.

Do not create separate indexes, decision logs, status files, diagrams, or changelogs by default. Add an artifact only when it has a unique maintenance owner and a clear re-read trigger.
