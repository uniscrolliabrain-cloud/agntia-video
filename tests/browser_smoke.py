"""Exercise the real frontend/API through Playwright routing, without opening a port.

Run: python tests/browser_smoke.py
Optional: AGNTIA_BROWSER_EXECUTABLE=/usr/bin/chromium
All project/media files are temporary; no API keys or provider calls are used.
"""
import array
import math
import os
import tempfile
import wave
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient
from playwright.sync_api import sync_playwright

from agntia import storage
from agntia.app import app


def main():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        wav = root / "episode.wav"
        with wave.open(str(wav), "wb") as handle:
            handle.setparams((1, 2, 16000, 0, "NONE", "not compressed"))
            samples = array.array("h", (int(14000*math.sin(2*math.pi*120*(i/16000%0.5))*math.exp(-(i/16000%0.5)*40)) for i in range(4*16000)))
            handle.writeframes(samples.tobytes())
        errors = []
        env = {"AGNTIA_ACCESS_TOKEN": "", "DEEPSEEK_API_KEY": "", "GEMINI_API_KEY": ""}
        with patch.object(storage, "DATA", root / "data"), patch.object(storage, "INBOX", root / "inbox"), patch.dict(os.environ, env), TestClient(app) as client, sync_playwright() as p:
            browser = p.chromium.launch(headless=True, executable_path=os.getenv("AGNTIA_BROWSER_EXECUTABLE") or None)
            page = browser.new_page(viewport={"width": 1440, "height": 1000})
            page.on("pageerror", lambda error: errors.append(str(error)))

            def route_request(route):
                request = route.request
                response = client.request(request.method, request.url, headers=request.headers, content=request.post_data_buffer)
                headers = {k: v for k, v in response.headers.items() if k.lower() not in ("content-length", "content-encoding", "transfer-encoding")}
                route.fulfill(status=response.status_code, headers=headers, body=response.content)

            page.route("**/*", route_request)
            page.goto("http://testserver/")
            page.get_by_role("button", name="Crear mi primer proyecto").click()
            page.locator("#new-name").fill("Podcast · prueba de sonido")
            page.locator("#new-form button.primary").click()
            page.locator("#workspace").wait_for(state="visible")
            page.locator("#upload").set_input_files(str(wav))
            page.locator(".asset").wait_for(state="visible")
            page.locator("#add-segment").click()
            page.locator("#voice-mode").select_option("ai")
            page.locator("#music-asset").select_option(index=1)
            page.locator("#music-volume").evaluate("el => { el.value = '20'; el.dispatchEvent(new Event('input', {bubbles:true})); }")
            page.locator("#save-button").click()
            page.wait_for_function("document.querySelector('#save-state').textContent === 'Guardado'")
            page.locator("#detect-beats").click()
            page.wait_for_function("document.querySelector('#beat-info').textContent.includes('golpes detectados')", timeout=30000)
            page.locator("#add-segment").click()
            page.locator("#save-button").click()
            page.wait_for_function("document.querySelector('#save-state').textContent === 'Guardado'")
            page.locator("#preview-button").click()
            page.wait_for_function("!document.querySelector('#player').hidden", timeout=60000)
            page.wait_for_function("document.querySelector('#player').readyState >= 1", timeout=15000)
            page.locator("#add-clip").click()
            page.locator("#save-button").click()
            page.wait_for_function("document.querySelector('#save-state').textContent === 'Guardado'")
            # Audio controls must survive API persistence and page reload.
            page.reload()
            page.locator("#workspace").wait_for(state="visible")
            assert page.locator("#voice-mode").input_value() == "ai"
            assert page.locator("#music-volume").input_value() == "20"
            assert page.locator("#music-asset").input_value()
            assert page.locator("#beat-markers svg").count() == 1
            assert page.locator(".clip").count() == 1
            assert not errors, errors
            screenshots = Path(os.getenv("AGNTIA_SCREENSHOT_DIR", "/tmp/agntia-screenshots"))
            screenshots.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(screenshots / "studio-desktop.png"), full_page=True)
            page.set_viewport_size({"width": 390, "height": 844})
            page.screenshot(path=str(screenshots / "studio-mobile.png"), full_page=True)
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), "Mobile layout overflows"
            print("PASS: upload, AI voice, music settings, beats, preview playback, persistence, desktop/mobile")
            browser.close()


if __name__ == "__main__":
    main()
