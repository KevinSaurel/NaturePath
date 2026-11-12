# NaturePath implementation roadmap

Planning baseline: 12 November 2026. Build the complete MVP first; extend it only
when there is a demonstrated need. This roadmap supersedes the initial task list
in [backlog.md](backlog.md).

## Outcome and scope

A visitor presses a button at a trail entrance and receives understandable local
feedback about environmental conditions through an LCD, LED and buzzer. The Pi
collects real readings, computes an experimental condition index, stores history
and serves a local HTTP API and monitoring dashboard.

The product must help people decide whether to spend time outdoors without
requiring a smartphone. The dashboard supports monitoring and maintenance; the
physical indicator is the main visitor interface.

The team reports that all sensors and actuators are available. Plan to integrate
soil moisture, water detection, ambient temperature/humidity and an accelerometer,
plus the LCD, LED, buzzer and button. Exact models and connections still need to
be recorded before selecting drivers. Having hardware available does not mean it
has been connected, calibrated or verified.

The submitted proposal's minimum acceptance criteria remain the baseline. Water,
ambient sensing and inclination extend the original moisture-first MVP using the
hardware now available. Open-Meteo adds forecast context. LoRaWAN, solar power,
multi-node infrastructure, cloud platforms, MQTT and learned anomaly detectors
are later extensions, unless a new implementation rubric explicitly requires them.

## What has actually been verified

- Repository scaffold and proposal are on GitHub; application implementation is pending.
- Raspberry Pi 5, Python 3.13.5 and the existing `~/grove_env` are available.
- The Lab 4 `check_setup.py` passes: Grove imports, the Pi 5 GPIO backend is
  available, the HAT answers at `0x08`, and the installed ADC default matches it.
- Open-Meteo returns HTTP 200 without authentication for Bilbao coordinates,
  including current conditions and hourly precipitation/probability fields.
- Individual project sensors, their wiring, LCD and other actuators have not yet
  been tested as part of NaturePath.

## Alignment with the labs

Source archive: `~/IoT_labs_y_proyecto_contexto.zip`. Teaching materials were
reviewed locally; the archive and its nested Git repository are not copied into
this project. No separate Lab 2 handout is present in the archive.

| Source | Reuse in NaturePath | Adaptation |
| --- | --- | --- |
| Lab 1 and references to Lab 2 | Pi setup, network identity, SSH/VNC | Keep the working Pi installation; verify access from the demo laptop |
| Lab 3, sections 4–6 | Scheduling, logs, GPIO and button debounce | Use systemd for long-running services; use confirmed GPIO assignments |
| Lab 4, sections 2–3, pp. 2–5 | Pi 5 environment, ADC address, one-module tests | Keep the working `0x08` setup and test actual project modules |
| Lab 4, section 4, pp. 5–6 | Flask, JSON, LAN binding and HTTP codes | Implement the proposal's routes; serve acquired readings rather than reading hardware per request |
| Lab 5, sections 1.3–1.4, pp. 3–4 | `weather.py`, `requests`, a single hardware access layer | Use Open-Meteo and a shared sensor adapter; retain timestamps, units and per-sensor quality |
| Lab 5, sections 3.3–3.4, pp. 10–11 | Historical panels, network recovery, systemd | Start with Flask + SQLite; platform publishers are optional adapters |
| Lab 6, sections 1–5, pp. 3–6 | Recording, fault labels, temporal windows and evaluation | Basic validity/freshness checks first; train models only after real data exists |

The Lab 5 flat numeric payload is useful for telemetry platforms. The main project
API also needs metadata such as node ID, UTC timestamps, units, classification
reasons and sensor availability. An eventual publisher can flatten this richer
record without changing the hardware layer.

## Delivery order

The four sprints are ordered increments, not calendar commitments. Confirm the
implementation deadline before assigning dates; the supplied October dates refer
to the proposal and its presentation, not a newly established prototype deadline.

### Sprint 1 — Real sensing and the first complete software path

1. Record exact models, port labels, I2C addresses and button polarity in
   [hardware.md](hardware.md). Distinguish BCM GPIO numbers from physical header pins.
2. Stop any old lab scripts that own project pins. Verify one module at a time
   using the Lab 4 pattern, with a bounded test and output cleanup.
3. Create configuration for channels, pins, I2C addresses, sampling intervals,
   node identity and calibration. Do not hard-code lab example ports.
4. Implement the hardware adapter with timestamped readings, raw values, units
   and explicit errors. Start with soil moisture, then add water, ambient sensing
   and the actual accelerometer driver.
5. Record dry, damp and wet reference readings. Keep raw ADC readings; ADC voltage
   percentage is not calibrated soil water content.
6. Build the first vertical slice: real moisture → provisional configurable
   classification → `GET /api/moisture` and `GET /api/status` JSON.
7. Add a clearly identified simulated adapter for repeatable software tests when
   physical modules are unavailable. Never switch to simulation silently.

**Done:** a laptop can retrieve real moisture and status from the Pi, each installed
sensor has a recorded individual test, and invalid mandatory data yields
`unavailable`. Thresholds remain explicitly provisional until validated.

**Human input needed:** models and wiring, physical module tests and calibration samples.
**Coding work:** configuration, adapters, sample model, initial rules and minimal API.

### Sprint 2 — Condition analysis and visitor feedback

1. Add calibrated moisture and water rules, ambient context and inclination.
   Decide how combined conditions escalate the result using measured scenarios.
2. Calibrate the accelerometer at a known reference angle and install it in a
   fixed orientation representing the monitored surface. Document that a loose
   or handheld module does not measure the trail's slope.
3. Separate environmental condition (`good`, `caution`, `poor`, `unavailable`)
   from sensor quality and degraded context. A missing forecast must not erase
   a valid local reading; a failed mandatory sensor must not produce `good`.
4. Include reasons for each classification. Add hysteresis or a short persistence
   rule to avoid flickering around a threshold. Validate boundary transitions.
5. Implement LCD text, the actual LED type, short buzzer patterns and button
   debounce. Make status understandable without relying on colour alone.
6. Ensure bounded buzzer duration and release resources on shutdown. Avoid
   blocking sensor acquisition while showing messages or playing feedback.

**Done:** pressing the button presents the latest measured condition physically;
controlled dry/wet/water/inclined scenarios produce explainable results, including
sensor failure and recovery. No final numeric threshold is invented without data.

**Human input needed:** mounting/reference angles, calibration observations and confirmation
that LCD text, LED and buzzer are understandable.
**Coding work:** sensor fusion, decision reasons, stability rules and actuator control.

### Sprint 3 — Persistence, weather and monitoring

1. Store measurements, condition, quality, reasons, UTC timestamps and calibration
   version in SQLite. Define bounded retention and CSV export for evidence.
2. Finish the proposed REST routes: `/api/moisture`, `/api/water`,
   `/api/environment`, `/api/inclination`, `/api/status` and `/api/all`.
   Add a bounded history query and health endpoint for monitoring.
3. Define schemas and HTTP errors consistently, including unsupported routes,
   unavailable data and invalid history parameters. Use JSON `null` for missing
   values rather than presenting fabricated zeros as measurements.
4. Query Open-Meteo using configured coordinates. Cache forecasts, set a timeout,
   back off after failure and expose source, update time and freshness.
5. Keep outdoor forecast estimates distinct from local ambient measurements.
   Add rainfall context only through explicit, testable rules.
6. Implement a local Flask dashboard with current status/reasons, latest readings,
   a history chart and hardware/weather freshness. Include Open-Meteo attribution.
   The dashboard must continue showing stored/local data when Internet fails.

**Done:** SQLite survives restart, the API agrees with the physical indicator,
and a laptop on the LAN can inspect the current condition and historical readings.
A weather timeout does not block local sensing or indicators.

**Human input needed:** monitored location/coordinates and access to a second device on the LAN.
**Coding work:** storage, REST contract, weather client/cache and dashboard.

### Sprint 4 — Autonomous operation, validation and demonstration

1. Package reproducible installation and configuration instructions for this Pi.
2. Run acquisition and web serving under systemd with the correct venv, working
   directory, logs and restart policy. Use a suitable WSGI server for the deployed
   API; do not rely on the Flask development reloader.
3. Give one acquisition process ownership of GPIO. Web workers must not start
   extra sensor loops. Verify SQLite access across the service boundaries.
4. Test reboot, process failure, stale readings, unavailable weather and temporary
   network loss. Demonstrate sensor failures through controlled software error
   injection; do not unplug powered Grove modules to create a failure.
5. Record a continuous run of at least 30 minutes as an engineering target inspired
   by Lab 5. Keep readings, logs, API examples and screenshots as evidence.
6. Validate the full loop against the proposal's acceptance criteria and document
   calibration limits. Compare observed readings and displayed results.
7. Run the proposed 10–15-person comprehension/usefulness check if feasible:
   target 80% correct interpretation and 70% positive feedback.
8. Prepare a short demonstration: ordinary conditions → changed moisture/water
   or inclination → physical feedback → matching API/history → failure handling.

**Done:** the system starts without a developer terminal, recovers from failures,
and demonstrates sensing → analysis → physical action → HTTP/history.

**Human input needed:** physical scenarios, reboot/demo supervision and participant feedback.
**Coding work:** deployment units, recovery behaviour, meaningful automated tests and documentation.

## Weather: no token required for the proposed integration

The Lab 5 example uses **Open-Meteo**, not OpenWeather or WeatherAPI. The challenge
mentions **Euskalmet** as a possible open-data source; that is a different provider.
Start with Open-Meteo for the academic MVP, matching the lab. Add Euskalmet later
if local-data requirements justify the extra integration.

Official references checked on 12 November 2026:

- [Open-Meteo documentation](https://open-meteo.com/en/docs)
- [Free API and pricing](https://open-meteo.com/en/pricing): non-commercial free API,
  no account/API key required; confirm applicable limits before deployment.
- [Data attribution](https://open-meteo.com/en/licence): credit Open-Meteo in the dashboard/report.

A proposed starting schedule is local sampling every 5 seconds and weather fetching
every 15 minutes (96 fetches/day for one location). Confirm each sensor's supported
read rate before using this schedule. Do not call the weather service per sensor
sample or browser request. Forecast data is context, not ground truth at the trail.

## Tasks for the team before and during coding

| Task | What to provide | Why it matters |
| --- | --- | --- |
| Inventory | Exact model/revision of moisture, water, ambient sensor, accelerometer, LCD, LED and buzzer | Driver/protocol compatibility, especially DHT variants on Pi 5 |
| Wiring | Module → labelled Grove port; BCM GPIO/channel and I2C address where known | Prevents driver and pin conflicts; lab ports are examples |
| Mounting | How the accelerometer is fixed and its zero/reference angle | Makes inclination meaningful |
| Calibration | Raw readings in dry/damp/wet soil, water absent/present and known angles | Enables defensible thresholds and transition tests |
| Location | One monitored location and coordinates; confirm Bilbao defaults if suitable | Ensures the forecast represents the intended area |
| Network/demo | Pi and laptop on a reachable LAN and a stable power supply | Allows HTTP demonstration and reboot tests |
| UX validation | Check LCD messages, button response and LED/buzzer patterns with users | Validates the nature-first, inclusive value proposition |
| Delivery | Confirm final implementation deadline and any additional prototype rubric | Sets dates and determines whether extensions are necessary |

No weather account, cloud subscription or extra hardware purchase is needed to
start. The team performs physical wiring and observations; software work can begin
with explicit interfaces and test fixtures while those inputs are collected.
An initial three-person task split can follow hardware/calibration, rules/feedback,
and API/storage/weather, with cross-review and joint integration. Agree owners at
sprint planning rather than assuming roles from names.

## Architecture that supports later extensions

```text
Grove drivers → acquisition → validated sample → classification → LCD / LED / buzzer
                     ↑                              ↑  ↓
                  config         cached Open-Meteo ──┘  SQLite → Flask API → dashboard
```

Interfaces should let storage and publishers consume the same validated readings.
Keep sensor access, classification and transport separate without introducing a
cloud dependency into the local feedback loop.

After MVP acceptance, consider these independently:

1. **MQTT:** publish measurements and health from an adapter; use a local broker
   for campus demonstrations. Lab 5 warns that outbound MQTT ports can be blocked
   on campus, so test the actual network rather than assuming cloud connectivity.
2. **Platform:** add one of InfluxDB/Grafana, ThingsBoard or ThingSpeak if needed;
   do not deploy all three. Accounts/tokens are needed only for the chosen path.
3. **Edge health detection:** reuse Lab 6 recording, training and evaluation with
   actual project data. A stable moisture value is not automatically a frozen
   sensor, and naturally wet soil is not a sensor fault. Keep device health separate
   from trail condition. Never present CPU temperature as ambient temperature.
4. **Distributed outdoor nodes:** investigate microcontrollers, LoRaWAN, power,
   enclosures and coverage after the local data model and use case are validated.

## Acceptance gate

- [ ] Real, calibrated readings from the installed project sensors.
- [ ] Explainable condition index and `unavailable` handling.
- [ ] LCD, LED, buzzer and button verified physically.
- [ ] HTTP JSON routes accessible from another device.
- [ ] SQLite history and a monitoring dashboard with current and past values.
- [ ] Weather provenance, cache and graceful loss of external context.
- [ ] Autonomous startup and controlled failure/recovery demonstration.
- [ ] Evidence, known limitations and visitor comprehension documented.

These gates establish an end-to-end MVP. Additional lab deliverables and proposal
presentation requirements remain separate unless the teacher explicitly combines them.
