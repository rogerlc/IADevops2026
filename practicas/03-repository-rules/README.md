# Práctica 3: Reglas del repositorio

## Objetivo

Configurar un flujo de colaboración que proteja la rama `main`, automatice las
validaciones repetibles y mantenga una aprobación humana antes de fusionar cada
Pull Request.

## Validaciones automáticas

El workflow `Repository Quality` ejecuta cuatro checks en los Pull Requests hacia
`main`:

- `Secret Scan`: usa Gitleaks para detectar llaves, tokens, credenciales y
  contraseñas de base de datos dentro del historial propuesto.
- `Conventional Commits`: valida el título del Pull Request y todos sus commits.
- `Tests`: ejecuta las pruebas del validador y del MCP Server.
- `Code Quality`: ejecuta Ruff sobre el código Python.

Los colaboradores no necesitan instalar Gitleaks. El análisis se ejecuta de
forma centralizada en GitHub Actions. Si detecta un secreto, el Pull Request no
puede fusionarse.

Los archivos `.env`, llaves privadas y almacenes de certificados están
excluidos mediante `.gitignore`. El archivo `.env.example` documenta únicamente
variables con valores ficticios. Las credenciales reales deben almacenarse en
GitHub Secrets o en el gestor de secretos aprobado por la empresa.

> `Secret Scan` ocurre después de subir una rama. Por ello bloquea el merge,
> pero no garantiza que una contraseña genérica nunca llegue temporalmente a
> una rama remota. Una credencial real expuesta debe revocarse o rotarse
> inmediatamente.

Los mensajes deben seguir este formato:

```text
tipo(alcance opcional): descripción
```

Tipos permitidos:

- `feat`
- `fix`
- `docs`
- `style`
- `refactor`
- `test`
- `build`
- `ci`
- `chore`
- `perf`
- `revert`

La automatización verifica la estructura. La persona responsable de la revisión
confirma que el tipo elegido corresponda realmente al cambio.

## Reglas previstas para `main`

El Ruleset requerirá:

- Cambios mediante Pull Request.
- Una aprobación humana.
- Nueva aprobación cuando se agreguen cambios después de aprobar.
- Resolución de todas las conversaciones.
- Los cuatro checks automáticos aprobados, incluido `Secret Scan`.
- Bloqueo de force push y eliminación de `main`.
- Aplicación sin bypass para administradores.

El repositorio utilizará únicamente Squash merge. Auto-merge permanecerá
desactivado para conservar la revisión humana antes de cada fusión.

## Estado de implementación

El workflow y el Ruleset `main-protection` están activos. Para completar el
flujo, al menos un colaborador autorizado debe aceptar su invitación y aprobar
el Pull Request, ya que una persona no puede aprobar su propio cambio.
