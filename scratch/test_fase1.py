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
PORT = 9227
HTML_FILE = os.path.abspath("Calculadora Financeira 17bIi.html")

async def run_tests():
    import websockets

    print(f"Iniciando Edge headless para testar {HTML_FILE}...")
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

            print("\n--- TESTE 1: Inicialização e Estrutura dos Registradores R0-R9 ---")
            await eval_js("app.setMode('RPN'); app.clearRegisters(); app.pressKey('CLR');")
            reg_len = await eval_js("app.registers.length")
            check("10 registradores presentes", reg_len, 10)
            reg_zero = await eval_js("app.registers.every(r => r === 0)")
            check("Registradores inicializados com 0", reg_zero, True)

            print("\n--- TESTE 2: Tecla STO direta (STO 1 = 123.45, STO 2 = 50) ---")
            await eval_js("app.setResult(123.45); app.pressKey('STO'); app.pressDigit('1');")
            check("app.registers[1] == 123.45", await eval_js("app.registers[1]"), 123.45)
            await eval_js("app.setResult(50); app.pressKey('STO'); app.pressDigit('2');")
            check("app.registers[2] == 50", await eval_js("app.registers[2]"), 50)

            print("\n--- TESTE 3: Aritmética de Registrador (STO +, STO -, STO *, STO /) ---")
            # STO + 1: adicionar 10 ao registrador 1 (123.45 + 10 = 133.45)
            await eval_js("app.setResult(10); app.pressKey('STO'); app.pressOp('+'); app.pressDigit('1');")
            check("STO + 1 => 133.45", await eval_js("app.registers[1]"), 133.45)

            # STO - 2: subtrair 20 do registrador 2 (50 - 20 = 30)
            await eval_js("app.setResult(20); app.pressKey('STO'); app.pressOp('-'); app.pressDigit('2');")
            check("STO - 2 => 30", await eval_js("app.registers[2]"), 30)

            # STO * 2: multiplicar registrador 2 por 3 (30 * 3 = 90)
            await eval_js("app.setResult(3); app.pressKey('STO'); app.pressOp('*'); app.pressDigit('2');")
            check("STO * 2 => 90", await eval_js("app.registers[2]"), 90)

            # STO / 2: dividir registrador 2 por 2 (90 / 2 = 45)
            await eval_js("app.setResult(2); app.pressKey('STO'); app.pressOp('/'); app.pressDigit('2');")
            check("STO / 2 => 45", await eval_js("app.registers[2]"), 45)

            print("\n--- TESTE 4: Tecla RCL (RCL 1 e RCL 2) ---")
            await eval_js("app.pressKey('CLR'); app.pressKey('RCL'); app.pressDigit('1');")
            check("RCL 1 coloca 133.45 no visor X", await eval_js("app.stack.x"), 133.45)
            await eval_js("app.pressKey('CLR'); app.pressKey('RCL'); app.pressDigit('2');")
            check("RCL 2 coloca 45 no visor X", await eval_js("app.stack.x"), 45)

            print("\n--- TESTE 5: Tecla RND (Shift + RCL) ---")
            await eval_js("app.setDecimals(2); app.stack.x = 3.14159265; app.toggleShift(); app.pressKey('RCL');")
            check("RND arredonda X para 2 casas (3.14)", await eval_js("app.stack.x"), 3.14)

            print("\n--- TESTE 6: Tecla SHOW (Shift + .) ---")
            await eval_js("app.stack.x = 1234567.89012; app.toggleShift(); app.pressDot();")
            line2_show = await eval_js("document.getElementById('lcdLine2').textContent")
            check("SHOW exibe valor completo sem arredondamento", "1234567,89012" in line2_show or "1234567.89012" in line2_show, True)

            print("\n--- TESTE 7: Tecla MEM (Shift + 0) ---")
            await eval_js("app.toggleShift(); app.pressDigit('0');")
            line1_mem = await eval_js("document.getElementById('lcdLine1').textContent")
            line2_mem = await eval_js("document.getElementById('lcdLine2').textContent")
            check("MEM no LCD linha 1", "MEM: 10 REG DISP" in line1_mem, True)
            check("MEM no LCD linha 2", "LIVRE: 100%" in line2_mem, True)

            print("\n--- TESTE 8: Tecla E (Shift + +/-) Notação Científica ---")
            await eval_js("app.pressKey('CLR'); app.pressDigit('1'); app.pressDot(); app.pressDigit('2'); app.pressDigit('5'); app.toggleShift(); app.pressKey('+/-'); app.pressDigit('6');")
            val_sci = await eval_js("app.getDisplayValue()")
            check("1.25E6 interpretado como 1250000", val_sci, 1250000)

            print("\n--- TESTE 9: LAST X (Shift + =) ---")
            # 10 ENTER 2 / => 5, LAST X deve ser 2
            await eval_js("app.pressKey('CLR'); app.setResult(10); app.pressEnter(); app.pressDigit('2'); app.pressOp('/');")
            check("Divisão 10 / 2 = 5", await eval_js("app.stack.x"), 5)
            await eval_js("app.toggleShift(); app.pressEnter();")
            check("LAST X recupera o divisor 2", await eval_js("app.stack.x"), 2)

            print("\n--- TESTE 10: RPN Stack Drop e Duplicação do Topo T ---")
            # Configurar pilha: T=1, Z=2, Y=3, X=4
            await eval_js("app.pressKey('CLR'); app.stack.t = 1; app.stack.z = 2; app.stack.y = 3; app.stack.x = 4;")
            await eval_js("app.pressOp('+');")
            # X = 3 + 4 = 7, Y = 2, Z = 1, T = 1 (T duplicado e preservado!)
            check("RPN binária: X = 7", await eval_js("app.stack.x"), 7)
            check("RPN stack drop: Y = 2", await eval_js("app.stack.y"), 2)
            check("RPN stack drop: Z = 1", await eval_js("app.stack.z"), 1)
            check("RPN stack drop: T preservado = 1", await eval_js("app.stack.t"), 1)

            print("\n--- TESTE 11: RPN Roll Down (DOWN) e Roll Up (UP) ---")
            # Pilha: T=1, Z=2, Y=3, X=4
            await eval_js("app.pressKey('CLR'); app.stack.t = 1; app.stack.z = 2; app.stack.y = 3; app.stack.x = 4;")
            await eval_js("app.pressKey('DOWN');")
            # Roll Down: X recebe Y(3), Y recebe Z(2), Z recebe T(1), T recebe X antigo(4)
            check("Roll Down: X = 3", await eval_js("app.stack.x"), 3)
            check("Roll Down: T = 4", await eval_js("app.stack.t"), 4)
            await eval_js("app.pressKey('UP');")
            # Roll Up volta ao estado anterior
            check("Roll Up: X = 4", await eval_js("app.stack.x"), 4)
            check("Roll Up: T = 1", await eval_js("app.stack.t"), 1)

            print("\n--- TESTE 12: Modo Algébrico com Parênteses (Manual HP Pág. 16: (3+4)*(5+6)=77) ---")
            await eval_js("app.setMode('ALG'); app.pressKey('CLR');")
            # ( 3 + 4 )
            await eval_js("app.pressKey('('); app.pressDigit('3'); app.pressOp('+'); app.pressDigit('4'); app.pressKey(')');")
            check("Parêntese 1 resolvido: X = 7", await eval_js("app.stack.x"), 7)
            # * ( 5 + 6 ) =
            await eval_js("app.pressOp('*'); app.pressKey('('); app.pressDigit('5'); app.pressOp('+'); app.pressDigit('6'); app.pressKey(')'); app.pressEnter();")
            check("(3+4)*(5+6) = 77", await eval_js("app.stack.x"), 77)

            print("\n--- TESTE 13: Parênteses Aninhados em ALG: ((2+3)*4)+1 = 21 ---")
            await eval_js("app.pressKey('CLR');")
            await eval_js("app.pressKey('('); app.pressKey('('); app.pressDigit('2'); app.pressOp('+'); app.pressDigit('3'); app.pressKey(')'); app.pressOp('*'); app.pressDigit('4'); app.pressKey(')'); app.pressOp('+'); app.pressDigit('1'); app.pressEnter();")
            check("((2+3)*4)+1 = 21", await eval_js("app.stack.x"), 21)

            print("\n--- TESTE 14: Grid de Registradores no DOM ---")
            await eval_js("app.switchTab('TAPE');")
            grid_cards = await eval_js("document.querySelectorAll('#tape-registers-grid > div').length")
            check("Grid de registradores possui 10 cartões no DOM", grid_cards, 10)

            print(f"\n==========================================")
            print(f"RESULTADO FINAL: {tests_passed}/{total_tests} testes passaram com sucesso!")
            print(f"==========================================")
            return tests_passed == total_tests

    finally:
        proc.terminate()
        proc.wait()

if __name__ == '__main__':
    ok = asyncio.run(run_tests())
    exit(0 if ok else 1)
