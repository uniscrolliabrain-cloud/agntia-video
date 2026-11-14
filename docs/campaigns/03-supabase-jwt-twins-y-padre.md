# VID-C03 — Supabase JWT, twins y padre

**RECOVERY_DELTA / PLANNED / NOT_EXECUTED.** Cerrar delta verificable de supabase jwt, twins y padre desde código y evidencias existentes sin reimplementar capacidades válidas.

Fuentes: `README.md`, `AGENTS.md`, `docs/architecture.md`, `docs/typescript-agents.md`, `.github/workflows/test.yml`. Dependencias: VID-C02. [Factory](../factory/00-README.md), [flow](../factory/01-PIPELINE.md), [baseline](../prep/README.md).

## Tareas previstas
- VID-C03-T01: Congelar SHA y verificar código. Aceptación: Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C03-T02: Reconciliar evidencias históricas con HEAD. Aceptación: Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C03-T03: Especificar delta y superficies de escritura. Aceptación: Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C03-T04: Definir contratos y permisos con padre. Aceptación: Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C03-T05: Diseñar pruebas positivas y negativas. Aceptación: Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C03-T06: Recopilar evidencias y rollback. Aceptación: Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C03-T07: Gate Codex/arquitecto y founder. Aceptación: Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.

## Gates no ejecutados
- VID-C03-G01: Tenant ajeno o permiso ausente bloquea acceso/efecto.
- VID-C03-G02: Fallo o estado incierto evita duplicados y permite rollback.

Rollback: Deshabilitar capacidad nueva, preservar datos/evidencias y conciliar efectos externos.

Tras meta-auditoría libre Astra y reconciliación: concretar patchsets, ownership, pruebas y handoffs por campaña. No fingir que el código actual no existe ni declarar PASS por este documento.
