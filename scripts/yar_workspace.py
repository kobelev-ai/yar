#!/usr/bin/env python3
"""Local Yar workspace operations. Python 3.10+, standard library only."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
from datetime import datetime
from uuid import uuid4

VERSION = "3.0"
DISTRIBUTION = Path(__file__).resolve().parent.parent
QUEUES = {
    "closures": "ops/tasks/review/closures.md",
    "insights": "ops/tasks/review/insights.md",
}


def workspace_root(explicit: str | None = None) -> Path:
    if explicit or os.environ.get("YAR_ROOT"):
        return Path(explicit or os.environ["YAR_ROOT"]).expanduser().resolve()
    for path in (Path.cwd(), *Path.cwd().parents):
        if (path / ".yar-root").is_file():
            return path.resolve()
    return DISTRIBUTION


def local_path(root: Path, relative: str) -> Path:
    name = Path(relative)
    if name.is_absolute() or ".." in name.parts:
        raise ValueError(f"Expected a path within the workspace: {relative}")
    path = root / name
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"Path leaves the workspace: {relative}")
    for parent in (path, *path.parents):
        if parent == root:
            break
        if parent.is_symlink():
            raise ValueError(f"Symlink path needs manual review: {relative}")
    return path


def create_once(root: Path, relative: str, content: str) -> bool:
    path = local_path(root, relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8") as output:
            output.write(content)
    except FileExistsError:
        if not path.is_file():
            raise ValueError(f"Expected a regular file: {relative}")
        return False
    return True


def render_template(name: str, values: dict[str, str]) -> str:
    text = (DISTRIBUTION / "templates" / name).read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def initialize(root: Path, name: str = "", language: str = "") -> list[str]:
    root.mkdir(parents=True, exist_ok=True)
    old = ["tasks/todo.md", "context/meetings/index.json"]
    if any((root / p).exists() for p in old):
        raise ValueError("Legacy operational files found. Preview migrate before init.")
    queues_path = local_path(root, "ops/tasks/review/queues.json")
    queues = json.loads(queues_path.read_text()) if queues_path.exists() else QUEUES
    if not isinstance(queues, dict) or any(not isinstance(queues.get(k), str) for k in QUEUES):
        raise ValueError("Review queues must declare local closures and insights paths.")
    values = {
        "OWNER_NAME": name or "(add when useful)",
        "OWNER_ROLE": "(add when useful)",
        "OWNER_COMPANY": "(add when useful)",
        "FOCUS_AREAS_LIST": "- Start with one real task",
        "KEY_PEOPLE_LIST": "- (add when useful)",
    }
    contents = {
        ".yar-root": "Yar workspace marker.\n",
        "ops/tasks/todo.md": (DISTRIBUTION / "templates/todo.md.template").read_text(),
        "ops/tasks/review/queues.json": json.dumps(QUEUES, indent=2) + "\n",
        queues["closures"]: "# Possible closures\n\nCandidates only; explicit owner confirmation is required.\n",
        queues["insights"]: "# Memory and decision candidates\n\nCandidates only; explicit owner confirmation is required.\n",
        "ops/meetings/index.json": "[]\n",
        "ops/meetings/speaker_mappings.json": "{}\n",
        "context/me.md": render_template("me.md.template", values),
        "context/me/preferences.md": "# Preferences\n\nLanguage: " + (language or "match the owner's conversation") + "\nBriefing: on request\n",
        "context/me/decisions.md": "# Confirmed decisions\n\nAppend-only. Record explicit confirmations and their sources.\n",
        "context/me/ideas.md": "# Ideas\n\nProposals and ideas; not commitments.\n",
        "context/me/speaker_signals.md": "# Speaker identification signals\n\nUse confirmed signals; keep uncertainty explicit.\n",
        "context/me/boundaries.md": "# Owner-defined processing boundaries\n\nNo rules recorded yet.\n",
        ".yar/installed.md": (DISTRIBUTION / "templates/installed.md.template").read_text(),
        ".yar/workspace.json": json.dumps({"version": VERSION, "created": datetime.now().astimezone().isoformat()}, indent=2) + "\n",
    }
    # Preflight all destinations before creating any files.
    for relative in contents:
        path = local_path(root, relative)
        if path.exists() and not path.is_file():
            raise ValueError(f"Expected a regular file: {relative}")
        for parent in path.parents:
            if parent == root:
                break
            if parent.exists() and not parent.is_dir():
                raise ValueError(f"Destination directory blocked: {relative}")
    created = [path for path, text in contents.items() if create_once(root, path, text)]
    for relative in ["inbox/processed", "tasks", "ops/meetings/processed", "ops/meetings/docs", "ops/tasks/archive"]:
        local_path(root, relative).mkdir(parents=True, exist_ok=True)
    return created


def create_task(root: Path, name: str, goal: str = "") -> Path:
    relative = Path(name)
    if not name.strip() or relative.is_absolute() or any(part in {".", ".."} for part in name.split("/")):
        raise ValueError("Give a nonempty task name without absolute or parent paths.")
    folder = local_path(root, str(Path("tasks") / relative))
    if folder.exists() and not folder.is_dir():
        raise ValueError("The task name is already a file.")
    folder.mkdir(parents=True, exist_ok=True)
    create_once(root, str(folder.relative_to(root) / "README.md"), render_template("task.md.template", {
        "TASK_NAME": relative.name,
        "GOAL": goal or "Use the owner's requested result; ask if it is unknown.",
        "TODAY": datetime.now().astimezone().isoformat(timespec="minutes"),
    }))
    return folder


def create_demo(root: Path) -> Path:
    folder = local_path(root, "demos/" + datetime.now().strftime("%y-%m-%d_%H%M%S_") + uuid4().hex[:8])
    folder.mkdir(parents=True, exist_ok=False)
    # Distribution code and workflows are copied, never real working data.
    for filename in ["AGENTS.md", "CLAUDE.md", "README.md", ".gitignore"]:
        shutil.copy2(DISTRIBUTION / filename, folder / filename)
    for dirname in ["templates", ".claude"]:
        shutil.copytree(DISTRIBUTION / dirname, folder / dirname,
                        ignore=shutil.ignore_patterns(".env*", "*.log", "__pycache__", "settings.local.json"))
    (folder / "scripts").mkdir()
    shutil.copy2(DISTRIBUTION / "scripts/yar_workspace.py", folder / "scripts/yar_workspace.py")
    initialize(folder, "Fictional demo owner", "English")
    task = create_task(folder, "Compare_proposals", "Compare total first-year cost, coverage and delivery; recommend with source references.")
    for source in (DISTRIBUTION / "templates/demo/offers").iterdir():
        if source.is_file():
            shutil.copy2(source, task / source.name)
    return folder


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest() if hasattr(hashlib, "file_digest") else hashlib.sha256(stream.read()).hexdigest()


def migration_plan(root: Path) -> list[tuple[str, str]]:
    plan = []
    if (root / "tasks/todo.md").exists():
        plan.append(("tasks/todo.md", "ops/tasks/todo.md"))
    for old, new in [("tasks/archive", "ops/tasks/archive"), ("context/meetings", "ops/meetings")]:
        source = local_path(root, old)
        if source.is_symlink():
            raise ValueError(f"Symlink legacy folder needs manual review: {old}")
        if source.exists():
            for item in sorted(source.rglob("*")):
                local_path(root, str(item.relative_to(root)))
                if item.is_file() and item.name != ".gitkeep":
                    plan.append((str(item.relative_to(root)), str(Path(new) / item.relative_to(source))))
    for old, new in plan:
        source, dest = local_path(root, old), local_path(root, new)
        if not source.is_file():
            raise ValueError(f"Expected a regular source: {old}")
        if dest.exists():
            raise ValueError(f"Migration conflict: {old} and {new} both exist. Neither was changed.")
        for parent in dest.parents:
            if parent == root:
                break
            if parent.exists() and not parent.is_dir():
                raise ValueError(f"Migration destination blocked: {new}")
    return plan


def rewrite_meeting_paths(value, root: Path):
    if isinstance(value, dict):
        return {k: rewrite_meeting_paths(v, root) for k, v in value.items()}
    if isinstance(value, list):
        return [rewrite_meeting_paths(v, root) for v in value]
    if isinstance(value, str):
        for old, new in [("context/meetings/", "ops/meetings/"),
                         (str(root / "context/meetings") + "/", str(root / "ops/meetings") + "/")]:
            if value.startswith(old):
                return new + value[len(old):]
    return value


def migrate(root: Path, apply: bool = False) -> dict:
    plan = migration_plan(root)
    # Validate metadata before any move.
    metadata = {}
    for old, new in plan:
        if new in {"ops/meetings/index.json", "ops/meetings/speaker_mappings.json"}:
            original = json.loads((root / old).read_text(encoding="utf-8"))
            updated = rewrite_meeting_paths(original, root)
            if updated != original:
                metadata[new] = json.dumps(updated, ensure_ascii=False, indent=2) + "\n"
    result = {"moves": [{"from": a, "to": b} for a, b in plan], "applied": False}
    if not apply:
        return result
    if not plan:
        result["created"] = initialize(root)
        result["applied"] = True
        return result
    backup = local_path(root, ".yar/backups/" + datetime.now().strftime("%y-%m-%d_%H%M%S_") + uuid4().hex[:8] + "_v3")
    manifest = []
    for old, new in plan:
        saved = backup / "originals" / old
        saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / old, saved)
        checksum = digest(root / old)
        if digest(saved) != checksum:
            raise OSError(f"Backup verification failed: {old}")
        manifest.append({"from": old, "to": new, "sha256": checksum})
    (backup / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    moved, owned_destinations = [], []
    try:
        for record in manifest:
            source, dest = root / record["from"], root / record["to"]
            dest.parent.mkdir(parents=True, exist_ok=True)
            # Exclusive creation prevents an existing destination being overwritten.
            with dest.open("xb") as output:
                owned_destinations.append(dest)
                with source.open("rb") as input_file:
                    shutil.copyfileobj(input_file, output)
            if digest(dest) != record["sha256"]:
                raise OSError(f"Move verification failed: {record['from']}")
            source.unlink()
            moved.append(record)
        for relative, content in metadata.items():
            (root / relative).write_text(content, encoding="utf-8")
        result["created"] = initialize(root)
    except Exception:
        for record in reversed(moved):
            source = root / record["from"]
            if not source.exists():
                source.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(backup / "originals" / record["from"], source)
        for dest in owned_destinations:
            dest.unlink(missing_ok=True)
        raise
    result.update({"applied": True, "backup": str(backup)})
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", help="explicit workspace; overrides YAR_ROOT")
    commands = parser.add_subparsers(dest="command", required=True)
    setup = commands.add_parser("init", help="create missing files, preserving existing contents")
    setup.add_argument("--name", default="")
    setup.add_argument("--language", default="")
    task = commands.add_parser("task", help="create a task folder and missing README")
    task.add_argument("name")
    task.add_argument("--goal", default="")
    commands.add_parser("demo", help="create a separate synthetic workspace")
    upgrade = commands.add_parser("migrate", help="preview legacy moves; --apply makes a verified backup and migrates")
    upgrade.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    root = workspace_root(args.root)
    try:
        if args.command == "init":
            result = {"root": str(root), "created": initialize(root, args.name, args.language)}
        elif args.command == "task":
            result = {"task": str(create_task(root, args.name, args.goal))}
        elif args.command == "demo":
            result = {"demo": str(create_demo(root)), "synthetic": True}
        else:
            result = migrate(root, args.apply)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (OSError, ValueError) as error:
        print(f"Yar: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
