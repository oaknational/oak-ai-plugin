"""Prove each published plugin is a faithful copy of its recorded source.

PROVENANCE.json records, for every plugin copy this repository publishes,
the source repository, the commit the copy was taken from, the paths left
out of the copy and any known, explained divergences. This script clones
each source at its recorded commit (sparse and blobless, so it is quick)
and diffs it against the copy. Any differing, missing or extra file that
is not excluded or recorded as a known divergence fails the check, as does
a plugin manifest whose version differs from the recorded one.

Run by CI (the "Sync fidelity" job); needs network access. Run it locally
the same way: python3 scripts/check_provenance.py
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(args: list[str], cwd: Path) -> str:
    return subprocess.run(
        args, cwd=cwd, check=True, capture_output=True, text=True
    ).stdout


def clone_source(publish: dict, workdir: Path) -> Path:
    """Sparse-clone the source repository at the recorded commit and return
    the path of the source plugin directory."""
    repo = workdir / "source"
    run(
        [
            "git",
            "clone",
            "--filter=blob:none",
            "--no-checkout",
            publish["source_repo"],
            str(repo),
        ],
        cwd=workdir,
    )
    run(["git", "sparse-checkout", "set", publish["source_path"]], cwd=repo)
    run(["git", "checkout", "--quiet", publish["commit"]], cwd=repo)
    return repo / publish["source_path"]


def differing_files(source: Path, copy: Path, excluded: list[str]) -> list[str]:
    """Files that differ between the source tree and the copy, as paths
    relative to the copy. Excluded paths are pruned from the source first,
    so a file is reported when it differs, is missing from the copy, or
    exists only in the copy."""
    for pattern in excluded:
        target = source / pattern.rstrip("/")
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()
    proc = subprocess.run(
        ["git", "diff", "--no-index", "--name-only", str(source), str(copy)],
        capture_output=True,
        text=True,
    )
    if proc.returncode not in (0, 1):
        raise RuntimeError(f"git diff failed: {proc.stderr}")
    names = set()
    for line in proc.stdout.splitlines():
        for base in (str(source), str(copy)):
            if line.startswith(base + "/"):
                names.add(line[len(base) + 1 :])
    return sorted(names)


def check_publish(publish: dict) -> list[str]:
    problems = []
    copy = ROOT / publish["path"]
    if not copy.is_dir():
        return [f"{publish['path']}: recorded in PROVENANCE.json but not in the repository"]
    if not re.fullmatch(r"[0-9a-f]{40}", publish["commit"]):
        problems.append(f"{publish['path']}: commit must be a full 40-character SHA")
        return problems

    manifest = json.loads((copy / ".claude-plugin" / "plugin.json").read_text())
    if manifest["version"] != publish["plugin_version"]:
        problems.append(
            f"{publish['path']}: plugin.json says {manifest['version']}, "
            f"PROVENANCE.json says {publish['plugin_version']}"
        )

    with tempfile.TemporaryDirectory() as tmp:
        source = clone_source(publish, Path(tmp))
        differing = differing_files(source, copy, publish["excluded"])

    allowed = {d["file"] for d in publish.get("known_divergences", [])}
    for name in differing:
        if name not in allowed:
            problems.append(
                f"{publish['path']}/{name}: differs from "
                f"{publish['source_path']} at {publish['commit'][:9]} and is not "
                "a recorded divergence — re-run the sync, or record why it differs"
            )
    for name in sorted(allowed - set(differing)):
        print(
            f"note: {publish['path']}/{name} no longer differs from the source; "
            "its known_divergences entry can be removed"
        )
    return problems


def main() -> int:
    provenance = json.loads((ROOT / "PROVENANCE.json").read_text())
    problems = []
    for publish in provenance["publishes"]:
        problems.extend(check_publish(publish))
    prefix = "::error::" if subprocess.os.environ.get("GITHUB_ACTIONS") else "error: "
    for problem in problems:
        print(f"{prefix}{problem}")
    if not problems:
        print(f"Sync fidelity: {len(provenance['publishes'])} publish(es) match their recorded sources.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
