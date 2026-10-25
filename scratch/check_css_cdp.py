import os, subprocess, json, time, urllib.request, asyncio, sys
sys.stdout.reconfigure(encoding='utf-8')

async def check():
    import websockets
    edge_bin = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    html_path = os.path.abspath("Calculadora Financeira 17bIi.html")
    file_url = "file:" + urllib.request.pathname2url(html_path)
    port = 9330

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
            # Don't change theme yet, see what matches
            res = await send_cmd("CSS.enable")
            # Get node id
            node_resp = await send_cmd("DOM.getDocument")
            root_id = node_resp['result']['root']['nodeId']
            del_resp = await send_cmd("DOM.querySelector", {"nodeId": root_id, "selector": ".custom-formula-delete-btn"})
            del_node_id = del_resp['result']['nodeId']
            
            matched_styles = await send_cmd("CSS.getMatchedStylesForNode", {"nodeId": del_node_id})
            # Print matched rules for color
            for r in matched_styles.get('result', {}).get('matchedCSSRules', []):
                rule = r.get('rule', {})
                selector = rule.get('selectorList', {}).get('text')
                css_props = [f"{p['name']}: {p['value']}" for p in rule.get('style', {}).get('cssProperties', []) if p['name'] == 'color']
                if css_props:
                    print(f"Selector: {selector} => {css_props}")
    finally:
        proc.terminate()

asyncio.run(check())

