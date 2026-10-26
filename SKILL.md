---
name: arch-thinking-skill
description: Work effectively in long-lived Coding repositories by restoring workspace knowledge, following an approved design, tracing real code semantics, debugging feedback, and maintaining architecture knowledge. Use for design-led implementation, cross-module bugs, legacy-system exploration, PR / operations work, and workspace knowledge maintenance.
---

# Architecture Thinking

Use the workspace's own knowledge system as the durable memory. Restore its index first, then load only the knowledge and operating strategy relevant to the current task. Source and runtime evidence remain authoritative.

## Route by task phase

- **Approved design → implementation:** Read references/task-routing.md, section Design-led implementation. Follow the approved PRD / Tech Design and acceptance criteria; keep settled design decisions.
- **Feedback / bug:** Read references/task-routing.md, section Feedback and debugging, then references/flow-tracing.md when the mechanism crosses boundaries.
- **Legacy system / unclear behavior:** Read references/flow-tracing.md and use source evidence to recover the relevant system model.
- **PR / operations / release:** Read references/task-routing.md, section Delivery and operations.
- **Workspace knowledge setup or maintenance:** Read references/workspace-memory.md and references/memory-maintenance.md.

## Shared mechanism

1. Read repository instructions and the workspace knowledge index.
2. Identify the current task phase and the uncertainty or acceptance criterion that matters.
3. Reuse relevant workspace knowledge; search source with rg / grep and narrow reads.
4. Trace actual semantics across callers, transformations, state owners, side effects, consumers and failure paths as needed.
5. Make the smallest coherent change under the approved task and system contracts.
6. Trace semantics before deciding whether tests are needed. Add tests only when they constrain meaningful behavior or materially reduce risk; align them with the affected architecture.
7. Update only the authoritative knowledge asset whose understanding changed. Re-read dependent notes when source evidence changes.
8. Report implementation, evidence, remaining uncertainty and delivery status.

## Knowledge model

The default workspace layout is defined by references/workspace-memory.md; do not create a parallel .arch/ system if the workspace already has a coherent one. Knowledge belongs to the workspace, not implicit agent memory.

The helper scripts/arch_memory.py can initialize a minimal knowledge set, locate notes citing changed source files, and validate evidence references. It is mechanical support, not a semantic architecture analyzer.
