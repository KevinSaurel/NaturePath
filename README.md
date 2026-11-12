# NaturePath

An IoT trail condition monitoring system designed to make access to nature more inclusive.
IoT group project 2026–2027 · University of Deusto.

**Team:** Hugo Arenaza, Kevin Saurel, and Ruben Alonso.

## Project status

The repository is ready for development. The MVP has not been implemented yet.
The proposal uses a Raspberry Pi 5, Grove sensors, Python, Flask, and SQLite.
The experimental classification will report `good`, `caution`, or `poor`, with
`unavailable` used when sensor data cannot be trusted or obtained.
The index provides environmental guidance and does not guarantee trail safety or accessibility.

## Getting started on this Raspberry Pi

```bash
cd ~/NaturePath
python3 scripts/check_environment.py
# Existing lab environment with Flask and Grove installed:
~/grove_env/bin/python scripts/check_environment.py
```

The diagnostic does not read sensors or activate outputs. Detecting Python modules
does not validate the wiring. No server or automatic hardware acquisition is included yet.

To create a separate environment (requires network access):

```bash
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Configure Grove separately following the [hardware guide](docs/hardware.md).
Do not install the legacy `RPi.GPIO` package on the Pi 5.
The shared `~/grove_env` environment does not need to be modified.

## Implementation roadmap

See the [MVP roadmap](docs/roadmap.md) for lab alignment, sprint deliverables,
team inputs, weather integration, and later extensions.

## Repository structure

- `docs/challengeIoT_groupXX-1.pdf`: original proposal, including figures.
- `docs/challenge.md`: extracted text for reference and searching.
- `docs/requirements.md`: scope and acceptance criteria.
- `docs/architecture.md`: proposed modules and initial HTTP API contract.
- `docs/backlog.md`: four planned sprints and their completion criteria.
- `docs/hardware.md`: hardware inventory and pending checks.
- `docs/git-setup.md`: Git connection, authentication, and initial setup issues.
- `src/naturepath/`: project source code; currently an empty starter package.
- `scripts/`: environment diagnostic tools.
- `tests/`: planned tests for classification, persistence, and the API.
- `data/`: local databases, excluded from Git.

## Team workflow

```bash
git switch -c feat/task-name
# Edit and check your changes
git add path/to/file
git commit -m "feat: describe change"
git push -u origin feat/task-name
```

Open a pull request targeting `main` and ask another team member to review it.
Keep credentials, virtual environments, and databases out of the repository.
Clearly label simulated data so it cannot be mistaken for real measurements.
Before starting a task, update your branch with `git pull --ff-only`.
