# Requisitos del MVP

Fuente: `challengeIoT_groupXX-1.pdf`, apartados 1.3, 5, 7 y 11.1.

## Obligatorio

| ID | Requisito | Comprobación pendiente |
| --- | --- | --- |
| R1 | Leer humedad del suelo con Raspberry Pi 5 y Grove | Lecturas reales en varios niveles de humedad |
| R2 | Calcular índice experimental `good`, `caution`, `poor` | Ensayos y umbrales calibrados y documentados |
| R3 | LCD, LED y buzzer comunican la condición | Demostración física; confirmar tipo de LED |
| R4 | Botón permite solicitar información | Pulsación muestra información; definir señal acústica |
| R5 | HTTP/REST devuelve mediciones reales en JSON | Consultas a la Raspberry y comparación con lectura |
| R6 | Dashboard muestra mediciones y estado actual | Verificación con cambios de humedad |
| R7 | Gestionar datos inválidos o ausentes | Sensor desconectado produce `unavailable`, nunca `good` |
| R8 | Demostrar el circuito completo | Sensor → cálculo → indicadores → API/dashboard |
| R9 | Persistencia e histórico SQLite | Consultar lecturas anteriores tras reiniciar |

Los umbrales se determinan experimentalmente: no asumir porcentajes a partir del ADC
ni fijar valores arbitrarios como si estuvieran calibrados. Registrar unidad y valor bruto.

## Ampliaciones

Agua acumulada, temperatura/humedad ambiental, acelerómetro y API meteorológica se
integrarán según disponibilidad y tiempo. Los endpoints opcionales deben comunicar
su ausencia explícitamente. Falta definir su esquema y códigos HTTP.

LoRaWAN, MQTT distribuido, paneles solares, múltiples nodos, Grafana y despliegue
urbano forman parte de la evolución y no condicionan el MVP.

## Privacidad y evaluación

Sin cámaras, micrófonos ni seguimiento de personas. Validación propuesta con 10–15
participantes: al menos 80 % interpreta los indicadores y 70 % da valoración positiva.
El índice orienta sobre condiciones ambientales y no garantiza accesibilidad o seguridad.
