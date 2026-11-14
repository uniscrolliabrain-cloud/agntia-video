# VID-C11 — Anam y voces opt-in

**SCAFFOLD RECOVERY / NOT_STARTED.** [Campaña delta original](../../campaigns/11-anam-y-voces-opt-in.md) · [Factory](../../factory/00-README.md) · [Flow](../../factory/01-PIPELINE.md) · [ADTC](../../factory/03-TRACE-OBSERVABILITY.md).

## Objetivo
Cerrar delta verificable de anam y voces opt-in desde código y evidencias existentes sin reimplementar capacidades válidas.

## Dependencias
VID-C10

## Tareas pendientes
- VID-C11-T01: Congelar SHA y verificar código; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C11-T02: Reconciliar evidencias históricas con HEAD; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C11-T03: Especificar delta y superficies de escritura; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C11-T04: Definir contratos y permisos con padre; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C11-T05: Diseñar pruebas positivas y negativas; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C11-T06: Recopilar evidencias y rollback; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C11-T07: Gate Codex/arquitecto y founder; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.

## Gates sin ejecutar
- VID-C11-G01: Tenant ajeno o permiso ausente bloquea acceso/efecto.
- VID-C11-G02: Fallo o estado incierto evita duplicados y permite rollback.

Rollback: Deshabilitar capacidad nueva, preservar datos/evidencias y conciliar efectos externos.

Tras Astra y reconciliación: sustituir este scaffold por patchsets, pruebas y handoffs de campaña. No reescribir funcionalidad existente sin delta probado.
