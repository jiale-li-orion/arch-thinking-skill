# arch-thinking-skill

An evidence-first architecture skill for agents working in existing, cross-module codebases.

It turns source exploration into a small, maintainable model of how a system actually behaves: module boundaries, end-to-end business flows, state ownership, side effects, and failure/recovery paths. The skill uses rg / grep and ordinary source tools as the default exploration interface. It does not require a code graph, vector database, or a large mandatory workflow.

## The idea

The durable asset is not a pile of summaries. It is a model that tells the next agent where to search, which state owns the behavior, what evidence supports the explanation, and what to re-read when code changes.

The skill keeps its entry point concise and loads focused references only for flow tracing or memory maintenance. An optional standard-library script initializes two minimal notes and checks source evidence references.

## Use

Invoke the skill for an unfamiliar repository, a cross-module bug, a business-flow investigation, or a change whose safety depends on understanding state and side effects.

The project memory convention is .arch/:
- ARCHITECTURE.md: stable module map.
- STATE.md: current understanding and unresolved questions.
- flows/: only recurring or non-trivial cross-module lifecycles.

Initialize memory from the skill checkout:

    python scripts/arch_memory.py init --root /path/to/repository

After adding evidence references:

    python scripts/arch_memory.py check --root /path/to/repository

Evidence lines use this form:

    Evidence: path=src/path/File.java symbol=methodName at=abc1234

The checker validates paths and symbols, warns when cited files have uncommitted changes, and warns when source has changed since the recorded commit. It does not claim to understand semantics automatically; an agent must still judge whether the documented behavior remains true.

## Design influences

This project uses the Agent Skills format and takes selective inspiration from:
- OpenAI Codex skill-creator: concise routing, progressive disclosure, and scripts only for deterministic repeated work.
- Anthropic's public Skills repository: a portable folder with a clear skill entry point and optional resources.
- Graphify: persistent knowledge should be queryable and evidence should have provenance.

The architecture-thinking method here is original: use cheap source search to build a task-relevant behavioral model, preserve state ownership and discriminating evidence, and re-read memory when relevant implementation evidence changes. It intentionally avoids mandatory graph generation, blanket checklists, and per-task documentation.

## References

- https://github.com/openai/codex/tree/main/codex-rs/skills/src/assets/samples/skill-creator
- https://github.com/anthropics/skills
- https://github.com/Graphify-Labs/graphify

## License

MIT. See LICENSE.
