import json
import subprocess
import tempfile
from pathlib import Path

from .models import Plan
from .storage import asset_path

EXTENSIONS = {".mp4", ".mov", ".mkv", ".webm", ".avi", ".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg"}


def run(args: list[str], timeout: int = 7200, cwd=None):
    try:
        return subprocess.run(args, capture_output=True, text=True, check=True, timeout=timeout, cwd=cwd)
    except FileNotFoundError:
        raise ValueError("Instala FFmpeg y ffprobe y añádelos al PATH") from None
    except subprocess.TimeoutExpired:
        raise ValueError("El proceso de vídeo ha superado el tiempo máximo") from None
    except subprocess.CalledProcessError as exc:
        # Local paths may occur here; never include API secrets in command arguments.
        raise ValueError("FFmpeg/ffprobe: " + exc.stderr[-1800:]) from None


def probe(path: Path) -> dict:
    result = json.loads(run(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)], timeout=60).stdout)
    streams = result.get("streams", [])
    duration = float(result.get("format", {}).get("duration", 0))
    if not 0 < duration < 86400:
        raise ValueError("El archivo necesita una duración válida inferior a 24 horas")
    video = any(s["codec_type"] == "video" and not s.get("disposition", {}).get("attached_pic") for s in streams)
    audio = any(s["codec_type"] == "audio" for s in streams)
    if not video and not audio:
        raise ValueError("No se ha encontrado vídeo ni audio")
    return {"duration": duration, "has_video": video, "has_audio": audio}


def resize(width: int, height: int, fit: str) -> str:
    if fit == "crop":
        return f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},setsar=1,fps=25"
    return f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=0x10121a,setsar=1,fps=25"


def render(project: dict, plan: Plan, target: Path, vertical=False, preview=True, cues=None):
    if not plan.segments:
        raise ValueError("Añade al menos un corte al montaje")
    width, height = ((270, 480) if vertical else (854, 480)) if preview else ((1080, 1920) if vertical else (1920, 1080))
    assets = {a["id"]: a for a in project["assets"]}
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="render-", dir=target.parent) as directory:
        work = Path(directory)
        pieces = []
        for number, segment in enumerate(plan.segments):
            source = assets[segment.asset_id]
            duration = segment.end - segment.start
            args = ["ffmpeg", "-nostdin", "-v", "error", "-y", "-threads", "2"]
            if source["has_video"]:
                args += ["-ss", str(segment.start), "-i", str(asset_path(project["id"], source))]
            else:
                args += ["-f", "lavfi", "-i", f"color=c=0x10121a:s={width}x{height}:r=25"]
            audio = assets[segment.audio_id] if segment.audio_id else source
            audio_start = segment.audio_start if segment.audio_start is not None else segment.start
            if audio["has_audio"]:
                args += ["-ss", str(audio_start), "-i", str(asset_path(project["id"], audio))]
            else:
                args += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
            output = work / f"part-{number:04d}.mp4"
            args += ["-t", str(duration), "-map", "0:v:0", "-map", "1:a:0", "-vf", resize(width, height, project["settings"]["fit"]),
                     "-af", "aresample=48000", "-c:v", "libx264", "-preset", "ultrafast" if preview else "fast", "-crf", "27" if preview else "21",
                     "-threads", "2", "-filter_threads", "1", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ac", "2", "-ar", "48000", str(output)]
            run(args)
            pieces.append(f"file '{output.name}'")
        (work / "concat.txt").write_text("\n".join(pieces), encoding="utf-8")
        run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "concat.txt", "-c", "copy", "joined.mp4"], cwd=work)
        args = ["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", "joined.mp4"]
        if cues:
            (work / "subtitles.srt").write_text(srt(cues), encoding="utf-8")
            args += ["-vf", "subtitles=subtitles.srt", "-c:v", "libx264", "-preset", "ultrafast" if preview else "fast", "-crf", "25" if preview else "21", "-threads", "2", "-filter_threads", "1"]
        else:
            args += ["-c:v", "copy"]
        args += ["-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-movflags", "+faststart", str(target.resolve())]
        run(args, cwd=work)
    if cues:
        target.with_suffix(".srt").write_text(srt(cues), encoding="utf-8")


def timeline_cues(project: dict, plan: Plan) -> list[dict]:
    assets = {a["id"]: a for a in project["assets"]}
    cues, cursor = [], 0.0
    for segment in plan.segments:
        source = assets[segment.audio_id or segment.asset_id]
        begin = (segment.audio_start if segment.audio_start is not None else segment.start) if segment.audio_id else segment.start
        duration = segment.end - segment.start
        for item in source.get("analysis", {}).get("transcript", []):
            left, right = max(begin, item["start"]), min(begin + duration, item["end"])
            if right > left and item.get("text", "").strip():
                cues.append({"start": cursor + left - begin, "end": cursor + right - begin, "text": item["text"]})
        cursor += duration
    return sorted(cues, key=lambda cue: cue["start"])


def srt(cues: list[dict]) -> str:
    def clock(seconds):
        ms = round(seconds * 1000)
        return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"
    return "\n\n".join(f"{n}\n{clock(c['start'])} --> {clock(c['end'])}\n{c['text']}" for n, c in enumerate(cues, 1)) + "\n"
