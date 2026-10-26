# Design a maintainable workspace knowledge system

Use this reference when entering a long-lived workspace, establishing its memory structure, or repairing duplicated and stale knowledge. The goal is continuity of understanding across sessions and tasks, not documentation coverage.

## Borrow the mechanism, not the file count

For a large coding repository, do not default to placing all architecture notes in the main source Git history. A dedicated small memory repository is often cleaner: its commits track changes in system understanding, while source commits track implementation. Link the two through repository-relative evidence paths and recorded source revisions. The same memory tool should also support a local `.arch/` directory for small projects or teams that prefer co-located docs.

The Research workspace demonstrates a useful separation of responsibilities: README routes the reader; AGENTS defines continuation and read-back rules; stable frameworks and trees preserve the global problem structure; STATE records current judgment and next choice; detailed formulation and insight assets support local reasoning; evidence and run records preserve source facts and execution results; original notes and archives retain provenance.

An engineering workspace needs the same functional separation, adapted to software behavior. Do not copy research-specific filenames mechanically. Do not create every possible file in every repository.

## Default knowledge roles

| Artifact | Owns | Changes when | Does not own |
|---|---|---|---|
| README.md | Entry point, navigation, task-to-asset routing | The knowledge map or starting procedure changes | Detailed architecture explanations |
| AGENTS.md | Stable maintenance rules, read-back conditions, ownership and update protocol | The protocol or dependencies change | Current incident status or duplicated architecture summaries |
| ARCHITECTURE.md | Global system model: boundaries, responsibilities, dependencies, authoritative state and invariants | The system boundary or a cross-cutting relationship changes | Every method or every active hypothesis |
| STATE.md | Best current explanation, open questions, competing mechanisms and next useful probe | Evidence changes the current understanding or investigation focus | Session diary or full historical chronology |
| flows/<name>.md | A specific end-to-end lifecycle whose details matter across modules | The lifecycle, state owner, contract, side effects or failure semantics change | A second copy of source code |
| Existing ADR / run record | A durable decision or a concrete execution with reproducible evidence | A decision is made or an execution occurs | The current global model |

Use existing authoritative documents when they already fulfill a role. Create a new file only if it owns distinct knowledge and has a clear update trigger.

## Global synthesis and local depth

ARCHITECTURE.md is the global model. It should explain how the major pieces fit together, where authority and state live, and which relationships constrain changes. It is a navigational model, not a complete inventory.

STATE.md is the current synthesis of what is understood and what still matters. It should make the next investigation choice intelligible without repeating the full global map.

A flow note is a local model. It follows one behavior across boundaries, with transformations, state ownership, persistence, asynchronous handoffs, completion signals, and failure/recovery paths. A local finding updates the global model only when it changes a boundary, dependency, invariant, ownership rule, or explanation that affects other flows.

This produces two connected scales of reasoning:
- Global: what system behavior and constraints explain the whole?
- Local: what mechanism explains this path, and what evidence distinguishes it from alternatives?

Do not let a local fix silently redefine the global architecture. Do not preserve a global abstraction after verified local behavior contradicts it; revise only the affected claim and its consequences.

## Separate memory history from source history

When using a separate memory repository, the source repository remains the authority for code paths, symbols, and source commit IDs; the memory repository is the authority for architecture notes and their history. Invoke the checker with both roots, for example `arch_memory.py check --root /path/to/source-repo --memory-root /path/to/architecture-memory`. This keeps source-change detection tied to source Git while keeping note commits independent. Do not automatically create or push a public repository; storage location and sharing policy are workspace decisions.

## Read-back policy

Read-back is triggered by the task and by evidence changes, not by a fixed ritual.

- At workspace entry, read README and AGENTS, then the global map and current state when the task depends on architecture.
- Before changing a flow, read its note if one exists and search current source for the relevant entry points and state writes.
- When source files change, use evidence references to identify memory notes that should be re-read.
- When a public contract, state owner, persistence rule, retry/cancellation behavior, or cross-module dependency changes, revisit both the local flow and the global model.
- If a note is contradicted by source or runtime behavior, correct the note in place and update dependent conclusions.
- For a small self-contained edit, skip unrelated architecture notes.

A source change triggers review, not automatic invalidation: confirm whether the documented behavior actually changed.

## Knowledge update protocol

1. Capture the new observation and its source.
2. Determine whether it changes a local flow, the global model, current investigation state, or only a test/run record.
3. Update the one authoritative owner first.
4. Update dependent notes only where their conclusions or navigation changed.
5. Run the evidence checker and any relevant project validation.
6. Remove duplicated or obsolete claims instead of appending another summary.

Keep observed facts, inferred mechanisms, and unresolved questions distinguishable. Cite evidence beside important claims. When Git is available, record the source revision. Use Git history for chronology; keep archives only when original provenance or a meaningful before/after comparison is needed.

## Automatic maintenance boundary

Automate mechanical work: initializing missing files without overwriting human content, checking referenced paths and symbols, finding notes affected by changed files, and flagging source revisions that need re-reading.

Keep semantic work with the agent: deciding what a code change means, whether a state owner changed, whether a hypothesis survives, and which global conclusions must be revised. A script can detect a stale citation; it cannot certify an architecture explanation.

## Pruning criteria

A knowledge asset stays only if it changes future navigation, explanation, decision, or verification. Merge or delete notes that duplicate a more authoritative owner, describe only transient task progress, or no longer affect any future decision. Prefer a small, current model plus source-linked local analyses over an ever-growing collection of summaries.
