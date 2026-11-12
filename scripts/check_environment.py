#!/usr/bin/env python3
"""Diagnóstico sin lecturas de sensores ni activación de GPIO."""
import glob
import importlib.util
import json
import platform
import sqlite3
import sys
from pathlib import Path


def module_available(name):
    try:
        return importlib.util.find_spec(name) is not None
    except (ImportError, ValueError, ModuleNotFoundError):
        return False


def main():
    model_path = Path("/proc/device-tree/model")
    model = model_path.read_text().rstrip("\x00\n") if model_path.exists() else None
    report = {
        "python": platform.python_version(),
        "python_supported": sys.version_info >= (3, 11),
        "executable": sys.executable,
        "virtual_environment": sys.prefix != sys.base_prefix,
        "architecture": platform.machine(),
        "raspberry_model": model,
        "sqlite": sqlite3.sqlite_version,
        "modules_discoverable": {
            name: module_available(name)
            for name in ("flask", "grove", "smbus2", "lgpio")
        },
        "visible_devices": {
            "i2c": sorted(glob.glob("/dev/i2c*")),
            "gpio": sorted(glob.glob("/dev/gpiochip*")),
        },
        "hardware_readings_verified": False,
        "note": "Diagnóstico de entorno; no valida conexión, sensores ni calibración.",
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["python_supported"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
