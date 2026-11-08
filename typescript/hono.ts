import { Hono } from 'hono';
import { AgntiaClient, AgntiaError } from './client.ts';
import { createAgntiaTools } from './agents.ts';
import type { AgentOptions } from './agents.ts';

export interface HonoOptions extends AgentOptions {
  client: AgntiaClient;
  /** Required: integrate your Hono app's real session/API-key authorization here. */
  authorize: (request: Request) => boolean | Promise<boolean>;
}

/** Mount via app.route('/agntia', createAgntiaRouter(...)). All routes require host authorization. */
export function createAgntiaRouter(options: HonoOptions): Hono {
  if (typeof options.authorize !== 'function') throw new TypeError('Hono authorization is required');
  const app = new Hono();
  const tools = createAgntiaTools(options.client, options);
  function outputLinks(result: unknown, prefix: string): unknown {
    if (!result || typeof result !== 'object' || !('outputs' in result) || !Array.isArray(result.outputs)) return result;
    return { ...result, outputs: result.outputs.map((output: { url: string; srt?: string | null }) => ({
      ...output, url: prefix + output.url.replace(/^\/api/, ''), srt: output.srt ? prefix + output.srt.replace(/^\/api/, '') : null,
    })) };
  }
  app.use('*', async (c, next) => {
    if (!await options.authorize(c.req.raw)) return c.json({ error: 'Unauthorized' }, 401);
    await next();
  });
  app.onError((error, c) => {
    if (error instanceof AgntiaError) return new Response(JSON.stringify({ error: error.message, detail: error.detail }), { status: error.status, headers: { 'Content-Type': 'application/json' } });
    if (error instanceof TypeError || error instanceof SyntaxError) return c.json({ error: error.message }, 400);
    return c.json({ error: 'Agntia service unavailable' }, 502);
  });
  app.get('/status', async c => c.json(await options.client.status()));
  app.get('/tools', c => c.json({ tools: tools.definitions }));
  app.post('/tools/:name', async c => {
    const args: unknown = await c.req.json();
    const result = await tools.execute(c.req.param('name'), args);
    const prefix = c.req.path.slice(0, c.req.path.lastIndexOf('/tools/'));
    return c.body(JSON.stringify(outputLinks(result, prefix)), 200, { 'Content-Type': 'application/json' });
  });
  app.get('/projects/:pid/jobs/:jid', async c => {
    const prefix = c.req.path.slice(0, c.req.path.lastIndexOf('/projects/'));
    const job = await options.client.getJob(c.req.param('pid'), c.req.param('jid'));
    return c.body(JSON.stringify(outputLinks(job, prefix)), 200, { 'Content-Type': 'application/json' });
  });
  async function stream(path: string, range?: string): Promise<Response> {
    const upstream = await options.client.download(path, range);
    const headers = new Headers({ 'Cache-Control': 'private, no-store', 'X-Content-Type-Options': 'nosniff' });
    for (const name of ['Content-Type', 'Content-Length', 'Content-Range', 'Accept-Ranges', 'ETag', 'Last-Modified']) {
      const value = upstream.headers.get(name); if (value) headers.set(name, value);
    }
    return new Response(upstream.body, { status: upstream.status, headers });
  }
  app.get('/projects/:pid/assets/:aid/media', c => stream(`/api/projects/${c.req.param('pid')}/assets/${c.req.param('aid')}/media`, c.req.header('Range')));
  app.get('/projects/:pid/renders/:group/:file', c => stream(`/api/projects/${c.req.param('pid')}/renders/${c.req.param('group')}/${c.req.param('file')}`, c.req.header('Range')));
  return app;
}
