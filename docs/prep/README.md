# Baseline y recuperación — agntia-video

**2026-11-14 · DOCUMENTATION_PREP.** Estado observado por lectura selectiva GitHub: MVP 0.4 implementado: FastAPI/Python/FFmpeg/RNNoise, editor web, SDK TS @agntia/video, Hono, herramientas de agentes, tests Python/Node/Playwright y workflow CI. No se han ejecutado aquí los tests ni se ha verificado despliegue o integración con padre.

## Evidencias originales a preservar
- [README.md](../../README.md)
- [AGENTS.md](../../AGENTS.md)
- [docs/architecture.md](../../docs/architecture.md)
- [docs/typescript-agents.md](../../docs/typescript-agents.md)
- [package.json](../../package.json)
- [.github/workflows/test.yml](../../.github/workflows/test.yml)

No borrar, reescribir ni marcar pruebas antiguas como nuevas. No se han ejecutado tests, CI, despliegues ni conexión a terceros en esta preparación. Antes de implementar: SHA exacto, inventario del checkout, status Git, tests reales, versiones, mapa de cambios y comparación con documentos históricos. Diferenciar CODE_PRESENT, HISTORICAL_TEST_REPORTED, REPRODUCED_TEST, UNKNOWN y BLOCKED.

## Fronteras
Exportar no equivale a publicar; job no equivale a resultado. FFmpeg queda fuera de edge; no migrar Python a TS por principio. API actual con token global no prueba multitenancy. Respetar revision/409 y media de usuario no confiable.
