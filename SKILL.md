---
name: arch-thinking-skill
description: Understand, trace, debug, and safely change existing software systems whose behavior crosses modules, services, state machines, persistence, or external APIs. Use for unfamiliar repositories, cross-module bugs, implementing an already-approved design, feedback-driven fixes, and maintaining architecture knowledge across sessions.
---

# Architecture Thinking

Build the smallest evidence-backed model that explains the behavior relevant to the task. Source code and runtime evidence are authoritative; architecture notes accelerate discovery but never replace verification.

## Route by task phase

First identify the user's actual phase; do not force every task through the same workflow.

- **Approved design → implementation:** When the user supplies or points to an approved PRD / Tech Design, treat it as the task contract. Read references/task-routing.md § Design-led implementation. Do not repeat design exploration, rewrite the design, or ask questions already answered there. Map requirements and acceptance criteria to existing code, implement the requested scope, verify it, and report gaps. Ask only about contradictions or decisions that materially block safe implementation.
- **Implementation feedback / bug:** When a feature exists but fails a stated acceptance criterion or user-observed behavior, read references/task-routing.md § Feedback and debugging. Reproduce or localize the failure, trace the actual implementation, find the mechanism, make a targeted fix, and verify the reported case plus a relevant regression path.
- **Legacy / unfamiliar system:** When the intended behavior or architecture is unclear, start from the observable behavior and recover the relevant flow from source. Read references/flow-tracing.md; build only enough global context to explain the issue.
- **PR / operations / release:** After implementation or a fix, follow the repository's existing verification, branch, PR, deployment and rollback conventions. See references/task-routing.md § Delivery and operations. Never deploy, merge, or perform destructive operations without authorization.
- **Architecture or memory maintenance:** Read references/workspace-memory.md and references/memory-maintenance.md only when the task needs them.

## Operating mechanism

1. **Recover.** Read repository instructions and current task context. If the project already has a maintained knowledge system, follow its entry and dependency rules instead of creating a parallel one. Otherwise, use .arch/ if present: read README.md and AGENTS.md, then ARCHITECTURE.md and STATE.md as relevant. Load only flow notes needed for this task.
2. **Choose the next uncertainty.** Identify the behavior, decision, or acceptance criterion that must be explained or satisfied. Reuse current knowledge and target the gap that could change the conclusion.
3. **Search cheaply.** Prefer rg, grep, git grep, git log, git blame, and narrow source reads. Follow callers, transformations, state writes, configuration, persistence, side effects, and consumers. Expand scope when evidence requires it.
4. **Build a behavioral explanation.** Trace trigger → producer → transformations → authoritative state owner → persistence or external effect → consumer → completion, failure, retry, and recovery. Record only boundaries that change behavior or ownership.
5. **Discriminate explanations.** Separate observed facts, inferred mechanisms, and unknowns. If multiple mechanisms explain the observation, choose the smallest safe probe that makes their predictions differ.
6. **Change at the correct boundary.** Understand the caller contract and authoritative state owner before editing. Make the smallest change that preserves unrelated behavior. Prefer tracing code semantics over adding tests as a ritual; add tests only when they cover a meaningful behavior, regression risk, or contract that cannot be established adequately from the existing evidence.
7. **Maintain reusable knowledge.** Update a note only when the discovery changes future search, interpretation, implementation, or verification. Re-read notes implicated by relevant source changes. Do not turn each task into a report.
8. **Close with evidence.** State what changed, what was verified, what remains uncertain, and which durable knowledge was updated.

## Knowledge model

The default memory layout has four semantic owners (stored in `.arch/` or a separate small Git repository):

- README.md — entry point and task-to-document routing.
- AGENTS.md — stable maintenance rules, dependencies, ownership, and re-read triggers.
- ARCHITECTURE.md — global system model: boundaries, responsibilities, dependencies, state ownership, and invariants.
- STATE.md — current understanding, unresolved questions, competing explanations, and next useful probe.
- flows/<name>.md — optional local deep analysis for cross-module or failure-prone business lifecycles.

These are defaults, not a mandate. If a workspace already has equivalents such as a research tree, formulation, evidence base, and run records, preserve its semantic divisions and extend it. Do not force it into this layout.

Initialize a new memory set without overwriting existing files:

    python <skill-dir>/scripts/arch_memory.py init --root <source-repository> --memory-root <separate-memory-directory>

Find notes that cite files being changed:

    python <skill-dir>/scripts/arch_memory.py impact --root <source-repository> --memory-root <separate-memory-directory> --files path/to/File.java path/to/other.ts

After meaningful source or note changes, validate evidence:

    python <skill-dir>/scripts/arch_memory.py check --root <source-repository> --memory-root <separate-memory-directory>

Evidence references can record a repository-relative path, exact symbol or distinctive string, and optionally the Git commit at which it was checked. The checker validates references and flags likely stale evidence; it cannot prove semantic correctness.

## Testing policy

Do not add shallow validation tests that merely assert a file, field, method, mock call, status code, or happy-path return exists. First trace the actual implementation semantics: callers, state writers, transformations, persistence, async handoffs, and consumers. Use that understanding to decide whether a test is needed.

When tests materially reduce risk, make their structure isomorphic to the architecture being changed: test the relevant module boundary and business lifecycle, preserve the real contract between adjacent modules, and assert externally meaningful state transitions or outcomes. Avoid tests that invent a parallel architecture, over-mock the behavior under investigation, or pass while the reported failure remains possible. Prefer one meaningful boundary/integration test over a pile of shallow checks when that test covers the real risk. For hardware, external services, or timing-sensitive behavior, combine deterministic tests with explicit semantic tracing and name any runtime boundary that remains unverified. If the change is trivial and existing checks plus source semantics are sufficient, add no test.

## Progressive loading

- Approved design or implementation in progress: read references/task-routing.md.
- Feedback-driven fix or legacy incident: read references/task-routing.md and references/flow-tracing.md.
- Cross-module flow with unclear behavior: read references/flow-tracing.md.
- Workspace setup, global/local knowledge design: read references/workspace-memory.md.
- Updating, pruning, or validating memory: read references/memory-maintenance.md.
- Simple local edits: follow project instructions and the relevant task contract; do not load every reference.

No full-repository graph, vector database, mandatory design document, or per-task diary by default. Add mechanisms only when they reduce a concrete class of rediscovery or error.
