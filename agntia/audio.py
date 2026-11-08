"""Local speech processing and beat-guided edits. No cloud inference."""
import array
import bisect
import json
import math
import statistics
import tempfile
import wave
from pathlib import Path

from . import media, storage
from .models import Plan, Settings, validate_plan

MODEL = Path(__file__).parent / "resources" / "rnnoise.rnnn"


def capabilities() -> dict:
    try:
        filters = media.run(["ffmpeg", "-hide_banner", "-filters"], timeout=15).stdout
    except ValueError:
        filters = ""
    return {"voice_ai": MODEL.is_file() and " arnndn " in filters, "voice_studio": " afftdn " in filters,
            "beats": bool(filters), "engine": "RNNoise / FFmpeg", "local": True}


def voice_filter(settings: Settings, work: Path) -> str:
    if settings.voice_enhancement == "off":
        return "anull"
    filters = ["aresample=48000", "highpass=f=75"]
    if settings.voice_enhancement == "ai":
        if not MODEL.is_file():
            raise ValueError("Falta el modelo local RNNoise. Reinstala Agntia con sus recursos.")
        # A relative fixed name avoids FFmpeg filter escaping on Windows paths.
        import shutil
        shutil.copyfile(MODEL, work / "voice-model.rnnn")
        filters += [f"arnndn=m=voice-model.rnnn:mix={settings.voice_strength}"]
    else:
        filters += [f"afftdn=nr={4 + settings.voice_strength * 12}:nf=-30:tn=1"]
    filters += ["equalizer=f=3000:t=q:w=1:g=2", "acompressor=threshold=0.125:ratio=2:attack=10:release=120:makeup=1.4"]
    return ",".join(filters)


def mix_filter(settings: Settings, duration: float, music: dict | None, timeline_start: float) -> str:
    graph = ["[0:a]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,aformat=channel_layouts=stereo[voice]"]
    selected = settings.music
    offset = selected.start + timeline_start
    if music is None or selected.volume == 0 or (not selected.loop and offset >= music["duration"]):
        return ";".join(graph + ["[voice]alimiter=limit=0.891:level=0:latency=1[outa]"])
    if selected.loop:
        offset %= music["duration"]
    fade = min(selected.fade_seconds, duration / 2)
    graph += [f"[1:a]atrim=start={offset}:duration={duration},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={duration},atrim=duration={duration},volume={selected.volume}[musicbase]"]
    if fade:
        graph += [f"[musicbase]afade=t=in:d={fade},afade=t=out:st={max(0, duration-fade)}:d={fade}[music]"]
    else:
        graph += ["[musicbase]anull[music]"]
    if selected.ducking:
        graph += ["[voice]asplit=2[mainvoice][sidechain]", "[music][sidechain]sidechaincompress=threshold=0.025:ratio=8:attack=15:release=300[ducked]",
                  "[mainvoice][ducked]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[mixed]"]
    else:
        graph += ["[voice][music]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[mixed]"]
    graph += ["[mixed]alimiter=limit=0.891:level=0:latency=1[outa]"]
    return ";".join(graph)


def detect_beats(project: dict, asset: dict, progress=lambda _: None) -> dict:
    if not asset["has_audio"]:
        raise ValueError("El archivo seleccionado no tiene audio")
    if asset["duration"] > 7200:
        raise ValueError("Divide la música en archivos de hasta 2 horas para detectar beats")
    cache = storage.DATA / "beats" / f"v1-{asset['sha256']}.json"
    if cache.is_file():
        return json.loads(cache.read_text(encoding="utf-8"))
    progress("Detectando golpes de la música en este equipo")
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "beats.wav"
        media.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(storage.asset_path(project["id"], asset)),
                   "-vn", "-af", "highpass=f=35,lowpass=f=240", "-ac", "1", "-ar", "8000", "-c:a", "pcm_s16le", str(path)])
        energy = []
        with wave.open(str(path), "rb") as source:
            decoded_duration = source.getnframes() / source.getframerate()
            while raw := source.readframes(160):
                samples = array.array("h", raw)
                import sys
                if sys.byteorder != "little":
                    samples.byteswap()
                energy.append(math.sqrt(sum(s*s for s in samples) / max(len(samples), 1)) / 32768)
    # Positive changes in low-frequency energy reveal kick/percussive onsets.
    novelty = [max(0, value - (energy[i-1] if i else 0)) for i, value in enumerate(energy)]
    peak = max(novelty, default=0)
    beats, strengths = [], []
    for i, value in enumerate(novelty):
        if peak < 0.0001 or value < peak * 0.06:
            continue
        local = novelty[max(0, i-20):i+21]
        threshold = statistics.median(local) * 2 + peak * .025
        if value <= threshold or value < max(novelty[max(0, i-2):i+3]):
            continue
        moment = round(i * .02, 3)
        if beats and moment - beats[-1] < .22:
            if value > strengths[-1]:
                beats[-1], strengths[-1] = moment, value
        else:
            beats.append(moment)
            strengths.append(value)
    intervals = [b-a for a, b in zip(beats, beats[1:]) if .25 <= b-a <= 1.5]
    interval = statistics.median(intervals) if len(intervals) >= 3 else None
    bpm = round(60 / interval, 1) if interval else None
    regularity = max(0, 1 - statistics.pstdev(intervals) / interval) if interval else 0
    result = {"times": beats, "bpm": bpm, "regularity": round(regularity, 3), "detector": "low-frequency-onset-v1",
              "duration": decoded_duration,
              "notice": "Golpes percutivos estimados; revisa los marcadores. No todos los golpes son beats musicales."}
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(result), encoding="utf-8")
    return result


def music_beats_near(moment: float, settings: Settings, asset: dict, tolerance: float) -> list[float]:
    times = asset.get("beats", {}).get("times", [])
    duration = asset.get("beats", {}).get("duration", asset["duration"])
    original = moment + settings.music.start
    cycle = math.floor(original / duration)
    candidates = []
    for n in ([max(0, cycle-1), cycle, cycle+1] if settings.music.loop else [0]):
        target = original - n * duration
        left, right = bisect.bisect_left(times, target-tolerance), bisect.bisect_right(times, target+tolerance)
        candidates.extend(t + n * duration - settings.music.start for t in times[left:right])
    return sorted(set(candidates), key=lambda t: abs(t-moment))


def snap_to_beats(project: dict, tolerance: float, minimum: float) -> tuple[Plan, int]:
    settings = Settings.model_validate(project["settings"])
    index = {a["id"]: a for a in project["assets"]}
    song = index.get(settings.music.asset_id)
    if not song or not song.get("beats", {}).get("times"):
        raise ValueError("Selecciona una música y detecta sus beats primero")
    plan = validate_plan(Plan.model_validate(project["plan"]), project["assets"])
    if len(plan.segments) < 2:
        raise ValueError("Necesitas al menos dos cortes para ajustar una transición al beat")
    boundaries, capacities = [0.0], []
    for segment in plan.segments:
        boundaries.append(boundaries[-1] + segment.end - segment.start)
        capacity = index[segment.asset_id]["duration"] - segment.start
        if segment.audio_id:
            begin = segment.audio_start if segment.audio_start is not None else segment.start
            capacity = min(capacity, index[segment.audio_id]["duration"] - begin)
        capacities.append(capacity)
    changed = 0
    for i in range(1, len(boundaries)-1):
        # Keep source IN points fixed. Only OUT points change; episode duration and clips stay put.
        for candidate in music_beats_near(boundaries[i], settings, song, tolerance):
            previous_length, next_length = candidate-boundaries[i-1], boundaries[i+1]-candidate
            if minimum <= previous_length <= capacities[i-1] and minimum <= next_length <= capacities[i]:
                if abs(candidate-boundaries[i]) > .001:
                    boundaries[i] = candidate
                    changed += 1
                break
    for i, segment in enumerate(plan.segments):
        segment.end = segment.start + boundaries[i+1] - boundaries[i]
    return validate_plan(plan, project["assets"]), changed
