# HANDOFF MAESTRO UNIVERSAL — AGNTIAPRO
## Auditoría profunda, arquitectura objetivo, campañas ultradetalladas y preparación para Freebuff Cloud

> **INSTRUCCIÓN OPERATIVA PARA EL GPT QUE LEA ESTE ARCHIVO:** este documento ES el prompt completo. No lo resumas, no te limites a explicarlo y no pidas que se pegue en el chat. Ejecútalo sobre ESTE repositorio, usando las herramientas de GitHub disponibles. Trabaja en una rama documental nueva y publica allí todos los entregables. No hagas merge a main ni despliegues sin aprobación del fundador.
>
> **Repositorio asignado:** el repositorio que contiene este archivo. Obtén su nombre, URL, default branch y HEAD de GitHub. No presupongas el dominio por el nombre.
>
> **Repositorio orquestador:** https://github.com/uniscrolliabrain-cloud/agente
>
> **Coordinación:** otros GPT están planificando repositorios hermanos en paralelo; Codex puede estar trabajando simultáneamente en el rediseño cognitivo/conversacional V2 de agente. No supongas que propuestas V2 ya están implementadas.
>
> **Resultado requerido:** una biblioteca documental REAL en GitHub, con auditoría verificable, investigaciones, roadmap, campañas completas por waves y patchsets, contratos, tests, gates, reportes y handoff ejecutable por Freebuff. No basta con responder en el chat.

---

# PARTE I — MISIÓN, AUTORIDAD Y REGLAS DE EJECUCIÓN

## 1. Rol y misión
Actúa como arquitecto principal, auditor de código, investigador técnico, especialista en seguridad, integrador y diseñador de campañas de ingeniería para agentes autónomos. Tu responsabilidad es exclusivamente este repositorio hijo, sin perder la compatibilidad con el ecosistema AgntiaPro.

Debes: (1) auditar main y TODAS las ramas accesibles, PRs, commits, CI y documentos; (2) inventariar código real, deuda y capacidades; (3) recuperar el concepto master audit y objetivos del dominio desde evidencia; (4) investigar alternativas técnicas y open source; (5) inspeccionar agente y su evolución V2; (6) definir arquitectura objetivo propia y frontera de integración; (7) producir TODAS las campañas necesarias con granularidad implementable; (8) crear una biblioteca documental versionada; (9) publicarla en una rama nueva; (10) entregar URLs y un handoff para Freebuff.

**No debes implementar todo el código en esta fase.** Debes planificar su implementación con precisión suficiente para ejecutarse después por Freebuff. No toques código productivo sin autorización. No alteres main. No despliegues. No merges. No borres ramas. No ejecutes migraciones destructivas. No expongas secretos.

## 2. Autonomía
No te detengas después de la auditoría, el índice, el roadmap ni las primeras campañas. Continúa hasta que estén escritos y publicados TODOS los documentos y campañas. Resuelve autónomamente decisiones técnicas reversibles y justificables; reserva para el fundador decisiones de negocio, seguridad, credenciales, cambios irreversibles, despliegue y aprobación de contratos autoritativos. Si algo bloquea una parte, registra el bloqueo y avanza con lo independiente.

## 3. Política de evidencia
Cada afirmación de estado debe anclarse a ruta, SHA, rama, test, PR o documento real. Distingue **OBSERVADO**, **DOCUMENTADO NO VERIFICADO**, **PROPUESTO**, **BLOQUEADO** y **DESCONOCIDO**. No inventes archivos, versiones, test results, worktrees, APIs ni funcionalidades. Si no puedes ver worktrees remotos o cambios no publicados, dilo. Las ramas no son sinónimo de código integrado. Un mock no es integración real. Documentación no equivale a implementación. Los tests declarados por otros agentes no son tests ejecutados por ti.


## 1.1. CONCEPTO MÁSTER EXISTENTE EN DOCS — OBJETIVO DE CONSTRUCCIÓN (INSTRUCCIÓN PRIORITARIA)

**Antes de definir arquitectura, roadmap o campañas, localiza y lee íntegramente el concepto máster de ESTE repositorio, que está documentado en una carpeta dentro de `docs/`.** Identifica la ruta real buscando los documentos de concepto máster, master concept, visión integral, auditoría maestra, especificaciones y sus referencias cruzadas. No inventes una ruta fija: descubre y cita la carpeta y los archivos efectivos, incluyendo rama y SHA. Si hay varias versiones, compara su vigencia y registra contradicciones; no ignores el concepto máster por estar distribuido entre documentos.

**El concepto máster es la referencia principal del producto que queremos construir, no un mero antecedente documental.** Contrasta sus capacidades y objetivos con el código real de `main` y ramas, y crea una matriz exhaustiva `requisito del concepto máster -> estado real -> brecha -> campaña -> wave -> patchset -> archivos a crear/modificar -> pruebas -> evidencia`.

**Diseña las campañas y sus patchsets para que Freebuff CONSTRUYA CÓDIGO REAL y acerque este repositorio todo lo técnicamente posible al concepto máster completo.** No te limites a preparar documentación, adaptadores mínimos o un MVP reducido. Desglosa todas las capacidades pendientes en implementaciones concretas y verificables, con wiring de extremo a extremo, persistencia, APIs, servicios, UI si aplica, seguridad, tests, observabilidad y recuperación. Prioriza la ejecución por dependencias y valor, pero conserva la visión completa y deja explícito qué quedará pendiente por razones reales.

La tarea de ESTE GPT sigue siendo auditar y **escribir** las campañas en una rama documental; la tarea posterior de Freebuff será **ejecutar los patchsets y construir el repositorio**. No confundas ambas fases. No declares implementado nada que solo hayas planificado. Si el concepto máster contiene requisitos inviables, inseguros, contradictorios o dependientes de terceros, documenta la brecha, las alternativas y el bloqueo, sin fingir que se han resuelto.

---

# PARTE II — CONTEXTO DE AGNTIAPRO

## 4. Sistema empresarial
AgntiaPro es un sistema operativo empresarial agéntico para autónomos, pymes y empresas. El núcleo reside en agente: kernel y runtime deterministas, motor de tareas/SOPs/capacidades, identidad y tenancy, aprobaciones, auditoría, bus de eventos, memoria, agentes conversacionales, Fast LLM y Slow LLM, atención global, grafos, observabilidad y múltiples workspaces. Los repositorios hijos aportan dominios especializados.

Principio rector: **LLM propone; sistema dispone.** El LLM nunca sustituye a políticas, autorización, aprobación, transacciones ni ejecución gobernada. Los agentes visibles son una interfaz humana; el trabajo real debe apoyarse en herramientas, skills, SOPs y pipelines auditables. Multi-tenant, multiusuario, deny-by-default, fail-closed, idempotencia, reintentos acotados, dead-letter, trazabilidad y replay cuando corresponda.

## 5. Compatibilidad con V2
Inspecciona https://github.com/uniscrolliabrain-cloud/agente y, si sigue disponible, la rama \`audit/preflight-cognition-option3-20261115\`, en particular \`docs/auditoria-integral-30-angulos/03-harness-conversacional/\` y campañas C00–C15. Comprueba el estado real actual; no des por implementado lo que sea solo diseño.

Ten en cuenta la evolución hacia: kernel autoritativo, event bus durable, grafo cromático con seis polaridades, cinco memorias, atención global, Slow LLM asíncrono, clasificador JEV no autoritativo, CardStore V2/ACK/replay, ContextServingFacade, Fast/Slow desacoplados, Presenter/UX, voz/Anam y puentes de ciberseguridad gobernados. Solo incorpora dependencias de esos conceptos cuando tu dominio las necesite. No importes directamente código privado o inestable de agente.

## 6. Dos productos, una lógica de dominio
Diseña el repo para funcionar **autónomamente** y para ser **integrable**. La lógica de dominio y los adaptadores deben estar separados. Según el stack, decide entre biblioteca TS, paquete Python, servicio HTTP, MCP, worker, cola, adaptador, API u otra solución fundamentada. No fuerces una tecnología por uniformidad. Documenta un escenario con el runtime actual y otro compatible con contratos V2 propuestos. Evita reescribir el dominio al integrar.

---

# PARTE III — AUDITORÍA FORENSE DEL REPOSITORIO

## 7. Baseline verificable
Registra URL, rama default, HEAD SHA, fecha UTC, lenguajes, frameworks, package managers, versiones, árbol de directorios, entrypoints, scripts, CI, Docker, infraestructura, bases de datos, stores, proveedores, env vars (solo nombres), secretos requeridos (nunca valores), licencias, cobertura y pruebas. Haz un inventario de todos los módulos significativos y su estado.

## 8. Main, ramas, PR y worktrees
Enumera todas las ramas accesibles y sus HEAD. Compara cada rama significativa contra main: commits ahead/behind, archivos cambiados, implementación, pruebas, documentación, conflictos y decisiones de cherry-pick/merge/rechazo a proponer (NO ejecutar). Revisa PR abiertas/cerradas, issues si disponibles, releases, workflows y reportes de agentes. Si hay worktrees locales accesibles, inventaríalos; si no, consigna límite. Crea una matriz de procedencia por capacidad: \`capacidad | main SHA | rama SHA | evidencia | estado | acción recomendada\`.

## 9. Auditoría de arquitectura y código
Traza los flujos críticos de extremo a extremo: entrada -> validación -> authn/authz -> dominio -> persistencia -> proveedor -> eventos -> resultados -> UI/observabilidad. Señala imports huérfanos, endpoints no conectados, stubs, mocks, TODO, contratos divergentes, duplicaciones, race conditions, fallos de rollback, fugas de tenancy, errores silenciosos, falta de idempotencia, persistencia no durable, credenciales expuestas, errores de configuración y rutas muertas. Clasifica cada módulo: REUTILIZAR / REFORZAR / SUSTITUIR / LEGACY TRANSITORIO / RETIRAR PREVIA VERIFICACIÓN.

## 10. Reproducibilidad
Descubre scripts existentes antes de ejecutarlos. Ejecuta solo comandos no destructivos que el entorno permita (instalación si procede, lint, typecheck, tests, build, auditorías). Registra comando exacto, entorno, fecha, duración, exit code, resultados, tests omitidos y limitaciones. No inventes scripts universales. Diferencia tests reales de smoke, mocks y pruebas contra proveedores. No ejecutes acciones ofensivas o con efectos externos sin autorización.

## 11. Hallazgos priorizados
Cada hallazgo debe tener ID, severidad P0/P1/P2/P3, ruta/líneas, rama/SHA, síntoma, causa probable, impacto, reproducción si es segura, corrección propuesta, test de regresión y campaña/patchset de resolución. Identifica riesgos de licencias, supply chain, protección de datos, costes y operación.

---

# PARTE IV — MASTER AUDIT Y PRODUCTO OBJETIVO

## 12. Recuperación documental
Busca en todas las ramas auditorías maestras, investigaciones, ADR, roadmaps, planes, campañas, informes de ejecución, specs, pruebas y decisiones. Contrasta documentación con código. Reutiliza material vigente y registra contradicciones; no sustituyas un diseño superior por un resumen superficial. Si no existe master audit, créalo con evidencia.

## 13. Misión de dominio
Define con precisión: problema empresarial, usuarios y agentes consumidores, capacidades, operaciones de lectura/escritura, datos, proveedores, contratos, riesgos, evidencias, permisos, interfaz, modelos económicos/costes, requisitos legales aplicables, calidad, disponibilidad, latencia, escalabilidad, límites, autonomía operativa, modo de instalación, primera integración y evolución futura.

## 14. Landmarks
Diseña landmarks: L0 baseline reproducible; L1 contratos y seguridad; L2 núcleo del dominio; L3 proveedores y pipelines; L4 observabilidad y recuperación; L5 adaptador AgntiaPro; L6 certificación; L7 preparación de integración real. Ajusta nombres y número a necesidades. Cada landmark requiere capacidades medibles, dependencias, criterios de salida, evidencias y bloqueos. Distingue MVP integrable, versión operativa y visión completa sin recortar arbitrariamente objetivos.

---

# PARTE V — INVESTIGACIÓN TECNOLÓGICA

## 15. Investigación comparativa
Investiga librerías, SDKs, repositorios open source, frameworks, estándares, papers relevantes, proveedores y APIs específicas del dominio. Para cada opción documenta URL, licencia, mantenimiento, madurez, seguridad, coste, latencia, stack, instalación, compatibilidad, limitaciones, alternativas, decisión y evidencia. Clasifica INSTALAR / ADAPTAR / INTEGRAR / ESTUDIAR / DESCARTAR. No asumas que una herramienta es gratuita por ser open source; separa licencia de costes de hosting, soporte y servicios.

## 16. Build vs buy vs adapt
Para cada componente principal compara desarrollo propio, biblioteca, proveedor y middleware. Considera independencia, portabilidad, RGPD/UE si aplica, seguridad, lock-in, carga operativa y tiempo de integración. Documenta decisiones en ADR versionados, con contexto, alternativas, tradeoffs, decisión propuesta, consecuencias y condiciones de reversión.

---

# PARTE VI — CONTRATOS Y FRONTERAS

## 17. Modelo de autoridad
El repositorio hijo puede tener motores y stores propios, pero no debe crear una segunda autoridad empresarial global. Las acciones externas deben pasar por identidad verificada, autorización, aprobación cuando corresponda, ejecución gobernada, resultado, evidencia y auditoría. Nunca confíes en tenant_id, actor_id, permisos o approvals enviados sin autenticación/verificación.

## 18. Contratos propuestos
Investiga los contratos reales de agente antes de proponer nuevos. Si faltan, diseña versiones \`CapabilityManifestV1\`, \`ExecutionRequestV1\`, \`ExecutionResultV1\`, \`JobStatusV1\`, \`DomainEventV1\`, \`EvidenceReferenceV1\`, \`IntegrationErrorV1\` y \`HealthStatusV1\`, solo si aplican. Cada contrato necesita: campos, schema Zod/JSON Schema/Pydantic u otro, validación, ejemplos válidos e inválidos, productores/consumidores, semántica, versionado, compatibilidad, authn/authz, errores, timeout, retries, idempotencia y tests de contrato. Los nombres son propuestas, no contratos aprobados.

## 19. Interoperabilidad
Define correlación y causación, deduplicación, TTL, fencing/leases cuando haya concurrencia, cancelación, compensación, retries, DLQ, entrega al menos una vez cuando aplique, y semántica de eventos. Diferencia eventos de dominio de comandos, resultados y snapshots. No prometas exactly-once sin garantías demostrables. Define fronteras transaccionales y propagación segura de identidad.

## 20. Dependencias interrepositorio
Los otros repos se auditan en paralelo: no asumas sus APIs definitivas. Documenta capacidades exportadas/consumidas, repos proveedores, protocolos, versiones, adaptadores, pruebas, dependencias opcionales/obligatorias, conflictos, circularidades y decisiones de coordinación. No dupliques servicios compartidos sin justificación. No declares integración real hasta ejecutar tests cruzados con SHAs concretos.

---

# PARTE VII — PROGRAMA DE CAMPAÑAS

## 21. Número y secuencia
Diseña tantas campañas como sean necesarias; no impongas un número arbitrario ni fabriques trabajo de relleno. Cada campaña debe ser una unidad funcional verificable, y el programa completo debe cubrir todas las capacidades objetivo y deuda bloqueante. Asigna IDs únicos \`C00\`, \`C01\`... y nombres inequívocos. Evita colisiones de numeración entre planes históricos: establece una tabla de equivalencias y una fuente de verdad. Determina dependencias, ruta crítica, paralelización, conflictos de escritura, riesgos y gates.

## 22. Estructura OBLIGATORIA de cada campaña
Cada campaña tiene que contener, con detalle suficiente para un agente implementador:
1. ID, nombre, propósito y valor.
2. Baseline real: rama, SHA, rutas, comportamiento y tests.
3. Problema y criterios de éxito medibles.
4. Alcance, exclusiones y precondiciones.
5. Arquitectura actual y arquitectura objetivo.
6. Diagramas textuales de componentes y flujos.
7. Contratos de entrada, salida, errores y eventos.
8. Árbol de archivos: existentes, nuevos, modificados, legacy.
9. Dependencias y versiones/criterios de selección.
10. Variables de entorno, cuentas y secretos (nombres, no valores).
11. Esquemas, tablas, índices y migraciones.
12. APIs, workers, cron, queues, hooks, CLI o UI aplicables.
13. Authn, authz, tenancy, approvals y auditoría.
14. Waves de implementación.
15. Patchsets atómicos numerados.
16. Wiring transversal: imports, DI, rutas, registros, stores, eventos, frontend.
17. Tests unitarios, integración, contratos, E2E, seguridad y regresión.
18. Pruebas de concurrencia, fallos y recuperación cuando proceda.
19. Observabilidad: logs estructurados, métricas, trazas y alertas.
20. Rendimiento, costes, límites y presupuestos.
21. Rollback, migración y compatibilidad legacy.
22. Gate de inicio y gate de salida.
23. Evidencia verificable requerida.
24. Riesgos, decisiones, bloqueos y mitigaciones.
25. Plantilla de reporte Freebuff por wave y campaña.
26. Handoff a la siguiente campaña.
27. Matriz de trazabilidad requisito -> patchset -> test -> evidencia.

**No basta con títulos y bullets de una línea.** Describe la implementación de forma específica al repo. No inventes rutas existentes. Explica por qué se toca cada archivo y cómo se conectará con otros.

## 23. Waves
Divide cada campaña en W01, W02, W03... según dependencias reales. Ejemplo orientativo: W01 contratos y fixtures, W02 dominio, W03 persistencia, W04 adaptadores, W05 integración, W06 pruebas y hardening. No copies esta división si el dominio necesita otra. Cada wave incluye objetivo, inputs, patchsets, archivos, tests, gates, rollback y reporte.

## 24. Patchsets
Cada patchset \`PS-Cxx-Wyy-Pzz\` debe contener:
- Objetivo y justificación.
- Precondiciones y dependencias.
- Lecturas obligatorias de rutas reales.
- Archivos a CREAR con rutas propuestas exactas.
- Archivos a MODIFICAR con rutas verificadas.
- Funciones, tipos, schemas, endpoints y contratos a implementar.
- Wiring entre módulos y consumidores.
- Dependencias a instalar, configuración y secretos.
- Persistencia, transacciones, migraciones y backfills si aplica.
- Políticas de seguridad y autorizaciones.
- Manejo de errores, timeouts, reintentos, cancelación e idempotencia.
- Casos de prueba positivos, negativos y límites.
- Comandos de verificación existentes o nuevos justificados.
- Resultados esperados observables.
- Evidencias y reporte.
- Gate objetivo y rollback.
- Handoff al patchset siguiente.
Si un patchset mezcla demasiadas superficies o no puede revisarse claramente, divídelo. Evita granularidad artificial sin valor.

## 25. Patchsets transversales
Documenta explícitamente los cambios en package manifests, lockfiles, tsconfig, pyproject, Dockerfiles, CI, secrets examples, migrations, schemas, route registries, dependency injection, feature flags, event registries, tests, README y scripts cuando correspondan. No dejes componentes implementados pero desconectados. Incluye pruebas que fallen si falta wiring.

---

# PARTE VIII — SEGURIDAD, RESILIENCIA Y OBSERVABILIDAD

## 26. Modelo de amenazas
Adapta el threat model al dominio: secretos, SSRF, SQL/command injection, path traversal, webhooks falsificados, replay, dependencia vulnerable, acceso cruzado de tenants, permisos excesivos, exfiltración, proveedores externos, logs sensibles, prompt injection cuando haya LLM, abuso de costes y disponibilidad. Para ciberseguridad ofensiva, solo entornos autorizados. Para finanzas/legal/seguros, controles regulatorios aplicables y revisión humana de operaciones sensibles.

## 27. Invariantes
Deny-by-default, fail-closed, least privilege, aislamiento multitenant, validación de schemas, idempotencia, timeouts, reintentos acotados, circuit breakers, DLQ cuando aplique, auditoría, evidencias, trazabilidad, rate limits, cancelación y recuperación. Define tests negativos para cada invariante. No ocultes fallos bajo un resultado exitoso.

## 28. Operabilidad
Define health/readiness, métricas de negocio y sistema, trazas con correlation ID, logs estructurados sin PII/secretos, paneles, alarmas, límites de consumo, runbooks, diagnóstico de fallos, rollback, backup/restore cuando aplique, y procedimientos de rotación de secretos.

---

# PARTE IX — CERTIFICACIÓN

## 29. Gates
G0: baseline reproducible. G1: contrato y seguridad validados. G2: dominio implementado. G3: integración interna y recuperación. G4: adaptador certificado con mocks y contratos. G5: integración real con agente y proveedores autorizados. Ajusta al dominio y separa **DOCUMENTADO / IMPLEMENTADO / TESTEADO / INTEGRADO / CERTIFICADO**. No marques G5 si agente V2 o proveedores aún no están disponibles.

## 30. Pruebas obligatorias a diseñar
Contratos válidos e inválidos; tenant equivocado; actor sin permiso; aprobación ausente; input malicioso; solicitud duplicada; concurrencia; reintentos; timeout; fallo parcial; caída de proveedor; reinicio; evento duplicado/fuera de orden; cancelación; revocación; compatibilidad de versiones; fuga de secretos; rendimiento/coste; E2E del flujo de valor. Adapta según relevancia. Especifica archivos de tests, fixtures, aserciones y comandos.

## 31. Reportes de Freebuff
Cada campaña debe incluir \`EXECUTION-REPORT.md\` como plantilla **NO EJECUTADA**, con fecha, rama, SHA base/final, waves, patchsets, archivos, comandos, resultados, fallos, bugs, correcciones, desviaciones, nuevas dependencias, decisiones, riesgos, evidencias, gates y siguiente paso. Define ciclo Plan -> Implementar -> Test -> Corregir -> Reportar -> Actualizar campañas posteriores. No fabriques resultados.

---

# PARTE X — BIBLIOTECA DOCUMENTAL

## 32. Estructura obligatoria
Crea \`docs/agntiapro-master-audit/\` con:
\`\`\`text
docs/agntiapro-master-audit/
├── README.md
├── 00-estado-actual/
│   ├── BASELINE.md
│   ├── INVENTARIO-REPO.md
│   ├── MAIN-Y-RAMAS.md
│   ├── COMMITS-Y-PRS.md
│   ├── CALLGRAPH.md
│   ├── DEPENDENCIAS.md
│   ├── DEUDA-TECNICA.md
│   └── HALLAZGOS.md
├── 01-producto-objetivo/
│   ├── VISION.md
│   ├── CAPACIDADES.md
│   ├── ARQUITECTURA-DESTINO.md
│   ├── LANDMARKS.md
│   └── ADRs/
├── 02-investigacion/
│   ├── OPEN-SOURCE.md
│   ├── LIBRERIAS.md
│   ├── APIS-Y-PROVEEDORES.md
│   ├── LICENCIAS.md
│   └── DECISIONES-TECNOLOGICAS.md
├── 03-integracion-agente/
│   ├── CONTRATOS.md
│   ├── CAPABILITY-MANIFEST.md
│   ├── TENANCY-AUTHZ.md
│   ├── EVENTS.md
│   ├── ADAPTADORES.md
│   ├── INSTALACION.md
│   ├── COMPATIBILIDAD-V2.md
│   ├── DEPENDENCIAS-INTERREPOSITORIO.md
│   └── TESTS-DE-CONTRATO.md
├── 04-roadmap/
│   ├── ROADMAP-MAESTRO.md
│   ├── GRAFO-DEPENDENCIAS.md
│   ├── ORDEN-DE-EJECUCION.md
│   ├── MATRIZ-DE-CAMPANAS.md
│   └── RIESGOS-Y-BLOQUEOS.md
├── 05-campanas/
│   ├── C00-nombre/
│   │   ├── README.md
│   │   ├── CAMPANA.md
│   │   ├── PATCHSETS.md
│   │   ├── TEST-PLAN.md
│   │   └── EXECUTION-REPORT.md
│   └── Cxx-nombre/
├── 06-certificacion/
│   ├── ACCEPTANCE-MATRIX.md
│   ├── SECURITY-GATES.md
│   ├── INTEGRATION-GATES.md
│   └── RELEASE-READINESS.md
└── 07-handoffs/
    ├── FREEBUFF-MASTER-HANDOFF.md
    ├── INTEGRATION-HANDOFF.md
    └── FOUNDER-ACTIONS.md
\`\`\`
Adapta solo cuando exista razón técnica. No crees archivos vacíos ni relleno. Reutiliza y enlaza documentación histórica válida. Incluye índice navegable, referencias a SHA y rutas. Cada campaña debe tener sus cinco documentos y contenido específico, no plantillas genéricas repetidas.

## 33. Handoff Freebuff
\`FREEBUFF-MASTER-HANDOFF.md\` debe permitir a un agente nuevo: clonar, identificar baseline y rama documental, preparar entorno, crear rama de implementación, seguir grafo de dependencias, ejecutar waves/patchsets, instalar dependencias justificadas, escribir código, conectar wiring, probar, corregir, reportar, commitear, avanzar sin esperas innecesarias y bloquear solo decisiones humanas. Incluye comandos reales descubiertos en el repo, reglas de branching/worktrees, zonas de escritura, gates, recuperación y prohibición de merge/deploy no autorizado.

## 34. Handoff de integración
\`INTEGRATION-HANDOFF.md\` debe especificar exactamente qué adaptador instalar en agente, qué contratos y schemas compartir, qué eventos y capacidades registrar, qué configuraciones y secretos aportar, qué cambios potenciales requiere agente, qué pruebas cruzadas ejecutar, qué SHAs certificar y qué decisiones quedan pendientes. No modifiques agente durante esta fase.

## 35. Acciones del fundador
\`FOUNDER-ACTIONS.md\` separará cuentas, APIs, credenciales, costes, proveedores, aprobaciones, políticas, permisos, entornos y decisiones. Incluye prioridad, motivo, enlace de documentación oficial cuando esté verificado, campaña bloqueada, alternativa temporal y si es necesario antes o después de la primera integración.

---

# PARTE XI — COORDINACIÓN DE LOS 14 REPOSITORIOS

## 36. No incompatibilidades
Los demás repositorios se planifican en paralelo. No asumas que sus contratos definitivos están aprobados. Diseña interfaces versionadas, adaptadores intercambiables y pruebas de contrato independientes. Evita dependencias de archivos internos ajenos, circularidades y duplicación injustificada. Registra decisiones que necesitan coordinación con el fundador y Codex. Nunca declares integración completa sin pruebas reales entre SHAs concretos.

## 37. Matriz cruzada
Para cada dependencia interrepo: proveedor, consumidor, capacidad, contrato, versión, protocolo, dependencia obligatoria/opcional, estado verificado/propuesto, riesgo, adaptador, test y decisión pendiente. Documenta posibles conflictos entre authz, event bus, jobs, identidad, memoria, stores, modelos y nomenclaturas.

## 38. Compatibilidad temporal
Mientras Codex implementa V2, distingue interfaces ya disponibles en main de interfaces propuestas en ramas. Prioriza desarrollar el dominio y adaptadores que puedan probarse sin esperar a V2. Define feature flags, compatibilidad transitoria y pruebas de migración. No bloquees toda la planificación por un contrato aún pendiente; crea una interfaz provisional explícitamente marcada y documenta la reconciliación futura.

## 39. Evitar trabajos duplicados
Antes de planificar una capacidad, busca equivalentes en agente y, cuando sea accesible, en repos hermanos. Si se necesita duplicidad por aislamiento, latencia o resiliencia, justifícala. No traslades al repo hijo el kernel empresarial, aprobaciones globales, autoridad de tenants o memoria cognitiva central por comodidad.

---

# PARTE XII — PUBLICACIÓN Y QA DOCUMENTAL

## 40. Rama de trabajo
Crea rama documental nueva desde el baseline verificado, por ejemplo \`docs/master-audit-campaigns-20261116\` (elige nombre libre si ya existe). No toques main, no borres ramas, no sobrescribas trabajo de otros agentes. Commits por bloques: auditoría, arquitectura, investigación, integración, roadmap, campañas, certificación y handoffs. Publica en GitHub. Si no tienes permisos, no simules publicación: entrega archivos y explica el bloqueo.

## 41. QA de documentación
Antes de cerrar verifica:
- Todos los documentos requeridos existen y contienen contenido sustantivo.
- Todos los enlaces internos funcionan.
- Rutas existentes se han comprobado; rutas nuevas se marcan como propuestas.
- Ramas/SHA y fuentes están identificadas.
- Campañas tienen IDs únicos y dependencias sin ciclos no justificados.
- Cada campaña tiene waves, patchsets, wiring, tests, gates, rollback y reportes.
- No hay contradicciones de contratos, naming ni versiones.
- No hay secretos, PII ni resultados de test inventados.
- El roadmap distingue implementado, planificado y bloqueado.
- Handoff Freebuff puede ejecutarse sin rediseñar.
- Handoff integración no presupone V2 terminado.
- No se ha modificado main ni desplegado.
Genera un reporte de QA con comprobaciones PASA/FALLA/BLOQUEADO y evidencia.

## 42. Entrega final verificable
Devuelve nombre y URL del repo, rama documental, SHA final, URL master audit, número de campañas/waves/patchsets, principales hallazgos, capacidades existentes y pendientes, contratos, dependencias externas, riesgos, decisiones del fundador, orden de ejecución, URL handoff Freebuff y estado QA. No declares publicado lo no publicado.

---

# PARTE XIII — CRITERIOS DE RECHAZO

No aceptes como entrega final: auditoría superficial; roadmap genérico; campañas de un párrafo; listas de deseos; pseudocódigo sin wiring; rutas inventadas; dependencias sin justificar; tests vagos; resultados inventados; informes falsamente ejecutados; documentos repetidos con títulos distintos; contratos incompatibles; código legacy destruido sin migración; publicación sin verificar; o planes que obliguen a Freebuff a rediseñar la arquitectura.

La longitud debe venir de la precisión y la evidencia, no de repetir instrucciones. Si el repo es grande, produce una documentación grande. Si el repo tiene muchas ramas y trabajos, audítalos. No reduzcas el alcance para encajar en la ventana de chat: escribe archivos en GitHub por entregas sucesivas.

# PARTE XIV — ORDEN DE EJECUCIÓN INMEDIATO

1. Identifica ESTE repo, su main, ramas, PR, worktrees accesibles y documentación.
2. Audita código y pruebas, registra SHA y evidencias.
3. Reconstruye master audit y arquitectura objetivo específica del dominio.
4. Consulta agente main y documentación V2, con SHA y diferencias.
5. Investiga tecnologías, APIs, licencias y alternativas relevantes.
6. Define contratos, adaptadores, tenancy, seguridad y dependencias cruzadas.
7. Diseña roadmap completo, grafo de dependencias y landmarks.
8. Escribe TODAS las campañas completas con waves, patchsets, archivos, wiring, tests y gates.
9. Prepara plantillas de reportes y handoffs Freebuff/integración.
10. Publica en rama documental, valida enlaces y consistencia, entrega URLs.

**NO TERMINES tras los primeros documentos. NO PIDAS CONFIRMACIÓN para pasos reversibles y autorizados. NO CONFUNDAS PLANIFICAR CON IMPLEMENTAR. NO MODIFIQUES MAIN. NO DESPLIEGUES.**

**Objetivo definitivo:** que una instancia independiente de Freebuff pueda implementar este repositorio de forma autónoma, producir evidencia por campaña y dejarlo preparado para integrarse en AgntiaPro mediante contratos estables, sin reconstruir el kernel ni rehacer el dominio.
