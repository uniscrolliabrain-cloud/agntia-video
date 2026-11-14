# Del estado actual a terminado — agntia-video

## Baseline conocido
MVP 0.4 implementado: FastAPI/Python/FFmpeg/RNNoise, editor web, SDK TS @agntia/video, Hono, herramientas de agentes, tests Python/Node/Playwright y workflow CI. No se han ejecutado aquí los tests ni se ha verificado despliegue o integración con padre.

## Ruta de finalización
inventario y ejecución reproducible de tests → seguridad de tokens y tenant → contrato padre/Supabase/twins → aislamiento de media y jobs → pipeline de assets, previews y export → Anam/voz y conectores opt-in → observabilidad/ADTC → E2E de dos tenants → hardening/piloto → aprobación founder

## Riesgos y límites
Exportar no equivale a publicar; job no equivale a resultado. FFmpeg queda fuera de edge; no migrar Python a TS por principio. API actual con token global no prueba multitenancy. Respetar revision/409 y media de usuario no confiable.

## No resuelto
Reproducibilidad del HEAD, compatibilidad real con padre, requisitos por tenant, costos, despliegue, aceptación y licencias/privacidad. Los documentos de campaña son **plan**, no evidencia de ejecución. Astra puede cuestionar este roadmap libremente.
