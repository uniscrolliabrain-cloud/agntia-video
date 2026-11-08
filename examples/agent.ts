import { AgntiaClient } from '../typescript/client.js';
import { createAgntiaTools } from '../typescript/agents.js';

const client = new AgntiaClient({ baseUrl: process.env.AGNTIA_BASE_URL || 'http://127.0.0.1:8000', token: process.env.AGNTIA_ACCESS_TOKEN });
export const videoTools = createAgntiaTools(client);

// Register videoTools.openAI in your existing model tool list. Your agent loop:
export async function executeVideoTool(name: string, jsonArguments: string) {
  return videoTools.execute(name, JSON.parse(jsonArguments));
}

// Or call the typed client directly, without paying for a second LLM:
export async function enableVoiceAndPreview(projectId: string) {
  const project = await client.getProject(projectId);
  await client.updateProject(projectId, { revision: project.revision, settings: { voice_enhancement: 'ai', voice_strength: .8 } });
  const job = await client.render(projectId, 'preview');
  return client.waitForJob(projectId, job.id);
}
