# Programa industrial — Agntia Video (42 campañas)

Estado: **planificación, no implementación**. Basado en README.md y package.json de main consultados el 14-11-2026. Antes de tocar código, Freebuff debe inspeccionar archivos reales y registrar baseline. No asumir que lo descrito en README está implementado ni que existen rutas concretas.

## Arquitectura que se debe preservar

- Backend Python 3.11+ / FFmpeg, interfaz web y paquete TypeScript @agntia/video 0.4.0, Hono y herramientas agénticas.
- Edición humana y agéntica del mismo proyecto; originales inmutables; previsualización y exportaciones como artefactos derivados.
- DeepSeek/Gemini opcionales; RNNoise local; no sustituir el motor Python por TS.
- El README indica que el servidor es single-owner y la cola vive en un proceso: **no anunciar multitenancy ni escalado horizontal hasta implementarlos y verificarlos**.

## Protocolo obligatorio de cada campaña

Siete tareas: (1) inspeccionar código y dependencias, (2) documentar contratos y riesgos, (3) implementar cambio mínimo vertical, (4) conectar Python/TS/Hono/UI/runtime según aplique, (5) escribir tests positivos, negativos y de regresión, (6) ejecutar verificaciones y registrar evidencia, (7) entregar reporte de Freebuff con archivos, diffs, comandos, resultados, riesgos y siguientes pasos. Dos gates: **G1** contratos/seguridad/aislamiento revisados; **G2** tests y regresión validados por Codex. No cerrar con gates fallidos. Cada campaña se ejecuta en rama propia; merge solo con aprobación y sin conflictos. Ningún secreto en Git. 

## Secuencia de campañas

### C01 — Inventario de arquitectura y baseline

**Objetivo:** auditar y fortalecer inventario de arquitectura y baseline sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C01-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C01 (baseline inicial).

### C02 — Contratos API Python y TS

**Objetivo:** auditar y fortalecer contratos api python y ts sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C02-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C01.

### C03 — Seguridad de autenticación Hono

**Objetivo:** auditar y fortalecer seguridad de autenticación hono sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C03-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C02.

### C04 — Aislamiento multiempresa

**Objetivo:** auditar y fortalecer aislamiento multiempresa sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C04-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C03.

### C05 — Autorización por proyecto y rol

**Objetivo:** auditar y fortalecer autorización por proyecto y rol sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C05-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C04.

### C06 — Persistencia y migraciones

**Objetivo:** auditar y fortalecer persistencia y migraciones sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C06-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C05.

### C07 — Almacenamiento de originales

**Objetivo:** auditar y fortalecer almacenamiento de originales sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C07-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C06.

### C08 — Ingesta segura y cuotas

**Objetivo:** auditar y fortalecer ingesta segura y cuotas sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C08-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C07.

### C09 — Colas persistentes de render

**Objetivo:** auditar y fortalecer colas persistentes de render sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C09-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C08.

### C10 — Idempotencia y reintentos

**Objetivo:** auditar y fortalecer idempotencia y reintentos sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C10-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C09.

### C11 — Cancelación y recuperación

**Objetivo:** auditar y fortalecer cancelación y recuperación sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C11-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C10.

### C12 — Eventos auditables append-only

**Objetivo:** auditar y fortalecer eventos auditables append-only sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C12-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C11.

### C13 — Integración runtime AgntiaPro

**Objetivo:** auditar y fortalecer integración runtime agntiapro sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C13-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C12.

### C14 — Herramientas tipadas de agentes

**Objetivo:** auditar y fortalecer herramientas tipadas de agentes sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C14-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C13.

### C15 — Aprobaciones humanas

**Objetivo:** auditar y fortalecer aprobaciones humanas sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C15-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C14.

### C16 — Briefing conversacional

**Objetivo:** auditar y fortalecer briefing conversacional sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C16-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C15.

### C17 — Plan de montaje versionado

**Objetivo:** auditar y fortalecer plan de montaje versionado sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C17-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C16.

### C18 — Conflictos de edición y merge

**Objetivo:** auditar y fortalecer conflictos de edición y merge sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C18-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C17.

### C19 — Timeline y UX accesible

**Objetivo:** auditar y fortalecer timeline y ux accesible sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C19-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C18.

### C20 — Previsualización fiel

**Objetivo:** auditar y fortalecer previsualización fiel sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C20-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C19.

### C21 — Motor FFmpeg reproducible

**Objetivo:** auditar y fortalecer motor ffmpeg reproducible sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C21-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C20.

### C22 — Optimización de CPU y temporales

**Objetivo:** auditar y fortalecer optimización de cpu y temporales sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C22-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C21.

### C23 — Limpieza de voz RNNoise

**Objetivo:** auditar y fortalecer limpieza de voz rnnoise sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C23-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C22.

### C24 — Mezcla musical y ducking

**Objetivo:** auditar y fortalecer mezcla musical y ducking sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C24-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C23.

### C25 — Detección de beats

**Objetivo:** auditar y fortalecer detección de beats sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C25-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C24.

### C26 — Transcripción Gemini y caché

**Objetivo:** auditar y fortalecer transcripción gemini y caché sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C26-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C25.

### C27 — Subtítulos multilingües

**Objetivo:** auditar y fortalecer subtítulos multilingües sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C27-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C26.

### C28 — Traducción y revisión editorial

**Objetivo:** auditar y fortalecer traducción y revisión editorial sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C28-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C27.

### C29 — Detección de highlights

**Objetivo:** auditar y fortalecer detección de highlights sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C29-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C28.

### C30 — Clips verticales automáticos

**Objetivo:** auditar y fortalecer clips verticales automáticos sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C30-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C29.

### C31 — Plantillas y marca por tenant

**Objetivo:** auditar y fortalecer plantillas y marca por tenant sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C31-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C30.

### C32 — Avatares y vídeo LAIA

**Objetivo:** auditar y fortalecer avatares y vídeo laia sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C32-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C31.

### C33 — Podcasts y entrevistas

**Objetivo:** auditar y fortalecer podcasts y entrevistas sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C33-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C32.

### C34 — Vídeo comercial multicanal

**Objetivo:** auditar y fortalecer vídeo comercial multicanal sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C34-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C33.

### C35 — Programación y publicación controlada

**Objetivo:** auditar y fortalecer programación y publicación controlada sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C35-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C34.

### C36 — Derechos y consentimiento audiovisual

**Objetivo:** auditar y fortalecer derechos y consentimiento audiovisual sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C36-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C35.

### C37 — Protección de datos y retención

**Objetivo:** auditar y fortalecer protección de datos y retención sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C37-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C36.

### C38 — Observabilidad y costes

**Objetivo:** auditar y fortalecer observabilidad y costes sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C38-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C37.

### C39 — Pruebas unitarias y contractuales

**Objetivo:** auditar y fortalecer pruebas unitarias y contractuales sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C39-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C38.

### C40 — Pruebas E2E y renders reales

**Objetivo:** auditar y fortalecer pruebas e2e y renders reales sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C40-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C39.

### C41 — Despliegue seguro y operación

**Objetivo:** auditar y fortalecer despliegue seguro y operación sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C41-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C40.

### C42 — Dogfooding, aceptación y release

**Objetivo:** auditar y fortalecer dogfooding, aceptación y release sobre el código existente, preservando compatibilidad hacia atrás. **Entregable:** implementación o decisión documentada con contratos, pruebas y rollback; reporte `docs/campanas-video/reportes/C42-reporte.md`. **Verificación específica:** prueba de aceptación del flujo afectado, denegación de operaciones no autorizadas, idempotencia cuando haya efectos y no regresión del flujo de proyecto→previsualización→exportación. **Dependencia:** C41.

## Gates globales de release

- 42 reportes y 84 gates trazables; no contar tareas como ejecutadas hasta verificar evidencia.
- Smoke del editor humano, cliente TS, adaptador Hono, FFmpeg real y permisos entre tenants.
- Validación de tiempos, costes, limpieza de temporales, retención, consentimiento y rollback.
- Aprobación explícita del founder para publicar, desplegar o conectar credenciales reales.
