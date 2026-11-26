# Agent activity log

Read [current context](agent-context.md) first for the latest state. Follow
[AGENTS.md](../AGENTS.md) when adding records. Entries describe work and evidence,
not a verbatim conversation. Never include credentials.

The first four entries below were reconstructed on 12 November 2026 from Git
history and the current agent's conversation/tool results. They are retrospective,
not contemporaneous records written by earlier agents. Exact times are not inferred.

## 2026-11-12 UTC — Codex — initial project preparation (retrospective)

**Commit:** `d920474` — `chore: prepare NaturePath IoT project from challenge document`

**What:** Created the repository scaffold, copied the proposal PDF, extracted its
text, and added requirements, architecture, backlog, hardware/Git notes,
`requirements.txt`, a starter package and `scripts/check_environment.py`.

**Why:** The user asked to inspect the challenge and prepare the existing empty
GitHub repository before starting implementation. The proposal established the
moisture-first MVP, local feedback, HTTP, SQLite and dashboard requirements.

**Validation:** Ran the diagnostic with system Python and the existing Grove venv;
compiled the Python scaffold and checked whitespace. Initial Git access attempts
failed in an isolated session. Later HTTPS publication succeeded after access changed.

**Limitations / next:** This was scaffolding, not a working MVP. Physical sensors,
actuators, calibration and application features remained unimplemented.

## 2026-11-12 UTC — Codex — HTTPS authentication documentation (retrospective)

**Commit:** `c663514` — `docs: document HTTPS authentication for project repository`

**What:** Updated `docs/git-setup.md` for HTTPS and the actual authenticating account,
`hugoArenaza-deusto`, while retaining the original access errors as historical context.

**Why:** The repository owner is `KevinSaurel`, but authentication must use the
account associated with the credential. The user requested publication from the Pi.

**Validation:** An initial authentication attempt was rejected. A subsequent
user-provided credential successfully pushed `main`; local and remote SHA were
both `c663514c2094f310c4b482c18309c6761798f70e`.

**Limitations / next:** Credentials were used transiently, not embedded in the
remote URL or project files. The user was advised to revoke disclosed credentials;
revocation was not verified. Application development remained pending.

## 2026-11-12 UTC — Codex — English README (retrospective)

**Commit:** `30aaac9` — `docs: translate project README into English`

**What:** Translated the README, shell-example comments and workflow examples
into English, preserving the stated project scope and pending implementation status.

**Why:** The user explicitly requested an English README.

**Validation:** Checked whitespace and successfully pushed the commit to `main`.
No application tests were needed for this translation.

**Limitations / next:** Existing Spanish documentation was retained. The change
did not implement or validate any sensor or server functionality.

## 2026-11-12 UTC — Codex — lab-aligned MVP roadmap (retrospective)

**Commit:** `1589eb8` — `docs: plan MVP implementation aligned with IoT labs and rubric`

**What:** Added `docs/roadmap.md`, linked it from the README and original backlog,
and updated hardware observations with the successful real-host diagnostic.
Reviewed the lab archive's handouts and code examples and the assessment text
supplied by the user. Kept teaching archives and nested repositories out of Git.

**Why:** The user confirmed hardware availability and asked for implementation
order and their own preparatory tasks. The later scope clarification was to finish
the MVP before scaling. The supplied proposal rubric permits a local server and
does not make cloud/MQTT/Edge AI mandatory for that MVP.

**Decisions:** Plan four demonstrable increments: sensing/minimal API; analysis
and physical feedback; SQLite/weather/dashboard; autonomous operation and validation.
Start with the Lab 5 Open-Meteo provider, without an API key. Keep Euskalmet,
MQTT/platforms, learned health detection and distributed nodes as later options.
Do not guess sensor models, GPIO wiring or classification thresholds.

**Validation:** Existing Lab 4 checker passed: Pi 5 GPIO backend, HAT at `0x08`,
matching installed Grove ADC default. A real Open-Meteo request returned HTTP 200
without a key and included requested current/hourly fields. Checked local Markdown
links and whitespace. Push succeeded; local and remote SHA both matched
`1589eb81179f4e16502c935e1eaba0f5cac4c0f5`.

**Limitations / next:** Passing the setup checker does not test individual modules.
Obtain exact models/port mapping and collect physical calibration observations.
The final implementation deadline remains unconfirmed. No application features
were added by this planning commit.

## 2026-11-12 UTC — Codex — agent handoff and required commit records

**Commit subject:** `docs: establish agent handoff context and commit logging rules`

**What:** Added root `AGENTS.md`, `docs/agent-context.md` and this activity log;
linked them from the README. Reconstructed prior commit records and summarised
accepted scope, verified environment, source locations, unresolved issues and next inputs.

**Why:** The user asked to preserve agent context from this conversation and to
require every agent to explain its work after every commit. `AGENTS.md` uses the
standard uppercase filename so coding agents can discover the instructions.

**Workflow decision:** Write the record immediately after a work commit, then amend
only that agent's just-created unpublished commit to include it before pushing.
Use the commit subject for self-identification to avoid recursive SHA changes.
Logging-only amendments do not generate another record. Published/shared history
must not be amended. Keep the current handoff context separate from historical entries.

**Validation:** Checked local documentation links, whitespace and absence of
GitHub token strings in the new/updated documentation. This documentation-only
change does not require application tests. Remote publication is checked after
push; consult live Git refs for publication state rather than treating this record
as proof of a future push.

**Limitations / next:** The user is still preparing hardware information before
coding. Exact models, wiring, location and calibration observations are outstanding.
Keyboard behaviour remains unresolved despite configuration changes. Credential
revocation is unverified. Continue with Sprint 1 only within the user's authorised scope.

## 2026-11-12 UTC — Codex — confirmed module inventory and LED bar plan

**Commit subject:** `docs: record Grove module inventory and LED bar design`

**What:** Replaced the generic hardware checklist with all eight user-reported
module names/revisions in `docs/hardware.md`. Added expected interfaces, candidate
local drivers, pending connection fields, validation order and manufacturer links.
Updated the current handoff and roadmap to use LED Bar v2.1 as the main visual
indicator and Red LED Button v1.0 as the visitor input/acknowledgement device.

**Why:** The user supplied the actual inventory and selected the LED bar to model
a future park entrance. Recording the two-signal requirements prevents future
agents from treating the bar or LED button as a one-GPIO plain LED/button.

**Decisions / assumptions:** Reported board markings are user-confirmed; DHT11 and
MMA7660FC identities and LCD/accelerometer addresses are expected from manufacturer
family documentation and remain physically unverified. The LED bar uses explicit
status masks, with LCD explanations, rather than an unexplained precision scale.
No GPIO assignments or calibration thresholds were invented.

**Validation:** Consulted Seeed manufacturer documentation for the LCD, ambient
sensor, accelerometer, LED bar, LED button and water sensor. Inspected existing
Grove source for JHD1802, LED button, water, moisture and ADC; observed contradictory
wet/dry example thresholds in the water module, so calibration is required.
Checked local documentation links, credential patterns and Git whitespace.
Documentation-only change; no hardware activation, library installation or
application tests performed. Verify publication through Git refs after pushing.

**Limitations / next:** Obtain the current module-to-port mapping or agree a new
conflict-free layout; confirm inferred device identities and electrical compatibility,
then run bounded individual hardware tests and physical calibration. The full
MVP implementation remains pending.

## 2026-11-12 UTC — Codex — session close-out

**Commit subject:** `docs: close agent session for 12 November 2026`

**What:** Added `docs/sessions/2026-11-12.md` summarising the day's work, decisions,
reported inventory, verification evidence, unresolved items and ordered resumption
steps. Updated `docs/agent-context.md` to mark the session closed at the user's
request and link the summary.

**Why:** The user asked to publish a final daily agent record and continue another
day. A concise handoff avoids redoing preparation or mistaking planning for working
hardware/software. No further implementation or hardware activity is to continue
as part of this session.

**Validation:** Confirmed the repository was clean and synchronised before the
close-out change. Checked local links, credential patterns and Git whitespace.
No application tests were run for this documentation-only change. Publication and
clean working-tree state are checked after push, without claiming them in advance.

**Limitations / next:** MVP implementation, individual module tests and calibration
remain pending. Next session starts with current connections or an agreed port map,
especially the two-signal LED bar and LED button. Preserve the known uncertainties
about driver identities, keyboard behaviour, credential revocation, location and deadline.

## 2026-11-19 UTC — Codex — visual hardware calibration workbench

**Commit subject:** `feat: add local visual Grove calibration workbench`

**What:** Added the local Flask calibration app, lazy real/simulated hardware
adapters, Spanish HTML/CSS/JS interface, source packaging, isolated project venv,
launcher, 13 automated tests and a physical calibration guide. Assigned moisture
A0, water A2, expected DHT11 D5, buzzer D16, LED bar D22 (22/23), red LED button
D24 (24/25), LCD and accelerometer to shared-bus I2C connectors. Updated the README,
hardware/context/roadmap, test notes and 19 November session record.

**Why:** The user confirmed all modules were disconnected and requested a port
assignment and visual calibration programs. The tool turns stable real observations
into reviewable references instead of guessing thresholds from lab examples.

**Decisions / assumptions:** Physical wiring and exact chip identities remain
unverified. Start the page disarmed and require explicit acquisition/output actions.
Use one acquisition worker, independent per-sensor errors, bounded output tests,
GPIO/I2C cleanup and a process lock for this tool. Simulation is explicit, visibly
labelled, stored separately and never a fallback. Derive cutoffs only from separate
observed ranges, keep partial profiles explicit, and use an immobile mean gravity
vector for zero; known-angle captures are validation evidence, not a fitted scale.
DHT polling is spaced by at least three seconds, even after failure.

**Validation:** 13 unittest checks passed, including overlap/polarity, moving-zero
rejection, cleanup after DHT failure, capture failure/cancellation, persistence,
mode isolation, cached observation counting and HTTP input/command guards.
Python compilation, launcher syntax, Markdown links, whitespace and token-pattern
checks passed. Built a wheel and verified the HTML/CSS/JS are included. System
Chromium/Playwright completed two simulated water captures, reference calculation,
a simulated output action and stop; no JavaScript errors or mobile overflow.
A final UI check confirmed Spanish profile messages. The real-mode launcher served
HTTP 200 with acquisition disarmed and no readings. Preview processes were stopped.
The isolated install reported an unrelated inherited types-flask-migrate dependency
warning; required imports and application checks passed. The shared lab venv was
not modified. The server restarted during development; saved state was checked
before resuming rather than repeating the completed install.

**Limitations / next:** No physical sensor read, GPIO activation, wiring change or
real calibration was performed by this task. The user must connect with power off,
confirm the map and observe individual tests. Start with dry/damp/wet soil and
dry/wet water batches, then level/known-angle checks; verify real DHT11 reliability
and output mapping. The final trail classifier, monitoring API/dashboard, weather
and autonomous MVP services are still pending. This app remains a local calibration
server, not a cloud-hosted Site or production deployment. Check Git refs after push
for publication state; do not infer publication from this pre-push record.

## 2026-11-26 UTC — Codex — delete saved calibration captures

**Commit subject:** `feat: allow deleting saved calibration captures`

**What:** Added a token-protected per-capture deletion endpoint and Spanish
**Borrar** buttons with confirmation in `src/naturepath/calibration.py`,
`static/calibration.js`, `static/calibration.css` and
`templates/calibration.html`. Updated `tests/test_calibration.py`,
`docs/calibration.md` and `docs/agent-context.md`.

**Why / decisions:** The user requested removal of saved calibration records.
Deletion requires acquisition to be fully stopped, removes only the selected
capture in the current mode, updates future exports and clears a deleted capture's
status. If the saved profile references that capture, remove the whole profile
before deleting the observations to prevent stale references after restart;
rebuilding remains explicit. Unused-capture deletion preserves the saved profile.
Other captures and already-downloaded exports remain intact. File failures return
JSON errors and retain the record when its file cannot be removed; a profile
already removed before a subsequent file failure must be rebuilt after retrying.

**Validation:** All 20 unittest checks passed after the final code/test edits,
including five new deletion regressions covering page-token protection,
unknown/repeated IDs, disk/restart persistence, CSV/JSON exports, hardware/simulation
isolation, running/stopping guards, dependent/unused profiles, level reset and file
permission errors. A temporary simulated Flask server and system Chromium via
Playwright passed capture, disabled deletion while running, cancelling and accepting
the confirmation, final-row removal, profile/status clearing, empty JSON export,
reload/reinitialisation persistence and a 390px viewport overflow check, with no
JavaScript errors. The sandbox initially blocked the local server socket; the same
browser check passed with approved escalation. `git diff --check` passed.
No physical sensors or actuators were activated, and no existing calibration data
was deleted by validation.

**Limitations / next:** Deletion is permanent and applies to whole captures, not
individual samples. Export first if a backup is needed. Restart an existing
calibration server and reload its page to use the updated code. Real soil/button
verification, physical reference collection and remaining MVP work are still
pending; no hardware validation is claimed. This commit is local; no push was
requested or performed.

## 2026-11-26 UTC — Codex — GitHub issue and Project coordination

**Commit subject:** `docs: align agent workflow with GitHub issues and milestones`

**Issue references:** `Refs #5, #7`. This is a follow-up to closed tracking issue
#5, and documents that capture deletion in `5558231` supports still-open #7.
Neither reference claims completion of outstanding physical calibration.

**What:** Added live issue/Project checks before work and each logical commit to
`AGENTS.md`, including acceptance criteria, comments, status, priority,
dependencies, assignees and official sprint. Documented task branches, issue
references, evidence/PR review requirements and access-limit reporting in
`docs/git-setup.md`. Reconciled `docs/agent-context.md` and `docs/roadmap.md` with
GitHub's three official milestones, 3 December review, 11 December submission,
week-of-14-December demo and P1 local MQTT task #17. Renamed the old roadmap's four
stages as implementation increments rather than official sprints. Preserved
historical records and distinguished issue status from unread Project fields.

**Why / decisions:** The user requested alignment with configured GitHub tracking
and installation of gh if necessary. Retrieved all 22 issues via the connector,
reviewed the related issues/acceptance guides, and rechecked #5/#7 and #7 comments
before committing. Issues #7/#8 remain In progress, #1–#6 are closed, and #9–#22
are Todo in the issue metadata snapshot. Issue #6's Done state is not additional
physical evidence for local soil/button uncertainties. Do not close #7 based on
software-only work. Created local branch `docs/github-project-workflow`; earlier
commits were not rewritten. No issue, Project item, assignment or milestone was
changed remotely, and no comment/message was posted.

**CLI setup / access:** gh was absent. The approved system apt installation could
not proceed because sudo required an unavailable interactive password. Downloaded
Debian's gh 2.46.0-3 arm64 package and installed its executable with approved
user-local access at `~/.local/bin/gh`, without changing system packages. The
executable is on PATH and reports version 2.46.0. CLI auth status reports no login;
no existing CLI auth configuration or GitHub environment credential was detected.
The user was asked to authenticate interactively with read:project access. The
GitHub connector supplies issue reads but no Project v2 read operation, and public
web reads of the repository/user Project pages failed. Project URL/owner/number,
custom fields and item status therefore remain unverified; no values were inferred.

**Validation:** `gh --version`, command discovery and issue-view help succeeded;
`gh auth status` correctly reported missing authentication. Connector reads
verified all issue metadata, related criteria/comments, milestone dates, no open
PRs and remote main at `f890da4` during this check. Local commits `ec4679a` and
`5558231` were not on that remote main snapshot. Checked local Markdown file links,
reviewed the documentation diff and ran `git diff --check`, all successfully.
The documented authenticated CLI/Project commands could not be exercised before
login. Application tests were not rerun for this documentation/setup change; no
application code or hardware was touched.

**Limitations / next:** Complete interactive gh login, then identify and read the
actual linked Project, fields and related items; record verified ownership/status
and any mismatches. Check live refs again before publishing, then use the team's
PR review flow with issue references. This documentation commit is local; no
push, PR creation, review or merge was requested or performed.
