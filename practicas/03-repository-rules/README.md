# Práctica 3: Reglas del repositorio

## Objetivo

Configurar un flujo de colaboración que proteja la rama `main`, automatice las
validaciones repetibles y mantenga una aprobación humana antes de fusionar cada
Pull Request.

## Validaciones automáticas

El workflow `Repository Quality` ejecuta tres checks en los Pull Requests hacia
`main`:

- `Conventional Commits`: valida el título del Pull Request y todos sus commits.
- `Tests`: ejecuta las pruebas del validador y del MCP Server.
- `Code Quality`: ejecuta Ruff sobre el código Python.

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
- Los tres checks automáticos aprobados.
- Bloqueo de force push y eliminación de `main`.
- Aplicación sin bypass para administradores.

El repositorio utilizará únicamente Squash merge. Auto-merge permanecerá
desactivado para conservar la revisión humana antes de cada fusión.

## Estado de implementación

El workflow y el Ruleset `main-protection` están activos. Para completar el
flujo, al menos un colaborador autorizado debe aceptar su invitación y aprobar
el Pull Request, ya que una persona no puede aprobar su propio cambio.
