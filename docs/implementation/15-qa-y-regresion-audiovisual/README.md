# VID-C15 — QA y regresión audiovisual

**SCAFFOLD RECOVERY / NOT_STARTED.** [Campaña delta original](../../campaigns/15-qa-y-regresion-audiovisual.md) · [Factory](../../factory/00-README.md) · [Flow](../../factory/01-PIPELINE.md) · [ADTC](../../factory/03-TRACE-OBSERVABILITY.md).

## Objetivo
Cerrar delta verificable de qa y regresión audiovisual desde código y evidencias existentes sin reimplementar capacidades válidas.

## Dependencias
VID-C14

## Tareas pendientes
- VID-C15-T01: Congelar SHA y verificar código; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C15-T02: Reconciliar evidencias históricas con HEAD; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C15-T03: Especificar delta y superficies de escritura; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C15-T04: Definir contratos y permisos con padre; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C15-T05: Diseñar pruebas positivas y negativas; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C15-T06: Recopilar evidencias y rollback; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.
- VID-C15-T07: Gate Codex/arquitecto y founder; Evidencia reproducible SHA y entorno; BLOCKED si no se ejecuta.

## Gates sin ejecutar
- VID-C15-G01: Tenant ajeno o permiso ausente bloquea acceso/efecto.
- VID-C15-G02: Fallo o estado incierto evita duplicados y permite rollback.

Rollback: Deshabilitar capacidad nueva, preservar datos/evidencias y conciliar efectos externos.

Tras Astra y reconciliación: sustituir este scaffold por patchsets, pruebas y handoffs de campaña. No reescribir funcionalidad existente sin delta probado.
