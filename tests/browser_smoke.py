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


def responsive_checks(browser, url, screenshots):
    for width, height in [(390, 844), (320, 740), (768, 1024), (1024, 768), (844, 390)]:
        context = browser.new_context(viewport={"width": width, "height": height}, is_mobile=True, has_touch=True, device_scale_factor=1)
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        try:
            page.goto(url)
            page.locator("#project-list-open").tap()
            wait_for(page, "document.querySelector('#mobile-project-select').options.length > 1")
            page.locator("#mobile-project-select").select_option(index=1)
            page.locator("#workspace").wait_for(state="visible")
            page.locator("#project-dialog").wait_for(state="hidden")
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), f"Layout overflows at {width}px"
            page.locator("#mobile-agent-toggle").tap()
            page.locator("#briefing-section").wait_for(state="visible")
            assert page.locator("#briefing-section").get_attribute("role") == "dialog"
            assert page.locator("#briefing-section").get_attribute("aria-modal") == "true"
            draft = f"Conserva los debates y prepara tres clips. Pantalla {width}."
            page.locator("#chat-input").fill(draft)
            assert page.locator("#chat-send").is_disabled(), "No paid API calls in tests"
            dock = page.locator("#briefing-section").bounding_box()
            send = page.locator("#chat-send").bounding_box()
            assert dock["width"] <= width + 1
            assert dock["height"] <= height + 1
            assert send["y"] >= 0 and send["y"] + send["height"] <= height + 1, "Composer clipped in compact viewport"
            assert page.evaluate("document.querySelector('.app-header').inert"), "Background should be inert while chatting"
            page.locator("#agent-close").focus()
            page.keyboard.press("Shift+Tab")
            assert page.evaluate("document.activeElement.id") == "chat-input", "Dialog focus should stay inside"
            page.keyboard.press("Tab")
            assert page.evaluate("document.activeElement.id") == "agent-close"
            page.keyboard.press("Escape")
            page.locator("#briefing-section").wait_for(state="hidden")
            assert not page.evaluate("document.querySelector('.app-header').inert")
            page.locator("#mobile-agent-toggle").tap()
            assert page.locator("#chat-input").input_value() == draft, "Closing the chat must preserve draft"
            if width == 390:
                page.screenshot(path=str(screenshots / "studio-mobile-chat.png"))
            page.locator("#chat-backdrop").tap(position={"x": 5, "y": 5})
            page.locator("#briefing-section").wait_for(state="hidden")
            if width == 390:
                # Real touch editing and saving, including a touch-accessible history.
                page.locator("#tab-cuts").tap()
                end_field = page.locator("#segments input[type=number]").nth(1)
                original = float(end_field.input_value())
                end_field.fill(str(original-.2))
                end_field.press("Tab")
                page.locator("#touch-undo").tap()
                assert float(page.locator("#segments input[type=number]").nth(1).input_value()) == original
                page.locator("#touch-redo").tap()
                assert abs(float(page.locator("#segments input[type=number]").nth(1).input_value())-(original-.2)) < .001
                page.locator("#mobile-save").tap()
                wait_for(page, "document.querySelector('#save-state').textContent === 'Guardado'")
                page.locator("#segments input[type=number]").nth(1).fill(str(original))
                page.locator("#segments input[type=number]").nth(1).press("Tab")
                page.locator("#mobile-save").tap()
                wait_for(page, "document.querySelector('#save-state').textContent === 'Guardado'")
                page.locator("#tab-media").tap()
                page.evaluate("window.scrollTo(0,0)")
                page.screenshot(path=str(screenshots / "studio-mobile.png"), full_page=True)
            if width == 768:
                page.screenshot(path=str(screenshots / "studio-tablet.png"), full_page=True)
            assert not errors, errors
            print(f"PASS: touch layout {width}x{height}, project switcher, chat drawer, draft, focus trap, reachable composer")
        except Exception:
            print("RESPONSIVE PAGE ERRORS:", errors)
            page.screenshot(path=str(screenshots / f"failure-{width}.png"), full_page=True)
            raise
        finally:
            context.close()


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
                        dock = page.locator("#briefing-section").bounding_box()
                        canvas = page.locator("#studio").bounding_box()
                        assert dock["x"] >= canvas["x"]+canvas["width"]-1, "Chat must occupy the right column"
                        page.locator("#chat-input").fill("Haz el montaje más ágil y conserva los debates.")
                        page.locator("#tab-sound").click()
                        assert page.locator("#briefing-section").is_visible(), "Chat must remain visible while editing"
                        page.locator("#tab-media").click()
                        page.screenshot(path=str(screenshots / "studio-desktop.png"), full_page=True)
                        responsive_checks(browser, url, screenshots)
                        print("PASS: persistent desktop chat, visual editing and real touch/responsive workflow")
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
