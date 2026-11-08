import { Hono } from 'hono';
import { bearerAuth } from 'hono/bearer-auth';
import { AgntiaClient } from '../typescript/client.ts';
import { createAgntiaRouter } from '../typescript/hono.ts';

// In your other repo, change imports to @agntia/video and @agntia/video/hono.
const app = new Hono();
const hostToken = process.env.HOST_AGENT_TOKEN;
const backendToken = process.env.AGNTIA_ACCESS_TOKEN;
if (!hostToken || !backendToken) throw new Error('Configure HOST_AGENT_TOKEN and AGNTIA_ACCESS_TOKEN');

const client = new AgntiaClient({ baseUrl: process.env.AGNTIA_BASE_URL || 'http://127.0.0.1:8000', token: backendToken });
// Replace with your own session/auth middleware. This example uses a separate host token.
app.use('/video/*', bearerAuth({ token: hostToken }));
app.route('/video', createAgntiaRouter({
  client,
  // The middleware above has already verified this request. Required explicitly.
  authorize: () => true,
}));
export default app;
