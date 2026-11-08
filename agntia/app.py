import copy
import hmac
import json
import os
import shutil
import uuid
from typing import Any
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import Field

from . import audio, jobs, media, providers, storage
from .models import Plan, Settings, StrictModel, slice_plan, validate_plan, validate_settings

app = FastAPI(title="Agntia-video", version="0.3.0")
STATIC = Path(__file__).parent / "static"


@app.middleware("http")
async def authenticate(request: Request, call_next):
    token = os.getenv("AGNTIA_ACCESS_TOKEN", "")
    if request.url.path.startswith("/api/") and request.url.path != "/api/login":
        supplied = request.cookies.get("agntia_token", "") or request.headers.get("authorization", "").removeprefix("Bearer ")
        if token and not hmac.compare_digest(supplied.encode(), token.encode()):
            return JSONResponse({"detail": "Introduce el token de acceso del servidor"}, status_code=401)
        # A server without a token must never accept remote clients.
        if not token and request.client and request.client.host not in ("127.0.0.1", "::1", "testclient"):
            return JSONResponse({"detail": "Configura AGNTIA_ACCESS_TOKEN para acceso remoto"}, status_code=403)
    origin = request.headers.get("origin")
    if request.method not in ("GET", "HEAD", "OPTIONS") and origin and origin != str(request.base_url).rstrip("/"):
        return JSONResponse({"detail": "Origen no permitido"}, status_code=403)
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "same-origin"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; media-src 'self' blob:; connect-src 'self'; frame-ancestors 'none'"
    return response


@app.exception_handler(ValueError)
async def value_error(request, exc):
    return JSONResponse({"detail": str(exc)}, status_code=400)


@app.exception_handler(FileNotFoundError)
async def missing(request, exc):
    return JSONResponse({"detail": "No se ha encontrado el proyecto o archivo"}, status_code=404)


class Login(StrictModel):
    token: str = Field(max_length=500)


@app.post("/api/login")
def login(data: Login, request: Request):
    token = os.getenv("AGNTIA_ACCESS_TOKEN", "")
    if not token or not hmac.compare_digest(data.token.encode(), token.encode()):
        raise HTTPException(401, "Token incorrecto")
    response = JSONResponse({"ok": True})
    response.set_cookie("agntia_token", data.token, httponly=True, samesite="strict", secure=request.url.scheme == "https", max_age=86400)
    return response


@app.get("/api/status")
def status():
    return {"providers": providers.available(), "ffmpeg": bool(shutil.which("ffmpeg") and shutil.which("ffprobe")), "audio": audio.capabilities(), "inbox": str(storage.INBOX)}


@app.get("/api/openapi.json", include_in_schema=False)
def agent_openapi():
    return app.openapi()


@app.get("/api/projects")
def projects():
    values = []
    for path in (storage.DATA / "projects").glob("*/project.json"):
        p = storage.read(path.parent.name)
        values.append({"id": p["id"], "name": p["name"]})
    return values


class NewProject(StrictModel):
    name: str = Field(min_length=1, max_length=100)


@app.post("/api/projects")
def create(data: NewProject):
    return storage.create(data.name.strip() or "Mi podcast")


@app.get("/api/projects/{pid}")
def project(pid: str):
    return storage.read(pid)


class ProjectEdit(StrictModel):
    revision: int
    settings: Settings
    plan: Plan
    briefing: str = Field(max_length=20000)


@app.put("/api/projects/{pid}")
def save(pid: str, data: ProjectEdit):
    with storage.LOCK:
        p = storage.read(pid)
        if data.revision != p["revision"]:
            raise HTTPException(409, "El proyecto ha cambiado. Recárgalo antes de guardar.")
        validate_plan(data.plan, p["assets"])
        validate_settings(data.settings, p["assets"])
        if data.settings.voice_enhancement == "ai" and not audio.capabilities()["voice_ai"]:
            raise ValueError("Tu FFmpeg no incluye arnndn o falta el modelo RNNoise. Usa limpieza clásica o instala FFmpeg con arnndn.")
        p.update(settings=data.settings.model_dump(), plan=data.plan.model_dump(), briefing=data.briefing, revision=p["revision"] + 1)
        storage.write(p)
    return p


class ProjectPatch(StrictModel):
    revision: int
    briefing: str | None = Field(default=None, max_length=20000)
    settings: dict[str, Any] | None = None
    plan: Plan | None = None


@app.patch("/api/projects/{pid}")
def patch_project(pid: str, data: ProjectPatch):
    """Apply partial settings atomically, without losing another editor's changes."""
    with storage.LOCK:
        p = storage.read(pid)
        if data.revision != p["revision"]:
            raise HTTPException(409, "El proyecto ha cambiado. Lee la versión actual antes de editar.")
        settings = copy.deepcopy(p["settings"])
        if data.settings is not None:
            for key, value in data.settings.items():
                if key == "music" and isinstance(value, dict):
                    settings["music"].update(value)
                else:
                    settings[key] = value
        validated = validate_settings(Settings.model_validate(settings), p["assets"])
        if validated.voice_enhancement == "ai" and not audio.capabilities()["voice_ai"]:
            raise ValueError("La mejora RNNoise no está disponible en este servidor")
        if data.plan is not None:
            validate_plan(data.plan, p["assets"])
            p["plan"] = data.plan.model_dump()
        if data.briefing is not None:
            p["briefing"] = data.briefing
        p["settings"] = validated.model_dump()
        p["revision"] += 1
        storage.write(p)
    return p


def register(pid: str, path: Path, name: str):
    try:
        metadata = media.probe(path)
        sha = storage.fingerprint(path)
        with storage.LOCK:
            p = storage.read(pid)
            existing = next((a for a in p["assets"] if a["sha256"] == sha), None)
            if existing:
                path.unlink()
                return existing
            asset = {"id": uuid.uuid4().hex, "name": name, "stored_name": path.name, "sha256": sha,
                     "role": "dialogue" if metadata["has_audio"] else "broll", **metadata}
            p["assets"].append(asset)
            p["revision"] += 1
            storage.write(p)
            return asset
    except Exception:
        path.unlink(missing_ok=True)
        raise


@app.post("/api/projects/{pid}/upload")
def upload(pid: str, file: UploadFile = File(...)):
    storage.read(pid)
    name = (file.filename or "archivo").replace("\\", "/").split("/")[-1]
    suffix = Path(name).suffix.lower()
    if suffix not in media.EXTENSIONS:
        raise ValueError("Formato no admitido. Usa vídeo o audio (MP4, MOV, WAV, MP3…).")
    directory = storage.project_dir(pid) / "media"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{uuid.uuid4().hex}{suffix}"
    limit = float(os.getenv("AGNTIA_MAX_UPLOAD_GB", "10")) * 1024 ** 3
    try:
        size = 0
        with path.open("wb") as target:
            while chunk := file.file.read(1024 * 1024):
                size += len(chunk)
                if size > limit:
                    raise ValueError("El archivo supera AGNTIA_MAX_UPLOAD_GB")
                target.write(chunk)
        return register(pid, path, name)
    except Exception:
        path.unlink(missing_ok=True)
        raise
    finally:
        file.file.close()


@app.post("/api/projects/{pid}/import-inbox")
def import_inbox(pid: str):
    storage.read(pid)
    def work(progress):
        storage.INBOX.mkdir(parents=True, exist_ok=True)
        directory = storage.project_dir(pid) / "media"
        directory.mkdir(parents=True, exist_ok=True)
        count = 0
        for path in sorted(storage.INBOX.iterdir()):
            if path.is_symlink() or not path.is_file() or path.suffix.lower() not in media.EXTENSIONS:
                continue
            progress(f"Importando {path.name}")
            if path.stat().st_size > float(os.getenv("AGNTIA_MAX_UPLOAD_GB", "10")) * 1024 ** 3:
                raise ValueError(f"{path.name} supera el límite por archivo")
            target = directory / f"{uuid.uuid4().hex}{path.suffix.lower()}"
            shutil.copyfile(path, target)
            register(pid, target, path.name)
            count += 1
        return {"imported": count}
    return jobs.submit(pid, "import", work)


class AssetRole(StrictModel):
    role: Literal["dialogue", "avatar", "broll", "audio", "music"]


@app.patch("/api/projects/{pid}/assets/{aid}")
def asset_role(pid: str, aid: str, data: AssetRole):
    with storage.LOCK:
        p = storage.read(pid)
        asset = next((a for a in p["assets"] if a["id"] == aid), None)
        if not asset:
            raise HTTPException(404, "Archivo no encontrado")
        asset["role"] = data.role
        p["revision"] += 1
        storage.write(p)
    return asset


@app.get("/api/projects/{pid}/assets/{aid}/media")
def source_media(pid: str, aid: str):
    p = storage.read(pid)
    a = next((a for a in p["assets"] if a["id"] == aid), None)
    if not a:
        raise HTTPException(404, "Archivo no encontrado")
    return FileResponse(storage.asset_path(pid, a))


@app.post("/api/projects/{pid}/analyze")
def analyze(pid: str):
    p = storage.read(pid)
    if not providers.available()["gemini"]:
        raise ValueError("Gemini pendiente de configurar. Añade la clave al .env y reinicia.")
    if not p["assets"]:
        raise ValueError("Carga archivos antes de analizar")
    def work(progress):
        for asset in p["assets"]:
            if asset["role"] == "music" or asset["id"] == p["settings"]["music"]["asset_id"]:
                continue
            analysis = providers.analyze(p, asset, progress)
            with storage.LOCK:
                current = storage.read(pid)
                next(a for a in current["assets"] if a["id"] == asset["id"])["analysis"] = analysis
                current["revision"] += 1
                storage.write(current)
    return jobs.submit(pid, "analysis", work)


@app.post("/api/projects/{pid}/assets/{aid}/beats")
def detect_music_beats(pid: str, aid: str):
    p = storage.read(pid)
    asset = next((a for a in p["assets"] if a["id"] == aid), None)
    if not asset or not asset["has_audio"]:
        raise ValueError("Selecciona un archivo que tenga audio")
    def work(progress):
        result = audio.detect_beats(p, asset, progress)
        with storage.LOCK:
            current = storage.read(pid)
            next(a for a in current["assets"] if a["id"] == aid)["beats"] = result
            current["revision"] += 1
            storage.write(current)
        return {"beat_count": len(result["times"]), "bpm": result["bpm"]}
    return jobs.submit(pid, "beats", work)


class BeatSnapRequest(StrictModel):
    revision: int
    tolerance: float = Field(default=0.2, gt=0, le=1)
    minimum: float = Field(default=0.5, ge=0.2, le=10)


@app.post("/api/projects/{pid}/snap-beats")
def snap_music_beats(pid: str, data: BeatSnapRequest):
    with storage.LOCK:
        p = storage.read(pid)
        if p["revision"] != data.revision:
            raise HTTPException(409, "El proyecto ha cambiado. Recárgalo antes de ajustar los beats.")
        plan, changed = audio.snap_to_beats(p, data.tolerance, data.minimum)
        if changed:
            p["beat_undo"] = {"before": copy.deepcopy(p["plan"]), "after": plan.model_dump()}
            p["plan"] = plan.model_dump()
            p["revision"] += 1
            storage.write(p)
    return {"project": p, "changed": changed}


class UndoBeatsRequest(StrictModel):
    revision: int


@app.post("/api/projects/{pid}/undo-beats")
def undo_music_beats(pid: str, data: UndoBeatsRequest):
    with storage.LOCK:
        p = storage.read(pid)
        undo = p.get("beat_undo")
        if data.revision != p["revision"] or not undo or undo["after"] != p["plan"]:
            raise HTTPException(409, "El montaje cambió o no hay un ajuste de beats que deshacer")
        p["plan"] = undo["before"]
        p.pop("beat_undo")
        p["revision"] += 1
        storage.write(p)
    return p


class ChatMessage(StrictModel):
    message: str = Field(min_length=1, max_length=10000)


@app.post("/api/projects/{pid}/chat")
def chat(pid: str, data: ChatMessage):
    snapshot = storage.read(pid)
    if not providers.available()["deepseek"]:
        raise ValueError("DeepSeek pendiente de configurar. Puedes escribir el briefing y editar cortes manualmente.")
    def work(progress):
        progress("El agente está revisando tu briefing y el montaje")
        answer = providers.chat(snapshot, data.message)
        with storage.LOCK:
            p = storage.read(pid)
            if p["revision"] != snapshot["revision"]:
                raise ValueError("El proyecto cambió durante la respuesta. Envía tu indicación de nuevo.")
            p["briefing"] = answer["briefing"]
            if answer.get("plan") is not None:
                p["plan"] = answer["plan"]
            p["messages"] += [{"role": "user", "content": data.message}, {"role": "assistant", "content": answer["reply"]}]
            p["revision"] += 1
            storage.write(p)
        return {"reply": answer["reply"]}
    return jobs.submit(pid, "chat", work)


class RenderRequest(StrictModel):
    mode: Literal["preview", "export"] = "preview"


@app.post("/api/projects/{pid}/render")
def render(pid: str, data: RenderRequest):
    p = copy.deepcopy(storage.read(pid))
    plan = validate_plan(Plan.model_validate(p["plan"]), p["assets"])
    if not plan.segments:
        raise ValueError("Añade cortes al montaje antes de previsualizar")
    def work(progress):
        group = uuid.uuid4().hex
        directory = storage.project_dir(pid) / "renders" / group
        outputs = []
        variants = [("podcast", plan, False, 0)] + [(f"clip-{n:02d}", slice_plan(plan, c.start, c.end), True, c.start) for n, c in enumerate(plan.clips, 1)]
        for label, variant, vertical, timeline_start in variants:
            progress(f"{'Previsualizando' if data.mode == 'preview' else 'Exportando'} {label}")
            cues = None
            language = p["settings"]["subtitles"]
            if language != "off":
                cues = media.timeline_cues(p, variant)
                if not cues:
                    raise ValueError("No hay transcripción para subtitular. Analiza los audios o selecciona sin subtítulos.")
                if language != "original":
                    cues = providers.translate(cues, language)
            target = directory / f"{label}.mp4"
            media.render(p, variant, target, vertical=vertical, preview=data.mode == "preview", cues=cues, timeline_start=timeline_start)
            outputs.append({"name": label, "url": f"/api/projects/{pid}/renders/{group}/{target.name}", "srt": f"/api/projects/{pid}/renders/{group}/{label}.srt" if cues else None})
        return {"outputs": outputs, "revision": p["revision"], "mode": data.mode}
    return jobs.submit(pid, data.mode, work)


@app.get("/api/projects/{pid}/jobs")
def project_jobs(pid: str):
    storage.read(pid)
    return jobs.list_jobs(pid)


@app.get("/api/projects/{pid}/jobs/{jid}")
def project_job(pid: str, jid: str):
    storage.read(pid)
    return jobs.get_job(pid, jid)


@app.get("/api/projects/{pid}/renders/{group}/{filename}")
def output(pid: str, group: str, filename: str):
    storage.read(pid)
    storage.identifier(group)
    if filename != "podcast.mp4" and filename != "podcast.srt" and not __import__("re").fullmatch(r"clip-\d{2}\.(mp4|srt)", filename):
        raise HTTPException(404, "Exportación no encontrada")
    path = storage.project_dir(pid) / "renders" / group / filename
    if not path.is_file():
        raise HTTPException(404, "Exportación no encontrada")
    return FileResponse(path)


@app.get("/api/projects/{pid}/download-plan")
def download_plan(pid: str):
    p = storage.read(pid)
    return JSONResponse({k: p[k] for k in ("name", "briefing", "settings", "plan")}, headers={"Content-Disposition": 'attachment; filename="agntia-plan.json"'})


app.mount("/", StaticFiles(directory=STATIC, html=True), name="studio")
