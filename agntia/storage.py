import hashlib
import json
import os
import re
import threading
import uuid
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
DATA = Path(os.getenv("AGNTIA_DATA_DIR", "./data")).resolve()
INBOX = Path(os.getenv("AGNTIA_INBOX_DIR", "./inbox")).resolve()
LOCK = threading.RLock()


def identifier(value: str) -> str:
    if not re.fullmatch(r"[a-f0-9]{32}", value):
        raise ValueError("Identificador inválido")
    return value


def project_dir(pid: str) -> Path:
    return DATA / "projects" / identifier(pid)


def read(pid: str) -> dict:
    with LOCK:
        return json.loads((project_dir(pid) / "project.json").read_text(encoding="utf-8"))


def write(project: dict):
    with LOCK:
        path = project_dir(project["id"]) / "project.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        temp = path.with_suffix(".tmp")
        temp.write_text(json.dumps(project, ensure_ascii=False, indent=2), encoding="utf-8")
        temp.replace(path)


def create(name: str) -> dict:
    project = {"id": uuid.uuid4().hex, "name": name, "assets": [], "briefing": "", "messages": [],
               "settings": {"source_language": "auto", "subtitles": "off", "fit": "contain"},
               "plan": {"segments": [], "clips": []}, "revision": 0}
    write(project)
    return project


def fingerprint(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def asset_path(pid: str, asset: dict) -> Path:
    # Uploaded names are never interpreted as filesystem paths.
    return project_dir(pid) / "media" / asset["stored_name"]
