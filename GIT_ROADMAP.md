# Mission Control: Git and GitHub side campaign

Created: 2026-11-01. A companion track to `ROADMAP.md`.

## Goal

Learn Git and GitHub from basics to the level expected of a forward deployed engineer (FDE) or an engineer at a large organisation, by using them on Mission Control itself. Target coverage: the ~90% of day-to-day and incident work that such engineers actually do. Plumbing internals, server administration, and rare tools are explicitly out of scope (see the end).

## Rules

- This is a **side campaign**. It awards no ADK XP and never blocks an ADK quest. Track it separately in `PROGRESS.md` under "Git track".
- Each scenario is triggered by a point in the ADK campaign, so Git practice happens on real work, not toy repos. Scenarios may be done early.
- A scenario is complete when its **Done when** condition is observable (in `git log`, on GitHub, or in a terminal transcript), and the user can explain **when to use** and **when not to use** the technique.
- Some scenarios need a "teammate". Simulate one with a second clone **outside OneDrive**, e.g. `~/scratch/mc-teammate`, using a different `user.name`.
- Use your own terminal for interactive commands (`git rebase -i`, `git add -p`); some AI tool environments cannot drive them.

## Format of each scenario

- **When:** the ADK quest that triggers it.
- **Situation:** what happens in the project.
- **Learn:** commands and concepts.
- **Do / Done when:** the task and its observable success condition.
- **Don't:** when the technique is the wrong tool.

## Ranks

| Rank | Scenarios | Paired ADK act |
| --- | --- | --- |
| White belt: solo developer | G0–G10, Git Boss 1 | Act I |
| Green belt: team player | G11–G16, Git Boss 2 | Act II |
| Brown belt: release and safety engineer | G17–G21, Git Boss 3 | Act III |
| Black belt: platform and FDE engineer | G22–G28, Git Boss 4 | Act IV |

---

## White belt: solo developer (Act I)

### G0: Set up your identity and tooling

- **When:** before Quest 1.
- **Situation:** you have a BCG identity and a personal GitHub account (`Sir-Sloth-The-Lazy`). Commits must carry the right email for the right repo.
- **Learn:** `git config --global` (`user.name`, `user.email`, `init.defaultBranch main`, `pull.rebase true`, `core.editor`), conditional includes (`[includeIf "gitdir:~/path/"]`), `gh auth login`, SSH keys vs HTTPS tokens, `git config --list --show-origin`.
- **Do:** configure global defaults. Add an `includeIf` so this folder uses the email you want on GitHub. Authenticate `gh`.
- **Done when:** `git config user.email` inside this repo prints the intended address, and `gh auth status` succeeds.
- **Don't:** commit with an email you don't want public. GitHub shows it on every commit; use your GitHub `noreply` address if unsure.
- **Note on OneDrive:** this repo lives in a OneDrive-synced folder. Sync can corrupt `.git` (half-synced objects, "conflicted copy" files). Push often, so GitHub is your real backup. If `git status` ever looks impossible, re-clone instead of repairing.

### G1: The first commit, done properly

- **When:** start of Quest 1, before any code is committed.
- **Situation:** Quest 1 needs a `.env` with a model API key, a virtualenv, and `__pycache__`. None of these may reach GitHub. The current `.gitignore` only ignores `.vscode`.
- **Learn:** the three areas (working tree, staging area, repository), `git status`, `git add <path>`, `git add -p`, `git diff`, `git diff --staged`, `git commit`, `.gitignore` patterns, `git check-ignore -v <file>`, commit message structure (subject ≤ 50 chars in the imperative mood, blank line, body explaining *why*).
- **Do:** extend `.gitignore` (`.env`, `.venv/`, `__pycache__/`, `*.pyc`, `*.db`, `.DS_Store`). Decide deliberately whether `.claude/` and `.vscode/` belong in the repo. Make a first commit containing only the project memory files.
- **Done when:** `git log` shows one commit, and `git check-ignore -v .env` names the ignore rule.
- **Don't:** use `git add .` or `git add -A` before checking `git status`. That is how secrets get committed.

### G2: First push and the remote

- **When:** right after G1.
- **Situation:** `origin` points to `State-aware-bot` on GitHub, and nothing has been pushed yet.
- **Learn:** `git remote -v`, `git push -u origin main` (upstream tracking), `git fetch` vs `git pull`, `git branch -vv`, public vs private repos, optional repo rename (`gh repo rename`, `git remote set-url`).
- **Do:** push `main`. Decide whether the repo should be private. Optionally rename it to match the project.
- **Done when:** the commit is visible on GitHub and `git status` says "up to date with 'origin/main'".
- **Don't:** use `pull` when you only want to look. `fetch` is always safe; `pull` changes your branch.

### G3: Read history like a detective

- **When:** Quest 1, after a few commits.
- **Learn:** `git log --oneline --graph --decorate --all`, `git show <sha>`, `git diff <a>..<b>`, `git log -p <file>`, `git log --author`, `git log --since`, relative refs (`HEAD~2`, `HEAD^`), and aliases (`git config --global alias.lg "log --oneline --graph --decorate --all"`).
- **Do:** answer, using only Git: "What changed in the agent instructions between my first and latest commit?"
- **Done when:** you can produce that diff in one command.

### G4: Undo locally (before pushing)

- **When:** Quest 1, iterating on the agent instruction.
- **Situation:** you made a bad edit, staged the wrong file, and committed with a typo in the message.
- **Learn:** `git restore <file>` (discard edits), `git restore --staged <file>` (unstage), `git commit --amend`, `git reset --soft HEAD~1` (undo commit, keep staged), `git reset --mixed HEAD~1` (the default: keep the changes but unstage them), and `git reset --hard` (discard everything; dangerous).
- **Do:** perform each undo once on purpose.
- **Done when:** you can say which command to use for each of the five situations above without looking.
- **Don't:** amend or reset commits that are **already pushed** and shared. Use G9 (`revert`) for those.

### G5: A branch for every quest

- **When:** start of Quest 2.
- **Learn:** `git switch -c feat/q2-tools`, `git branch`, `git switch main`, fast-forward vs three-way merge, `git merge --no-ff`, deleting branches (`git branch -d`, `git push origin --delete`), naming conventions (`feat/`, `fix/`, `chore/`, `docs/`).
- **Do:** build Quest 2 tools on a branch and merge it into `main`.
- **Done when:** `git log --graph` shows the branch and merge, and the branch is deleted locally and on the remote.
- **Don't:** keep long-lived branches. The longer a branch lives, the worse the merge.

### G6: Pull requests, issues and the GitHub flow

- **When:** Quest 2 onward; becomes the default way of working.
- **Situation:** big organisations never push directly to `main`. Every change goes through a PR.
- **Learn:** issues (one per quest; labels; milestones per act), `gh issue create`, `gh pr create --fill`, linking with `Closes #12`, PR descriptions (what, why, how tested), self-review on the "Files changed" tab, merge methods (merge commit, squash, rebase) and their effect on history, `gh pr merge --squash --delete-branch`.
- **Do:** open an issue for Quest 2, a PR that closes it, review your own diff, and squash-merge.
- **Done when:** the issue closed automatically, and `main` has one clean commit for the PR.
- **Don't:** make a PR with 40 files across 3 concerns. Reviewers can't review it. Keep one concern per PR.

### G7: Your first merge conflict

- **When:** Quest 3.
- **Situation:** two branches both edit the agent's instruction string, one adding event logging and one rewording the brief format.
- **Learn:** conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`), `git status` during a conflict, resolving in VS Code, `git add` to mark it resolved, `git merge --abort`, `git diff --name-only --diff-filter=U`, `git checkout --ours/--theirs <file>`.
- **Do:** create the conflict on purpose, resolve it by combining both intents, and verify that the agent still runs.
- **Done when:** the merge commit exists and no conflict markers remain (`git grep -n '<<<<<<<'` returns nothing).
- **Don't:** resolve by blindly taking one side. A conflict means two intentions collided, and the resolution must honour both or consciously drop one.

### G8: Stash: switch tasks mid-flight

- **When:** Quest 3 or 4.
- **Situation:** you're halfway through state-scoping work when you notice that a tool on `main` has a bug that needs fixing now.
- **Learn:** `git stash push -m "wip state scopes"`, `git stash list`, `git stash pop` vs `apply`, `git stash -u` (include untracked files), `git stash show -p`.
- **Do:** stash, fix the bug on a new branch, PR it, return and pop.
- **Done when:** both changes are complete and `git stash list` is empty.
- **Don't:** use stash as long-term storage. Stashes are easy to forget; for anything you'll keep for more than a day, use a WIP commit on a branch.

### G9: Revert a bad change that is already on `main`

- **When:** Quest 4.
- **Situation:** a merged PR breaks session persistence, and others (or CI, later) already have that commit.
- **Learn:** `git revert <sha>`, `git revert -m 1 <merge-sha>`, why revert is safe for shared history while reset is not.
- **Do:** revert the bad commit through a PR.
- **Done when:** history shows both the bad commit and its revert, and the behaviour is restored.
- **Don't:** use `git reset` plus a force-push on a shared branch.

### G10: Reflog rescue

- **When:** any time in Act I (do it as a drill).
- **Situation:** you ran `git reset --hard` or deleted a branch and lost commits.
- **Learn:** `git reflog`, `git branch rescue <sha>`, `git reset --hard HEAD@{2}`. Reflog is local and expires after about 90 days by default, and uncommitted work is **not** recoverable.
- **Do:** deliberately lose a commit, then recover it.
- **Done when:** the commit is back on a branch.
- **Lesson:** commit early. Git can rescue almost any commit, but almost never uncommitted edits.

### Git Boss 1: The protected main branch

- **When:** alongside ADK Boss 1.
- **Challenge:** turn on a branch protection rule or ruleset for `main`: require PRs and block force-pushes. Then try to push directly to `main` and watch it get rejected. Deliver Boss 1 work through issue → branch → PR → squash-merge. Tag the result (`git tag -a boss-1 -m "..."`, `git push origin boss-1`).
- **Done when:** the direct push was rejected, the PR is merged, and the tag is visible on GitHub.

---

## Green belt: team player (Act II)

### G11: Keep your branch current with rebase

- **When:** Quest 5.
- **Situation:** `main` moved on while you built the Sequential pipeline. Your PR is now stale.
- **Learn:** `git fetch` then `git rebase origin/main`, resolving conflicts mid-rebase (`git rebase --continue / --skip / --abort`), merge vs rebase trade-offs, `git push --force-with-lease`, `git pull --rebase`.
- **Do:** with the teammate clone, push a change to `main`, then rebase your feature branch on top of it.
- **Done when:** your branch history is linear on top of `origin/main` and the PR shows no conflicts.
- **Don't:** rebase a branch someone else is building on. Never use plain `--force`; `--force-with-lease` refuses to overwrite work you haven't seen.

### G12: Polish history before review (interactive rebase)

- **When:** Quest 5 or 6, before opening a PR.
- **Situation:** your branch has "wip", "fix typo", and "actually fix" commits.
- **Learn:** `git rebase -i origin/main` (pick, reword, squash, fixup, drop, reorder), `git commit --fixup <sha>` plus `git rebase -i --autosquash`, `git add -p` to split concerns into separate commits.
- **Do:** turn a messy branch into 2–4 logical commits, each of which runs.
- **Done when:** each commit's message explains one coherent change.
- **Don't:** rewrite commits that are already merged into `main`.

### G13: Worktrees for parallel researchers

- **When:** Quest 6 (parallel agents, parallel branches).
- **Situation:** you want to work on the web researcher and the document researcher at the same time, without stashing or switching branches.
- **Learn:** `git worktree add ../mc-web -b feat/web-researcher`, `git worktree list`, `git worktree remove`. Each worktree is a separate checkout that shares one repository.
- **Do:** develop two researchers in two worktrees and merge both via PRs.
- **Done when:** `git worktree list` shows both during the work and only the main worktree afterwards.
- **Don't:** check out the same branch in two worktrees (Git blocks it). Put worktrees outside OneDrive.

### G14: Cherry-pick a fix to the right place

- **When:** Quest 7.
- **Situation:** you fixed a routing bug while on the coordinator branch, but it needs to ship to `main` now, separately.
- **Learn:** `git cherry-pick <sha>`, `-x` (records the origin), resolving cherry-pick conflicts, and why cherry-picks create a *new* commit with a different SHA.
- **Do:** cherry-pick the fix onto a `fix/` branch and PR it.
- **Done when:** the fix is on `main`, and the coordinator branch rebases cleanly afterwards.
- **Don't:** use it routinely to move whole features between branches. That's a merge or rebase.

### G15: Bisect: find the commit that broke the critic

- **When:** Quest 8.
- **Situation:** the critic loop used to stop at its revision limit; now it runs forever. There are 20 commits between "working" and "broken".
- **Learn:** `git bisect start`, `git bisect bad`, `git bisect good <sha-or-tag>`, `git bisect run <test-command>`, `git bisect reset`.
- **Do:** write a small deterministic test for the stopping condition (no live model calls, using a stub), plant a regression a few commits back, and let `bisect run` find it.
- **Done when:** bisect names the exact offending commit.
- **Don't:** bisect with flaky tests (live LLM calls are non-deterministic). Bisect needs a reliable yes/no check.

### G16: Archaeology: blame and the pickaxe

- **When:** Quest 8.
- **Situation:** "Who changed `max_iterations` from 3 to 10, and why?"
- **Learn:** `git blame -w -C <file>`, `git log -S "max_iterations"` (the pickaxe: commits that add or remove the string), `git log -G <regex>`, `git log -L :function_name:file.py`, GitHub's blame view and "view PR" link.
- **Do:** answer the question, including the PR that introduced it.
- **Done when:** you can link the commit and the PR discussion.
- **Lesson:** this is why commit messages and PR descriptions explain *why*.

### Git Boss 2: The crowded repository

- **When:** alongside ADK Boss 2.
- **Challenge:** using the teammate clone, create three concurrent branches that touch overlapping files: the evidence merger, the critic, and a schema change. Enable `git config rerere.enabled true`. Land all three through PRs: one via rebase, one with a real conflict, and one that needs a cherry-picked prerequisite. Keep `main` working after every merge.
- **Done when:** all three PRs are merged, no merge produced broken code, and you can explain each choice of merge or rebase.

---

## Brown belt: release and safety engineer (Act III)

### G17: The leaked API key (incident drill)

- **When:** Quest 9 or 10, or the first time any credential exists in the project. Use a **fake** key for the drill.
- **Situation:** a key was committed and pushed. Bots scrape public GitHub for keys within minutes.
- **Learn:** the correct order is (1) **revoke and rotate the key first**, (2) remove it from the code (`git rm --cached .env`, then `.gitignore`), (3) purge it from history only if needed (`git filter-repo --path .env --invert-paths` or BFG, then force-push and have everyone re-clone), (4) prevent recurrence. Also learn GitHub secret scanning and push protection, and why deleting the file in a new commit is not enough.
- **Do:** run the full drill on a throwaway repo with a fake key.
- **Done when:** the fake key is absent from `git log -p --all`, and you can recite the order of steps.
- **Don't:** treat a history rewrite as the fix. The rotation is the fix; the rewrite is cleanup.

### G18: Large and generated files

- **When:** Quest 9 (artifacts) and Quest 10 (memory and session stores).
- **Situation:** report versions, uploaded PDFs, SQLite session databases and eval outputs start appearing in `git status`.
- **Learn:** what belongs in Git (source, config, small fixtures) vs what doesn't (runtime data, caches, build output, model outputs); `git rm -r --cached <dir>`; Git LFS (`git lfs track "*.pdf"`, `.gitattributes`) for files that legitimately need versioning; `.gitattributes` for line endings and diff behaviour; and why a 100 MB file in history bloats every clone forever.
- **Do:** ignore runtime data directories, and keep a small set of test fixtures tracked (via LFS if they are binary).
- **Done when:** a fresh clone is small, and the app still runs from it.

### G19: Tags, semantic versions and GitHub releases

- **When:** Boss 3. Optionally tag every boss retroactively.
- **Learn:** annotated vs lightweight tags, semantic versioning (`v0.3.0`: MAJOR.MINOR.PATCH), `git tag -a`, `git push origin <tag>`, `git switch --detach v0.2.0` (inspect an old version), `gh release create v0.3.0 --generate-notes`, `git describe`.
- **Do:** release `v0.3.0` at the end of Act III with generated release notes.
- **Done when:** the release appears on GitHub, and `git describe` on `main` references it.
- **Don't:** move or delete a tag that others have pulled. Make a new version instead.

### G20: Hotfix on a release branch

- **When:** Quest 11 or 12.
- **Situation:** `v0.3.0` is "in use" (pretend a stakeholder runs it). `main` already contains half-finished Quest 12 work. A bug is found in `v0.3.0`.
- **Learn:** `git switch -c release/v0.3 v0.3.0`, fix, tag `v0.3.1`, then bring the fix back to `main` (cherry-pick or merge). This is the release-branch model used by large organisations.
- **Done when:** `v0.3.1` exists, contains only the fix, and the fix is also on `main`.
- **Don't:** ship `main` as the hotfix. It contains unreleased, unfinished work.

### G21: Commit conventions and changelogs

- **When:** Act III onward.
- **Learn:** Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`, `!` for breaking changes), why many organisations enforce them (automated versioning and changelogs), and `CHANGELOG.md` maintenance.
- **Do:** adopt the convention for all PR titles, which become squash-merge commit messages.
- **Done when:** the release notes for the next tag read like a meaningful changelog.

### Git Boss 3: The poisoned release

- **When:** alongside ADK Boss 3.
- **Challenge:** a teammate's PR shipped in `v0.3.1`. It contains (a) a fake credential in a config file and (b) a regression in resume behaviour. Rotate the fake credential, purge it from history, bisect between `v0.3.0` and `v0.3.1` to find the regression, revert it via a PR, and release `v0.3.2`.
- **Done when:** `v0.3.2` is clean, the credential is gone from history, and you can explain each step's order.

---

## Black belt: platform and FDE engineer (Act IV)

### G22: Pre-commit hooks

- **When:** Quest 13.
- **Situation:** catch problems before they leave your machine.
- **Learn:** `.git/hooks` (local and not shared) vs the `pre-commit` framework (`.pre-commit-config.yaml`, shared through the repo); hooks for `ruff` (lint and format), `gitleaks` (secrets), large-file checks, and trailing whitespace; `git commit --no-verify` and why reviewers frown on it.
- **Do:** install pre-commit with at least formatting and secret scanning.
- **Done when:** committing a fake key is blocked locally.

### G23: Continuous integration with GitHub Actions

- **When:** Quest 15 (the eval arena is a natural CI job).
- **Learn:** `.github/workflows/*.yml`, triggers (`pull_request`, `push`, `workflow_dispatch`), jobs, steps, the `actions/checkout` and `actions/setup-python` actions, dependency caching, matrix builds, repository secrets (`${{ secrets.X }}`), why PRs from forks don't receive secrets, and keeping paid model calls out of default CI (use deterministic tests, and run live evals manually or on a schedule).
- **Do:** run lint plus unit tests on every PR. Add a manually triggered workflow for ADK evals.
- **Done when:** a PR shows a green check, and a deliberately broken PR shows a red one.

### G24: Governance: rulesets, CODEOWNERS, templates

- **When:** Quest 15 or 16.
- **Learn:** rulesets and branch protection (required status checks, required reviews, linear history, signed commits), `CODEOWNERS`, PR and issue templates (`.github/pull_request_template.md`, `.github/ISSUE_TEMPLATE/`), Dependabot (`.github/dependabot.yml`) for dependency updates such as the pinned ADK version.
- **Do:** require CI to pass before merging to `main`, add a PR template with "what / why / how tested / evidence", and enable Dependabot.
- **Done when:** a PR with failing CI cannot be merged, and Dependabot opens its first PR.

### G25: Deploy from Git

- **When:** Quest 16.
- **Learn:** deploying on a tag push (`on: push: tags: ['v*']`), GitHub Environments with protection rules (manual approval before production), OIDC / Workload Identity Federation to Google Cloud instead of long-lived JSON keys, and rollback by redeploying the previous tag.
- **Do:** pushing `v1.0.0` deploys Mission Control to Cloud Run after an approval.
- **Done when:** the deploy run is linked to the tag, and you can roll back to the previous tag.

### G26: Forks and open-source contribution

- **When:** any time in Act IV. Quest 14 (MCP) is a natural point: you'll be reading upstream source.
- **Situation:** you find a docs error or a small bug in `google/adk-python` or `adk-recipes`.
- **Learn:** fork vs clone, `git remote add upstream`, syncing a fork (`git fetch upstream`, `git rebase upstream/main`, or `gh repo sync`), contributing guidelines, CLA / DCO (`git commit -s`), and responding to review by pushing more commits.
- **Do:** open a real upstream PR (even a typo fix), or rehearse the full flow on a fork if nothing is worth submitting.
- **Done when:** a PR from your fork exists against an upstream repo, or the rehearsal is documented.

### G27: Signed commits and identity hygiene

- **When:** Act IV.
- **Learn:** why organisations require signed commits, SSH commit signing (`git config gpg.format ssh`, `user.signingkey`, `commit.gpgsign true`), adding the signing key to GitHub, and the "Verified" badge.
- **Done when:** your new commits show "Verified" on GitHub.

### G28: The FDE field kit

- **When:** late in Act IV, as preparation for client work.
- **Situation:** FDEs work inside *someone else's* Git setup, often with restrictions.
- **Learn:**
  - Multiple identities: `includeIf` per client directory, separate SSH keys via `~/.ssh/config` host aliases.
  - Other hosts: GitHub Enterprise, GitLab (a "merge request" is a PR), Azure DevOps, Bitbucket. The concepts are identical; the UI and CLI differ.
  - Huge monorepos: shallow clones (`--depth 1`), partial clones (`--filter=blob:none`), `git sparse-checkout set <dirs>`.
  - Submodules: recognise them (`.gitmodules`), use `git clone --recurse-submodules` and `git submodule update --init`. Avoid introducing them yourself.
  - No push access or air-gapped environments: `git format-patch` / `git am`, `git bundle create`.
  - Reading an unfamiliar repo fast: `git log --stat`, `git shortlog -sn`, and `git log --since="3 months" --name-only` to see the hot files.
- **Do:** clone a large public monorepo partially and sparsely. Move a commit between two clones using only a patch file.
- **Done when:** both are done, and you can explain when each would be needed on a client engagement.

### Git Boss 4: The production incident

- **When:** alongside ADK Boss 4.
- **Challenge:** `v1.1.0` is deployed and broken. Under time pressure:
  1. Roll back by redeploying `v1.0.0`.
  2. Bisect between the tags to find the cause.
  3. Fix it on a branch with CI passing and required review.
  4. Release `v1.1.1` through the protected pipeline.
  5. Write a short post-mortem that links commits, PRs and the deploy runs.
- **Done when:** the post-mortem reconstructs the incident entirely from Git and GitHub records.

---

## Quick decision table: "I want to undo…"

| Situation | Use | Never |
| --- | --- | --- |
| Unsaved edits to a file | `git restore <file>` | — |
| Staged the wrong file | `git restore --staged <file>` | — |
| Last commit, not yet pushed | `git commit --amend` or `git reset --soft HEAD~1` | — |
| A commit already pushed and shared | `git revert <sha>` | `reset` plus force-push |
| Lost commits after a reset or branch delete | `git reflog` | panic |
| A secret was pushed | Rotate first, then remove, then purge history | Only deleting the file |
| A remote branch or tag | `git push origin --delete <name>` | Deleting tags others use |

## Out of scope (the remaining ~10%)

Plumbing commands (`hash-object`, `cat-file` beyond curiosity), custom merge drivers, `git-svn` and other migrations, hosting your own Git server, Gerrit-style stacked review, and advanced monorepo tooling (Scalar, VFS). Learn these on demand.

## Change log

- 2026-11-01: Created the Git and GitHub side campaign at the user's request (28 scenarios plus 4 Git bosses, paired with ADK acts). It awards no ADK XP and does not block ADK quests.
