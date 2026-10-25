# -*- coding: utf-8 -*-
import os, subprocess, json, time, urllib.request, asyncio, sys
sys.stdout.reconfigure(encoding='utf-8')

async def test_clear_buttons():
    import websockets
    edge_bin = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    html_path = os.path.abspath("Calculadora Financeira 17bIi.html")
    file_url = "file:" + urllib.request.pathname2url(html_path)
    port = 9235

    proc = subprocess.Popen([
        edge_bin,
        "--headless=new",
        f"--remote-debugging-port={port}",
        "--window-size=1600,1000",
        "--no-first-run",
        "--disable-gpu",
        file_url
    ])

    time.sleep(2)

    try:
        ws_url = None
        for _ in range(25):
            time.sleep(0.4)
            try:
                resp = urllib.request.urlopen(f"http://127.0.0.1:{port}/json", timeout=2)
                targets = json.loads(resp.read().decode())
                for t in targets:
                    if t.get('type') == 'page' and 'Calculadora' in t.get('url', ''):
                        ws_url = t.get('webSocketDebuggerUrl')
                        break
                    elif t.get('type') == 'page' and not ws_url:
                        ws_url = t.get('webSocketDebuggerUrl')
                if ws_url:
                    break
            except Exception:
                pass

        async with websockets.connect(ws_url) as ws:
            msg_id = 1
            async def send(method, params=None):
                nonlocal msg_id
                cid = msg_id
                msg_id += 1
                await ws.send(json.dumps({"id": cid, "method": method, "params": params or {}}))
                while True:
                    resp = json.loads(await ws.recv())
                    if resp.get("id") == cid:
                        return resp

            async def evaluate(expr):
                r = await send("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
                result = r.get("result", {})
                if "exceptionDetails" in result:
                    raise Exception(result["exceptionDetails"])
                return result.get("result", {}).get("value")

            print("\n--- TESTE 1: Botão Limpar Campo em Fórmulas (#solve-clear-variables) ---")
            solve_btn_text = await evaluate("document.getElementById('solve-clear-variables').innerText.trim()")
            solve_btn_bg = await evaluate("window.getComputedStyle(document.getElementById('solve-clear-variables')).backgroundColor")
            solve_btn_color = await evaluate("window.getComputedStyle(document.getElementById('solve-clear-variables')).color")
            print(f"Texto: {solve_btn_text}")
            print(f"Background: {solve_btn_bg}")
            print(f"Color: {solve_btn_color}")
            assert solve_btn_text == "Limpar Campo", f"Esperado 'Limpar Campo', obtido {solve_btn_text}"
            assert "185, 28, 28" in solve_btn_bg, f"Esperado rgb(185, 28, 28), obtido {solve_btn_bg}"

            print("\n--- TESTE 2: Botão Limpar Campos do Toolbar (#module-clear-fields-btn) ---")
            # switch to TVM tab to show moduleExampleToolbar
            await evaluate("app.switchTab('TVM')")
            toolbar_btn_text = await evaluate("document.getElementById('module-clear-fields-btn').innerText.trim()")
            toolbar_btn_bg = await evaluate("window.getComputedStyle(document.getElementById('module-clear-fields-btn')).backgroundColor")
            toolbar_btn_color = await evaluate("window.getComputedStyle(document.getElementById('module-clear-fields-btn')).color")
            toolbar_btn_html = await evaluate("document.getElementById('module-clear-fields-btn').innerHTML")
            print(f"Texto: {toolbar_btn_text}")
            print(f"Background: {toolbar_btn_bg}")
            print(f"Color: {toolbar_btn_color}")
            print(f"HTML: {toolbar_btn_html}")
            assert toolbar_btn_text == "Limpar Campos", f"Esperado 'Limpar Campos', obtido {toolbar_btn_text}"
            assert "✕" not in toolbar_btn_html, "X ainda está presente no botão!"
            assert "185, 28, 28" in toolbar_btn_bg, f"Esperado rgb(185, 28, 28), obtido {toolbar_btn_bg}"

            print("\n--- TESTE 3: Botão Limpar TVM no cabeçalho do painel TVM ---")
            tvm_btn_bg = await evaluate("window.getComputedStyle(document.querySelector('#panel-TVM button.btn-clear-module')).backgroundColor")
            tvm_btn_text = await evaluate("document.querySelector('#panel-TVM button.btn-clear-module').innerText.trim()")
            tvm_btn_html = await evaluate("document.querySelector('#panel-TVM button.btn-clear-module').innerHTML")
            print(f"Texto: {tvm_btn_text}")
            print(f"Background: {tvm_btn_bg}")
            assert tvm_btn_text == "Limpar TVM", f"Esperado 'Limpar TVM', obtido {tvm_btn_text}"
            assert "↺" not in tvm_btn_html, "Ícone ainda está presente no botão Limpar TVM!"
            assert "185, 28, 28" in tvm_btn_bg, f"Esperado rgb(185, 28, 28), obtido {tvm_btn_bg}"

            print("\n--- TESTE 4: Botão Limpar CFLO no cabeçalho do painel CFLO ---")
            await evaluate("app.switchTab('CFLO')")
            cflo_btn_bg = await evaluate("window.getComputedStyle(document.querySelector('#panel-CFLO button.btn-clear-module')).backgroundColor")
            cflo_btn_text = await evaluate("document.querySelector('#panel-CFLO button.btn-clear-module').innerText.trim()")
            cflo_btn_html = await evaluate("document.querySelector('#panel-CFLO button.btn-clear-module').innerHTML")
            print(f"Texto: {cflo_btn_text}")
            print(f"Background: {cflo_btn_bg}")
            assert cflo_btn_text == "Limpar CFLO", f"Esperado 'Limpar CFLO', obtido {cflo_btn_text}"
            assert "↺" not in cflo_btn_html, "Ícone ainda está presente no botão Limpar CFLO!"
            assert "185, 28, 28" in cflo_btn_bg, f"Esperado rgb(185, 28, 28), obtido {cflo_btn_bg}"

            print("\n--- TESTE 5: Funcionalidade de Limpeza nos Módulos ---")
            # Fill CFLO inputs
            await evaluate("document.getElementById('input-cflo-rate').value = '15'")
            await evaluate("document.getElementById('cflo-new-amount').value = '1000'")
            # Click Limpar Campos (toolbar)
            await evaluate("document.getElementById('module-clear-fields-btn').click()")
            rate_val = await evaluate("document.getElementById('input-cflo-rate').value")
            amount_val = await evaluate("document.getElementById('cflo-new-amount').value")
            print(f"Após clique em Limpar Campos: rate='{rate_val}', amount='{amount_val}'")
            assert rate_val == "" and amount_val == "", "Campos não foram limpos!"

            print("\n--- TESTE 6: Funcionalidade do Botão Limpar CFLO no Cabeçalho ---")
            await evaluate("document.getElementById('input-cflo-rate').value = '18'")
            await evaluate("document.getElementById('cflo-new-amount').value = '2500'")
            await evaluate("document.querySelector('#panel-CFLO button.btn-clear-module').click()")
            rate_val2 = await evaluate("document.getElementById('input-cflo-rate').value")
            amount_val2 = await evaluate("document.getElementById('cflo-new-amount').value")
            print(f"Após clique em Limpar CFLO: rate='{rate_val2}', amount='{amount_val2}'")
            assert rate_val2 == "" and amount_val2 == "", "Campos não foram limpos pelo botão Limpar CFLO!"

            print("\n==========================================")
            print("TODOS OS TESTES DE ESTILO E FUNCIONALIDADE DOS BOTÕES PASSARAM COM SUCESSO!")
            print("==========================================")

    finally:
        proc.kill()

if __name__ == "__main__":
    asyncio.run(test_clear_buttons())
