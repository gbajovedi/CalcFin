import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('Calculadora Financeira 17bIi.html', encoding='utf-8') as f:
    text = f.read()

# 1. tvm object declaration
t1 = """            tvm: {
                N: null,
                I: null,
                PV: null,
                PMT: null,
                FV: null,
                PYR: null,
                isBegin: false
            },"""
print("t1 in text:", t1 in text)

# 2. HTML input-tvm-FV
t2 = """<input type="text" inputmode="decimal" maxlength="18" autocomplete="off" spellcheck="false" id="input-tvm-FV" placeholder="Insira os dados" value="" """
print("t2 in text:", t2 in text)

# 3. HTML input-tvm-PYR
t3 = """<input type="text" inputmode="numeric" maxlength="3" autocomplete="off" spellcheck="false" id="input-tvm-PYR" placeholder="Insira os dados" value="" """
print("t3 in text:", t3 in text)

# 4. loadWorkspaceState legacy demo
t4 = """                        const isLegacyDemoTvm = state.tvm.N === 12 && state.tvm.I === 12 && state.tvm.PV === -10000 && state.tvm.PMT === 0 && state.tvm.FV === 0;
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
print("t4 in text:", t4 in text)

# 5. resetAll
t5 = """this.tvm = { N: null, I: null, PV: null, PMT: null, FV: null, PYR: null, isBegin: false };"""
print("t5 in text:", t5 in text)

