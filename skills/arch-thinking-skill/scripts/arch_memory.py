#!/usr/bin/env python3
"""Initialize, query, and validate a small evidence-linked architecture memory."""
from __future__ import annotations

import argparse
import os
import re
import subprocess
from pathlib import Path

EVIDENCE_RE = re.compile(
    r"Evidence:\s*path=([^\s;]+)"
    r"(?:\s+symbol=([^\s;]+))?"
    r"(?:\s+at=([0-9a-fA-F]{7,40}))?"
)

TEMPLATE_ROOT = Path(__file__).resolve().parents[1] / "assets" / "workspace"
METHOD_FILENAME = "engineering-thinking.md"
LEGACY_METHOD_FILENAME = "工程思维.md"
TEMPLATES = {
    name: (TEMPLATE_ROOT / name).read_text(encoding="utf-8")
    for name in ("README.md", "AGENTS.md", METHOD_FILENAME, "ARCHITECTURE.md", "STATE.md")
}


def git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def note_root(source_root: Path, memory_root: Path | None) -> Path:
    """Use the chosen workspace documents, retaining existing .arch installations."""
    if memory_root is not None:
        return memory_root.resolve()
    legacy = source_root / ".arch"
    if legacy.is_dir() and not (source_root / "ARCHITECTURE.md").exists():
        return legacy
    return source_root


def init_memory(source_root: Path, memory_root: Path | None = None) -> list[Path]:
    target = note_root(source_root, memory_root)
    target.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    # An existing Chinese method is the authority for that workspace. Do not
    # introduce a second copy with conflicting rules during initialization.
    use_legacy_method = (target / LEGACY_METHOD_FILENAME).is_file() and not (target / METHOD_FILENAME).exists()
    for name, content in TEMPLATES.items():
        if name == METHOD_FILENAME and use_legacy_method:
            continue
        if name in ("README.md", "AGENTS.md") and use_legacy_method:
            content = content.replace(METHOD_FILENAME, LEGACY_METHOD_FILENAME)
        path = target / name
        try:
            with path.open("x", encoding="utf-8") as stream:
                stream.write(content)
        except FileExistsError:
            continue
        created.append(path)
    return created


def iter_evidence(memory_root: Path, *, source_root: Path):
    if not memory_root.is_dir():
        return
    if memory_root.resolve() == source_root.resolve():
        # A large source repository can contain unrelated Markdown trees. The
        # default workspace owns root-level notes and optional flows/ only.
        notes = list(memory_root.glob("*.md"))
        flows = memory_root / "flows"
        if flows.is_dir():
            notes.extend(flows.rglob("*.md"))
    else:
        notes = []
        for directory, children, files in os.walk(memory_root):
            children[:] = sorted(
                name for name in children
                if name not in {".git", "node_modules", ".venv", "__pycache__"}
            )
            notes.extend(Path(directory) / name for name in files if name.endswith(".md"))
    for note in sorted(notes):
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

    for note, number, (rel_path, symbol, commit) in iter_evidence(notes_root, source_root=source_root):
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
    for note, _number, (rel_path, _symbol, _commit) in iter_evidence(notes_root, source_root=source_root):
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
        help="existing knowledge location; defaults to source root, or existing .arch for legacy workspaces",
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
            print("UNCHANGED: all workspace template paths already exist")
        print("STRUCTURE READY: follow references/initialization.md to restore real system knowledge and task continuity.")
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
