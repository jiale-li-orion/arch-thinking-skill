# Engineering Thinking: Understanding, Implementing, and Evolving Systems

This document preserves reusable methods of engineering judgment. ARCHITECTURE explains the actual system, STATE tracks the current task, and AGENTS holds project instructions. Read the core method and the six engineering decision rules first; load other sections when relevant.

## Core Method

**Explain how a behavior occurs, who owns it, and what changing it would affect; then make the smallest complete change and deliver an observable result.**

Keep three sources of evidence distinct: approved designs and user requirements define expected behavior; source code and configuration explain what a particular version implements; runtime observations establish what happened in a particular environment. When they diverge, locate the responsible contract, execution path, or deployment condition before choosing to fix code, complete implementation, adjust the environment, or propose a design revision. Within an approved design, the agent makes implementation decisions autonomously. Conflicts affecting product behavior or architecture commitments go to the user with concrete consequences and a proposed resolution.

The **delivery loop** is *contract → implementation gap → change → verification → delivery*. The **understanding loop** is *global relationships → local tracing → behavioral explanation → revised global model*. They alternate: understanding directs action; observed outcomes correct the system model.

**Global understanding guides local tracing.** Identify entry points, responsibilities, state owners, external dependencies, and material constraints before choosing where to search. For a function, inspect invocation conditions upstream and consumers and side effects downstream.

**Local evidence revises global understanding.** A new writer, implementation-selection branch, cache bypass, or background lifecycle can affect other paths. When boundaries, ownership, or dependencies change, revise the appropriate architecture text and diagrams. Investigate as deeply as the task contract and impact surface demand, then proceed once the explanation supports the required action.

Architecture understanding must predict concrete behavior. Given an entry point, configuration version, and object state, explain which implementation executes, who updates the authoritative value, and which consumer observes the result. Changing an edge should reveal affected user behavior, failure recovery, and historical-data paths. Module labels only help navigation; conditional call, data, and ownership relationships support such predictions. When observations diverge from predictions, examine the earliest divergent edge and revise the global model.

## Six Engineering Decision Rules

1. Trace code semantics before deciding whether testing is necessary. Tests do not substitute for understanding code.
2. When tests are warranted, their structure should correspond to the affected architectural modules and business paths, verifying real contracts, critical state transitions, or user-observable behavior.
3. Do not add unnecessary tests or pad verification with field checks, mock-call assertions, or trivial happy-path tests.
4. Prefer the smallest **complete** change; preserve existing interfaces, data formats, and unrelated behavior.
5. Preserve the distinction between design contracts and actual implementations; resolve conflicts explicitly rather than silently allowing either to overwrite the other.
6. Do not generate a summary for every task, retain investigation steps without reusable value, or introduce full code graphs, vector databases, or large documentation systems by default.

The following methods were distilled from these rules and real engineering situations. Verify each example's conditions in the target system.

## Let the Global Model Direct Local Tracing

Start with the smallest relevant system outline: user entry points, runtime units, state owners, external dependencies, and deployed versions. Select a real path capable of producing the target behavior; confirm registration, configuration, and invocation conditions, then trace inputs, writes, handoffs, and final consumers. If another writer, bypass, or version branch changes global dependencies, revise the system diagram. Leave function-level details in the source and necessary path explanations.

For example, `save` may exist in a legacy API, background imports, and a new page. Determine which path the request actually selects, which storage is authoritative, and which consumer reads the value before choosing what to reuse or edit. A matching name identifies a candidate; runtime selection and the data lifecycle establish relevance. Move to implementation when you can explain the behavior, assign change responsibility, and identify material impact paths.

## Choose Reuse, Adaptation, or Separate Ownership by Contract Differences

Describe the approved design and the existing implementation using the same dimensions of a business behavior: entry point, input semantics, state transition, output, failure and recovery, and affected consumers. Identify existing capabilities, real gaps, and evidence. Reuse when contracts match; adapt explicitly at a boundary when formats differ but internal semantics agree; keep separate entry points when responsibilities differ, specifying shared mechanisms, state ownership, and coexistence conditions.

For example, an existing `save` fills defaults, emits an event, and acknowledges after transaction commit. A new requirement saves a draft and delays publication. Direct reuse may notify consumers prematurely; a separate persistence implementation may introduce a second authoritative value. Separate *persist draft* from *publish event*, inspect existing consumers and historical data, then choose a transition within the current owner, a boundary adapter, or a new flow with explicit selection conditions. Design establishes the target; code and runtime evidence establish the present behavior. Resolve substantial product-semantic or data-compatibility conflicts with a concrete difference and recommendation.

## Recover Implicit Contracts from Scattered Implementations

**The unit of understanding is a conditional business behavior.** Recover what must be true before invocation, what must remain true while it runs, what completion guarantees, and who continues its side effects. Directories, classes, and symbols provide search entry points; business identity, state transitions, and ownership determine which code belongs to one explanation. A responsibility may span an entry point, shared libraries, and background jobs, while a module may serve several responsibilities. Recover these boundaries conceptually before choosing the change scope.

Infer implicit contracts from usage. What does the caller do immediately after a return, and which guarantee does that imply? What state and branch conditions does the callee require? What must persisted data and downstream consumers assume remains stable? Compare both sides for the same object, version, and execution phase to find gaps between guarantees and dependencies. Trace the success path as well as relevant retry, cancellation, recovery, and concurrency paths; use the flow-tracing reference for specific procedures.

Distinguish an **implementation dependency** from a **behavioral commitment worth preserving**. Code may reveal reliance on ordering, a single writer, or a default. User requirements, approved designs, external interfaces, and actual consumers determine its compatibility value. Record who relies on the condition, why, and what changes without it. Then preserve it, migrate the dependency, or revise the contract. A successful run supports only the conditions of that run; durable compatibility judgments also examine callers and historical data.

## Derive End-to-End Correctness from Local Guarantees

At module handoffs, upstream guarantees must satisfy downstream preconditions. Across time, identify how a guarantee remains valid: *check then act* depends on whether the checked fact still holds when action occurs. Single-call correctness must combine with concurrent writes, retry identity, and failure recovery to explain multiple calls. At every step ask who establishes a condition, what can invalidate it, who consumes it, and who maintains or rechecks it.

Reconstruct system-wide constraints and owners: how duplicate business effects are controlled, how object versions persist through computation and commit, what stage completion acknowledgments cover, and how resources are eventually released. The actual business determines the constraints. When no owner maintains one, identify the missing responsibility; when several do, compare scope and coordination. Connect guarantees and their dependencies explicitly in diagrams to predict behavior from module relationships.

## Explain How State Produced the Observed Result

Express a causal hypothesis as a traceable mechanism: **trigger → selected path → critical state change or handoff → propagation → user observation**. Distinguish where the symptom appears, where the deviation first forms, and where the violated contract should be restored. Workload, configuration, or timing may trigger failures; shared state, acknowledgment semantics, or recovery policies may make them occur and propagate. Preserve each role when factors jointly explain the result.

A causal claim must show how the result arises and why available evidence favors it. Code predicts behavior under stated conditions; runtime evidence checks an instance's actual conditions and path. Competing explanations should focus on differences that change repair decisions and yield discriminating observations. Interpret a fix by its actual intervention: improving a patch that changes caching, timing, and inputs together supports the combined intervention, while finer attribution needs evidence separating those effects.

Attribution depth should serve engineering decisions. Proceed if local evidence already supports a safe, complete repair. Gather further evidence if uncertainty could change the repair site, compatibility boundary, or recovery behavior. Shared mechanisms that explain several failure paths belong in architecture knowledge; incident-specific details belong with the task.

## Reconstruct Producers, Consumers, and Lifecycles from Business Behavior

Choose a real request, object, or event, and trace **production → transformation → handoff → write → read → consumption**. Preserve business identity, version, units, and time semantics; examine creation, cancellation, timeouts, retries, completion, and release of resources. Search for assignments, updates, resets, and deletions to identify every relevant writer.

For file processing, examine upload, object storage, queueing, computation, result persistence, and page display. Does the queue carry bytes or a reference? Which version does the reference name? Do retries reuse a task identity? How is the result matched to a user? Who deletes temporary files? Tracing the same object through these stages exposes broken responsibility chains.

At each handoff inspect **where the data went** and **what stage the receiver actually promised to complete**. Request acceptance, durable persistence, completed computation, and downstream visibility require different confirmation signals. Locate return statements, transaction commits, queue acknowledgments, or callbacks, and examine how callers interpret them.

## Analyze Storage, Computation, and Communication Together

| Dimension | What to trace | Decision supported |
| --- | --- | --- |
| **Storage** | Sources of truth, indexes and versions, cache invalidation, transaction commits, retention and deletion; replicas and writers of the same object | State ownership, read consistency, and recovery |
| **Computation** | Which thread, process, or device performs work; input snapshots, duplicate computation, batching, locks, and concurrency scope | Execution placement, isolation, and resource budgets |
| **Communication** | Serialization, units, ordering, message identity, buffering, retries, acknowledgments, and cancellation propagation | Handoff contracts, capacity, and failure handling |

Increasing worker concurrency may simply move the queue from the task scheduler to the database connection pool. Follow arrivals, completions, queue age, in-flight work, lock waits, and downstream latency before increasing concurrency, reducing redundant access, rate-limiting, or adjusting batches. Compare under the same load and data conditions, including downstream and recovery behavior.

Caching demands the same compositional analysis: it saves computation or communication but adds replicas and invalidation responsibility. A performance change should explain where it reduces cost, what new state it creates, and how capacity limits and failures are handled.

## Decision Cases: Choose Actions by Discriminating Mechanisms

### Similar Symptoms Can Require Different Repairs

A value reverting after save and refresh may come from writing a different store, reading via an old implementation, background synchronization overwriting the new value, or stale cache versions. Fix the object identity, version, and environment; obtain evidence about the write result, later writes, and selected read path. Investigate the boundary that most clearly distinguishes the explanations before choosing a repair location. Distinguish the error-reporting site, first divergence, and component responsible for restoring the contract.

### The Same Present Outcome Can Conceal Different Future States

A caller timeout may mean a request is still queued, executing, or already committed with its acknowledgment lost. The current symptom is identical, but retries produce different consequences. Trace business identity, the commit point, and result lookup to decide whether a retry should reuse committed results or suppress duplicate effects. Cancellation also distinguishes ending a wait, stopping computation, and handling committed results.

Knowledge compression must preserve this difference. A statement such as *task succeeded* needs to distinguish acceptance, commit, and completion when restarts, retries, and recovery depend on them.

This is also an architecture-memory fidelity criterion. Two explanations may both advise *query status after timeout*, but one assumes the request is queued while the other assumes commit succeeded and acknowledgment was lost. An automatic retry consumer demands different handling in each case. Preserve state definitions, commit points, evidence, and divergent responses to later events. Current architecture documentation owns the live explanation; task records retain historical evidence.

### When Consumers Stop, How Do Producers and Resources Exit?

A consumer that only needs a subset of results may leave producers blocked on sends or still holding resources. Trace how termination signals reach production stages, who waits for work to finish, and who releases connections and buffers. Larger buffers change capacity; a complete termination protocol covers the lifecycle. This example follows [Go pipelines](https://go.dev/blog/pipelines); check the target runtime and APIs before applying it.

### When a Capability Exists, Locate the Missing Connection

A feature works from an administration interface but fails through a new page. Hold input, identity, and environment constant, then compare entry-point selection, parameter conversion, permissions, configuration, and final consumers. Distinguish an integration gap from a missing core capability. Reuse the working path and implement only the real difference.

### Reuse Depends on Contracts; New Logic Needs Ownership

A `save` method may imply transaction behavior, defaults, event emission, and caller identity. Compare the requested contract with actual existing behavior, then choose direct reuse, boundary adaptation, shared stable mechanisms, or separately owned business responsibilities. A new implementation must also define entry selection, data ownership, the fate of existing callers, and coexistence conditions. When repairing a shared mechanism, follow its callers to identify affected behavior.

### Local Optimizations Must Respect Global Resource Constraints

Throughput may rise while tail latency worsens because queues move, lock contention increases, or retries amplify demand. Reconstruct waiting and execution time for the same workload, comparing completed work, resource use, and recovery behavior. Identify where costs moved before changing the bottleneck.

## Smallest Complete Change and Verification

Responsibility and impact determine the change boundary. Identify the guarantee to restore and compare viable edit locations: what conditions and effects each changes, who depends on those effects, and which legitimate business differences must survive. Local adapters suit boundary mismatches; incorrect state transitions shared by multiple entry points belong at the common owner. **Smallest is defined by necessary responsibility; complete is defined by affected dependencies.** Lines, files, and abstraction layers are implementation properties.

Four answers indicate that evidence supports the chosen boundary: why the target path executes; how the deviation or implementation gap arises; how the change restores the guarantee; and how affected callers, data, and lifecycles remain valid. Inspect caller assumptions backward, readers and writers of shared data in both directions, and in-flight tasks, old data, and coexisting versions over time. At each expanded boundary, verify that the original guarantee and additional effects are accounted for; stop or continue accordingly. Prioritize remaining doubts by whether resolving them would change the decision.

The necessary evidence depends on the claim. A local branch can be explained from complete code semantics; configuration-selected behavior requires the relevant configuration; claims about a specific production incident require actual deployed conditions. If competing timing hypotheses or external-service semantics affect the solution, gather observations or targeted verification. Describe temporary mitigations by the effects they control and the conditions in which they remain valid; do not overstate causal certainty.

An evolution plan must explain intermediate states: how old callers, new implementations, historical data, and in-flight work coexist, when state authority transfers, and how a failed cutover resumes. When comparing reuse with a new path, account for adapters, shared state, entry selection, and responsibilities for retiring the old path.

Before choosing verification, semantic tracing should establish what was expected, how the discrepancy arose, and how the change restores the contract. Reuse existing checks that exercise the actual behavior. Add tests only when necessary and target real module handoffs and state transitions: for example, commit followed by a lost acknowledgment and retry, or an old request returning after a newer one. Mocks may isolate external conditions, but the real implementation must own the critical failure boundary.

UI behavior needs observation of the actual page; devices and external services need appropriate runtime evidence. Report the versions, environments, and boundaries actually verified. Deliver when acceptance conditions hold; engineering progress is demonstrated by reliable behavior and explicit delivery state.

## What Diagrams and Memory Should Preserve

**Architecture diagrams are decision interfaces for humans.** From a diagram and the adjacent explanation, a reader should understand how the system runs, what evidence supports the view, and what a change affects, with a path back to code and runtime facts. System diagrams preserve runtime units, dependencies, major storage, and communication. Module diagrams preserve responsibilities, interfaces, and state ownership. Sequence and state diagrams preserve important handoffs, concurrency, and recovery. Significant nodes link to symbols, configurations, or runtime objects; edges carry conditions and distinguish calls, data, control, guarantees, and dependencies. Detailed drawing, evidence, and coverage rules live in the knowledge-maintenance reference.

Persist only knowledge that can alter later search directions, reuse decisions, repair boundaries, or verification methods. For important decisions, save the conditions under which they hold, their evidence, and changes that would require revisiting them. Adding a second writer, for instance, changes a safety judgment that assumed a single writer even if the original function stays unchanged. Leave incidental searches in the current task, keep authoritative explanations in their designated documents, and retain history through Git and task records.
