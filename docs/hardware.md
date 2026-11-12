# Hardware inventory and validation

Inventory reported by the user on 12 November 2026. Availability and printed board
names are confirmed by the user; individual operation, wiring and calibration are
not yet verified. Board revision numbers alone do not establish driver compatibility.

## Raspberry Pi environment

- Raspberry Pi 5 Model B Rev 1.0, aarch64, Python 3.13.5.
- Existing `~/grove_env`: Grove setup, Flask 3.1.3 and smbus2.
- Existing lab code in `~/lab4`, `~/lab5` and `~/grove.py` is preserved.
- The Lab 4 setup checker passed on 12 November 2026: Pi 5 GPIO backend available,
  Grove HAT ADC at `0x08`, installed Grove ADC default matching `0x08`.
- Earlier missing device nodes were a restriction of the initial isolated session,
  not evidence of a disabled host I2C bus.

## Available modules

| Module as reported | Role in NaturePath | Expected interface / driver direction | Physical validation |
| --- | --- | --- | --- |
| Grove 16x2 LCD (White on Blue) v2.0 | Current condition and short explanations | I2C, documented family address `0x3E`; existing `grove.display.jhd1802.JHD1802` is a candidate | Address, text and contrast pending |
| Grove Temperature and Humidity Sensor v1.2 | Ambient measurements | Reported family matches Seeed's DHT11 documentation; digital timing protocol; confirm sensor marking before fixing the driver | Type, GPIO and valid repeated reads pending |
| Grove Buzzer v1.2 | Brief acoustic feedback | Digital output; confirm bounded on/off behaviour | GPIO and sound test pending |
| Grove Red LED Button v1.0 | Request information; optional acknowledgement LED | Two digital signals; local Grove driver uses LED on slot GPIO and active-low button on the second GPIO (`pin + 1`) | Port, polarity, debounce and LED pending |
| Grove Moisture Sensor v1.4 | Ground moisture input | Analog via HAT ADC; existing Grove moisture module is a candidate | Channel, raw/mV references and calibration pending |
| Grove 3-Axis Digital Accelerometer (±1.5g) v1.3 | Estimate inclination at a fixed monitored point | Documented ±1.5g family uses MMA7660FC over I2C, expected `0x4C`; confirm installed device/revision | Identity, address, axes and reference angles pending |
| Grove LED Bar v2.1 | Main visible trail-condition indicator, replacing a single LED | Documented family uses MY9221 and 10 fixed-colour segments; two digital signals for data/clock | Driver, both GPIOs, segment order and patterns pending |
| Grove Water Sensor v1.1 | Detect water contact/accumulation at the monitored point | Supports analog or digital use; plan HAT analog acquisition for calibration and diagnostics | Channel, electrical compatibility and wet/dry polarity pending |

The LCD is the monochrome white-on-blue variant, not an RGB backlight display.
The LED bar is a segmented indicator, not an individually recolourable RGB strip.
The red LED button supplies the required push button; a separate plain button is
not required for this inventory.

## Driver investigation completed without activating hardware

Inspected the existing Grove checkout under `~/grove.py`:

- `grove/display/jhd1802.py` explicitly lists the white-on-blue 16x2 family and
  defaults to `0x3E`. Its constructor writes to the display; do not instantiate it
  merely to check whether a module imports.
- `grove/grove_ryb_led_button.py` uses two GPIO lines and active-low button input.
- `grove/grove_moisture_sensor.py` returns millivolts through `read_voltage`;
  ADC ratio/voltage is not calibrated soil water content.
- `grove/grove_water_sensor.py` contains contradictory wet/dry example thresholds
  between its documentation and executable example. Establish actual polarity
  and thresholds experimentally rather than copying either example.
- No matching MMA7660, LED bar or DHT implementation file was found in the limited
  local file-name searches performed. This is not proof that no usable package is
  installed. Select and verify Pi 5-compatible drivers before adding dependencies.

Do not install GrovePi code just because an official example imports `grovepi`:
this project has a Grove Base HAT, which is different hardware. Arduino and old
Raspberry Pi examples need adaptation to the actual Pi 5 backend.

## Connection plan: pending physical information

| Module | Grove port label | BCM GPIO(s) / ADC channel | I2C address |
| --- | --- | --- | --- |
| Soil moisture | TBD | ADC channel TBD | HAT ADC `0x08`, verified |
| Water | TBD | ADC channel TBD | Via HAT ADC |
| Temperature/humidity | TBD | GPIO TBD | Not I2C for the expected DHT11 variant |
| Buzzer | TBD | GPIO TBD | — |
| Red LED button | TBD | LED GPIO TBD + button GPIO TBD | — |
| LED bar | TBD | Data GPIO TBD + clock GPIO TBD | — |
| LCD | I2C connector TBD | Shared I2C bus | Expected `0x3E`, unverified |
| Accelerometer | I2C connector TBD | Shared I2C bus | Expected `0x4C`, unverified |

Account for both signal wires on the LED bar and button connector. Do not assume
adjacent port labels represent independent, unused GPIOs: check the HAT pinout.
The LCD and accelerometer can share I2C if their actual addresses do not conflict;
check connector availability and power/signal compatibility before connecting.
Use the documented HAT connections; do not assume 5 V signals are safe on Pi GPIO.
Connect or move modules with Pi power disconnected.

## Proposed visitor feedback (not implemented)

The user selected the LED bar to better represent a future park entrance.
Use explicit segment masks/patterns, not an unlabelled bar level that might suggest
precision the experimental index does not have. Initial proposal:

- `good`: selected green segments and LCD text identifying favourable conditions.
- `caution`: amber/yellow segment and a short explanation on the LCD.
- `poor`: red segment and the relevant environmental reason.
- `unavailable`: a distinct temporal pattern plus an explicit unavailable message;
  avoid presenting darkness alone as a healthy or failed state.
- Button press: show the latest information and briefly acknowledge through its
  integrated red LED, independently of the environmental classification.
- Buzzer: short, bounded patterns rather than continuous sound.

Segment positions, visibility, messages and timing must be tested with the real
bar/LCD. Do not rely on colour alone. Treat the MMA7660-family result as an
experimental inclination estimate after calibration, not a certified slope measure.

## Next validation order

1. Record current connections, or agree a non-conflicting port map before wiring.
2. Test soil moisture and water readings independently; record raw values and units.
3. Verify LCD and accelerometer I2C addresses after connection, then test each.
4. Test the button, integrated LED, buzzer and LED bar individually with cleanup.
5. Verify the ambient sensor type and repeated readings on the Pi 5. Lab 6 warns
   that DHT11 timing can produce missing/checksum-failed readings; handle those
   explicitly rather than substituting weather data as if it came from the sensor.
6. Record soil/water/angle calibration and proceed with Sprint 1 of the roadmap.

No module tests, GPIO activation, driver installation or wiring changes were
performed while recording this inventory.

## Manufacturer references

Checked 12 November 2026; family documentation supports the expected interfaces,
not proof that the reported physical revisions have been electronically identified.

- [Grove 16x2 LCD](https://wiki.seeedstudio.com/Grove-16x2_LCD_Series/)
- [Temperature and humidity / DHT11](https://wiki.seeedstudio.com/Grove-TemperatureAndHumidity_Sensor/)
- [±1.5g accelerometer / MMA7660FC](https://wiki.seeedstudio.com/Grove-3-Axis_Digital_Accelerometer-1.5g/)
- [LED bar / MY9221](https://wiki.seeedstudio.com/Grove-LED_Bar/)
- [LED button](https://wiki.seeedstudio.com/Grove-LED_Button/)
- [Water sensor](https://wiki.seeedstudio.com/Grove-Water_Sensor/)

For Pi 5 installation, retain the lab's compatible GPIO backend and existing
`--system-site-packages` venv. Do not replace it with legacy `RPi.GPIO` packages.
