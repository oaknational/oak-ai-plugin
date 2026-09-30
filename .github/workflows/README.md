# CI workflows

Every workflow here declares an explicit `permissions:` block, pins third-party
actions to a full commit SHA with the version in a trailing comment, and sets a
job timeout. Tools installed from npm are installed with lifecycle scripts
disabled, and the gitleaks archive is checked against its published checksum
before it runs.

| Workflow                           | Runs when                                           | What it does                                                                                                                                                                                            |
| ---------------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`checks.yml`](checks.yml)         | Pull requests; pushes to `main`; manually           | `claude plugin validate --strict` on the marketplace and each plugin; checks the README, CHANGELOG and marketplace entry against the plugin; markdownlint and Prettier; gitleaks over the full history. |
| [`link-check.yml`](link-check.yml) | Pull requests; pushes to `main`; manually           | Checks every Markdown link that points inside the repository, anchors included, offline. The plugin's copied changelog is skipped.                                                                      |
| [`pr-title.yml`](pr-title.yml)     | Pull requests opened, edited, reopened or pushed to | Checks the pull request title with commitlint. Pull requests are squash-merged, so the title becomes the commit on `main`.                                                                              |

GitHub also runs **CodeQL** (default setup, not a workflow file here) on the
workflow files and the check script, and **Dependabot** checks the pinned
actions weekly.

The same lint, format, secret and plugin checks run locally through the
pre-commit hooks in [`.pre-commit-config.yaml`](../../.pre-commit-config.yaml).

## Required status checks

The branch ruleset on `main` requires these checks by name. **If you rename a
job, update the ruleset in the same change** — a renamed job silently stops
being required:

- `Plugin validation`
- `Markdown lint + Prettier`
- `Secret scan (gitleaks)`
- `Link check`
- `PR title`

The ruleset also requires CodeQL results, an approving review from a code owner,
and every review thread resolved.
