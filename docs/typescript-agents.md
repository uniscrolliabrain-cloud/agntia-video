# Instalar Agntia en TypeScript, Hono y pnpm

Agntia tiene dos piezas: el **motor de vídeo Python + FFmpeg**, que ejecutas en Windows o un servidor, y un **paquete TypeScript** con cliente tipado, herramientas para agentes y adaptador Hono. Los agentes crean y editan los mismos proyectos que ves en el estudio web; no necesitan automatizar clics ni pagar por otro LLM para tomar las decisiones de edición.

El motor necesita disco y procesos de FFmpeg. Una app Hono desplegada en Cloudflare Workers u otro entorno edge se conecta al motor mediante HTTP; no intenta ejecutar FFmpeg dentro del Worker. La versión compilada del SDK y el router usan Fetch. Para instalar/compilar el paquete usa Node **22.13+**.

## Instalar desde GitHub

Dentro de tu otro repositorio:

```bash
pnpm add github:uniscrolliabrain-cloud/agntia-video#main
```

El nombre de importación es `@agntia/video`. Este paquete **no está publicado en npm**: se instala desde GitHub, y `prepare` genera los módulos JavaScript. Fija un commit en lugar de `main` para una instalación reproducible. Si tu política de pnpm no ejecuta la preparación de dependencias Git, puedes instalar un `.tgz` ya compilado desde los artefactos del workflow **Test → agntia-typescript-package**, o construirlo desde un checkout con `pnpm install && pnpm build && pnpm pack`. Después: `pnpm add ./agntia-video-0.3.0.tgz`.

Arranca el motor según el README. Configura en su `.env` un `AGNTIA_ACCESS_TOKEN` largo para acceso remoto y usa ese mismo valor solo en el servidor Hono. El paquete pnpm no instala Python ni FFmpeg automáticamente.

```dotenv
AGNTIA_BASE_URL=http://127.0.0.1:8000
AGNTIA_ACCESS_TOKEN=token_del_motor
```

Dentro de una red Docker, la URL puede ser `http://studio:8000`. Entre máquinas usa HTTPS. El cliente requiere un origen HTTP(S) sin rutas: el motor sirve su API en `/api`.

## Cliente tipado

```ts
import { AgntiaClient } from '@agntia/video';

const video = new AgntiaClient({
  baseUrl: process.env.AGNTIA_BASE_URL!,
  token: process.env.AGNTIA_ACCESS_TOKEN!,
});

const project = await video.getProject(projectId);
await video.updateProject(project.id, {
  revision: project.revision,
  settings: {
    voice_enhancement: 'ai',
    music: { asset_id: musicAssetId, volume: 0.15, ducking: true },
  },
});
const task = await video.render(project.id, 'preview');
const done = await video.waitForJob(project.id, task.id);
// done.outputs: podcast y clips, con rutas MP4/SRT protegidas.
const response = await video.download(done.outputs[0].url);
// Transmite response.body a tu almacenamiento o a un usuario autorizado.
```

`updateProject` hace una actualización parcial y conserva los campos omitidos, incluidos los de música. `saveProject` reemplaza briefing/settings/plan completos usando la revisión leída. Un 409 significa que otra persona o agente ha cambiado el proyecto: vuelve a leer y concilia. No hay reintentos automáticos de mutaciones.

Para subir un archivo desde Node, sin cargarlo entero en memoria:

```ts
import { openAsBlob } from 'node:fs';
const asset = await video.upload(projectId, await openAsBlob(authorizedPath), 'camara.mp4');
```

En otro runtime puedes pasar un `File` o `Blob` obtenido de una subida autorizada. Los límites de tamaño/memoria de la aplicación anfitriona siguen aplicándose. La copia multipart del motor también usa espacio temporal.

## Herramientas para tus agentes

```ts
import { createAgntiaTools } from '@agntia/video/agents';

const videoTools = createAgntiaTools(video, {
  resolveUpload: async reference => {
    // Integra aquí el almacenamiento y los permisos reales de tu aplicación.
    const file = await yourAuthorizedStorage.get(reference);
    return { file: file.blob, filename: file.name };
  },
});

// Con un proveedor que acepte function calling estilo OpenAI:
const definitions = videoTools.openAI;
// Tu bucle de agente despacha las llamadas recibidas:
const result = await videoTools.execute(call.function.name, JSON.parse(call.function.arguments));
```

`yourAuthorizedStorage` y `call` son puntos de integración de tu repositorio, no servicios incluidos. Para otros frameworks usa `definitions` (nombre, descripción y JSON Schema) y registra `execute` como manejador. No es un servidor MCP ni una dependencia de un framework de agentes concreto.

Se ofrecen **16 herramientas por defecto**, más `agntia_upload` si proporcionas `resolveUpload`:

| Acción | Herramienta |
| --- | --- |
| Capacidades y proyectos | `agntia_status`, `agntia_projects`, `agntia_create_project`, `agntia_project` |
| Briefing, cortes, clips, voz y música | `agntia_update_project` |
| Subidas, clasificación e inbox | `agntia_upload`, `agntia_asset_role`, `agntia_import_inbox` |
| Análisis Gemini y briefing DeepSeek opcional | `agntia_analyze`, `agntia_chat` |
| Beats | `agntia_detect_beats`, `agntia_snap_beats`, `agntia_undo_beats` |
| Previsualización/exportación y seguimiento | `agntia_render`, `agntia_jobs`, `agntia_job`, `agntia_plan` |

El agente anfitrión puede leer transcripciones, decidir qué conservar y escribir el plan directamente. No necesita DeepSeek para eso. Solo usa `agntia_chat` si quieres delegar esa conversación al agente de Agntia.

El catálogo valida argumentos antes de actuar. Puedes limitar herramientas por agente con `allow: ['agntia_status', 'agntia_project', 'agntia_job']`. Una referencia de subida es un ID resuelto por tu aplicación: no se aceptan herramientas de URL arbitraria ni se da acceso al disco del servidor por una ruta escrita por el modelo.

Las operaciones largas devuelven un **job**. El agente debe consultar `agntia_job` hasta `done` o `error`; la espera no cancela ni reinicia el trabajo. `waitForJob` es útil en procesos de servidor de larga duración; en Workers con límites de ejecución, guarda el ID y consulta el trabajo en solicitudes posteriores. No anuncies un vídeo terminado solo por recibir un ID.

## Montarlo en Hono

```ts
import { Hono } from 'hono';
import { createAgntiaRouter } from '@agntia/video/hono';

const app = new Hono();
app.route('/video', createAgntiaRouter({
  client: video,
  authorize: request => yourExistingAuthorization(request),
  resolveUpload: reference => yourAuthorizedUpload(reference),
}));
```

Las dos funciones `your...` deben usar los permisos existentes de tu repo; no son librerías incluidas. El router exige autorización y no crea una ruta pública con el token del motor.

- `GET /video/tools`: catálogo JSON de herramientas.
- `POST /video/tools/:name`: ejecuta una herramienta con sus argumentos JSON como cuerpo.
- `GET /video/status`: capacidades.
- `GET /video/projects/:pid/jobs/:jid`: progreso individual.
- `GET /video/projects/:pid/assets/:aid/media`: original protegido.
- `GET /video/projects/:pid/renders/:group/:file`: MP4/SRT protegido, transmitido por streaming con soporte de `Range` para el reproductor.

Los resultados de trabajos consultados por el router devuelven enlaces bajo `/video/...`, sin exponer el token ni la dirección interna del motor. Todos esos enlaces exigen la autenticación anfitriona. Los agentes deben usar el token/sesión de la app Hono; el token del motor se queda en su servidor.

El motor original sigue disponible para personas en su URL del estudio. Esta integración añade el control programático y las entregas protegidas en tu app; no monta la interfaz completa bajo una subruta de Hono ni añade un iframe. Consulta [examples/hono.ts](../examples/hono.ts) y [examples/agent.ts](../examples/agent.ts).

## CLI para agentes de código

Después de instalar el paquete en el repositorio anfitrión también puedes usar `pnpm exec agntia-video tools`, `pnpm exec agntia-video call ...` y `pnpm exec agntia-video upload ...`.

En un checkout de Agntia con `pnpm install && pnpm build`:

```bash
pnpm agntia tools
pnpm agntia call agntia_status '{}'
pnpm agntia call agntia_create_project '{"name":"Mi podcast"}'
pnpm agntia upload PROJECT_ID ./camara.mp4
pnpm agntia call agntia_update_project @plan-change.json
```

Las variables de conexión se leen del entorno del proceso; la CLI no carga secretos desde argumentos ni los incluye en respuestas. Copia o enlaza las instrucciones de [AGENTS.md](../AGENTS.md) en la guía de agentes del repositorio anfitrión. El esquema completo del motor está en `GET /api/openapi.json`, protegido con el mismo Bearer token.

## Alcance

La API actual comparte una biblioteca/proyectos para un propietario de confianza. No añade aislamiento de tenants ni usuarios por proyecto. Si tu repo sirve a varios clientes, su autorización debe restringir las referencias y proyectos, o usar instancias separadas del motor. Los agentes respetan las mismas limitaciones de montaje del estudio: sincronización manual de pistas, una banda sonora y revisión del diálogo después de ajustar beats.
