# Backlog inicial

Plan extraído del apartado 11 del challenge. Reparto entre integrantes pendiente.

## Sprint 1 · Hardware y sensores

- [ ] Confirmar modelo de HAT, sensor y conexiones físicas.
- [ ] Verificar GPIO e I²C desde una terminal con acceso a dispositivos.
- [ ] Confirmar dirección ADC (0x04 o 0x08) y canal de humedad.
- [ ] Leer el sensor, registrar valores brutos y calibrar en varias condiciones.
- [ ] Definir unidad, frecuencia y umbrales iniciales a partir de los ensayos.
- [ ] Inventariar sensores opcionales disponibles.

Hecho cuando hay lecturas reales repetibles y tabla de calibración documentada.

## Sprint 2 · Procesamiento e indicadores

- [ ] Implementar clasificación pura y probar límites y fallos.
- [ ] Añadir estado `unavailable` y tratamiento de datos caducados.
- [ ] Integrar LCD, LED, buzzer y botón con pines verificados.
- [ ] Demostrar transiciones de estado y recuperación de errores.

Hecho cuando los indicadores corresponden al resultado de las lecturas reales.

## Sprint 3 · Datos y comunicación

- [ ] Persistir mediciones con timestamp UTC en SQLite.
- [ ] Desarrollar rutas REST del contrato y probar respuestas JSON.
- [ ] Desarrollar dashboard con estado actual e historial.
- [ ] Separar adquisición de las peticiones HTTP.
- [ ] Explorar meteorología y MQTT si sobra tiempo.

Hecho cuando la API y el dashboard muestran lecturas reales y conservan el histórico.

## Sprint 4 · Integración y evaluación

- [ ] Probar cadena completa, desconexión de sensor y reinicio.
- [ ] Validar umbrales experimentalmente y documentar limitaciones.
- [ ] Evaluar comprensión con 10–15 participantes.
- [ ] Preparar demostración, instrucciones reproducibles y documentación final.

Hecho cuando se verifican los criterios R1–R9 de requirements.md.
