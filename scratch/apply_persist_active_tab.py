# -*- coding: utf-8 -*-
import hashlib

def apply_changes():
    with open('Calculadora Financeira 17bIi.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update selectFormula signature and switchTab call
    target_sel = '''            selectFormula(formulaId, preserveVars = false) {'''
    replacement_sel = '''            selectFormula(formulaId, preserveVars = false, shouldSwitchTab = true) {'''
    assert target_sel in content, "target_sel not found"
    content = content.replace(target_sel, replacement_sel, 1)

    target_sel_end = '''                this.renderSolveVariables();
                this.renderCatalog();
                this.updateLCD();
                this.switchTab('SOLVE');
                this.saveWorkspaceState();
            },'''
    replacement_sel_end = '''                this.renderSolveVariables();
                this.renderCatalog();
                this.updateLCD();
                if (shouldSwitchTab) {
                    this.switchTab('SOLVE');
                    this.saveWorkspaceState();
                }
            },'''
    assert target_sel_end in content, "target_sel_end not found"
    content = content.replace(target_sel_end, replacement_sel_end, 1)

    # 2. Update init() to pass shouldSwitchTab = false
    target_init = '''                const hadSavedState = this.loadWorkspaceState();
                if (!hadSavedState) {
                    this.selectFormula('coef_financiamento_carencia_premio');
                    this.addTapeEntry('*** HP 17bII+ SILVER INICIADA ***');
                } else {
                    const formulaId = (this.solve && this.solve.activeFormulaId) ? this.solve.activeFormulaId : 'coef_financiamento_carencia_premio';
                    this.selectFormula(formulaId, true);
                    this.renderTape();
                }'''
    replacement_init = '''                const hadSavedState = this.loadWorkspaceState();
                if (!hadSavedState) {
                    this.selectFormula('coef_financiamento_carencia_premio', false, false);
                    this.addTapeEntry('*** HP 17bII+ SILVER INICIADA ***');
                } else {
                    const formulaId = (this.solve && this.solve.activeFormulaId) ? this.solve.activeFormulaId : 'coef_financiamento_carencia_premio';
                    this.selectFormula(formulaId, true, false);
                    this.renderTape();
                }'''
    assert target_init in content, "target_init not found"
    content = content.replace(target_init, replacement_init, 1)

    # 3. Update resetToFactoryDefaults to pass false
    target_reset = '''                this.selectFormula('coef_financiamento_carencia_premio');
                this.renderCatalog();'''
    replacement_reset = '''                this.selectFormula('coef_financiamento_carencia_premio', false, false);
                this.renderCatalog();'''
    assert target_reset in content, "target_reset not found"
    content = content.replace(target_reset, replacement_reset, 1)

    # Ensure CRLF line endings
    content_crlf = content.replace('\r\n', '\n').replace('\n', '\r\n')

    with open('Calculadora Financeira 17bIi.html', 'wb') as f:
        f.write(content_crlf.encode('utf-8'))

    with open('index.html', 'wb') as f:
        f.write(content_crlf.encode('utf-8'))

    h1 = hashlib.sha256(open('Calculadora Financeira 17bIi.html', 'rb').read()).hexdigest()
    h2 = hashlib.sha256(open('index.html', 'rb').read()).hexdigest()
    print(f"SHA-256 Calculadora Financeira 17bIi.html: {h1}")
    print(f"SHA-256 index.html:                       {h2}")
    assert h1 == h2, "Hashes do not match!"
    print("ALL REPLACEMENTS APPLIED AND PARITY VERIFIED!")

if __name__ == '__main__':
    apply_changes()

