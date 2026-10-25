# -*- coding: utf-8 -*-
"""
test_haptic.py
Automated CDP verification for dedicated haptic feedback toggle switch in mobile mode.
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

    port = 9229
    html_file = os.path.abspath('Calculadora Financeira 17bIi.html')
    cmd = [
        edge_exe,
        "--headless=new",
        f"--remote-debugging-port={port}",
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        "--window-size=1280,800",
        html_file
    ]

    print(f"Iniciando Edge headless para testar feedback tátil em {html_file}...")
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

            async def send_cmd(method, params=None):
                nonlocal msg_id, ws
                msg_id += 1
                req = {"id": msg_id, "method": method}
                if params:
                    req["params"] = params
                await ws.send(json.dumps(req))
                while True:
                    rep = json.loads(await ws.recv())
                    if rep.get("id") == msg_id:
                        return rep

            async def eval_js(expr):
                rep = await send_cmd("Runtime.evaluate", {
                    "expression": expr,
                    "returnByValue": True,
                    "awaitPromise": True
                })
                result = rep.get("result", {})
                if "exceptionDetails" in result:
                    raise Exception(result["exceptionDetails"])
                return result.get("result", {}).get("value")

            # Wait for app readiness
            for _ in range(30):
                ready = await eval_js("typeof window.app !== 'undefined' && typeof window.app.hapticFeedbackEnabled !== 'undefined'")
                if ready:
                    break
                await asyncio.sleep(0.2)

            passed = 0
            failed = 0

            def check(test_name, condition, details=""):
                nonlocal passed, failed
                if condition:
                    passed += 1
                    print(f"  [PASS] {test_name}")
                else:
                    failed += 1
                    print(f"  [FAIL] {test_name}: {details}")

            print("\n--- GRUPO 1: Elemento e Estado Inicial ---")
            exists = await eval_js("document.getElementById('haptic-toggle') !== null")
            check("Elemento #haptic-toggle existe no DOM", exists)

            initial_state = await eval_js("window.app.hapticFeedbackEnabled")
            check("Estado inicial hapticFeedbackEnabled é true", initial_state is True, f"Obtido: {initial_state}")

            aria_checked = await eval_js("document.getElementById('haptic-toggle').getAttribute('aria-checked')")
            check("Atributo aria-checked inicial é 'true'", aria_checked == "true", f"Obtido: {aria_checked}")

            print("\n--- GRUPO 2: Visibilidade Responsiva (Desktop vs Celular) ---")
            # In window size 1280x800, viewport width is >= 1024px.
            desktop_display = await eval_js("""
                (() => {
                    const el = document.getElementById('haptic-toggle');
                    return window.getComputedStyle(el).display;
                })()
            """)
            check("No desktop (>= 1024px), #haptic-toggle está oculto (display: none)", desktop_display == "none", f"Obtido: {desktop_display}")

            # Agora simula viewport de celular (390x844 - iPhone 14 / celular moderno)
            await send_cmd("Emulation.setDeviceMetricsOverride", {
                "width": 390,
                "height": 844,
                "deviceScaleFactor": 3,
                "mobile": True
            })
            await asyncio.sleep(0.3)

            mobile_display = await eval_js("""
                (() => {
                    const el = document.getElementById('haptic-toggle');
                    return window.getComputedStyle(el).display;
                })()
            """)
            check("No celular (390px), #haptic-toggle está visível (display: flex/inline-flex)", mobile_display in ["flex", "inline-flex"], f"Obtido: {mobile_display}")

            print("\n--- GRUPO 3: Alternância (Toggle) e Persistência localStorage ---")
            # Click on haptic-toggle
            await eval_js("document.getElementById('haptic-toggle').click()")
            toggled_state_1 = await eval_js("window.app.hapticFeedbackEnabled")
            aria_checked_1 = await eval_js("document.getElementById('haptic-toggle').getAttribute('aria-checked')")
            storage_1 = await eval_js("localStorage.getItem('calcfin_haptic_feedback')")
            check("Clique 1 desativa vibração (hapticFeedbackEnabled = false)", toggled_state_1 is False)
            check("Aria-checked atualizado para 'false'", aria_checked_1 == "false")
            check("LocalStorage salvo como 'false'", storage_1 == "false")

            # Click again
            await eval_js("document.getElementById('haptic-toggle').click()")
            toggled_state_2 = await eval_js("window.app.hapticFeedbackEnabled")
            aria_checked_2 = await eval_js("document.getElementById('haptic-toggle').getAttribute('aria-checked')")
            storage_2 = await eval_js("localStorage.getItem('calcfin_haptic_feedback')")
            check("Clique 2 reativa vibração (hapticFeedbackEnabled = true)", toggled_state_2 is True)
            check("Aria-checked atualizado para 'true'", aria_checked_2 == "true")
            check("LocalStorage salvo como 'true'", storage_2 == "true")

            print("\n--- GRUPO 4: Independência entre Som e Vibração ---")
            # Turn sound OFF, keep haptic ON
            await eval_js("window.app.mobileFeedbackEnabled = false; window.app.hapticFeedbackEnabled = true;")
            feedback_state = await eval_js("""
                (() => {
                    let hapticFired = false;
                    let soundFired = false;
                    const origHaptic = window.app.triggerHaptic;
                    const origSound = window.app.playKeyClick;
                    window.app.triggerHaptic = () => { hapticFired = true; };
                    window.app.playKeyClick = () => { soundFired = true; };
                    
                    // Força isMobileMode como true para o teste
                    const origIsMob = window.app.isMobileMode;
                    window.app.isMobileMode = () => true;
                    
                    window.app.triggerKeyFeedback();
                    
                    // Restaura
                    window.app.triggerHaptic = origHaptic;
                    window.app.playKeyClick = origSound;
                    window.app.isMobileMode = origIsMob;
                    
                    return { hapticFired, soundFired };
                })()
            """)
            check("Com som OFF e haptic ON: dispara apenas vibração", feedback_state.get("hapticFired") is True and feedback_state.get("soundFired") is False, f"Obtido: {feedback_state}")

            # Turn sound ON, turn haptic OFF
            await eval_js("window.app.mobileFeedbackEnabled = true; window.app.hapticFeedbackEnabled = false;")
            feedback_state2 = await eval_js("""
                (() => {
                    let hapticFired = false;
                    let soundFired = false;
                    const origHaptic = window.app.triggerHaptic;
                    const origSound = window.app.playKeyClick;
                    window.app.triggerHaptic = () => { hapticFired = true; };
                    window.app.playKeyClick = () => { soundFired = true; };
                    
                    const origIsMob = window.app.isMobileMode;
                    window.app.isMobileMode = () => true;
                    
                    window.app.triggerKeyFeedback();
                    
                    window.app.triggerHaptic = origHaptic;
                    window.app.playKeyClick = origSound;
                    window.app.isMobileMode = origIsMob;
                    
                    return { hapticFired, soundFired };
                })()
            """)
            check("Com som ON e haptic OFF: dispara apenas som", feedback_state2.get("hapticFired") is False and feedback_state2.get("soundFired") is True, f"Obtido: {feedback_state2}")

            # Restaura estados
            await eval_js("window.app.mobileFeedbackEnabled = true; window.app.hapticFeedbackEnabled = true;")

            print(f"\n==========================================")
            print(f"Total de testes: {passed + failed}")
            print(f"Passaram: {passed}")
            print(f"Falharam: {failed}")
            print(f"==========================================")

            if failed > 0:
                sys.exit(1)

    finally:
        try:
            proc.terminate()
            proc.wait(timeout=2)
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass

if __name__ == '__main__':
    asyncio.run(run_tests())
