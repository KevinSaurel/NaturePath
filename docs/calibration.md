# Local visual calibration workbench

This is a preparation tool, not the finished NaturePath monitoring service.
It reads the agreed hardware map, records labelled batches, exports evidence and
builds experimental reference cutoffs. The Spanish interface is designed for the
team operating the Pi. Documentation remains in English.

## Wiring plan

Power off and disconnect Pi power before attaching or moving Grove cables.
These are the printed **Grove port labels**, not physical header pin numbers.
The plan is software-configured; the user's actual connections remain unverified.

| Module | Grove port | Signal assignment |
| --- | --- | --- |
| Moisture v1.4 | **A0** | ADC channel 0 |
| Water v1.1 | **A2** | ADC channel 2 |
| Temperature/humidity v1.2, expected DHT11 | **D5** | BCM 5 |
| Buzzer v1.2 | **D16** | BCM 16 |
| LED Bar v2.1 | **D22** | Data BCM 22; clock BCM 23 |
| Red LED Button v1.0 | **D24** | LED BCM 24; active-low button BCM 25 |
| White-on-blue 16x2 LCD v2.0 | **Any I2C socket** | Bus 1; expected address `0x3E` |
| ±1.5g accelerometer v1.3, expected MMA7660FC | **Another I2C socket** | Bus 1; expected address `0x4C` |

The HAT's analog converter is at `0x08`, verified previously. Its three I2C
connectors share one bus. The assigned GPIO sets are disjoint; D22 and D24 each
reserve both signal wires. Leave other connectors unused for this tool. This map
applies to the full Grove Base HAT with D5/D16/D18/D22/D24/D26 and A0/A2/A4/A6;
if your labels differ, stop and identify the board before wiring.

Manufacturer references:

- [HAT connector map](https://wiki.seeedstudio.com/Grove_Base_Hat_for_Raspberry_Pi/)
- [LED button signals](https://wiki.seeedstudio.com/Grove-LED_Button/)
- [LED bar protocol reference](https://github.com/Seeed-Studio/Grove_LED_Bar)
- [MMA7660 reference](https://wiki.seeedstudio.com/Grove-3-Axis_Digital_Accelerometer-1.5g/)

## Install and launch

The project `.venv` was created on this Pi without modifying `~/grove_env`.
To reproduce it on a compatible Pi 5 lab setup:

```bash
cd ~/NaturePath
python3 -m venv --system-site-packages .venv
.venv/bin/python -m pip install -e '.[dht]'
```

The Pi 5 `rpi-lgpio` backend must be installed at system level as in Lab 4;
legacy `RPi.GPIO` must not replace it. Optional `[dht]` installs the Adafruit DHT11
driver; a successful install/import does not prove reliable timing on the sensor.

Start the local tool:

```bash
cd ~/NaturePath
bash scripts/run_calibration.sh
```

Open **http://127.0.0.1:5050** in the Pi browser. To use a second computer on your
trusted laboratory LAN, start with `bash scripts/run_calibration.sh --host 0.0.0.0`
and browse to `http://<PI-IP>:5050`. This is a temporary calibration development
server, not an Internet deployment or the final MVP service.

The page starts disarmed: no sensor access or output activation until **Iniciar
lecturas**. Stop old lab programs first so that they do not own these pins.
Starting acquisition configures the accelerometer, reads the ADC, attempts the
DHT11 and reads the button. Each sensor reports its own error; no synthetic data
is substituted for a failed real sensor. Output tests are explicit page actions.

Use **Detener** before exiting and Ctrl+C to stop the server. Outputs are bounded
and released on normal shutdown. Before moving cables, shut down and remove power.
No systemd service is installed and the tool does not start automatically at boot.

## Runtime configuration

No `.env` file or user-defined environment variables are required by this tool.
Wiring is currently a Python constant and host/port/data directory/simulation are
CLI options. The DHT adapter internally sets `BLINKA_SKIP_DEPENDENCY_CHECK=1`
before importing Blinka-dependent modules to prevent interactive dependency
installation from blocking the worker. The Python `.venv` is a separate concept.

`POST /api/stop` returns 200 when stopped or 202 when shutdown is pending; poll
`/api/state` for `stopping`/`running`. The frontend displays the stopping state.
Refresh the page after a server restart to obtain the new page command token.

## Procedure

### 1. Confirm operation before capturing

- Start readings and check the raw ADC and millivolt values respond to each analog
  sensor. An ADC responding does not prove a sensor is plugged into that channel.
- Check accelerometer axes and tilt change when its orientation changes.
- Check ambient measurements; DHT11 failures appear explicitly. Retrying is spaced
  by at least three seconds, including after a failed attempt.
- Hold the red button long enough to observe the page indicator; the tool polls it
  for validation and does not yet implement the final MVP's event/debounce UX.
- Trigger LCD, LED bar, button LED and buzzer tests separately. The page confirms
  command completion, not physical success: a person must observe the module.
- LED bar test lights the first segment, second segment, then remaining segments;
  confirm which colours those positions represent on the actual unit.

Do not treat zero-like or static readings as evidence of connection or calibration.

### 2. Soil moisture references

Prepare dry, damp and very wet samples using the same soil/substrate. Keep insertion
depth, compaction and placement comparable. Keep the connector/electronics dry.

1. Select soil moisture and **Tierra seca**. Let the signal stabilise.
2. Add notes describing the sample/depth and capture 20 observations (~10 seconds
   without slower hardware errors). Observe the spread as well as the median.
3. Repeat with **Tierra húmeda** and **Tierra muy mojada**.
4. Repeat inconsistent captures instead of forcing numeric boundaries. The latest
   capture for each label is used when building a profile.

The tool records raw ADC and millivolts. These are project references for categories,
not a scientifically calibrated percentage of soil water or a universal trail threshold.
Recalibrate when substrate, placement, sensor or electrical configuration changes.

### 3. Water references

Capture the dry sensing area as **Sin agua**, then water contacting only the
sensing traces as **Agua sobre zona sensible**. Keep the electronics and connector
dry. Record at least 20 new readings per state; the observed polarity determines
which side of the derived cutoff represents water. The tool does not copy the
contradictory example thresholds found in the local Grove water module.

### 4. Accelerometer zero and angle check

Place the sensor immobile on a known level surface in the intended mounting
orientation and capture **Nivelado**. Build/save the profile to apply its mean
gravity vector as the reference. Then use **Comprobar ángulo conocido**, enter a
known angle (for example a measured 15° reference), capture and compare the mean
reported angle and its spread against that reference.

The profile rejects a moving level reference (axis standard deviation >0.05 g)
or mean gravity outside 0.8–1.2 g. Those are provisional quality checks, not a
manufacturer accuracy guarantee. MMA7660 resolution makes this an experimental
estimate. The angle-check capture records evidence; it does not fit an automatic
scale correction. A moving sensor measures acceleration, not just trail slope.

### 5. Ambient sensor and actuators

Ambient captures are **observations**, not automatic calibration. Compare them
with a suitable reference instrument when available. Only new DHT observations
count toward a capture, so 20 readings normally take around a minute.
LCD/LED bar/buzzer/button need functional tests, not numeric calibration.

## Records, profiles and exports

- Captures: `data/calibration/hardware/capture-<id>.json`.
- Experimental references: `data/calibration/hardware/profile.json`.
- Every capture includes UTC metadata, epoch sample times, notes, wiring, mode,
  original readings and mean/median/min/max/population-standard-deviation summaries.
- CSV and JSON downloads include raw observations. Local data stays excluded from Git.
- Soil cutoffs require dry/damp/wet ranges in monotonic order with no overlap;
  water cutoffs require two separated ranges. Increasing and decreasing polarity
  are both supported. Boundaries fall midway between neighbouring observed ranges.
- A partial profile reports missing/overlapping references. It must not be treated
  as complete calibration or used to claim trail safety. Previous complete sensor
  results are replaced by the new profile, so resolve pending references first.
- Saving applies a valid level vector to the current acquisition. Persisted profiles
  are reloaded by the tool on restart; environmental validation remains separate.
- Sensor failure or stop aborts an unfinished capture; no partial batch is saved.
  Cancel similarly discards the in-progress batch. Older completed captures remain.

For review, keep exports and describe the physical procedure/results in the project
documentation. Do not publish fictitious test data as experimental measurements.

## Explicit simulation for software checks

```bash
bash scripts/run_calibration.sh --simulate --port 5051
```

This never constructs the hardware driver. Its banner and exported records say
`simulation`, with separate files under `data/calibration/simulation/`. Sliders
allow dry/wet/angle workflow checks without physical modules. Simulation commands
are rejected in hardware mode. Simulation is never a fallback for hardware errors.

## Verification and remaining limits

```bash
.venv/bin/python -m unittest discover -s tests -v
```

Automated checks cover reference polarity/overlap, persistence, failed/cancelled
captures, fresh observation counting, unavailable hardware and HTTP command guards.
Browser checks use explicitly simulated data. Neither these checks nor installing
the DHT dependency establishes physical compatibility of the reported revisions.
Real wiring, I2C addresses, output colour/order, DHT reliability and calibration
remain to be verified by the team. The final trail classifier, history dashboard,
weather integration and autonomous MVP services are still separate roadmap work.
