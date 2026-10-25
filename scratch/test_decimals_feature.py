# -*- coding: utf-8 -*-
import os, subprocess, json, time, urllib.request, asyncio, sys
sys.stdout.reconfigure(encoding='utf-8')

async def test_decimals():
    import websockets
    edge_bin = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    html_path = os.path.abspath("Calculadora Financeira 17bIi.html")
    file_url = "file:" + urllib.request.pathname2url(html_path)
    port = 9265

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

            print("\n--- TESTE 1: Padrão Inicial de 4 Dígitos após a Vírgula ---")
            dec_val = await eval_js("app.decimals")
            badge_text = await eval_js("document.getElementById('lcdDecBadge').textContent.trim()")
            ind_text = await eval_js("document.getElementById('label-decimals-indicator').textContent.trim()")
            lcd2_text = await eval_js("document.getElementById('lcdLine2').textContent.trim()")
            print(f"app.decimals: {dec_val}")
            print(f"lcdDecBadge: '{badge_text}'")
            print(f"label-decimals-indicator: '{ind_text}'")
            print(f"lcdLine2: '{lcd2_text}'")
            assert dec_val == 4, f"Esperado decimals=4, obteve {dec_val}"
            assert badge_text == "4 DEC", f"Esperado '4 DEC', obteve '{badge_text}'"
            assert ind_text == "4 casas", f"Esperado '4 casas', obteve '{ind_text}'"
            assert lcd2_text == "0,0000", f"Esperado '0,0000', obteve '{lcd2_text}'"

            print("\n--- TESTE 2: Aumentar Casas Decimais (+ button) ---")
            await eval_js("document.getElementById('btn-dec-increase').click()")
            dec_inc = await eval_js("app.decimals")
            ind_inc = await eval_js("document.getElementById('label-decimals-indicator').textContent.trim()")
            badge_inc = await eval_js("document.getElementById('lcdDecBadge').textContent.trim()")
            lcd2_inc = await eval_js("document.getElementById('lcdLine2').textContent.trim()")
            print(f"Após incremento: {dec_inc} (Ind: '{ind_inc}', Badge: '{badge_inc}', LCD: '{lcd2_inc}')")
            assert dec_inc == 5, f"Esperado 5, obteve {dec_inc}"
            assert ind_inc == "5 casas", f"Esperado '5 casas', obteve '{ind_inc}'"
            assert badge_inc == "5 DEC", f"Esperado '5 DEC', obteve '{badge_inc}'"
            assert lcd2_inc == "0,00000", f"Esperado '0,00000', obteve '{lcd2_inc}'"

            print("\n--- TESTE 3: Diminuir Casas Decimais (− button) ---")
            await eval_js("document.getElementById('btn-dec-decrease').click()")
            await eval_js("document.getElementById('btn-dec-decrease').click()")
            dec_dec = await eval_js("app.decimals")
            ind_dec = await eval_js("document.getElementById('label-decimals-indicator').textContent.trim()")
            badge_dec = await eval_js("document.getElementById('lcdDecBadge').textContent.trim()")
            print(f"Após 2 decrementos: {dec_dec} (Ind: '{ind_dec}', Badge: '{badge_dec}')")
            assert dec_dec == 3, f"Esperado 3, obteve {dec_dec}"
            assert ind_dec == "3 casas", f"Esperado '3 casas', obteve '{ind_dec}'"
            assert badge_dec == "3 DEC", f"Esperado '3 DEC', obteve '{badge_dec}'"

            print("\n--- TESTE 4: Limite Mínimo (0 casas) ---")
            await eval_js("app.setDecimals(0)")
            dec_zero = await eval_js("app.decimals")
            ind_zero = await eval_js("document.getElementById('label-decimals-indicator').textContent.trim()")
            btn_dec_disabled = await eval_js("document.getElementById('btn-dec-decrease').disabled")
            print(f"Com 0 casas: {dec_zero} (Ind: '{ind_zero}', Botão − desabilitado: {btn_dec_disabled})")
            assert dec_zero == 0
            assert ind_zero == "0 casas"
            assert btn_dec_disabled == True

            print("\n--- TESTE 5: Retorno para 4 Casas Decimais ---")
            await eval_js("app.setDecimals(4)")
            assert await eval_js("app.decimals") == 4
            assert await eval_js("document.getElementById('label-decimals-indicator').textContent.trim()") == "4 casas"

            print("\n==========================================")
            print("TODOS OS TESTES DO CONTROLE DE CASAS DECIMAIS PASSARAM COM SUCESSO!")
            print("==========================================")

    finally:
        proc.kill()

if __name__ == "__main__":
    asyncio.run(test_decimals())
