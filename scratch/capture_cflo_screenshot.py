# -*- coding: utf-8 -*-
import os, subprocess, json, time, urllib.request, asyncio, base64

async def capture_cflo_screenshots():
    import websockets
    edge_bin = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    html_path = os.path.abspath("Calculadora Financeira 17bIi.html")
    file_url = "file:" + urllib.request.pathname2url(html_path)
    port = 9230

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
                box = await eval_js(f"""
                    (() => {{
                        const el = document.querySelector('{clip_selector}');
                        if (!el) return null;
                        el.scrollIntoView();
                        const r = el.getBoundingClientRect();
                        return {{ x: Math.round(r.x), y: Math.round(r.y), width: Math.round(r.width), height: Math.round(r.height), scale: 1 }};
                    }})()
                """)
                msg_id = int(time.time() * 1000) % 1000000
                params = {"format": "png"}
                if box and box["width"] > 0 and box["height"] > 0:
                    params["clip"] = box
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

            # Switch to CFLO
            await eval_js("app.setMobileView('workstation'); app.switchTab('CFLO');")
            # Populate CFLO
            await eval_js("""
                (() => {
                    document.getElementById('input-cflo-rate').value = '10';
                    app.syncCfloRate('10');
                    app.cflo = [
                        { amount: -1000, count: 1 },
                        { amount: 300, count: 2 },
                        { amount: 400, count: 1 },
                        { amount: 500, count: 1 }
                    ];
                    app.renderCashFlows();
                    app.computeNPV();
                    app.computeIRR();
                    document.body.classList.add('light-mode');
                })()
            """)
            await asyncio.sleep(0.5)

            await take_screenshot("scratch/cflo_cards_light.png", "#panel-CFLO > div.grid")

    finally:
        proc.kill()

if __name__ == '__main__':
    asyncio.run(capture_cflo_screenshots())

