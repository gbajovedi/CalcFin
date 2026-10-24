# -*- coding: utf-8 -*-
"""
Verification script for all 6 UI/UX TVM improvements via Headless Edge/CDP.
"""
import os
import subprocess
import json
import time
import urllib.request
import asyncio
import sys

async def run_tests():
    try:
        import websockets
    except ImportError:
        print("websockets not installed")
        return

    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    edge_bin = next((p for p in edge_paths if os.path.exists(p)), None)
    if not edge_bin:
        print("Edge binary not found")
        return

    html_path = os.path.abspath("Calculadora Financeira 17bIi.html")
    file_url = "file:" + urllib.request.pathname2url(html_path)
    port = 9226

    proc = subprocess.Popen([
        edge_bin,
        "--headless=new",
        f"--remote-debugging-port={port}",
        "--no-first-run",
        "--disable-gpu",
        file_url
    ])

    try:
        await asyncio.sleep(2)
        resp = urllib.request.urlopen(f"http://127.0.0.1:{port}/json")
        targets = json.loads(resp.read().decode())
        page_target = next((t for t in targets if t.get("type") == "page"), targets[0])
        ws_url = page_target["webSocketDebuggerUrl"]

        async with websockets.connect(ws_url) as ws:
            async def eval_js(expr):
                nonlocal ws
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

            # 1. Switch to TVM tab
            tab_status = await eval_js("""
                (() => {
                    app.switchTab('TVM');
                    return {
                        panelTvmHidden: document.getElementById('panel-TVM').classList.contains('hidden')
                    };
                })()
            """)
            print("Switched to TVM:", tab_status)

            # 2. Check units on all 6 cards
            units_check = await eval_js("""
                (() => {
                    const cards = [
                        ['N', 'períodos'],
                        ['I', '% a.a.'],
                        ['PV', 'R$'],
                        ['PMT', 'R$'],
                        ['FV', 'R$'],
                        ['PYR', 'pagtos/ano']
                    ];
                    return cards.map(([k, expected]) => {
                        const card = document.getElementById(k === 'PYR' ? 'card-tvm-PYR' : `card-tvm-${k}`);
                        const text = card ? (card.innerText || card.textContent || '') : '';
                        return { key: k, found: text.includes(expected), expected };
                    });
                })()
            """)
            print("Units Check:", units_check)
            all_units_ok = all(u["found"] for u in units_check)
            assert all_units_ok, f"Units failed: {units_check}"

            # 3. Check Segmented Control BGN/END
            seg_initial = await eval_js("""
                (() => {
                    const btnEnd = document.getElementById('btn-tvm-mode-end');
                    const btnBgn = document.getElementById('btn-tvm-mode-bgn');
                    const badge = document.getElementById('tvm-mode-badge');
                    return {
                        endActive: btnEnd.className.includes('bg-sky-600'),
                        bgnActive: btnBgn.className.includes('bg-amber-600'),
                        badge: badge.textContent,
                        appIsBegin: app.tvm.isBegin
                    };
                })()
            """)
            print("Segmented initial (END):", seg_initial)
            assert seg_initial["endActive"] and not seg_initial["bgnActive"] and "Postecipado" in seg_initial["badge"]

            # Click BGN
            await eval_js("app.setTvmMode(true)")
            seg_bgn = await eval_js("""
                (() => {
                    const btnEnd = document.getElementById('btn-tvm-mode-end');
                    const btnBgn = document.getElementById('btn-tvm-mode-bgn');
                    const badge = document.getElementById('tvm-mode-badge');
                    return {
                        endActive: btnEnd.className.includes('bg-sky-600'),
                        bgnActive: btnBgn.className.includes('bg-amber-600'),
                        badge: badge.textContent,
                        appIsBegin: app.tvm.isBegin
                    };
                })()
            """)
            print("Segmented switched (BGN):", seg_bgn)
            assert not seg_bgn["endActive"] and seg_bgn["bgnActive"] and "Antecipado" in seg_bgn["badge"]

            # Switch back to END
            await eval_js("app.setTvmMode(false)")

            # 4. Calculate a value (e.g. PMT) and verify side-by-side buttons
            await eval_js("""
                (() => {
                    document.getElementById('input-tvm-N').value = '12';
                    app.syncInputToState('tvm', 'N', '12');
                    document.getElementById('input-tvm-I').value = '12';
                    app.syncInputToState('tvm', 'I', '12');
                    document.getElementById('input-tvm-PV').value = '1000';
                    app.syncInputToState('tvm', 'PV', '1000');
                    document.getElementById('input-tvm-FV').value = '0';
                    app.syncInputToState('tvm', 'FV', '0');
                    app.calculateTVM('PMT');
                })()
            """)

            card_symmetry = await eval_js("""
                (() => {
                    const actionsPmt = document.getElementById('actions-tvm-PMT');
                    const btnPmt = document.getElementById('btn-tvm-PMT');
                    const copyPmt = document.getElementById('copy-tvm-PMT');
                    const rolePmt = document.getElementById('role-tvm-PMT');
                    const pmtVal = document.getElementById('input-tvm-PMT').value;
                    const rectBtn = btnPmt.getBoundingClientRect();
                    const rectCopy = copyPmt.getBoundingClientRect();

                    return {
                        pmtVal,
                        roleText: rolePmt.textContent,
                        actionsClass: actionsPmt.className,
                        btnText: btnPmt.textContent,
                        copyHidden: copyPmt.classList.contains('hidden'),
                        sideBySide: Math.abs(rectBtn.top - rectCopy.top) < 3
                    };
                })()
            """)
            print("Card Symmetry Check (PMT calculated):", json.dumps(card_symmetry, ensure_ascii=False))
            assert "grid-cols-2" in card_symmetry["actionsClass"]
            assert not card_symmetry["copyHidden"]
            assert card_symmetry["sideBySide"], f"Buttons are not side-by-side! {card_symmetry}"

            # 5. Check Amortization Table, Copy and CSV
            await eval_js("app.generateAmortizationTable()")
            amort_check = await eval_js("""
                (() => {
                    const rows = document.querySelectorAll('#amort-table-body tr');
                    const foot = document.getElementById('amort-table-foot');
                    const schedLen = app._currentAmortSchedule ? app._currentAmortSchedule.length : 0;
                    return {
                        rowCount: rows.length,
                        firstRow: rows[0] ? rows[0].innerText.replace(/\\s+/g, ' ') : '',
                        footVisible: !foot.classList.contains('hidden'),
                        footText: foot.innerText.replace(/\\s+/g, ' '),
                        schedLen
                    };
                })()
            """)
            print("Amortization Table Check:", json.dumps(amort_check, ensure_ascii=False))
            assert amort_check["schedLen"] == 12
            assert amort_check["footVisible"]

            # Test Copy Table with await
            copy_res = await eval_js("""
                (async () => {
                    const btn = document.getElementById('btn-copy-amort');
                    await app.copyAmortizationTable(btn);
                    const feedback = document.getElementById('module-action-feedback');
                    return {
                        feedback: feedback ? feedback.textContent : '',
                        btnText: btn.textContent
                    };
                })()
            """)
            print("Amortization Copy Check:", json.dumps(copy_res, ensure_ascii=False))
            assert "copiada" in copy_res["feedback"] or "✓" in copy_res["btnText"]

            # 6. Check Light Mode Table Header Contrast
            await eval_js("document.body.classList.add('light-mode')")
            header_contrast = await eval_js("""
                (() => {
                    const thead = document.querySelector('#panel-TVM table thead');
                    const th = thead.querySelector('th');
                    const styleThead = window.getComputedStyle(thead);
                    const styleTh = window.getComputedStyle(th);
                    return {
                        theadBg: styleThead.backgroundColor,
                        thColor: styleTh.color,
                        thFontWeight: styleTh.fontWeight
                    };
                })()
            """)
            print("Light Mode Header Contrast Check:", header_contrast)
            assert "241, 245, 249" in header_contrast["theadBg"], f"Unexpected bg: {header_contrast['theadBg']}"
            assert "15, 23, 42" in header_contrast["thColor"], f"Unexpected color: {header_contrast['thColor']}"

            # 7. Test Limpar TVM
            await eval_js("app.clearTvmModule()")
            clear_check = await eval_js("""
                (() => {
                    const inputs = ['N', 'I', 'PV', 'PMT', 'FV'].map(k => document.getElementById(`input-tvm-${k}`).value);
                    const pyr = document.getElementById('input-tvm-PYR').value;
                    const roles = ['N', 'I', 'PV', 'PMT', 'FV'].map(k => document.getElementById(`role-tvm-${k}`).textContent);
                    const actionsPmt = document.getElementById('actions-tvm-PMT');
                    const copyPmt = document.getElementById('copy-tvm-PMT');
                    const rows = document.querySelectorAll('#amort-table-body tr');
                    return {
                        inputsAllEmpty: inputs.every(v => v === ''),
                        pyr,
                        rolesAllDado: roles.every(r => r === 'Dado TVM'),
                        actionsClass: actionsPmt.className,
                        copyHidden: copyPmt.classList.contains('hidden'),
                        amortReset: rows.length === 1 && rows[0].innerText.includes('Clique em "Gerar Tabela"')
                    };
                })()
            """)
            print("Limpar TVM Check:", clear_check)
            assert clear_check["inputsAllEmpty"]
            assert clear_check["rolesAllDado"]
            assert "grid-cols-1" in clear_check["actionsClass"]
            assert clear_check["copyHidden"]
            assert clear_check["amortReset"]

            print("\n>>> ALL 6 UI/UX IMPROVEMENTS VERIFIED AND WORKING 100%! <<<")

    finally:
        proc.kill()

if __name__ == '__main__':
    asyncio.run(run_tests())

