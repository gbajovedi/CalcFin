# -*- coding: utf-8 -*-
"""
apply_fase4.py
Implements Fase 4: Alphanumeric Input on LCD (ALPHA Menu for Solver)
"""

import sys
import os
import hashlib
import re

sys.stdout.reconfigure(encoding='utf-8')

def run():
    target_path = 'Calculadora Financeira 17bIi.html'
    index_path = 'index.html'

    with open(target_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add alpha properties to app state
    old_state = '''            timeCalc: { date1: '2026-01-15', date2: '2026-04-15', daysAdd: 30, dateFormat: 'D.M' },'''

    new_state = '''            timeCalc: { date1: '2026-01-15', date2: '2026-04-15', daysAdd: 30, dateFormat: 'D.M' },
            alphaBuffer: '',
            alphaSubmenu: null,'''

    if old_state in content:
        content = content.replace(old_state, new_state)
        print("✓ Step 1: alphaBuffer and alphaSubmenu added to app state")
    elif 'alphaBuffer:' in content:
        print("✓ Step 1: alphaBuffer already present")
    else:
        print("✗ Step 1: old_state not found!")
        return False

    # 2. Add ALPHA case in getMenuTitle
    old_menutitle = '''                    case 'TIME_CALC': return 'TIME CALC: Prazos e Projeções de Datas';
                    case 'CURRX': return 'MENU CURRX: Câmbio de Moedas';'''

    new_menutitle = '''                    case 'TIME_CALC': return 'TIME CALC: Prazos e Projeções de Datas';
                    case 'ALPHA': return 'MENU ALPHA: Digitação de Equações';
                    case 'CURRX': return 'MENU CURRX: Câmbio de Moedas';'''

    if old_menutitle in content:
        content = content.replace(old_menutitle, new_menutitle)
        print("✓ Step 2: getMenuTitle updated for ALPHA")
    elif 'MENU ALPHA:' in content:
        print("✓ Step 2: getMenuTitle already updated")
    else:
        print("✗ Step 2: old_menutitle not found!")
        return False

    # 3. Update renderSoftkeyLabels for SOLVE and ALPHA
    old_sk_solve = '''                    case 'SOLVE':
                        for (let i = 0; i < 5; i++) {
                            if (this.solve && this.solve.varNames && this.solve.varNames[i]) {
                                labels[i] = this.solve.varNames[i];
                            }
                        }
                        labels[5] = 'MAIN';
                        break;'''

    new_sk_solve = '''                    case 'SOLVE':
                        for (let i = 0; i < 5; i++) {
                            if (this.solve && this.solve.varNames && this.solve.varNames[i]) {
                                labels[i] = this.solve.varNames[i];
                            }
                        }
                        if (this.solve && this.solve.varNames && this.solve.varNames.length < 5) {
                            labels[this.solve.varNames.length] = 'NOVA';
                        }
                        labels[5] = 'MAIN';
                        break;
                    case 'ALPHA':
                        if (!this.alphaSubmenu) {
                            labels[0] = 'A-E';
                            labels[1] = 'F-J';
                            labels[2] = 'K-O';
                            labels[3] = 'P-T';
                            labels[4] = 'U-Z';
                            labels[5] = 'OUTR';
                        } else if (this.alphaSubmenu === 'AE') {
                            labels[0] = 'A'; labels[1] = 'B'; labels[2] = 'C'; labels[3] = 'D'; labels[4] = 'E'; labels[5] = 'ALPH';
                        } else if (this.alphaSubmenu === 'FJ') {
                            labels[0] = 'F'; labels[1] = 'G'; labels[2] = 'H'; labels[3] = 'I'; labels[4] = 'J'; labels[5] = 'ALPH';
                        } else if (this.alphaSubmenu === 'KO') {
                            labels[0] = 'K'; labels[1] = 'L'; labels[2] = 'M'; labels[3] = 'N'; labels[4] = 'O'; labels[5] = 'ALPH';
                        } else if (this.alphaSubmenu === 'PT') {
                            labels[0] = 'P'; labels[1] = 'Q'; labels[2] = 'R'; labels[3] = 'S'; labels[4] = 'T'; labels[5] = 'ALPH';
                        } else if (this.alphaSubmenu === 'UZ') {
                            labels[0] = 'U'; labels[1] = 'V'; labels[2] = 'W'; labels[3] = 'X'; labels[4] = 'Y'; labels[5] = 'Z';
                        } else if (this.alphaSubmenu === 'OUTR') {
                            labels[0] = 'ESP'; labels[1] = '='; labels[2] = '+'; labels[3] = '-'; labels[4] = '*'; labels[5] = 'ALPH';
                        }
                        break;'''

    if old_sk_solve in content:
        content = content.replace(old_sk_solve, new_sk_solve)
        print("✓ Step 3: renderSoftkeyLabels updated for SOLVE NOVA and ALPHA")
    elif 'case \'ALPHA\':' in content:
        print("✓ Step 3: renderSoftkeyLabels already updated")
    else:
        print("✗ Step 3: old_sk_solve not found!")
        return False

    # 4. Update pressSoftkey for ALPHA and SOLVE NOVA
    old_sk_press = '''            // Execução Centralizada das Softkeys F1 a F6 no LCD
            pressSoftkey(index) {
                this.triggerKeyFeedback();'''

    new_sk_press = '''            // Execução Centralizada das Softkeys F1 a F6 no LCD
            pressSoftkey(index) {
                this.triggerKeyFeedback();

                // 0. MODO ALFANUMÉRICO (ALPHA) NO VISOR HP
                if (this.isAlphaMode()) {
                    if (!this.alphaSubmenu) {
                        switch (index) {
                            case 0: this.alphaSubmenu = 'AE'; break;
                            case 1: this.alphaSubmenu = 'FJ'; break;
                            case 2: this.alphaSubmenu = 'KO'; break;
                            case 3: this.alphaSubmenu = 'PT'; break;
                            case 4: this.alphaSubmenu = 'UZ'; break;
                            case 5: this.alphaSubmenu = 'OUTR'; break;
                        }
                    } else {
                        const sub = this.alphaSubmenu;
                        if (sub === 'AE') {
                            const letters = ['A', 'B', 'C', 'D', 'E'];
                            if (index < 5) this.alphaBuffer += letters[index];
                            else this.alphaSubmenu = null;
                        } else if (sub === 'FJ') {
                            const letters = ['F', 'G', 'H', 'I', 'J'];
                            if (index < 5) this.alphaBuffer += letters[index];
                            else this.alphaSubmenu = null;
                        } else if (sub === 'KO') {
                            const letters = ['K', 'L', 'M', 'N', 'O'];
                            if (index < 5) this.alphaBuffer += letters[index];
                            else this.alphaSubmenu = null;
                        } else if (sub === 'PT') {
                            const letters = ['P', 'Q', 'R', 'S', 'T'];
                            if (index < 5) this.alphaBuffer += letters[index];
                            else this.alphaSubmenu = null;
                        } else if (sub === 'UZ') {
                            const letters = ['U', 'V', 'W', 'X', 'Y', 'Z'];
                            this.alphaBuffer += letters[index];
                        } else if (sub === 'OUTR') {
                            const syms = [' ', ' = ', ' + ', ' - ', ' * '];
                            if (index < 5) this.alphaBuffer += syms[index];
                            else this.alphaSubmenu = null;
                        }
                    }
                    this.updateAlphaLcd();
                    return;
                }'''

    if old_sk_press in content:
        content = content.replace(old_sk_press, new_sk_press)
        print("✓ Step 4: pressSoftkey updated with ALPHA mode execution")
    elif 'isAlphaMode()' in content:
        print("✓ Step 4: pressSoftkey ALPHA already present")
    else:
        print("✗ Step 4: old_sk_press not found!")
        return False

    # 5. Handle NOVA in SOLVE menu
    old_solve_handler = '''                // 16. MENU SOLVE (Equações)
                if (this.currentMenu === 'SOLVE') {
                    if (index < 5 && this.solve && this.solve.varNames && this.solve.varNames[index]) {
                        this.handleSolveSoftkey(this.solve.varNames[index]);
                        return;
                    }
                    if (index === 5) {
                        this.navigateToMenu('MAIN', 'HP 17bII+ Menu Principal');
                        return;
                    }
                }'''

    new_solve_handler = '''                // 16. MENU SOLVE (Equações)
                if (this.currentMenu === 'SOLVE') {
                    if (index < 5 && this.solve && this.solve.varNames && this.solve.varNames[index]) {
                        this.handleSolveSoftkey(this.solve.varNames[index]);
                        return;
                    }
                    // Softkey NOVA para criar nova equação pelo visor
                    if (this.solve && this.solve.varNames && index === this.solve.varNames.length) {
                        this.startAlphaEditor();
                        return;
                    }
                    if (index === 5) {
                        this.navigateToMenu('MAIN', 'HP 17bII+ Menu Principal');
                        return;
                    }
                }'''

    if old_solve_handler in content:
        content = content.replace(old_solve_handler, new_solve_handler)
        print("✓ Step 5: SOLVE softkey NOVA handler added")
    elif 'startAlphaEditor()' in content:
        print("✓ Step 5: SOLVE NOVA already present")
    else:
        print("✗ Step 5: old_solve_handler not found!")
        return False

    # 6. Intercept pressDigit, pressOp, pressDot in ALPHA mode
    old_press_digit = '''            pressDigit(d) {
                this.triggerKeyFeedback();'''

    new_press_digit = '''            pressDigit(d) {
                this.triggerKeyFeedback();

                if (this.isAlphaMode()) {
                    this.alphaBuffer += d;
                    this.updateAlphaLcd();
                    return;
                }'''

    if old_press_digit in content:
        content = content.replace(old_press_digit, new_press_digit)
        print("✓ Step 6a: pressDigit updated for ALPHA mode")
    elif 'this.isAlphaMode()' in content:
        print("✓ Step 6a: pressDigit already updated")
    else:
        print("✗ Step 6a: old_press_digit not found!")
        return False

    old_press_op = '''            pressOp(op) {
                this.triggerKeyFeedback();'''

    new_press_op = '''            pressOp(op) {
                this.triggerKeyFeedback();

                if (this.isAlphaMode()) {
                    this.alphaBuffer += ' ' + op + ' ';
                    this.updateAlphaLcd();
                    return;
                }'''

    if old_press_op in content:
        content = content.replace(old_press_op, new_press_op)
        print("✓ Step 6b: pressOp updated for ALPHA mode")
    elif 'pressOp(op)' in content and 'this.isAlphaMode()' in content:
        print("✓ Step 6b: pressOp already updated")
    else:
        print("✗ Step 6b: old_press_op not found!")
        return False

    old_press_dot = '''            pressDot() {
                this.triggerKeyFeedback();'''

    new_press_dot = '''            pressDot() {
                this.triggerKeyFeedback();

                if (this.isAlphaMode()) {
                    this.alphaBuffer += '.';
                    this.updateAlphaLcd();
                    return;
                }'''

    if old_press_dot in content:
        content = content.replace(old_press_dot, new_press_dot)
        print("✓ Step 6c: pressDot updated for ALPHA mode")
    elif 'pressDot()' in content and 'this.isAlphaMode()' in content:
        print("✓ Step 6c: pressDot already updated")
    else:
        print("✗ Step 6c: old_press_dot not found!")
        return False

    # 7. Intercept pressKey in ALPHA mode for BACKSPACE, CLR, EXIT, INPUT, ENTER, =, (, )
    old_press_key = '''            pressKey(key) {
                this.triggerKeyFeedback();'''

    new_press_key = '''            pressKey(key) {
                this.triggerKeyFeedback();

                if (this.isAlphaMode()) {
                    if (key === 'BACKSPACE') {
                        this.alphaBuffer = this.alphaBuffer.trimEnd();
                        this.alphaBuffer = this.alphaBuffer.slice(0, -1);
                        this.updateAlphaLcd();
                        return;
                    }
                    if (key === 'CLR') {
                        this.alphaBuffer = '';
                        this.updateAlphaLcd();
                        return;
                    }
                    if (key === 'EXIT') {
                        if (this.alphaSubmenu) {
                            this.alphaSubmenu = null;
                            this.renderSoftkeyLabels();
                            this.updateLCD();
                        } else {
                            this.exitAlphaMode();
                        }
                        return;
                    }
                    if (key === 'INPUT' || key === 'ENTER') {
                        this.commitAlphaEquation();
                        return;
                    }
                    if (key === '(' || key === ')') {
                        this.alphaBuffer += key;
                        this.updateAlphaLcd();
                        return;
                    }
                    if (key === '=') {
                        this.alphaBuffer += ' = ';
                        this.updateAlphaLcd();
                        return;
                    }
                }'''

    if old_press_key in content:
        content = content.replace(old_press_key, new_press_key)
        print("✓ Step 7: pressKey updated for ALPHA mode keys")
    elif 'pressKey(key)' in content and 'this.isAlphaMode()' in content:
        print("✓ Step 7: pressKey already updated")
    else:
        print("✗ Step 7: old_press_key not found!")
        return False

    # 8. Add ALPHA and Solver Methods in JS
    old_methods_loc = '''            calcDepreciationSL() {
                const costField = document.getElementById('input-depr-cost');'''

    new_alpha_methods = '''            // ==========================================
            // MÓDULO ALFANUMÉRICO ALPHA (HP 17bII+ FASE 4)
            // ==========================================
            isAlphaMode() {
                return this.currentMenu === 'ALPHA';
            },

            startAlphaEditor(initialText = '') {
                this.switchTab('SOLVE');
                this.alphaBuffer = initialText;
                this.alphaSubmenu = null;
                this.navigateToMenu('ALPHA', 'ALPHA: ' + (initialText || '_'));
                this.updateAlphaLcd();
            },

            exitAlphaMode() {
                this.alphaBuffer = '';
                this.alphaSubmenu = null;
                this.navigateToMenu('SOLVE', 'MENU SOLVE: Equações');
                this.updateLCD();
            },

            updateAlphaLcd() {
                const l1 = document.getElementById('lcdLine1');
                const l2 = document.getElementById('lcdLine2');
                if (l1) l1.textContent = 'ALPHA: ' + (this.alphaBuffer || '') + '_';
                if (l2) l2.textContent = this.alphaBuffer ? 'INPUT: Salva | EXIT: Sai' : 'Digite letras e números';
                this.renderSoftkeyLabels();
            },

            commitAlphaEquation() {
                const eq = (this.alphaBuffer || '').trim();
                if (!eq) {
                    this.setError('Equação em branco');
                    return;
                }
                const success = this.createCustomFormula(eq);
                if (success) {
                    this.alphaBuffer = '';
                    this.alphaSubmenu = null;
                    this.currentMenu = 'SOLVE';
                    const form = this.formulas.find(f => f.id === this.solve.activeFormulaId);
                    const l1 = document.getElementById('lcdLine1');
                    if (l1) l1.textContent = `SOLVE: ${form.title}`;
                    this.renderCatalog();
                    this.renderSoftkeyLabels();
                    this.updateLCD();
                    this.setResult(0, `Nova equação salva: ${eq}`);
                }
            },

            submitQuickEquation() {
                const inp = document.getElementById('input-quick-equation');
                const eq = inp ? inp.value.trim() : '';
                if (!eq) {
                    this.setError('Informe a equação');
                    return;
                }
                const success = this.createCustomFormula(eq);
                if (success && inp) inp.value = '';
            },

            createCustomFormula(eqStr) {
                const vars = this.extractVariablesFromEquation(eqStr);
                if (!vars || vars.length === 0) {
                    this.setError('Nenhuma variável válida');
                    return false;
                }
                const id = 'custom_' + Date.now();
                const title = eqStr.split('=')[0].trim() || 'Equação Custom';
                const compiled = this.compileEquation(eqStr, vars);

                const newForm = {
                    id,
                    title,
                    category: 'Personalizadas (ALPHA)',
                    equation: eqStr,
                    vars,
                    evalResidual: compiled
                };

                this.formulas.push(newForm);
                this.selectFormula(id);
                return true;
            },

            extractVariablesFromEquation(eqStr) {
                let eq = eqStr;
                if (eq.includes(':')) {
                    eq = eq.split(':')[1];
                }
                const tokens = eq.match(/\\b[A-Za-z_][A-Za-z0-9_]*\\b/g) || [];
                const keywords = new Set(['EXP', 'LN', 'LOG', 'SQRT', 'SIN', 'COS', 'TAN', 'IF', 'MAX', 'MIN', 'ABS', 'INV']);
                const vars = [];
                for (const t of tokens) {
                    const u = t.toUpperCase();
                    if (!keywords.has(u) && !vars.includes(u)) {
                        vars.push(u);
                    }
                }
                return vars;
            },

            compileEquation(eqStr, varNames) {
                let eq = eqStr;
                if (eq.includes(':')) {
                    eq = eq.split(':')[1];
                }
                const parts = eq.split('=');
                let lhs = parts[0].trim();
                let rhs = parts.length > 1 ? parts.slice(1).join('=').trim() : '0';

                lhs = lhs.replace(/\\^/g, '**')
                         .replace(/\\bLN\\s*\\(/gi, 'Math.log(')
                         .replace(/\\bLOG\\s*\\(/gi, 'Math.log10(')
                         .replace(/\\bEXP\\s*\\(/gi, 'Math.exp(')
                         .replace(/\\bSQRT\\s*\\(/gi, 'Math.sqrt(');

                rhs = rhs.replace(/\\^/g, '**')
                         .replace(/\\bLN\\s*\\(/gi, 'Math.log(')
                         .replace(/\\bLOG\\s*\\(/gi, 'Math.log10(')
                         .replace(/\\bEXP\\s*\\(/gi, 'Math.exp(')
                         .replace(/\\bSQRT\\s*\\(/gi, 'Math.sqrt(');

                const sortedVars = [...varNames].sort((a, b) => b.length - a.length);
                let evalStr = `(${lhs}) - (${rhs})`;
                for (const v of sortedVars) {
                    const regex = new RegExp(`\\\\b${v}\\\\b`, 'g');
                    evalStr = evalStr.replace(regex, `(v['${v}'] !== undefined ? Number(v['${v}']) : 0)`);
                }

                return (v) => {
                    try {
                        return Function('v', `return ${evalStr};`)(v);
                    } catch (e) {
                        return NaN;
                    }
                };
            },

            calcDepreciationSL() {
                const costField = document.getElementById('input-depr-cost');'''

    if old_methods_loc in content:
        content = content.replace(old_methods_loc, new_alpha_methods)
        print("✓ Step 8: ALPHA methods and dynamic equation compiler added")
    elif 'createCustomFormula' in content:
        print("✓ Step 8: ALPHA methods already present")
    else:
        print("✗ Step 8: old_methods_loc not found!")
        return False

    # 9. Update evaluateEquationResidual to use compiled residual
    old_eval_res = '''            evaluateEquationResidual(targetVar, testVal) {
                const form = this.formulas.find(f => f.id === this.solve.activeFormulaId);
                if (!form) return 0;

                const v = { ...this.solve.vars, [targetVar]: testVal };

                try {
                    switch (form.id) {'''

    new_eval_res = '''            evaluateEquationResidual(targetVar, testVal) {
                const form = this.formulas.find(f => f.id === this.solve.activeFormulaId);
                if (!form) return 0;

                const v = { ...this.solve.vars, [targetVar]: testVal };

                if (typeof form.evalResidual === 'function') {
                    return form.evalResidual(v);
                }

                try {
                    switch (form.id) {'''

    if old_eval_res in content:
        content = content.replace(old_eval_res, new_eval_res)
        print("✓ Step 9: evaluateEquationResidual updated with compiled residual execution")
    elif 'typeof form.evalResidual === \'function\'' in content:
        print("✓ Step 9: evaluateEquationResidual already updated")
    else:
        print("✗ Step 9: old_eval_res not found!")
        return False

    # 10. Add default fallback in evaluateEquationResidual switch
    old_eval_default = '''                        default:
                            return 0;
                    }
                } catch (e) {
                    return NaN;
                }
            },'''

    new_eval_default = '''                        default: {
                            if (form.equation && form.vars) {
                                if (!form.evalResidual) {
                                    form.evalResidual = this.compileEquation(form.equation, form.vars);
                                }
                                return form.evalResidual(v);
                            }
                            return 0;
                        }
                    }
                } catch (e) {
                    return NaN;
                }
            },'''

    if old_eval_default in content:
        content = content.replace(old_eval_default, new_eval_default)
        print("✓ Step 10: evaluateEquationResidual default dynamic fallback added")
    elif 'form.evalResidual = this.compileEquation' in content:
        print("✓ Step 10: evaluateEquationResidual default already updated")
    else:
        print("✗ Step 10: old_eval_default not found!")
        return False

    # 11. Add UI action bar in panel-SOLVE
    old_panel_solve = '''                                <!-- Card da Fórmula Atual -->
                                <div class="bg-slate-950/90 border border-amber-500/30 rounded-xl p-3.5">'''

    new_panel_solve = '''                                <!-- Barra de Ações Rápidas do Solver -->
                                <div class="flex flex-wrap items-center justify-between gap-2 mb-1 p-2 rounded-xl bg-slate-950 border border-slate-800">
                                    <button onclick="app.startAlphaEditor()" id="btn-open-alpha" class="px-2.5 py-1 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold font-mono text-xs rounded transition inline-flex items-center gap-1 shadow-sm">
                                        <span>🔤</span> Digitar Equação no Visor (ALPHA)
                                    </button>
                                    <div class="flex items-center gap-1.5 min-w-[240px]">
                                        <input type="text" id="input-quick-equation" placeholder="Ex: LUCRO = VENDA - CUSTO" class="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1 text-xs font-mono text-white placeholder:text-slate-600 focus:outline-none focus:ring-1 focus:ring-amber-500">
                                        <button onclick="app.submitQuickEquation()" class="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-amber-400 font-bold font-mono text-xs rounded border border-slate-700 transition shrink-0">
                                            Salvar
                                        </button>
                                    </div>
                                </div>

                                <!-- Card da Fórmula Atual -->
                                <div class="bg-slate-950/90 border border-amber-500/30 rounded-xl p-3.5">'''

    if old_panel_solve in content:
        content = content.replace(old_panel_solve, new_panel_solve)
        print("✓ Step 11: panel-SOLVE action bar with ALPHA button added")
    elif 'id="btn-open-alpha"' in content:
        print("✓ Step 11: panel-SOLVE action bar already present")
    else:
        print("✗ Step 11: old_panel_solve not found!")
        return False

    # 12. Update syncModuleToCalculator to preserve ALPHA
    old_sync = '''                    || (tabId === 'CURRX' && this.currentMenu === 'CURRX')
                    || (this.currentMenu === tabId);'''

    new_sync = '''                    || (tabId === 'CURRX' && this.currentMenu === 'CURRX')
                    || (tabId === 'SOLVE' && (this.currentMenu === 'SOLVE' || this.currentMenu === 'ALPHA'))
                    || (this.currentMenu === tabId);'''

    if old_sync in content:
        content = content.replace(old_sync, new_sync)
        print("✓ Step 12: syncModuleToCalculator updated for ALPHA")
    elif 'this.currentMenu === \'ALPHA\'' in content:
        print("✓ Step 12: syncModuleToCalculator already updated")
    else:
        print("✗ Step 12: old_sync not found!")
        return False

    # Normalizar quebras de linha para CRLF
    content = content.replace('\r\n', '\n').replace('\n', '\r\n')

    # Salvar em Calculadora Financeira 17bIi.html
    with open(target_path, 'wb') as f:
        f.write(content.encode('utf-8'))
    print(f"✓ Saved {target_path}")

    # Salvar em index.html
    with open(index_path, 'wb') as f:
        f.write(content.encode('utf-8'))
    print(f"✓ Saved {index_path}")

    # Checar paridade SHA256
    with open(target_path, 'rb') as f:
        h1 = hashlib.sha256(f.read()).hexdigest()
    with open(index_path, 'rb') as f:
        h2 = hashlib.sha256(f.read()).hexdigest()

    print(f"SHA256 target: {h1}")
    print(f"SHA256 index:  {h2}")
    if h1 == h2:
        print("✓ Files are 100% byte-for-byte identical!")
        return True
    else:
        print("✗ SHA256 mismatch!")
        return False

if __name__ == '__main__':
    success = run()
    exit(0 if success else 1)
