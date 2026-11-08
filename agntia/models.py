import math
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


class MusicSettings(StrictModel):
    asset_id: str | None = None
    volume: float = Field(default=0.15, ge=0, le=1)
    start: float = Field(default=0, ge=0)
    loop: bool = True
    ducking: bool = True
    fade_seconds: float = Field(default=1, ge=0, le=10)


class Settings(StrictModel):
    source_language: Literal["auto", "es", "en", "fr"] = "auto"
    subtitles: Literal["off", "original", "es", "en", "fr"] = "off"
    fit: Literal["contain", "crop"] = "contain"
    voice_enhancement: Literal["off", "studio", "ai"] = "off"
    voice_strength: float = Field(default=0.8, ge=0, le=1)
    music: MusicSettings = Field(default_factory=MusicSettings)


def validate_settings(settings: Settings, assets: list[dict]) -> Settings:
    if settings.music.asset_id:
        asset = next((a for a in assets if a["id"] == settings.music.asset_id), None)
        if not asset or not asset["has_audio"]:
            raise ValueError("Elige un archivo con audio para la música")
        if settings.music.start >= asset["duration"]:
            raise ValueError("El inicio de la música debe estar dentro del archivo")
    return settings


class Segment(StrictModel):
    asset_id: str
    start: float = Field(ge=0)
    end: float = Field(gt=0)
    audio_id: str | None = None
    audio_start: float | None = Field(default=None, ge=0)
    note: str = Field(default="", max_length=1000)

    @model_validator(mode="after")
    def ordered(self):
        if self.end <= self.start:
            raise ValueError("El final debe ser mayor que el inicio")
        if self.audio_start is not None and self.audio_id is None:
            raise ValueError("audio_start necesita audio_id")
        return self


class Clip(StrictModel):
    title: str = Field(min_length=1, max_length=120)
    start: float = Field(ge=0)
    end: float = Field(gt=0)


class Caption(StrictModel):
    start: float = Field(ge=0)
    end: float = Field(gt=0)
    text: str = Field(min_length=1, max_length=2000)

    @model_validator(mode="after")
    def ordered(self):
        if self.end <= self.start:
            raise ValueError("El subtítulo debe terminar después de empezar")
        return self


class Plan(StrictModel):
    segments: list[Segment] = Field(default_factory=list, max_length=500)
    clips: list[Clip] = Field(default_factory=list, max_length=30)
    captions: list[Caption] | None = Field(default=None, max_length=3000)


def validate_plan(plan: Plan, assets: list[dict]) -> Plan:
    index = {a["id"]: a for a in assets}
    total = 0.0
    for segment in plan.segments:
        if segment.asset_id not in index:
            raise ValueError("El plan menciona un archivo inexistente")
        asset = index[segment.asset_id]
        if segment.end > asset["duration"] + 0.05:
            raise ValueError(f"El corte supera la duración de {asset['name']}")
        duration = segment.end - segment.start
        if segment.audio_id:
            audio = index.get(segment.audio_id)
            if not audio or not audio["has_audio"]:
                raise ValueError("La pista de audio no existe o no tiene audio")
            start = segment.audio_start if segment.audio_start is not None else segment.start
            if start + duration > audio["duration"] + 0.05:
                raise ValueError("El corte supera la duración del audio separado")
        total += duration
    for clip in plan.clips:
        if not math.isfinite(clip.end) or clip.end <= clip.start or clip.end > total + 0.01:
            raise ValueError("Los clips deben estar dentro del podcast montado")
    for caption in plan.captions or []:
        if caption.end > total + 0.01:
            raise ValueError("Los subtítulos deben estar dentro del podcast montado")
    return plan


def slice_plan(plan: Plan, start: float, end: float) -> Plan:
    """Clip times belong to the OUTPUT timeline, not to the source files."""
    result = []
    cursor = 0.0
    for segment in plan.segments:
        duration = segment.end - segment.start
        left, right = max(start, cursor), min(end, cursor + duration)
        if right > left:
            offset = left - cursor
            data = segment.model_dump()
            data.update(start=segment.start + offset, end=segment.start + offset + right - left)
            if segment.audio_id:
                data["audio_start"] = (segment.audio_start if segment.audio_start is not None else segment.start) + offset
            result.append(Segment(**data))
        cursor += duration
    captions = None if plan.captions is None else [Caption(start=max(start, c.start)-start, end=min(end, c.end)-start, text=c.text) for c in plan.captions if min(end, c.end)>max(start, c.start)]
    return Plan(segments=result, captions=captions)
