# arch-thinking-skill

An evidence-first architecture and implementation skill for agents working in existing codebases.

The primary use case is not asking an agent to invent a new product design. The user has usually finished the PRD and Tech Design in chat and wants the agent to implement that contract faithfully, respond to feedback, debug defects, verify changes, and handle PR / operational follow-through. A separate path handles legacy repositories whose actual behavior and intended contract are unclear.

## Core distinction

- Approved design + implementation in progress: treat the supplied design and acceptance criteria as the contract. Map them to existing code, implement the gap, verify, and report. Do not repeat design exploration.
- Feedback / bug: compare expected and actual behavior, trace the real path and state owner, find the earliest divergence, make a targeted fix, and verify the relevant regression path.
- Legacy / unclear repository: reconstruct the smallest evidence-backed behavioral model before making broad changes.
- PR / operations: verify the diff, checks, delivery status and rollback implications; do not claim actions that were not confirmed.

## Testing philosophy

The skill does not equate more tests with better engineering. Trace code semantics first, then add a test only when it constrains a meaningful behavior or regression risk. Test structure should mirror the affected architecture and its contracts; shallow existence checks, mock-call assertions, and happy-path-only tests are not substitutes for understanding the actual implementation.

## Knowledge maintenance

The memory can live outside the coding repository, ideally in a small dedicated Git repository. This keeps architectural reasoning out of the main code diff while preserving its own history. Pass the source repo with `--root` and the separate memory directory with `--memory-root`. The legacy in-repository `.arch/` layout remains supported.

Example setup:

    mkdir -p ~/intern/来源项目/arch-memory/my-service
    git -C ~/intern/来源项目/arch-memory/my-service init
    python scripts/arch_memory.py init --root /path/to/my-service --memory-root ~/intern/来源项目/arch-memory/my-service

The memory repository stores semantic notes; source evidence paths remain relative to the coding repository.

The default in-repository memory convention is `.arch/`:
- README.md routes the next reader to the right knowledge.
- AGENTS.md owns stable maintenance and read-back rules.
- ARCHITECTURE.md owns the global system model.
- STATE.md owns current understanding and unresolved questions.
- flows/ holds only important, recurring or failure-prone cross-module lifecycles.

If a workspace already has an established knowledge architecture, preserve its semantic roles rather than creating parallel documents. See references/workspace-memory.md for the design principles distilled from a long-running research workspace.

Initialize a new memory set:

    python scripts/arch_memory.py init --root /path/to/repository --memory-root /path/to/separate-memory-repo

Find architecture notes affected by changed source files:

    python scripts/arch_memory.py impact --root /path/to/repository --memory-root /path/to/separate-memory-repo --files src/Foo.java src/Bar.ts

Validate cited evidence:

    python scripts/arch_memory.py check --root /path/to/repository --memory-root /path/to/separate-memory-repo

The checker can verify references and flag likely stale evidence; semantic validity still requires reading the code.

## Design influences

The skill uses progressive disclosure and small deterministic helpers found in established skill repositories, but its workflow and memory model are designed around evidence-backed system understanding, faithful execution of an approved design, feedback-driven debugging, and maintainable cross-session knowledge.

References:
- https://github.com/openai/codex/tree/main/codex-rs/skills/src/assets/samples/skill-creator
- https://github.com/anthropics/skills
- https://github.com/Graphify-Labs/graphify

## License

MIT. See LICENSE.
