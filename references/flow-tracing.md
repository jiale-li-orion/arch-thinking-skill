# Trace a business flow from evidence

Use this playbook when behavior crosses modules, an asynchronous boundary, a state machine, storage, or an external service.

## 1. Start from the observable behavior

Write one sentence describing the trigger and expected outcome. Search user-visible text, API route, event name, log message, or known symbol first. Use rg -n for content and rg --files to locate candidates. Read small ranges around matches; do not dump whole directories into context.

## 2. Follow control flow and data flow

For each meaningful boundary, record only details that affect behavior:

- Entry: who calls it, under which state or event.
- Input/output: what object or payload enters and leaves; which fields change or disappear.
- State: who owns the authoritative value, who may write it, and when it resets.
- Effects: database transaction, queue, filesystem, network, SDK, device, or media operation.
- Timing: synchronous call, callback, event stream, task, retry, timeout, cancellation, or background lifecycle.
- Completion: what proves the consumer completed the work, rather than merely accepting a request.

Search writes as carefully as reads. A field declaration does not establish state ownership or lifecycle. Find assignments, mutations, resets, persistence writes, and recovery paths relevant to the task.

## 3. Keep a compact trace

Use one row per meaningful boundary, not one row per method.

| Boundary | Input → output | State owner / side effect | Evidence |
|---|---|---|---|
| Trigger / entry | Event → request | Caller or session | path + symbol |
| Decision | Request → branch / command | Decision state | path + symbol |
| Execution | Command → external effect | SDK / service | path + symbol |
| Persistence | Result → durable record | Repository / database / object store | path + symbol |
| Completion / recovery | Ack, failure, retry or restore | State owner | path + symbol |

Add nodes only when they explain a transformation, ownership boundary, asynchronous handoff, or failure mode.

## 4. Explain failures as competing mechanisms

For each plausible explanation, identify the observation it explains, evidence supporting it, evidence that would distinguish it from alternatives, and the cheapest safe probe.

Prefer read-only inspection and narrow instrumentation before changing code. For nondeterministic failures, preserve timing, state transitions, request IDs and relevant input/output at each boundary. Do not infer causality from adjacent log lines alone.

## 5. Verify the real contract

Read the caller and consumer as well as the implementation. Inspect configuration and SDK semantics when code delegates behavior externally. Tests are evidence for paths they execute; a passing suite does not prove an untested production path.

After a change, validate the edited path, the handoff contract, and the most relevant failure/recovery behavior. If full integration cannot run, name the unverified boundary explicitly.

## 6. Promote only reusable discoveries

Create or update a flow note when the flow is likely to be revisited, has non-obvious state ownership, crosses multiple modules, or explains a recurring incident. A one-off local fix with no durable architectural implication usually needs no new memory file.
