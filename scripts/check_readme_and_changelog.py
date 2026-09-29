"""Check the README and CHANGELOG against the Claude plugin they describe.

The README restates facts the plugin holds: the skills that ship, the
workflows' commands and the MCP config. The CHANGELOG's latest entry must be
the version the plugin carries. Each is recomputed from the plugin, so the
two files can't drift from it. Run by CI and by the pre-commit hook.
"""

import json
import os
import re
import sys

PLUGIN = "claude/plugin/oak-open-curriculum"


def main() -> int:
    readme = open("README.md", encoding="utf-8").read()
    skills = set(os.listdir(f"{PLUGIN}/skills"))
    workflows = set(os.listdir(f"{PLUGIN}/workflows"))
    table = readme.split("## The skills", 1)[1].split("###", 1)[0]
    listed = set(re.findall(r"^\|\s*`([^`]+)`\s*\|", table, re.M))
    commands = set(re.findall(r"^\|\s*`/([a-z-]+)", readme, re.M))
    snippet = json.loads(re.search(r"```json\n(.*?)```", readme, re.S).group(1))
    mcp = json.load(open(f"{PLUGIN}/.mcp.json", encoding="utf-8"))

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

    version = json.load(open(f"{PLUGIN}/.claude-plugin/plugin.json", encoding="utf-8"))["version"]
    changelog = open("CHANGELOG.md", encoding="utf-8").read()
    latest = re.search(r"^## (\S+)", changelog, re.M)
    if not latest or latest.group(1) != version:
        found = latest.group(1) if latest else "none"
        problems.append(f"CHANGELOG: latest entry is {found}, plugin.json says {version}")

    prefix = "::error::" if os.environ.get("GITHUB_ACTIONS") else "error: "
    for problem in problems:
        print(f"{prefix}{problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
