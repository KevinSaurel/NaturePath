# Raspberry y hardware

## Observado durante la preparación

- Raspberry Pi 5 Model B Rev 1.0; arquitectura `aarch64`.
- Python 3.13.5 y Git 2.47.3.
- Entorno de laboratorio `~/grove_env` con Flask 3.1.3, Grove y smbus2 detectables por Python.
- Código existente en `~/lab4`, `~/lab5` y `~/grove.py`, conservado sin modificaciones.
- Los dispositivos `/dev/i2c*` y `/dev/gpiochip*` no son visibles en esta sesión.
  Esto no demuestra que I²C esté desactivado en el sistema anfitrión; puede deberse
  al aislamiento de la terminal. Falta comprobar desde una terminal física de la Pi.

## Cableado por confirmar

| Componente | Puerto / dirección | Estado |
| --- | --- | --- |
| HAT Grove | I²C; comprobar 0x04 / 0x08 | Modelo exacto y dirección pendientes |
| Humedad del suelo | Canal analógico por confirmar | Prioridad del sprint 1 |
| LCD | Modelo y dirección por confirmar | Pendiente |
| LED | Tipo y GPIO por confirmar | Pendiente |
| Buzzer | Tipo y GPIO por confirmar | Pendiente |
| Botón | GPIO por confirmar | Pendiente |
| Sensores opcionales | Según disponibilidad | No requeridos para arrancar |

No inferir pines del proyecto a partir de los ejemplos de laboratorio.
Conectar físicamente con la alimentación desconectada.

## Configuración

El README del laboratorio indica `rpi-lgpio` para Pi 5 y un entorno con
`--system-site-packages`. La biblioteca Grove se instala aparte; su setup puede
intentar instalar dependencias GPIO incompatibles. Revisar `~/lab4/README.md`
antes de instalarla. No se ha reinstalado ni parcheado ninguna biblioteca.

Confirmar dirección ADC real antes de configurar el adaptador del proyecto.
No modificar globalmente `grove/adc.py` para el proyecto: preferir una dirección
explícita si la API instalada lo permite.

Primero ejecutar `python scripts/check_environment.py`; las pruebas de lectura,
calibración y actuadores se harán cuando se confirme el cableado.
