# NaturePath

Sistema IoT de monitorización de condiciones de senderos para facilitar el acceso a la naturaleza.
Proyecto grupal de IoT 2026–2027 · Universidad de Deusto.

**Equipo:** Hugo Arenaza, Kevin Saurel y Ruben Alonso.

## Estado

Repositorio preparado para empezar el desarrollo. El MVP todavía no está implementado.
El documento propone Raspberry Pi 5, sensores Grove, Python, Flask y SQLite.
La clasificación experimental será `good`, `caution`, `poor` y `unavailable` ante fallos.
Es orientación ambiental, sin garantía de seguridad ni accesibilidad del sendero.

## Empezar en esta Raspberry

```bash
cd ~/NaturePath
python3 scripts/check_environment.py
# Entorno de laboratorio existente, con Flask y Grove instalados:
~/grove_env/bin/python scripts/check_environment.py
```

El diagnóstico no lee sensores ni activa salidas. La detección de módulos no valida el cableado.
No hay servidor ni lectura automática de hardware en esta preparación.

Para un entorno propio (requiere acceso a la red):

```bash
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Grove se configura aparte según [hardware](docs/hardware.md). No instalar el antiguo
`RPi.GPIO` en Pi 5. No es necesario modificar el entorno compartido `~/grove_env`.

## Estructura

- `docs/challengeIoT_groupXX-1.pdf`: documento original con las figuras.
- `docs/challenge.md`: extracción de texto para consulta y búsquedas.
- `docs/requirements.md`: alcance y criterios de aceptación.
- `docs/architecture.md`: propuesta de módulos y contrato HTTP inicial.
- `docs/backlog.md`: los cuatro sprints y sus comprobaciones.
- `docs/hardware.md`: inventario y comprobaciones pendientes.
- `docs/git-setup.md`: conexión Git y bloqueo de publicación observado.
- `src/naturepath/`: código del proyecto; paquete vacío como punto de partida.
- `scripts/`: herramientas de diagnóstico.
- `tests/`: futuras pruebas del índice, persistencia y API.
- `data/`: bases de datos locales, excluidas de Git.

## Trabajo en equipo

```bash
git switch -c feat/nombre-tarea
# Editar y comprobar los cambios
git add ruta/al/archivo
git commit -m "feat: describir cambio"
git push -u origin feat/nombre-tarea
```

Crear una pull request hacia `main` y pedir revisión a otro integrante. No subir
credenciales, entornos virtuales, bases de datos ni datos simulados como mediciones reales.
Antes de empezar una tarea, actualizar con `git pull --ff-only` cuando el acceso funcione.
