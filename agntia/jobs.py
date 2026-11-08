import copy
import json
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor

from . import storage

EXECUTOR = ThreadPoolExecutor(max_workers=1, thread_name_prefix="agntia")
JOBS = {}
LOCK = threading.RLock()


def update(job, **values):
    with LOCK:
        job.update(values)
        path = storage.project_dir(job["project_id"]) / "jobs"
        path.mkdir(parents=True, exist_ok=True)
        target = path / f"{job['id']}.json"
        temp = target.with_suffix(".tmp")
        temp.write_text(json.dumps(job, ensure_ascii=False), encoding="utf-8")
        temp.replace(target)


def submit(pid: str, kind: str, function):
    with LOCK:
        active = [j for j in JOBS.values() if j["status"] in ("queued", "running")]
        if len(active) >= 20:
            raise ValueError("Hay demasiados trabajos pendientes; espera a que terminen")
        job = {"id": uuid.uuid4().hex, "project_id": pid, "kind": kind, "status": "queued", "message": "En cola", "outputs": []}
        JOBS[job["id"]] = job
        update(job)

    def work():
        update(job, status="running", message="Preparando")
        try:
            result = function(lambda message: update(job, message=message))
            update(job, status="done", message="Terminado", **(result or {}))
        except Exception as exc:
            # Provider errors have already been sanitized; don't expose traceback or env.
            update(job, status="error", message=str(exc)[:2000])
    EXECUTOR.submit(work)
    return copy.deepcopy(job)


def list_jobs(pid: str):
    with LOCK:
        directory = storage.project_dir(pid) / "jobs"
        values = []
        for path in sorted(directory.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)[:50]:
            job = json.loads(path.read_text(encoding="utf-8"))
            if job["id"] not in JOBS and job["status"] in ("queued", "running"):
                job.update(status="error", message="Interrumpido al reiniciar. Puedes volver a lanzarlo.")
            values.append(job)
        return values
