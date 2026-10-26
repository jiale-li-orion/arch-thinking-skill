# Task routing: design-led implementation, debugging, and delivery

This reference separates work by the state of the product and the user's current goal. Select the path that matches the evidence; do not apply all paths to every task.

## Design-led implementation

Use when the user has already completed or approved the PRD / Tech Design in chat, a document, an issue, or a linked source of truth.

1. **Recover the contract.** Read the supplied design and acceptance criteria. If they are in the conversation, use that content directly; do not assume the coding repository must contain a duplicate PRD. Inspect only the existing code, repository instructions, and relevant memory needed to map the contract.
2. **Map criteria to implementation.** For each required behavior, identify the owning module, entry point, state owner, consumer, and validation path. Reuse existing patterns and dependencies unless the design explicitly changes them.
3. **Check the implementation gap.** Distinguish already implemented, partially implemented, missing, and contradictory behavior. Do not rewrite working code merely to make it resemble a new architecture diagram.
4. **Implement in the user's requested scope.** Make the smallest coherent change. Preserve existing behavior outside acceptance criteria. Ask only when the design contains a contradiction, omits a decision that blocks implementation, or conflicts with a material repository constraint. Do not ask again about settled requirements.
5. **Verify against the contract.** First trace the implementation semantics and the real module boundaries. Do not add a test merely to assert that a method, field, mock call, or happy-path return exists. If a test materially reduces risk, make it isomorphic to the affected architecture: exercise the relevant module contract and meaningful state transition, and assert an observable acceptance criterion. Prefer one behavior-representative test over shallow test accumulation. For trivial changes, existing checks and code-semantic inspection may be sufficient. If a criterion cannot be tested in the available environment, state exactly which boundary remains unverified.
6. **Update durable knowledge only when warranted.** Record a newly discovered boundary, state owner, non-obvious contract, or reusable failure mode. Routine implementation progress belongs in the PR/task record, not a new architecture note.

The design is the specification of intended behavior; current source is evidence of actual behavior. When they disagree, preserve that distinction and report the gap instead of silently rewriting the design to fit the code.

## Feedback and debugging

Use when a user reports that a newly implemented feature is wrong, incomplete, flaky, or different from expected behavior.

1. Capture the concrete observation: expected result, actual result, triggering conditions, environment, and frequency. Reuse logs or screenshots already supplied; do not ask the user to repeat them.
2. Locate the feature entry point and trace the actual implementation through decisions, state mutations, async boundaries, persistence, external calls, and the final consumer.
3. Compare the observed path with the intended contract and any prior implementation. Identify the earliest boundary where the values, state, timing, or side effect diverge.
4. Keep competing mechanisms explicit until evidence distinguishes them. Prefer targeted reads, existing logs, narrow instrumentation, or a minimal reproduction over speculative multi-file edits.
5. Make a targeted correction after locating the responsible mechanism. If an urgent mitigation is needed before root cause is fully established, label it as mitigation and keep the investigation open.
6. Trace the actual semantics before deciding on tests. Add tests only when they meaningfully constrain the failure mechanism or prevent a plausible regression; align them with the architecture boundaries and state transitions involved. Avoid shallow validation tests and over-mocked tests that can pass while the reported behavior is still broken. Validate the reported case and relevant recovery path using the strongest available evidence, and name any unverified runtime boundary. Check neighboring call sites and state writers when the fix changes shared behavior.
7. Report the root cause with evidence, the exact change, verification performed, residual uncertainty, and PR status. Do not equate tests passing with production verification when the failing boundary was not exercised.

## Legacy repository / unclear intent

Use when no reliable design contract is available or the repository has accumulated undocumented behavior.

Start from the observable behavior and source. Recover the smallest relevant business flow before proposing architecture changes. Search symbols and references with rg / grep, then trace writes and lifecycle transitions. Read caller and consumer, not only the method that looks suspicious. Treat names, comments, tests, and old docs as evidence with different confidence, not as unquestioned truth.

If intended behavior is genuinely unknown, describe the competing interpretations and ask only the decision that changes implementation. Avoid speculative repository-wide refactors during incident diagnosis.

## Delivery and operations

After a code change:

- Trace the changed behavior through its owning module and relevant adjacent boundaries before choosing checks. Tests are evidence, not a substitute for semantic understanding.
- Inspect the diff and working tree; confirm no unrelated files or generated artifacts were changed.
- Run checks that exercise the changed contract and the most relevant adjacent path.
- Follow existing branch and PR conventions. Summarize behavior changed, evidence, tests, limitations, and rollback implications.
- Open or update a PR when requested or when it is the repository's established delivery step. Do not claim a PR is merged, deployed, or healthy without checking.
- For deployment, migrations, production toggles, deletion, or other high-impact operations, verify the target and rollback path and obtain explicit authorization where required.
- When a user reports a post-deployment issue, switch back to Feedback and debugging; the previous successful build is not evidence that the production lifecycle works.

## Lightweight task classification

Ask internally:
- Is the intended behavior already specified and approved? → Design-led implementation.
- Is there a concrete mismatch between expected and actual behavior? → Feedback and debugging.
- Is the intended behavior or state ownership unclear? → Legacy repository exploration.
- Is the change implemented and the task now about review, PR, release, or recovery? → Delivery and operations.

A task can transition between paths. For example, implementation may expose a design ambiguity, or a production report may reveal a previously undocumented state transition. Switch paths when the evidence changes; do not begin the entire workflow from the start.
