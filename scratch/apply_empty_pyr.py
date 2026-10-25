# -*- coding: utf-8 -*-
import hashlib

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. HTML input-tvm-PYR
    old_input = """<input type="text" inputmode="numeric" maxlength="3" autocomplete="off" spellcheck="false" id="input-tvm-PYR" placeholder="Insira os dados" value="12" oninput="app.handleNumericInput(this, {allowNegative:false, allowDecimal:false, maxLength:3}); app.syncInputToState('tvm', 'PYR', this.value)" onblur="if(!this.value||parseInt(this.value,10)<1){this.value='12';app.syncInputToState('tvm','PYR','12');}" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-sm font-mono text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-sky-500/50">"""
    new_input = """<input type="text" inputmode="numeric" maxlength="3" autocomplete="off" spellcheck="false" id="input-tvm-PYR" placeholder="Insira os dados" value="" oninput="app.handleNumericInput(this, {allowNegative:false, allowDecimal:false, maxLength:3}); app.syncInputToState('tvm', 'PYR', this.value)" onblur="app.syncInputToState('tvm', 'PYR', this.value);" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-sm font-mono text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-sky-500/50">"""
    if old_input in content:
        content = content.replace(old_input, new_input)
        print(f"Updated HTML input in {filepath}")

    # 2. Initial state
    old_init = """            // TVM (Time Value of Money)
            tvm: {
                N: null,
                I: null,
                PV: null,
                PMT: null,
                FV: null,
                PYR: 12,
                isBegin: false
            },"""
    new_init = """            // TVM (Time Value of Money)
            tvm: {
                N: null,
                I: null,
                PV: null,
                PMT: null,
                FV: null,
                PYR: null,
                isBegin: false
            },"""
    assert old_init in content, f"old_init not found in {filepath}"
    content = content.replace(old_init, new_init)
    print(f"Updated initial state in {filepath}")

    # 3. calculateTVM P/YR validation
    old_calc_pyr = """                // 1. Ler e validar P/YR
                const pyrField = document.getElementById('input-tvm-PYR');
                let pyr = pyrField ? this.parseNumericValue(pyrField.value) : 12;
                if (!pyr || pyr <= 0) pyr = 12;
                this.tvm.PYR = pyr;
                if (pyrField && pyrField.value !== String(pyr)) pyrField.value = String(pyr);"""
    new_calc_pyr = """                // 1. Ler e validar P/YR (não auto-preenche 12 na interface)
                const pyrField = document.getElementById('input-tvm-PYR');
                const rawPyr = (pyrField && pyrField.value.trim() !== '') ? this.parseNumericValue(pyrField.value) : null;
                const pyr = (rawPyr && rawPyr > 0) ? rawPyr : 12;
                this.tvm.PYR = rawPyr;"""
    assert old_calc_pyr in content, f"old_calc_pyr not found in {filepath}"
    content = content.replace(old_calc_pyr, new_calc_pyr)
    print(f"Updated calculateTVM in {filepath}")

    # 4. clearTvmModule
    old_clear_pyr = """                this.tvm.PYR = 12;
                const pyr = document.getElementById('input-tvm-PYR');
                if (pyr) pyr.value = '12';"""
    new_clear_pyr = """                this.tvm.PYR = null;
                const pyr = document.getElementById('input-tvm-PYR');
                if (pyr) pyr.value = '';"""
    assert old_clear_pyr in content, f"old_clear_pyr not found in {filepath}"
    content = content.replace(old_clear_pyr, new_clear_pyr)
    print(f"Updated clearTvmModule in {filepath}")

    # 5. syncTvmInputsFromState
    old_sync_pyr = """                const pyrEl = document.getElementById('input-tvm-PYR');
                if (pyrEl && (force || document.activeElement !== pyrEl)) {
                    pyrEl.value = (this.tvm.PYR !== null && this.tvm.PYR !== undefined) ? this.tvm.PYR : 12;
                }"""
    new_sync_pyr = """                const pyrEl = document.getElementById('input-tvm-PYR');
                if (pyrEl && (force || document.activeElement !== pyrEl)) {
                    pyrEl.value = (this.tvm.PYR !== null && this.tvm.PYR !== undefined && this.tvm.PYR !== '') ? this.tvm.PYR : '';
                }"""
    assert old_sync_pyr in content, f"old_sync_pyr not found in {filepath}"
    content = content.replace(old_sync_pyr, new_sync_pyr)
    print(f"Updated syncTvmInputsFromState in {filepath}")

    # 6. clearActiveModuleFields
    old_ids = "TVM: ['input-tvm-N','input-tvm-I','input-tvm-PV','input-tvm-PMT','input-tvm-FV'],"
    new_ids = "TVM: ['input-tvm-N','input-tvm-I','input-tvm-PV','input-tvm-PMT','input-tvm-FV','input-tvm-PYR'],"
    if old_ids in content:
        content = content.replace(old_ids, new_ids)
        print(f"Updated clearActiveModuleFields in {filepath}")

    # 7. Workspace restore / reset
    old_res1 = "this.tvm = { N: null, I: null, PV: null, PMT: null, FV: null, PYR: 12, isBegin: false };"
    new_res1 = "this.tvm = { N: null, I: null, PV: null, PMT: null, FV: null, PYR: null, isBegin: false };"
    if old_res1 in content:
        content = content.replace(old_res1, new_res1)
        print(f"Updated reset tvm in {filepath}")

    old_res2 = "PYR: Number(state.tvm.PYR) || 12,"
    new_res2 = "PYR: (state.tvm && state.tvm.PYR) ? Number(state.tvm.PYR) : null,"
    if old_res2 in content:
        content = content.replace(old_res2, new_res2)
        print(f"Updated workspace restore in {filepath}")

    # Ensure CRLF
    content = content.replace('\r\n', '\n').replace('\n', '\r\n')

    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        f.write(content)

update_file("Calculadora Financeira 17bIi.html")
update_file("index.html")

# Check hashes
h1 = hashlib.sha256(open("Calculadora Financeira 17bIi.html", "rb").read()).hexdigest()
h2 = hashlib.sha256(open("index.html", "rb").read()).hexdigest()
print(f"SHA-256 Calculadora Financeira 17bIi.html: {h1}")
print(f"SHA-256 index.html:                       {h2}")
assert h1 == h2, "Hashes do not match!"
print("PARITY VERIFIED: Both files are 100% byte-for-byte identical!")
