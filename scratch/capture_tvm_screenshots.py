# -*- coding: utf-8 -*-
import os, subprocess, json, time, urllib.request, asyncio, base64

async def capture_screenshots():
    import websockets
    edge_bin = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    html_path = os.path.abspath("Calculadora Financeira 17bIi.html")
    file_url = "file:" + urllib.request.pathname2url(html_path)
    port = 9228

    proc = subprocess.Popen([
        edge_bin,
        "--headless=new",
        f"--remote-debugging-port={port}",
        "--window-size=1600,1000",
        "--no-first-run",
        "--disable-gpu",
        file_url
    ])

    try:
        await asyncio.sleep(2)
        resp = urllib.request.urlopen(f"http://127.0.0.1:{port}/json")
        targets = json.loads(resp.read().decode())
        page_target = next((t for t in targets if t.get("type") == "page"), targets[0])
        ws_url = page_target["webSocketDebuggerUrl"]

        async with websockets.connect(ws_url) as ws:
            async def eval_js(expr):
                nonlocal ws
                msg_id = int(time.time() * 1000) % 1000000
                await ws.send(json.dumps({
                    "id": msg_id,
                    "method": "Runtime.evaluate",
                    "params": {"expression": expr, "returnByValue": True, "awaitPromise": True}
                }))
                while True:
                    rep = json.loads(await ws.recv())
                    if rep.get("id") == msg_id:
                        return rep.get("result", {}).get("result", {}).get("value")

            async def take_screenshot(filename, clip_selector=None):
                clip = None
                if clip_selector:
                    box = await eval_js(f"""
                        (() => {{
                            const el = document.querySelector('{clip_selector}');
                            if (!el) return null;
                            const r = el.getBoundingClientRect();
                            return {{ x: Math.round(r.x), y: Math.round(r.y), width: Math.round(r.width), height: Math.round(r.height), scale: 1 }};
                        }})()
                    """)
                    if box and box["width"] > 0 and box["height"] > 0:
                        clip = box

                msg_id = int(time.time() * 1000) % 1000000
                params = {"format": "png"}
                if clip:
                    params["clip"] = clip
                await ws.send(json.dumps({
                    "id": msg_id,
                    "method": "Page.captureScreenshot",
                    "params": params
                }))
                while True:
                    rep = json.loads(await ws.recv())
                    if rep.get("id") == msg_id:
                        data = rep["result"]["data"]
                        with open(filename, "wb") as f:
                            f.write(base64.b64decode(data))
                        print(f"Saved {filename}")
                        break

            # 1. Switch to TVM tab and make sure workstation view is active
            await eval_js("app.setMobileView('workstation'); app.switchTab('TVM');")
            # Populate TVM
            await eval_js("""
                (() => {
                    document.getElementById('input-tvm-N').value = '12';
                    app.syncInputToState('tvm', 'N', '12');
                    document.getElementById('input-tvm-I').value = '12';
                    app.syncInputToState('tvm', 'I', '12');
                    document.getElementById('input-tvm-PV').value = '1000';
                    app.syncInputToState('tvm', 'PV', '1000');
                    document.getElementById('input-tvm-FV').value = '0';
                    app.syncInputToState('tvm', 'FV', '0');
                    app.calculateTVM('PMT');
                    app.generateAmortizationTable();
                })()
            """)

            # Screenshot Dark Mode
            await take_screenshot("scratch/tvm_dark_mode.png", "#panel-TVM")

            # Switch to Light Mode
            await eval_js("document.body.classList.add('light-mode')")
            await asyncio.sleep(0.5)

            # Screenshot Light Mode
            await take_screenshot("scratch/tvm_light_mode.png", "#panel-TVM")

    finally:
        proc.kill()

if __name__ == '__main__':
    asyncio.run(capture_screenshots())

