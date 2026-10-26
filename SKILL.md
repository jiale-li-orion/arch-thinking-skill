---
name: arch-thinking-skill
description: Understand, trace, debug, and safely change existing software systems whose behavior crosses modules, services, state machines, persistence, or external APIs. Use for unfamiliar repositories, cross-module bugs, business-flow tracing, and maintaining architecture knowledge across sessions.
---

# Architecture Thinking

Build the smallest evidence-backed model that explains the behavior relevant to the task. Source code and runtime evidence are authoritative; architecture notes accelerate discovery but never replace verification.

## Operating loop

1. **Recover.** If .arch/ exists, read ARCHITECTURE.md and STATE.md, then only the flow notes relevant to this task. Read applicable AGENTS.md and README instructions. Treat memory as a map, not ground truth.
2. **Choose a question.** Classify the task as orientation, flow tracing, failure diagnosis, behavior change, or memory maintenance. State the concrete behavior to explain or change.
3. **Search cheaply.** Start with rg --files, rg -n, git grep, git log, git blame, and narrow source reads. Follow symbols, callers, state writes, configuration, persistence, external calls, and tests. Expand scope only when evidence requires it.
4. **Trace the behavior.** Follow the relevant path end to end: trigger → producer → transformations → authoritative state owner → persistence / external side effect → consumer → completion, failure, retry, and recovery.
5. **Separate evidence from interpretation.** Record what code or runtime evidence directly shows, what mechanism you infer, and what remains unknown. When explanations compete, find the smallest probe that distinguishes them.
6. **Change at the right boundary.** Identify the state owner and caller contract before editing. Prefer the smallest change that preserves unrelated behavior. Validate the changed path and the important adjacent failure path.
7. **Update memory selectively.** Persist only knowledge that will materially reduce future rediscovery: a durable boundary, cross-module flow, state owner, failure/recovery rule, or decision that changes future work. Fix stale notes when contradicted. Do not create a report for every task.
8. **Close the loop.** State what was verified, what remains inferred or unverified, and which memory changed. A diagram alone does not prove a flow is understood.

## Memory model

Project memory lives in .arch/ and stays intentionally small:

- ARCHITECTURE.md — stable module boundaries, responsibilities, entry points, and dependency direction.
- STATE.md — current understanding, unresolved questions, active investigation, and the next useful probe. Replace obsolete state instead of accumulating a diary.
- flows/<name>.md — only for important or repeatedly investigated cross-module behavior. Capture lifecycle, state ownership, side effects, failure paths, and source evidence.
- Durable architectural decisions may use an existing ADR convention. Do not introduce an ADR system by default.

Initialize the two core notes only when they will be maintained:

    python <skill-dir>/scripts/arch_memory.py init --root <repository>

Validate evidence after meaningful memory edits:

    python <skill-dir>/scripts/arch_memory.py check --root <repository>

Use this checkable evidence form beside important claims:

    Evidence: path=src/path/File.java symbol=methodName at=abc1234

The path is repository-relative. The symbol is an exact identifier or distinctive source string. The optional Git commit records when the source was checked. The checker reports missing paths/symbols as errors and changed evidence as stale warnings.

## Load details only when needed

- For a cross-module feature or incident, read references/flow-tracing.md.
- When creating, updating, or pruning architecture memory, read references/memory-maintenance.md.

Do not load both references for a simple local edit. Do not build a full repository graph, read every file, or introduce a database / vector store unless a concrete query need justifies it.
