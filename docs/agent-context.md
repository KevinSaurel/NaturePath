# Current agent handoff context

Last updated: 12 November 2026 (UTC).

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
monitoring. All required hardware is available according to the user, but exact
models, ports and calibrations remain unconfirmed.

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
- Open-Meteo returned HTTP 200 from the Pi without an API key for Bilbao weather
  and hourly precipitation/probability fields. It is the Lab 5 provider.
- Initial repository, English README and roadmap were pushed and verified against
  `origin/main`. Later agents must recheck live Git state rather than assume it.

Application functionality is still pending: no project sensor acquisition,
classification engine, actuator control, API server, persistence or dashboard has
been implemented. No individual NaturePath sensor or actuator has been validated.

## Decisions to preserve

- Start with Open-Meteo for the academic MVP: no weather account/token is needed.
  The proposal mentions Euskalmet as a possible later source; OpenWeather and
  WeatherAPI are different services. Credit Open-Meteo when displaying its data.
- Do not hard-code example GPIO assignments from the labs.
- Calibrate thresholds using actual observations. ADC voltage percentage is not
  calibrated soil water content; CPU temperature is not ambient temperature.
- Keep acquisition, classification, outputs, storage and HTTP separate. One process
  owns GPIO; HTTP requests/reloaders must not start additional acquisition loops.
- A failed mandatory sensor must not yield `good`; loss of optional weather context
  should be exposed without disabling valid local feedback.
- MQTT/platforms, trained anomaly detection and distributed outdoor nodes are extensions.

## Pending inputs and next implementation step

The user is preparing before coding. Obtain the exact sensor/actuator models and
module-to-port mapping, confirm the monitored location, and arrange physical
calibration observations. The accelerometer needs a fixed orientation/reference.
Follow Sprint 1 of the roadmap: test modules individually, record calibration,
then build real soil-moisture acquisition and a minimal status API. Software
interfaces/test fixtures can be prepared while physical information is collected.
No production thresholds or wiring should be guessed.

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
