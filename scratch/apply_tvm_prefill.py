# -*- coding: utf-8 -*-
import hashlib

def apply_changes():
    with open('Calculadora Financeira 17bIi.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. input-tvm-PYR markup
    target1 = 'id="input-tvm-PYR" placeholder="Insira os dados" value="12"'
    replacement1 = 'id="input-tvm-PYR" placeholder="Insira os dados" value="1"'
    assert target1 in content, "target1 not found"
    content = content.replace(target1, replacement1, 1)

    # 2. tvm initial state in app object
    target2 = '''            tvm: {
                N: null,
                I: null,
                PV: null,
                PMT: null,
                FV: 0,
                PYR: 12,
                isBegin: false
            },'''
    replacement2 = '''            tvm: {
                N: null,
                I: null,
                PV: null,
                PMT: null,
                FV: 0,
                PYR: 1,
                isBegin: false
            },'''
    assert target2 in content, "target2 not found"
    content = content.replace(target2, replacement2, 1)

    # 3. calculateTVM rawPyr fallback
    target3 = '''                const pyrField = document.getElementById('input-tvm-PYR');
                const rawPyr = (pyrField && pyrField.value.trim() !== '') ? this.parseNumericValue(pyrField.value) : null;
                const pyr = (rawPyr && rawPyr > 0) ? rawPyr : 12;
                this.tvm.PYR = rawPyr;'''
    replacement3 = '''                const pyrField = document.getElementById('input-tvm-PYR');
                const rawPyr = (pyrField && pyrField.value.trim() !== '') ? this.parseNumericValue(pyrField.value) : null;
                const pyr = (rawPyr && rawPyr > 0) ? rawPyr : 1;
                this.tvm.PYR = pyr;'''
    assert target3 in content, "target3 not found"
    content = content.replace(target3, replacement3, 1)

    # 4. generateAmortizationSchedule pyr
    target4 = 'const pyr = this.tvm.PYR || 12;'
    replacement4 = 'const pyr = this.tvm.PYR || 1;'
    assert target4 in content, "target4 not found"
    content = content.replace(target4, replacement4, 1)

    # 5. syncModuleToCalculator TVM tab
    target5 = '''                if (tabId === 'TVM') {
                    this.syncStateToInputs(false);
                    this.updateTvmLcdHeader();
                }'''
    replacement5 = '''                if (tabId === 'TVM') {
                    const inputFv = document.getElementById('input-tvm-FV');
                    const inputPyr = document.getElementById('input-tvm-PYR');
                    if (this.tvm.FV === null || this.tvm.FV === undefined || this.tvm.FV === '' || (inputFv && inputFv.value.trim() === '')) {
                        this.tvm.FV = 0;
                    }
                    if (this.tvm.PYR === null || this.tvm.PYR === undefined || this.tvm.PYR === '' || this.tvm.PYR === 12 || (inputPyr && (inputPyr.value.trim() === '' || inputPyr.value.trim() === '12'))) {
                        this.tvm.PYR = 1;
                    }
                    this.syncStateToInputs(false);
                    this.updateTvmLcdHeader();
                }'''
    assert target5 in content, "target5 not found"
    content = content.replace(target5, replacement5, 1)

    # 6. switchTab TVM handling
    target6 = '''                // Expande o catálogo automaticamente na aba Fórmulas (SOLVE) e recolhe nas demais abas
                this.toggleCatalog(tabId !== 'SOLVE');'''
    replacement6 = '''                // Pré-preenche FV=0 e P/YR=1 ao abrir a aba de matemática financeira
                if (tabId === 'TVM') {
                    const inputFv = document.getElementById('input-tvm-FV');
                    const inputPyr = document.getElementById('input-tvm-PYR');
                    if (this.tvm.FV === null || this.tvm.FV === undefined || this.tvm.FV === '' || (inputFv && inputFv.value.trim() === '')) {
                        this.tvm.FV = 0;
                        if (inputFv) inputFv.value = (0).toFixed(this.decimals !== undefined ? this.decimals : 4);
                    }
                    if (this.tvm.PYR === null || this.tvm.PYR === undefined || this.tvm.PYR === '' || this.tvm.PYR === 12 || (inputPyr && (inputPyr.value.trim() === '' || inputPyr.value.trim() === '12'))) {
                        this.tvm.PYR = 1;
                        if (inputPyr) inputPyr.value = '1';
                    }
                }

                // Expande o catálogo automaticamente na aba Fórmulas (SOLVE) e recolhe nas demais abas
                this.toggleCatalog(tabId !== 'SOLVE');'''
    assert target6 in content, "target6 not found"
    content = content.replace(target6, replacement6, 1)

    # 7. loadWorkspaceState
    target7 = '''                    if (state.tvm && typeof state.tvm === 'object') {
                        const isLegacyDemoTvm = state.tvm.N === 12 && state.tvm.I === 12 && state.tvm.PV === -10000 && state.tvm.PMT === 0 && state.tvm.FV === 0;
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
                        }
                    }'''
    replacement7 = '''                    if (state.tvm && typeof state.tvm === 'object') {
                        const isLegacyDemoTvm = state.tvm.N === 12 && state.tvm.I === 12 && state.tvm.PV === -10000 && state.tvm.PMT === 0 && state.tvm.FV === 0;
                        if (isLegacyDemoTvm) {
                            this.tvm = { N: null, I: null, PV: null, PMT: null, FV: 0, PYR: 1, isBegin: !!state.tvm.isBegin };
                        } else {
                            Object.assign(this.tvm, {
                                N: (state.tvm.N !== null && state.tvm.N !== undefined && state.tvm.N !== '') ? Number(state.tvm.N) : null,
                                I: (state.tvm.I !== null && state.tvm.I !== undefined && state.tvm.I !== '') ? Number(state.tvm.I) : null,
                                PV: (state.tvm.PV !== null && state.tvm.PV !== undefined && state.tvm.PV !== '') ? Number(state.tvm.PV) : null,
                                PMT: (state.tvm.PMT !== null && state.tvm.PMT !== undefined && state.tvm.PMT !== '') ? Number(state.tvm.PMT) : null,
                                FV: (state.tvm.FV !== null && state.tvm.FV !== undefined && state.tvm.FV !== '') ? Number(state.tvm.FV) : 0,
                                PYR: (state.tvm.PYR !== null && state.tvm.PYR !== undefined && state.tvm.PYR !== '' && state.tvm.PYR !== 12) ? Number(state.tvm.PYR) : 1,
                                isBegin: !!state.tvm.isBegin
                            });
                        }
                    }'''
    assert target7 in content, "target7 not found"
    content = content.replace(target7, replacement7, 1)

    # 8. resetToFactoryDefaults
    target8 = 'this.tvm = { N: null, I: null, PV: null, PMT: null, FV: 0, PYR: 12, isBegin: false };'
    replacement8 = 'this.tvm = { N: null, I: null, PV: null, PMT: null, FV: 0, PYR: 1, isBegin: false };'
    assert target8 in content, "target8 not found"
    content = content.replace(target8, replacement8, 1)

    # Save to Calculadora Financeira 17bIi.html
    # Ensure CRLF line endings
    content_crlf = content.replace('\r\n', '\n').replace('\n', '\r\n')
    with open('Calculadora Financeira 17bIi.html', 'wb') as f:
        f.write(content_crlf.encode('utf-8'))

    # Save identical copy to index.html
    with open('index.html', 'wb') as f:
        f.write(content_crlf.encode('utf-8'))

    h1 = hashlib.sha256(open('Calculadora Financeira 17bIi.html', 'rb').read()).hexdigest()
    h2 = hashlib.sha256(open('index.html', 'rb').read()).hexdigest()
    print(f"SHA-256 Calculadora Financeira 17bIi.html: {h1}")
    print(f"SHA-256 index.html:                       {h2}")
    assert h1 == h2, "Hashes do not match!"
    print("ALL REPLACEMENTS APPLIED SUCCESSFULLY AND HASHES MATCH!")

if __name__ == '__main__':
    apply_changes()
