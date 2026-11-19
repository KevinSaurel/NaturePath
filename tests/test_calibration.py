"""Contract, persistence and failure-path checks; never touch physical GPIO."""
import json
import re
import tempfile
import time
import unittest
from pathlib import Path

from naturepath.calibration import Workbench, build_profile, create_app, summarise
from naturepath.hardware import Hardware, SimulatedHardware, WIRING, signed_axis, tilt_degrees
from unittest.mock import Mock


def reference(sensor, label, values, mode='hardware'):
    samples = [{'raw': value} for value in values]
    return {'id': f'{sensor}-{label}', 'sensor': sensor, 'label': label, 'mode': mode,
            'wiring': WIRING, 'summary': summarise(samples, ('raw',))}


class ReferencesTest(unittest.TestCase):
    def test_increasing_and_decreasing_reference_polarity(self):
        for values, increasing in [([100, 1500, 3000], True), ([3500, 2000, 100], False)]:
            records = [reference('moisture', label, [v-4, v, v+4])
                       for label, v in zip(('dry', 'damp', 'wet'), values)]
            records += [reference('water', 'dry', [3400, 3404]), reference('water', 'wet', [100, 110])]
            result = build_profile(records, 'hardware')
            soil = result['sensors']['moisture']
            self.assertEqual(soil['raw_increases_with_wetness'], increasing)
            self.assertEqual(len(soil['boundaries_raw']), 2)
            self.assertFalse(result['sensors']['water']['raw_increases_with_wetness'])

    def test_overlap_inverted_middle_and_simulation_never_accepted(self):
        for middle in ([90, 110], [400, 410]):
            records = [reference('moisture', 'dry', [100, 120]),
                       reference('moisture', 'damp', middle),
                       reference('moisture', 'wet', [300, 310])]
            self.assertNotIn('moisture', build_profile(records, 'hardware')['sensors'])
        records = [reference('water', 'dry', [3500], mode='simulation'),
                   reference('water', 'wet', [100], mode='simulation')]
        self.assertNotIn('water', build_profile(records, 'hardware')['sensors'])

    def test_moving_zero_reference_is_not_applied(self):
        samples = [{'x_g': x, 'y_g': 0, 'z_g': 1, 'tilt_deg': 0} for x in (-0.3, 0.3)]
        record = {'id': 'moving', 'sensor': 'accelerometer', 'label': 'level',
                  'mode': 'hardware', 'wiring': WIRING,
                  'summary': summarise(samples, ('x_g', 'y_g', 'z_g', 'tilt_deg'))}
        result = build_profile([record], 'hardware')
        self.assertNotIn('accelerometer', result['sensors'])
        self.assertTrue(any('moved' in item for item in result['pending']))

    def test_cleanup_continues_after_dht_failure(self):
        device = Hardware.__new__(Hardware)
        device.dht = Mock()
        device.dht.exit.side_effect = RuntimeError('DHT failed during close')
        device.gpio = Mock()
        device.claimed = {16, 24}
        device.bus = Mock()
        with self.assertRaises(RuntimeError):
            device.close()
        device.gpio.output.assert_any_call(16, False)
        device.gpio.output.assert_any_call(24, False)
        device.gpio.cleanup.assert_called_once()
        device.bus.close.assert_called_once()

    def test_accelerometer_signed_values_and_orientation(self):
        self.assertEqual(signed_axis(0x3F), -1)
        self.assertEqual(signed_axis(0x20), -32)
        with self.assertRaises(ValueError):
            signed_axis(0x40)
        self.assertAlmostEqual(tilt_degrees((0, 0, 1)), 0)
        self.assertAlmostEqual(tilt_degrees((1, 0, 0)), 90)
        self.assertAlmostEqual(tilt_degrees((1, 0, 0), (1, 0, 0)), 0)
        with self.assertRaises(ValueError):
            tilt_degrees((0, 0, 0))


class WorkbenchTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.bench = Workbench(self.temp.name, simulate=True, interval=0.005)
        self.app = create_app(self.bench)
        self.client = self.app.test_client()
        html = self.client.get('/').get_data(as_text=True)
        token = re.search('name="naturepath-token" content="([^"]+)"', html).group(1)
        self.headers = {'X-NaturePath-Token': token}

    def tearDown(self):
        self.bench.stop()
        self.temp.cleanup()

    def post(self, path, data=None):
        return self.client.post(path, json=data or {}, headers=self.headers)

    def wait(self, predicate):
        deadline = time.monotonic() + 3
        while time.monotonic() < deadline:
            if predicate():
                return
            time.sleep(0.01)
        self.fail('Timed out waiting for simulated acquisition')

    def start(self):
        self.assertEqual(self.post('/api/start').status_code, 200)
        self.wait(lambda: self.bench.state()['latest_at'] is not None)

    def test_page_is_disarmed_and_commands_require_page_token(self):
        state = self.client.get('/api/state').get_json()
        self.assertFalse(state['running'])
        self.assertEqual(state['readings'], {})
        self.assertEqual(self.client.post('/api/start').status_code, 403)
        self.assertEqual(self.post('/api/capture', {'sensor': 'moisture', 'label': 'dry'}).status_code, 400)
        self.assertEqual(self.post('/api/output/buzzer').status_code, 400)

    def test_capture_persists_and_exports_independent_samples(self):
        self.start()
        result = self.post('/api/capture', {'sensor': 'moisture', 'label': 'dry', 'target': 10})
        self.assertEqual(result.status_code, 200)
        self.wait(lambda: self.bench.state()['capture']['state'] == 'complete')
        record = self.bench.records[0]
        self.assertEqual(len(record['samples']), 10)
        self.assertEqual(record['mode'], 'simulation')
        self.assertEqual(self.client.get('/api/export').get_json()['records'][0]['id'], record['id'])
        csv = self.client.get('/api/export?format=csv').get_data(as_text=True)
        self.assertEqual(len(csv.splitlines()), 11)
        self.bench.stop()
        reloaded = Workbench(self.temp.name, simulate=True)
        self.assertEqual(reloaded.records[0]['id'], record['id'])
        real = Workbench(self.temp.name)
        self.assertEqual(real.records, [])
        self.assertTrue((Path(self.temp.name)/'simulation'/f"capture-{record['id']}.json").exists())

    def test_profile_survives_restart_and_modes_stay_isolated(self):
        self.bench.records = [reference('water', 'dry', [3500, 3510], 'simulation'),
                              reference('water', 'wet', [100, 110], 'simulation')]
        self.bench.save_profile()
        reloaded = Workbench(self.temp.name, simulate=True)
        self.assertIn('water', reloaded.profile['sensors'])
        hardware = Workbench(self.temp.name)
        self.assertIsNone(hardware.profile)

    def test_cancel_and_block_outputs_during_capture(self):
        self.start()
        self.post('/api/capture', {'sensor': 'water', 'label': 'dry', 'target': 120})
        self.assertEqual(self.post('/api/output/buzzer').status_code, 400)
        self.assertEqual(self.post('/api/profile').status_code, 400)
        self.post('/api/cancel')
        self.assertEqual(self.bench.state()['capture']['state'], 'cancelled')
        self.assertEqual(self.bench.records, [])

    def test_invalid_input_is_rejected_without_server_error(self):
        self.start()
        for payload in ({}, {'sensor': [], 'label': 'dry'},
                        {'sensor': 'moisture', 'label': 'dry', 'target': True},
                        {'sensor': 'accelerometer', 'label': 'angle', 'known_angle': -1},
                        {'sensor': 'water', 'label': 'dry', 'extra': 1}):
            response = self.post('/api/capture', payload)
            self.assertEqual(response.status_code, 400, response.get_data(as_text=True))
        self.assertEqual(self.post('/api/simulation', {'water': 99999}).status_code, 400)
        self.assertEqual(self.post('/api/output/unknown').status_code, 400)

    def test_missing_hardware_reports_error_without_simulation_fallback(self):
        def unavailable():
            raise OSError('No I2C bus')
        bench = Workbench(self.temp.name, factory=unavailable)
        bench.start()
        self.wait(lambda: not bench.state()['running'])
        self.assertEqual(bench.state()['mode'], 'hardware')
        self.assertIn('No I2C bus', bench.state()['error'])
        self.assertFalse(bench.state()['readings'])
        bench.stop()

    def test_sensor_failure_aborts_capture_without_saving(self):
        self.start()
        self.bench.begin_capture('moisture', 'dry')
        with self.bench.lock:
            self.bench._capture_sample({'moisture': {'ok': False, 'error': 'sensor failed'}}, time.time())
        self.assertEqual(self.bench.state()['capture']['state'], 'failed')
        self.assertEqual(self.bench.records, [])

    def test_cached_environment_does_not_count_as_fresh_observations(self):
        self.start()
        with self.bench.lock:
            self.bench.begin_capture('environment', 'observation')
            sample = {'environment': {'ok': True, 'temperature_c': 22, 'humidity_pct': 55, 'measured_at': 100}}
            self.bench._capture_sample(sample, 100)
            self.bench._capture_sample(sample, 101)
            self.assertEqual(self.bench.state()['capture']['collected'], 1)
            self.bench.cancel_capture()


if __name__ == '__main__':
    unittest.main()
