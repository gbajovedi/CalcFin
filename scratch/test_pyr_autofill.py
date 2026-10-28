# -*- coding: utf-8 -*-
import asyncio
import json
import os
import subprocess
import time
import urllib.request
import websockets

def find_edge_path():
    candidates = [
        os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%LocalAppData%\Microsoft\Edge\Application\msedge.exe"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return "msedge.exe"

async def run_tests():
    edge_bin = find_edge_path()
    port = 9226
    user_data_dir = os.path.abspath("scratch/edge_profile_pyr_autofill")
    file_url = "file:///" + os.path.abspath("Calculadora Financeira 17bIi.html").replace("\\", "/")

    cmd = [
        edge_bin,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={user_data_dir}",
        "--headless=new",
        "--disable-gpu",
        "--no-first-run",
        file_url
    ]
    proc = subprocess.Popen(cmd)
    try:
        ws_url = None
        for _ in range(25):
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{port}/json") as resp:
                    tabs = json.loads(resp.read().decode())
                    for tab in tabs:
                        if tab.get("type") == "page" and "webSocketDebuggerUrl" in tab:
                            ws_url = tab["webSocketDebuggerUrl"]
                            break
                    if ws_url:
                        break
            except Exception:
                pass
            time.sleep(0.3)

        assert ws_url, "Falha ao obter WebSocketDebuggerUrl do Edge"

        async with websockets.connect(ws_url, ping_interval=None) as ws:
            req_id = 0
            async def eval_js(expression):
                nonlocal req_id
                req_id += 1
                msg = {
                    "id": req_id,
                    "method": "Runtime.evaluate",
                    "params": {
                        "expression": expression,
                        "returnByValue": True,
                        "awaitPromise": True
                    }
                }
                await ws.send(json.dumps(msg))
                while True:
                    res = json.loads(await ws.recv())
                    if res.get("id") == req_id:
                        result = res.get("result", {}).get("result", {})
                        if "value" in result:
                            return result["value"]
                        elif result.get("subtype") == "error":
                            raise RuntimeError(result.get("description", "JS Error"))
                        return None

            for _ in range(30):
                try:
                    ready = await eval_js("typeof window.app !== 'undefined' && typeof window.app.switchTab === 'function'")
                    if ready:
                        break
                except Exception:
                    pass
                await asyncio.sleep(0.3)

            # Switch to TVM and clear all fields
            await eval_js("app.switchTab('TVM')")
            await eval_js("app.clearActiveModuleFields()")
            await asyncio.sleep(0.2)

            print("\n=== CENÁRIO 1: Calcular PMT sem preencher FV nem P/YR ===")
            # Preenche N=12, I=12, PV=-1000, deixa FV e P/YR vazios
            await eval_js("""
                document.getElementById('input-tvm-N').value = '12';
                app.syncInputToState('tvm', 'N', '12');
                document.getElementById('input-tvm-I').value = '12';
                app.syncInputToState('tvm', 'I', '12');
                document.getElementById('input-tvm-PV').value = '-1000';
                app.syncInputToState('tvm', 'PV', '-1000');
                document.getElementById('input-tvm-FV').value = '';
                app.syncInputToState('tvm', 'FV', '');
                document.getElementById('input-tvm-PYR').value = '';
                app.syncInputToState('tvm', 'PYR', '');
            """)

            # Clica no botão Calcular PMT
            await eval_js("document.getElementById('btn-tvm-PMT').click()")
            await asyncio.sleep(0.2)

            pyr_val = await eval_js("document.getElementById('input-tvm-PYR').value")
            fv_val = await eval_js("document.getElementById('input-tvm-FV').value")
            pmt_val = await eval_js("app.tvm.PMT")
            app_pyr = await eval_js("app.tvm.PYR")
            app_fv = await eval_js("app.tvm.FV")

            print(f"input-tvm-PYR preenchido: '{pyr_val}' (Esperado: '1')")
            print(f"input-tvm-FV preenchido:  '{fv_val}' (Esperado: '0.0000')")
            print(f"app.tvm.PYR: {app_pyr} (Esperado: 1)")
            print(f"app.tvm.FV:  {app_fv} (Esperado: 0)")
            print(f"app.tvm.PMT: {pmt_val}")

            assert pyr_val == '1', f"Esperava PYR '1', obteve '{pyr_val}'"
            assert '0.0000' in fv_val or fv_val == '0', f"Esperava FV '0.0000' ou '0', obteve '{fv_val}'"
            assert app_pyr == 1, f"app.tvm.PYR esperado 1, obteve {app_pyr}"
            assert app_fv == 0, f"app.tvm.FV esperado 0, obteve {app_fv}"
            # Com i = 12% / 1 = 12%, n=12, PV=-1000, FV=0: PMT = 161.4367...
            assert pmt_val is not None and abs(pmt_val - 161.4367) < 0.05, f"PMT inesperado: {pmt_val}"
            print("=> CENÁRIO 1 PASSOU COM SUCESSO!")

            print("\n=== CENÁRIO 2: Calcular PV sem preencher FV nem P/YR ===")
            await eval_js("app.clearActiveModuleFields()")
            await eval_js("""
                document.getElementById('input-tvm-N').value = '10';
                app.syncInputToState('tvm', 'N', '10');
                document.getElementById('input-tvm-I').value = '5';
                app.syncInputToState('tvm', 'I', '5');
                document.getElementById('input-tvm-PMT').value = '100';
                app.syncInputToState('tvm', 'PMT', '100');
                document.getElementById('input-tvm-FV').value = '';
                app.syncInputToState('tvm', 'FV', '');
                document.getElementById('input-tvm-PYR').value = '';
                app.syncInputToState('tvm', 'PYR', '');
            """)
            await eval_js("document.getElementById('btn-tvm-PV').click()")
            await asyncio.sleep(0.2)

            pyr_val2 = await eval_js("document.getElementById('input-tvm-PYR').value")
            fv_val2 = await eval_js("document.getElementById('input-tvm-FV').value")
            pv_val2 = await eval_js("app.tvm.PV")
            print(f"input-tvm-PYR preenchido: '{pyr_val2}' (Esperado: '1')")
            print(f"input-tvm-FV preenchido:  '{fv_val2}' (Esperado: '0.0000')")
            print(f"app.tvm.PV: {pv_val2}")
            assert pyr_val2 == '1', f"Esperava PYR '1', obteve '{pyr_val2}'"
            assert '0.0000' in fv_val2 or fv_val2 == '0', f"Esperava FV '0.0000', obteve '{fv_val2}'"
            assert pv_val2 is not None and pv_val2 < 0, f"PV esperado negativo, obteve {pv_val2}"
            print("=> CENÁRIO 2 PASSOU COM SUCESSO!")

            print("\n=== CENÁRIO 3: Calcular FV sem preencher P/YR ===")
            await eval_js("app.clearActiveModuleFields()")
            await eval_js("""
                document.getElementById('input-tvm-N').value = '12';
                app.syncInputToState('tvm', 'N', '12');
                document.getElementById('input-tvm-I').value = '10';
                app.syncInputToState('tvm', 'I', '10');
                document.getElementById('input-tvm-PV').value = '-1000';
                app.syncInputToState('tvm', 'PV', '-1000');
                document.getElementById('input-tvm-PMT').value = '0';
                app.syncInputToState('tvm', 'PMT', '0');
                document.getElementById('input-tvm-PYR').value = '';
                app.syncInputToState('tvm', 'PYR', '');
            """)
            await eval_js("document.getElementById('btn-tvm-FV').click()")
            await asyncio.sleep(0.2)

            pyr_val3 = await eval_js("document.getElementById('input-tvm-PYR').value")
            fv_val3 = await eval_js("app.tvm.FV")
            print(f"input-tvm-PYR preenchido: '{pyr_val3}' (Esperado: '1')")
            print(f"app.tvm.FV: {fv_val3}")
            assert pyr_val3 == '1', f"Esperava PYR '1', obteve '{pyr_val3}'"
            assert fv_val3 is not None and abs(fv_val3 - 3138.43) < 1.0, f"FV inesperado: {fv_val3}"
            print("=> CENÁRIO 3 PASSOU COM SUCESSO!")

            print("\n=== CENÁRIO 4: Usuário informa P/YR customizado (ex: 12) - NÃO SOBRESCREVER ===")
            await eval_js("app.clearActiveModuleFields()")
            await eval_js("""
                document.getElementById('input-tvm-N').value = '12';
                app.syncInputToState('tvm', 'N', '12');
                document.getElementById('input-tvm-I').value = '12';
                app.syncInputToState('tvm', 'I', '12');
                document.getElementById('input-tvm-PV').value = '-1000';
                app.syncInputToState('tvm', 'PV', '-1000');
                document.getElementById('input-tvm-PYR').value = '12';
                app.syncInputToState('tvm', 'PYR', '12');
                document.getElementById('input-tvm-FV').value = '';
                app.syncInputToState('tvm', 'FV', '');
            """)
            await eval_js("document.getElementById('btn-tvm-PMT').click()")
            await asyncio.sleep(0.2)

            pyr_val4 = await eval_js("document.getElementById('input-tvm-PYR').value")
            fv_val4 = await eval_js("document.getElementById('input-tvm-FV').value")
            pmt_val4 = await eval_js("app.tvm.PMT")
            print(f"input-tvm-PYR preservado: '{pyr_val4}' (Esperado: '12')")
            print(f"input-tvm-FV preenchido:  '{fv_val4}' (Esperado: '0.0000')")
            print(f"app.tvm.PMT (mensal a 1%): {pmt_val4}")
            assert pyr_val4 == '12', f"PYR esperado '12', obteve '{pyr_val4}'"
            assert '0.0000' in fv_val4 or fv_val4 == '0', f"FV esperado '0.0000', obteve '{fv_val4}'"
            # Com taxa anual 12% / 12 = 1% a.m., n=12, PV=-1000: PMT = 88.8488...
            assert pmt_val4 is not None and abs(pmt_val4 - 88.85) < 0.1, f"PMT inesperado: {pmt_val4}"
            print("=> CENÁRIO 4 PASSOU: P/YR CUSTOMIZADO PRESERVADO!")

            print("\n===========================================================")
            print("TODOS OS TESTES DE AUTO-PREENCHIMENTO DE P/YR COM 1 PASSARAM!")
            print("===========================================================")

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()

if __name__ == '__main__':
    asyncio.run(run_tests())
