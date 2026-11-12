# Conexión con GitHub

- Repositorio: https://github.com/KevinSaurel/NaturePath
- Directorio local: `/home/hugokevinruben/NaturePath`
- Rama inicial: `main`
- Remoto `origin`: `git@github.com:KevinSaurel/NaturePath.git`

## Estado observado al preparar

El remoto estaba vacío. La copia local está inicializada y tiene su commit base.
**No se ha publicado ni sincronizado el commit con GitHub.**

Bloqueos verificados:

1. SSH falla con `Bad owner or permissions on
   /etc/ssh/ssh_config.d/20-systemd-ssh-proxy.conf` antes de autenticar.
2. El intento HTTPS desde esta terminal falla con `Could not resolve host: github.com`.
3. El conector GitHub permite leer el repositorio, pero crear README devuelve
   HTTP 403 `Resource not accessible by integration`, aunque los metadatos del
   repositorio indiquen permiso push. No se creó ningún archivo remoto.

No se modificaron permisos del sistema, claves SSH ni credenciales.

## Publicar cuando haya acceso

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

Resolver la configuración SSH y disponer de una clave autorizada para usar la URL
actual. Alternativamente, cambiar a HTTPS con autenticación disponible en esa terminal:

```bash
git remote set-url origin https://github.com/KevinSaurel/NaturePath.git
git push -u origin main
```

No hacer force push. Nunca guardar tokens o claves en archivos versionados.
