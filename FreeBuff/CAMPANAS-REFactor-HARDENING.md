# FreeBuff — programa de refactorización/hardening y vertical funcional

**Repositorio:** `uniscrolliabrain-cloud/agntia-video` · **Fecha:** 2026-11-14 · **Estado:** PLANIFICADO / NO EJECUTADO. **Diagnóstico inicial por README y artefactos puntuales:** MVP Python FastAPI/FFmpeg 0.4 + SDK TS/Hono; existe código y tests. **Estrategia:** refactorizar, no reconstruir. Las rutas que se citan como nuevas son propuestas y deben cotejarse con el árbol real antes de crear archivos.

## Resultado esperado y límites

Dejar el repositorio listo para una instalación **interna en entorno aislado** y para una futura integración controlada con Doppler y `/agente`, **no** listo automáticamente para producción. No modificar `/agente`, `agntia-gestoria`, ni otros repos; no desplegar, comprar, enviar mensajes, publicar, cobrar, firmar, acceder a clientes ni conectar cuentas reales. Si faltan permisos o dependencias, reportar BLOCKED, no inventar PASS. No reemplazar tecnología existente sin ADR y migración.

**Vertical objetivo:** Proyecto sintético → ingestión → timeline → render aislado → previsualización → aprobación → entrega hash.

**Capacidades a construir o verificar:** ingesta multimedia autorizada; proyectos y timeline; render FFmpeg sandbox; subtítulos y traducción; voz RNNoise y música; Gemini/DeepSeek opcionales; SDK Hono tools de agente; descarga y entrega con receipts.

**Riesgos específicos:** path traversal y symlinks; SSRF de importación; FFmpeg filtros y recursos; fuga de API keys; licencias codecs/modelos; archivos grandes y cancelación.

## Secuencia obligatoria de 12 campañas

### FB-01 — Inventario real y baseline

**Propósito:** Identificar árbol real, lenguajes, scripts, contratos, CI, estado de cada una de las 42 campañas y archivos ya implementados. Crear matriz existente/parcial/ausente con SHA y pruebas. Nunca asumir que docs equivalen a runtime.

**Tareas granulares:**
1. Fijar SHA de `main`, inspeccionar `README.md`, `AGENTS.md`, `docs/campaigns/`, manifiestos y módulos existentes; registrar si la capacidad ya existe, está parcial o ausente.
2. Especificar contrato de entrada/salida para **ingesta multimedia autorizada** con `tenant_id`, `actor_id`, `correlation_id`, `schemaVersion`, recurso y permisos; modelar caso válido y cinco inválidos.
3. Crear o modificar únicamente los archivos confirmados en inventario: `src/contracts/`, `src/domain/`, `src/runtime/`, `src/adapters/`, `src/api/`, `tests/`, `docs/` según arquitectura real; listar paths exactos en el reporte antes de escribir.
4. Añadir pruebas unitarias para validación, roles, serialización, idempotencia y errores; fixture de dos tenants, principal humano, twin agente y principal no autorizado.
5. Introducir test negativo del riesgo **path traversal y symlinks** y simular proveedor ausente, timeout, retry duplicado y estado parcialmente persistido.
6. Ejecutar scripts reales de lint/typecheck/build/test y verificar migraciones/rollback cuando existan; capturar comandos, exit codes, SHA y skips.
7. Actualizar README/contratos/runbook sin borrar historia, añadir `FreeBuff/reportes/FB-01-REPORT.md`, explicar archivos tocados, evidencias, riesgos residuales y decisión PASS/PARTIAL/FAIL/BLOCKED.
8. Entregar PR acotada; Codex u otro revisor independiente verifica regresiones, cross-tenant y diffs; no fusionar con gates rojos.

**Gate de aceptación:** funcionalidad demostrada en fixtures para ingesta multimedia autorizada; control de path traversal y symlinks demostrado con negativo; no side effects reales; rollback documentado y reporte verificable.

### FB-02 — Monorepo/middleware y toolchain

**Propósito:** Estructurar paquete instalable según stack existente; si documentación-only elegir TypeScript/Hono/pnpm para middleware y PostgreSQL/Supabase donde proceda, sin introducir Python salvo motivo. ESLint, TS strict, build, tests y CI reproducible.

**Tareas granulares:**
1. Fijar SHA de `main`, inspeccionar `README.md`, `AGENTS.md`, `docs/campaigns/`, manifiestos y módulos existentes; registrar si la capacidad ya existe, está parcial o ausente.
2. Especificar contrato de entrada/salida para **proyectos y timeline** con `tenant_id`, `actor_id`, `correlation_id`, `schemaVersion`, recurso y permisos; modelar caso válido y cinco inválidos.
3. Crear o modificar únicamente los archivos confirmados en inventario: `src/contracts/`, `src/domain/`, `src/runtime/`, `src/adapters/`, `src/api/`, `tests/`, `docs/` según arquitectura real; listar paths exactos en el reporte antes de escribir.
4. Añadir pruebas unitarias para validación, roles, serialización, idempotencia y errores; fixture de dos tenants, principal humano, twin agente y principal no autorizado.
5. Introducir test negativo del riesgo **SSRF de importación** y simular proveedor ausente, timeout, retry duplicado y estado parcialmente persistido.
6. Ejecutar scripts reales de lint/typecheck/build/test y verificar migraciones/rollback cuando existan; capturar comandos, exit codes, SHA y skips.
7. Actualizar README/contratos/runbook sin borrar historia, añadir `FreeBuff/reportes/FB-02-REPORT.md`, explicar archivos tocados, evidencias, riesgos residuales y decisión PASS/PARTIAL/FAIL/BLOCKED.
8. Entregar PR acotada; Codex u otro revisor independiente verifica regresiones, cross-tenant y diffs; no fusionar con gates rojos.

**Gate de aceptación:** funcionalidad demostrada en fixtures para proyectos y timeline; control de SSRF de importación demostrado con negativo; no side effects reales; rollback documentado y reporte verificable.

### FB-03 — Identidad, tenants y políticas

**Propósito:** Verificar JWT Supabase vía JWKS con issuer/audience/exp, membresía server-side, ACL y RLS; agentes canónicos en /agente y twins delegados con scope; denegar por defecto. Si repo existente usa auth propia, crear adaptador sin reemplazo ciego.

**Tareas granulares:**
1. Fijar SHA de `main`, inspeccionar `README.md`, `AGENTS.md`, `docs/campaigns/`, manifiestos y módulos existentes; registrar si la capacidad ya existe, está parcial o ausente.
2. Especificar contrato de entrada/salida para **render FFmpeg sandbox** con `tenant_id`, `actor_id`, `correlation_id`, `schemaVersion`, recurso y permisos; modelar caso válido y cinco inválidos.
3. Crear o modificar únicamente los archivos confirmados en inventario: `src/contracts/`, `src/domain/`, `src/runtime/`, `src/adapters/`, `src/api/`, `tests/`, `docs/` según arquitectura real; listar paths exactos en el reporte antes de escribir.
4. Añadir pruebas unitarias para validación, roles, serialización, idempotencia y errores; fixture de dos tenants, principal humano, twin agente y principal no autorizado.
5. Introducir test negativo del riesgo **FFmpeg filtros y recursos** y simular proveedor ausente, timeout, retry duplicado y estado parcialmente persistido.
6. Ejecutar scripts reales de lint/typecheck/build/test y verificar migraciones/rollback cuando existan; capturar comandos, exit codes, SHA y skips.
7. Actualizar README/contratos/runbook sin borrar historia, añadir `FreeBuff/reportes/FB-03-REPORT.md`, explicar archivos tocados, evidencias, riesgos residuales y decisión PASS/PARTIAL/FAIL/BLOCKED.
8. Entregar PR acotada; Codex u otro revisor independiente verifica regresiones, cross-tenant y diffs; no fusionar con gates rojos.

**Gate de aceptación:** funcionalidad demostrada en fixtures para render FFmpeg sandbox; control de FFmpeg filtros y recursos demostrado con negativo; no side effects reales; rollback documentado y reporte verificable.

### FB-04 — Contratos y persistencia

**Propósito:** Zod schemas versionados para tenant/actor/resource/job/approval/event/receipt; migraciones idempotentes, transacciones, tenant_id en todas las claves y queries; índices y rollback; no secretos en BD.

**Tareas granulares:**
1. Fijar SHA de `main`, inspeccionar `README.md`, `AGENTS.md`, `docs/campaigns/`, manifiestos y módulos existentes; registrar si la capacidad ya existe, está parcial o ausente.
2. Especificar contrato de entrada/salida para **subtítulos y traducción** con `tenant_id`, `actor_id`, `correlation_id`, `schemaVersion`, recurso y permisos; modelar caso válido y cinco inválidos.
3. Crear o modificar únicamente los archivos confirmados en inventario: `src/contracts/`, `src/domain/`, `src/runtime/`, `src/adapters/`, `src/api/`, `tests/`, `docs/` según arquitectura real; listar paths exactos en el reporte antes de escribir.
4. Añadir pruebas unitarias para validación, roles, serialización, idempotencia y errores; fixture de dos tenants, principal humano, twin agente y principal no autorizado.
5. Introducir test negativo del riesgo **fuga de API keys** y simular proveedor ausente, timeout, retry duplicado y estado parcialmente persistido.
6. Ejecutar scripts reales de lint/typecheck/build/test y verificar migraciones/rollback cuando existan; capturar comandos, exit codes, SHA y skips.
7. Actualizar README/contratos/runbook sin borrar historia, añadir `FreeBuff/reportes/FB-04-REPORT.md`, explicar archivos tocados, evidencias, riesgos residuales y decisión PASS/PARTIAL/FAIL/BLOCKED.
8. Entregar PR acotada; Codex u otro revisor independiente verifica regresiones, cross-tenant y diffs; no fusionar con gates rojos.

**Gate de aceptación:** funcionalidad demostrada en fixtures para subtítulos y traducción; control de fuga de API keys demostrado con negativo; no side effects reales; rollback documentado y reporte verificable.

### FB-05 — Runtime determinista y workers

**Propósito:** SOPs tipados, idempotency keys, lease/fencing, retries acotados, dead-letter, audit append-only, snapshots, replays y recuperación tras crash. El LLM solo propone.

**Tareas granulares:**
1. Fijar SHA de `main`, inspeccionar `README.md`, `AGENTS.md`, `docs/campaigns/`, manifiestos y módulos existentes; registrar si la capacidad ya existe, está parcial o ausente.
2. Especificar contrato de entrada/salida para **voz RNNoise y música** con `tenant_id`, `actor_id`, `correlation_id`, `schemaVersion`, recurso y permisos; modelar caso válido y cinco inválidos.
3. Crear o modificar únicamente los archivos confirmados en inventario: `src/contracts/`, `src/domain/`, `src/runtime/`, `src/adapters/`, `src/api/`, `tests/`, `docs/` según arquitectura real; listar paths exactos en el reporte antes de escribir.
4. Añadir pruebas unitarias para validación, roles, serialización, idempotencia y errores; fixture de dos tenants, principal humano, twin agente y principal no autorizado.
5. Introducir test negativo del riesgo **licencias codecs/modelos** y simular proveedor ausente, timeout, retry duplicado y estado parcialmente persistido.
6. Ejecutar scripts reales de lint/typecheck/build/test y verificar migraciones/rollback cuando existan; capturar comandos, exit codes, SHA y skips.
7. Actualizar README/contratos/runbook sin borrar historia, añadir `FreeBuff/reportes/FB-05-REPORT.md`, explicar archivos tocados, evidencias, riesgos residuales y decisión PASS/PARTIAL/FAIL/BLOCKED.
8. Entregar PR acotada; Codex u otro revisor independiente verifica regresiones, cross-tenant y diffs; no fusionar con gates rojos.

**Gate de aceptación:** funcionalidad demostrada en fixtures para voz RNNoise y música; control de licencias codecs/modelos demostrado con negativo; no side effects reales; rollback documentado y reporte verificable.

### FB-06 — Primera vertical de negocio

**Propósito:** Implementar el flujo dominio de principio a fin con datos sintéticos, conectores mock y decisiones humanas; registrar cada transición y receipt.

**Tareas granulares:**
1. Fijar SHA de `main`, inspeccionar `README.md`, `AGENTS.md`, `docs/campaigns/`, manifiestos y módulos existentes; registrar si la capacidad ya existe, está parcial o ausente.
2. Especificar contrato de entrada/salida para **Gemini/DeepSeek opcionales** con `tenant_id`, `actor_id`, `correlation_id`, `schemaVersion`, recurso y permisos; modelar caso válido y cinco inválidos.
3. Crear o modificar únicamente los archivos confirmados en inventario: `src/contracts/`, `src/domain/`, `src/runtime/`, `src/adapters/`, `src/api/`, `tests/`, `docs/` según arquitectura real; listar paths exactos en el reporte antes de escribir.
4. Añadir pruebas unitarias para validación, roles, serialización, idempotencia y errores; fixture de dos tenants, principal humano, twin agente y principal no autorizado.
5. Introducir test negativo del riesgo **archivos grandes y cancelación** y simular proveedor ausente, timeout, retry duplicado y estado parcialmente persistido.
6. Ejecutar scripts reales de lint/typecheck/build/test y verificar migraciones/rollback cuando existan; capturar comandos, exit codes, SHA y skips.
7. Actualizar README/contratos/runbook sin borrar historia, añadir `FreeBuff/reportes/FB-06-REPORT.md`, explicar archivos tocados, evidencias, riesgos residuales y decisión PASS/PARTIAL/FAIL/BLOCKED.
8. Entregar PR acotada; Codex u otro revisor independiente verifica regresiones, cross-tenant y diffs; no fusionar con gates rojos.

**Gate de aceptación:** funcionalidad demostrada en fixtures para Gemini/DeepSeek opcionales; control de archivos grandes y cancelación demostrado con negativo; no side effects reales; rollback documentado y reporte verificable.

### FB-07 — Puertos y adaptadores

**Propósito:** Definir interfaz de proveedores, capability matrix, timeouts, retries, circuit breaker, quotas, redacción, fixture de fallos; ningún proveedor real sin aprobación.

**Tareas granulares:**
1. Fijar SHA de `main`, inspeccionar `README.md`, `AGENTS.md`, `docs/campaigns/`, manifiestos y módulos existentes; registrar si la capacidad ya existe, está parcial o ausente.
2. Especificar contrato de entrada/salida para **SDK Hono tools de agente** con `tenant_id`, `actor_id`, `correlation_id`, `schemaVersion`, recurso y permisos; modelar caso válido y cinco inválidos.
3. Crear o modificar únicamente los archivos confirmados en inventario: `src/contracts/`, `src/domain/`, `src/runtime/`, `src/adapters/`, `src/api/`, `tests/`, `docs/` según arquitectura real; listar paths exactos en el reporte antes de escribir.
4. Añadir pruebas unitarias para validación, roles, serialización, idempotencia y errores; fixture de dos tenants, principal humano, twin agente y principal no autorizado.
5. Introducir test negativo del riesgo **path traversal y symlinks** y simular proveedor ausente, timeout, retry duplicado y estado parcialmente persistido.
6. Ejecutar scripts reales de lint/typecheck/build/test y verificar migraciones/rollback cuando existan; capturar comandos, exit codes, SHA y skips.
7. Actualizar README/contratos/runbook sin borrar historia, añadir `FreeBuff/reportes/FB-07-REPORT.md`, explicar archivos tocados, evidencias, riesgos residuales y decisión PASS/PARTIAL/FAIL/BLOCKED.
8. Entregar PR acotada; Codex u otro revisor independiente verifica regresiones, cross-tenant y diffs; no fusionar con gates rojos.

**Gate de aceptación:** funcionalidad demostrada en fixtures para SDK Hono tools de agente; control de path traversal y symlinks demostrado con negativo; no side effects reales; rollback documentado y reporte verificable.

### FB-08 — API Hono y SDK AgntiaPro

**Propósito:** Cliente TS tipado, rutas Hono sin proxy arbitrario, tools de agente con inputs cerrados y grants one-use; tenant elegido por BFF; outbox at-least-once y consumidor idempotente.

**Tareas granulares:**
1. Fijar SHA de `main`, inspeccionar `README.md`, `AGENTS.md`, `docs/campaigns/`, manifiestos y módulos existentes; registrar si la capacidad ya existe, está parcial o ausente.
2. Especificar contrato de entrada/salida para **descarga y entrega con receipts** con `tenant_id`, `actor_id`, `correlation_id`, `schemaVersion`, recurso y permisos; modelar caso válido y cinco inválidos.
3. Crear o modificar únicamente los archivos confirmados en inventario: `src/contracts/`, `src/domain/`, `src/runtime/`, `src/adapters/`, `src/api/`, `tests/`, `docs/` según arquitectura real; listar paths exactos en el reporte antes de escribir.
4. Añadir pruebas unitarias para validación, roles, serialización, idempotencia y errores; fixture de dos tenants, principal humano, twin agente y principal no autorizado.
5. Introducir test negativo del riesgo **SSRF de importación** y simular proveedor ausente, timeout, retry duplicado y estado parcialmente persistido.
6. Ejecutar scripts reales de lint/typecheck/build/test y verificar migraciones/rollback cuando existan; capturar comandos, exit codes, SHA y skips.
7. Actualizar README/contratos/runbook sin borrar historia, añadir `FreeBuff/reportes/FB-08-REPORT.md`, explicar archivos tocados, evidencias, riesgos residuales y decisión PASS/PARTIAL/FAIL/BLOCKED.
8. Entregar PR acotada; Codex u otro revisor independiente verifica regresiones, cross-tenant y diffs; no fusionar con gates rojos.

**Gate de aceptación:** funcionalidad demostrada en fixtures para descarga y entrega con receipts; control de SSRF de importación demostrado con negativo; no side effects reales; rollback documentado y reporte verificable.

### FB-09 — UX y observabilidad

**Propósito:** Portal mínimo accesible responsive, estados vacíos/errores/pendientes, bandeja de aprobación, trazas OTel, métricas de negocio y técnicas, logs sin PII.

**Tareas granulares:**
1. Fijar SHA de `main`, inspeccionar `README.md`, `AGENTS.md`, `docs/campaigns/`, manifiestos y módulos existentes; registrar si la capacidad ya existe, está parcial o ausente.
2. Especificar contrato de entrada/salida para **ingesta multimedia autorizada** con `tenant_id`, `actor_id`, `correlation_id`, `schemaVersion`, recurso y permisos; modelar caso válido y cinco inválidos.
3. Crear o modificar únicamente los archivos confirmados en inventario: `src/contracts/`, `src/domain/`, `src/runtime/`, `src/adapters/`, `src/api/`, `tests/`, `docs/` según arquitectura real; listar paths exactos en el reporte antes de escribir.
4. Añadir pruebas unitarias para validación, roles, serialización, idempotencia y errores; fixture de dos tenants, principal humano, twin agente y principal no autorizado.
5. Introducir test negativo del riesgo **FFmpeg filtros y recursos** y simular proveedor ausente, timeout, retry duplicado y estado parcialmente persistido.
6. Ejecutar scripts reales de lint/typecheck/build/test y verificar migraciones/rollback cuando existan; capturar comandos, exit codes, SHA y skips.
7. Actualizar README/contratos/runbook sin borrar historia, añadir `FreeBuff/reportes/FB-09-REPORT.md`, explicar archivos tocados, evidencias, riesgos residuales y decisión PASS/PARTIAL/FAIL/BLOCKED.
8. Entregar PR acotada; Codex u otro revisor independiente verifica regresiones, cross-tenant y diffs; no fusionar con gates rojos.

**Gate de aceptación:** funcionalidad demostrada en fixtures para ingesta multimedia autorizada; control de FFmpeg filtros y recursos demostrado con negativo; no side effects reales; rollback documentado y reporte verificable.

### FB-10 — Pruebas adversariales y hardening

**Propósito:** Unit/integration/contract/E2E, dos tenants, fuzz de schemas, race conditions, prompt injection, SSRF, XSS, path traversal, replay, rotación de credenciales y caída de proveedores.

**Tareas granulares:**
1. Fijar SHA de `main`, inspeccionar `README.md`, `AGENTS.md`, `docs/campaigns/`, manifiestos y módulos existentes; registrar si la capacidad ya existe, está parcial o ausente.
2. Especificar contrato de entrada/salida para **proyectos y timeline** con `tenant_id`, `actor_id`, `correlation_id`, `schemaVersion`, recurso y permisos; modelar caso válido y cinco inválidos.
3. Crear o modificar únicamente los archivos confirmados en inventario: `src/contracts/`, `src/domain/`, `src/runtime/`, `src/adapters/`, `src/api/`, `tests/`, `docs/` según arquitectura real; listar paths exactos en el reporte antes de escribir.
4. Añadir pruebas unitarias para validación, roles, serialización, idempotencia y errores; fixture de dos tenants, principal humano, twin agente y principal no autorizado.
5. Introducir test negativo del riesgo **fuga de API keys** y simular proveedor ausente, timeout, retry duplicado y estado parcialmente persistido.
6. Ejecutar scripts reales de lint/typecheck/build/test y verificar migraciones/rollback cuando existan; capturar comandos, exit codes, SHA y skips.
7. Actualizar README/contratos/runbook sin borrar historia, añadir `FreeBuff/reportes/FB-10-REPORT.md`, explicar archivos tocados, evidencias, riesgos residuales y decisión PASS/PARTIAL/FAIL/BLOCKED.
8. Entregar PR acotada; Codex u otro revisor independiente verifica regresiones, cross-tenant y diffs; no fusionar con gates rojos.

**Gate de aceptación:** funcionalidad demostrada en fixtures para proyectos y timeline; control de fuga de API keys demostrado con negativo; no side effects reales; rollback documentado y reporte verificable.

### FB-11 — Doppler-ready sin conectar secretos

**Propósito:** Inventario env names y owners, config.example sin valores, secret provider interface, startup fail-closed, detección de secretos hardcodeados, mapping dev/stg/prod, política de rotación; no crear proyecto ni instalar Doppler aún.

**Tareas granulares:**
1. Fijar SHA de `main`, inspeccionar `README.md`, `AGENTS.md`, `docs/campaigns/`, manifiestos y módulos existentes; registrar si la capacidad ya existe, está parcial o ausente.
2. Especificar contrato de entrada/salida para **render FFmpeg sandbox** con `tenant_id`, `actor_id`, `correlation_id`, `schemaVersion`, recurso y permisos; modelar caso válido y cinco inválidos.
3. Crear o modificar únicamente los archivos confirmados en inventario: `src/contracts/`, `src/domain/`, `src/runtime/`, `src/adapters/`, `src/api/`, `tests/`, `docs/` según arquitectura real; listar paths exactos en el reporte antes de escribir.
4. Añadir pruebas unitarias para validación, roles, serialización, idempotencia y errores; fixture de dos tenants, principal humano, twin agente y principal no autorizado.
5. Introducir test negativo del riesgo **licencias codecs/modelos** y simular proveedor ausente, timeout, retry duplicado y estado parcialmente persistido.
6. Ejecutar scripts reales de lint/typecheck/build/test y verificar migraciones/rollback cuando existan; capturar comandos, exit codes, SHA y skips.
7. Actualizar README/contratos/runbook sin borrar historia, añadir `FreeBuff/reportes/FB-11-REPORT.md`, explicar archivos tocados, evidencias, riesgos residuales y decisión PASS/PARTIAL/FAIL/BLOCKED.
8. Entregar PR acotada; Codex u otro revisor independiente verifica regresiones, cross-tenant y diffs; no fusionar con gates rojos.

**Gate de aceptación:** funcionalidad demostrada en fixtures para render FFmpeg sandbox; control de licencias codecs/modelos demostrado con negativo; no side effects reales; rollback documentado y reporte verificable.

### FB-12 — Release interno y handoff al padre

**Propósito:** Paquete reproducible, SBOM, licencias, checksums, runbook, backup/restore, matriz de compatibilidad, smoke tests y propuesta de patchset /agente NO APLICADA; gate founder.

**Tareas granulares:**
1. Fijar SHA de `main`, inspeccionar `README.md`, `AGENTS.md`, `docs/campaigns/`, manifiestos y módulos existentes; registrar si la capacidad ya existe, está parcial o ausente.
2. Especificar contrato de entrada/salida para **subtítulos y traducción** con `tenant_id`, `actor_id`, `correlation_id`, `schemaVersion`, recurso y permisos; modelar caso válido y cinco inválidos.
3. Crear o modificar únicamente los archivos confirmados en inventario: `src/contracts/`, `src/domain/`, `src/runtime/`, `src/adapters/`, `src/api/`, `tests/`, `docs/` según arquitectura real; listar paths exactos en el reporte antes de escribir.
4. Añadir pruebas unitarias para validación, roles, serialización, idempotencia y errores; fixture de dos tenants, principal humano, twin agente y principal no autorizado.
5. Introducir test negativo del riesgo **archivos grandes y cancelación** y simular proveedor ausente, timeout, retry duplicado y estado parcialmente persistido.
6. Ejecutar scripts reales de lint/typecheck/build/test y verificar migraciones/rollback cuando existan; capturar comandos, exit codes, SHA y skips.
7. Actualizar README/contratos/runbook sin borrar historia, añadir `FreeBuff/reportes/FB-12-REPORT.md`, explicar archivos tocados, evidencias, riesgos residuales y decisión PASS/PARTIAL/FAIL/BLOCKED.
8. Entregar PR acotada; Codex u otro revisor independiente verifica regresiones, cross-tenant y diffs; no fusionar con gates rojos.

**Gate de aceptación:** funcionalidad demostrada en fixtures para subtítulos y traducción; control de archivos grandes y cancelación demostrado con negativo; no side effects reales; rollback documentado y reporte verificable.

## Contrato técnico de referencia (adaptar, no copiar ciegamente)

```ts
import { z } from "zod";
export const ExecutionEnvelope = z.object({
  schemaVersion: z.literal(1),
  tenantId: z.string().min(1), actorId: z.string().min(1),
  correlationId: z.string().uuid(), idempotencyKey: z.string().min(8),
  resourceId: z.string().min(1), capability: z.string().min(1),
  payload: z.unknown(),
}).strict();
export type ExecutionEnvelope = z.infer<typeof ExecutionEnvelope>;
// El handler debe derivar tenant/actor de principal verificado, no confiar en payload.
// Persistir idempotencyKey + tenant + capability bajo constraint UNIQUE.
// Comprobar policy/approval/revision antes de efectos, registrar receipt y outbox en una transacción.
```

**SQL orientativo, sujeto a la DB elegida:** `UNIQUE(tenant_id, capability, idempotency_key)`; `PRIMARY KEY(tenant_id, id)`; índices de `tenant_id, status, created_at`; RLS con `WITH CHECK` y `USING` por principal autenticado. No sustituye revisión de migrations reales.

## Gates transversales

G0 inventario y verdad del estado; G1 compilación/tests; G2 aislamiento y autorización; G3 no duplicación de efectos; G4 proveedor caído/rollback; G5 trazabilidad, observabilidad y evidencia; G6 aceptación de founder. **Los 42 documentos históricos no se declaran completados por ejecutar estas 12 campañas.** Registrar correspondencia `FB-xx ↔ Cxx` y delta pendiente. Solo el gate G6 permite proponer integración, no ejecutarla.

## Preparación Doppler y padre

Entregar `FreeBuff/DOPPLER-READY.md` con tabla de variables (nombre, función, entorno, owner, rotación, criticidad, origen, si es secreto), `.env.example` solo con nombres y placeholders no sensibles, estrategia secret-provider server-side, validación de arranque y detección de secretos; sin tokens en git ni browser. Crear `FreeBuff/INTEGRATION-AGENTE-PROPOSAL.md` con paquete, endpoint, tools, permisos, event schemas, outbox, versionado, smoke tests y rollback. No editar repo padre. Se autorizará conexión Doppler y patchset después de revisar gates.

## Reportes por campaña

Cada reporte incluirá: base SHA, head SHA, PR, cambios archivo-a-archivo, decisión técnica/ADR, comandos exactos y exit codes, conteos passed/failed/skipped, fixtures, logs redactados, cobertura, riesgos, migración y rollback, bloqueos, próximas tareas y firma de revisión humana. Prohibido usar SUCCESS para pruebas no ejecutadas.
