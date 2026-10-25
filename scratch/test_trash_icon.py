# -*- coding: utf-8 -*-
import os, subprocess, json, time, urllib.request, asyncio, sys
sys.stdout.reconfigure(encoding='utf-8')

async def run_trash_tests():
    import websockets
    edge_bin = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    html_path = os.path.abspath("Calculadora Financeira 17bIi.html")
    file_url = "file:" + urllib.request.pathname2url(html_path)
    port = 9420

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

        assert ws_url, "Failed to connect to headless Edge"

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

            print("\n=== TESTE 1: Criando Fórmula Personalizada ===")
            await eval_js("app.setMobileView('tools')")
            await eval_js("app.createCustomFormula('LUCRO_LIQ = RECEITA - DESPESAS')")
            custom_id = await eval_js("app.formulas.find(f => f.category === 'Personalizadas').id")
            print(f"Fórmula customizada criada com id: {custom_id}")

            print("\n=== TESTE 2: Verificando Existência e Dimensões do Ícone de Lixeira ===")
            del_btn_exists = await eval_js("Boolean(document.querySelector('.custom-formula-delete-btn'))")
            svg_width = await eval_js("document.querySelector('.custom-formula-delete-btn svg').getBoundingClientRect().width")
            svg_height = await eval_js("document.querySelector('.custom-formula-delete-btn svg').getBoundingClientRect().height")
            print(f"Delete button existe: {del_btn_exists}")
            print(f"SVG largura calculada: {svg_width}px, altura: {svg_height}px")
            assert del_btn_exists, "Botão de lixeira não encontrado!"
            assert svg_width >= 16 and svg_height >= 16, f"Dimensões do SVG inválidas: {svg_width}x{svg_height}"

            print("\n=== TESTE 3: Verificando Posição: Lixeira à ESQUERDA da Estrela ===")
            rel_pos = await eval_js("""(() => {
                const card = document.querySelector('.formula-card[data-formula-id="' + '""" + custom_id + """' + '"]');
                const del = card.querySelector('.custom-formula-delete-btn');
                const star = card.querySelector('.favorite-star-btn');
                const delRect = del.getBoundingClientRect();
                const starRect = star.getBoundingClientRect();
                const isPreviousSibling = star.previousElementSibling === del;
                const isLeft = delRect.left < starRect.left;
                return { isPreviousSibling, isLeft, delLeft: delRect.left, starLeft: starRect.left };
            })()""")
            print(f"Posição relativa: {rel_pos}")
            assert rel_pos['isLeft'], f"Lixeira NÃO está à esquerda da estrela! delLeft={rel_pos['delLeft']}, starLeft={rel_pos['starLeft']}"
            assert rel_pos['isPreviousSibling'], "Lixeira não é elemento anterior à estrela no DOM!"
            print("=> TESTE DE POSICIONAMENTO PASSOU: Lixeira está à esquerda da estrela de favorito!")

            print("\n=== TESTE 4: Cores no MODO ESCURO ===")
            await eval_js("app.applyTheme('dark')")
            await asyncio.sleep(0.3)
            dark_color = await eval_js("window.getComputedStyle(document.querySelector('.custom-formula-delete-btn')).color")
            print(f"Cor computada no modo escuro: {dark_color}")
            # rgb(248, 113, 113) / rgb(248, 112, 112) é #f87171
            assert "248, 11" in dark_color or "239, 68, 68" in dark_color, f"Cor escura inesperada: {dark_color}"

            print("\n=== TESTE 5: Cores no MODO CLARO ===")
            await eval_js("app.applyTheme('light')")
            await asyncio.sleep(0.4)
            light_color = await eval_js("window.getComputedStyle(document.querySelector('.custom-formula-delete-btn')).color")
            print(f"Cor computada no modo claro: {light_color}")
            # rgb(220, 38, 38) é #dc2626
            assert "220," in light_color or "185," in light_color, f"Cor clara inesperada: {light_color}"

            print("\n=== TESTE 6: Deleção Funcional via Clique ===")
            await eval_js("window.confirm = () => true;")
            await eval_js("document.querySelector('.custom-formula-delete-btn').click()")
            has_custom = await eval_js("Boolean(app.formulas.find(f => f.category === 'Personalizadas'))")
            print(f"Fórmula customizada ainda existe após clique: {has_custom}")
            assert not has_custom, "Fórmula não foi deletada após clique!"

            print("\n=== TODOS OS TESTES DO ÍCONE DE LIXEIRA PASSARAM COM SUCESSO! ===")

    finally:
        try:
            proc.terminate()
            proc.wait(timeout=2)
        except Exception:
            pass

if __name__ == '__main__':
    asyncio.run(run_trash_tests())

