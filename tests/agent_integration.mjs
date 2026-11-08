import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { openAsBlob } from 'node:fs';
import { mkdtemp, writeFile, rm } from 'node:fs/promises';
import { createServer } from 'node:net';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { AgntiaClient, AgntiaError } from '../dist/client.js';
import { createAgntiaTools } from '../dist/agents.js';
import { createAgntiaRouter } from '../dist/hono.js';
import { Hono } from 'hono';

const root = await mkdtemp(join(tmpdir(), 'agntia-agent-'));
const token = 'integration-only-local-test-token';
const listener = createServer();
await new Promise(resolve => listener.listen(0, '127.0.0.1', resolve));
const port = listener.address().port;
await new Promise(resolve => listener.close(resolve));
const server = spawn(process.env.PYTHON || 'python', ['-m', 'uvicorn', 'agntia.app:app', '--host', '127.0.0.1', '--port', String(port)], {
  env: { ...process.env, AGNTIA_DATA_DIR: join(root, 'data'), AGNTIA_INBOX_DIR: join(root, 'inbox'), AGNTIA_ACCESS_TOKEN: token, DEEPSEEK_API_KEY: '', GEMINI_API_KEY: '' },
  stdio: ['ignore', 'pipe', 'pipe'],
});
let logs = ''; server.stdout.on('data', data => logs += data); server.stderr.on('data', data => logs += data);
try {
  const client = new AgntiaClient({ baseUrl: `http://127.0.0.1:${port}`, token });
  let ready = false;
  for (let n = 0; n < 100; n++) {
    try { await client.status(); ready = true; break; } catch { await new Promise(resolve => setTimeout(resolve, 100)); }
  }
  assert(ready, 'Python backend did not start');
  const rate = 16000, count = rate * 4, buffer = Buffer.alloc(44 + count * 2);
  buffer.write('RIFF', 0); buffer.writeUInt32LE(buffer.length - 8, 4); buffer.write('WAVEfmt ', 8);
  buffer.writeUInt32LE(16, 16); buffer.writeUInt16LE(1, 20); buffer.writeUInt16LE(1, 22);
  buffer.writeUInt32LE(rate, 24); buffer.writeUInt32LE(rate * 2, 28); buffer.writeUInt16LE(2, 32); buffer.writeUInt16LE(16, 34);
  buffer.write('data', 36); buffer.writeUInt32LE(count * 2, 40);
  for (let n = 0; n < count; n++) { const t = n / rate % .5; buffer.writeInt16LE(Math.round(14000 * Math.sin(2 * Math.PI * 120 * t) * Math.exp(-40 * t)), 44 + n * 2); }
  const path = join(root, 'episode.wav'); await writeFile(path, buffer);
  const tools = createAgntiaTools(client, { resolveUpload: async ref => { assert.equal(ref, 'episode'); return { file: await openAsBlob(path), filename: 'episode.wav' }; } });
  const project = await tools.execute('agntia_create_project', { name: 'Agent-operated podcast' });
  const asset = await tools.execute('agntia_upload', { project_id: project.id, upload_ref: 'episode' });
  let current = await client.getProject(project.id);
  current = await tools.execute('agntia_update_project', { project_id: project.id, revision: current.revision, briefing: 'Clear voice and rhythmic cuts',
    settings: { voice_enhancement: 'ai', music: { asset_id: asset.id, volume: .15, ducking: true } },
    plan: { segments: [{ asset_id: asset.id, start: 0, end: 1.12 }, { asset_id: asset.id, start: 1.3, end: 2.2 }], clips: [{ title: 'Moment', start: 0, end: .6 }] },
  });
  await assert.rejects(client.updateProject(project.id, { revision: project.revision, briefing: 'stale' }), error => error instanceof AgntiaError && error.status === 409);
  const detection = await tools.execute('agntia_detect_beats', { project_id: project.id, asset_id: asset.id });
  await client.waitForJob(project.id, detection.id);
  current = await client.getProject(project.id); assert(current.assets[0].beats.times.length > 3);
  await tools.execute('agntia_snap_beats', { project_id: project.id, revision: current.revision, tolerance: .2 });
  const rendering = await tools.execute('agntia_render', { project_id: project.id, mode: 'preview' });
  const done = await client.waitForJob(project.id, rendering.id, { timeoutMs: 60000 });
  assert.equal(done.outputs.length, 2);
  const result = await client.download(done.outputs[0].url, 'bytes=0-99');
  assert.equal(result.status, 206); assert.equal((await result.arrayBuffer()).byteLength, 100);
  // The same result is available through the host app, with its own access control.
  const app = new Hono(); app.route('/video', createAgntiaRouter({ client, authorize: req => req.headers.get('x-session') === 'test-session' }));
  const headers = { 'x-session': 'test-session' };
  const response = await app.request(`/video/projects/${project.id}/jobs/${done.id}`, { headers });
  const routed = await response.json();
  const protectedUrl = routed.outputs[0].url; assert(protectedUrl.startsWith('/video/'));
  assert.equal((await app.request(protectedUrl)).status, 401);
  const media = await app.request(protectedUrl, { headers: { ...headers, Range: 'bytes=0-99' } });
  assert.equal(media.status, 206); assert.equal((await media.arrayBuffer()).byteLength, 100);
  console.log('PASS: TypeScript agent + Python API + real upload + revision conflict + local voice/music/beats + podcast/clip preview + Hono protected streaming');
} catch (error) { console.error(logs); throw error; }
finally {
  server.kill('SIGTERM');
  await new Promise(resolve => { const timer = setTimeout(() => { server.kill('SIGKILL'); resolve(); }, 10000); server.once('exit', () => { clearTimeout(timer); resolve(); }); });
  await rm(root, { recursive: true, force: true });
}
