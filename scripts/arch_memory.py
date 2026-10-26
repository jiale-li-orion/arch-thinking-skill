#!/usr/bin/env python3
"""Initialize and validate a small, evidence-linked .arch memory directory."""
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

ARCHITECTURE_TEMPLATE = """# Architecture map

Purpose: preserve stable system boundaries and dependency relationships that help a future agent navigate the codebase.

## System boundary
Describe the system responsibility and external dependencies. Cite evidence for non-obvious claims.

## Modules and dependency direction
| Module | Responsibility | Entry points / contracts | Depends on |
|---|---|---|---|

## Durable state and side-effect boundaries
Record only state owners, persistence boundaries, and external effects that influence multiple flows.

## High-value flows
Link to .arch/flows/ notes only when they explain recurring or cross-module behavior.

## Evidence convention
Example format: path=relative/path/File.java symbol=methodName at=abc1234
"""

STATE_TEMPLATE = """# Current architecture understanding

Replace this note as understanding changes; do not append a session diary.

## Current model
State the smallest evidence-backed explanation relevant to ongoing work.

## Unresolved questions
List only questions whose answers could change a diagnosis, design, or next search. Separate observations from inferences.

## Next useful probe
Name the cheapest probe that best distinguishes the remaining explanations.
"""


def git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def init_memory(root: Path) -> list[Path]:
    arch = root / ".arch"
    arch.mkdir(parents=True, exist_ok=True)
    created = []
    for name, content in (
        ("ARCHITECTURE.md", ARCHITECTURE_TEMPLATE),
        ("STATE.md", STATE_TEMPLATE),
    ):
        path = arch / name
        if not path.exists():
            path.write_text(content, encoding="utf-8")
            created.append(path)
    return created


def check_memory(root: Path) -> tuple[list[str], list[str], int]:
    arch = root / ".arch"
    if not arch.is_dir():
        return [".arch/ does not exist; run init first"], [], 0

    errors: list[str] = []
    warnings: list[str] = []
    checked = 0
    is_git = git(root, "rev-parse", "--show-toplevel").returncode == 0

    for note in sorted(arch.rglob("*.md")):
        try:
            lines = note.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            errors.append(f"{note.relative_to(root)}: not UTF-8 text")
            continue

        for number, line in enumerate(lines, 1):
            match = EVIDENCE_RE.search(line)
            if not match:
                continue
            checked += 1
            rel_path, symbol, commit = match.groups()
            source = (root / rel_path).resolve()
            try:
                source.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{note.relative_to(root)}:{number}: evidence path escapes repository")
                continue
            if not source.is_file():
                errors.append(f"{note.relative_to(root)}:{number}: missing evidence path {rel_path}")
                continue

            content = source.read_text(encoding="utf-8", errors="replace")
            if symbol and symbol not in content:
                errors.append(
                    f"{note.relative_to(root)}:{number}: symbol {symbol!r} not found in {rel_path}"
                )

            if is_git:
                dirty = git(root, "status", "--porcelain", "--", rel_path)
                if dirty.stdout.strip():
                    warnings.append(
                        f"{note.relative_to(root)}:{number}: {rel_path} has uncommitted changes; recheck evidence"
                    )
                if commit:
                    exists = git(root, "cat-file", "-e", f"{commit}^{{commit}}")
                    if exists.returncode:
                        warnings.append(
                            f"{note.relative_to(root)}:{number}: evidence commit {commit} is unavailable"
                        )
                    else:
                        changed = git(root, "diff", "--quiet", commit, "HEAD", "--", rel_path)
                        if changed.returncode == 1:
                            warnings.append(
                                f"{note.relative_to(root)}:{number}: {rel_path} changed after {commit}; recheck claim"
                            )
                        elif changed.returncode not in (0, 1):
                            warnings.append(
                                f"{note.relative_to(root)}:{number}: unable to compare {rel_path} with {commit}"
                            )

    return errors, warnings, checked


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("init", "check"))
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()

    if not root.is_dir():
        print(f"ERROR: root is not a directory: {root}")
        return 2

    if args.command == "init":
        created = init_memory(root)
        if created:
            for path in created:
                print(f"CREATED {path.relative_to(root)}")
        else:
            print("UNCHANGED: both core memory files already exist")
        return 0

    errors, warnings, checked = check_memory(root)
    for item in errors:
        print(f"ERROR: {item}")
    for item in warnings:
        print(f"STALE: {item}")
    print(f"Checked {checked} evidence reference(s); {len(errors)} error(s), {len(warnings)} stale warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
