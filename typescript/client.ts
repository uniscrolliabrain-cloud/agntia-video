import type { Asset, AssetRole, Job, Plan, Project, ProjectPatch, Status } from './types.js';
export type * from './types.js';

export class AgntiaError extends Error {
  readonly status: number;
  readonly detail: unknown;
  constructor(status: number, detail: unknown) {
    super(typeof detail === 'string' ? detail : `Agntia returned HTTP ${status}`);
    this.name = 'AgntiaError'; this.status = status; this.detail = detail;
  }
}

export interface ClientOptions {
  baseUrl: string; token?: string; fetch?: typeof globalThis.fetch; timeoutMs?: number;
}
export interface WaitOptions { timeoutMs?: number; intervalMs?: number; signal?: AbortSignal; onProgress?: (job: Job) => void }
const id = (value: string): string => {
  if (!/^[a-f0-9]{32}$/.test(value)) throw new TypeError('Invalid Agntia identifier');
  return value;
};

/** Server-side client: keep its token out of browser bundles and model prompts. */
export class AgntiaClient {
  readonly baseUrl: string;
  #token: string; #fetch: typeof globalThis.fetch; #timeout: number;
  constructor(options: ClientOptions) {
    const url = new URL(options.baseUrl);
    if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password || url.search || url.hash || url.pathname !== '/') {
      throw new TypeError('baseUrl must be an HTTP(S) origin without credentials or path');
    }
    this.baseUrl = url.origin; this.#token = options.token || ''; this.#fetch = options.fetch || globalThis.fetch;
    this.#timeout = options.timeoutMs ?? 120000;
  }
  async #response(path: string, init: RequestInit = {}): Promise<Response> {
    const headers = new Headers(init.headers);
    if (this.#token) headers.set('Authorization', `Bearer ${this.#token}`);
    const signal = init.signal ? AbortSignal.any([init.signal, AbortSignal.timeout(this.#timeout)]) : AbortSignal.timeout(this.#timeout);
    const response = await this.#fetch(this.baseUrl + path, { ...init, headers, signal, redirect: 'error' });
    if (!response.ok) {
      let detail: unknown = `Agntia returned HTTP ${response.status}`;
      try { detail = ((await response.json()) as { detail?: unknown }).detail ?? detail; } catch { /* Non-JSON errors are not exposed. */ }
      throw new AgntiaError(response.status, detail);
    }
    return response;
  }
  async #json<T>(path: string, method = 'GET', body?: unknown, signal?: AbortSignal): Promise<T> {
    const response = await this.#response(path, { method, ...(body !== undefined ? { headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) } : {}), signal });
    return await response.json() as T;
  }
  status(): Promise<Status> { return this.#json('/api/status'); }
  listProjects(): Promise<Pick<Project, 'id' | 'name'>[]> { return this.#json('/api/projects'); }
  createProject(name: string): Promise<Project> { return this.#json('/api/projects', 'POST', { name }); }
  getProject(pid: string): Promise<Project> { return this.#json(`/api/projects/${id(pid)}`); }
  /** revision is mandatory: a 409 requires reading the project again, never a blind retry. */
  updateProject(pid: string, patch: ProjectPatch): Promise<Project> { return this.#json(`/api/projects/${id(pid)}`, 'PATCH', patch); }
  saveProject(project: Project): Promise<Project> {
    return this.#json(`/api/projects/${id(project.id)}`, 'PUT', { revision: project.revision, settings: project.settings, plan: project.plan, briefing: project.briefing });
  }
  async upload(pid: string, file: Blob, filename: string, signal?: AbortSignal): Promise<Asset> {
    const form = new FormData(); form.append('file', file, filename);
    return (await this.#response(`/api/projects/${id(pid)}/upload`, { method: 'POST', body: form, signal })).json() as Promise<Asset>;
  }
  setAssetRole(pid: string, aid: string, role: AssetRole): Promise<Asset> { return this.#json(`/api/projects/${id(pid)}/assets/${id(aid)}`, 'PATCH', { role }); }
  importInbox(pid: string): Promise<Job> { return this.#json(`/api/projects/${id(pid)}/import-inbox`, 'POST'); }
  analyze(pid: string): Promise<Job> { return this.#json(`/api/projects/${id(pid)}/analyze`, 'POST'); }
  chat(pid: string, message: string): Promise<Job> { return this.#json(`/api/projects/${id(pid)}/chat`, 'POST', { message }); }
  detectBeats(pid: string, aid: string): Promise<Job> { return this.#json(`/api/projects/${id(pid)}/assets/${id(aid)}/beats`, 'POST'); }
  snapBeats(pid: string, revision: number, tolerance = .2, minimum = .5): Promise<{ project: Project; changed: number }> {
    return this.#json(`/api/projects/${id(pid)}/snap-beats`, 'POST', { revision, tolerance, minimum });
  }
  undoBeats(pid: string, revision: number): Promise<Project> { return this.#json(`/api/projects/${id(pid)}/undo-beats`, 'POST', { revision }); }
  render(pid: string, mode: 'preview' | 'export' = 'preview'): Promise<Job> { return this.#json(`/api/projects/${id(pid)}/render`, 'POST', { mode }); }
  listJobs(pid: string): Promise<Job[]> { return this.#json(`/api/projects/${id(pid)}/jobs`); }
  getJob(pid: string, jid: string, signal?: AbortSignal): Promise<Job> { return this.#json(`/api/projects/${id(pid)}/jobs/${id(jid)}`, 'GET', undefined, signal); }
  getPlan(pid: string): Promise<{ name: string; briefing: string; settings: Project['settings']; plan: Plan }> { return this.#json(`/api/projects/${id(pid)}/download-plan`); }
  /** Paths are restricted before adding the token. No arbitrary URL download/SSRF tool. */
  download(path: string, range?: string): Promise<Response> {
    if (!/^\/api\/projects\/[a-f0-9]{32}\/(?:renders\/[a-f0-9]{32}\/(?:podcast|clip-\d{2})\.(?:mp4|srt)|assets\/[a-f0-9]{32}\/media)$/.test(path)) {
      throw new TypeError('Only Agntia source media and render paths can be downloaded');
    }
    return this.#response(path, { headers: range ? { Range: range } : undefined });
  }
  async waitForJob(pid: string, jid: string, options: WaitOptions = {}): Promise<Job> {
    const signal = AbortSignal.any([AbortSignal.timeout(options.timeoutMs ?? 600000), ...(options.signal ? [options.signal] : [])]);
    const interval = Math.max(100, options.intervalMs ?? 1000);
    while (true) {
      signal.throwIfAborted();
      const job = await this.getJob(pid, jid, signal); options.onProgress?.(job);
      if (job.status === 'error') throw new AgntiaError(422, job.message);
      if (job.status === 'done') return job;
      await new Promise<void>((resolve, reject) => {
        const abort = () => { clearTimeout(timer); reject(signal.reason); };
        const timer = setTimeout(() => { signal.removeEventListener('abort', abort); resolve(); }, interval);
        signal.addEventListener('abort', abort, { once: true });
        if (signal.aborted) abort();
      });
    }
  }
}
