# -*- coding: utf-8 -*-
import hashlib

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. tvm object declaration default values (FV: 0, PYR: 12, isBegin: false)
    t1_old = """            tvm: {
                N: null,
                I: null,
                PV: null,
                PMT: null,
                FV: null,
                PYR: null,
                isBegin: false
            },"""

    t1_new = """            tvm: {
                N: null,
                I: null,
                PV: null,
                PMT: null,
                FV: 0,
                PYR: 12,
                isBegin: false
            },"""
    assert t1_old in content, f"t1_old not found in {filepath}"
    content = content.replace(t1_old, t1_new)
    print(f"Updated default tvm object in {filepath}")

    # 2. HTML input-tvm-FV initial value
    t2_old = """<input type="text" inputmode="decimal" maxlength="18" autocomplete="off" spellcheck="false" id="input-tvm-FV" placeholder="Insira os dados" value="" """
    t2_new = """<input type="text" inputmode="decimal" maxlength="18" autocomplete="off" spellcheck="false" id="input-tvm-FV" placeholder="Insira os dados" value="0,0000" """
    assert t2_old in content, f"t2_old not found in {filepath}"
    content = content.replace(t2_old, t2_new)
    print(f"Updated input-tvm-FV initial markup in {filepath}")

    # 3. HTML input-tvm-PYR initial value
    t3_old = """<input type="text" inputmode="numeric" maxlength="3" autocomplete="off" spellcheck="false" id="input-tvm-PYR" placeholder="Insira os dados" value="" """
    t3_new = """<input type="text" inputmode="numeric" maxlength="3" autocomplete="off" spellcheck="false" id="input-tvm-PYR" placeholder="Insira os dados" value="12" """
    assert t3_old in content, f"t3_old not found in {filepath}"
    content = content.replace(t3_old, t3_new)
    print(f"Updated input-tvm-PYR initial markup in {filepath}")

    # 4. loadWorkspaceState: preserve user's saved JSON values, default to manual standards if undefined
    t4_old = """                        const isLegacyDemoTvm = state.tvm.N === 12 && state.tvm.I === 12 && state.tvm.PV === -10000 && state.tvm.PMT === 0 && state.tvm.FV === 0;
                        if (isLegacyDemoTvm) {
                            this.tvm = { N: null, I: null, PV: null, PMT: null, FV: null, PYR: 12, isBegin: !!state.tvm.isBegin };
                        } else {
                            Object.assign(this.tvm, {
                                N: (state.tvm.N !== null && state.tvm.N !== undefined && state.tvm.N !== '') ? Number(state.tvm.N) : null,
                                I: (state.tvm.I !== null && state.tvm.I !== undefined && state.tvm.I !== '') ? Number(state.tvm.I) : null,
                                PV: (state.tvm.PV !== null && state.tvm.PV !== undefined && state.tvm.PV !== '') ? Number(state.tvm.PV) : null,
                                PMT: (state.tvm.PMT !== null && state.tvm.PMT !== undefined && state.tvm.PMT !== '') ? Number(state.tvm.PMT) : null,
                                FV: (state.tvm.FV !== null && state.tvm.FV !== undefined && state.tvm.FV !== '') ? Number(state.tvm.FV) : null,
                                PYR: (state.tvm && state.tvm.PYR) ? Number(state.tvm.PYR) : null,
                                isBegin: !!state.tvm.isBegin
                            });
                        }"""

    t4_new = """                        const isLegacyDemoTvm = state.tvm.N === 12 && state.tvm.I === 12 && state.tvm.PV === -10000 && state.tvm.PMT === 0 && state.tvm.FV === 0;
                        if (isLegacyDemoTvm) {
                            this.tvm = { N: null, I: null, PV: null, PMT: null, FV: 0, PYR: 12, isBegin: !!state.tvm.isBegin };
                        } else {
                            Object.assign(this.tvm, {
                                N: (state.tvm.N !== null && state.tvm.N !== undefined && state.tvm.N !== '') ? Number(state.tvm.N) : null,
                                I: (state.tvm.I !== null && state.tvm.I !== undefined && state.tvm.I !== '') ? Number(state.tvm.I) : null,
                                PV: (state.tvm.PV !== null && state.tvm.PV !== undefined && state.tvm.PV !== '') ? Number(state.tvm.PV) : null,
                                PMT: (state.tvm.PMT !== null && state.tvm.PMT !== undefined && state.tvm.PMT !== '') ? Number(state.tvm.PMT) : null,
                                FV: (state.tvm.FV !== null && state.tvm.FV !== undefined && state.tvm.FV !== '') ? Number(state.tvm.FV) : (state.tvm.FV === null ? null : 0),
                                PYR: (state.tvm.PYR !== null && state.tvm.PYR !== undefined && state.tvm.PYR !== '') ? Number(state.tvm.PYR) : (state.tvm.PYR === null ? null : 12),
                                isBegin: !!state.tvm.isBegin
                            });
                        }"""
    assert t4_old in content, f"t4_old not found in {filepath}"
    content = content.replace(t4_old, t4_new)
    print(f"Updated loadWorkspaceState in {filepath}")

    # 5. resetAll factory defaults
    t5_old = """this.tvm = { N: null, I: null, PV: null, PMT: null, FV: null, PYR: null, isBegin: false };"""
    t5_new = """this.tvm = { N: null, I: null, PV: null, PMT: null, FV: 0, PYR: 12, isBegin: false };"""
    assert t5_old in content, f"t5_old not found in {filepath}"
    content = content.replace(t5_old, t5_new)
    print(f"Updated resetAll in {filepath}")

    # Ensure CRLF line endings
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
