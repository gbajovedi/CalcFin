import os, subprocess, json, time, urllib.request, asyncio, sys
sys.stdout.reconfigure(encoding='utf-8')

async def check():
    import websockets
    edge_bin = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    html_path = os.path.abspath("Calculadora Financeira 17bIi.html")
    file_url = "file:" + urllib.request.pathname2url(html_path)
    port = 9335

    proc = subprocess.Popen([
        edge_bin,
        "--headless=new",
        f"--remote-debugging-port={port}",
        "--window-size=1440,900",
        "--disable-gpu",
        file_url
    ])

    time.sleep(2)
    try:
        resp = urllib.request.urlopen(f"http://127.0.0.1:{port}/json", timeout=2)
        targets = json.loads(resp.read().decode())
        ws_url = [t['webSocketDebuggerUrl'] for t in targets if t.get('type') == 'page'][0]

        async with websockets.connect(ws_url) as ws:
            msg_id = 0
            async def send_cmd(method, params=None):
                nonlocal msg_id
                msg_id += 1
                await ws.send(json.dumps({'id': msg_id, 'method': method, 'params': params or {}}))
                while True:
                    r = json.loads(await ws.recv())
                    if r.get('id') == msg_id:
                        return r

            async def eval_js(expr):
                r = await send_cmd('Runtime.evaluate', {'expression': expr, 'returnByValue': True})
                return r.get('result', {}).get('result', {}).get('value')

            await eval_js("app.createCustomFormula('TESTE = A + B')")
            node_resp = await send_cmd("DOM.getDocument")
            root_id = node_resp['result']['root']['nodeId']
            del_resp = await send_cmd("DOM.querySelector", {"nodeId": root_id, "selector": ".custom-formula-delete-btn"})
            del_node_id = del_resp['result']['nodeId']

            comp = await send_cmd("CSS.getComputedStyleForNode", {"nodeId": del_node_id})
            for p in comp.get('result', {}).get('computedStyle', []):
                if p['name'] in ['color', 'display', 'visibility']:
                    print(f"{p['name']}: {p['value']}")
    finally:
        proc.terminate()

asyncio.run(check())

