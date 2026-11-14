# VID-C06 — Subidas y rutas no confiables

**SCAFFOLD RECOVERY / NOT_STARTED.** [Campaña delta original](../../campaigns/06-subidas-y-rutas-no-confiables.md) · [Factory](../../factory/00-README.md) · [Flow](../../factory/01-PIPELINE.md) · [ADTC](../../factory/03-TRACE-OBSERVABILITY.md).

## Objetivo
Cerrar delta verificable de subidas y rutas no confiables desde código y evidencias existentes sin reimplementar capacidades válidas.

## Dependencias
VID-C05

## Tareas pendientes
- VID-C06-T01: Congelar SHA y verificar código; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C06-T02: Reconciliar evidencias históricas con HEAD; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C06-T03: Especificar delta y superficies de escritura; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C06-T04: Definir contratos y permisos con padre; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C06-T05: Diseñar pruebas positivas y negativas; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C06-T06: Recopilar evidencias y rollback; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C06-T07: Gate Codex/arquitecto y founder; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.

## Gates sin ejecutar
- VID-C06-G01: Tenant ajeno o permiso ausente bloquea acceso/efecto.
- VID-C06-G02: Fallo o estado incierto evita duplicados y permite rollback.

Rollback: Deshabilitar capacidad nueva, preservar datos/evidencias y conciliar efectos externos.

Tras Astra y reconciliación: sustituir este scaffold por patchsets, pruebas y handoffs de campaña. No reescribir funcionalidad existente sin delta probado.
