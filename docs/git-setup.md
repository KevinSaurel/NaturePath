# Conexión con GitHub

- Repositorio: https://github.com/KevinSaurel/NaturePath
- Directorio local: `/home/hugokevinruben/NaturePath`
- Rama inicial: `main`
- Remoto `origin`: `https://github.com/KevinSaurel/NaturePath.git`

## Current issue and Project workflow

The following workflow supersedes the initial empty-repository publishing example
below. Historical connection failures are not evidence of current access failure.

Before work and before every logical commit, inspect the applicable issue and its
linked Project item: acceptance criteria, discussion, issue state, Project status,
priority, dependencies, assignees and official sprint. Prefer the GitHub connector
for supported reads. Use GitHub CLI for Project fields; verify Project ownership,
number, URL and actual field names instead of assuming they match the repository.
Issue state/status and a Project item's custom status are distinct observations.

GitHub CLI 2.46.0 was installed on this Pi on 26 November 2026 from Debian's arm64
package into `~/.local/bin/gh`, without sudo or changes to system packages. Use the
absolute user path if `gh` is not on the current shell's PATH. CLI authentication
is separate from the connected GitHub app and from Git push authentication.

```bash
~/.local/bin/gh --version
~/.local/bin/gh auth status
# Run interactively when not authenticated; do not paste credentials into chat.
~/.local/bin/gh auth login --web --git-protocol https --scopes read:project
~/.local/bin/gh issue list --repo KevinSaurel/NaturePath --state all --limit 100
~/.local/bin/gh issue view 7 --repo KevinSaurel/NaturePath --comments
~/.local/bin/gh issue view 7 --repo KevinSaurel/NaturePath --json number,title,state,assignees,labels,milestone,projectItems
```

Discover the Project associated with the repository/issue. Once its actual owner
and number are known, use `gh project view`, `gh project field-list` and
`gh project item-list` with that owner and number, and inspect dependency links
through the issue/API. If existing CLI authentication lacks Project read access,
request only the required read scope with `gh auth refresh --scopes read:project`.
Do not request write scopes just to inspect the board. Record missing access
rather than inferring Project field values from an issue state.

Start a task branch from a reviewed current base; inspect local unpublished work
before pulling, rebasing or moving commits. Use the existing team PR review flow.
For example, a partial calibration improvement should include `Refs #7` in its
commit body and PR. It must not use `Closes #7`: real labelled captures and
repeatability evidence remain separate acceptance criteria. Update tracking only
to the extent supported by completed work and evidence. Never invent a review.

Every work commit still needs its immediate agent-log entry and log-only amendment
under [AGENTS.md](../AGENTS.md). Before publishing, check live remote history and
preserve others' work. Do not amend earlier published commits to add issue links;
use a follow-up commit/PR description to document the relationship instead.

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
