# Agent instructions — NaturePath

## Read before working

Read [current context](docs/agent-context.md), the latest entries in
[the agent log](docs/agent-log.md), and [the MVP roadmap](docs/roadmap.md).
Check the working tree and recent commits; preserve other contributors' changes.

## GitHub issues and Project alignment

Before starting work and again before each logical work commit, inspect the live
GitHub issue(s) and linked Project for `KevinSaurel/NaturePath`. Read the objective,
acceptance criteria, comments, state, Project status, priority, dependencies,
assignees and milestone/sprint. Use the connected GitHub tools where supported;
use `gh` for Project fields and other unsupported reads. See
[GitHub workflow](docs/git-setup.md#current-issue-and-project-workflow).

Work on a feature/documentation/fix branch and reference the applicable issue in
commit messages and PR descriptions (`Refs #7` for partial calibration work, for
example). Recheck remote history before publishing; do not rewrite published or
other contributors' commits. Keep the required log-only amendment below.

Treat the current GitHub plan and its official milestones as the coordination
baseline; the roadmap's four implementation increments are not official sprints.
Reconcile outdated local context explicitly. If an issue or Project cannot be
read, record the exact access limitation and distinguish verified issue metadata
from unverified Project fields. Never invent task IDs, status or dependencies.

Keep tracking aligned with actual evidence. Partial tooling improvements do not
complete a hardware-calibration issue. Use `Closes #N` or mark an issue/Project
item Done only when all applicable criteria, evidence and required PR review are
complete. Report remaining work and distinguish local commits, published work
and reviewed/merged work. Do not claim or backdate team review.

## Required record after every commit

Every agent must document **every logical work commit**, including documentation,
configuration and fixes. Immediately after creating a commit, and before pushing
or handing off, append an entry to `docs/agent-log.md` containing:

- Date in UTC and agent identity (use `Codex` if no other identity is available).
- Exact commit subject; include the SHA for earlier commits when useful.
- What changed and the relevant files.
- Why the work was needed and the decisions or assumptions behind it.
- Checks actually run and their outcomes; distinguish untested work and proposals
  from verified behaviour.
- Remaining limitations, blockers and the next useful action.

Persist the entry by amending **only your own just-created, unpublished commit**.
Identify that commit by its subject: including its final SHA in its own file would
change the SHA again. An amendment solely to attach or correct this record does
not require another entry. Do not amend a published commit or another author's
work; use a follow-up documentation commit with its own entry instead.

Update `docs/agent-context.md` whenever the current state, accepted decisions,
blockers or next steps change. Do not finish a task with an uncommitted record.
Keep entries chronological. Correct historical mistakes explicitly rather than
silently rewriting what was previously reported.

## Project essentials

Build the end-to-end MVP first, following the roadmap and the submitted proposal.
Do not claim hardware is tested merely because a module imports or a mock passes.
Use English for new repository documentation; communicate with the user in Spanish.
Never record tokens, passwords, private keys or unredacted credential-bearing
commands in documentation, logs, code or commit messages. Summarise relevant
conversation decisions; do not copy the chat transcript.
