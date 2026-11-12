# Arquitectura prevista

```text
Humedad Grove → adaptador de hardware → adquisición periódica
                                            ↓
                                     índice experimental
                                      ↙            ↘
                          LCD / LED / buzzer       SQLite
                              ↑                     ↓
                            botón              Flask REST
                                                    ↓
                                                dashboard
```

## Separación propuesta

- `sensors`: lectura Grove, validación, unidades y errores de hardware.
- `classification`: reglas puras, umbrales configurables y estado `unavailable`.
- `indicators`: LCD, LED, buzzer y botón; definir los pines tras verificar cableado.
- `storage`: SQLite, lecturas UTC y consultas históricas.
- `collector`: único propietario de la adquisición e indicadores.
- `api`: Flask consulta el último estado persistido y el historial.

Esto es un diseño, no módulos implementados. Evitar que cada petición HTTP lea el
hardware y que el reloader de Flask arranque dos bucles de adquisición.
Los datos antiguos deben marcarse como no disponibles; definir el tiempo máximo de
validez al fijar la frecuencia de muestreo. Un modo simulado deberá identificarse
explícitamente, sin sustituir silenciosamente fallos del hardware.

## Rutas propuestas por el documento

| Ruta GET | Información |
| --- | --- |
| `/api/moisture` | Humedad del suelo |
| `/api/water` | Agua acumulada, opcional |
| `/api/environment` | Temperatura y humedad ambiental, opcional |
| `/api/inclination` | Inclinación, opcional |
| `/api/status` | Clasificación del sendero |
| `/api/all` | Todas las mediciones disponibles |

El JSON de ejemplo del PDF contiene `node_id`, `soil_moisture`, `status` y `timestamp`.
Antes de implementar, concretar esquema, unidades, información de errores y códigos HTTP.
No hay rutas HTTP implementadas en esta preparación.
