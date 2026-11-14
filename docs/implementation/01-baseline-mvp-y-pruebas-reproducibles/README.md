# VID-C01 — Baseline MVP y pruebas reproducibles

**SCAFFOLD RECOVERY / NOT_STARTED.** [Campaña delta original](../../campaigns/01-baseline-mvp-y-pruebas-reproducibles.md) · [Factory](../../factory/00-README.md) · [Flow](../../factory/01-PIPELINE.md) · [ADTC](../../factory/03-TRACE-OBSERVABILITY.md).

## Objetivo
Cerrar delta verificable de baseline mvp y pruebas reproducibles desde código y evidencias existentes sin reimplementar capacidades válidas.

## Dependencias
ninguna

## Tareas pendientes
- VID-C01-T01: Congelar SHA y verificar código; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C01-T02: Reconciliar evidencias históricas con HEAD; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C01-T03: Especificar delta y superficies de escritura; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C01-T04: Definir contratos y permisos con padre; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C01-T05: Diseñar pruebas positivas y negativas; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C01-T06: Recopilar evidencias y rollback; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C01-T07: Gate Codex/arquitecto y founder; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.

## Gates sin ejecutar
- VID-C01-G01: Tenant ajeno o permiso ausente bloquea acceso/efecto.
- VID-C01-G02: Fallo o estado incierto evita duplicados y permite rollback.

Rollback: Deshabilitar capacidad nueva, preservar datos/evidencias y conciliar efectos externos.

Tras Astra y reconciliación: sustituir este scaffold por patchsets, pruebas y handoffs de campaña. No reescribir funcionalidad existente sin delta probado.
