# Flow específico — agntia-video

inventario y ejecución reproducible de tests → seguridad de tokens y tenant → contrato padre/Supabase/twins → aislamiento de media y jobs → pipeline de assets, previews y export → Anam/voz y conectores opt-in → observabilidad/ADTC → E2E de dos tenants → hardening/piloto → aprobación founder

**Gates de etapa:** BASELINE_OBSERVED → ASTRA_META_AUDIT_PENDING → FINDINGS_RECONCILED → CAMPAIGN_DELTA_APPROVED → FREEBUFF_IMPLEMENTATION → CODEX_SHA_VERIFICATION → ARCHITECT_REVIEW → FOUNDER_APPROVAL → RELEASE. No transformar documentación en PASS. Futuros handoffs por campaña deben enumerar superficies de escritura, patchsets, dependencias, acceptance, evidencia, rollback y condiciones BLOCKED.

## Reglas de ejecución
Sin modificación de main, padre ni despliegue por defecto. Ramas por campaña, escritor único, pruebas independientes sobre SHA congelado, no ocultar fallos. Diferenciar smoke sintético, integración real y aceptación de cliente. Los resultados previos son históricos hasta reproducirlos.
