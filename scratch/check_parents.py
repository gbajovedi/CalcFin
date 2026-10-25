import os, subprocess, json, time, urllib.request, asyncio, sys
sys.stdout.reconfigure(encoding='utf-8')

async def check():
    import websockets
    edge_bin = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    html_path = os.path.abspath("Calculadora Financeira 17bIi.html")
    file_url = "file:" + urllib.request.pathname2url(html_path)
    port = 9281

    proc = subprocess.Popen([
        edge_bin,
        "--headless=new",
        f"--remote-debugging-port={port}",
        "--window-size=1280,850",
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

            parents_info = await eval_js("""(() => {
                let el = document.getElementById('solve-library-list');
                const chain = [];
                while (el) {
                    const cs = window.getComputedStyle(el);
                    chain.push({
                        tag: el.tagName,
                        id: el.id,
                        className: el.className,
                        display: cs.display,
                        visibility: cs.visibility,
                        offsetParent: el.offsetParent ? el.offsetParent.tagName + '#' + el.offsetParent.id : null,
                        rect: { width: el.getBoundingClientRect().width, height: el.getBoundingClientRect().height }
                    });
                    el = el.parentElement;
                }
                return chain;
            })()""")
            for p in parents_info:
                print(f"{p['tag']}#{p['id']} ({p['className'][:30]}...): display={p['display']}, w={p['rect']['width']}, h={p['rect']['height']}")
    finally:
        proc.terminate()

asyncio.run(check())

