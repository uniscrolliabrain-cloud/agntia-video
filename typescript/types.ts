export type Language = 'es' | 'en' | 'fr';
export type AssetRole = 'dialogue' | 'avatar' | 'broll' | 'audio' | 'music';
export interface MusicSettings {
  asset_id: string | null; volume: number; start: number; loop: boolean; ducking: boolean; fade_seconds: number;
}
export interface Settings {
  source_language: 'auto' | Language;
  subtitles: 'off' | 'original' | Language;
  fit: 'contain' | 'crop';
  voice_enhancement: 'off' | 'studio' | 'ai';
  voice_strength: number;
  music: MusicSettings;
}
export interface Segment {
  asset_id: string; start: number; end: number; audio_id?: string | null; audio_start?: number | null; note?: string;
}
export interface Clip { title: string; start: number; end: number }
export interface Plan { segments: Segment[]; clips: Clip[] }
export interface TranscriptItem { start: number; end: number; text: string }
export interface Analysis { summary: string; transcript: TranscriptItem[]; highlights: TranscriptItem[]; model?: string }
export interface Beats { times: number[]; bpm: number | null; duration?: number; regularity?: number; notice?: string }
export interface Asset {
  id: string; name: string; stored_name: string; sha256: string; role: AssetRole;
  duration: number; has_audio: boolean; has_video: boolean; analysis?: Analysis; beats?: Beats;
}
export interface Project {
  id: string; name: string; revision: number; briefing: string; settings: Settings; plan: Plan; assets: Asset[];
  messages: { role: 'user' | 'assistant'; content: string }[];
  beat_undo?: { before: Plan; after: Plan };
}
export interface ProjectPatch {
  revision: number; briefing?: string; plan?: Plan;
  settings?: Partial<Omit<Settings, 'music'>> & { music?: Partial<MusicSettings> };
}
export interface Output { name: string; url: string; srt: string | null }
export interface Job {
  id: string; project_id: string; kind: string; status: 'queued' | 'running' | 'done' | 'error';
  message: string; outputs: Output[]; revision?: number; mode?: 'preview' | 'export';
  reply?: string; beat_count?: number; bpm?: number | null;
}
export interface Status {
  providers: { deepseek: boolean; gemini: boolean; deepseek_model: string; gemini_model: string };
  ffmpeg: boolean; inbox: string;
  audio: { voice_ai: boolean; voice_studio: boolean; beats: boolean; engine: string; local: boolean };
}
