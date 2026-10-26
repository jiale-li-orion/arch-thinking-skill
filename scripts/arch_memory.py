#!/usr/bin/env python3
"""Initialize, query, and validate a small evidence-linked architecture memory."""
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

EVIDENCE_RE = re.compile(
    r"Evidence:\s*path=([^\s;]+)"
    r"(?:\s+symbol=([^\s;]+))?"
    r"(?:\s+at=([0-9a-fA-F]{7,40}))?"
)

TEMPLATES = {
    "README.md": """# Architecture memory

This directory stores the smallest reusable model of how this system behaves.

## Read by task
- Start with AGENTS.md for the maintenance protocol and re-read triggers.
- Read ARCHITECTURE.md for the global system model.
- Read STATE.md for the current understanding and unresolved questions.
- Read flows/ only for a task that touches that lifecycle.

## Ownership
AGENTS.md owns the maintenance rules; ARCHITECTURE.md owns global structure; STATE.md owns current understanding; each flow note owns its local lifecycle. Keep one authoritative home for each claim.

## Evidence
Important implementation claims should cite repository-relative source paths and exact symbols using the Evidence convention described in AGENTS.md.
""",
    "AGENTS.md": """# Architecture memory maintenance rules

These rules govern this knowledge directory. Keep the mechanism stable and update the system model as evidence changes.

## Source of truth
Current source, configuration, runtime evidence and user-approved design contracts are primary evidence. Notes are navigation and accumulated reasoning; verify relevant claims before changing code. When approved design and actual implementation disagree, record the gap rather than silently redefining either one.

## Read-back
- At entry, read README.md and the relevant repository instructions.
- For architecture-affecting work, read ARCHITECTURE.md and STATE.md.
- Before changing a documented flow, read that flow note and inspect current source.
- When source changes, run the impact command to identify notes that cite changed files; re-read those notes before assuming their claims remain true.
- A source change triggers review, not automatic invalidation. Confirm semantic impact.

## Update ownership
- Global boundary, dependency, invariant, or state ownership changed: update ARCHITECTURE.md.
- Current explanation, competing mechanism, next probe, or investigation focus changed: update STATE.md.
- One cross-module lifecycle changed: update its flow note.
- Routine progress and command logs belong in the task / PR record, not new memory files.
- Update the authoritative owner first, then dependent notes only where their conclusions or navigation changed.

## Evidence convention
Put important claims next to an evidence line. Its fields are `path=src/path/File.java`, `symbol=methodName`, and optional `at=abc1234`.

The path is relative to the source repository, not this knowledge directory. The symbol is an exact identifier or distinctive source string. The optional commit is the revision at which the evidence was checked. Run arch_memory.py check after meaningful updates. Missing evidence is an error; changed evidence is a re-read warning, not automatic proof that the explanation is false.

## Pruning
Remove or merge notes that no longer change search, explanation, implementation, or verification. Prefer Git history for chronology. Keep snapshots only when they preserve otherwise-lost provenance or explain a meaningful regression. Do not add indexes, diaries, decision logs, or diagrams by default.
""",
    "ARCHITECTURE.md": """# Architecture map

Purpose: preserve stable system boundaries and dependency relationships that help a future agent navigate the codebase.

## System boundary
Describe the system responsibility and external dependencies. Cite evidence for non-obvious claims.

## Modules and dependency direction
| Module | Responsibility | Entry points / contracts | Depends on |
|---|---|---|---|

## Durable state and side-effect boundaries
Record only state owners, persistence boundaries, and external effects that influence multiple flows.

## Invariants and cross-cutting constraints
Record only rules that materially constrain changes across modules.

## High-value flows
Link to flows/ notes only when they explain recurring or cross-module behavior.
""",
    "STATE.md": """# Current architecture understanding

Replace this note as understanding changes; do not append a session diary.

## Current model
State the smallest evidence-backed explanation relevant to ongoing work.

## Unresolved questions
List only questions whose answers could change a diagnosis, design, or next search. Separate observations from inferences.

## Next useful probe
Name the cheapest probe that best distinguishes the remaining explanations.
""",
}


def git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def note_root(source_root: Path, memory_root: Path | None) -> Path:
    """Use an external memory repository when supplied; otherwise retain .arch compatibility."""
    return memory_root.resolve() if memory_root is not None else source_root / ".arch"


def init_memory(source_root: Path, memory_root: Path | None = None) -> list[Path]:
    target = note_root(source_root, memory_root)
    target.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    for name, content in TEMPLATES.items():
        path = target / name
        if not path.exists():
            path.write_text(content, encoding="utf-8")
            created.append(path)
    return created


def iter_evidence(memory_root: Path):
    if not memory_root.is_dir():
        return
    for note in sorted(memory_root.rglob("*.md")):
        try:
            lines = note.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for number, line in enumerate(lines, 1):
            match = EVIDENCE_RE.search(line)
            if match:
                yield note, number, match.groups()


def check_memory(source_root: Path, memory_root: Path | None = None) -> tuple[list[str], list[str], int]:
    notes_root = note_root(source_root, memory_root)
    if not notes_root.is_dir():
        return [f"memory directory does not exist: {notes_root}"], [], 0

    errors: list[str] = []
    warnings: list[str] = []
    checked = 0
    is_git = git(source_root, "rev-parse", "--show-toplevel").returncode == 0

    for note, number, (rel_path, symbol, commit) in iter_evidence(notes_root):
        checked += 1
        source = (source_root / rel_path).resolve()
        try:
            source.relative_to(source_root.resolve())
        except ValueError:
            errors.append(f"{note.relative_to(notes_root)}:{number}: evidence path escapes source repository")
            continue
        if not source.is_file():
            errors.append(f"{note.relative_to(notes_root)}:{number}: missing evidence path {rel_path}")
            continue

        content = source.read_text(encoding="utf-8", errors="replace")
        if symbol and symbol not in content:
            errors.append(
                f"{note.relative_to(notes_root)}:{number}: symbol {symbol!r} not found in {rel_path}"
            )

        if is_git:
            dirty = git(source_root, "status", "--porcelain", "--", rel_path)
            if dirty.stdout.strip():
                warnings.append(
                    f"{note.relative_to(notes_root)}:{number}: {rel_path} has uncommitted changes; recheck evidence"
                )
            if commit:
                exists = git(source_root, "cat-file", "-e", f"{commit}^{{commit}}")
                if exists.returncode:
                    warnings.append(
                        f"{note.relative_to(notes_root)}:{number}: evidence commit {commit} is unavailable"
                    )
                else:
                    changed = git(source_root, "diff", "--quiet", commit, "HEAD", "--", rel_path)
                    if changed.returncode == 1:
                        warnings.append(
                            f"{note.relative_to(notes_root)}:{number}: {rel_path} changed after {commit}; recheck claim"
                        )
                    elif changed.returncode not in (0, 1):
                        warnings.append(
                            f"{note.relative_to(notes_root)}:{number}: unable to compare {rel_path} with {commit}"
                        )

    return errors, warnings, checked


def impact_memory(
    source_root: Path, files: list[str], memory_root: Path | None = None
) -> tuple[list[tuple[Path, list[str]]], list[str]]:
    notes_root = note_root(source_root, memory_root)
    if not notes_root.is_dir():
        return [], [f"memory directory does not exist: {notes_root}"]
    changed: set[str] = set()
    errors: list[str] = []
    for raw in files:
        path = Path(raw)
        if path.is_absolute():
            try:
                path = path.resolve().relative_to(source_root.resolve())
            except ValueError:
                errors.append(f"ignored path outside source repository: {raw}")
                continue
        normalized = path.as_posix()
        if normalized == ".." or normalized.startswith("../"):
            errors.append(f"ignored path outside source repository: {raw}")
            continue
        changed.add(normalized)

    hits: dict[Path, set[str]] = {}
    for note, _number, (rel_path, _symbol, _commit) in iter_evidence(notes_root):
        if rel_path in changed:
            hits.setdefault(note, set()).add(rel_path)

    return [(note, sorted(paths)) for note, paths in sorted(hits.items())], errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("init", "check", "impact"))
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="source repository root")
    parser.add_argument(
        "--memory-root",
        type=Path,
        default=None,
        help="separate knowledge directory or small Git repository; defaults to <root>/.arch",
    )
    parser.add_argument("--files", nargs="*", default=[])
    args = parser.parse_args()
    source_root = args.root.resolve()
    memory_root = args.memory_root.resolve() if args.memory_root is not None else None

    if not source_root.is_dir():
        print(f"ERROR: source root is not a directory: {source_root}")
        return 2

    if args.command == "init":
        created = init_memory(source_root, memory_root)
        if created:
            for path in created:
                print(f"CREATED {path}")
        else:
            print("UNCHANGED: all four core memory files already exist")
        return 0

    if args.command == "impact":
        if not args.files:
            print("ERROR: impact requires --files path/to/source [more paths...]")
            return 2
        results, errors = impact_memory(source_root, args.files, memory_root)
        for item in errors:
            print(f"WARNING: {item}")
        if not results:
            print("No architecture notes cite the supplied source paths.")
        for note, paths in results:
            print(f"RE-READ {note}")
            for path in paths:
                print(f"  <- {path}")
        print(f"{len(results)} note(s) affected.")
        return 0

    errors, warnings, checked = check_memory(source_root, memory_root)
    for item in errors:
        print(f"ERROR: {item}")
    for item in warnings:
        print(f"STALE: {item}")
    print(f"Checked {checked} evidence reference(s); {len(errors)} error(s), {len(warnings)} stale warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
