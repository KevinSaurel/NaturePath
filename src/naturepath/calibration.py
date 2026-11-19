"""Local visual calibration workbench. Run: python -m naturepath.calibration."""
import argparse
import atexit
import copy
import csv
import fcntl
import io
import json
import math
import os
import queue
import secrets
import statistics
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, render_template, request, Response
from .hardware import Hardware, SimulatedHardware, WIRING

LABELS = {'moisture': ('dry', 'damp', 'wet'), 'water': ('dry', 'wet'),
          'accelerometer': ('level', 'angle'), 'environment': ('observation',)}
FIELDS = {'moisture': ('raw', 'millivolts'), 'water': ('raw', 'millivolts'),
          'accelerometer': ('x_g', 'y_g', 'z_g', 'tilt_deg'),
          'environment': ('temperature_c', 'humidity_pct')}
OUTPUTS = ('buzzer', 'button_led', 'led_bar', 'lcd')


def utc():
    return datetime.now(timezone.utc).isoformat()


def atomic_json(path, value):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')
    os.replace(temporary, path)


def summarise(samples, fields):
    summary = {}
    for field in fields:
        values = [row[field] for row in samples]
        if not values or not all(math.isfinite(v) for v in values):
            raise ValueError('Invalid samples; capture was not saved')
        summary[field] = {'mean': statistics.mean(values), 'median': statistics.median(values),
                          'min': min(values), 'max': max(values),
                          'std': statistics.pstdev(values)}
    return summary


def build_profile(records, mode):
    """Derive experimental cutoffs only from separated observed reference ranges."""
    profile = {'created_at': utc(), 'mode': mode, 'wiring': WIRING,
               'purpose': 'Experimental references; not a validated trail safety index',
               'sensors': {}, 'pending': []}
    for sensor, labels in [('moisture', ('dry', 'damp', 'wet')), ('water', ('dry', 'wet'))]:
        selected = []
        for label in labels:
            matches = [r for r in records if r['sensor'] == sensor and r['label'] == label
                       and r['mode'] == mode and r['wiring'] == WIRING]
            if not matches:
                break
            selected.append(matches[-1])
        if len(selected) != len(labels):
            profile['pending'].append(f'{sensor}: missing labelled references')
            continue
        ranges = [r['summary']['raw'] for r in selected]
        increasing = all(a['max'] < b['min'] for a, b in zip(ranges, ranges[1:]))
        decreasing = all(a['min'] > b['max'] for a, b in zip(ranges, ranges[1:]))
        if not (increasing or decreasing):
            profile['pending'].append(f'{sensor}: reference ranges overlap or are out of order; repeat captures')
            continue
        boundaries = [(a['max'] + b['min'])/2 if increasing else (a['min'] + b['max'])/2
                      for a, b in zip(ranges, ranges[1:])]
        profile['sensors'][sensor] = {'labels': list(labels), 'raw_increases_with_wetness': increasing,
                                      'boundaries_raw': boundaries,
                                      'capture_ids': [r['id'] for r in selected]}
    levels = [r for r in records if r['sensor'] == 'accelerometer' and r['label'] == 'level'
              and r['mode'] == mode and r['wiring'] == WIRING]
    if levels:
        record = levels[-1]
        if max(record['summary'][axis]['std'] for axis in ('x_g', 'y_g', 'z_g')) > 0.05:
            profile['pending'].append('accelerometer: reference moved; repeat level capture')
        else:
            vector = [record['summary'][axis]['mean'] for axis in ('x_g', 'y_g', 'z_g')]
            if not 0.8 < math.sqrt(sum(v*v for v in vector)) < 1.2:
                profile['pending'].append('accelerometer: reference magnitude is not close to 1 g')
            else:
                profile['sensors']['accelerometer'] = {'reference_g': vector, 'capture_id': record['id'],
                                                       'note': 'Zero reference only; validate with known angles'}
    else:
        profile['pending'].append('accelerometer: missing level reference')
    return profile


class Workbench:
    def __init__(self, directory, simulate=False, factory=None, interval=0.5):
        self.mode = 'simulation' if simulate else 'hardware'
        self.directory = Path(directory) / self.mode
        self.directory.mkdir(parents=True, exist_ok=True)
        self.factory = factory or (SimulatedHardware if simulate else Hardware)
        self.interval = interval
        self.lock = threading.RLock()
        self.stop_event = threading.Event()
        self.thread = None
        self.commands = queue.Queue()
        self.device = None
        self.latest = {}
        self.latest_at = None
        self.running = False
        self.error = None
        self.capture = None
        self.last_action = None
        self.profile = None
        self.records = []
        self.history = []
        for path in sorted(self.directory.glob('capture-*.json')):
            try:
                record = json.loads(path.read_text())
                if record['mode'] == self.mode and record['wiring'] == WIRING:
                    self.records.append(record)
            except (OSError, ValueError, KeyError):
                continue
        self.records.sort(key=lambda r: r['created_at'])
        profile_path = self.directory / 'profile.json'
        if profile_path.exists():
            try:
                profile = json.loads(profile_path.read_text())
                if profile['mode'] == self.mode and profile['wiring'] == WIRING:
                    self.profile = profile
            except (OSError, ValueError, KeyError):
                pass

    def start(self):
        with self.lock:
            if self.thread and self.thread.is_alive():
                raise ValueError('Acquisition is already running or stopping')
            self.stop_event.clear()
            self.running = True
            self.error = None
            self.latest = {}
            self.latest_at = None
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()

    def stop(self):
        self.stop_event.set()
        if self.thread:
            self.thread.join(timeout=8)
        if self.thread and self.thread.is_alive():
            raise ValueError('Still stopping; wait for the active hardware operation to finish')

    def _run(self):
        lockfile = None
        try:
            # Prevent two copies of this tool from owning the same physical hardware.
            if self.mode == 'hardware':
                lockfile = (self.directory.parent / '.hardware.lock').open('a')
                fcntl.flock(lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.device = self.factory()
            if self.profile and 'accelerometer' in self.profile['sensors']:
                self.device.reference = self.profile['sensors']['accelerometer']['reference_g']
            while not self.stop_event.is_set():
                try:
                    command = self.commands.get_nowait()
                except queue.Empty:
                    command = None
                if command:
                    name, value = command
                    try:
                        if name == 'output':
                            self.device.test_output(value)
                        elif name == 'reference':
                            self.device.reference = value
                        elif name == 'levels':
                            self.device.levels.update(value)
                        with self.lock:
                            self.last_action = {'ok': True, 'name': name, 'value': value, 'at': utc()}
                    except Exception as exc:
                        with self.lock:
                            self.last_action = {'ok': False, 'name': name, 'error': str(exc), 'at': utc()}
                readings = self.device.read()
                now = time.time()
                with self.lock:
                    self.latest, self.latest_at = readings, now
                    self.history.append({'at': now, 'moisture': readings.get('moisture', {}).get('raw'),
                                         'water': readings.get('water', {}).get('raw')})
                    self.history = self.history[-120:]
                    self._capture_sample(readings, now)
                self.stop_event.wait(self.interval)
        except Exception as exc:
            with self.lock:
                self.error = f'{type(exc).__name__}: {exc}'
        finally:
            try:
                if self.device:
                    self.device.close()
            except Exception as exc:
                with self.lock:
                    self.error = f'Cleanup failed: {exc}'
            if lockfile:
                lockfile.close()
            with self.lock:
                self.device = None
                self.running = False
                if self.capture and self.capture['state'] == 'collecting':
                    self.capture.update(state='failed', error='Acquisition stopped before capture completed')
                while not self.commands.empty():
                    self.commands.get_nowait()

    def _capture_sample(self, readings, now):
        job = self.capture
        if not job or job['state'] != 'collecting':
            return
        sensor = readings[job['sensor']]
        if not sensor['ok']:
            job.update(state='failed', error=sensor['error'])
            return
        measured_at = sensor.get('measured_at', now)
        if job['samples'] and measured_at <= job['samples'][-1]['timestamp']:
            return  # cached DHT sample is not a new observation
        job['samples'].append({'timestamp': measured_at,
                               **{f: sensor[f] for f in FIELDS[job['sensor']]}})
        if len(job['samples']) < job['target']:
            return
        summary = summarise(job['samples'], FIELDS[job['sensor']])
        record = {k: job[k] for k in ('id', 'sensor', 'label', 'notes', 'known_angle', 'created_at', 'samples')}
        record.update(mode=self.mode, wiring=WIRING, summary=summary)
        atomic_json(self.directory / f"capture-{record['id']}.json", record)
        self.records.append(record)
        job.update(state='complete', summary=summary)

    def begin_capture(self, sensor=None, label=None, target=20, notes='', known_angle=None):
        with self.lock:
            if not self.running or self.latest_at is None or time.time()-self.latest_at > 4:
                raise ValueError('Start acquisition and wait for fresh readings first')
            if not isinstance(sensor, str) or sensor not in LABELS or not isinstance(label, str) or label not in LABELS[sensor]:
                raise ValueError('Invalid sensor or reference label')
            if type(target) is not int or not 10 <= target <= 120:
                raise ValueError('Capture size must be an integer between 10 and 120')
            if not isinstance(notes, str) or len(notes) > 1000:
                raise ValueError('Notes must contain at most 1000 characters')
            if sensor == 'accelerometer' and label == 'angle':
                if isinstance(known_angle, bool) or not isinstance(known_angle, (float, int)) or not 0 < known_angle <= 90:
                    raise ValueError('Enter a known reference angle between 0 and 90 degrees')
            elif known_angle is not None:
                raise ValueError('Known angle is only used for an angle-check capture')
            if not self.latest.get(sensor, {}).get('ok'):
                raise ValueError('This sensor is unavailable; resolve the error before capturing')
            if self.capture and self.capture['state'] == 'collecting':
                raise ValueError('A capture is already in progress')
            self.capture = {'id': uuid.uuid4().hex, 'sensor': sensor, 'label': label,
                            'target': target, 'notes': notes, 'known_angle': known_angle,
                            'created_at': utc(), 'samples': [], 'state': 'collecting'}

    def cancel_capture(self):
        with self.lock:
            if self.capture and self.capture['state'] == 'collecting':
                self.capture.update(state='cancelled')

    def enqueue(self, name, value):
        with self.lock:
            if not self.running or self.latest_at is None or time.time() - self.latest_at > 4:
                raise ValueError('Start acquisition and wait for fresh readings first')
            if self.capture and self.capture['state'] == 'collecting':
                raise ValueError('Finish or cancel the capture before testing outputs or changing references')
            if not self.commands.empty():
                raise ValueError('An operation is already waiting; retry shortly')
            self.commands.put((name, value))

    def save_profile(self):
        with self.lock:
            if self.capture and self.capture['state'] == 'collecting':
                raise ValueError('Finish the current capture first')
            result = build_profile(self.records, self.mode)
            if self.running and 'accelerometer' in result['sensors']:
                self.enqueue('reference', result['sensors']['accelerometer']['reference_g'])
            atomic_json(self.directory / 'profile.json', result)
            self.profile = result
            return result

    def state(self):
        with self.lock:
            capture = None if not self.capture else {k: v for k, v in self.capture.items() if k != 'samples'}
            if capture:
                capture['collected'] = len(self.capture['samples'])
            return copy.deepcopy({'mode': self.mode, 'running': self.running, 'error': self.error,
                                  'readings': self.latest, 'latest_at': self.latest_at,
                                  'capture': capture, 'last_action': self.last_action, 'profile': self.profile,
                                  'history': self.history,
                                  'records': [{k: v for k, v in r.items() if k != 'samples'} for r in self.records]})


def create_app(workbench):
    app = Flask(__name__)
    token = secrets.token_urlsafe(32)
    app.config['MAX_CONTENT_LENGTH'] = 8192

    @app.before_request
    def protect_mutations():
        if request.method == 'POST' and not secrets.compare_digest(request.headers.get('X-NaturePath-Token', ''), token):
            return jsonify(error='Open the local workbench page before sending commands'), 403

    @app.after_request
    def headers(response):
        response.headers['Cache-Control'] = 'no-store'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self'; frame-ancestors 'none'; base-uri 'none'"
        return response

    @app.errorhandler(ValueError)
    def invalid(exc):
        return jsonify(error=str(exc)), 400

    @app.get('/')
    def index():
        return render_template('calibration.html', token=token, mode=workbench.mode)

    @app.get('/api/state')
    def state():
        return jsonify({**workbench.state(), 'wiring': WIRING})

    @app.post('/api/start')
    def start():
        workbench.start()
        return jsonify(ok=True)

    @app.post('/api/stop')
    def stop():
        workbench.stop()
        return jsonify(ok=True)

    @app.post('/api/capture')
    def capture():
        data = request.get_json()
        if not isinstance(data, dict) or set(data)-{'sensor', 'label', 'target', 'notes', 'known_angle'}:
            raise ValueError('Invalid capture request')
        workbench.begin_capture(**data)
        return jsonify(ok=True)

    @app.post('/api/cancel')
    def cancel():
        workbench.cancel_capture()
        return jsonify(ok=True)

    @app.post('/api/profile')
    def profile():
        return jsonify(workbench.save_profile())

    @app.post('/api/output/<name>')
    def output(name):
        if name not in OUTPUTS:
            raise ValueError('Unknown actuator')
        workbench.enqueue('output', name)
        return jsonify(ok=True)

    @app.post('/api/simulation')
    def simulation():
        if workbench.mode != 'simulation':
            raise ValueError('Simulation controls are disabled in hardware mode')
        data = request.get_json()
        if not isinstance(data, dict) or not data or set(data)-{'moisture', 'water', 'angle'}:
            raise ValueError('Invalid simulation settings')
        for key, value in data.items():
            limit = 90 if key == 'angle' else 4095
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= limit:
                raise ValueError('Simulation value outside allowed range')
        workbench.enqueue('levels', data)
        return jsonify(ok=True)

    @app.get('/api/export')
    def export():
        with workbench.lock:
            records = copy.deepcopy(workbench.records)
        if request.args.get('format') == 'csv':
            stream = io.StringIO()
            columns = ['capture_id', 'mode', 'sensor', 'label', 'known_angle', 'timestamp',
                       'raw', 'millivolts', 'x_g', 'y_g', 'z_g', 'tilt_deg', 'temperature_c', 'humidity_pct']
            writer = csv.DictWriter(stream, fieldnames=columns)
            writer.writeheader()
            for record in records:
                for sample in record['samples']:
                    writer.writerow({'capture_id': record['id'], 'mode': record['mode'],
                                     **{k: record[k] for k in ('sensor', 'label', 'known_angle')}, **sample})
            return Response(stream.getvalue(), mimetype='text/csv',
                            headers={'Content-Disposition': 'attachment; filename=naturepath-captures.csv'})
        return Response(json.dumps({'mode': workbench.mode, 'records': records}, indent=2),
                        mimetype='application/json',
                        headers={'Content-Disposition': 'attachment; filename=naturepath-captures.json'})

    return app


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--simulate', action='store_true', help='Explicit demo without hardware access')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=5050)
    parser.add_argument('--data-dir', default='data/calibration')
    args = parser.parse_args()
    bench = Workbench(args.data_dir, simulate=args.simulate)
    atexit.register(bench.stop)
    print(f'NaturePath {bench.mode}: http://{args.host}:{args.port} — acquisition starts only from the page', flush=True)
    try:
        create_app(bench).run(host=args.host, port=args.port, threaded=True, use_reloader=False)
    finally:
        bench.stop()


if __name__ == '__main__':
    main()
