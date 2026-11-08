import array
import copy
import json
import math
import os
import subprocess
import tempfile
import unittest
import wave
from pathlib import Path
from unittest.mock import patch

from agntia import audio, media, storage
from agntia.models import Plan, Segment, Settings, validate_settings


def write_wav(path, samples, rate=16000):
    with wave.open(str(path), "wb") as handle:
        handle.setparams((1, 2, rate, 0, "NONE", "not compressed"))
        handle.writeframes(array.array("h", samples).tobytes())


def pcm(path):
    result = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ss", "0.2", "-t", "0.5", "-vn", "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True, check=True, timeout=30)
    return array.array("h", result.stdout)


def strength(samples, frequency, rate=8000):
    real = sum(s*math.cos(2*math.pi*frequency*i/rate) for i, s in enumerate(samples))
    imaginary = sum(s*math.sin(2*math.pi*frequency*i/rate) for i, s in enumerate(samples))
    return math.hypot(real, imaginary)/len(samples)


class AudioTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.patch = patch.object(storage, "DATA", self.root / "data")
        self.patch.start()
        self.project = storage.create("Prueba de audio")
        self.folder = storage.project_dir(self.project["id"]) / "media"
        self.folder.mkdir()
        self.voice = self.folder / "voice.wav"
        self.song = self.folder / "song.mp3"
        write_wav(self.voice, [int(3000*math.sin(2*math.pi*440*i/16000)) for i in range(4*16000)])
        source = self.root / "song.wav"
        write_wav(source, [int(6000*math.sin(2*math.pi*(880 if i<16000 else 1320)*i/16000)) for i in range(4*16000)])
        media.run(["ffmpeg", "-v", "error", "-y", "-i", str(source), "-c:a", "libmp3lame", str(self.song)])
        self.project["assets"] = [self.asset("voice", self.voice), self.asset("song", self.song)]
        self.project["settings"] = Settings(music={"asset_id": "song", "volume": .3, "fade_seconds": 0, "ducking": False}).model_dump()
        self.plan = Plan(segments=[Segment(asset_id="voice", start=0, end=1)])

    def tearDown(self):
        self.patch.stop()
        self.temp.cleanup()

    def asset(self, aid, path):
        return {"id": aid, "name": path.name, "stored_name": path.name, "sha256": storage.fingerprint(path), "role": "music" if aid=="song" else "audio", **media.probe(path)}

    def render(self, name, plan=None, **kwargs):
        target = self.root / f"{name}.mp4"
        media.render(self.project, plan or self.plan, target, **kwargs)
        return target

    def test_mp3_mixing_volume_and_ducking_are_audible(self):
        self.project["settings"]["music"]["volume"] = .1
        quiet = strength(pcm(self.render("quiet")), 880)
        self.project["settings"]["music"]["volume"] = .6
        loud = strength(pcm(self.render("loud")), 880)
        self.project["settings"]["music"]["ducking"] = True
        ducked = strength(pcm(self.render("ducked")), 880)
        self.assertGreater(loud, quiet*3)
        self.assertLess(ducked, loud*.7)

    def test_clip_music_uses_episode_offset(self):
        target = self.render("clip", timeline_start=1.2)
        samples = pcm(target)
        self.assertGreater(strength(samples, 1320), strength(samples, 880)*4)
        self.assertAlmostEqual(media.probe(target)["duration"], 1, delta=.1)

    def test_neural_voice_model_runs_locally_and_changes_audio(self):
        self.assertTrue(audio.capabilities()["voice_ai"])
        self.project["settings"]["music"]["asset_id"] = None
        original = pcm(self.render("original"))
        self.project["settings"]["voice_enhancement"] = "ai"
        target = self.render("enhanced")
        enhanced = pcm(target)
        self.assertNotEqual(original.tobytes(), enhanced.tobytes())
        self.assertAlmostEqual(media.probe(target)["duration"], 1, delta=.15)
        self.assertTrue(media.probe(target)["has_audio"])

    def test_classic_voice_and_short_nonloop_music_keep_full_duration(self):
        self.project["settings"]["voice_enhancement"] = "studio"
        self.project["settings"]["music"].update(loop=False, start=3.7, fade_seconds=.1)
        target = self.render("short-song")
        self.assertAlmostEqual(media.probe(target)["duration"], 1, delta=.15)
        # If a clip starts after the non-looping song ends, dialogue continues.
        target = self.render("after-song", timeline_start=8)
        self.assertAlmostEqual(media.probe(target)["duration"], 1, delta=.15)

    def test_looping_music_keeps_clip_phase_and_duration(self):
        self.project["settings"]["music"].update(loop=True, start=.2)
        target = self.render("loop", timeline_start=8)
        # Duration metadata includes MP3 padding; the expected first-tone region is still 880 Hz.
        samples = pcm(target)
        self.assertGreater(strength(samples, 880), strength(samples, 1320)*3)
        self.assertAlmostEqual(media.probe(target)["duration"], 1, delta=.15)

    def test_detect_percussive_120_bpm_and_cache(self):
        kick = self.folder / "kick.wav"
        samples = []
        for i in range(6*16000):
            t = i/16000
            phase = (t-.2) % .5
            sample = 18000*math.sin(2*math.pi*120*phase)*math.exp(-phase*55) if t>=.2 and phase<.12 else 0
            samples.append(int(sample))
        write_wav(kick, samples)
        asset = self.asset("kick", kick)
        beats = audio.detect_beats(self.project, asset)
        self.assertGreaterEqual(len(beats["times"]), 10)
        self.assertAlmostEqual(beats["bpm"], 120, delta=3)
        self.assertAlmostEqual(beats["times"][0], .2, delta=.04)
        with patch.object(media, "run", side_effect=AssertionError("cached")):
            self.assertEqual(audio.detect_beats(self.project, asset), beats)

    def test_no_beats_in_silence(self):
        silence = self.folder / "silence.wav"
        write_wav(silence, [0]*16000)
        result = audio.detect_beats(self.project, self.asset("silent", silence))
        self.assertEqual(result["times"], [])
        self.assertIsNone(result["bpm"])

    def test_snap_preserves_duration_and_separate_audio_start(self):
        p = copy.deepcopy(self.project)
        p["assets"][1]["beats"] = {"times": [.5, 1, 1.5, 2, 2.5, 3]}
        p["plan"] = Plan(segments=[Segment(asset_id="voice", start=0, end=1.1, audio_id="song", audio_start=.4), Segment(asset_id="voice", start=0, end=1.9)]).model_dump()
        plan, changed = audio.snap_to_beats(p, .2, .5)
        self.assertEqual(changed, 1)
        self.assertAlmostEqual(plan.segments[0].end, 1)
        self.assertAlmostEqual(sum(s.end-s.start for s in plan.segments), 3)
        self.assertEqual(plan.segments[0].audio_start, .4)
        self.assertEqual(plan.segments[1].start, 0)

    def test_snap_skips_beat_beyond_source_and_applies_song_offset(self):
        p = copy.deepcopy(self.project)
        p["settings"]["music"]["start"] = .2
        p["assets"][1]["beats"] = {"times": [1.2, 1.7, 2.2, 2.7]}
        p["assets"][0]["duration"] = 1.1
        p["plan"] = Plan(segments=[Segment(asset_id="voice", start=0, end=1.1), Segment(asset_id="voice", start=0, end=1)]).model_dump()
        # Moving to 1s would make the next segment 1.1s, still valid.
        plan, changed = audio.snap_to_beats(p, .2, .5)
        self.assertEqual(changed, 1)
        self.assertAlmostEqual(plan.segments[0].end, 1)
        p["assets"][0]["duration"] = 1.09
        p["assets"].append({"id": "tight", "name": "tight.wav", "duration": 1, "has_audio": True})
        p["plan"]["segments"][1]["asset_id"] = "tight"
        p["plan"]["segments"][0]["end"] = 1.08
        plan, changed = audio.snap_to_beats(p, .2, .5)
        self.assertEqual(changed, 0)

    def test_music_settings_reject_video_without_audio_and_invalid_start(self):
        with self.assertRaises(ValueError):
            validate_settings(Settings(music={"asset_id": "unknown"}), self.project["assets"])
        with self.assertRaises(ValueError):
            validate_settings(Settings(music={"asset_id": "song", "start": 100}), self.project["assets"])
        with self.assertRaises(ValueError):
            Settings(music={"volume": 1.1})


if __name__ == "__main__":
    unittest.main()
