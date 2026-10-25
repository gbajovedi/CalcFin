# -*- coding: utf-8 -*-
import os, subprocess, json, time, urllib.request, asyncio, sys
sys.stdout.reconfigure(encoding='utf-8')

async def test_pyr():
    import websockets
    edge_bin = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    html_path = os.path.abspath("Calculadora Financeira 17bIi.html")
    file_url = "file:" + urllib.request.pathname2url(html_path)
    port = 9260

    proc = subprocess.Popen([
        edge_bin,
        "--headless=new",
        f"--remote-debugging-port={port}",
        "--window-size=1280,800",
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
                    if t.get('type') == 'page':
                        ws_url = t.get('webSocketDebuggerUrl')
                        break
                if ws_url:
                    break
            except Exception:
                pass

        async with websockets.connect(ws_url) as ws:
            msg_id = 0
            async def send_cmd(method, params=None):
                nonlocal msg_id
                msg_id += 1
                await ws.send(json.dumps({'id': msg_id, 'method': method, 'params': params or {}}))
                while True:
                    resp = json.loads(await ws.recv())
                    if resp.get('id') == msg_id:
                        return resp

            async def eval_js(expr):
                r = await send_cmd('Runtime.evaluate', {'expression': expr, 'returnByValue': True})
                return r.get('result', {}).get('result', {}).get('value')

            print("\n--- TESTE 1: Estado Inicial do Campo P/YR ---")
            await eval_js("app.switchTab('TVM')")
            pyr_val = await eval_js("document.getElementById('input-tvm-PYR').value")
            pyr_ph = await eval_js("document.getElementById('input-tvm-PYR').placeholder")
            print(f"P/YR Value: '{pyr_val}'")
            print(f"P/YR Placeholder: '{pyr_ph}'")
            assert pyr_val == "", f"Esperado valor vazio, mas obteve '{pyr_val}'"
            assert pyr_ph == "Insira os dados", f"Esperado placeholder 'Insira os dados', obteve '{pyr_ph}'"

            print("\n--- TESTE 2: Blur no Campo P/YR Vazio Não Preenche 12 ---")
            await eval_js("const el = document.getElementById('input-tvm-PYR'); el.focus(); el.blur();")
            pyr_val_after_blur = await eval_js("document.getElementById('input-tvm-PYR').value")
            print(f"P/YR após blur: '{pyr_val_after_blur}'")
            assert pyr_val_after_blur == "", f"Blur preencheu automaticamente com '{pyr_val_after_blur}'!"

            print("\n--- TESTE 3: Cálculo de TVM sem P/YR Mantém Campo Vazio ---")
            # Preenche N=12, I=12, PV=-1000, FV=0
            await eval_js("document.getElementById('input-tvm-N').value = '12'")
            await eval_js("document.getElementById('input-tvm-I').value = '12'")
            await eval_js("document.getElementById('input-tvm-PV').value = '-1000'")
            await eval_js("document.getElementById('input-tvm-FV').value = '0'")
            # Dispara cálculo de PMT
            await eval_js("app.calculateTVM('PMT')")
            pmt_val = await eval_js("document.getElementById('input-tvm-PMT').value")
            pyr_val_after_calc = await eval_js("document.getElementById('input-tvm-PYR').value")
            print(f"PMT calculado: {pmt_val}")
            print(f"P/YR após cálculo: '{pyr_val_after_calc}'")
            assert pmt_val != "", "PMT deveria ter sido calculado!"
            assert pyr_val_after_calc == "", f"Cálculo preencheu P/YR com '{pyr_val_after_calc}', mas deveria manter vazio!"

            print("\n--- TESTE 4: Limpar TVM Mantém Campo Vazio ---")
            await eval_js("app.clearTvmModule()")
            pyr_after_clear = await eval_js("document.getElementById('input-tvm-PYR').value")
            print(f"P/YR após Limpar TVM: '{pyr_after_clear}'")
            assert pyr_after_clear == "", f"Limpar TVM deixou valor '{pyr_after_clear}'!"

            print("\n==========================================")
            print("TODOS OS TESTES DE COMPORTAMENTO DO P/YR PASSARAM COM SUCESSO!")
            print("==========================================")

    finally:
        proc.kill()

if __name__ == "__main__":
    asyncio.run(test_pyr())

