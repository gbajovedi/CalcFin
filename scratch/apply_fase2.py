# -*- coding: utf-8 -*-
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

    # 1. Atualizar propriedades do app (menuStack, bus, currx, bond, depr)
    old_app_header = '''            registers: new Array(10).fill(0), // Registradores 0 a 9 de armazenamento oficial
            stoState: null, // null ou 'pending'
            stoOp: null, // null, '+', '-', '*', '/'
            rclState: false, // true quando aguarda dígito de registrador 0-9
            stackLift: true, // Controle de Stack Lift da pilha RPN'''

    new_app_header = '''            registers: new Array(10).fill(0), // Registradores 0 a 9 de armazenamento oficial
            stoState: null, // null ou 'pending'
            stoOp: null, // null, '+', '-', '*', '/'
            rclState: false, // true quando aguarda dígito de registrador 0-9
            stackLift: true, // Controle de Stack Lift da pilha RPN
            menuStack: [], // Pilha hierárquica oficial de navegação de menus
            bus: { oldVal: 0, newVal: 0, cost: 0, price: 0, total: 0, part: 0 },
            currx: { base: 'USD', rates: { USD: 1.0, BRL: 5.65, EUR: 0.92, GBP: 0.78 } },
            bond: { price: 100, ytm: 8, coupon: 8 },
            depr: { cost: 10000, salvage: 1000, life: 5 },'''

    if old_app_header in content:
        content = content.replace(old_app_header, new_app_header)
        print("✓ Block 1: App state properties added (menuStack, bus, currx, bond, depr)")
    elif 'menuStack: []' in content:
        print("✓ Block 1: Already present")
    else:
        # replace the earlier one
        content = re.sub(r'menuStack:\s*\[[\'\"A-Z]*\],', "menuStack: [],", content)
        print("✓ Block 1: Updated menuStack to []")

    # 2. Substituir renderSoftkeyLabels e pressSoftkey
    sk_match = re.search(r'            // Navega[^\n]*\n\s*navigateToMenu\(newMenu[\s\S]*?\n            // Entrada Num[^\n]*', content)
    if not sk_match:
        sk_match = re.search(r'            renderSoftkeyLabels\(\) \{[\s\S]*?\n            // Entrada Num[^\n]*', content)
    if not sk_match:
        print("✗ Block 2: softkeys block not found via regex!")
        return False

    old_sk_text = sk_match.group(0)

    new_sk_text = '''            // Navegação Hierárquica Oficial de Menus no Visor LCD (HP 17bII+)
            navigateToMenu(newMenu, lineTitle = '') {
                if (this.currentMenu !== newMenu) {
                    if (!Array.isArray(this.menuStack)) this.menuStack = [];
                    this.menuStack.push(this.currentMenu);
                }
                this.currentMenu = newMenu;
                const title = lineTitle || this.getMenuTitle(newMenu);
                const l1 = document.getElementById('lcdLine1');
                if (l1) l1.textContent = title;
                this.updateLCD();
            },

            getMenuTitle(menu) {
                switch (menu) {
                    case 'MAIN': return 'HP 17bII+ Menu Principal';
                    case 'FIN': return 'MENU FIN: Finanças e Negócios';
                    case 'TVM': return 'MENU TVM: Matemática Financeira';
                    case 'TVM_OTHER': return 'TVM OTHER: P/YR, BGN/END e Amortização';
                    case 'ICNV': return 'MENU ICNV: Conversão de Taxas';
                    case 'CFLO': return 'MENU CFLO: Fluxo de Caixa Descontado';
                    case 'BOND': return 'MENU BOND: Títulos de Renda Fixa';
                    case 'DEPRC': return 'MENU DEPRC: Depreciação de Ativos';
                    case 'BUS': return 'MENU BUS: Ferramentas Comerciais';
                    case 'BUS_PCHG': return 'BUS: %CHG Variação Percentual';
                    case 'BUS_PTOTL': return 'BUS: %TOTL Percentual do Total';
                    case 'BUS_MUC': return 'BUS: MU%C Markup sobre o Custo';
                    case 'BUS_MUP': return 'BUS: MU%P Margem sobre o Preço';
                    case 'SUM': return 'MENU SUM: Estatística e Regressão';
                    case 'TIME': return 'MENU TIME: Relógio e Calendário';
                    case 'CURRX': return 'MENU CURRX: Câmbio de Moedas';
                    case 'DSP': return 'MENU DSP: Ajustes de Exibição';
                    case 'MODES': return 'MENU MODES: Configurações Gerais';
                    case 'MATH': return 'MENU MATH: Funções Matemáticas';
                    case 'SOLVE': return 'MENU SOLVE: Equações';
                    case 'TAPE': return 'MENU FITA: Histórico e Registradores';
                    default: return 'HP 17bII+ Menu Principal';
                }
            },

            renderSoftkeyLabels() {
                const labels = ['', '', '', '', '', ''];

                switch (this.currentMenu) {
                    case 'MAIN':
                        labels[0] = 'FIN';
                        labels[1] = 'BUS';
                        labels[2] = 'SUM';
                        labels[3] = 'TIME';
                        labels[4] = 'SOLVE';
                        labels[5] = 'CURRX';
                        break;
                    case 'FIN':
                        labels[0] = 'TVM';
                        labels[1] = 'ICNV';
                        labels[2] = 'CFLO';
                        labels[3] = 'BOND';
                        labels[4] = 'DEPRC';
                        labels[5] = 'MAIN';
                        break;
                    case 'TVM':
                        labels[0] = 'N';
                        labels[1] = 'I%YR';
                        labels[2] = 'PV';
                        labels[3] = 'PMT';
                        labels[4] = 'FV';
                        labels[5] = 'OTHER';
                        break;
                    case 'TVM_OTHER':
                        labels[0] = 'P/YR';
                        labels[1] = 'BEG';
                        labels[2] = 'END';
                        labels[3] = 'RESET';
                        labels[4] = '';
                        labels[5] = 'AMRT';
                        break;
                    case 'ICNV':
                    case 'FIN_TOOLS':
                        labels[0] = 'NOM%';
                        labels[1] = 'EFF%';
                        labels[2] = 'P/YR';
                        labels[3] = 'SL';
                        labels[4] = 'DEPR';
                        labels[5] = 'FIN';
                        break;
                    case 'CFLO':
                        labels[0] = 'FLOW';
                        labels[1] = 'I%';
                        labels[2] = 'NPV';
                        labels[3] = 'IRR';
                        labels[4] = 'RESET';
                        labels[5] = 'FIN';
                        break;
                    case 'BOND':
                        labels[0] = 'PREÇO';
                        labels[1] = 'YTM';
                        labels[2] = 'CUPOM';
                        labels[3] = '';
                        labels[4] = '';
                        labels[5] = 'FIN';
                        break;
                    case 'DEPRC':
                        labels[0] = 'SL';
                        labels[1] = 'SOYD';
                        labels[2] = 'DB';
                        labels[3] = 'CUSTO';
                        labels[4] = 'RESID';
                        labels[5] = 'FIN';
                        break;
                    case 'BUS':
                        labels[0] = '%CHG';
                        labels[1] = '%TOTL';
                        labels[2] = 'MU%C';
                        labels[3] = 'MU%P';
                        labels[4] = '';
                        labels[5] = 'MAIN';
                        break;
                    case 'BUS_PCHG':
                        labels[0] = 'OLD';
                        labels[1] = 'NEW';
                        labels[2] = '%CHG';
                        labels[3] = '';
                        labels[4] = '';
                        labels[5] = 'BUS';
                        break;
                    case 'BUS_PTOTL':
                        labels[0] = 'TOTAL';
                        labels[1] = 'PART';
                        labels[2] = '%TOTL';
                        labels[3] = '';
                        labels[4] = '';
                        labels[5] = 'BUS';
                        break;
                    case 'BUS_MUC':
                        labels[0] = 'COST';
                        labels[1] = 'PRICE';
                        labels[2] = 'MU%C';
                        labels[3] = '';
                        labels[4] = '';
                        labels[5] = 'BUS';
                        break;
                    case 'BUS_MUP':
                        labels[0] = 'COST';
                        labels[1] = 'PRICE';
                        labels[2] = 'MARG';
                        labels[3] = '';
                        labels[4] = '';
                        labels[5] = 'BUS';
                        break;
                    case 'SUM':
                    case 'BUS_SUM':
                        labels[0] = 'Σ+';
                        labels[1] = 'Σ-';
                        labels[2] = 'TOTAL';
                        labels[3] = 'MEAN';
                        labels[4] = 'SDEV';
                        labels[5] = 'MAIN';
                        break;
                    case 'TIME':
                        labels[0] = 'CALC';
                        labels[1] = 'SET';
                        labels[2] = 'FORMAT';
                        labels[3] = '';
                        labels[4] = '';
                        labels[5] = 'MAIN';
                        break;
                    case 'CURRX':
                        labels[0] = 'USD';
                        labels[1] = 'EUR';
                        labels[2] = 'GBP';
                        labels[3] = 'BRL';
                        labels[4] = 'SET';
                        labels[5] = 'MAIN';
                        break;
                    case 'DSP':
                        labels[0] = 'FIX';
                        labels[1] = 'ALL';
                        labels[2] = '.';
                        labels[3] = ',';
                        labels[4] = '';
                        labels[5] = 'MAIN';
                        break;
                    case 'MODES':
                        labels[0] = 'BEEP';
                        labels[1] = 'PRNT';
                        labels[2] = 'DBL';
                        labels[3] = 'ALG';
                        labels[4] = 'RPN';
                        labels[5] = 'MAIN';
                        break;
                    case 'MATH':
                        labels[0] = 'LOG';
                        labels[1] = '10^x';
                        labels[2] = 'LN';
                        labels[3] = 'EXP';
                        labels[4] = 'N!';
                        labels[5] = 'PI';
                        break;
                    case 'SOLVE':
                        for (let i = 0; i < 5; i++) {
                            if (this.solve && this.solve.varNames && this.solve.varNames[i]) {
                                labels[i] = this.solve.varNames[i];
                            }
                        }
                        labels[5] = 'MAIN';
                        break;
                    case 'TAPE':
                        labels[0] = 'COPIAR';
                        labels[1] = 'LIMPAR';
                        labels[2] = 'RCL';
                        labels[3] = 'STO';
                        labels[4] = 'REG';
                        labels[5] = 'MAIN';
                        break;
                    default:
                        labels[0] = 'FIN';
                        labels[1] = 'BUS';
                        labels[2] = 'SUM';
                        labels[3] = 'TIME';
                        labels[4] = 'SOLVE';
                        labels[5] = 'CURRX';
                        break;
                }

                for (let i = 0; i < 6; i++) {
                    const sk = document.getElementById(`sk-${i + 1}`);
                    if (sk) {
                        sk.textContent = labels[i] || `F${i + 1}`;
                    }
                }
            },

            // Execução Centralizada das Softkeys F1 a F6 no LCD
            pressSoftkey(index) {
                this.triggerKeyFeedback();

                // 1. MENU PRINCIPAL (MAIN)
                if (this.currentMenu === 'MAIN') {
                    switch (index) {
                        case 0: // FIN
                            this.navigateToMenu('FIN', 'MENU FIN: Finanças e Negócios');
                            break;
                        case 1: // BUS
                            this.switchTab('BUS_SUM');
                            this.navigateToMenu('BUS', 'MENU BUS: Ferramentas Comerciais');
                            break;
                        case 2: // SUM
                            this.switchTab('BUS_SUM');
                            this.navigateToMenu('SUM', 'MENU SUM: Estatística e Regressão');
                            break;
                        case 3: // TIME
                            const nowStr = new Date().toLocaleTimeString('pt-BR') + ' ' + new Date().toLocaleDateString('pt-BR');
                            this.navigateToMenu('TIME', `TIME: ${nowStr}`);
                            break;
                        case 4: // SOLVE
                            this.switchTab('SOLVE');
                            this.navigateToMenu('SOLVE', 'MENU SOLVE: Equações');
                            break;
                        case 5: // CURRX
                            this.navigateToMenu('CURRX', 'CURRX: Câmbio de Moedas (1 USD = R$ 5,65)');
                            break;
                    }
                    return;
                }

                // 2. MENU FINANCEIRO (FIN)
                if (this.currentMenu === 'FIN') {
                    switch (index) {
                        case 0: // TVM
                            this.switchTab('TVM');
                            this.navigateToMenu('TVM', 'MENU TVM: Matemática Financeira');
                            break;
                        case 1: // ICNV
                            this.switchTab('FIN_TOOLS');
                            this.navigateToMenu('ICNV', 'MENU ICNV: Conversão de Taxas');
                            break;
                        case 2: // CFLO
                            this.switchTab('CFLO');
                            this.navigateToMenu('CFLO', 'MENU CFLO: Fluxo de Caixa Descontado');
                            break;
                        case 3: // BOND
                            this.navigateToMenu('BOND', 'MENU BOND: Títulos de Renda Fixa');
                            break;
                        case 4: // DEPRC
                            this.switchTab('FIN_TOOLS');
                            this.navigateToMenu('DEPRC', 'MENU DEPRC: Depreciação de Ativos');
                            break;
                        case 5: // MAIN
                            this.navigateToMenu('MAIN', 'HP 17bII+ Menu Principal');
                            break;
                    }
                    return;
                }

                // 3. SUBMENU TVM
                if (this.currentMenu === 'TVM') {
                    if (index === 5) {
                        this.navigateToMenu('TVM_OTHER', 'TVM OTHER: P/YR, BGN/END e Amortização');
                        return;
                    }
                    const keys = ['N', 'I', 'PV', 'PMT', 'FV'];
                    const key = keys[index];
                    if (this.entry.isEntering) {
                        const typed = parseFloat(this.entry.buffer.replace(',', '.'));
                        const val = isNaN(typed) ? 0 : this.cleanFloat(typed, this.decimals);
                        this.tvm[key] = val;
                        this.clearTvmCalculatedCard(key);
                        this.syncStateToInputs();
                        this.entry.isEntering = false;
                        this.entry.buffer = '0';
                        this.entry.hasDot = false;
                        this.setResult(val, `TVM: ${key} armazenado`);
                        this.syncModuleToCalculator('TVM');
                        this.saveWorkspaceState();
                    } else {
                        this.calculateTVM(key);
                        this.syncModuleToCalculator('TVM');
                    }
                    return;
                }

                // 4. SUBMENU TVM OTHER
                if (this.currentMenu === 'TVM_OTHER') {
                    switch (index) {
                        case 0: // P/YR
                            if (this.entry.isEntering) {
                                const val = parseFloat(this.entry.buffer.replace(',', '.'));
                                if (!isNaN(val) && val > 0) {
                                    this.tvm.PYR = val;
                                    const inp = document.getElementById('input-tvm-PYR');
                                    if (inp) inp.value = val;
                                    this.entry.isEntering = false;
                                    this.entry.buffer = '0';
                                    this.entry.hasDot = false;
                                    this.setResult(val, `TVM: P/YR definido para ${val}`);
                                    this.saveWorkspaceState();
                                }
                            } else {
                                this.setResult(this.tvm.PYR, `TVM: Pagtos/ano (P/YR) = ${this.tvm.PYR}`);
                            }
                            break;
                        case 1: // BEG
                            this.setTvmMode(true);
                            document.getElementById('lcdLine1').textContent = 'TVM: Modo BGN (Antecipado)';
                            break;
                        case 2: // END
                            this.setTvmMode(false);
                            document.getElementById('lcdLine1').textContent = 'TVM: Modo END (Postecipado)';
                            break;
                        case 3: // RESET
                            this.clearTvmModule();
                            document.getElementById('lcdLine1').textContent = 'TVM: Todos os dados limpos';
                            break;
                        case 5: // AMRT
                            this.switchTab('TVM');
                            this.generateAmortizationSchedule();
                            document.getElementById('lcdLine1').textContent = 'AMRT: Tabela gerada na aba TVM';
                            break;
                    }
                    this.updateLCD();
                    return;
                }

                // 5. SUBMENU ICNV (Conversão de Taxas)
                if (this.currentMenu === 'ICNV' || this.currentMenu === 'FIN_TOOLS') {
                    if (index === 5) {
                        this.navigateToMenu('FIN', 'MENU FIN: Finanças e Negócios');
                        return;
                    }
                    const nomEl = document.getElementById('input-icnv-nom');
                    const pyrEl = document.getElementById('input-icnv-pyr');
                    const pyr = pyrEl ? (parseFloat(pyrEl.value) || 12) : 12;
                    if (index === 0) { // NOM%
                        if (this.entry.isEntering) {
                            const val = parseFloat(this.entry.buffer.replace(',', '.'));
                            if (!isNaN(val) && nomEl) nomEl.value = val;
                            this.entry.isEntering = false;
                            this.setResult(val, `ICNV: Taxa Nominal = ${this.formatNum(val)}%`);
                        } else {
                            this.calcEffectiveRate();
                        }
                    } else if (index === 1) { // EFF%
                        this.calcEffectiveRate();
                    } else if (index === 2) { // P/YR
                        if (this.entry.isEntering) {
                            const val = parseFloat(this.entry.buffer.replace(',', '.'));
                            if (!isNaN(val) && val > 0 && pyrEl) pyrEl.value = val;
                            this.entry.isEntering = false;
                            this.setResult(val, `ICNV: P/YR = ${val}`);
                        } else {
                            this.setResult(pyr, `ICNV: P/YR = ${pyr}`);
                        }
                    }
                    this.updateLCD();
                    return;
                }

                // 6. SUBMENU CFLO (Fluxo de Caixa)
                if (this.currentMenu === 'CFLO') {
                    if (index === 5) {
                        this.navigateToMenu('FIN', 'MENU FIN: Finanças e Negócios');
                        return;
                    }
                    switch (index) {
                        case 0: // FLOW
                            if (this.entry.isEntering) {
                                const typed = parseFloat(this.entry.buffer.replace(',', '.'));
                                if (!isNaN(typed)) {
                                    this.cflo.push({ amount: this.cleanFloat(typed, this.decimals), count: 1 });
                                    this.renderCashFlows();
                                    this.entry.isEntering = false;
                                    this.entry.buffer = '0';
                                    this.entry.hasDot = false;
                                    this.setResult(typed, `CF${this.cflo.length - 1} = ${this.formatNum(typed)}`);
                                    this.saveWorkspaceState();
                                }
                            } else {
                                const total = this.cflo.reduce((s, c) => s + (c.amount * (c.count || 1)), 0);
                                this.setResult(total, `Total dos ${this.cflo.length} Fluxos`, null, 'R$');
                            }
                            break;
                        case 1: // I%
                            if (this.entry.isEntering) {
                                const typed = parseFloat(this.entry.buffer.replace(',', '.'));
                                if (!isNaN(typed)) {
                                    const rateEl = document.getElementById('input-cflo-rate');
                                    if (rateEl) rateEl.value = typed;
                                    this.entry.isEntering = false;
                                    this.entry.buffer = '0';
                                    this.entry.hasDot = false;
                                    this.setResult(typed, `CFLO: Taxa I% = ${this.formatNum(typed)}%`);
                                }
                            } else {
                                const rateEl = document.getElementById('input-cflo-rate');
                                const r = rateEl ? parseFloat(rateEl.value) || 0 : 0;
                                this.setResult(r, `CFLO: Taxa I% = ${this.formatNum(r)}%`);
                            }
                            break;
                        case 2: // NPV
                            this.calcNPV();
                            break;
                        case 3: // IRR
                            this.calcIRR();
                            break;
                        case 4: // RESET
                            this.cflo = [];
                            this.renderCashFlows();
                            this.clearCfloResults();
                            this.setResult(0, 'CFLO: Fluxos de caixa zerados');
                            this.saveWorkspaceState();
                            break;
                    }
                    this.updateLCD();
                    return;
                }

                // 7. SUBMENU BOND (Títulos de Renda Fixa)
                if (this.currentMenu === 'BOND') {
                    if (index === 5) {
                        this.navigateToMenu('FIN', 'MENU FIN: Finanças e Negócios');
                        return;
                    }
                    const b = this.bond || { price: 100, ytm: 8, coupon: 8 };
                    if (index === 0) { // PREÇO
                        if (this.entry.isEntering) {
                            b.price = this.getDisplayValue();
                            this.entry.isEntering = false;
                            this.setResult(b.price, `BOND: Preço = ${this.formatNum(b.price)}`);
                        } else {
                            const p = (b.coupon / (b.ytm / 100));
                            b.price = this.cleanFloat(p, this.decimals);
                            this.setResult(b.price, `BOND: Preço Calculado = ${this.formatNum(b.price)}`);
                        }
                    } else if (index === 1) { // YTM
                        if (this.entry.isEntering) {
                            b.ytm = this.getDisplayValue();
                            this.entry.isEntering = false;
                            this.setResult(b.ytm, `BOND: YTM = ${this.formatNum(b.ytm)}%`);
                        } else {
                            const y = (b.coupon / b.price) * 100;
                            b.ytm = this.cleanFloat(y, this.decimals);
                            this.setResult(b.ytm, `BOND: YTM Calculado = ${this.formatNum(b.ytm)}%`);
                        }
                    } else if (index === 2) { // CUPOM
                        if (this.entry.isEntering) {
                            b.coupon = this.getDisplayValue();
                            this.entry.isEntering = false;
                            this.setResult(b.coupon, `BOND: Cupom = ${this.formatNum(b.coupon)}%`);
                        } else {
                            this.setResult(b.coupon, `BOND: Cupom = ${this.formatNum(b.coupon)}%`);
                        }
                    }
                    this.bond = b;
                    this.updateLCD();
                    return;
                }

                // 8. SUBMENU DEPRC (Depreciação de Ativos)
                if (this.currentMenu === 'DEPRC') {
                    if (index === 5) {
                        this.navigateToMenu('FIN', 'MENU FIN: Finanças e Negócios');
                        return;
                    }
                    const d = this.depr || { cost: 10000, salvage: 1000, life: 5 };
                    if (index === 0) { // SL
                        const sl = (d.cost - d.salvage) / Math.max(1, d.life);
                        this.setResult(sl, `DEPR SL: Depreciação Linear = ${this.formatNum(sl)}/ano`);
                    } else if (index === 1) { // SOYD
                        const sumYears = (d.life * (d.life + 1)) / 2;
                        const soydYear1 = (d.cost - d.salvage) * (d.life / sumYears);
                        this.setResult(soydYear1, `DEPR SOYD (Ano 1) = ${this.formatNum(soydYear1)}`);
                    } else if (index === 2) { // DB
                        const rate = 2 / Math.max(1, d.life);
                        const dbYear1 = d.cost * rate;
                        this.setResult(dbYear1, `DEPR DB (200% Ano 1) = ${this.formatNum(dbYear1)}`);
                    } else if (index === 3) { // CUSTO
                        if (this.entry.isEntering) {
                            d.cost = this.getDisplayValue();
                            this.entry.isEntering = false;
                            this.setResult(d.cost, `DEPR: Custo = ${this.formatNum(d.cost)}`);
                        } else {
                            this.setResult(d.cost, `DEPR: Custo = ${this.formatNum(d.cost)}`);
                        }
                    } else if (index === 4) { // RESID
                        if (this.entry.isEntering) {
                            d.salvage = this.getDisplayValue();
                            this.entry.isEntering = false;
                            this.setResult(d.salvage, `DEPR: Residual = ${this.formatNum(d.salvage)}`);
                        } else {
                            this.setResult(d.salvage, `DEPR: Residual = ${this.formatNum(d.salvage)}`);
                        }
                    }
                    this.depr = d;
                    this.updateLCD();
                    return;
                }

                // 9. MENU COMERCIAL (BUS)
                if (this.currentMenu === 'BUS') {
                    switch (index) {
                        case 0: // %CHG
                            this.navigateToMenu('BUS_PCHG', 'BUS: %CHG Variação Percentual');
                            break;
                        case 1: // %TOTL
                            this.navigateToMenu('BUS_PTOTL', 'BUS: %TOTL Percentual do Total');
                            break;
                        case 2: // MU%C
                            this.navigateToMenu('BUS_MUC', 'BUS: MU%C Markup s/ Custo');
                            break;
                        case 3: // MU%P
                            this.navigateToMenu('BUS_MUP', 'BUS: MU%P Margem s/ Preço');
                            break;
                        case 5: // MAIN
                            this.navigateToMenu('MAIN', 'HP 17bII+ Menu Principal');
                            break;
                    }
                    return;
                }

                // 9.1 SUBMENU BUS: %CHG
                if (this.currentMenu === 'BUS_PCHG') {
                    const b = this.bus;
                    if (index === 0) { // OLD
                        b.oldVal = this.getDisplayValue();
                        this.entry.isEntering = false;
                        this.setResult(b.oldVal, `Valor Antigo (OLD) = ${this.formatNum(b.oldVal)}`);
                    } else if (index === 1) { // NEW
                        b.newVal = this.getDisplayValue();
                        this.entry.isEntering = false;
                        this.setResult(b.newVal, `Valor Novo (NEW) = ${this.formatNum(b.newVal)}`);
                    } else if (index === 2) { // %CHG
                        if (b.oldVal === 0) {
                            this.setError('Divisão por zero em %CHG');
                        } else {
                            const chg = ((b.newVal - b.oldVal) / Math.abs(b.oldVal)) * 100;
                            this.setResult(chg, `%CHG = ${this.formatNum(chg)}%`);
                        }
                    } else if (index === 5) {
                        this.navigateToMenu('BUS', 'MENU BUS: Ferramentas Comerciais');
                    }
                    this.updateLCD();
                    return;
                }

                // 9.2 SUBMENU BUS: %TOTL
                if (this.currentMenu === 'BUS_PTOTL') {
                    const b = this.bus;
                    if (index === 0) { // TOTAL
                        b.total = this.getDisplayValue();
                        this.entry.isEntering = false;
                        this.setResult(b.total, `TOTAL = ${this.formatNum(b.total)}`);
                    } else if (index === 1) { // PART
                        b.part = this.getDisplayValue();
                        this.entry.isEntering = false;
                        this.setResult(b.part, `PARTE = ${this.formatNum(b.part)}`);
                    } else if (index === 2) { // %TOTL
                        if (b.total === 0) {
                            this.setError('Total não pode ser zero');
                        } else {
                            const pct = (b.part / b.total) * 100;
                            this.setResult(pct, `%TOTL = ${this.formatNum(pct)}%`);
                        }
                    } else if (index === 5) {
                        this.navigateToMenu('BUS', 'MENU BUS: Ferramentas Comerciais');
                    }
                    this.updateLCD();
                    return;
                }

                // 9.3 SUBMENU BUS: MU%C
                if (this.currentMenu === 'BUS_MUC') {
                    const b = this.bus;
                    if (index === 0) { // COST
                        b.cost = this.getDisplayValue();
                        this.entry.isEntering = false;
                        this.setResult(b.cost, `Custo = ${this.formatNum(b.cost)}`);
                    } else if (index === 1) { // PRICE
                        b.price = this.getDisplayValue();
                        this.entry.isEntering = false;
                        this.setResult(b.price, `Preço = ${this.formatNum(b.price)}`);
                    } else if (index === 2) { // MU%C
                        if (b.cost === 0) {
                            this.setError('Custo não pode ser zero');
                        } else {
                            const muc = ((b.price - b.cost) / b.cost) * 100;
                            this.setResult(muc, `MU%C = ${this.formatNum(muc)}%`);
                        }
                    } else if (index === 5) {
                        this.navigateToMenu('BUS', 'MENU BUS: Ferramentas Comerciais');
                    }
                    this.updateLCD();
                    return;
                }

                // 9.4 SUBMENU BUS: MU%P (Margem)
                if (this.currentMenu === 'BUS_MUP') {
                    const b = this.bus;
                    if (index === 0) { // COST
                        b.cost = this.getDisplayValue();
                        this.entry.isEntering = false;
                        this.setResult(b.cost, `Custo = ${this.formatNum(b.cost)}`);
                    } else if (index === 1) { // PRICE
                        b.price = this.getDisplayValue();
                        this.entry.isEntering = false;
                        this.setResult(b.price, `Preço = ${this.formatNum(b.price)}`);
                    } else if (index === 2) { // MARG
                        if (b.price === 0) {
                            this.setError('Preço não pode ser zero');
                        } else {
                            const marg = ((b.price - b.cost) / b.price) * 100;
                            this.setResult(marg, `Margem = ${this.formatNum(marg)}%`);
                        }
                    } else if (index === 5) {
                        this.navigateToMenu('BUS', 'MENU BUS: Ferramentas Comerciais');
                    }
                    this.updateLCD();
                    return;
                }

                // 10. MENU ESTATÍSTICA (SUM)
                if (this.currentMenu === 'SUM' || this.currentMenu === 'BUS_SUM') {
                    if (index === 5) {
                        this.navigateToMenu('MAIN', 'HP 17bII+ Menu Principal');
                        return;
                    }
                    switch (index) {
                        case 0: // Σ+
                            const x = this.getDisplayValue();
                            const y = this.mode === 'RPN' ? this.stack.y : 1;
                            if (!this.stats.pairs) this.stats.pairs = [];
                            this.stats.pairs.push({ x, y });
                            this.entry.isEntering = false;
                            this.renderStatPairsList();
                            this.setResult(this.stats.pairs.length, `SUM: n = ${this.stats.pairs.length} itens`);
                            break;
                        case 1: // Σ-
                            if (this.stats.pairs && this.stats.pairs.length > 0) {
                                this.stats.pairs.pop();
                                this.renderStatPairsList();
                                this.setResult(this.stats.pairs.length, `SUM: Item removido (n=${this.stats.pairs.length})`);
                            } else {
                                this.setResult(0, 'SUM: Nenhum dado na lista');
                            }
                            break;
                        case 2: // TOTAL
                            const tot = (this.stats.pairs || []).reduce((s, p) => s + p.x, 0);
                            this.setResult(tot, `SUM: Σx = ${this.formatNum(tot)}`);
                            break;
                        case 3: // MEAN
                            const sMean = this.computeStats();
                            if (!sMean) {
                                this.setError('Sem dados estatísticos');
                            } else {
                                this.setResult(sMean.meanX, `SUM: Média X̄ = ${this.formatNum(sMean.meanX)}`);
                            }
                            break;
                        case 4: // SDEV
                            const sSdev = this.computeStats();
                            if (!sSdev || sSdev.n < 2) {
                                this.setError('São necessários pelo menos 2 dados');
                            } else {
                                this.setResult(sSdev.sx, `SUM: Desvio Padrão Sx = ${this.formatNum(sSdev.sx, 4)}`);
                            }
                            break;
                    }
                    this.updateLCD();
                    return;
                }

                // 11. MENU TIME (Tempo e Relógio)
                if (this.currentMenu === 'TIME') {
                    if (index === 5) {
                        this.navigateToMenu('MAIN', 'HP 17bII+ Menu Principal');
                        return;
                    }
                    if (index === 0) { // CALC
                        const now = new Date();
                        this.setResult(now.getDate(), `TIME: Hoje é dia ${now.toLocaleDateString('pt-BR')}`);
                    }
                    this.updateLCD();
                    return;
                }

                // 12. MENU CURRX (Câmbio)
                if (this.currentMenu === 'CURRX') {
                    if (index === 5) {
                        this.navigateToMenu('MAIN', 'HP 17bII+ Menu Principal');
                        return;
                    }
                    const rates = (this.currx && this.currx.rates) ? this.currx.rates : { USD: 1.0, BRL: 5.65, EUR: 0.92, GBP: 0.78 };
                    const x = this.getDisplayValue();
                    switch (index) {
                        case 0: // USD
                            const inUsd = x / (rates.BRL || 5.65);
                            this.setResult(inUsd, `R$ ${this.formatNum(x)} => US$ ${this.formatNum(inUsd)}`, null, 'US$');
                            break;
                        case 1: // EUR
                            const inEur = (x / (rates.BRL || 5.65)) * (rates.EUR || 0.92);
                            this.setResult(inEur, `R$ ${this.formatNum(x)} => € ${this.formatNum(inEur)}`, null, '€');
                            break;
                        case 2: // GBP
                            const inGbp = (x / (rates.BRL || 5.65)) * (rates.GBP || 0.78);
                            this.setResult(inGbp, `R$ ${this.formatNum(x)} => £ ${this.formatNum(inGbp)}`, null, '£');
                            break;
                        case 3: // BRL
                            const inBrl = x * (rates.BRL || 5.65);
                            this.setResult(inBrl, `US$ ${this.formatNum(x)} => R$ ${this.formatNum(inBrl)}`, null, 'R$');
                            break;
                        case 4: // SET
                            if (this.entry.isEntering && x > 0) {
                                rates.BRL = x;
                                this.entry.isEntering = false;
                                this.setResult(x, `CURRX: Cotação USD/BRL fixada em ${this.formatNum(x)}`);
                            } else {
                                this.setResult(rates.BRL, `CURRX: Cotação USD/BRL = R$ ${this.formatNum(rates.BRL)}`);
                            }
                            break;
                    }
                    this.currx.rates = rates;
                    this.updateLCD();
                    return;
                }

                // 13. MENU DSP (Ajustes de Exibição)
                if (this.currentMenu === 'DSP') {
                    switch (index) {
                        case 0: // FIX (Cicla 2, 4, 6, 0)
                            const nextDec = this.decimals === 2 ? 4 : (this.decimals === 4 ? 6 : (this.decimals === 6 ? 0 : 2));
                            this.setDecimals(nextDec);
                            break;
                        case 1: // ALL (11 casas)
                            this.setDecimals(11);
                            break;
                        case 2: // .
                            document.getElementById('lcdLine1').textContent = 'Ponto decimal (.) ativado';
                            break;
                        case 3: // ,
                            document.getElementById('lcdLine1').textContent = 'Vírgula decimal (,) ativada';
                            break;
                        case 5: // MAIN
                            this.navigateToMenu('MAIN', 'HP 17bII+ Menu Principal');
                            break;
                    }
                    this.updateLCD();
                    return;
                }

                // 14. MENU MODES (Configurações Gerais)
                if (this.currentMenu === 'MODES') {
                    switch (index) {
                        case 0: // BEEP
                            this.toggleMobileFeedback();
                            break;
                        case 1: // PRNT
                            this.switchTab('TAPE');
                            this.navigateToMenu('TAPE', 'Histórico e Registradores');
                            break;
                        case 3: // ALG
                            this.setMode('ALG');
                            break;
                        case 4: // RPN
                            this.setMode('RPN');
                            break;
                        case 5: // MAIN
                            this.navigateToMenu('MAIN', 'HP 17bII+ Menu Principal');
                            break;
                    }
                    this.updateLCD();
                    return;
                }

                // 15. MENU MATH (Funções Matemáticas)
                if (this.currentMenu === 'MATH') {
                    const x = this.getDisplayValue();
                    switch (index) {
                        case 0: // LOG
                            if (x <= 0) {
                                this.setError('Log de número ≤ 0', `LOG(${this.formatNum(x)})`);
                            } else {
                                this.setResult(Math.log10(x), `LOG(${this.formatNum(x)})`);
                            }
                            break;
                        case 1: // 10^x
                            const p10 = Math.pow(10, x);
                            if (!isFinite(p10)) {
                                this.setError('Overflow em 10^x', `10^(${this.formatNum(x)})`);
                            } else {
                                this.setResult(p10, `10^(${this.formatNum(x)})`);
                            }
                            break;
                        case 2: // LN
                            if (x <= 0) {
                                this.setError('LN de número ≤ 0', `LN(${this.formatNum(x)})`);
                            } else {
                                this.setResult(Math.log(x), `LN(${this.formatNum(x)})`);
                            }
                            break;
                        case 3: // EXP
                            const expRes = Math.exp(x);
                            if (!isFinite(expRes)) {
                                this.setError('Overflow em EXP', `EXP(${this.formatNum(x)})`);
                            } else {
                                this.setResult(expRes, `EXP(${this.formatNum(x)})`);
                            }
                            break;
                        case 4: // N!
                            if (x < 0 || !Number.isInteger(x) || x > 170) {
                                this.setError('Fatorial inválido (0 a 170)', `(${this.formatNum(x)})!`);
                            } else {
                                let f = 1;
                                for (let i = 2; i <= x; i++) f *= i;
                                this.setResult(f, `(${x})! = ${this.formatNum(f)}`);
                            }
                            break;
                        case 5: // PI
                            this.setResult(Math.PI, 'π = 3,14159265359');
                            break;
                    }
                    this.updateLCD();
                    return;
                }

                // 16. MENU SOLVE (Equações)
                if (this.currentMenu === 'SOLVE') {
                    if (index < 5 && this.solve && this.solve.varNames && this.solve.varNames[index]) {
                        this.handleSolveSoftkey(this.solve.varNames[index]);
                        return;
                    }
                    if (index === 5) {
                        this.navigateToMenu('MAIN', 'HP 17bII+ Menu Principal');
                        return;
                    }
                }

                // 17. MENU TAPE (Fita)
                if (this.currentMenu === 'TAPE') {
                    if (index === 5) {
                        this.navigateToMenu('MAIN', 'HP 17bII+ Menu Principal');
                        return;
                    }
                    switch (index) {
                        case 0: this.copyTape(); break;
                        case 1: this.clearTape(); break;
                        case 2:
                            if (this.lastResult && Number.isFinite(this.lastResult.value)) {
                                this.setResult(this.lastResult.value, `RCL: ${this.formatNum(this.lastResult.value)}`);
                            }
                            break;
                        case 3:
                            this.pressKey('STO');
                            break;
                        case 4:
                            document.getElementById('lcdLine1').textContent = `REG: X=${this.formatNum(this.stack.x)} Y=${this.formatNum(this.stack.y)}`;
                            break;
                    }
                    this.updateLCD();
                    return;
                }

                this.updateLCD();
            },

            // Entrada Numérica Oficial HP 17bII+'''

    content = content.replace(old_sk_text, new_sk_text)
    print("✓ Block 2: Official softkeys hierarchy updated")

    # 3. Atualizar pressKey('EXIT'), pressKey('DSP'), pressKey('%')
    pk_match = re.search(r'if \(key === \'EXIT\'\) \{[\s\S]*?if \(key === \'CLR\'\) \{', content)
    if not pk_match:
        print("✗ Block 3: pressKey block not found via regex!")
        return False

    old_pk_text = pk_match.group(0)

    new_pk_text = '''if (key === 'EXIT') {
                    this.stoState = null;
                    this.stoOp = null;
                    this.rclState = false;
                    if (this.shiftActive) {
                        this.shiftActive = false;
                        this.currentMenu = 'MAIN';
                        this.menuStack = [];
                        document.getElementById('lcdLine1').textContent = 'HP 17bII+ Menu Principal';
                    } else {
                        if (Array.isArray(this.menuStack) && this.menuStack.length > 0) {
                            this.currentMenu = this.menuStack.pop();
                        } else {
                            this.currentMenu = 'MAIN';
                        }
                        document.getElementById('lcdLine1').textContent = this.getMenuTitle(this.currentMenu);
                    }
                    this.updateLCD();
                    return;
                }

                if (key === 'DSP') {
                    if (this.shiftActive) {
                        this.shiftActive = false;
                        this.navigateToMenu('MODES', 'MENU MODES: Configurações Gerais');
                    } else {
                        this.navigateToMenu('DSP', 'MENU DSP: Ajustes de Exibição');
                    }
                    return;
                }

                if (key === '%') {
                    if (this.shiftActive) {
                        this.shiftActive = false;
                        this.navigateToMenu('MATH', 'MENU MATH: Funções Matemáticas');
                    } else {
                        const x = this.getDisplayValue();
                        const y = this.stack.y;
                        const pct = (y * x) / 100;
                        if (!isFinite(pct) || isNaN(pct)) {
                            this.setError('Erro de cálculo', `${x}% de ${this.formatNum(y)}`);
                            return;
                        }
                        this.setResult(pct, `${x}% de ${this.formatNum(y)}`);
                    }
                    this.updateLCD();
                    return;
                }

                if (key === 'CLR') {'''

    content = content.replace(old_pk_text, new_pk_text)
    print("✓ Block 3: pressKey EXIT stack pop corrected")

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

