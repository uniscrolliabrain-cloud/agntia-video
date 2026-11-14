# ADTC conceptual — agntia-video

Propuesta de envelope: schemaVersion, eventId, eventType, tenantId, actorId, taskId, correlationId, causationId, requestId, traceId, spanId, idempotencyKey, source, resourceRefs, approvalRef, evidenceRefs, payloadRef. No afirmar SystemEvent nativo ni compatibilidad real. Bridge versionado a padre; outbox/inbox, dedupe, DLQ, unknown outcome y reconciliación. Ciberseguridad observa metadatos mínimos bajo ACL, sin acceso universal a medios, documentos, PII, credenciales o mensajes. Logs sanitizados. Un side effect externo por AuthorityMap.
