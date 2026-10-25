# -*- coding: utf-8 -*-
"""
test_fase4.py
Automated CDP test suite for Fase 4 (Alphanumeric Input & Dynamic Equation Solver)
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

    port = 9228
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

    print(f"Iniciando Edge headless para testar Fase 4 em {html_file}...")
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

            for _ in range(50):
                is_ready = await eval_js("typeof window.app !== 'undefined'")
                if is_ready:
                    break
                await asyncio.sleep(0.1)

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

            print("\n--- TESTE 1: Ativação do Menu ALPHA no Visor LCD ---")
            await eval_js("app.startAlphaEditor();")
            check("Menu atual é ALPHA", await eval_js("app.currentMenu"), "ALPHA")
            labels_alpha = await get_labels()
            check("Softkeys iniciais de ALPHA", labels_alpha, ['A-E', 'F-J', 'K-O', 'P-T', 'U-Z', 'OUTR'])

            print("\n--- TESTE 2: Submenus de Letras do Teclado ALPHA ---")
            # F1 entra no bloco A-E
            await eval_js("app.pressSoftkey(0);")
            labels_ae = await get_labels()
            check("Softkeys do bloco A-E", labels_ae, ['A', 'B', 'C', 'D', 'E', 'ALPH'])

            # F1 digita 'A'
            await eval_js("app.pressSoftkey(0);")
            check("alphaBuffer contém 'A'", await eval_js("app.alphaBuffer"), "A")

            # F6 volta para os blocos principais
            await eval_js("app.pressSoftkey(5);")
            labels_back = await get_labels()
            check("F6 volta para blocos principais", labels_back, ['A-E', 'F-J', 'K-O', 'P-T', 'U-Z', 'OUTR'])

            print("\n--- TESTE 3: Criação de Equação Dinâmica via ALPHA ---")
            # Configurar buffer para LUCRO = VENDA - CUSTO e comitar via INPUT
            await eval_js("app.alphaBuffer = 'LUCRO = VENDA - CUSTO';")
            await eval_js("app.commitAlphaEquation();")

            check("Menu volta para SOLVE", await eval_js("app.currentMenu"), "SOLVE")
            var_names = await eval_js("app.solve.varNames")
            check("Variáveis extraídas", var_names, ['LUCRO', 'VENDA', 'CUSTO'])

            labels_solve = await get_labels()
            check("Softkeys do Solver com as variáveis e NOVA", labels_solve, ['LUCRO', 'VENDA', 'CUSTO', 'NOVA', 'F5', 'MAIN'])

            print("\n--- TESTE 4: Resolução Numérica da Equação Customizada ---")
            # Definir VENDA = 300
            await eval_js("app.setResult(300); app.entry.isEntering = true; app.entry.buffer = '300'; app.pressSoftkey(1);")
            check("VENDA armazenado com 300", await eval_js("app.solve.vars.VENDA"), 300)

            # Definir CUSTO = 200
            await eval_js("app.setResult(200); app.entry.isEntering = true; app.entry.buffer = '200'; app.pressSoftkey(2);")
            check("CUSTO armazenado com 200", await eval_js("app.solve.vars.CUSTO"), 200)

            # Resolver para LUCRO (F1 sem digitar)
            await eval_js("app.entry.isEntering = false; app.pressSoftkey(0);")
            check("Solver calcula LUCRO = 100", await eval_js("app.solve.vars.LUCRO"), 100, approx=True)

            # Resolver inversamente: mudar LUCRO = 150 e calcular VENDA
            await eval_js("app.setResult(150); app.entry.isEntering = true; app.entry.buffer = '150'; app.pressSoftkey(0);")
            check("LUCRO atualizado para 150", await eval_js("app.solve.vars.LUCRO"), 150)

            # Resolver VENDA (F2 sem digitar)
            await eval_js("app.entry.isEntering = false; app.pressSoftkey(1);")
            check("Solver calcula VENDA = 350", await eval_js("app.solve.vars.VENDA"), 350, approx=True)

            print("\n--- TESTE 5: Criação Rápida de Equação Financeira (JUROS = PV * I * N / 100) ---")
            await eval_js("app.createCustomFormula('JUROS = PV * I * N / 100');")
            check("Variáveis da fórmula de Juros", await eval_js("app.solve.varNames"), ['JUROS', 'PV', 'I', 'N'])

            # PV = 1000, I = 5, N = 2 -> JUROS = 100
            await eval_js("app.solve.vars = {PV: 1000, I: 5, N: 2, JUROS: null};")
            await eval_js("app.solveForVariable('JUROS');")
            check("Solver calcula JUROS = 100", await eval_js("app.solve.vars.JUROS"), 100, approx=True)

            # PV = null, JUROS = 100, I = 5, N = 2 -> PV = 1000
            await eval_js("app.solve.vars = {PV: null, JUROS: 100, I: 5, N: 2};")
            await eval_js("app.solveForVariable('PV');")
            check("Solver calcula PV = 1000 a partir dos Juros", await eval_js("app.solve.vars.PV"), 1000, approx=True)

            print("\n--- TESTE 6: Elementos da Interface da Workstation para ALPHA ---")
            btn_alpha_exists = await eval_js("Boolean(document.getElementById('btn-open-alpha'))")
            check("Botão 'Digitar Equação no Visor (ALPHA)' presente", btn_alpha_exists, True)

            input_quick_exists = await eval_js("Boolean(document.getElementById('input-quick-equation'))")
            check("Input de equação rápida presente", input_quick_exists, True)

            print(f"\n==========================================")
            print(f"RESULTADO FINAL FASE 4: {tests_passed}/{total_tests} testes passaram com sucesso!")
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
