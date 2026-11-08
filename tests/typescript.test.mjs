import test from 'node:test';
import assert from 'node:assert/strict';
import { AgntiaClient, AgntiaError } from '../dist/client.js';
import { createAgntiaTools } from '../dist/agents.js';

const pid = 'a'.repeat(32), aid = 'b'.repeat(32), jid = 'c'.repeat(32), group = 'd'.repeat(32);
const mediaPath = `/api/projects/${pid}/renders/${group}/podcast.mp4`;
const json = (data, status = 200) => new Response(JSON.stringify(data), { status, headers: { 'Content-Type': 'application/json' } });
function clientWith(handler) { return new AgntiaClient({ baseUrl: 'https://video.example', token: 'backend-secret', fetch: handler }); }

test('typed client sends bearer server-side, current revision and partial audio settings', async () => {
  let call;
  const client = clientWith(async (url, init) => { call = { url, init }; return json({ id: pid, revision: 8 }); });
  await client.updateProject(pid, { revision: 7, settings: { music: { volume: .2 }, voice_enhancement: 'ai' } });
  assert.equal(call.url, `https://video.example/api/projects/${pid}`);
  assert.equal(call.init.method, 'PATCH');
  assert.equal(call.init.headers.get('Authorization'), 'Bearer backend-secret');
  assert.deepEqual(JSON.parse(call.init.body), { revision: 7, settings: { music: { volume: .2 }, voice_enhancement: 'ai' } });
  assert.equal(call.init.redirect, 'error');
});

test('upload uses real multipart form without forcing JSON content type', async () => {
  const client = clientWith(async (_url, init) => {
    assert(init.body instanceof FormData);
    assert.equal(init.body.get('file').name, 'voice.wav');
    assert.equal(await init.body.get('file').text(), 'media');
    assert.equal(init.headers.get('Content-Type'), null);
    return json({ id: aid });
  });
  assert.equal((await client.upload(pid, new Blob(['media']), 'voice.wav')).id, aid);
});

test('conflicts surface as 409 and mutations are never automatically retried', async () => {
  let calls = 0;
  const client = clientWith(async () => { calls++; return json({ detail: 'Revision conflict' }, 409); });
  await assert.rejects(client.updateProject(pid, { revision: 1 }), error => error instanceof AgntiaError && error.status === 409);
  assert.equal(calls, 1);
});

test('downloads restrict token to known media routes and preserve Range', async () => {
  let calls = 0;
  const client = clientWith(async (url, init) => { calls++; assert.equal(url, `https://video.example${mediaPath}`); assert.equal(init.headers.get('Range'), 'bytes=0-9'); return new Response('0123456789', { status: 206 }); });
  assert.equal((await client.download(mediaPath, 'bytes=0-9')).status, 206);
  for (const path of ['https://attacker.example/x', '//attacker.example/x', '/api/projects/../secrets', mediaPath+'?redirect=x']) assert.throws(() => client.download(path));
  assert.equal(calls, 1);
  assert.throws(() => new AgntiaClient({ baseUrl: 'https://user:secret@video.example' }));
});

test('job polling returns real completion and reports errors/abort', async () => {
  const states = ['queued', 'running', 'done'];
  const progress = [];
  const client = clientWith(async () => json({ id: jid, project_id: pid, status: states.shift(), outputs: [], message: 'ok' }));
  const done = await client.waitForJob(pid, jid, { intervalMs: 100, onProgress: job => progress.push(job.status) });
  assert.equal(done.status, 'done'); assert.deepEqual(progress, ['queued', 'running', 'done']);
  const failed = clientWith(async () => json({ id: jid, status: 'error', message: 'Missing FFmpeg' }));
  await assert.rejects(failed.waitForJob(pid, jid), /Missing FFmpeg/);
  const controller = new AbortController(); controller.abort();
  await assert.rejects(client.waitForJob(pid, jid, { signal: controller.signal }));
});

test('agent tools expose the real workflow, validate JSON and limit available actions', async () => {
  let calls = 0;
  const client = clientWith(async () => { calls++; return json({ id: pid }); });
  const tools = createAgntiaTools(client);
  assert(tools.definitions.some(t => t.name === 'agntia_render'));
  assert(!tools.definitions.some(t => t.name === 'agntia_upload'));
  for (const args of [{ project_id: pid, revision: 1, settings: { music: { volume: 2 } } },
    { project_id: pid, revision: 1.5 }, { project_id: pid, revision: 1, plan: { segments: [], clips: [], shell: 'bad' } }]) {
    await assert.rejects(tools.execute('agntia_update_project', args), TypeError);
  }
  await assert.rejects(tools.execute('agntia_render', { project_id: '../bad' }), TypeError);
  assert.equal(calls, 0);
  await tools.execute('agntia_render', { project_id: pid }); assert.equal(calls, 1);
  const readOnly = createAgntiaTools(client, { allow: ['agntia_status', 'agntia_project'] });
  assert.equal(readOnly.definitions.length, 2);
  await assert.rejects(readOnly.execute('agntia_render', { project_id: pid }));
  assert.equal(calls, 1);
});

test('uploads resolve only host-authorized references', async () => {
  const refs = [];
  const tools = createAgntiaTools(clientWith(async () => json({ id: aid })), {
    resolveUpload: async ref => { refs.push(ref); if (ref !== 'episode-42') throw new Error('Unknown upload reference'); return { file: new Blob(['x']), filename: 'x.wav' }; },
  });
  assert.equal((await tools.execute('agntia_upload', { project_id: pid, upload_ref: 'episode-42' })).id, aid);
  await assert.rejects(tools.execute('agntia_upload', { project_id: pid, upload_ref: '/etc/passwd' }), /Unknown upload/);
  assert.deepEqual(refs, ['episode-42', '/etc/passwd']);
});

test('Hono router requires host authorization and streams authenticated video', { skip: !!process.env.AGNTIA_SKIP_HONO }, async () => {
  const { Hono } = await import('hono');
  const { createAgntiaRouter } = await import('../dist/hono.js');
  let calls = 0;
  const client = clientWith(async (url, init) => {
    calls++;
    assert.equal(init.headers.get('Authorization'), 'Bearer backend-secret');
    if (url.endsWith('/media') || url.endsWith('.mp4')) {
      assert.equal(init.headers.get('Range'), 'bytes=0-9');
      return new Response('0123456789', { status: 206, headers: { 'Content-Range': 'bytes 0-9/100', 'Content-Type': 'video/mp4' } });
    }
    return json({ id: jid, status: 'done', outputs: [{ name: 'podcast', url: mediaPath, srt: null }] });
  });
  assert.throws(() => createAgntiaRouter({ client }));
  const app = new Hono();
  app.route('/video', createAgntiaRouter({ client, authorize: req => req.headers.get('x-host-session') === 'valid-session' }));
  assert.equal((await app.request('/video/tools')).status, 401); assert.equal(calls, 0);
  const headers = { 'x-host-session': 'valid-session', 'Content-Type': 'application/json' };
  const response = await app.request('/video/tools/agntia_job', { method: 'POST', headers, body: JSON.stringify({ project_id: pid, job_id: jid }) });
  assert.equal(response.status, 200);
  assert.equal((await response.json()).outputs[0].url, mediaPath.replace('/api', '/video'));
  const stream = await app.request(mediaPath.replace('/api', '/video'), { headers: { ...headers, Range: 'bytes=0-9' } });
  assert.equal(stream.status, 206); assert.equal(stream.headers.get('Content-Range'), 'bytes 0-9/100');
  assert.equal(await stream.text(), '0123456789');
});
