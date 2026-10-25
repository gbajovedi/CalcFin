# -*- coding: utf-8 -*-
import os, subprocess, json, time, urllib.request, asyncio, sys
sys.stdout.reconfigure(encoding='utf-8')

async def run_tests():
    import websockets
    edge_bin = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    html_path = os.path.abspath("Calculadora Financeira 17bIi.html")
    file_url = "file:" + urllib.request.pathname2url(html_path)
    port = 9430

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

            print("\n=== CENÁRIO 1: Novo Usuário (Sem Dados Pré-existentes no localStorage) ===")
            await eval_js("localStorage.removeItem('hp17bii-workspace-state')")
            # Recarrega a página limpa
            await eval_js("location.reload()")
            await asyncio.sleep(1)

            # Aguarda inicialização completa
            for _ in range(15):
                ready = await eval_js("document.readyState === 'complete' && Boolean(window.app)")
                if ready:
                    break
                await asyncio.sleep(0.2)

            # Alternar para a aba TVM
            await eval_js("app.switchTab('TVM')")
            
            pyr_state = await eval_js("app.tvm.PYR")
            fv_state = await eval_js("app.tvm.FV")
            is_begin = await eval_js("app.tvm.isBegin")
            n_state = await eval_js("app.tvm.N")
            i_state = await eval_js("app.tvm.I")
            pv_state = await eval_js("app.tvm.PV")
            pmt_state = await eval_js("app.tvm.PMT")

            pyr_input = await eval_js("document.getElementById('input-tvm-PYR').value")
            fv_input = await eval_js("document.getElementById('input-tvm-FV').value")
            n_input = await eval_js("document.getElementById('input-tvm-N').value")

            print(f"app.tvm.PYR: {pyr_state} (Esperado: 12)")
            print(f"app.tvm.FV: {fv_state} (Esperado: 0)")
            print(f"app.tvm.isBegin: {is_begin} (Esperado: False -> END mode)")
            print(f"Campos N, I, PV, PMT: {n_state}, {i_state}, {pv_state}, {pmt_state} (Esperados: null)")
            print(f"Input P/YR: '{pyr_input}' (Esperado: '12')")
            print(f"Input FV: '{fv_input}' (Esperado: '0.0000')")
            print(f"Input N: '{n_input}' (Esperado: '')")

            assert pyr_state == 12, f"P/YR deveria ser 12 para novo usuário, obteve {pyr_state}"
            assert fv_state == 0, f"FV deveria ser 0 para novo usuário, obteve {fv_state}"
            assert is_begin is False, f"Modo de pagamento deveria ser END (isBegin=false)"
            assert n_state is None and i_state is None and pv_state is None and pmt_state is None
            assert pyr_input == "12", f"Input P/YR deveria ser '12', obteve '{pyr_input}'"
            assert fv_input == "0.0000", f"Input FV deveria ser '0.0000', obteve '{fv_input}'"
            assert n_input == "", f"Input N deveria estar vazio com placeholder, obteve '{n_input}'"
            print("=> CENÁRIO 1 PASSOU COM SUCESSO!")

            print("\n=== CENÁRIO 2: Usuário Existente com Dados Salvos no JSON (NÃO SOBRESCREVER) ===")
            # Simula um usuário que configurou P/YR = 1 (modo anual acadêmico), FV = 2500, N = 36, I = 8.5
            custom_user_state = {
                "version": 1,
                "mode": "ALG",
                "decimals": 4,
                "hasCustomDecimals": True,
                "tvm": {
                    "N": 36,
                    "I": 8.5,
                    "PV": -15000,
                    "PMT": 473.53,
                    "FV": 2500,
                    "PYR": 1,
                    "isBegin": True
                }
            }
            await eval_js(f"localStorage.setItem('hp17bii-workspace-state', JSON.stringify({json.dumps(custom_user_state)}))")
            
            # Recarrega a página
            await eval_js("location.reload()")
            await asyncio.sleep(1)

            for _ in range(15):
                ready = await eval_js("document.readyState === 'complete' && Boolean(window.app)")
                if ready:
                    break
                await asyncio.sleep(0.2)

            await eval_js("app.switchTab('TVM')")

            user_pyr = await eval_js("app.tvm.PYR")
            user_fv = await eval_js("app.tvm.FV")
            user_n = await eval_js("app.tvm.N")
            user_i = await eval_js("app.tvm.I")
            user_pv = await eval_js("app.tvm.PV")
            user_pmt = await eval_js("app.tvm.PMT")
            user_begin = await eval_js("app.tvm.isBegin")

            user_pyr_input = await eval_js("document.getElementById('input-tvm-PYR').value")
            user_fv_input = await eval_js("document.getElementById('input-tvm-FV').value")

            print(f"app.tvm.PYR preservado: {user_pyr} (Esperado: 1, NÃO sobrescrito por 12)")
            print(f"app.tvm.FV preservado: {user_fv} (Esperado: 2500, NÃO sobrescrito por 0)")
            print(f"app.tvm.N preservado: {user_n} (Esperado: 36)")
            print(f"app.tvm.isBegin preservado: {user_begin} (Esperado: True -> BEG mode)")
            print(f"Input P/YR no formulário: '{user_pyr_input}' (Esperado: '1')")
            print(f"Input FV no formulário: '{user_fv_input}' (Esperado: '2500.0000')")

            assert user_pyr == 1, f"Valor de P/YR do usuário foi sobrescrito! Obteve {user_pyr}"
            assert user_fv == 2500, f"Valor de FV do usuário foi sobrescrito! Obteve {user_fv}"
            assert user_n == 36, f"Valor de N do usuário foi alterado!"
            assert user_begin is True, f"Modo BEG do usuário foi alterado!"
            assert user_pyr_input == "1"
            assert user_fv_input == "2500.0000"
            print("=> CENÁRIO 2 PASSOU: DADOS PREVIAMENTE PREENCHIDOS PELO USUÁRIO FORAM PRESERVADOS!")

            print("\n=== CENÁRIO 3: Restauração para Padrões de Fábrica (Reset) ===")
            await eval_js("app.resetToFactoryDefaults(false)")
            await eval_js("app.switchTab('TVM')")
            
            reset_pyr = await eval_js("app.tvm.PYR")
            reset_fv = await eval_js("app.tvm.FV")
            reset_begin = await eval_js("app.tvm.isBegin")
            reset_pyr_inp = await eval_js("document.getElementById('input-tvm-PYR').value")
            reset_fv_inp = await eval_js("document.getElementById('input-tvm-FV').value")

            print(f"Após Reset - P/YR: {reset_pyr} (Esperado: 12)")
            print(f"Após Reset - FV: {reset_fv} (Esperado: 0)")
            print(f"Após Reset - isBegin: {reset_begin} (Esperado: False)")
            print(f"Após Reset - Input P/YR: '{reset_pyr_inp}'")
            print(f"Após Reset - Input FV: '{reset_fv_inp}'")

            assert reset_pyr == 12, "Reset não restaurou P/YR para 12!"
            assert reset_fv == 0, "Reset não restaurou FV para 0!"
            assert reset_begin is False, "Reset não restaurou modo para END!"
            assert reset_pyr_inp == "12"
            assert reset_fv_inp == "0.0000"
            print("=> CENÁRIO 3 PASSOU COM SUCESSO!")

            print("\n=======================================================")
            print("TODOS OS TESTES DE VALORES PADRÃO DO MANUAL PASSARAM!")
            print("=======================================================")

    finally:
        try:
            proc.terminate()
            proc.wait(timeout=2)
        except Exception:
            pass

if __name__ == '__main__':
    asyncio.run(run_tests())
