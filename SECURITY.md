# Security Policy

## Supported Versions

We continuously update and improve Oak National Academy's product and codebase,
including patching security vulnerabilities.

Only the latest published version of each plugin is supported: the version on
`main` and in the latest [release](https://github.com/oaknational/oak-ai-plugins/releases).
Fixes are rolled forward in a new version, not backported to earlier releases.

| Version                      | Supported          |
| ---------------------------- | ------------------ |
| Latest release, as on `main` | :white_check_mark: |
| Any earlier release          | :x:                |

The plugins connect to the Oak Curriculum MCP server at
`https://mcp.thenational.academy/mcp`. Vulnerabilities in that service are
reported the same way.

## Reporting a Vulnerability

To report any vulnerability please see our [security.txt](https://www.thenational.academy/.well-known/security.txt) file

Please do **not** report vulnerabilities through the AI plugin feedback form, a
pull request, or any other public channel. See [SUPPORT.md](SUPPORT.md) for
non-security questions.
