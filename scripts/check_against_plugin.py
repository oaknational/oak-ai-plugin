"""Check the README, CHANGELOG and marketplace entry against the Claude plugin.

The README restates facts the plugin holds: the skills that ship, the
workflows' commands and the MCP config. The CHANGELOG's latest entry must be
the version the plugin carries. The marketplace entry repeats the plugin's
display name, description and keywords. Each is recomputed from the plugin,
so none of them can drift from it. Run by CI and by the pre-commit hook.
"""

import json
import os
import re
import sys

PLUGIN = "claude/plugins/oak-national-academy"


def read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def check_readme() -> list:
    """The README's skills table, commands table and MCP snippet, each
    recomputed from what the plugin ships."""
    readme = read("README.md")
    skills = set(os.listdir(f"{PLUGIN}/skills"))
    workflows = set(os.listdir(f"{PLUGIN}/workflows"))
    table = readme.split("## The skills", 1)[1].split("###", 1)[0]
    listed = set(re.findall(r"^\|\s*`([^`]+)`\s*\|", table, re.M))
    commands = set(re.findall(r"^\|\s*`/([a-z-]+)", readme, re.M))
    snippet = json.loads(re.search(r"```json\n(.*?)```", readme, re.S).group(1))
    mcp = json.loads(read(f"{PLUGIN}/.mcp.json"))

    problems = []
    if listed != skills | workflows:
        problems.append(
            f"README: skills table lists {sorted(listed)}, plugin ships {sorted(skills | workflows)}"
        )
    if commands != workflows:
        problems.append(
            f"README: commands table lists {sorted(commands)}, plugin ships {sorted(workflows)}"
        )
    if snippet != mcp:
        problems.append("README: MCP config snippet differs from the plugin's .mcp.json")
    return problems


def check_changelog(version: str) -> list:
    """The CHANGELOG's latest entry must be the plugin's version."""
    latest = re.search(r"^## (\S+)", read("CHANGELOG.md"), re.M)
    if latest and latest.group(1) == version:
        return []
    found = latest.group(1) if latest else "none"
    return [f"CHANGELOG: latest entry is {found}, plugin.json says {version}"]


def check_marketplace(manifest: dict) -> list:
    """The marketplace entry must repeat the plugin manifest's fields."""
    marketplace = json.loads(read(".claude-plugin/marketplace.json"))
    entries = [e for e in marketplace["plugins"] if e["source"] == f"./{PLUGIN}"]
    if len(entries) != 1:
        return [f"marketplace: expected one entry with source ./{PLUGIN}, found {len(entries)}"]
    return [
        f"marketplace: {field} differs from the plugin's plugin.json"
        for field in ("name", "displayName", "description", "keywords")
        if entries[0].get(field) != manifest.get(field)
    ]


def main() -> int:
    manifest = json.loads(read(f"{PLUGIN}/.claude-plugin/plugin.json"))
    problems = (
        check_readme() + check_changelog(manifest["version"]) + check_marketplace(manifest)
    )
    prefix = "::error::" if os.environ.get("GITHUB_ACTIONS") else "error: "
    for problem in problems:
        print(f"{prefix}{problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
