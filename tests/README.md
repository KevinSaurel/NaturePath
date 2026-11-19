# Verification

Run the current calibration checks without physical hardware:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

`test_calibration.py` covers reference polarity and overlapping ranges, moving
accelerometer references, resource cleanup after failure, capture persistence,
separation of simulation/hardware records and profiles, cancellation, unavailable
hardware, invalid HTTP input and cached ambient observation counting.

Browser QA on 19 November 2026 used system Chromium through Playwright with the
explicit simulation mode: start/stop, dry/wet water captures, profile calculation,
a simulated actuator command and desktop/mobile rendering. The API tests
separately verified CSV/JSON exports.
Playwright was installed only in the project venv as a QA tool; it is not a runtime
dependency. No browser download was needed. All simulated evidence stayed outside
tracked project data.

Physical driver/module tests and real calibration remain pending. Future MVP
checks will cover classification boundaries, SQLite persistence, history/REST
responses, integration of actual indicators and restart/network recovery.
