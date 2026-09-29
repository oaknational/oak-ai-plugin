<!-- Title: a Conventional Commit with the ticket at the end, for example
"chore: publish plugin 0.1.4 from oak-open-curriculum-ecosystem (MCP-123)".
Pull requests are squash-merged, so the title becomes the commit on main. -->

## Description

<!-- What this changes, and why. For a plugin update, name the plugin version and the
oak-open-curriculum-ecosystem commit and release it was copied from. -->

-

## Issue(s)

Fixes MCP-

## How to test

1.

## Checklist

- [ ] Plugin changes were made in oak-open-curriculum-ecosystem first; each package under `<host>/<kind>/<package>/` is an unedited copy of a named commit, without the `evals/` folders, apart from any difference named in this pull request and in `CHANGELOG.md`
- [ ] The plugin version in `plugin.json` has a matching entry at the top of `CHANGELOG.md`, dated the day this merges
- [ ] `claude plugin validate --strict` passes for the plugin and the marketplace
- [ ] The README's skills and commands tables still match what ships
- [ ] The title is a [Conventional Commit](https://www.conventionalcommits.org/) with the ticket at the end
- [ ] Licences respected: Oak brand per the [brand guidelines](https://support.thenational.academy/using-the-oak-brand); Oak curriculum data attributed under OGL v3.0
