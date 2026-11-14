# Handoff de reconciliación y scaffolding integral — Agntia Vídeo

**Fecha:** 2026-11-14 · **Tipo:** instrucción diferencial de la fábrica existente, NO sustitución · **Estado:** PREPARADO / NO EJECUTADO.

## Autoridad y estado observado

PR #1 integró `docs/factory-recovery-v1-20261114` en main (merge `44bea31ae085a050512c51a0c7faf3f702e53a1d`). Solo ramas vistas: `main` y la rama recovery. La rama recovery aportó 18 campañas VID-C01..C18, 126 tareas y 36 gates, todos PLANNED/NOT_EXECUTED según `docs/campaigns/recovery-manifest.json`. No marcar PASS por este documento. CI del head de recovery `0bd8ab58ffedccd85896dc6ea6871d505ac84c9f` reportó Test SUCCESS (run 43651416921); eso no prueba todas las nuevas condiciones ni CI de este commit.

**Código existente que NO debe reescribirse a ciegas:** `agntia/app.py` FastAPI 0.4, `agntia/storage.py` proyectos JSON/revision, `agntia/models.py`, `agntia/media.py`, `agntia/audio.py`, `agntia/jobs.py`, `agntia/providers.py`, `agntia/static/` editor; `typescript/client.ts`, `typescript/hono.ts`, `typescript/agents.ts`, `typescript/types.ts`, `tests/agent_integration.mjs`, `.github/workflows/test.yml`. Paquete `@agntia/video` 0.4 y motor Python FFmpeg/RNNoise. `docs/architecture.md` establece FFmpeg fuera de edge, original media preservada, revision/409, renders snapshot, límites de voz y licencias.

**Hallazgos de revisión estática selectiva:** middleware actual `agntia/app.py` usa `AGNTIA_ACCESS_TOKEN` global y localhost sin token; `agntia/storage.py` usa `DATA/projects/{pid}/project.json` sin tenant namespace visible; `typescript/hono.ts` recibe `authorize(request):boolean` sin principal/scopes en firma. Son límites de arquitectura actual, no hallazgos de pentest. No se ha hecho revisión línea por línea ni tests locales en este handoff. Resolver con migración compatible y tests, no arrancar un proyecto nuevo.

## Reglas de precedencia

1. Fuente principal: código real en HEAD + `README.md`, `AGENTS.md`, `docs/architecture.md`, `docs/typescript-agents.md`, `docs/campaigns/recovery-manifest.json`, los **18** `docs/campaigns/*.md` y `docs/implementation/*/README.md`.
2. `docs/factory/00-README.md`, `01-PIPELINE.md`, `05-INTERFACES-ADAPTERS.md` y `06-READINESS-AUDIT.md` establecen orden PREP → auditoría conceptual Astra → reconciliación → granularización → Freebuff/Codex/Arquitecto/Founder. **No saltarse gates**; pedir aprobación founder si el gate conceptual sigue pendiente.
3. Este documento añade un **mapa de patchsets para scaffolding completo**, no nuevas campañas ni una vertical reducida. Cada VID-Cxx mantiene sus siete tareas y dos gates originales. No eliminar documentación, no modificar `/agente` ni `agntia-gestoria` ni proveedores.

## Orden obligatorio de ejecución y mapa de superficies

### VID-C01 — Baseline MVP y pruebas reproducibles

**Dependencia:** ninguna. **Fuente:** `docs/campaigns/01-baseline-mvp-y-pruebas-reproducibles.md`; **scaffold:** `docs/implementation/01-baseline-mvp-y-pruebas-reproducibles/README.md`.

**Superficies que Freebuff debe verificar antes de editar:** `agntia/app.py`, `agntia/storage.py`, `tests/`, `.github/workflows/test.yml` (si alguna no existe, documentar y ajustar).

**Patchset específico a concretar contra HEAD:** Inventariar endpoints, estado, scripts, matrices Linux/Windows; ejecutar pytest/unittest, pnpm, integración agente, browser; registrar SHA, logs y skips; no afirmar multitenancy.

**Microsecuencia obligatoria (respeta VID-Cxx-T01..T07):** 1. baseline SHA y diff; 2. contrastar código/documento y tests; 3. dibujar contrato/estado/permisos; 4. patchset archivo-a-archivo con pseudocódigo o código compilable según lenguaje real; 5. tests positivos, negativos y dos tenants donde proceda; 6. CI, restore/rollback y evidencias; 7. revisión Codex/arquitecto/founder. Ejecutar los dos gates `VID-C01-G01` y `VID-C01-G02` exactamente como los define el manifiesto; registrar bloqueos sin maquillarlos.

**Reporte:** `FreeBuff/reportes/VID-C01-REPORT.md` con SHA base/head, PR, rutas, código cambiado, comandos, exit codes, passed/failed/skipped, tests de seguridad, licencias, reversibilidad, riesgos y decisión PASS/PARTIAL/FAIL/BLOCKED. Si el gate falla, detener antes de la siguiente campaña.

### VID-C02 — Identidad y tokens actuales

**Dependencia:** VID-C01. **Fuente:** `docs/campaigns/02-identidad-y-tokens-actuales.md`; **scaffold:** `docs/implementation/02-identidad-y-tokens-actuales/README.md`.

**Superficies que Freebuff debe verificar antes de editar:** `agntia/app.py`, `agntia/storage.py`, `typescript/client.ts`, `docs/typescript-agents.md` (si alguna no existe, documentar y ajustar).

**Patchset específico a concretar contra HEAD:** Extraer middleware de autenticación del token global a interfaz AuthPrincipal, sin romper localhost; tests token ausente/remoto, cookie, Origin/CSRF, headers y expiración; token actual es de servicio, no usuario.

**Microsecuencia obligatoria (respeta VID-Cxx-T01..T07):** 1. baseline SHA y diff; 2. contrastar código/documento y tests; 3. dibujar contrato/estado/permisos; 4. patchset archivo-a-archivo con pseudocódigo o código compilable según lenguaje real; 5. tests positivos, negativos y dos tenants donde proceda; 6. CI, restore/rollback y evidencias; 7. revisión Codex/arquitecto/founder. Ejecutar los dos gates `VID-C02-G01` y `VID-C02-G02` exactamente como los define el manifiesto; registrar bloqueos sin maquillarlos.

**Reporte:** `FreeBuff/reportes/VID-C02-REPORT.md` con SHA base/head, PR, rutas, código cambiado, comandos, exit codes, passed/failed/skipped, tests de seguridad, licencias, reversibilidad, riesgos y decisión PASS/PARTIAL/FAIL/BLOCKED. Si el gate falla, detener antes de la siguiente campaña.

### VID-C03 — Supabase JWT, twins y padre

**Dependencia:** VID-C02. **Fuente:** `docs/campaigns/03-supabase-jwt-twins-y-padre.md`; **scaffold:** `docs/implementation/03-supabase-jwt-twins-y-padre/README.md`.

**Superficies que Freebuff debe verificar antes de editar:** `agntia/app.py`, `typescript/hono.ts`, `typescript/agents.ts`, `typescript/types.ts` (si alguna no existe, documentar y ajustar).

**Patchset específico a concretar contra HEAD:** Definir adaptador verificador JWKS Supabase, issuer/audience/exp, tenant membership desde padre, twin grants, claims, ACL; no introducir Supabase como IdP local paralelo; contrato BFF y tests fake JWKS.

**Microsecuencia obligatoria (respeta VID-Cxx-T01..T07):** 1. baseline SHA y diff; 2. contrastar código/documento y tests; 3. dibujar contrato/estado/permisos; 4. patchset archivo-a-archivo con pseudocódigo o código compilable según lenguaje real; 5. tests positivos, negativos y dos tenants donde proceda; 6. CI, restore/rollback y evidencias; 7. revisión Codex/arquitecto/founder. Ejecutar los dos gates `VID-C03-G01` y `VID-C03-G02` exactamente como los define el manifiesto; registrar bloqueos sin maquillarlos.

**Reporte:** `FreeBuff/reportes/VID-C03-REPORT.md` con SHA base/head, PR, rutas, código cambiado, comandos, exit codes, passed/failed/skipped, tests de seguridad, licencias, reversibilidad, riesgos y decisión PASS/PARTIAL/FAIL/BLOCKED. Si el gate falla, detener antes de la siguiente campaña.

### VID-C04 — Aislamiento de proyectos y assets

**Dependencia:** VID-C03. **Fuente:** `docs/campaigns/04-aislamiento-de-proyectos-y-assets.md`; **scaffold:** `docs/implementation/04-aislamiento-de-proyectos-y-assets/README.md`.

**Superficies que Freebuff debe verificar antes de editar:** `agntia/storage.py`, `agntia/app.py`, `agntia/media.py` (si alguna no existe, documentar y ajustar).

**Patchset específico a concretar contra HEAD:** Aislar DATA/projects, asset IDs y cache por tenant; migración compatible de proyectos legacy; tests cross-tenant de lectura/escritura/renders/download/listJobs; policy en capa de servicio y no solo Hono.

**Microsecuencia obligatoria (respeta VID-Cxx-T01..T07):** 1. baseline SHA y diff; 2. contrastar código/documento y tests; 3. dibujar contrato/estado/permisos; 4. patchset archivo-a-archivo con pseudocódigo o código compilable según lenguaje real; 5. tests positivos, negativos y dos tenants donde proceda; 6. CI, restore/rollback y evidencias; 7. revisión Codex/arquitecto/founder. Ejecutar los dos gates `VID-C04-G01` y `VID-C04-G02` exactamente como los define el manifiesto; registrar bloqueos sin maquillarlos.

**Reporte:** `FreeBuff/reportes/VID-C04-REPORT.md` con SHA base/head, PR, rutas, código cambiado, comandos, exit codes, passed/failed/skipped, tests de seguridad, licencias, reversibilidad, riesgos y decisión PASS/PARTIAL/FAIL/BLOCKED. Si el gate falla, detener antes de la siguiente campaña.

### VID-C05 — Concurrencia revision/409

**Dependencia:** VID-C04. **Fuente:** `docs/campaigns/05-concurrencia-revision-409.md`; **scaffold:** `docs/implementation/05-concurrencia-revision-409/README.md`.

**Superficies que Freebuff debe verificar antes de editar:** `agntia/storage.py`, `agntia/app.py`, `typescript/client.ts`, `tests/agent_integration.mjs` (si alguna no existe, documentar y ajustar).

**Patchset específico a concretar contra HEAD:** Mantener revision/409, CAS en persistencia y lock interproceso; tests concurrentes humano/agente, update stale, render con snapshot inmutable, conflictos y rollback.

**Microsecuencia obligatoria (respeta VID-Cxx-T01..T07):** 1. baseline SHA y diff; 2. contrastar código/documento y tests; 3. dibujar contrato/estado/permisos; 4. patchset archivo-a-archivo con pseudocódigo o código compilable según lenguaje real; 5. tests positivos, negativos y dos tenants donde proceda; 6. CI, restore/rollback y evidencias; 7. revisión Codex/arquitecto/founder. Ejecutar los dos gates `VID-C05-G01` y `VID-C05-G02` exactamente como los define el manifiesto; registrar bloqueos sin maquillarlos.

**Reporte:** `FreeBuff/reportes/VID-C05-REPORT.md` con SHA base/head, PR, rutas, código cambiado, comandos, exit codes, passed/failed/skipped, tests de seguridad, licencias, reversibilidad, riesgos y decisión PASS/PARTIAL/FAIL/BLOCKED. Si el gate falla, detener antes de la siguiente campaña.

### VID-C06 — Subidas y rutas no confiables

**Dependencia:** VID-C05. **Fuente:** `docs/campaigns/06-subidas-y-rutas-no-confiables.md`; **scaffold:** `docs/implementation/06-subidas-y-rutas-no-confiables/README.md`.

**Superficies que Freebuff debe verificar antes de editar:** `agntia/app.py`, `agntia/media.py`, `agntia/storage.py`, `typescript/agents.ts` (si alguna no existe, documentar y ajustar).

**Patchset específico a concretar contra HEAD:** Validar MIME magic/ffprobe, cuotas bytes/tiempo, paths y symlinks, multipart, inbox import solo permitido; fuzz nombres, archivos corruptos, bomb y path traversal; sin URL arbitraria.

**Microsecuencia obligatoria (respeta VID-Cxx-T01..T07):** 1. baseline SHA y diff; 2. contrastar código/documento y tests; 3. dibujar contrato/estado/permisos; 4. patchset archivo-a-archivo con pseudocódigo o código compilable según lenguaje real; 5. tests positivos, negativos y dos tenants donde proceda; 6. CI, restore/rollback y evidencias; 7. revisión Codex/arquitecto/founder. Ejecutar los dos gates `VID-C06-G01` y `VID-C06-G02` exactamente como los define el manifiesto; registrar bloqueos sin maquillarlos.

**Reporte:** `FreeBuff/reportes/VID-C06-REPORT.md` con SHA base/head, PR, rutas, código cambiado, comandos, exit codes, passed/failed/skipped, tests de seguridad, licencias, reversibilidad, riesgos y decisión PASS/PARTIAL/FAIL/BLOCKED. Si el gate falla, detener antes de la siguiente campaña.

### VID-C07 — Jobs, colas y cancelación

**Dependencia:** VID-C06. **Fuente:** `docs/campaigns/07-jobs-colas-y-cancelacion.md`; **scaffold:** `docs/implementation/07-jobs-colas-y-cancelacion/README.md`.

**Superficies que Freebuff debe verificar antes de editar:** `agntia/jobs.py`, `agntia/app.py`, `agntia/storage.py`, `typescript/client.ts` (si alguna no existe, documentar y ajustar).

**Patchset específico a concretar contra HEAD:** Persistencia durable de job, state machine, lease/fencing, cancelación y cleanup; reinicio durante render, doble render, retry y DLQ; snapshot del plan, receipt y status explícito.

**Microsecuencia obligatoria (respeta VID-Cxx-T01..T07):** 1. baseline SHA y diff; 2. contrastar código/documento y tests; 3. dibujar contrato/estado/permisos; 4. patchset archivo-a-archivo con pseudocódigo o código compilable según lenguaje real; 5. tests positivos, negativos y dos tenants donde proceda; 6. CI, restore/rollback y evidencias; 7. revisión Codex/arquitecto/founder. Ejecutar los dos gates `VID-C07-G01` y `VID-C07-G02` exactamente como los define el manifiesto; registrar bloqueos sin maquillarlos.

**Reporte:** `FreeBuff/reportes/VID-C07-REPORT.md` con SHA base/head, PR, rutas, código cambiado, comandos, exit codes, passed/failed/skipped, tests de seguridad, licencias, reversibilidad, riesgos y decisión PASS/PARTIAL/FAIL/BLOCKED. Si el gate falla, detener antes de la siguiente campaña.

### VID-C08 — FFmpeg y RNNoise

**Dependencia:** VID-C07. **Fuente:** `docs/campaigns/08-ffmpeg-y-rnnoise.md`; **scaffold:** `docs/implementation/08-ffmpeg-y-rnnoise/README.md`.

**Superficies que Freebuff debe verificar antes de editar:** `agntia/audio.py`, `agntia/media.py`, `agntia/resources/`, `tests/` (si alguna no existe, documentar y ajustar).

**Patchset específico a concretar contra HEAD:** Conservar pipeline FFmpeg/RNNoise y licencia BSD; verificar shell=False, filtros y parámetros, límites CPU/duración/memoria, cancelación, timeouts, pruebas con fixtures sintéticos, hashes de salida.

**Microsecuencia obligatoria (respeta VID-Cxx-T01..T07):** 1. baseline SHA y diff; 2. contrastar código/documento y tests; 3. dibujar contrato/estado/permisos; 4. patchset archivo-a-archivo con pseudocódigo o código compilable según lenguaje real; 5. tests positivos, negativos y dos tenants donde proceda; 6. CI, restore/rollback y evidencias; 7. revisión Codex/arquitecto/founder. Ejecutar los dos gates `VID-C08-G01` y `VID-C08-G02` exactamente como los define el manifiesto; registrar bloqueos sin maquillarlos.

**Reporte:** `FreeBuff/reportes/VID-C08-REPORT.md` con SHA base/head, PR, rutas, código cambiado, comandos, exit codes, passed/failed/skipped, tests de seguridad, licencias, reversibilidad, riesgos y decisión PASS/PARTIAL/FAIL/BLOCKED. Si el gate falla, detener antes de la siguiente campaña.

### VID-C09 — Timecodes, subtítulos y clips

**Dependencia:** VID-C08. **Fuente:** `docs/campaigns/09-timecodes-subtitulos-y-clips.md`; **scaffold:** `docs/implementation/09-timecodes-subtitulos-y-clips/README.md`.

**Superficies que Freebuff debe verificar antes de editar:** `agntia/models.py`, `agntia/media.py`, `agntia/app.py`, `agntia/static/` (si alguna no existe, documentar y ajustar).

**Patchset específico a concretar contra HEAD:** Validar segmentos, audio_start, clip output timeline, SRT, traducciones y subtítulos manuales; golden fixtures de 25 fps, límites, cambio de orden, preview vs export.

**Microsecuencia obligatoria (respeta VID-Cxx-T01..T07):** 1. baseline SHA y diff; 2. contrastar código/documento y tests; 3. dibujar contrato/estado/permisos; 4. patchset archivo-a-archivo con pseudocódigo o código compilable según lenguaje real; 5. tests positivos, negativos y dos tenants donde proceda; 6. CI, restore/rollback y evidencias; 7. revisión Codex/arquitecto/founder. Ejecutar los dos gates `VID-C09-G01` y `VID-C09-G02` exactamente como los define el manifiesto; registrar bloqueos sin maquillarlos.

**Reporte:** `FreeBuff/reportes/VID-C09-REPORT.md` con SHA base/head, PR, rutas, código cambiado, comandos, exit codes, passed/failed/skipped, tests de seguridad, licencias, reversibilidad, riesgos y decisión PASS/PARTIAL/FAIL/BLOCKED. Si el gate falla, detener antes de la siguiente campaña.

### VID-C10 — Derechos de media y voz

**Dependencia:** VID-C09. **Fuente:** `docs/campaigns/10-derechos-de-media-y-voz.md`; **scaffold:** `docs/implementation/10-derechos-de-media-y-voz/README.md`.

**Superficies que Freebuff debe verificar antes de editar:** `agntia/storage.py`, `agntia/models.py`, `agntia/app.py` (si alguna no existe, documentar y ajustar).

**Patchset específico a concretar contra HEAD:** Adjuntar provenance/rights metadata y consentimientos por asset y voz; gate previo a render/entrega; borrado, licencias, trazabilidad y no afirmar titularidad.

**Microsecuencia obligatoria (respeta VID-Cxx-T01..T07):** 1. baseline SHA y diff; 2. contrastar código/documento y tests; 3. dibujar contrato/estado/permisos; 4. patchset archivo-a-archivo con pseudocódigo o código compilable según lenguaje real; 5. tests positivos, negativos y dos tenants donde proceda; 6. CI, restore/rollback y evidencias; 7. revisión Codex/arquitecto/founder. Ejecutar los dos gates `VID-C10-G01` y `VID-C10-G02` exactamente como los define el manifiesto; registrar bloqueos sin maquillarlos.

**Reporte:** `FreeBuff/reportes/VID-C10-REPORT.md` con SHA base/head, PR, rutas, código cambiado, comandos, exit codes, passed/failed/skipped, tests de seguridad, licencias, reversibilidad, riesgos y decisión PASS/PARTIAL/FAIL/BLOCKED. Si el gate falla, detener antes de la siguiente campaña.

### VID-C11 — Anam y voces opt-in

**Dependencia:** VID-C10. **Fuente:** `docs/campaigns/11-anam-y-voces-opt-in.md`; **scaffold:** `docs/implementation/11-anam-y-voces-opt-in/README.md`.

**Superficies que Freebuff debe verificar antes de editar:** `agntia/providers.py`, `agntia/audio.py`, `agntia/app.py` (si alguna no existe, documentar y ajustar).

**Patchset específico a concretar contra HEAD:** Adaptador opt-in Anam/voz sin reemplazar RNNoise ni DeepSeek/Gemini; mocks y contracts, costes, retención y consentimiento explícito; no conectar claves.

**Microsecuencia obligatoria (respeta VID-Cxx-T01..T07):** 1. baseline SHA y diff; 2. contrastar código/documento y tests; 3. dibujar contrato/estado/permisos; 4. patchset archivo-a-archivo con pseudocódigo o código compilable según lenguaje real; 5. tests positivos, negativos y dos tenants donde proceda; 6. CI, restore/rollback y evidencias; 7. revisión Codex/arquitecto/founder. Ejecutar los dos gates `VID-C11-G01` y `VID-C11-G02` exactamente como los define el manifiesto; registrar bloqueos sin maquillarlos.

**Reporte:** `FreeBuff/reportes/VID-C11-REPORT.md` con SHA base/head, PR, rutas, código cambiado, comandos, exit codes, passed/failed/skipped, tests de seguridad, licencias, reversibilidad, riesgos y decisión PASS/PARTIAL/FAIL/BLOCKED. Si el gate falla, detener antes de la siguiente campaña.

### VID-C12 — Backups y retención

**Dependencia:** VID-C11. **Fuente:** `docs/campaigns/12-backups-y-retencion.md`; **scaffold:** `docs/implementation/12-backups-y-retencion/README.md`.

**Superficies que Freebuff debe verificar antes de editar:** `agntia/storage.py`, `agntia/jobs.py`, `agntia/app.py` (si alguna no existe, documentar y ajustar).

**Patchset específico a concretar contra HEAD:** Política de retención por tenant, export/backup cifrado, restore probado, purga de originales/proxies/caché/jobs, legal hold y receipt; nunca borrar datos sin aprobación.

**Microsecuencia obligatoria (respeta VID-Cxx-T01..T07):** 1. baseline SHA y diff; 2. contrastar código/documento y tests; 3. dibujar contrato/estado/permisos; 4. patchset archivo-a-archivo con pseudocódigo o código compilable según lenguaje real; 5. tests positivos, negativos y dos tenants donde proceda; 6. CI, restore/rollback y evidencias; 7. revisión Codex/arquitecto/founder. Ejecutar los dos gates `VID-C12-G01` y `VID-C12-G02` exactamente como los define el manifiesto; registrar bloqueos sin maquillarlos.

**Reporte:** `FreeBuff/reportes/VID-C12-REPORT.md` con SHA base/head, PR, rutas, código cambiado, comandos, exit codes, passed/failed/skipped, tests de seguridad, licencias, reversibilidad, riesgos y decisión PASS/PARTIAL/FAIL/BLOCKED. Si el gate falla, detener antes de la siguiente campaña.

### VID-C13 — SDK TypeScript/Hono y tool ACL

**Dependencia:** VID-C12. **Fuente:** `docs/campaigns/13-sdk-typescript-hono-y-tool-acl.md`; **scaffold:** `docs/implementation/13-sdk-typescript-hono-y-tool-acl/README.md`.

**Superficies que Freebuff debe verificar antes de editar:** `typescript/client.ts`, `typescript/hono.ts`, `typescript/agents.ts`, `typescript/types.ts`, `tests/typescript.test.mjs` (si alguna no existe, documentar y ajustar).

**Patchset específico a concretar contra HEAD:** Mantener 16/17 tools, allow-list, validate argumentos y download path; scopes por capability/tenant, grants, error taxonomy, timeout, no SSRF, stream auth, Hono host auth y tests negativos.

**Microsecuencia obligatoria (respeta VID-Cxx-T01..T07):** 1. baseline SHA y diff; 2. contrastar código/documento y tests; 3. dibujar contrato/estado/permisos; 4. patchset archivo-a-archivo con pseudocódigo o código compilable según lenguaje real; 5. tests positivos, negativos y dos tenants donde proceda; 6. CI, restore/rollback y evidencias; 7. revisión Codex/arquitecto/founder. Ejecutar los dos gates `VID-C13-G01` y `VID-C13-G02` exactamente como los define el manifiesto; registrar bloqueos sin maquillarlos.

**Reporte:** `FreeBuff/reportes/VID-C13-REPORT.md` con SHA base/head, PR, rutas, código cambiado, comandos, exit codes, passed/failed/skipped, tests de seguridad, licencias, reversibilidad, riesgos y decisión PASS/PARTIAL/FAIL/BLOCKED. Si el gate falla, detener antes de la siguiente campaña.

### VID-C14 — ADTC y reconciliación de export

**Dependencia:** VID-C13. **Fuente:** `docs/campaigns/14-adtc-y-reconciliacion-de-export.md`; **scaffold:** `docs/implementation/14-adtc-y-reconciliacion-de-export/README.md`.

**Superficies que Freebuff debe verificar antes de editar:** `agntia/jobs.py`, `agntia/storage.py`, `typescript/client.ts`, `docs/factory/03-TRACE-OBSERVABILITY.md` (si alguna no existe, documentar y ajustar).

**Patchset específico a concretar contra HEAD:** Añadir ADTC/event envelope versionado, correlation/causation, audit append-only, outbox con dedupe y receipts; reconciliar export generado vs entregado; no publicar.

**Microsecuencia obligatoria (respeta VID-Cxx-T01..T07):** 1. baseline SHA y diff; 2. contrastar código/documento y tests; 3. dibujar contrato/estado/permisos; 4. patchset archivo-a-archivo con pseudocódigo o código compilable según lenguaje real; 5. tests positivos, negativos y dos tenants donde proceda; 6. CI, restore/rollback y evidencias; 7. revisión Codex/arquitecto/founder. Ejecutar los dos gates `VID-C14-G01` y `VID-C14-G02` exactamente como los define el manifiesto; registrar bloqueos sin maquillarlos.

**Reporte:** `FreeBuff/reportes/VID-C14-REPORT.md` con SHA base/head, PR, rutas, código cambiado, comandos, exit codes, passed/failed/skipped, tests de seguridad, licencias, reversibilidad, riesgos y decisión PASS/PARTIAL/FAIL/BLOCKED. Si el gate falla, detener antes de la siguiente campaña.

### VID-C15 — QA y regresión audiovisual

**Dependencia:** VID-C14. **Fuente:** `docs/campaigns/15-qa-y-regresion-audiovisual.md`; **scaffold:** `docs/implementation/15-qa-y-regresion-audiovisual/README.md`.

**Superficies que Freebuff debe verificar antes de editar:** `tests/`, `tests/browser_smoke.py`, `tests/agent_integration.mjs`, `.github/workflows/test.yml` (si alguna no existe, documentar y ajustar).

**Patchset específico a concretar contra HEAD:** Golden audiovisual, cross-platform, ffprobe outputs, Playwright UI, fallos proveedores, concurrencia y artefactos de CI; no confiar solo en status de workflow.

**Microsecuencia obligatoria (respeta VID-Cxx-T01..T07):** 1. baseline SHA y diff; 2. contrastar código/documento y tests; 3. dibujar contrato/estado/permisos; 4. patchset archivo-a-archivo con pseudocódigo o código compilable según lenguaje real; 5. tests positivos, negativos y dos tenants donde proceda; 6. CI, restore/rollback y evidencias; 7. revisión Codex/arquitecto/founder. Ejecutar los dos gates `VID-C15-G01` y `VID-C15-G02` exactamente como los define el manifiesto; registrar bloqueos sin maquillarlos.

**Reporte:** `FreeBuff/reportes/VID-C15-REPORT.md` con SHA base/head, PR, rutas, código cambiado, comandos, exit codes, passed/failed/skipped, tests de seguridad, licencias, reversibilidad, riesgos y decisión PASS/PARTIAL/FAIL/BLOCKED. Si el gate falla, detener antes de la siguiente campaña.

### VID-C16 — Dos tenants sintéticos E2E

**Dependencia:** VID-C15. **Fuente:** `docs/campaigns/16-dos-tenants-sinteticos-e2e.md`; **scaffold:** `docs/implementation/16-dos-tenants-sinteticos-e2e/README.md`.

**Superficies que Freebuff debe verificar antes de editar:** `agntia/app.py`, `agntia/storage.py`, `typescript/hono.ts`, `tests/` (si alguna no existe, documentar y ajustar).

**Patchset específico a concretar contra HEAD:** Fixture dos tenants y dos actores + twins, leer/listar/subir/render/descargar/denegar cross-tenant, roles y aprobaciones; verificar contra motor Python y BFF, no solo mocks.

**Microsecuencia obligatoria (respeta VID-Cxx-T01..T07):** 1. baseline SHA y diff; 2. contrastar código/documento y tests; 3. dibujar contrato/estado/permisos; 4. patchset archivo-a-archivo con pseudocódigo o código compilable según lenguaje real; 5. tests positivos, negativos y dos tenants donde proceda; 6. CI, restore/rollback y evidencias; 7. revisión Codex/arquitecto/founder. Ejecutar los dos gates `VID-C16-G01` y `VID-C16-G02` exactamente como los define el manifiesto; registrar bloqueos sin maquillarlos.

**Reporte:** `FreeBuff/reportes/VID-C16-REPORT.md` con SHA base/head, PR, rutas, código cambiado, comandos, exit codes, passed/failed/skipped, tests de seguridad, licencias, reversibilidad, riesgos y decisión PASS/PARTIAL/FAIL/BLOCKED. Si el gate falla, detener antes de la siguiente campaña.

### VID-C17 — Hardening y costes

**Dependencia:** VID-C16. **Fuente:** `docs/campaigns/17-hardening-y-costes.md`; **scaffold:** `docs/implementation/17-hardening-y-costes/README.md`.

**Superficies que Freebuff debe verificar antes de editar:** `agntia/media.py`, `agntia/jobs.py`, `agntia/providers.py`, `package.json`, `pyproject.toml` (si alguna no existe, documentar y ajustar).

**Patchset específico a concretar contra HEAD:** Threat model, budgets de FFmpeg, quotas y proveedores, secret references Doppler-ready, SBOM/licencias, dependencias pinning, rate limits, logs redactados, restores.

**Microsecuencia obligatoria (respeta VID-Cxx-T01..T07):** 1. baseline SHA y diff; 2. contrastar código/documento y tests; 3. dibujar contrato/estado/permisos; 4. patchset archivo-a-archivo con pseudocódigo o código compilable según lenguaje real; 5. tests positivos, negativos y dos tenants donde proceda; 6. CI, restore/rollback y evidencias; 7. revisión Codex/arquitecto/founder. Ejecutar los dos gates `VID-C17-G01` y `VID-C17-G02` exactamente como los define el manifiesto; registrar bloqueos sin maquillarlos.

**Reporte:** `FreeBuff/reportes/VID-C17-REPORT.md` con SHA base/head, PR, rutas, código cambiado, comandos, exit codes, passed/failed/skipped, tests de seguridad, licencias, reversibilidad, riesgos y decisión PASS/PARTIAL/FAIL/BLOCKED. Si el gate falla, detener antes de la siguiente campaña.

### VID-C18 — Release y aprobación

**Dependencia:** VID-C17. **Fuente:** `docs/campaigns/18-release-y-aprobacion.md`; **scaffold:** `docs/implementation/18-release-y-aprobacion/README.md`.

**Superficies que Freebuff debe verificar antes de editar:** `README.md`, `AGENTS.md`, `docs/typescript-agents.md`, `.github/workflows/test.yml`, `docs/factory/HANDOFF-ARCHITECT-FOUNDER.md` (si alguna no existe, documentar y ajustar).

**Patchset específico a concretar contra HEAD:** Paquetes reproducibles SDK Python/TS, smoke de instalación Windows/Linux, runbook, versionado, matrix de compatibilidad padre, propuesta de patchset no aplicada, aceptación founder.

**Microsecuencia obligatoria (respeta VID-Cxx-T01..T07):** 1. baseline SHA y diff; 2. contrastar código/documento y tests; 3. dibujar contrato/estado/permisos; 4. patchset archivo-a-archivo con pseudocódigo o código compilable según lenguaje real; 5. tests positivos, negativos y dos tenants donde proceda; 6. CI, restore/rollback y evidencias; 7. revisión Codex/arquitecto/founder. Ejecutar los dos gates `VID-C18-G01` y `VID-C18-G02` exactamente como los define el manifiesto; registrar bloqueos sin maquillarlos.

**Reporte:** `FreeBuff/reportes/VID-C18-REPORT.md` con SHA base/head, PR, rutas, código cambiado, comandos, exit codes, passed/failed/skipped, tests de seguridad, licencias, reversibilidad, riesgos y decisión PASS/PARTIAL/FAIL/BLOCKED. Si el gate falla, detener antes de la siguiente campaña.

## Contratos de integración, sin aplicar al padre

```ts
// Propuesta de puerto nuevo, no API ya implementada:
interface VideoPrincipal {
  tenantId: string; subjectId: string; actorKind: 'human' | 'agent-twin';
  canonicalAgentId?: string; capabilities: readonly string[];
}
interface VideoCommandContext {
  principal: VideoPrincipal; correlationId: string;
  idempotencyKey: string; approvalId?: string;
}
interface VideoJobReceipt {
  jobId: string; projectId: string; tenantId: string;
  state: 'queued' | 'running' | 'done' | 'error' | 'cancelled';
  outputSha256?: string; completedAt?: string;
}
// Autorizar en BFF Y motor; tenantId del payload nunca prueba identidad.
// El plan de render es inmutable; exportar no publica.
```

**Doppler-ready:** `FreeBuff/DOPPLER-READY.md` a producir durante VID-C17: nombres de variables y scopes por entorno, `AGNTIA_ACCESS_TOKEN` legacy, `AGNTIA_DATA_DIR`, `AGNTIA_INBOX_DIR`, `DEEPSEEK_API_KEY`, `GEMINI_API_KEY` y futuras refs; sin valores secretos ni conexión real. Config fail-closed y rotación. **Padre:** `FreeBuff/INTEGRATION-AGENTE-PROPOSAL.md` a producir en VID-C18 con versión SDK, BFF/Hono, twins, permisos, eventos, approvals, health, E2E y rollback; no editar repo padre.

## Prompt maestra de Freebuff

> Eres el implementador del scaffolding integral de `agntia-video`, no de un MVP nuevo. Tu fuente de verdad es el código y las 18 campañas recovery ya integradas en main. Empieza por fijar SHA, inventariar TODO el árbol y ejecutar el baseline. Respeta la arquitectura Python/FFmpeg + TS/Hono, la edición 0.4, revision/409 y los 16/17 tools. Revisa la meta-auditoría conceptual Astra y detente si está pendiente de aprobación. Para cada VID-C01..C18, lee el manifiesto y documento completo, identifica delta real, concreta paths y código, implementa patchset en rama independiente, corre tests y gates, entrega reporte verificable, solicita revisión Codex/arquitecto/founder. No cambies padre ni gestoría, no instales Doppler, no conectes proveedores ni declares producción. Tras VID-C18, entrega `FreeBuff/FOUNDER-FINAL-REPORT.md` con matriz 18×(tareas/gates), pruebas, deuda, licencias, backups, Doppler-ready y propuesta de integración. No avanzar con FAIL/BLOCKED.

**Definición de cierre de este documento:** solo plan y handoff revisable; no equivale a ejecución, hardening ni aprobación.
