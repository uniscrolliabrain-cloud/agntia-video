# Interfaces y AuthorityMap — agntia-video

Padre: identidad/agentes canónicos, Supabase JWT, membresía, policy, SOP, approvals, memoria, bus. Especialista: dominio y workers con permisos delegados, receipts, evidence. Portal externo usa el mismo contrato de identidad, no IdP soberano. Integraciones con otros especialistas solo mediante contrato, no escrituras cruzadas silenciosas. Exportar no equivale a publicar; job no equivale a resultado. FFmpeg queda fuera de edge; no migrar Python a TS por principio. API actual con token global no prueba multitenancy. Respetar revision/409 y media de usuario no confiable.

Versionar puertos, capabilities, error taxonomies, idempotency, scopes, timeout, retries, data residency y provider receipts. No conectar proveedores ni cambiar padre sin aprobación.
