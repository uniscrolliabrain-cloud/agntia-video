# AGNTIA VÍDEO — CONCEPT MASTER V1.0
**Fecha:** 2026-11-15 · **Estado:** visión de destino, fundamentada en software existente · **Repositorio:** `uniscrolliabrain-cloud/agntia-video`

> **Visión:** evolucionar un estudio de podcast funcional hacia un **sistema operativo audiovisual agéntico**: investigación, guion, dirección, ingestión, edición no destructiva, composición, audio, subtítulos, localización, revisión, renderizado y distribución coordinada de vídeo profesional. Humanos y agentes trabajan sobre el mismo proyecto, con un motor de medios determinista, derechos verificables y un historial reproducible de decisiones.

## 0. Contrato de realidad: lo que existe y lo que aspiramos a construir

**Software observado en repositorio:** versión 0.4, Python 3.11+/FastAPI, FFmpeg/ffprobe, estudio web, proyectos persistentes, clips, B-roll, audio separado, edición de cortes, previsualización/exportación, RNNoise local, música y ducking, detección de beats, subtítulos SRT, DeepSeek y Gemini opcionales, SDK TypeScript `@agntia/video`, adaptador Hono y 16 herramientas por defecto (17 con upload autorizado). El motor usa revisiones optimistas y 409 para concurrencia, cola de un worker y snapshots de render. Los análisis externos se cachean. No se ha ejecutado aquí una batería de pruebas: estas capacidades se describen a partir de documentación y código inspeccionados, no de una certificación independiente.

**Límites explícitos de V0.4:** motor compartido de propietario de confianza, sin aislamiento nativo multi-tenant por proyecto; sincronización manual de pistas, una banda sonora, sin mezcla arbitraria multitrack; exportación no publica en redes; no hay contabilidad de costes de modelos; trabajos interrumpidos no se reanudan automáticamente; clips referidos al tiempo del episodio final; análisis Gemini y traducción requieren configuración. El SDK Hono autoriza en el host, pero eso no sustituye ACL en el motor cuando varios tenants comparten la instancia.

**Etiquetas:** [E] presente según repositorio; [D] diseño de destino; [H] hipótesis que exige investigación. No se declara ninguna ampliación como implementada. Este documento **no modifica código, agentes ni campañas existentes**.

## 1. Tesis: de editor de podcasts a fábrica audiovisual de empresas

La producción audiovisual empresarial está fragmentada entre investigación, guion, grabación, avatares, montaje, subtitulado, identidad visual, licencias, aprobación, distribución y medición. La IA generativa facilita assets, pero no garantiza continuidad, coherencia, fidelidad de la voz, derechos, accesibilidad ni reproducción exacta. Un agente que produce un vídeo debe poder demostrar qué material usó, qué decisiones tomó, quién aprobó el resultado y qué archivo se entregó.

**Agntia Media Production OS** tendrá tres formas de trabajo: (1) estudio humano visual con timeline profesional; (2) producción conversacional supervisada por LAIA y especialistas; (3) pipelines SOP reproducibles para producir series, piezas, versiones y campañas. No se reemplaza el editor por prompts: se integran ambos sobre un **modelo canónico de edición**.

### Diez apuestas diferenciales
1. **Media Reality Graph [D]:** grafo de fuentes, escenas, voces, personas consentidas, derechos, tiempos, versiones y entregas.
2. **Canonical Edit Graph [D]:** representación tipada y no destructiva de composición, tracks, transiciones, filtros, audio y captions, exportable a estándares.
3. **Evidence-to-Frame Ledger [D]:** trazabilidad de claims y assets hasta el fotograma y el render que los contiene.
4. **Creative Intent Compiler [D]:** convierte brief, estilo, formato y límites en un plan ejecutable y revisable.
5. **Multimodal Story Intelligence [D]:** indexa escenas, habla, gestos, música, estructura narrativa y puntos destacados con incertidumbre.
6. **Synthetic Presenter Studio [D]:** avatares, voz, presentadores virtuales y continuidad de personaje con identidad y consentimiento.
7. **Render Provenance Engine [D]:** snapshots inmutables, manifest de dependencias, FFmpeg reproducible y artefactos con checksums.
8. **Human-Agent Editorial Merge [D]:** colaboración multiusuario con conflictos semánticos, revisión de diffs y control de versiones.
9. **Content Adaptation Factory [D]:** transforma una fuente en episodios, verticales, subtítulos, traducciones y formatos de canal.
10. **Creative Quality & Rights Governor [D]:** evalúa calidad, accesibilidad, seguridad, claims, licencias y aprobaciones antes de exportar/publicar.

## 2. Atlas tecnológico y científico

### 2.1 Editores y plataformas a investigar
**DaVinci Resolve/Fairlight, Adobe Premiere Pro/After Effects, Final Cut Pro, Avid Media Composer**: referencias de NLE profesional, mezcla, color, timeline y colaboración. **Descript, Riverside, OpusClip, Runway, CapCut, VEED, Canva, HeyGen, Synthesia, Tavus, Anam, ElevenLabs**: referencias para transcripción, edición por texto, clips, medios sintéticos, avatares y voz. Sus funcionalidades, licencias, APIs, costes y restricciones requieren verificación por producto y fecha; son benchmarking, no capacidades acreditadas de Agntia.

### 2.2 Open source y estándares
- **FFmpeg/ffprobe:** núcleo de codificación, filtros y render. https://ffmpeg.org/
- **GStreamer:** grafos de medios y streaming. https://gstreamer.freedesktop.org/
- **OpenTimelineIO:** intercambio de timelines; investigar compatibilidad de efectos y límites de exportación. https://github.com/AcademySoftwareFoundation/OpenTimelineIO
- **MLT Framework:** motor de edición basado en timelines. https://github.com/mltframework/mlt
- **Blender:** composición, 3D, VFX y escenas. https://github.com/blender/blender
- **OpenShot/libopenshot:** referencia de timeline y composición. https://github.com/OpenShot/libopenshot
- **Kdenlive:** referencia de NLE open source. https://github.com/KDE/kdenlive
- **auto-editor:** edición basada en audio/silencios, con revisión expresiva. https://github.com/WyattBlue/auto-editor
- **WhisperX:** alineación y diarización para investigar. https://github.com/m-bain/whisperX
- **FunClip:** selección de fragmentos por transcripción. https://github.com/modelscope/FunClip
- **PySceneDetect:** detección de escenas. https://github.com/Breakthrough/PySceneDetect
- **Demucs:** separación de fuentes de audio, según licencia y recursos. https://github.com/facebookresearch/demucs
- **librosa:** análisis de audio y ritmo. https://github.com/librosa/librosa
- **RNNoise:** reducción de ruido de voz. https://github.com/xiph/rnnoise
- **C2PA:** procedencia y credenciales de contenido. https://c2pa.org/
- **OpenColorIO:** gestión de color. https://github.com/AcademySoftwareFoundation/OpenColorIO
- **OpenEXR:** formato de imagen HDR/VFX. https://openexr.com/
- **WebRTC:** presencia y colaboración audiovisual en tiempo real. https://www.w3.org/TR/webrtc/
- **OpenTelemetry:** trazas y métricas de trabajos. https://opentelemetry.io/

**Investigación científica:** reconocimiento multimodal, alineación audio-vídeo, diarización, source separation, speech enhancement, segmentación temporal, vision-language models, retrieval multimodal, narrative structure, métricas perceptuales (VMAF/SSIM con límites), calidad subjetiva, generación temporalmente consistente, incertidumbre y evaluación humano-IA. **Hipótesis**: modelos de dirección creativa con memoria narrativa y optimización de ritmo editorial; no prometer gusto humano reproducible ni predicción de viralidad.

### 2.3 Criterios de selección
Para cada componente: licencia concreta, origen, mantenimiento, formato de entrada/salida, memoria/CPU/GPU, coste, privacidad, reproducibilidad, calidad por idioma, fallos, compatibilidad Windows/Linux, facilidad de sandbox, observabilidad y reversibilidad. Preferir adaptadores y workers aislados; no introducir un stack pesado por prestigio.

## 3. Mapa de 96 capacidades finales

### A. Proyecto, ingestión y biblioteca
**VID01 [E]** Proyectos persistentes con revisiones y assets.
**VID02 [E]** Importación navegador/inbox y fingerprint de contenido.
**VID03 [E]** Roles de material: diálogo, avatar, B-roll, audio y música.
**VID04 [D]** Aislamiento tenant/proyecto en motor, DB, disco y trabajos.
**VID05 [D]** Biblioteca de medios multiusuario con ACL y retención.
**VID06 [D]** Uploads reanudables, cuarentena y análisis de malware.
**VID07 [D]** Metadata avanzada: timecode, codecs, color, audio, frame rate.
**VID08 [D]** Proxies adaptativos y gestión de originales inmutables.
**VID09 [D]** Media Reality Graph con procedencia y caducidad.
**VID10 [D]** Rights Vault de consentimientos, licencias y restricciones.
**VID11 [D]** Búsqueda semántica audiovisual autorizada.
**VID12 [H]** Catalogación narrativa y afectiva sin atribuciones psicológicas invasivas.

### B. Comprensión y preproducción
**VID13 [E]** Briefing conversacional opcional con DeepSeek.
**VID14 [E]** Análisis audiovisual Gemini por segmentos y caché.
**VID15 [D]** Guion técnico, escaleta y storyboard versionados.
**VID16 [D]** Shot list y plan de rodaje por formato.
**VID17 [D]** Multimodal Story Intelligence con evidencia temporal.
**VID18 [D]** Transcripción local y alineación palabra/fonema.
**VID19 [D]** Diarización y atribución de hablante revisable.
**VID20 [D]** Detección de escenas, planos, objetos y momentos.
**VID21 [D]** Creative Intent Compiler con límites y estilos.
**VID22 [D]** Generación de alternativas editoriales comparables.
**VID23 [H]** Predicción de claridad narrativa y fatiga de audiencia.
**VID24 [D]** Investigación de claims y fuentes para piezas informativas.

### C. Timeline y edición
**VID25 [E]** Cortes secuenciales, reordenación, división y duplicación.
**VID26 [E]** Imagen y audio independientes por corte.
**VID27 [E]** Timeline visual, inspector, deshacer/rehacer local.
**VID28 [E]** Captions manuales sobre tiempo de salida.
**VID29 [D]** Canonical Edit Graph con tracks, nodos y keyframes.
**VID30 [D]** Composición multicapa y transiciones parametrizadas.
**VID31 [D]** Edición no destructiva por texto y por timeline.
**VID32 [D]** Sincronización automática multicámara/audio.
**VID33 [D]** Seguimiento de hablante y reencuadre.
**VID34 [D]** B-roll contextual con licencia y revisión.
**VID35 [D]** OpenTimelineIO import/export con loss report.
**VID36 [D]** Human-Agent Editorial Merge con diff semántico.
**VID37 [D]** Versiones, ramas creativas y comparación A/B.
**VID38 [H]** Dirección editorial asistida basada en ritmo, intención y evidencia.

### D. Audio y música
**VID39 [E]** RNNoise local y limpieza clásica de voz.
**VID40 [E]** Música, volumen, loop, ducking y limitación final.
**VID41 [E]** Beats, BPM estimado y snap reversible.
**VID42 [D]** Mezcla multipista y buses de audio.
**VID43 [D]** Loudness y true peak por destino.
**VID44 [D]** Diarización, aislamiento y reparación de voces.
**VID45 [D]** Edición espectral y restauración.
**VID46 [D]** Música con cue sheets, licencias y stems.
**VID47 [D]** Voz sintética autorizada y versionada.
**VID48 [D]** Doblaje y lip-sync con consentimiento.
**VID49 [H]** Mezcla adaptativa a emoción narrativa sin inventar estados mentales.
**VID50 [D]** Control de derechos de voz y trazabilidad de clones.

### E. Vídeo, composición y color
**VID51 [E]** Exportación MP4/H.264 horizontal y vertical.
**VID52 [E]** Previsualización y renders sobre snapshots.
**VID53 [D]** Color management con perfiles y conversiones verificadas.
**VID54 [D]** Motion graphics, overlays, lower thirds y branding.
**VID55 [D]** Corrección de color y LUTs no destructivas.
**VID56 [D]** Estabilización, denoise y reencuadre.
**VID57 [D]** Composición 2D/3D mediante puertos a Blender.
**VID58 [D]** VFX, máscaras y tracking.
**VID59 [D]** Adaptación automática de proporciones con revisión.
**VID60 [D]** Render HDR/SDR y perfiles de destino.
**VID61 [H]** Composición generativa temporalmente coherente.
**VID62 [D]** Control de artefactos, flicker, lipsync y calidad perceptual.

### F. Subtítulos, localización y accesibilidad
**VID63 [E]** Subtítulos originales/traducidos y SRT.
**VID64 [D]** Captions por palabra, estilos y safe areas.
**VID65 [D]** Traducción con glosarios de marca y revisión.
**VID66 [D]** Subtítulos SDH y accesibilidad.
**VID67 [D]** Audiodescripción y versiones accesibles.
**VID68 [D]** Doblaje multilingüe autorizado.
**VID69 [D]** Localización cultural por mercado.
**VID70 [D]** QA de sincronización, ortografía y lectura.

### G. Avatares, presentadores y producción sintética
**VID71 [D]** Synthetic Presenter Studio con Anam/otros puertos.
**VID72 [D]** Personajes persistentes, identidad y continuidad visual.
**VID73 [D]** Integración de voces ElevenLabs/otras bajo licencia.
**VID74 [D]** Guiones y actuaciones revisables de avatares.
**VID75 [D]** Composición avatar+cámara+B-roll.
**VID76 [D]** Consentimiento de imagen/voz y derechos de personaje.
**VID77 [D]** Etiquetado de contenido sintético cuando proceda.
**VID78 [H]** Dirección multimodal de personajes entre episodios.
**VID79 [D]** Presencia en directo separada de render offline.
**VID80 [H]** Escenas narrativas persistentes y mundos audiovisuales.

### H. Render, entrega y operaciones
**VID81 [E]** Jobs de preview/render/export con estado.
**VID82 [E]** Descarga protegida vía host Hono y SDK.
**VID83 [D]** Render Provenance Engine con manifests y checksums.
**VID84 [D]** Workers distribuidos y colas con leases.
**VID85 [D]** Reanudación, reconciliación y retry seguro.
**VID86 [D]** Object storage cifrado y lifecycle.
**VID87 [D]** Presets por plataforma y múltiples codecs.
**VID88 [D]** Paquetes de entrega con masters, clips, captions y fuentes.
**VID89 [D]** Control de coste CPU/GPU/tokens por proyecto.
**VID90 [D]** Quality Gates de audio, vídeo, derechos y accesibilidad.

### I. Agentes, integración y medición
**VID91 [E]** SDK TypeScript, herramientas y adaptador Hono.
**VID92 [D]** LAIA y especialistas de guion, edición, sonido, color, QA.
**VID93 [D]** WorkOrders, SOPs y approvals del padre.
**VID94 [D]** Puertos de entrega a Redes, Marketing, Branding y Comunicación.
**VID95 [D]** Evaluación de trayectoria creativa y feedback humano.
**VID96 [H]** Aprendizaje de preferencias editoriales por empresa, sin filtración inter-tenant.


## 4. Arquitectura de destino: diez planos

1. **Identity & Rights Plane:** tenant, principal, ACL, consentimiento, licencias y uso permitido.
2. **Media Ingest Plane:** uploads, hashes, ffprobe, cuarentena, proxies, almacenamiento.
3. **Semantic Intelligence Plane:** ASR, diarización, escenas, indexación, evidence refs.
4. **Creative Planning Plane:** briefs, guiones, propuestas, alternativas y versiones.
5. **Canonical Edit Plane:** grafo de edición, tiempo, tracks, composición, efectos y captions.
6. **Audio & Voice Plane:** limpieza, mezcla, música, voces sintéticas, derechos.
7. **Synthetic & Visual Plane:** avatares, overlays, color, VFX, motion graphics.
8. **Render & Artifact Plane:** FFmpeg, snapshots, jobs, manifests, checksums, entrega.
9. **Agent & Collaboration Plane:** humanos, LAIA, especialistas, diffs y approvals.
10. **Quality & Operations Plane:** QA, observabilidad, costes, recuperación y seguridad.

### 4.1 Pipeline completo
`objetivo → briefing → investigación y derechos → guion/storyboard → ingestión → análisis multimodal → propuesta de edición → diff/revisión → plan tipado aprobado → snapshot inmutable → render preview → QA humano/técnico → revisión → export master y derivados → delivery receipt → handoff a publicador → métricas y aprendizaje`.

El estudio **produce**; Redes/Marketing/Comunicación **publican** bajo autoridad separada. Un render completo no significa publicación. Un enlace de descarga no prueba que un destinatario vio el vídeo.

### 4.2 Canonical Edit Graph
Propuesta de contrato:
```ts
type EditProject = {
  tenantId: string;
  projectId: string;
  revision: number;
  mediaManifestRef: string;
  rightsSnapshotRef: string;
  sequence: SequenceNode[];
  audioBuses: AudioBus[];
  captions: CaptionTrack[];
  deliveryProfiles: DeliveryProfile[];
  provenance: EvidenceRef[];
};
type SequenceNode = {
  nodeId: string;
  sourceAssetRef: string;
  sourceIn: RationalTime;
  sourceOut: RationalTime;
  timelineStart: RationalTime;
  transforms: TransformNode[];
  audioRouting?: AudioRouting;
};
type RationalTime = { numerator: number; denominator: number };
```
Usar tiempo racional/frame-aware, no sumar floats arbitrarios; distinguir source time, timeline time, media PTS y wall-clock. El motor actual conserva su JSON y se migra mediante adaptador versionado con roundtrip tests. Un `loss report` documenta efectos no representables al importar/exportar OTIO.

### 4.3 Render reproducible
`RenderIntent = {tenantId, projectRevision, editGraphHash, assetHashes[], codecProfile, ffmpegVersion, modelVersions, fontsRefs, rightsSnapshot, approvalRef, budgetRef}`.
`RenderJob = QUEUED | LEASED | RUNNING | VERIFYING | DONE | FAILED | CANCELLED | OUTCOME_UNKNOWN`.
Cada job captura un snapshot; el worker no relee el plan mutable para renderizar. Los archivos finales se publican por commit atómico tras verificación, con checksum, duración, resolución, loudness, pistas y subtítulos. Reintentar un render no debe sobrescribir el master anterior. Los procesos interrumpidos se marcan reconciliables, no exitosos. Los recursos de CPU/GPU se reservan por tenant y prioridad.

### 4.4 Human-Agent Editorial Merge
Un 409 no es un error para reintentar a ciegas: leer nueva revisión, calcular diff entre base, versión local y versión remota; conciliar cortes, captions, ajustes y referencias; mostrar conflictos. Futura colaboración en vivo puede usar operaciones tipadas o CRDT para campos compatibles, pero no mezclar operaciones de timeline incompatibles sin control semántico. Deshacer/rehacer local no equivale a rollback de una exportación ya emitida.

### 4.5 Modelo de dominio
`Tenant, Principal, MediaProject, ProjectRevision, MediaAsset, AssetHash, AssetRights, ConsentGrant, SourceEvidence, MediaProxy, Transcript, WordAlignment, SpeakerHypothesis, SceneSegment, CreativeBrief, ScriptRevision, Storyboard, EditGraph, Track, ClipNode, TransformNode, AudioBus, CaptionTrack, AvatarBinding, VoiceLicense, RenderIntent, RenderJob, RenderManifest, DeliveryArtifact, QualityFinding, ApprovalBinding, WorkOrder, HandoffReceipt, AuditEvent`.
Todas las entidades relevantes incorporan tenant, ACL, versión, fuente, estado y retención. No mezclar identidades de persona, voz sintética y personaje.

## 5. La frontera de seguridad: de estudio local a servicio multiempresa

**Problema observado:** el motor 0.4 utiliza biblioteca compartida y token del motor; el adaptador Hono exige autorización anfitriona pero no dota automáticamente al backend Python de separación de proyectos por tenant. La arquitectura actual es adecuada para propietario de confianza o instancias aisladas, **no debe exponerse como servicio multi-tenant compartido sin controles adicionales**.

**Estrategia de migración:**
- **Opción A, aislamiento por instancia:** una instancia del motor por tenant, con almacenamiento, credenciales y red separados. Primera vía segura para dogfooding si el coste lo permite.
- **Opción B, aislamiento nativo:** tenantId derivado de identidad autenticada, DB con RLS o equivalente, storage por tenant, signed asset refs, autorización en todos los endpoints y jobs, scopes de agentes, control de exportaciones y backups, pruebas de cruces de tenant.
- **Opción C, híbrida:** control plane común, workers aislados por tenant/proyecto y almacenamiento cifrado por prefijo/clave; verificación de rutas y job ownership.

**Nunca** confiar en tenantId enviado por el LLM, filename, projectId adivinable, cookie del navegador o filtro de UI como única barrera. Revisar acceso a assets, thumbnails, proxies, render URLs, jobs, cachés, temporales, errores, previews y WebSocket. El token del motor permanece server-side. Cualquier integración con /agente usa autorización y mandato reales, no solo el catálogo de herramientas.

## 6. Oficina audiovisual agéntica

**LAIA** dirige el briefing, explica decisiones, presenta previews y pide aprobaciones. Especialistas de dominio: investigador audiovisual, guionista, editor, montador de clips, director de fotografía/color, ingeniero de sonido, subtitulador/localizador, responsable de derechos y QA. Son **roles de trabajo/SOPs**, no nuevos agentes canónicos independientes que alteren el kernel.

**Tools nominadas:** `video.project.read`, `video.assets.list`, `video.brief.propose`, `video.script.propose`, `video.analysis.request`, `video.edit.diff`, `video.edit.propose`, `video.render.preview`, `video.render.status`, `video.quality.report`, `video.export.prepare`, `video.delivery.status`. Reutilizar herramientas reales `agntia_*` donde existan; añadir policy en el host. Exportaciones, uploads, uso de proveedores de pago, voces sintéticas y envíos externos requieren permisos diferenciados. No introducir `execute-anything`.

**SOP ejemplo:** «De un briefing de producto, generar un vídeo explicativo horizontal, tres clips verticales, subtítulos ES/EN y paquete de publicación». La ejecución debe registrar objetivos, fuentes, claims, assets, derechos, plan, preview, QA, aprobación, costes, entregas y handoff. La publicación real pertenece a Redes/Comunicación.

## 7. UX de destino

**Espacios:** Creative Briefing, Media Library, Story & Script, Timeline Studio, Audio Lab, Caption & Localization, Synthetic Presenter Studio, Color & Motion, Review Room, Render Farm, Delivery Center, Rights Vault, Agent Office y Quality Observatory.

**Interacción:** lienzo con previsualización real, timeline multipista, inspector, diff visual entre versiones, chat de LAIA, estados de jobs, comparación A/B, comentarios anclados a timecode, revisión de derechos, export profiles y costes. Mostrar si la vista corresponde a **original**, **preview vigente**, **preview obsoleta** o **master exportado**. El móvil conserva revisión y acciones básicas; la edición densa se adapta sin prometer paridad ergonómica absoluta con escritorio.

**Avatar:** Anam/otros proveedores pueden crear presentadores y presencia en directo; el estudio offline mantiene assets y renders, y Comunicación gestiona sesiones en vivo. No confundir un avatar renderizado con una llamada bidireccional. Los personajes persistentes requieren consistencia de identidad, consentimiento y trazabilidad de generación.

## 8. Calidad, derechos y gobernanza

**Derechos:** contratos de imagen/voz, licencias de música, stock, fuentes tipográficas, uso comercial de modelos, contenido de terceros, consentimiento de participantes, retirada y caducidad. Los modelos generativos no confieren derechos sobre material de entrada. Prohibir clonación de voz o likeness sin autorización. Identificar contenido sintético cuando corresponda.

**Integridad:** claims corporativos con source refs; captions contrastados con audio; traducciones revisables; no fabricar testimonios ni simular declaraciones reales; provenance de cada frame/clip cuando sea técnicamente posible. C2PA es candidato para credenciales, no garantía de veracidad de contenido.

**Seguridad:** media files como entrada no confiable; límites de tamaño, duración, codecs, decodificación, CPU, memoria, disco, rutas, sandbox de FFmpeg, malware scanning, aislamiento de workers, timeouts y limpieza de temporales. Prompt injection desde transcripciones, subtítulos y metadata nunca altera herramientas ni policy. HTTPS, secretos server-side, URLs temporales, ACL por asset y auditoría.

**Privacidad:** RGPD/LOPDGDD, minimización, base jurídica, retención, borrado de originales y derivados, tratamiento de voz/rostro, proveedores externos y transferencia internacional cuando aplique. No usar vídeos privados de un tenant para entrenar modelos de otro sin autorización específica y garantías.

## 9. Evaluación y pruebas adversariales

**Calidad técnica:** fps/PTS, A/V sync, cortes, black frames, clipping, loudness, true peak, subtítulos, codec, bitrate, tamaño, tiempo de render, memoria y coste. **Calidad creativa:** coherencia con brief, estructura narrativa, claridad, ritmo, continuidad, marca, accesibilidad y revisión humana. **Agentes:** exactitud de herramientas, no alucinación de assets, respeto de revisiones, abstención, trazabilidad y estado final. **Seguridad:** aislamiento tenant, derechos, no ejecución de metadata, no exposición de secretos y no export sin aprobación.

**Escenarios críticos:**
1. Dos tenants comparten nombres de archivo e IDs parecidos; no cruzar assets.
2. Un usuario autorizado en Hono intenta descargar render ajeno mediante URL conocida.
3. Un agente recibe transcripción con instrucciones para leer secretos.
4. Un asset cambia de licencia entre propuesta y export.
5. El modelo devuelve un clip fuera de duración o con NaN.
6. Audio separado empieza después del final visual.
7. El usuario reordena cortes con captions manuales y debe revisar alineación.
8. Un proyecto cambia tras comenzar un render; el snapshot debe conservarse.
9. Dos editores guardan la misma revisión; 409 y merge, nunca overwrite silencioso.
10. Un job muere durante FFmpeg; no declarar `DONE`.
11. Se agota disco y debe limpiar temporales sin borrar originales.
12. Una exportación se reintenta y no duplica entregas facturables.
13. Un subtítulo traducido altera una cifra o nombre propio.
14. Un avatar cambia de rostro entre planos sin aprobación.
15. Un modelo intenta generar una voz sin licencia.
16. Un vídeo contiene material con derecho de retirada.
17. Un proveedor Gemini/DeepSeek no tiene clave: capacidad deshabilitada, sin fingir análisis.
18. Un clip vertical corta la cara o los subtítulos.
19. Una sesión móvil pierde conexión durante upload; reanudación y checksum.
20. Un agente informa «publicado» cuando solo hay render local.
21. Un proyecto contiene vídeo malformado que dispara consumo excesivo de decodificador.
22. Un archivo de medios contiene rutas o nombres con shell metacharacters.
23. Un render mezcla frame rates y VFR con desincronización.
24. El usuario solicita borrar un proyecto y se deben localizar derivados, cachés y backups según política.

Pruebas de mocks no equivalen a validación de FFmpeg real, codecs reales ni proveedores externos. Definir fixtures audiovisuales con ground truth y ejecutar tests en Windows/Linux, diferentes versiones de FFmpeg y perfiles de hardware.

## 10. Roadmap de convergencia

**G0 — Inventario & Concept Atlas:** auditar código real, capacidades, contratos, fuentes, benchmarks y licencias.
**G1 — Seguridad multiempresa:** aislamiento por instancia o tenant nativo, auth, storage y job ownership.
**G2 — Modelo de edición:** Canonical Edit Graph, tiempo racional, versionado y migración V0.4.
**G3 — Inteligencia audiovisual:** transcripción local, alineación, diarización, escenas, búsqueda y evidencia.
**G4 — Editor profesional:** multipista, sincronización, efectos, captions, colaboración y OTIO.
**G5 — Audio/Color/Composición:** mezcla, restauración, color, motion y QA.
**G6 — Synthetic Studio:** avatares, voces, presentadores y consentimiento.
**G7 — Render Fabric:** workers, almacenamiento, manifests, recuperación y costes.
**G8 — Agentic Media Office:** LAIA, SOPs, roles, WorkOrders, approvals y handoffs.
**G9 — Evaluation & Reliability:** red team, rendimiento, derechos, calidad y observabilidad.
**G10 — Concept V2:** reevaluación con resultados reales y nuevas tecnologías.

No se deben trasladar de forma mecánica las 42 campañas de repos documentales a este repo ya funcional. Aquí la prioridad es **no romper el estudio 0.4**: introducir contratos versionados, adaptadores y tests de regresión; cambios de esquema con migración reversible. No desplegar sin aprobación del founder.

## 11. Hipótesis abiertas

1. ¿Cuál es el mínimo Canonical Edit Graph capaz de cubrir 80% de trabajos sin sacrificar edición avanzada? [H]
2. ¿Qué partes del pipeline se benefician realmente de GPU frente a CPU? [H]
3. ¿Qué modelos locales de ASR/diarización ofrecen calidad suficiente en ES/EN/FR? [H]
4. ¿Cómo medir calidad creativa sin optimizar únicamente métricas superficiales? [H]
5. ¿Qué garantías técnicas permiten una reproducción bit a bit o perceptualmente equivalente? [H]
6. ¿Cómo diseñar merge semántico de timelines sin sorpresas para editores humanos? [H]
7. ¿Qué estándares permiten intercambiar timelines conservando subtítulos, efectos y derechos? [H]
8. ¿Qué nivel de automatización de reencuadre respeta intención narrativa y accesibilidad? [H]
9. ¿Qué proveedores de avatares permiten identidad consistente, export y control de datos? [H]
10. ¿Cómo garantizar derechos y procedencia en medios generados o mezclados? [H]
11. ¿Qué coste por minuto de vídeo final es sostenible para pymes? [H]
12. ¿Cómo adaptar episodios a canales sin fabricar mensajes o testimonios? [H]
13. ¿Qué forma de aislamiento por tenant resulta más económica sin comprometer seguridad? [H]
14. ¿Cómo incorporar comentarios/revisiones sobre fotogramas a SOPs deterministas? [H]

Cada hipótesis exige protocolo, dataset/fixtures, baseline, métricas, coste, fecha y decisión versionada.

## 12. Fuentes inspeccionadas y límites

**Código/documentación del repositorio:**
- [README](../../README.md)
- [Arquitectura](../architecture.md)
- [Integración TypeScript y agentes](../typescript-agents.md)
- [Guía de agentes](../../AGENTS.md)
- [Motor FastAPI](../../agntia/app.py)
- [Paquete TypeScript](../../package.json)
- [Proyecto Python](../../pyproject.toml)

**Fuentes técnicas externas:** FFmpeg, OTIO, MLT, Blender, Kdenlive, auto-editor, WhisperX, FunClip, PySceneDetect, RNNoise, OpenColorIO, C2PA, WebRTC y OpenTelemetry (enlaces en §2).

**Límite:** documento conceptual basado en código y documentación consultados, no ejecución de tests en esta sesión, ni auditoría exhaustiva de licencias, APIs o modelos. Los nombres de productos externos son líneas de investigación; las capacidades [D]/[H] no están implementadas por crear este archivo. V1.x añade investigación y evidencias; V2 podrá redefinir la visión sin falsear el estado actual.
