# Conexión con GitHub

- Repositorio: https://github.com/KevinSaurel/NaturePath
- Directorio local: `/home/hugokevinruben/NaturePath`
- Rama inicial: `main`
- Remoto `origin`: `https://github.com/KevinSaurel/NaturePath.git`

## Diagnóstico del primer intento (antes de habilitar acceso completo)

El remoto estaba vacío. Se preparó un commit local; aquel primer intento de
publicación quedó bloqueado por las restricciones descritas abajo.

Bloqueos verificados:

1. SSH falla con `Bad owner or permissions on
   /etc/ssh/ssh_config.d/20-systemd-ssh-proxy.conf` antes de autenticar.
2. El intento HTTPS desde esta terminal falla con `Could not resolve host: github.com`.
3. El conector GitHub permite leer el repositorio, pero crear README devuelve
   HTTP 403 `Resource not accessible by integration`, aunque los metadatos del
   repositorio indiquen permiso push. No se creó ningún archivo remoto.

No se modificaron permisos del sistema, claves SSH ni credenciales.

## Publicar por HTTPS

Desde una terminal de la Raspberry con red y autenticación GitHub operativas:

```bash
cd ~/NaturePath
git remote -v
git status
git ls-remote origin
# Si otro integrante ya ha publicado, revisar e integrar su historial primero.
# Si el remoto continúa vacío:
git push -u origin main
```

El remoto utiliza HTTPS. Al solicitar credenciales, usar el usuario propietario
del token (en este equipo, `hugoArenaza-deusto`) y el token como contraseña.
Esa cuenta debe tener permiso de escritura en el repositorio.
Para evitar guardar credenciales al publicar:

```bash
git -c credential.helper= push -u origin main
```

No hacer force push. Nunca guardar tokens o claves en archivos versionados.
