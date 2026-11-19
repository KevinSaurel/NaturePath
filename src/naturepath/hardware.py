"""Explicit, lazy hardware access for the agreed Grove Base HAT wiring."""
import math
import random
import time

WIRING = {
    'moisture': {'port': 'A0', 'channel': 0},
    'water': {'port': 'A2', 'channel': 2},
    'environment': {'port': 'D5', 'gpio': 5},
    'buzzer': {'port': 'D16', 'gpio': 16},
    'led_bar': {'port': 'D22', 'data': 22, 'clock': 23},
    'button': {'port': 'D24', 'led': 24, 'input': 25},
    'lcd': {'port': 'I2C', 'address': 0x3E},
    'accelerometer': {'port': 'I2C', 'address': 0x4C},
}


def tilt_degrees(vector, reference=(0, 0, 1)):
    length = math.sqrt(sum(x*x for x in vector))
    ref_length = math.sqrt(sum(x*x for x in reference))
    if not 0.5 < length < 1.5 or ref_length < 0.1:
        raise ValueError('Keep the accelerometer stationary; gravity magnitude is invalid')
    cosine = sum(a*b for a, b in zip(vector, reference)) / (length*ref_length)
    return math.degrees(math.acos(max(-1, min(1, cosine))))


def signed_axis(value):
    if value & 0x40:
        raise ValueError('Accelerometer ALERT bit set; retry required')
    value &= 0x3F
    return value - 64 if value & 0x20 else value


class Hardware:
    """Construct only on explicit user start; no automatic output pulses."""
    mode = 'hardware'

    def __init__(self):
        from smbus2 import SMBus
        self.bus = SMBus(1)
        self.gpio = None
        self.claimed = set()
        self.accel_ready = False
        self.dht = None
        self.env_last = 0
        self.env_result = None
        self.reference = (0, 0, 1)

    def _gpio(self):
        if self.gpio is None:
            import RPi.GPIO as GPIO
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            self.gpio = GPIO
        return self.gpio

    def _output(self, pin):
        g = self._gpio()
        if pin not in self.claimed:
            g.setup(pin, g.OUT, initial=g.LOW)
            self.claimed.add(pin)
        return g

    def _adc(self, channel):
        def read(register):
            self.bus.write_byte(0x08, register)
            return self.bus.read_word_data(0x08, register)
        raw, mv = read(0x10 + channel), read(0x20 + channel)
        if not 0 <= raw <= 4095 or not 0 <= mv <= 3600:
            raise ValueError('ADC response outside expected range')
        return {'raw': raw, 'millivolts': mv}

    def _accel(self):
        address = WIRING['accelerometer']['address']
        if not self.accel_ready:
            self.bus.write_byte_data(address, 0x07, 0)  # standby for configuration
            self.bus.write_byte_data(address, 0x08, 2)  # 32 samples/s
            self.bus.write_byte_data(address, 0x07, 1)
            time.sleep(0.05)
            self.accel_ready = True
        for attempt in range(5):
            values = self.bus.read_i2c_block_data(address, 0, 3)
            if not any(x & 0x40 for x in values):
                axes = [signed_axis(x) / 21.33 for x in values]
                return {'x_g': axes[0], 'y_g': axes[1], 'z_g': axes[2],
                        'tilt_deg': tilt_degrees(axes, self.reference)}
            time.sleep(0.01)
        raise ValueError('Accelerometer did not produce a stable valid register read')

    def _environment(self):
        # DHT measurements are slow and must not be polled at the ADC frequency.
        if time.monotonic() - self.env_last < 3:
            if self.env_result:
                return self.env_result
            raise RuntimeError('DHT11 unavailable; waiting before the next read attempt')
        self.env_last = time.monotonic()
        if self.dht is None:
            import adafruit_dht
            import board
            self.dht = adafruit_dht.DHT11(board.D5, use_pulseio=False)
        temperature, humidity = self.dht.temperature, self.dht.humidity
        if temperature is None or humidity is None:
            raise ValueError('DHT11 returned no measurement')
        if not 0 <= temperature <= 50 or not 0 <= humidity <= 100:
            raise ValueError('Ambient reading outside expected DHT11 range')
        self.env_result = {'temperature_c': temperature, 'humidity_pct': humidity,
                           'measured_at': time.time()}
        return self.env_result

    def _button(self):
        g = self._gpio()
        pin = WIRING['button']['input']
        if pin not in self.claimed:
            g.setup(pin, g.IN, pull_up_down=g.PUD_UP)
            self.claimed.add(pin)
        return {'pressed': not bool(g.input(pin))}

    def read(self):
        result = {}
        readers = {'moisture': lambda: self._adc(0), 'water': lambda: self._adc(2),
                   'accelerometer': self._accel, 'environment': self._environment,
                   'button': self._button}
        for name, reader in readers.items():
            try:
                result[name] = {'ok': True, **reader()}
            except Exception as exc:
                if name == 'accelerometer':
                    self.accel_ready = False
                if name == 'environment':
                    self.env_result = None
                result[name] = {'ok': False, 'error': f'{type(exc).__name__}: {exc}'}
        return result

    def _bar(self, mask):
        """MY9221 serial frame: command, twelve channels, four-pulse latch."""
        g = self._output(22)
        self._output(23)
        level = False
        words = [0] + [255 if mask & (1 << i) else 0 for i in range(12)]
        for word in words:
            for bit in range(15, -1, -1):
                g.output(22, bool(word & (1 << bit)))
                g.output(23, level)
                level = not level
        g.output(22, False)
        g.output(23, True)
        g.output(23, False)
        g.output(23, True)
        g.output(23, False)
        time.sleep(0.0003)
        for _ in range(4):
            g.output(22, True)
            g.output(22, False)
        g.output(23, True)
        g.output(23, False)

    def test_output(self, name):
        if name in ('buzzer', 'button_led'):
            pin = 16 if name == 'buzzer' else 24
            g = self._output(pin)
            try:
                g.output(pin, True)
                time.sleep(0.15 if name == 'buzzer' else 0.8)
            finally:
                g.output(pin, False)
        elif name == 'led_bar':
            try:
                for mask in (1, 2, 0x3FC):
                    self._bar(mask)
                    time.sleep(0.6)
            finally:
                self._bar(0)
        elif name == 'lcd':
            address = WIRING['lcd']['address']
            for command in (0x02, 0x0C, 0x28, 0x01):
                self.bus.write_byte_data(address, 0x80, command)
                time.sleep(0.1)
            for command, message in ((0x80, 'NaturePath'), (0xC0, 'LCD test OK?')):
                self.bus.write_byte_data(address, 0x80, command)
                for char in message:
                    self.bus.write_byte_data(address, 0x40, ord(char))
        else:
            raise ValueError('Unknown actuator')

    def close(self):
        errors = []
        if self.dht:
            try:
                self.dht.exit()
            except Exception as exc:
                errors.append(str(exc))
        if self.gpio:
            for pin in (16, 24, 22, 23):
                if pin in self.claimed:
                    try:
                        self.gpio.output(pin, False)
                    except Exception as exc:
                        errors.append(str(exc))
            if self.claimed:
                try:
                    self.gpio.cleanup(list(self.claimed))
                except Exception as exc:
                    errors.append(str(exc))
        try:
            self.bus.close()
        except Exception as exc:
            errors.append(str(exc))
        if errors:
            raise RuntimeError('; '.join(errors))


class SimulatedHardware:
    """Only selected by the explicit --simulate CLI flag. Never a fallback."""
    mode = 'simulation'

    def __init__(self):
        self.reference = (0, 0, 1)
        self.levels = {'moisture': 1600, 'water': 3500, 'angle': 0}

    def read(self):
        result = {name: {'ok': True, 'raw': round(self.levels[name] + random.uniform(-8, 8)),
                         'millivolts': round(self.levels[name] * 3300 / 4095)}
                  for name in ('moisture', 'water')}
        angle = math.radians(self.levels['angle'])
        vector = (math.sin(angle), 0, math.cos(angle))
        result['accelerometer'] = {'ok': True, 'x_g': vector[0], 'y_g': 0,
                                  'z_g': vector[2], 'tilt_deg': tilt_degrees(vector, self.reference)}
        result['environment'] = {'ok': True, 'temperature_c': 22, 'humidity_pct': 55,
                                 'measured_at': time.time()}
        result['button'] = {'ok': True, 'pressed': False}
        return result

    def test_output(self, name):
        time.sleep(0.05)

    def close(self):
        pass
