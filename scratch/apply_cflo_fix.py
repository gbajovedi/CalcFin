# -*- coding: utf-8 -*-
import hashlib

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update onclick on button
    btn_target = """onclick="app.clearActiveModule('CFLO')\""""
    btn_replacement = """onclick="app.clearCfloModule()\""""
    if btn_target in content:
        content = content.replace(btn_target, btn_replacement)
        print(f"Updated CFLO button onclick in {filepath}")

    # 2. Add clearCfloModule and clearActiveModule to app
    code_target = """            clearCfloResults() {"""
    code_replacement = """            clearCfloModule() {
                const ids = ['input-cflo-rate', 'cflo-new-amount'];
                ids.forEach(id => { const el = document.getElementById(id); if (el) el.value = ''; });
                this.cflo = [];
                this.renderCashFlows();
                this.clearCfloResults();
                const msg = document.getElementById('cflo-add-feedback');
                if (msg) msg.textContent = '';
                const result = document.getElementById('result-panel');
                if (result) result.classList.add('hidden');
                this.setModuleActionFeedback('Fluxos de caixa (CFLO) e resultados limpos com sucesso.', 'info');
            },

            clearActiveModule(moduleName) {
                if (moduleName === 'CFLO') {
                    this.clearCfloModule();
                } else if (moduleName === 'TVM') {
                    this.clearTvmModule();
                } else {
                    this.clearActiveModuleFields();
                }
            },

            clearCfloResults() {"""

    if code_target in content:
        content = content.replace(code_target, code_replacement, 1)
        print(f"Added clearCfloModule and clearActiveModule to {filepath}")
    else:
        print(f"WARNING: code target not found in {filepath}")

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

