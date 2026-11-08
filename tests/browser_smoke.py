"""Real browser + HTTP upload/playback test with temporary project data.

Run: python tests/browser_smoke.py
Optional: AGNTIA_BROWSER_EXECUTABLE=/usr/bin/chromium
Starts and stops its own local server; never calls paid APIs.
"""
import array
import math
import os
import socket
import subprocess
import sys
import tempfile
import time
import wave
from pathlib import Path

import httpx
from playwright.sync_api import sync_playwright


def wait_for(page, expression, timeout=30000):
    # CDP evaluation works with the production CSP; wait_for_function uses eval
    # inside the page, which correctly rejects unsafe-eval under that policy.
    deadline = time.monotonic() + timeout/1000
    while time.monotonic() < deadline:
        if page.evaluate("() => (" + expression + ")"):
            return
        page.wait_for_timeout(100)
    raise AssertionError("Browser condition did not become true: " + expression)


def exercise(page, wav):
    page.get_by_role("button", name="Crear mi primer proyecto").click()
    page.locator("#new-name").fill("Conversaciones sobre el futuro")
    page.locator("#new-form button.primary").click()
    page.locator("#workspace").wait_for(state="visible")
    page.locator("#upload").set_input_files(str(wav))
    page.locator(".asset").wait_for(state="visible")
    page.locator("#add-segment").click()
    assert page.locator("#timeline-svg .cut-block").count() == 1
    # Editing is direct, without requiring a model key or a chat.
    page.locator("#duplicate-button").click()
    assert page.locator("#timeline-svg .cut-block").count() == 2
    page.locator("#undo-button").click()
    assert page.locator("#timeline-svg .cut-block").count() == 1
    page.locator("#redo-button").click()
    assert page.locator("#timeline-svg .cut-block").count() == 2
    page.locator("#segments input[type=number]").nth(1).fill("3.5")
    page.locator("#segments input[type=number]").nth(1).press("Tab")
    page.locator("#save-button").click()
    wait_for(page, "document.querySelector('#save-state').textContent === 'Guardado'")
    # Edits after save must mutate the current plan, not stale input closures.
    page.locator("#segments input[type=number]").nth(1).fill("3")
    page.locator("#segments input[type=number]").nth(1).press("Tab")
    page.locator("#save-button").click()
    wait_for(page, "document.querySelector('#save-state').textContent === 'Guardado'")
    # Drag the right edge of the selected block inward, then undo it.
    handle = page.locator("#timeline-svg .selected [data-edge=end]")
    bounds = handle.bounding_box()
    page.mouse.move(bounds["x"]+3, bounds["y"]+15)
    page.mouse.down()
    page.mouse.move(bounds["x"]-25, bounds["y"]+15, steps=8)
    page.mouse.up()
    assert float(page.locator("#segments input[type=number]").nth(1).input_value()) < 3
    page.locator("#undo-button").click()
    assert float(page.locator("#segments input[type=number]").nth(1).input_value()) == 3
    page.locator("#split-button").click()
    assert page.locator("#timeline-svg .cut-block").count() == 3
    page.locator("#undo-button").click()
    assert page.locator("#timeline-svg .cut-block").count() == 2
    page.locator("#tab-sound").click()
    page.locator("#voice-mode").select_option("ai")
    page.locator("#music-asset").select_option(index=1)
    page.locator("#music-volume").evaluate("el => { el.value = '20'; el.dispatchEvent(new Event('input', {bubbles:true})); }")
    page.locator("#save-button").click()
    wait_for(page, "document.querySelector('#save-state').textContent === 'Guardado'")
    page.locator("#detect-beats").click()
    wait_for(page, "document.querySelector('#beat-info').textContent.includes('golpes detectados')", timeout=30000)
    page.locator("#tab-subtitles").click()
    page.locator("#add-caption").click()
    page.locator("#caption-list textarea").fill("Una conversación que merece quedarse.")
    page.locator("#save-button").click()
    wait_for(page, "document.querySelector('#save-state').textContent === 'Guardado'")
    page.locator("#tab-clips").click()
    page.locator("#add-clip").click()
    page.locator("#save-button").click()
    wait_for(page, "document.querySelector('#save-state').textContent === 'Guardado'")
    page.locator("#preview-button").click()
    wait_for(page, "document.querySelector('#preview-description').textContent === 'Podcast · previsualización'", timeout=60000)
    wait_for(page, "document.querySelector('#player').readyState >= 1", timeout=15000)
    page.reload()
    page.locator("#workspace").wait_for(state="visible")
    page.locator("#tab-sound").click()
    assert page.locator("#voice-mode").input_value() == "ai"
    assert page.locator("#music-volume").input_value() == "20"
    assert page.locator("#music-asset").input_value()
    assert page.locator("#beat-markers svg").count() == 1
    page.locator("#tab-subtitles").click()
    assert page.locator("#caption-list textarea").input_value() == "Una conversación que merece quedarse."
    page.locator("#tab-clips").click()
    assert page.locator(".clip").count() == 1
    assert page.locator("#timeline-svg .cut-block").count() == 2
    page.locator("#tab-media").click()


def main():
    screenshots = Path(os.getenv("AGNTIA_SCREENSHOT_DIR", "/tmp/agntia-screenshots"))
    screenshots.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        wav = root / "episode.wav"
        with wave.open(str(wav), "wb") as handle:
            handle.setparams((1, 2, 16000, 0, "NONE", "not compressed"))
            samples = array.array("h", (int(14000*math.sin(2*math.pi*120*(i/16000%0.5))*math.exp(-(i/16000%0.5)*40)) for i in range(4*16000)))
            handle.writeframes(samples.tobytes())
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        url = f"http://127.0.0.1:{port}"
        env = {**os.environ, "AGNTIA_ACCESS_TOKEN": "", "DEEPSEEK_API_KEY": "", "GEMINI_API_KEY": "",
               "AGNTIA_DATA_DIR": str(root / "data"), "AGNTIA_INBOX_DIR": str(root / "inbox")}
        with (screenshots / "server.log").open("w") as log:
            server = subprocess.Popen([sys.executable, "-m", "uvicorn", "agntia.app:app", "--host", "127.0.0.1", "--port", str(port)], env=env, stdout=log, stderr=subprocess.STDOUT)
            try:
                with httpx.Client(trust_env=False) as client:
                    for _ in range(100):
                        try:
                            if client.get(url+"/api/status").status_code == 200:
                                break
                        except httpx.HTTPError:
                            pass
                        time.sleep(.1)
                    else:
                        raise RuntimeError("Local smoke-test server did not start")
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True, executable_path=os.getenv("AGNTIA_BROWSER_EXECUTABLE") or None)
                    page = browser.new_page(viewport={"width": 1440, "height": 1000})
                    errors = []
                    page.on("pageerror", lambda error: errors.append(str(error)))
                    try:
                        page.goto(url)
                        exercise(page, wav)
                        assert not errors, errors
                        page.screenshot(path=str(screenshots / "studio-desktop.png"), full_page=True)
                        page.set_viewport_size({"width": 390, "height": 844})
                        page.screenshot(path=str(screenshots / "studio-mobile.png"), full_page=True)
                        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), "Mobile layout overflows"
                        print("PASS: visual editor, split/trim/undo/redo, manual subtitles, audio/beats, real preview, persistence, desktop/mobile")
                    except Exception:
                        print("PAGE ERRORS:", errors)
                        print("TOAST:", page.locator("#toast").text_content())
                        page.screenshot(path=str(screenshots / "failure.png"), full_page=True)
                        raise
                    finally:
                        browser.close()
            finally:
                server.terminate()
                try:
                    server.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    server.kill()
                    server.wait(timeout=10)


if __name__ == "__main__":
    main()
