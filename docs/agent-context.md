# Current agent handoff context

Last updated: 26 November 2026 (UTC).

The user resumed preparation on 19 November, initially with modules disconnected;
a port map and local visual calibration tool are now implemented. See the
[19 November session record](sessions/2026-11-19.md) for this work. The previous
[session summary](sessions/2026-11-12.md) is historical, not a current stop request.

## Project and accepted scope

NaturePath is a University of Deusto IoT group project (2026–2027) by Hugo Arenaza,
Kevin Saurel and Ruben Alonso. It provides inclusive trail-condition guidance via
sensing, analysis and physical feedback. It is not a safety/accessibility guarantee.

The user confirmed: implement the complete MVP first and scale only if needed.
The supplied assessment text concerns the proposal and permits a local server;
it does not establish MQTT, cloud platforms or Edge AI as mandatory MVP features.
Its October dates are proposal dates. The implementation deadline is not confirmed.

Target: Raspberry Pi 5 + Grove sensors + Python + Flask + SQLite; LCD, LED, buzzer
and a visitor button. The experimental index uses `good`, `caution`, `poor` and
`unavailable`. Keep the primary visitor experience physical; the dashboard is for
monitoring. All required hardware is available according to the user. The reported
board labels/revisions are now recorded in `docs/hardware.md`; connections,
chip identification where inferred and calibration remain unverified. Later that
day, real readings and user-observed output checks were obtained as noted below.

## Repository and reference material

- Local repository: `/home/hugokevinruben/NaturePath`.
- GitHub: https://github.com/KevinSaurel/NaturePath; HTTPS remote, branch `main`.
- Account used for successful pushes: `hugoArenaza-deusto` (different from owner).
- Original proposal: `docs/challengeIoT_groupXX-1.pdf`; searchable text in `docs/challenge.md`.
- Lab archive: `~/IoT_labs_y_proyecto_contexto.zip`; Labs 1, 3, 4, 5, 6 and proposal.
  No separate Lab 2 handout is present. Nested repositories were not imported.
- Existing lab setup: `~/lab4`, `~/lab5`, `~/grove.py`, `~/grove_env`.
- Active plan: [roadmap.md](roadmap.md); the earlier backlog is retained as history.
- Required commit records: [agent-log.md](agent-log.md), following root `AGENTS.md`.

Do not upload the raw lab archive or a verbatim chat transcript. Teaching materials
and conversation may contain credentials; document only relevant project context.

## Verified state

- Pi 5 Model B Rev 1.0, aarch64, Python 3.13.5.
- `~/grove_env` contains the Grove setup and Flask 3.1.3.
- `~/grove_env/bin/python ~/lab4/check_setup.py` passed on 12 November 2026:
  Pi 5 GPIO backend available, HAT ADC responds at `0x08`, installed Grove default matches.
- The project environment diagnostic runs with system Python and `grove_env`.
- Calibration software: 13 unit/integration tests pass without hardware. System
  Chromium/Playwright completed simulated start/stop, two water captures, reference
  calculation, simulated output and desktop/mobile checks without JavaScript errors.
  These results establish software behaviour, not real sensor compatibility.
- Open-Meteo returned HTTP 200 from the Pi without an API key for Bilbao weather
  and hourly precipitation/probability fields. It is the Lab 5 provider.
- Initial repository, English README and roadmap were pushed and verified against
  `origin/main`. Later agents must recheck live Git state rather than assume it.

The local calibration tool is now implemented in `naturepath.calibration`, with
lazy hardware adapters, raw readings, labelled batches, partial/reference profiles,
CSV/JSON exports and bounded actuator tests. The isolated project `.venv` contains
Flask, smbus2 and the optional Adafruit DHT driver; the lab venv was not modified.
Use `bash scripts/run_calibration.sh` and the Pi browser at `http://127.0.0.1:5050`.
It starts disarmed until the page's start action. `--simulate` is explicit and
stores data separately. See [calibration.md](calibration.md).

On 19 November the user connected the modules and authorised manual API checks.
I2C scanning detected `0x08`, `0x3E` and `0x4C`. Real accelerometer, ambient and water
channel readings arrived. Soil A0 stayed at raw 0 / 0 mV; wet/dry response is still
unverified. The user confirmed LCD text, buzzer, button LED and LED bar physically.
The button input was read as unpressed but a press transition was not observed.
Ambient readings arrived with intermittent DHT failures. No real calibration
references or complete profiles were produced.

The initial acquisition hang and HTTP 400 on stop were traced to Blinka's interactive
optional-dependency prompt during the DHT import. The driver now sets
`BLINKA_SKIP_DEPENDENCY_CHECK=1` internally before that import; no user `.env` is
required. Stop responds 200 when complete or 202 while a read is finishing, with
an explicit frontend stopping state. Fifteen tests passed on 19 November, including
two regressions; real browser start/stop/restart also passed. These corrections
were left uncommitted at the interruption and documented/committed on 24 November.

On 26 November the user requested deletion of saved calibration records. Each
capture now has a **Borrar** action with confirmation, available after acquisition
fully stops. The token-protected API removes the selected capture from disk,
state and future exports in its own mode. If the saved profile uses that capture,
the whole profile is removed and must be rebuilt explicitly; unrelated captures
and profiles are preserved. Existing downloaded exports are unchanged. Twenty
automated tests pass, including deletion, restart, exports, profile invalidation,
mode isolation, running/stopping guards and file-error handling. A Chromium check
with temporary simulated data passed capture, disabled deletion while running,
cancel/confirm, final-row removal, profile/status clearing, export, reload and mobile
width checks without JavaScript errors. No physical hardware activity was performed
for this change.

The user explicitly stopped testing on 19 November. Acquisition was confirmed
stopped then, with the page still served. Do not resume physical tests until the
user requests it. No hardware activity was performed for the 24 November question.
The final trail classifier, monitoring/history API, weather integration and
systemd MVP services remain pending. The calibration API is not the final MVP API.

## Decisions to preserve

- Start with Open-Meteo for the academic MVP: no weather account/token is needed.
  The proposal mentions Euskalmet as a possible later source; OpenWeather and
  WeatherAPI are different services. Credit Open-Meteo when displaying its data.
- Use the confirmed LED bar v2.1 as the main visual indicator; the Red LED Button
  v1.0 supplies the visitor button and an acknowledgement LED. Both need two
  digital signals; check the complete HAT pin map before assigning ports.
- Manufacturer family docs suggest DHT11 for the ambient sensor and MMA7660FC
  for the ±1.5g accelerometer; these are expected identities, not physical chip tests.
- Do not hard-code example GPIO assignments from the labs.
- Calibrate thresholds using actual observations. ADC voltage percentage is not
  calibrated soil water content; CPU temperature is not ambient temperature.
- Keep acquisition, classification, outputs, storage and HTTP separate. One process
  owns GPIO; HTTP requests/reloaders must not start additional acquisition loops.
- A failed mandatory sensor must not yield `good`; loss of optional weather context
  should be exposed without disabling valid local feedback.
- MQTT/platforms, trained anomaly detection and distributed outdoor nodes are extensions.

## Pending inputs and next implementation step

The user later confirmed all modules were connected. Assigned map: moisture A0, water
A2, expected DHT11 D5, buzzer D16, LED bar D22 (data 22/clock 23), red LED button
D24 (LED 24/input 25), LCD and accelerometer on separate shared-bus I2C sockets.
Initial wiring and tests are recorded above. Any later rewiring requires power off.

When the user resumes tests: verify soil response and button input, then collect soil
references (dry/damp/wet), water references (dry/wet), and an immobile level vector
plus known-angle checks. Confirm ambient chip identity and timing reliability.
The tool rejects overlapping reference ranges and keeps captures/errors explicit.
Confirm monitored location and implementation deadline when available. Real
physical evidence is required before treating a profile as validated.

## Operational history and limitations

Early sessions were isolated: DNS, system devices and sudo were restricted. Full
access later exposed real hardware and network access; these initial restrictions
are historical, not current evidence that I2C or networking is broken.
The GitHub connector previously rejected writes with 403; HTTPS Git pushes worked.
Access policies and credentials may change; verify them when needed.

GitHub credentials were disclosed in the conversation. They must never be copied
into this repository. The user was advised to revoke them; revocation is unverified.
Authentication was supplied transiently without adding credentials to Git config.

Keyboard setup is a separate unresolved support issue: `raspi-config` applied
Spanish (`es`) to system and labwc configuration and keyboard-setup was active,
but the user reported that the keyboard still behaved incorrectly. Do not claim
that issue is resolved; physical keyboard versus VNC/SSH access was not clarified.
