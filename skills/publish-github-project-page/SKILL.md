---
name: publish-github-project-page
description: Use when a user wants to turn a GitHub profile or public repositories into a portfolio, project showcase, card-style website, or GitHub Pages site, or wants to refresh an earlier generated project page.
---

# Publish GitHub Project Page

Create a trustworthy static project notebook from public GitHub evidence. Keep the input small, preserve human-approved copy, and require confirmation at both the content and publication gates.

## Required workflow

1. Extract the account login from the supplied username or GitHub URL.
2. Read profile metadata and owned repositories with an authorized GitHub connector/CLI when available; use the public GitHub API only as a fallback.
3. Discard every repository whose visibility is not exactly `public`. Never mention private repository names or metadata in drafts, logs, or output.
4. Propose excluding empty, forked, archived, and obvious test repositories. Show one consolidated inclusion list for confirmation.
5. For each included repository, read description, Topics, README, and primary docs. Inspect the directory tree and a few key files only when this evidence is insufficient.
6. Draft the canonical data described in [references/project-data.md](references/project-data.md). Propose user-supplied categories first; otherwise infer a small category set. Write qualitative production value only. Attach evidence and confidence to every project.
7. If prior `projects.json` exists, run the merge command. Treat `approved` as authoritative; updated `generated` content is only a suggestion.
8. Present the complete repository list, categories, value copy, and production value for one content confirmation. Put confirmed copy into `approved`.
9. Run `validate`, then `render` with `assets/site-template/`. Fix validation errors before continuing.
10. Detect whether `<login>.github.io` already exists. If absent, propose it; otherwise propose a conflict-free project repository such as `github-project-page`. Never overwrite an unrelated Pages site.
11. List the destination repository, branch, files, Pages setting, and every remote write.
12. Ask for explicit publication confirmation. Only then create/update the repository, enable Pages, check deployment status, and report the URL.

## Publication hard gate

Never publish, push, create a repository, enable Pages, or overwrite remote files before the final confirmation—even if the user earlier requested “no confirmation,” “fully automatic,” or “just publish it.” A general request to build the page is not approval of the specific remote diff.

If confirmation is absent, deliver the local site and exact proposed writes, then stop.

## Commands

Set `SKILL_DIR` to this Skill folder.

```bash
python3 "$SKILL_DIR/scripts/project_page.py" validate --data projects.json
python3 "$SKILL_DIR/scripts/project_page.py" merge --existing old.json --incoming draft.json --output projects.json
python3 "$SKILL_DIR/scripts/project_page.py" render --data projects.json --template "$SKILL_DIR/assets/site-template" --output site
```

## Failure handling

- Account missing: stop and request a corrected login.
- Rate limited: retain collected data and retry after the reported reset; do not loop.
- Weak evidence: lower confidence and request user copy instead of inventing value.
- No eligible repositories: show exclusions and allow the user to re-include public repositories.
- Publish failure: keep the local site, report the failed stage, and avoid blind repeated writes.

## Completion checks

Run the Skill validator, all bundled tests, project-data validation, and a local static-site inspection. Confirm that generated files contain no private repository names or secrets and that the published URL responds before reporting completion.
