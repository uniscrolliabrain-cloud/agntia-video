# Roadmap de integración — agntia-video

> Orden propuesto **9/14** · 2026-11-15 · Rama `docs/roadmap-integracion-agente-20261115`. Documento complementario a campañas existentes, no sustituye su trabajo.

## Estado y objetivo

**Dominio:** Edición, podcast, clips y exportación.

**README actual:** MVP v0.4 y paquete @agntia/video declarados. Este estado es declarado, no una certificación de código. Reauditar código, ramas, PRs, tests y reportes antes de empezar.

**Resultado esperado:** Briefing, proyecto, render job y exportación verificable. El producto debe poder usarse por un humano desde `agente` sin que intervenga ningún LLM.

## Landmarks y proceso secuencial

**L0 — Baseline:** inventariar `main`, todas las ramas y PRs, reconciliar sin pérdidas, leer documentación, código y reportes, ejecutar tests y registrar SHA. Nunca borrar o reescribir código existente sin auditoría.

**L1 — Terminar el hijo:** ejecutar campañas pendientes, completar software y SDK/adaptadores, schemas Zod/TS, persistencia, seguridad, permisos, pruebas, CI y métricas. Preservar implementaciones existentes; construir desde cero solo lo ausente.

**L2 — Contrato de integración:** bundle versionado de capabilities, SOPs, skills, pipelines, políticas, efectos, aprobaciones, idempotencia, retries, eventos y receipts. Documentar compatibilidad y rollback.

**L3 — Desarrollar `agente` en paralelo:** crear dominio padre, proyecciones, endpoints, UI humana, registro de capacidades, wiring kernel/policy/worker/event bus, autenticación/tenant y observabilidad. Mantener coordinación de contratos mientras se termina el hijo; certificar las integraciones **una por una**.

**L4 — Dogfooding humano:** demostrar briefing, proyecto, render job y exportación verificable con datos de empresa interna, desde la UI y sin LLM. Documentar fallos y repetir.

**L5 — Certificación:** smoke, unit, integración, E2E, adversarial, aislamiento multi-tenant, approvals, fallos, duplicados, replay de proyecciones, DLQ, rollback, métricas p50/p95 y evidencia verificable.

**L6 — Slow LLM:** añadir propuestas tipadas del motor cognitivo para el kernel; el kernel autoriza y el runtime ejecuta. Ningún LLM puede ejecutar efectos directamente.

**L7 — Fast harness conversacional:** Laia y otros agentes son **interfaces humanas** con identidad y memoria compartidas entre chat y Anam. El `FastConversationV2` no depende de RAG profundo, slow LLM ni workers para emitir primer token. Context card empresarial precargada; `IntentBridge` asíncrono; `ProgressProjector` de eventos confirmados. La animación SVG y cinco fases pedagógicas son representación narrativa, no estados técnicos exactos; jamás anunciar un efecto no confirmado. Barge-in detiene audio, no trabajo aprobado.

**L8 — Release:** canary, dos empresas dogfood, seguridad/RGPD, SLO, costes, runbook, reversibilidad y aprobación del founder. Dejar reportes de aprendizaje por campaña.

## Contrato vertical mínimo

`Solicitud humana → FastConversationV2 → IntentBridge → kernel/approval → capability del hijo → runtime/effect receipt → evento → UI/progress presenter → Laia`.

La tarjeta de Laia solo contiene contexto de negocio, identidad, tono, límites y situación del cliente. No incluir detalles técnicos de workers o SOPs en el prompt del agente.

## Orden de integración propuesto

1. agntia-ciberseguridad
2. agntia-clientes
3. agntia-gestoria
4. agntia-comunicacion
5. agntia-ventas
6. agntia-finanzas
7. agntia-redes
8. agntia-marketing
9. agntia-video **← este repo**
10. agntia-branding
11. agntia-dise-o
12. agntia-legal
13. agntia-seguros
14. agntia-formacion

El orden podrá ajustarse por dependencias encontradas en L0. Trabajo en repos hijos puede ser paralelo; integración y certificación en `agente` se cierran una a una, empezando por ciberseguridad.

## Handoff para el agente ejecutor

Auditar primero `main`, ramas, PRs, código y reportes; entregar baseline con SHA, rutas, líneas y pruebas. Proponer patchsets pequeños, registrar informe al final de cada campaña, no sobrescribir trabajo de otros agentes. Preparar y acordar contrato con el desarrollador de `agente` antes de cambios incompatibles. Marcar cada landmark como `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED` o `VERIFIED` con evidencia; nunca declarar producción por documentación.

**Estado:** roadmap escrito; no se han ejecutado pruebas ni modificado código en este cambio.
