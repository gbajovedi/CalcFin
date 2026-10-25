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
    port = 9225
    user_data_dir = os.path.abspath("scratch/edge_profile_tab_persist")
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

            await asyncio.sleep(0.5)

            print("\n=== CENÁRIO 1: Novo Usuário (Padrão Inicial deve ser Fórmulas SOLVE) ===")
            await eval_js("localStorage.clear(); location.reload();")
            await asyncio.sleep(0.8)

            active_mod = await eval_js("app.activeModuleId()")
            tab_solve_selected = await eval_js("document.getElementById('tab-SOLVE').getAttribute('aria-selected')")
            panel_solve_hidden = await eval_js("document.getElementById('panel-SOLVE').classList.contains('hidden')")
            print(f"Módulo ativo inicial: {active_mod} (Esperado: 'SOLVE')")
            print(f"tab-SOLVE aria-selected: {tab_solve_selected} (Esperado: 'true')")
            print(f"panel-SOLVE hidden: {panel_solve_hidden} (Esperado: False)")
            assert active_mod == 'SOLVE'
            assert tab_solve_selected == 'true'
            assert panel_solve_hidden is False
            print("=> CENÁRIO 1 PASSOU!")

            print("\n=== CENÁRIO 2: Trocar para 'CFLO' (Fluxo de Caixa) e Recarregar Página (F5) ===")
            await eval_js("app.switchTab('CFLO')")
            await asyncio.sleep(0.2)

            direct_tab = await eval_js("localStorage.getItem('hp17bii-active-tab')")
            ws_state = await eval_js("JSON.parse(localStorage.getItem('hp17bii-workspace-state')).activeTab")
            print(f"localStorage['hp17bii-active-tab']: {direct_tab}")
            print(f"workspace-state.activeTab: {ws_state}")
            assert direct_tab == 'CFLO'
            assert ws_state == 'CFLO'

            # Simular F5 / Refresh
            await eval_js("location.reload()")
            await asyncio.sleep(0.8)

            active_after_reload = await eval_js("app.activeModuleId()")
            panel_cflo_hidden = await eval_js("document.getElementById('panel-CFLO').classList.contains('hidden')")
            panel_solve_hidden = await eval_js("document.getElementById('panel-SOLVE').classList.contains('hidden')")
            tab_cflo_selected = await eval_js("document.getElementById('tab-CFLO').getAttribute('aria-selected')")
            print(f"Após reload - Módulo ativo: {active_after_reload} (Esperado: 'CFLO')")
            print(f"Após reload - panel-CFLO hidden: {panel_cflo_hidden} (Esperado: False)")
            print(f"Após reload - panel-SOLVE hidden: {panel_solve_hidden} (Esperado: True)")
            print(f"Após reload - tab-CFLO aria-selected: {tab_cflo_selected} (Esperado: 'true')")
            assert active_after_reload == 'CFLO'
            assert panel_cflo_hidden is False
            assert panel_solve_hidden is True
            assert tab_cflo_selected == 'true'
            print("=> CENÁRIO 2 PASSOU: Reabriu com sucesso em FLUXO DE CAIXA!")

            print("\n=== CENÁRIO 3: Trocar para 'TVM' (Matemática Financeira) e Recarregar Página ===")
            await eval_js("app.switchTab('TVM')")
            await asyncio.sleep(0.2)

            await eval_js("location.reload()")
            await asyncio.sleep(0.8)

            active_tvm_reload = await eval_js("app.activeModuleId()")
            panel_tvm_hidden = await eval_js("document.getElementById('panel-TVM').classList.contains('hidden')")
            tab_tvm_selected = await eval_js("document.getElementById('tab-TVM').getAttribute('aria-selected')")
            print(f"Após reload - Módulo ativo: {active_tvm_reload} (Esperado: 'TVM')")
            print(f"Após reload - panel-TVM hidden: {panel_tvm_hidden} (Esperado: False)")
            print(f"Após reload - tab-TVM aria-selected: {tab_tvm_selected} (Esperado: 'true')")
            assert active_tvm_reload == 'TVM'
            assert panel_tvm_hidden is False
            assert tab_tvm_selected == 'true'
            print("=> CENÁRIO 3 PASSOU: Reabriu com sucesso em MATEMÁTICA FINANCEIRA!")

            print("\n=== CENÁRIO 4: Testando Demais Abas (TIME, CURRX, FIN_TOOLS, BUS_SUM, TAPE) ===")
            for t in ['TIME', 'CURRX', 'FIN_TOOLS', 'BUS_SUM', 'TAPE']:
                await eval_js(f"app.switchTab('{t}')")
                await asyncio.sleep(0.1)
                await eval_js("location.reload()")
                await asyncio.sleep(0.6)
                act = await eval_js("app.activeModuleId()")
                print(f"Testando aba {t} -> reabriu em: {act}")
                assert act == t, f"Esperava reabrir em {t}, mas obteve {act}"
            print("=> CENÁRIO 4 PASSOU PARA TODAS AS ABAS!")

            print("\n=== CENÁRIO 5: Mobile Viewport (Puxar tela para baixo / pull-to-refresh no celular) ===")
            # Simular viewport de celular
            await eval_js("app.setMobileView('tools'); app.switchTab('CFLO');")
            await asyncio.sleep(0.1)
            is_mobile_tools = await eval_js("document.body.classList.contains('mobile-view-tools')")
            print(f"Antes do refresh - body.mobile-view-tools: {is_mobile_tools}")
            assert is_mobile_tools is True

            # Pull-to-refresh / reload
            await eval_js("location.reload()")
            await asyncio.sleep(0.8)

            mobile_tools_after = await eval_js("document.body.classList.contains('mobile-view-tools')")
            active_mod_mobile = await eval_js("app.activeModuleId()")
            print(f"Após pull-to-refresh - body.mobile-view-tools: {mobile_tools_after} (Esperado: True)")
            print(f"Após pull-to-refresh - Módulo ativo: {active_mod_mobile} (Esperado: 'CFLO')")
            assert mobile_tools_after is True
            assert active_mod_mobile == 'CFLO'
            print("=> CENÁRIO 5 PASSOU: Pull-to-refresh no celular preservou a visualização e a aba!")

            print("\n=== CENÁRIO 6: Reset de Fábrica restaura padrão SOLVE ===")
            await eval_js("app.resetToFactoryDefaults(false)")
            act_reset = await eval_js("app.activeModuleId()")
            print(f"Após reset - Módulo ativo: {act_reset} (Esperado: 'SOLVE')")
            assert act_reset == 'SOLVE'
            print("=> CENÁRIO 6 PASSOU!")

            print("\n===========================================================")
            print("TODOS OS TESTES DE PERSISTÊNCIA DA ÚLTIMA ABA PASSARAM!")
            print("===========================================================")

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()

if __name__ == '__main__':
    asyncio.run(run_tests())
