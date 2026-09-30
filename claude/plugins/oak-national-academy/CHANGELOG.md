# Changelog

Versions are the plugin manifest version. The Claude Code plugin and the
ChatGPT/Codex package are cut from the same source at the same version.

## 0.1.4 — unreleased

- The Claude plugin and the ChatGPT/Codex package are renamed from
  `oak-open-curriculum` to `oak-national-academy`, to match the display name.
  The full form of a command is now `/oak-national-academy:<skill>`. Claude
  Code moves existing installs to the new name.
- The MCP server is now named `oak-national-academy`. It is the same server at
  the same address, but Claude identifies it by the plugin and server names, so
  it asks you to sign in again and to approve each tool again the first time it
  is used.

## 0.1.3 — 2026-09-28 (repo release v1.185.3)

- Claude plugin: adds an icon, a privacy policy link and a README, which the
  Claude plugin directory asks for.
- oak-curriculum-principles: the hexagon diagram's path is a Markdown link,
  not code, so the directory does not hold the plugin for a reviewer.

## 0.1.2 — 2026-09-17 (repo release v1.182.0)

- Adds the ChatGPT/Codex package: the same skills, with the two workflows
  packaged as skills.
- oak-accessibility: transcripts recommended, not required, at WCAG AA.
- MCP-enabled skill and agents: tool names may arrive with underscores in
  place of hyphens.
- oak-curriculum-principles: three passages matched to oak-skills' approved
  wording.
- find-misconceptions: keeps the order the tool returns.

## 0.1.1 — 2026-09-07

- audit-sequence: checks same-year order now the tool serves it; reads
  prior-knowledge statements as what a unit assumes, not a dependency graph.

## 0.1.0 — 2026-08-07

- First release: three skills, two workflows, two agents, and the Oak
  Curriculum MCP binding.
