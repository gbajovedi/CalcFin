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
    port = 9224
    user_data_dir = os.path.abspath("scratch/edge_profile_prefill")
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
        # Wait for CDP
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

            await asyncio.sleep(0.5)

            print("\n=== CENÁRIO 1: Novo Usuário abrindo a aba de Matemática Financeira ===")
            await eval_js("localStorage.clear(); location.reload();")
            await asyncio.sleep(0.8)

            # Switch to TVM tab
            await eval_js("app.switchTab('TVM')")
            await asyncio.sleep(0.2)

            pyr_val = await eval_js("document.getElementById('input-tvm-PYR').value")
            fv_val = await eval_js("document.getElementById('input-tvm-FV').value")
            tvm_pyr = await eval_js("app.tvm.PYR")
            tvm_fv = await eval_js("app.tvm.FV")

            print(f"input-tvm-PYR: '{pyr_val}' (Esperado: '1')")
            print(f"input-tvm-FV:  '{fv_val}' (Esperado: '0.0000')")
            print(f"app.tvm.PYR:   {tvm_pyr} (Esperado: 1)")
            print(f"app.tvm.FV:    {tvm_fv} (Esperado: 0)")

            assert pyr_val == '1', f"PYR esperado '1', obteve '{pyr_val}'"
            assert fv_val == '0.0000', f"FV esperado '0.0000', obteve '{fv_val}'"
            assert tvm_pyr == 1, f"app.tvm.PYR esperado 1, obteve {tvm_pyr}"
            assert tvm_fv == 0, f"app.tvm.FV esperado 0, obteve {tvm_fv}"
            print("=> CENÁRIO 1 PASSOU COM SUCESSO!")

            print("\n=== CENÁRIO 2: Limpar Campos e Reabrir a Aba de Matemática Financeira ===")
            # Clear active module fields while in TVM
            await eval_js("app.clearActiveModuleFields()")
            await asyncio.sleep(0.1)

            # Switch to SOLVE
            await eval_js("app.switchTab('SOLVE')")
            await asyncio.sleep(0.1)

            # Switch back to TVM ("Quando eu abrir a aba de matematica financeira...")
            await eval_js("app.switchTab('TVM')")
            await asyncio.sleep(0.2)

            pyr_val2 = await eval_js("document.getElementById('input-tvm-PYR').value")
            fv_val2 = await eval_js("document.getElementById('input-tvm-FV').value")
            tvm_pyr2 = await eval_js("app.tvm.PYR")
            tvm_fv2 = await eval_js("app.tvm.FV")

            print(f"Reabertura - input-tvm-PYR: '{pyr_val2}' (Esperado: '1')")
            print(f"Reabertura - input-tvm-FV:  '{fv_val2}' (Esperado: '0.0000')")
            print(f"Reabertura - app.tvm.PYR:   {tvm_pyr2} (Esperado: 1)")
            print(f"Reabertura - app.tvm.FV:    {tvm_fv2} (Esperado: 0)")

            assert pyr_val2 == '1', f"Reabertura PYR esperado '1', obteve '{pyr_val2}'"
            assert fv_val2 == '0.0000', f"Reabertura FV esperado '0.0000', obteve '{fv_val2}'"
            assert tvm_pyr2 == 1, f"Reabertura app.tvm.PYR esperado 1, obteve {tvm_pyr2}"
            assert tvm_fv2 == 0, f"Reabertura app.tvm.FV esperado 0, obteve {tvm_fv2}"
            print("=> CENÁRIO 2 PASSOU COM SUCESSO!")

            print("\n=== CENÁRIO 3: Preservação de Valores Customizados do Usuário ===")
            await eval_js("""
                document.getElementById('input-tvm-FV').value = '5000.0000';
                app.syncInputToState('tvm', 'FV', '5000.0000');
                document.getElementById('input-tvm-PYR').value = '6';
                app.syncInputToState('tvm', 'PYR', '6');
                app.saveWorkspaceState();
            """)
            # Switch to SOLVE and back to TVM
            await eval_js("app.switchTab('SOLVE')")
            await asyncio.sleep(0.1)
            await eval_js("app.switchTab('TVM')")
            await asyncio.sleep(0.1)

            pyr_custom = await eval_js("document.getElementById('input-tvm-PYR').value")
            fv_custom = await eval_js("document.getElementById('input-tvm-FV').value")
            print(f"Custom input-tvm-PYR preservado: '{pyr_custom}' (Esperado: '6')")
            print(f"Custom input-tvm-FV preservado:  '{fv_custom}' (Esperado: '5000.0000')")
            assert pyr_custom == '6', f"PYR custom esperado '6', obteve '{pyr_custom}'"
            assert fv_custom == '5000.0000', f"FV custom esperado '5000.0000', obteve '{fv_custom}'"
            print("=> CENÁRIO 3 PASSOU COM SUCESSO!")

            print("\n=== CENÁRIO 4: Migração de Estado Antigo (PYR = 12) para P/YR = 1 ===")
            await eval_js("""
                localStorage.setItem('hp17bii-workspace-state', JSON.stringify({
                    tvm: { N: 24, I: 10, PV: -1000, PMT: 50, FV: 0, PYR: 12, isBegin: false }
                }));
                location.reload();
            """)
            await asyncio.sleep(0.8)
            await eval_js("app.switchTab('TVM')")
            await asyncio.sleep(0.2)

            pyr_migrated = await eval_js("document.getElementById('input-tvm-PYR').value")
            fv_migrated = await eval_js("document.getElementById('input-tvm-FV').value")
            print(f"Após reload com antigo 12 - input-tvm-PYR: '{pyr_migrated}' (Esperado: '1')")
            print(f"Após reload com antigo 12 - input-tvm-FV:  '{fv_migrated}' (Esperado: '0.0000')")
            assert pyr_migrated == '1', f"PYR esperado '1', obteve '{pyr_migrated}'"
            assert fv_migrated == '0.0000', f"FV esperado '0.0000', obteve '{fv_migrated}'"
            print("=> CENÁRIO 4 PASSOU COM SUCESSO!")

            print("\n=== CENÁRIO 5: Reset para Padrões de Fábrica ===")
            await eval_js("app.resetToFactoryDefaults(false)")
            await eval_js("app.switchTab('TVM')")
            await asyncio.sleep(0.2)

            pyr_reset = await eval_js("document.getElementById('input-tvm-PYR').value")
            fv_reset = await eval_js("document.getElementById('input-tvm-FV').value")
            print(f"Após Reset - input-tvm-PYR: '{pyr_reset}' (Esperado: '1')")
            print(f"Após Reset - input-tvm-FV:  '{fv_reset}' (Esperado: '0.0000')")
            assert pyr_reset == '1', f"Reset PYR esperado '1', obteve '{pyr_reset}'"
            assert fv_reset == '0.0000', f"Reset FV esperado '0.0000', obteve '{fv_reset}'"
            print("=> CENÁRIO 5 PASSOU COM SUCESSO!")

            print("\n=======================================================")
            print("TODOS OS TESTES DE PRÉ-PREENCHIMENTO DE FV=0 E P/YR=1 PASSARAM!")
            print("=======================================================")

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()

if __name__ == '__main__':
    asyncio.run(run_tests())
