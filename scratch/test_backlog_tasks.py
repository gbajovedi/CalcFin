# -*- coding: utf-8 -*-
import os, subprocess, json, time, urllib.request, asyncio, sys
sys.stdout.reconfigure(encoding='utf-8')

async def run_tests():
    import websockets
    edge_bin = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    html_path = os.path.abspath("Calculadora Financeira 17bIi.html")
    file_url = "file:" + urllib.request.pathname2url(html_path)
    port = 9270

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

            print("\n=== TESTE 1: Remoção de Botões Redundantes (TVM & CFLO) ===")
            has_tvm_clear = await eval_js("Boolean(document.querySelector('#panel-TVM button[onclick*=\"clearTvmModule\"]'))")
            has_cflo_clear = await eval_js("Boolean(document.querySelector('#panel-CFLO button[onclick*=\"clearCfloModule\"]'))")
            has_main_clear = await eval_js("Boolean(document.getElementById('module-clear-fields-btn'))")
            
            print(f"Botão Limpar TVM no #panel-TVM: {has_tvm_clear} (Esperado: False)")
            print(f"Botão Limpar CFLO no #panel-CFLO: {has_cflo_clear} (Esperado: False)")
            print(f"Botão unificado Limpar Campos na barra superior: {has_main_clear} (Esperado: True)")
            
            assert not has_tvm_clear, "Botão redundante Limpar TVM ainda existe no #panel-TVM!"
            assert not has_cflo_clear, "Botão redundante Limpar CFLO ainda existe no #panel-CFLO!"
            assert has_main_clear, "Botão principal Limpar Campos não encontrado no toolbar!"
            print("=> TESTE 1 PASSOU COM SUCESSO!")

            print("\n=== TESTE 2: Categoria 'Personalizadas' no Dropdown de Categorias ===")
            cat_options = await eval_js("Array.from(document.getElementById('solve-library-category').options).map(o => o.value)")
            print(f"Opções disponíveis no dropdown de categorias: {cat_options}")
            assert 'Personalizadas' in cat_options, "'Personalizadas' não está nas opções do dropdown de categorias!"
            print("=> TESTE 2 PASSOU COM SUCESSO!")

            print("\n=== TESTE 3: Criação de Fórmula Personalizada e Persistência ===")
            create_res = await eval_js("app.createCustomFormula('MARGEM = (PRECO - CUSTO) / PRECO * 100')")
            print(f"Resultado createCustomFormula: {create_res}")
            assert create_res is True, "Falha ao criar fórmula personalizada!"

            # Verificar no array de fórmulas
            custom_form = await eval_js("app.formulas.find(f => f.category === 'Personalizadas')")
            print(f"Fórmula criada encontrada: {custom_form.get('id')} - {custom_form.get('title')} ({custom_form.get('category')})")
            assert custom_form is not None, "Fórmula personalizada não encontrada em app.formulas!"
            assert custom_form.get('category') == 'Personalizadas', "Categoria da fórmula não é 'Personalizadas'!"
            assert custom_form.get('isCustom') is True, "isCustom não é True!"

            # Verificar no localStorage
            ls_raw = await eval_js("localStorage.getItem('hp17bii-custom-formulas')")
            print(f"localStorage['hp17bii-custom-formulas']: {ls_raw}")
            assert ls_raw and 'MARGEM' in ls_raw, "Fórmula não persistida no localStorage!"

            # Verificar Card no DOM
            card_badge = await eval_js(f"document.querySelector('.formula-card[data-formula-id=\"{custom_form['id']}\"] .custom-formula-badge')?.textContent")
            card_del_btn = await eval_js(f"Boolean(document.querySelector('.formula-card[data-formula-id=\"{custom_form['id']}\"] .custom-formula-delete-btn'))")
            print(f"Badge do Card: '{card_badge}' (Esperado: 'USUÁRIO')")
            print(f"Botão de Deletar no Card: {card_del_btn} (Esperado: True)")
            assert card_badge == 'USUÁRIO', f"Badge inesperado: '{card_badge}'"
            assert card_del_btn is True, "Botão de exclusão não encontrado no card da fórmula personalizada!"

            # Verificar que fórmulas nativas NÃO têm botão de exclusão
            native_del_btn = await eval_js("Boolean(document.querySelector('.formula-card[data-formula-id=\"coef_financiamento_carencia_premio\"] .custom-formula-delete-btn'))")
            print(f"Botão de Deletar em fórmula nativa: {native_del_btn} (Esperado: False)")
            assert native_del_btn is False, "Fórmula de fábrica não deve ter botão de exclusão!"

            print("\n=== TESTE 4: Filtragem pelo dropdown de 'Personalizadas' ===")
            await eval_js("document.getElementById('solve-library-category').value = 'Personalizadas'; app.filterCatalog();")
            count_text = await eval_js("document.getElementById('solve-library-count').textContent.trim()")
            print(f"Contagem com filtro 'Personalizadas': {count_text}")
            assert "1 de" in count_text or "1 fórmula" in count_text, f"Esperado 1 fórmula visível, obteve: {count_text}"

            print("\n=== TESTE 5: Exclusão de Fórmula Personalizada ===")
            custom_id = custom_form['id']
            # Simular confirmação no window.confirm
            await eval_js("window.confirm = () => true;")
            # Clicar no botão de exclusão do card
            await eval_js(f"document.querySelector('.formula-card[data-formula-id=\"{custom_id}\"] .custom-formula-delete-btn').click()")
            
            # Verificar se foi removida de app.formulas
            after_deleted_form = await eval_js(f"Boolean(app.formulas.find(f => f.id === '{custom_id}'))")
            print(f"Fórmula ainda existe em app.formulas após exclusão: {after_deleted_form} (Esperado: False)")
            assert not after_deleted_form, "Fórmula ainda encontrada em app.formulas!"

            # Verificar se foi removida de localStorage
            ls_after = await eval_js("localStorage.getItem('hp17bii-custom-formulas')")
            print(f"localStorage após exclusão: {ls_after}")
            assert ls_after == "[]", f"localStorage não está vazio: {ls_after}"

            # Verificar se o card sumiu do DOM
            card_exists = await eval_js(f"Boolean(document.querySelector('.formula-card[data-formula-id=\"{custom_id}\"]'))")
            print(f"Card existe no DOM após exclusão: {card_exists} (Esperado: False)")
            assert not card_exists, "Card ainda existe no DOM após exclusão!"

            # Resetar filtro para conferir fallback ativo
            await eval_js("document.getElementById('solve-library-category').value = ''; app.filterCatalog();")
            active_id = await eval_js("app.solve.activeFormulaId")
            print(f"Fórmula ativa após exclusão: {active_id}")
            assert active_id != custom_id, "Fórmula ativa ainda aponta para fórmula excluída!"

            print("\n=== TESTE 6: Tentativa Inválida de Excluir Fórmula Nativa ===")
            await eval_js("app.deleteCustomFormula('coef_financiamento_carencia_premio')")
            lcd_err = await eval_js("document.getElementById('lcdLine1').textContent")
            print(f"Mensagem no visor LCD ao tentar excluir nativa: '{lcd_err}'")
            assert "Apenas fórmulas personalizadas podem ser excluídas" in lcd_err, f"Erro inesperado: '{lcd_err}'"

            print("\n=== TODOS OS 6 TESTES DE BACKLOG FORAM EXECUTADOS COM SUCESSO! ===")

    finally:
        try:
            proc.terminate()
            proc.wait(timeout=2)
        except Exception:
            pass

if __name__ == '__main__':
    asyncio.run(run_tests())
