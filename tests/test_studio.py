"""Integration checks use generated media; providers use controlled responses."""
import array
import json
import os
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from agntia import jobs, media, providers, storage
from agntia.app import app
from agntia.models import Caption, Plan, Segment, slice_plan, validate_plan


class StudioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture_dir = tempfile.TemporaryDirectory()
        root = Path(cls.fixture_dir.name)
        cls.video = root / "camera.mp4"
        cls.audio = root / "voice.wav"
        media.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=red:s=160x90:r=25:d=4", "-f", "lavfi", "-i", "sine=frequency=440:duration=4", "-c:v", "libx264", "-threads", "1", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(cls.video)])
        media.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "sine=frequency=880:duration=6", str(cls.audio)])

    @classmethod
    def tearDownClass(cls):
        cls.fixture_dir.cleanup()

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        root = Path(self.directory.name)
        self.patches = [patch.object(storage, "DATA", root / "data"), patch.object(storage, "INBOX", root / "inbox"),
                        patch.object(providers, "DATA", root / "data"),
                        patch.dict(os.environ, {"AGNTIA_ACCESS_TOKEN": "", "DEEPSEEK_API_KEY": "", "GEMINI_API_KEY": ""})]
        for item in self.patches:
            item.start()
        self.client = TestClient(app)
        self.project = self.client.post("/api/projects", json={"name": "Podcast de prueba"}).json()
        self.pid = self.project["id"]
        self.base = f"/api/projects/{self.pid}"

    def tearDown(self):
        # A failed assertion must not leave background writes racing temp cleanup.
        deadline = time.monotonic() + 60
        while any(j["project_id"] == self.pid and j["status"] in ("queued", "running") for j in jobs.JOBS.values()) and time.monotonic() < deadline:
            time.sleep(.05)
        self.client.close()
        for item in reversed(self.patches):
            item.stop()
        self.directory.cleanup()

    def upload(self, path, name=None):
        with path.open("rb") as handle:
            response = self.client.post(self.base + "/upload", files={"file": (name or path.name, handle)})
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()

    def wait(self, jid):
        deadline = time.monotonic() + 60
        while time.monotonic() < deadline:
            job = next(j for j in self.client.get(self.base + "/jobs").json() if j["id"] == jid)
            if job["status"] in ("done", "error"):
                self.assertEqual(job["status"], "done", job["message"])
                return job
            time.sleep(.1)
        self.fail("Background job did not finish")

    def save(self, plan):
        p = self.client.get(self.base).json()
        return self.client.put(self.base, json={"revision": p["revision"], "settings": p["settings"], "briefing": "Conversación natural", "plan": plan})

    def test_upload_probe_deduplicate_and_path_safety(self):
        asset = self.upload(self.video, "../../camera.mp4")
        self.assertEqual(asset["name"], "camera.mp4")
        self.assertTrue(asset["has_video"] and asset["has_audio"])
        self.assertAlmostEqual(asset["duration"], 4, delta=.1)
        self.assertEqual(self.upload(self.video)["id"], asset["id"])
        self.assertEqual(len(self.client.get(self.base).json()["assets"]), 1)
        response = self.client.get(self.base + f"/assets/{asset['id']}/media", headers={"Range": "bytes=0-99"})
        self.assertEqual(response.status_code, 206)
        self.assertEqual(len(response.content), 100)

    def test_invalid_upload_cleans_partial_file(self):
        response = self.client.post(self.base + "/upload", files={"file": ("bad.mp4", b"not a video")})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(list((storage.project_dir(self.pid) / "media").iterdir()), [])

    def test_plan_rejects_unknown_asset_and_out_of_range_audio(self):
        video, audio = self.upload(self.video), self.upload(self.audio)
        invalid = [
            {"asset_id": "unknown", "start": 0, "end": 1},
            {"asset_id": video["id"], "start": 0, "end": 5},
            {"asset_id": video["id"], "start": 0, "end": 3, "audio_id": audio["id"], "audio_start": 5},
            {"asset_id": video["id"], "start": 2, "end": 1},
        ]
        for segment in invalid:
            with self.subTest(segment=segment):
                self.assertIn(self.save({"segments": [segment], "clips": []}).status_code, (400, 422))
        result = self.save({"segments": [{"asset_id": video["id"], "start": 0, "end": 2}], "clips": [{"title": "Fuera", "start": 1, "end": 3}]})
        self.assertEqual(result.status_code, 400)

    def test_revision_conflict_preserves_saved_plan(self):
        p = self.client.get(self.base).json()
        body = {"revision": p["revision"], "settings": p["settings"], "briefing": "Uno", "plan": p["plan"]}
        self.assertEqual(self.client.put(self.base, json=body).status_code, 200)
        body["briefing"] = "No sobrescribir"
        self.assertEqual(self.client.put(self.base, json=body).status_code, 409)
        self.assertEqual(self.client.get(self.base).json()["briefing"], "Uno")

    def test_partial_agent_settings_preserve_music_and_reject_stale_revision(self):
        p = storage.read(self.pid)
        response = self.client.patch(self.base, json={"revision": p["revision"], "settings": {"music": {"volume": .25}, "voice_enhancement": "studio"}})
        self.assertEqual(response.status_code, 200, response.text)
        updated = response.json()
        self.assertEqual(updated["settings"]["music"]["volume"], .25)
        self.assertTrue(updated["settings"]["music"]["ducking"])
        self.assertEqual(updated["settings"]["voice_enhancement"], "studio")
        self.assertEqual(self.client.patch(self.base, json={"revision": p["revision"], "briefing": "stale"}).status_code, 409)
        self.assertEqual(self.client.patch(self.base, json={"revision": updated["revision"], "settings": {"music": {"volume": 2}}}).status_code, 400)
        self.assertEqual(storage.read(self.pid)["revision"], updated["revision"])

    def test_agent_openapi_and_job_lookup_are_authenticated(self):
        schema = self.client.get("/api/openapi.json")
        self.assertEqual(schema.status_code, 200)
        self.assertIn("patch", schema.json()["paths"]["/api/projects/{pid}"])
        job = jobs.submit(self.pid, "test", lambda _: {"outputs": []})
        self.wait(job["id"])
        self.assertEqual(self.client.get(self.base+f"/jobs/{job['id']}").json()["status"], "done")
        other = storage.create("Other")
        self.assertEqual(self.client.get(f"/api/projects/{other['id']}/jobs/{job['id']}").status_code, 404)
        with patch.dict(os.environ, {"AGNTIA_ACCESS_TOKEN": "test-token"}):
            self.assertEqual(self.client.get("/api/openapi.json").status_code, 401)
            self.assertEqual(self.client.get(self.base+f"/jobs/{job['id']}").status_code, 401)

    def test_audio_settings_saved_and_beat_adjustment_undo(self):
        video, song = self.upload(self.video), self.upload(self.audio)
        p = storage.read(self.pid)
        p["assets"][1]["beats"] = {"times": [.5, 1, 1.5, 2, 2.5]}
        p["settings"]["music"].update(asset_id=song["id"], volume=.2, ducking=True)
        storage.write(p)
        self.assertEqual(self.save({"segments": [{"asset_id": video["id"], "start": 0, "end": 1.1}, {"asset_id": video["id"], "start": 0, "end": 1.9}], "clips": []}).status_code, 200)
        p = storage.read(self.pid)
        response = self.client.post(self.base+"/snap-beats", json={"revision": p["revision"], "tolerance": .2})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["changed"], 1)
        after = response.json()["project"]
        self.assertAlmostEqual(after["plan"]["segments"][0]["end"], 1)
        undone = self.client.post(self.base+"/undo-beats", json={"revision": after["revision"]})
        self.assertEqual(undone.status_code, 200)
        self.assertAlmostEqual(undone.json()["plan"]["segments"][0]["end"], 1.1)
        self.assertEqual(undone.json()["settings"]["music"]["asset_id"], song["id"])

    def test_clip_crossing_cuts_preserves_audio_offsets(self):
        plan = Plan(segments=[Segment(asset_id="video1", start=10, end=15, audio_id="voice", audio_start=20), Segment(asset_id="video2", start=30, end=35)])
        clipped = slice_plan(plan, 3, 8)
        self.assertEqual([(s.start, s.end) for s in clipped.segments], [(13, 15), (30, 33)])
        self.assertEqual(clipped.segments[0].audio_start, 23)

    def test_caption_mapping_uses_separate_audio(self):
        p = {"assets": [{"id": "visual", "analysis": {"transcript": [{"start": 0, "end": 2, "text": "Incorrecto"}]}},
                         {"id": "voice", "analysis": {"transcript": [{"start": 10, "end": 12, "text": "Bonjour"}]}}]}
        plan = Plan(segments=[Segment(asset_id="visual", start=1, end=3, audio_id="voice", audio_start=10)])
        cues = media.timeline_cues(p, plan)
        self.assertEqual(cues, [{"start": 0, "end": 2, "text": "Bonjour"}])
        self.assertIn("00:00:00,000 --> 00:00:02,000", media.srt(cues))

    def test_manual_caption_overrides_and_clip_rebasing(self):
        p = {"assets": [{"id": "voice", "duration": 10, "has_audio": True, "name": "voice", "analysis": {"transcript": [{"start": 0, "end": 10, "text": "Original"}]}}]}
        plan = Plan(segments=[Segment(asset_id="voice", start=0, end=10)], captions=[Caption(start=2, end=5, text="Texto corregido")])
        self.assertEqual(media.timeline_cues(p, plan), [{"start": 2, "end": 5, "text": "Texto corregido"}])
        clipped = slice_plan(plan, 3, 7)
        self.assertEqual(media.timeline_cues(p, clipped), [{"start": 0, "end": 2, "text": "Texto corregido"}])
        self.assertEqual(media.timeline_cues(p, Plan(segments=plan.segments, captions=[])), [])
        with self.assertRaises(ValueError):
            validate_plan(Plan(segments=plan.segments, captions=[Caption(start=9, end=12, text="Fuera")]), p["assets"])

    def test_manual_caption_can_be_saved_and_rendered_without_provider_keys(self):
        audio = self.upload(self.audio)
        p = storage.read(self.pid)
        p["settings"]["subtitles"] = "original"
        storage.write(p)
        plan = {"segments": [{"asset_id": audio["id"], "start": 0, "end": 1}], "clips": [], "captions": [{"start": .1, "end": .9, "text": "Bonjour, texto corregido"}]}
        saved = self.save(plan)
        self.assertEqual(saved.status_code, 200, saved.text)
        self.assertEqual(saved.json()["plan"]["captions"][0]["text"], "Bonjour, texto corregido")
        response = self.client.post(self.base+"/render", json={"mode": "preview"})
        job = self.wait(response.json()["id"])
        self.assertIn("Bonjour, texto corregido", self.client.get(job["outputs"][0]["srt"]).text)
        # Explicitly removing all captions must not reintroduce the transcript or break export.
        plan["captions"] = []
        self.assertEqual(self.save(plan).status_code, 200)
        response = self.client.post(self.base+"/render", json={"mode": "preview"})
        self.assertIsNone(self.wait(response.json()["id"])["outputs"][0]["srt"])

    def test_real_video_and_audio_thumbnails_are_cached_and_protected(self):
        for path in (self.video, self.audio):
            a = self.upload(path)
            url = self.base+f"/assets/{a['id']}/thumbnail"
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, response.text[:100] if response.status_code!=200 else "")
            self.assertEqual(response.content[:8], b"\x89PNG\r\n\x1a\n")
            with patch.object(media, "run", side_effect=AssertionError("thumbnail should be cached")):
                self.assertEqual(self.client.get(url).status_code, 200)
            with patch.dict(os.environ, {"AGNTIA_ACCESS_TOKEN": "secret"}):
                self.assertEqual(self.client.get(url).status_code, 401)

    def test_render_video_with_external_audio_and_vertical_clip(self):
        video, audio = self.upload(self.video), self.upload(self.audio)
        plan = {"segments": [{"asset_id": video["id"], "start": 0, "end": 1.2, "audio_id": audio["id"], "audio_start": 2}], "clips": [{"title": "Momento", "start": .2, "end": .8}]}
        self.assertEqual(self.save(plan).status_code, 200)
        response = self.client.post(self.base + "/render", json={"mode": "preview"})
        self.assertEqual(response.status_code, 200, response.text)
        job = self.wait(response.json()["id"])
        self.assertEqual(len(job["outputs"]), 2)
        url = job["outputs"][0]["url"]
        path = storage.project_dir(self.pid) / "renders" / url.split("/")[-2] / "podcast.mp4"
        info = media.probe(path)
        self.assertAlmostEqual(info["duration"], 1.2, delta=.15)
        # Verify audio is the 880 Hz external track rather than the camera's 440 Hz.
        import subprocess
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ss", "0.1", "-t", "0.5", "-vn", "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], check=True, capture_output=True).stdout
        samples = array.array("h", raw)
        crossings = sum(a < 0 <= b for a, b in zip(samples, samples[1:]))
        self.assertAlmostEqual(crossings / (len(samples) / 8000), 880, delta=25)
        clip = path.with_name("clip-01.mp4")
        streams = json.loads(media.run(["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(clip)]).stdout)["streams"]
        visual = next(s for s in streams if s["codec_type"] == "video")
        self.assertEqual((visual["width"], visual["height"]), (270, 480))
        self.assertAlmostEqual(media.probe(clip)["duration"], .6, delta=.15)
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_audio_only_render_and_burned_subtitles(self):
        asset = self.upload(self.audio)
        p = storage.read(self.pid)
        p["assets"][0]["analysis"] = {"transcript": [{"start": 0, "end": 1, "text": "Hola, bonjour, hello"}]}
        storage.write(p)
        plan = Plan(segments=[Segment(asset_id=asset["id"], start=0, end=1)])
        target = storage.project_dir(self.pid) / "test-render.mp4"
        cues = media.timeline_cues(p, plan)
        media.render(p, plan, target, cues=cues)
        self.assertTrue(media.probe(target)["has_video"])
        self.assertIn("Hola, bonjour, hello", target.with_suffix(".srt").read_text())

    def test_missing_keys_are_explicit_and_no_calls(self):
        with patch.object(providers, "request_json") as request:
            self.assertEqual(self.client.post(self.base + "/chat", json={"message": "Edita"}).status_code, 400)
            self.assertEqual(self.client.post(self.base + "/analyze").status_code, 400)
            request.assert_not_called()

    def test_chat_contract_validates_model_plan_before_writing(self):
        asset = self.upload(self.video)
        p = storage.read(self.pid)
        reply = {"reply": "Propuesta", "briefing": "Natural", "plan": {"segments": [{"asset_id": asset["id"], "start": 0, "end": 1}], "clips": []}}
        with patch.object(providers, "deepseek", return_value=reply):
            self.assertEqual(providers.chat(p, "Edita")["plan"]["segments"][0]["end"], 1)
        reply["plan"]["segments"][0]["end"] = 100
        with patch.object(providers, "deepseek", return_value=reply):
            with self.assertRaises(ValueError):
                providers.chat(p, "Edita")
        self.assertEqual(storage.read(self.pid)["plan"]["segments"], [])

    def test_gemini_contract_and_content_cache(self):
        asset = self.upload(self.video)
        response = {"candidates": [{"content": {"parts": [{"text": json.dumps({"summary": "Conversación", "transcript": [{"start": 0, "end": 1, "text": "Hello"}], "highlights": []})}]}}]}
        with patch.dict(os.environ, {"GEMINI_API_KEY": "fake-test-key"}), patch.object(providers, "request_json", return_value=response) as request:
            first = providers.analyze(storage.read(self.pid), asset, lambda _: None)
            second = providers.analyze(storage.read(self.pid), asset, lambda _: None)
            self.assertEqual(first, second)
            self.assertEqual(first["transcript"][0]["text"], "Hello")
            self.assertEqual(request.call_count, 1)
            self.assertEqual(request.call_args.args[2]["contents"][0]["parts"][1]["inline_data"]["mime_type"], "video/mp4")

    def test_translation_preserves_timing_and_reuses_cache(self):
        cues = [{"start": 2, "end": 4, "text": "Hello"}]
        with patch.object(providers, "deepseek", return_value={"texts": ["Bonjour"]}) as model:
            first = providers.translate(cues, "fr")
            second = providers.translate(cues, "fr")
            self.assertEqual(first, [{"start": 2, "end": 4, "text": "Bonjour"}])
            self.assertEqual(first, second)
            self.assertEqual(model.call_count, 1)

    def test_import_folder_and_skip_symlinks(self):
        storage.INBOX.mkdir()
        import shutil
        shutil.copyfile(self.video, storage.INBOX / "camera.mp4")
        (storage.INBOX / "ignored.txt").write_text("ignore")
        try:
            (storage.INBOX / "link.mp4").symlink_to(self.video)
        except OSError:
            pass
        job = self.client.post(self.base + "/import-inbox").json()
        self.assertEqual(self.wait(job["id"])["imported"], 1)
        self.assertEqual(len(storage.read(self.pid)["assets"]), 1)

    def test_auth_protects_media_and_rejects_cross_origin(self):
        asset = self.upload(self.video)
        with patch.dict(os.environ, {"AGNTIA_ACCESS_TOKEN": "a-long-test-token"}):
            self.assertEqual(self.client.get(self.base).status_code, 401)
            self.assertEqual(self.client.get(self.base + f"/assets/{asset['id']}/media").status_code, 401)
            self.assertEqual(self.client.post("/api/login", json={"token": "wrong"}).status_code, 401)
            self.assertEqual(self.client.post("/api/login", json={"token": "a-long-test-token"}).status_code, 200)
            self.assertEqual(self.client.get(self.base).status_code, 200)
            self.assertEqual(self.client.post("/api/projects", headers={"Origin": "https://elsewhere.example"}, json={"name": "Evil"}).status_code, 403)

    def test_remote_access_requires_token(self):
        with TestClient(app, client=("192.0.2.1", 1234)) as remote:
            self.assertEqual(remote.get("/api/status").status_code, 403)

    def test_unknown_project_id_cannot_escape_data_root(self):
        self.assertEqual(self.client.get("/api/projects/not-an-id").status_code, 400)
        self.assertEqual(self.client.get("/api/projects/" + "a" * 32).status_code, 404)


if __name__ == "__main__":
    unittest.main()
