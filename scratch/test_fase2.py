# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import time
import json
import urllib.request
import asyncio

sys.stdout.reconfigure(encoding='utf-8')

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 9228
HTML_FILE = os.path.abspath("Calculadora Financeira 17bIi.html")

async def run_tests():
    import websockets

    print(f"Iniciando Edge headless para testar Fase 2 em {HTML_FILE}...")
    file_url = "file:" + urllib.request.pathname2url(HTML_FILE)
    cmd = [
        EDGE_PATH,
        "--headless=new",
        f"--remote-debugging-port={PORT}",
        "--no-first-run",
        "--disable-gpu",
        file_url
    ]
    proc = subprocess.Popen(cmd)

    try:
        await asyncio.sleep(2)
        req = urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json")
        targets = json.loads(req.read().decode())
        page_targets = [t for t in targets if t.get("type") == "page"]
        if not page_targets:
            raise RuntimeError("Nenhuma página encontrada no Edge!")
        ws_url = page_targets[0]["webSocketDebuggerUrl"]
        print(f"Conectado ao CDP da página: {page_targets[0]['title']}")

        async with websockets.connect(ws_url) as ws:
            async def eval_js(expr):
                msg_id = int(time.time() * 1000) % 1000000
                await ws.send(json.dumps({
                    "id": msg_id,
                    "method": "Runtime.evaluate",
                    "params": {"expression": expr, "returnByValue": True, "awaitPromise": True}
                }))
                while True:
                    rep = json.loads(await ws.recv())
                    if rep.get("id") == msg_id:
                        result = rep.get("result", {}).get("result", {})
                        if "value" in result:
                            return result["value"]
                        elif "description" in result:
                            return result["description"]
                        return rep

            tests_passed = 0
            total_tests = 0

            def check(name, expr_res, expected):
                nonlocal tests_passed, total_tests
                total_tests += 1
                if expr_res == expected:
                    print(f"  [PASS] {name} => {expr_res}")
                    tests_passed += 1
                else:
                    print(f"  [FAIL] {name} => esperado: {expected}, obtido: {expr_res}")

            async def get_labels():
                return await eval_js("""
                    Array.from({length: 6}, (_, i) => document.getElementById(`sk-${i+1}`).textContent)
                """)

            print("\n--- TESTE 1: Menu Principal Oficial (MAIN) ---")
            await eval_js("app.pressKey('EXIT'); app.toggleShift(); app.pressKey('EXIT');")
            labels_main = await get_labels()
            check("Softkeys do Menu MAIN", labels_main, ['FIN', 'BUS', 'SUM', 'TIME', 'SOLVE', 'CURRX'])

            print("\n--- TESTE 2: Navegação Hierárquica MAIN -> FIN -> TVM -> TVM_OTHER ---")
            # F1 em MAIN abre FIN
            await eval_js("app.pressSoftkey(0);")
            check("Menu atual é FIN", await eval_js("app.currentMenu"), "FIN")
            labels_fin = await get_labels()
            check("Softkeys do Menu FIN", labels_fin, ['TVM', 'ICNV', 'CFLO', 'BOND', 'DEPRC', 'MAIN'])

            # F1 em FIN abre TVM
            await eval_js("app.pressSoftkey(0);")
            check("Menu atual é TVM", await eval_js("app.currentMenu"), "TVM")
            labels_tvm = await get_labels()
            check("Softkeys do Menu TVM (com OTHER na F6)", labels_tvm, ['N', 'I%YR', 'PV', 'PMT', 'FV', 'OTHER'])

            # F6 em TVM abre TVM_OTHER
            await eval_js("app.pressSoftkey(5);")
            check("Menu atual é TVM_OTHER", await eval_js("app.currentMenu"), "TVM_OTHER")
            labels_other = await get_labels()
            check("Softkeys de TVM_OTHER", labels_other, ['P/YR', 'BEG', 'END', 'RESET', 'F5', 'AMRT'])

            print("\n--- TESTE 3: Retorno Suave com a Tecla EXIT (Menu Stack) ---")
            # EXIT em TVM_OTHER deve voltar para TVM
            await eval_js("app.pressKey('EXIT');")
            check("EXIT em TVM_OTHER volta para TVM", await eval_js("app.currentMenu"), "TVM")

            # EXIT em TVM deve voltar para FIN
            await eval_js("app.pressKey('EXIT');")
            check("EXIT em TVM volta para FIN", await eval_js("app.currentMenu"), "FIN")

            # EXIT em FIN deve voltar para MAIN
            await eval_js("app.pressKey('EXIT');")
            check("EXIT em FIN volta para MAIN", await eval_js("app.currentMenu"), "MAIN")

            print("\n--- TESTE 4: Atalho Direto Shift + EXIT (MAIN) ---")
            # Entrar até TVM_OTHER
            await eval_js("app.pressSoftkey(0); app.pressSoftkey(0); app.pressSoftkey(5);")
            check("Em TVM_OTHER", await eval_js("app.currentMenu"), "TVM_OTHER")
            # Shift + EXIT pula direto para MAIN
            await eval_js("app.toggleShift(); app.pressKey('EXIT');")
            check("Shift + EXIT vai direto para MAIN", await eval_js("app.currentMenu"), "MAIN")

            print("\n--- TESTE 5: Funções de TVM_OTHER (BEG, END, P/YR) ---")
            await eval_js("app.navigateToMenu('TVM_OTHER');")
            await eval_js("app.pressSoftkey(1);") # BEG
            check("BEG ativa modo Antecipado", await eval_js("app.tvm.isBegin"), True)
            await eval_js("app.pressSoftkey(2);") # END
            check("END ativa modo Postecipado", await eval_js("app.tvm.isBegin"), False)

            print("\n--- TESTE 6: Menu Comercial (BUS) e Submenu %CHG ---")
            await eval_js("app.navigateToMenu('MAIN'); app.pressSoftkey(1);") # BUS
            labels_bus = await get_labels()
            check("Softkeys do Menu BUS", labels_bus, ['%CHG', '%TOTL', 'MU%C', 'MU%P', 'F5', 'MAIN'])
            # Entrar em %CHG
            await eval_js("app.pressSoftkey(0);")
            labels_pchg = await get_labels()
            check("Softkeys de BUS %CHG", labels_pchg, ['OLD', 'NEW', '%CHG', 'F4', 'F5', 'BUS'])
            # Definir OLD = 100, NEW = 150 -> calcular %CHG
            await eval_js("app.setResult(100); app.pressSoftkey(0);") # OLD = 100
            await eval_js("app.setResult(150); app.pressSoftkey(1);") # NEW = 150
            await eval_js("app.pressSoftkey(2);") # %CHG
            check("Cálculo %CHG ((150-100)/100)*100 = 50%", await eval_js("app.stack.x"), 50)
            # F6 volta para BUS
            await eval_js("app.pressSoftkey(5);")
            check("F6 em %CHG volta para BUS", await eval_js("app.currentMenu"), "BUS")

            print("\n--- TESTE 7: Menu Estatística (SUM) ---")
            await eval_js("app.navigateToMenu('MAIN'); app.pressSoftkey(2);") # SUM
            labels_sum = await get_labels()
            check("Softkeys de SUM", labels_sum, ['Σ+', 'Σ-', 'TOTAL', 'MEAN', 'SDEV', 'MAIN'])
            # Limpar lista e adicionar dados: 10, 20, 30
            await eval_js("app.stats.pairs = [];")
            await eval_js("app.setResult(10); app.pressSoftkey(0);")
            await eval_js("app.setResult(20); app.pressSoftkey(0);")
            await eval_js("app.setResult(30); app.pressSoftkey(0);")
            check("n = 3 itens adicionados", await eval_js("app.stats.pairs.length"), 3)
            # Total F3 (Σx = 60)
            await eval_js("app.pressSoftkey(2);")
            check("TOTAL Σx = 60", await eval_js("app.stack.x"), 60)
            # Média F4 (MEAN = 20)
            await eval_js("app.pressSoftkey(3);")
            check("MEAN = 20", await eval_js("app.stack.x"), 20)
            # Desvio padrão F5 (SDEV = 10)
            await eval_js("app.pressSoftkey(4);")
            check("SDEV = 10", await eval_js("app.stack.x"), 10)

            print("\n--- TESTE 8: Menu Matemático (MATH via Shift + %) ---")
            await eval_js("app.toggleShift(); app.pressKey('%');")
            labels_math = await get_labels()
            check("Softkeys de MATH", labels_math, ['LOG', '10^x', 'LN', 'EXP', 'N!', 'PI'])
            # LOG(100) = 2
            await eval_js("app.setResult(100); app.pressSoftkey(0);")
            check("LOG(100) = 2", await eval_js("app.stack.x"), 2)
            # 10^3 = 1000
            await eval_js("app.setResult(3); app.pressSoftkey(1);")
            check("10^3 = 1000", await eval_js("app.stack.x"), 1000)
            # EXP(0) = 1
            await eval_js("app.setResult(0); app.pressSoftkey(3);")
            check("EXP(0) = 1", await eval_js("app.stack.x"), 1)
            # 5! = 120
            await eval_js("app.setResult(5); app.pressSoftkey(4);")
            check("5! = 120", await eval_js("app.stack.x"), 120)
            # PI = 3.14159...
            await eval_js("app.pressSoftkey(5);")
            check("PI é aproximadamente 3.14159", round(await eval_js("app.stack.x"), 4), 3.1416)

            print("\n--- TESTE 9: Menus de Ajuste DSP e MODES ---")
            # DSP via tecla DSP
            await eval_js("app.pressKey('DSP');")
            labels_dsp = await get_labels()
            check("Softkeys de DSP", labels_dsp, ['FIX', 'ALL', '.', ',', 'F5', 'MAIN'])
            # MODES via Shift + DSP
            await eval_js("app.toggleShift(); app.pressKey('DSP');")
            labels_modes = await get_labels()
            check("Softkeys de MODES", labels_modes, ['BEEP', 'PRNT', 'DBL', 'ALG', 'RPN', 'MAIN'])
            # Alternar para ALG via F4
            await eval_js("app.pressSoftkey(3);")
            check("MODES: Modo alterado para ALG", await eval_js("app.mode"), "ALG")
            # Alternar para RPN via F5
            await eval_js("app.pressSoftkey(4);")
            check("MODES: Modo alterado para RPN", await eval_js("app.mode"), "RPN")

            print("\n--- TESTE 10: Menu Câmbio (CURRX) ---")
            await eval_js("app.navigateToMenu('MAIN'); app.pressSoftkey(5);") # CURRX
            labels_currx = await get_labels()
            check("Softkeys de CURRX", labels_currx, ['USD', 'EUR', 'GBP', 'BRL', 'SET', 'MAIN'])
            # Converter R$ 565 para USD (cotação base 5.65 -> 100 USD)
            await eval_js("app.setResult(565); app.pressSoftkey(0);")
            check("Conversão R$ 565 para USD = US$ 100", await eval_js("app.stack.x"), 100)

            print(f"\n==========================================")
            print(f"RESULTADO FINAL FASE 2: {tests_passed}/{total_tests} testes passaram com sucesso!")
            print(f"==========================================")
            return tests_passed == total_tests

    finally:
        proc.terminate()
        proc.wait()

if __name__ == '__main__':
    ok = asyncio.run(run_tests())
    exit(0 if ok else 1)

