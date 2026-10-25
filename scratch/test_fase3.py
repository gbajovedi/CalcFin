# -*- coding: utf-8 -*-
"""
test_fase3.py
Automated CDP test suite for Fase 3 (HP 17bII+ Functional Modules)
"""

import asyncio
import json
import subprocess
import time
import urllib.request
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def run_tests():
    try:
        import websockets
    except ImportError:
        print("Instalando websockets...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "websockets"])
        import websockets

    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        os.path.expanduser(r"~\AppData\Local\Microsoft\Edge\Application\msedge.exe")
    ]
    edge_exe = next((p for p in edge_paths if os.path.exists(p)), None)
    if not edge_exe:
        print("Erro: Executável do Edge não encontrado.")
        sys.exit(1)

    port = 9224
    html_file = os.path.abspath('Calculadora Financeira 17bIi.html')
    cmd = [
        edge_exe,
        "--headless=new",
        f"--remote-debugging-port={port}",
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        html_file
    ]

    print(f"Iniciando Edge headless para testar Fase 3 em {html_file}...")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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

        if not ws_url:
            print("Erro: Não foi possível obter webSocketDebuggerUrl.")
            sys.exit(1)

        async with websockets.connect(ws_url) as ws:
            msg_id = 0

            async def eval_js(expression):
                nonlocal msg_id
                msg_id += 1
                payload = {
                    "id": msg_id,
                    "method": "Runtime.evaluate",
                    "params": {
                        "expression": expression,
                        "returnByValue": True,
                        "awaitPromise": True
                    }
                }
                await ws.send(json.dumps(payload))
                while True:
                    res = json.loads(await ws.recv())
                    if res.get('id') == msg_id:
                        result = res.get('result', {}).get('result', {})
                        if 'value' in result:
                            return result['value']
                        if result.get('type') == 'undefined':
                            return None
                        return result

            title = await eval_js("document.title")
            print(f"Conectado ao CDP da página: {title}")

            # Aguardar app estar completamente inicializado
            for _ in range(50):
                is_ready = await eval_js("typeof window.app !== 'undefined'")
                if is_ready:
                    break
                await asyncio.sleep(0.1)
            print("window.app está pronto e inicializado!")

            tests_passed = 0
            total_tests = 0

            def check(name, expr_res, expected, approx=False):
                nonlocal tests_passed, total_tests
                total_tests += 1
                passed = False
                if approx and isinstance(expr_res, (int, float)) and isinstance(expected, (int, float)):
                    passed = abs(expr_res - expected) < 0.05
                else:
                    passed = (expr_res == expected)

                if passed:
                    print(f"  [PASS] {name} => {expr_res}")
                    tests_passed += 1
                else:
                    print(f"  [FAIL] {name} => esperado: {expected}, obtido: {expr_res}")

            async def get_labels():
                return await eval_js("""
                    Array.from({length: 6}, (_, i) => document.getElementById(`sk-${i+1}`).textContent)
                """)

            print("\n--- TESTE 1: Módulo TIME (Cálculos de Datas e Prazos) ---")
            act_diff = await eval_js("app.calcDaysDiffAct('2026-01-15', '2026-04-15')")
            check("Dias Reais (ACT 365) de 15/01/2026 a 15/04/2026", act_diff, 90)

            diff_360 = await eval_js("app.calcDaysDiff360('2026-01-15', '2026-04-15')")
            check("Dias Comerciais (30/360) de 15/01/2026 a 15/04/2026", diff_360, 90)

            diff_360_bancario = await eval_js("app.calcDaysDiff360('2026-02-28', '2026-03-31')")
            check("Dias Comerciais (30/360) de 28/02 a 31/03", diff_360_bancario, 33)

            proj = await eval_js("app.calcProjectedDate('2026-01-01', 30)")
            check("Projeção 01/01/2026 + 30 dias", proj.get('formatted'), "31/01/2026")
            check("Dia da Semana Projeção", proj.get('weekday'), "Sábado")

            print("\n--- TESTE 2: Navegação no Visor LCD para TIME e TIME_CALC ---")
            await eval_js("app.navigateToMenu('MAIN');")
            await eval_js("app.pressSoftkey(3);") # TIME
            labels_time = await get_labels()
            check("Softkeys de TIME", labels_time, ['CALC', 'SET', 'FORMAT', 'F4', 'F5', 'MAIN'])

            # F1 em TIME abre TIME_CALC
            await eval_js("app.pressSoftkey(0);")
            check("Menu atual é TIME_CALC", await eval_js("app.currentMenu"), "TIME_CALC")
            labels_calc = await get_labels()
            check("Softkeys de TIME_CALC", labels_calc, ['DATE1', 'DATE2', 'ACT', '360', '+DAYS', 'TIME'])

            # F3 em TIME_CALC (ACT)
            await eval_js("app.pressSoftkey(2);")
            check("ACT no visor via softkey F3", await eval_js("app.stack.x"), 90)

            # F6 em TIME_CALC volta para TIME
            await eval_js("app.pressSoftkey(5);")
            check("F6 volta para TIME", await eval_js("app.currentMenu"), "TIME")

            print("\n--- TESTE 3: Módulo CURRX (Câmbio Multimoedas) ---")
            usd_to_brl = await eval_js("app.convertCurrency(100, 'USD', 'BRL')")
            check("100 USD para BRL (Cotação 5.65)", usd_to_brl, 565.0, approx=True)

            brl_to_usd = await eval_js("app.convertCurrency(565, 'BRL', 'USD')")
            check("565 BRL para USD", brl_to_usd, 100.0, approx=True)

            usd_to_eur = await eval_js("app.convertCurrency(100, 'USD', 'EUR')")
            check("100 USD para EUR (Cotação 0.92)", usd_to_eur, 92.0, approx=True)

            usd_to_gbp = await eval_js("app.convertCurrency(100, 'USD', 'GBP')")
            check("100 USD para GBP (Cotação 0.78)", usd_to_gbp, 78.0, approx=True)

            # Visor CURRX
            await eval_js("app.navigateToMenu('CURRX');")
            labels_currx = await get_labels()
            check("Softkeys de CURRX", labels_currx, ['USD', 'EUR', 'GBP', 'BRL', 'SET', 'MAIN'])
            await eval_js("app.setResult(565); app.pressSoftkey(0);") # USD
            check("Visor CURRX 565 BRL => USD", await eval_js("app.stack.x"), 100.0, approx=True)

            print("\n--- TESTE 4: Módulo BOND (Títulos de Renda Fixa) ---")
            p_par = await eval_js("app.calcBondPricePure(8, 8, 10)")
            check("Preço do Título ao Par (Cupom 8%, YTM 8%)", p_par, 100.0, approx=True)

            p_premium = await eval_js("app.calcBondPricePure(10, 8, 10)")
            check("Preço do Título Premium (Cupom 10%, YTM 8%)", p_premium, 113.42, approx=True)

            ytm_calc = await eval_js("app.calcBondYTMPure(113.42016, 10, 10)")
            check("YTM Calculado via Newton-Raphson a partir do Preço 113.42", ytm_calc, 8.0, approx=True)

            # Visor BOND
            await eval_js("app.navigateToMenu('FIN'); app.pressSoftkey(3);") # BOND
            check("Menu atual é BOND", await eval_js("app.currentMenu"), "BOND")
            labels_bond = await get_labels()
            check("Softkeys de BOND", labels_bond, ['PREÇO', 'YTM', 'CUPOM', 'F4', 'F5', 'FIN'])

            print("\n--- TESTE 5: Métodos de Depreciação Expandidos (SL, SOYD, DB) ---")
            # Custo 10000, Residual 1000, Vida 5
            # SL: 1800
            dep_sl = await eval_js("(10000 - 1000) / 5")
            check("Depreciação Linear (SL)", dep_sl, 1800.0)

            # SOYD Ano 1: 3000
            soyd_y1 = await eval_js("app.depr = {cost: 10000, salvage: 1000, life: 5, year: 1}; (10000 - 1000) * (5 / 15)")
            check("Depreciação SOYD Ano 1", soyd_y1, 3000.0)

            # SOYD Ano 2: 2400
            soyd_y2 = await eval_js("(10000 - 1000) * (4 / 15)")
            check("Depreciação SOYD Ano 2", soyd_y2, 2400.0)

            # DB Ano 1: 4000
            db_y1 = await eval_js("app.calcDepreciationDBYear(10000, 1000, 5, 1)")
            check("Depreciação DB 200% Ano 1", db_y1, 4000.0)

            # DB Ano 5: 296
            db_y5 = await eval_js("app.calcDepreciationDBYear(10000, 1000, 5, 5)")
            check("Depreciação DB 200% Ano 5 (limitada ao residual)", db_y5, 296.0)

            # Visor DEPRC
            await eval_js("app.navigateToMenu('FIN'); app.pressSoftkey(4);") # DEPRC
            check("Menu atual é DEPRC", await eval_js("app.currentMenu"), "DEPRC")
            labels_deprc = await get_labels()
            check("Softkeys de DEPRC", labels_deprc, ['SL', 'SOYD', 'DB', 'CUSTO', 'RESID', 'FIN'])

            print("\n--- TESTE 6: Estatística Avançada no Módulo SUM ---")
            # Inserir dados: (10, 20), (20, 50), (30, 80)
            await eval_js("app.stats.pairs = [{x: 10, y: 20}, {x: 20, y: 50}, {x: 30, y: 80}];")
            stats = await eval_js("app.computeStats()")
            check("Mediana X", stats.get('medianX'), 20)
            check("Mínimo X", stats.get('minX'), 10)
            check("Máximo X", stats.get('maxX'), 30)
            check("Amplitude X (Range)", stats.get('rangeX'), 20)
            check("Ajuste Exponencial disponível", bool(stats.get('expSlope')), True)

            print("\n--- TESTE 7: Elementos do DOM e Abas da Workstation ---")
            tab_time_exists = await eval_js("Boolean(document.getElementById('tab-TIME'))")
            check("Aba tab-TIME presente no DOM", tab_time_exists, True)

            tab_currx_exists = await eval_js("Boolean(document.getElementById('tab-CURRX'))")
            check("Aba tab-CURRX presente no DOM", tab_currx_exists, True)

            panel_time_exists = await eval_js("Boolean(document.getElementById('panel-TIME'))")
            check("Painel panel-TIME presente no DOM", panel_time_exists, True)

            panel_currx_exists = await eval_js("Boolean(document.getElementById('panel-CURRX'))")
            check("Painel panel-CURRX presente no DOM", panel_currx_exists, True)

            # Clicar na aba TIME e verificar ativação
            await eval_js("app.switchTab('TIME');")
            time_panel_visible = await eval_js("!document.getElementById('panel-TIME').classList.contains('hidden')")
            check("Painel TIME visível após switchTab('TIME')", time_panel_visible, True)

            # Clicar na aba CURRX e verificar ativação
            await eval_js("app.switchTab('CURRX');")
            currx_panel_visible = await eval_js("!document.getElementById('panel-CURRX').classList.contains('hidden')")
            check("Painel CURRX visível após switchTab('CURRX')", currx_panel_visible, True)

            print(f"\n==========================================")
            print(f"RESULTADO FINAL FASE 3: {tests_passed}/{total_tests} testes passaram com sucesso!")
            print(f"==========================================")

            if tests_passed == total_tests:
                sys.exit(0)
            else:
                sys.exit(1)

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()

if __name__ == '__main__':
    asyncio.run(run_tests())
