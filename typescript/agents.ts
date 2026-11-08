import { AgntiaClient } from './client.js';
import type { AssetRole, ProjectPatch } from './types.js';

type Schema = {
  type?: string | string[]; properties?: Record<string, Schema>; required?: string[]; additionalProperties?: boolean;
  items?: Schema; enum?: unknown[]; minimum?: number; maximum?: number; minLength?: number; maxLength?: number;
  maxItems?: number; pattern?: string; description?: string;
};
export interface ToolDefinition { name: string; description: string; parameters: Schema }
export interface UploadSource { file: Blob; filename: string }
export interface AgentOptions {
  /** Resolve opaque IDs using your repository's own storage and permissions, never arbitrary model paths. */
  resolveUpload?: (reference: string) => Promise<UploadSource>;
  allow?: readonly string[];
}
const str = (maxLength = 1000): Schema => ({ type: 'string', minLength: 1, maxLength });
const identifier: Schema = { type: 'string', pattern: '^[a-f0-9]{32}$' };
const number = (minimum = 0, maximum = 86400): Schema => ({ type: 'number', minimum, maximum });
const choice = (...values: string[]): Schema => ({ type: 'string', enum: values });
const object = (properties: Record<string, Schema>, required = Object.keys(properties)): Schema => ({ type: 'object', properties, required, additionalProperties: false });
const revision: Schema = { type: 'integer', minimum: 0 };
const nullableId: Schema = { type: ['string', 'null'], pattern: '^[a-f0-9]{32}$' };
const plan: Schema = object({
  segments: { type: 'array', maxItems: 500, items: object({
    asset_id: identifier, start: number(), end: number(), audio_id: nullableId,
    audio_start: { type: ['number', 'null'], minimum: 0 }, note: { type: 'string', maxLength: 1000 },
  }, ['asset_id', 'start', 'end']) },
  clips: { type: 'array', maxItems: 30, items: object({ title: str(120), start: number(), end: number() }) },
  captions: { type: ['array', 'null'], maxItems: 3000, items: object({ start: number(), end: number(), text: str(2000) }) },
}, ['segments', 'clips']);
const settings: Schema = object({
  source_language: choice('auto', 'es', 'en', 'fr'), subtitles: choice('off', 'original', 'es', 'en', 'fr'), fit: choice('contain', 'crop'),
  voice_enhancement: choice('off', 'studio', 'ai'), voice_strength: number(0, 1),
  music: object({ asset_id: nullableId, volume: number(0, 1), start: number(), loop: { type: 'boolean' }, ducking: { type: 'boolean' }, fade_seconds: number(0, 10) }, []),
}, []);

/** Validate model arguments before any side effect, including unknown fields and NaN. */
function validate(value: unknown, schema: Schema, path = 'arguments'): void {
  if (schema.type) {
    const types = Array.isArray(schema.type) ? schema.type : [schema.type];
    const actual = value === null ? 'null' : Array.isArray(value) ? 'array' : typeof value;
    if (!types.includes(actual) && !(types.includes('integer') && typeof value === 'number' && Number.isInteger(value))) throw new TypeError(`${path}: invalid type`);
  }
  if (schema.enum && !schema.enum.includes(value)) throw new TypeError(`${path}: invalid choice`);
  if (typeof value === 'number' && (!Number.isFinite(value) || (schema.minimum !== undefined && value < schema.minimum) || (schema.maximum !== undefined && value > schema.maximum))) throw new TypeError(`${path}: number out of range`);
  if (typeof value === 'string' && ((schema.minLength !== undefined && value.length < schema.minLength) || (schema.maxLength !== undefined && value.length > schema.maxLength) || (schema.pattern && !new RegExp(schema.pattern).test(value)))) throw new TypeError(`${path}: invalid string`);
  if (Array.isArray(value)) {
    if (schema.maxItems !== undefined && value.length > schema.maxItems) throw new TypeError(`${path}: too many items`);
    if (schema.items) value.forEach((item, i) => validate(item, schema.items!, `${path}[${i}]`));
  } else if (value && typeof value === 'object') {
    const record = value as Record<string, unknown>;
    for (const key of schema.required || []) if (!Object.hasOwn(record, key)) throw new TypeError(`${path}.${key}: required`);
    for (const [key, val] of Object.entries(record)) {
      const property = Object.hasOwn(schema.properties || {}, key) ? schema.properties![key] : undefined;
      if (!property && schema.additionalProperties === false) throw new TypeError(`${path}.${key}: unexpected field`);
      if (property) validate(val, property, `${path}.${key}`);
    }
  }
}

export function createAgntiaTools(client: AgntiaClient, options: AgentOptions = {}) {
  const definitions: ToolDefinition[] = [];
  const handlers = new Map<string, (args: Record<string, unknown>) => Promise<unknown>>();
  function add(name: string, description: string, parameters: Schema, handler: (args: Record<string, unknown>) => Promise<unknown>) {
    if (options.allow && !options.allow.includes(name)) return;
    definitions.push({ name, description, parameters }); handlers.set(name, handler);
  }
  add('agntia_status', 'Check FFmpeg, local AI voice and configured providers. No API keys are returned.', object({}), () => client.status());
  add('agntia_projects', 'List available podcast projects.', object({}), () => client.listProjects());
  add('agntia_create_project', 'Create a project. Do not retry blindly; keep the returned project ID.', object({ name: str(100) }), a => client.createProject(a.name as string));
  add('agntia_project', 'Read assets, transcripts, beat markers, settings, plan and current revision before editing.', object({ project_id: identifier }), a => client.getProject(a.project_id as string));
  add('agntia_update_project', 'Edit briefing, ordered cuts, clips, AI voice or music. Include current revision. On 409 reread and reconcile; never overwrite blindly. Clips use output timeline seconds. Settings are merged.', object({ project_id: identifier, revision, briefing: { type: 'string', maxLength: 20000 }, settings, plan }, ['project_id', 'revision']), a => {
    const { project_id, ...patch } = a;
    return client.updateProject(project_id as string, patch as unknown as ProjectPatch);
  });
  if (options.resolveUpload) add('agntia_upload', 'Upload media using an opaque reference authorized by the host application. Do not supply URLs or local paths.', object({ project_id: identifier, upload_ref: str(500) }), async a => {
    const source = await options.resolveUpload!(a.upload_ref as string);
    return client.upload(a.project_id as string, source.file, source.filename);
  });
  add('agntia_asset_role', 'Classify an uploaded file as dialogue, avatar, B-roll, audio or music.', object({ project_id: identifier, asset_id: identifier, role: choice('dialogue', 'avatar', 'broll', 'audio', 'music') }), a => client.setAssetRole(a.project_id as string, a.asset_id as string, a.role as AssetRole));
  add('agntia_import_inbox', 'Import the Agntia SERVER inbox folder. This is not the agent computer filesystem. Returns an asynchronous job.', object({ project_id: identifier }), a => client.importInbox(a.project_id as string));
  add('agntia_analyze', 'Analyze source media with Gemini, returning a job. Sends reduced media to the provider and may incur cost. Requires its configured key.', object({ project_id: identifier }), a => client.analyze(a.project_id as string));
  add('agntia_chat', 'Ask configured DeepSeek to update the briefing or propose cuts. Returns a job. If the host agent edits the plan itself, use update_project instead; no extra LLM is needed.', object({ project_id: identifier, message: str(10000) }), a => client.chat(a.project_id as string, a.message as string));
  add('agntia_detect_beats', 'Detect percussion onsets locally in an uploaded song. Returns a job; then reread the project.', object({ project_id: identifier, asset_id: identifier }), a => client.detectBeats(a.project_id as string, a.asset_id as string));
  add('agntia_snap_beats', 'Move existing cut boundaries near detected song beats, preserving total duration and source limits. Review phrases in a preview.', object({ project_id: identifier, revision, tolerance: number(.001, 1), minimum: number(.2, 10) }, ['project_id', 'revision']), a => client.snapBeats(a.project_id as string, a.revision as number, a.tolerance as number | undefined, a.minimum as number | undefined));
  add('agntia_undo_beats', 'Undo the last beat adjustment if the plan has not changed.', object({ project_id: identifier, revision }), a => client.undoBeats(a.project_id as string, a.revision as number));
  add('agntia_render', 'Render a preview or final MP4 podcast and clips. Default mode is preview. Returns a job, NOT a completed video. Poll job until done and return outputs for review.', object({ project_id: identifier, mode: choice('preview', 'export') }, ['project_id']), a => client.render(a.project_id as string, (a.mode as 'preview' | 'export' | undefined) ?? 'preview'));
  add('agntia_jobs', 'List recent background jobs for a project.', object({ project_id: identifier }), a => client.listJobs(a.project_id as string));
  add('agntia_job', 'Read one job, including completion/error and media URLs. A stopped polling loop does not cancel a render.', object({ project_id: identifier, job_id: identifier }), a => client.getJob(a.project_id as string, a.job_id as string));
  add('agntia_plan', 'Get the editable briefing/settings/plan as JSON.', object({ project_id: identifier }), a => client.getPlan(a.project_id as string));
  return {
    definitions,
    /** OpenAI-compatible definitions; pair with execute in your existing agent loop. */
    openAI: definitions.map(definition => ({ type: 'function' as const, function: definition })),
    async execute(name: string, args: unknown): Promise<unknown> {
      const definition = definitions.find(item => item.name === name);
      const handler = handlers.get(name);
      if (!definition || !handler) throw new TypeError('Unknown or disabled Agntia tool');
      validate(args, definition.parameters);
      return handler(args as Record<string, unknown>);
    },
  };
}
export type AgntiaTools = ReturnType<typeof createAgntiaTools>;
