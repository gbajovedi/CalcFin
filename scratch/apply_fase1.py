import sys
sys.stdout.reconfigure(encoding='utf-8')
# -*- coding: utf-8 -*-
import os
import hashlib
import re

def run():
    target_path = 'Calculadora Financeira 17bIi.html'
    index_path = 'index.html'

    with open(target_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Painel TAPE: adicionar o grid de registradores R0-R9
    old_tape_panel = '''                                <div id="tape-content" class="bg-slate-950 border border-slate-800 rounded-xl p-3 font-mono text-xs text-amber-300 max-h-64 overflow-y-auto custom-scroll space-y-1">
                                    <!-- Entradas da fita -->
                                </div>
                            </div>'''

    new_tape_panel = '''                                <div id="tape-content" class="bg-slate-950 border border-slate-800 rounded-xl p-3 font-mono text-xs text-amber-300 max-h-56 overflow-y-auto custom-scroll space-y-1">
                                    <!-- Entradas da fita -->
                                </div>
                                <div class="border-t border-slate-800 pt-3">
                                    <div class="flex items-center justify-between mb-2">
                                        <h3 class="text-xs font-bold text-sky-400 font-mono flex items-center gap-1.5">
                                            <span>💾</span> Registradores de Armazenamento (R0 a R9)
                                        </h3>
                                        <button type="button" onclick="app.clearRegisters()" class="px-2 py-0.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 hover:text-white text-[10px] rounded font-mono transition">Zerar Registradores</button>
                                    </div>
                                    <div id="tape-registers-grid" class="grid grid-cols-2 sm:grid-cols-5 gap-1.5 font-mono text-xs">
                                        <!-- R0 a R9 cards gerados dinamicamente -->
                                    </div>
                                </div>
                            </div>'''

    if old_tape_panel in content:
        content = content.replace(old_tape_panel, new_tape_panel)
        print("✓ Block 1: panel-TAPE updated")
    else:
        print("✗ Block 1: old_tape_panel not found!")
        return False

    # 2. Configurações e Registradores no objeto app
    old_app_header = '''        const app = {
            // Configurações e Registradores
            mode: 'RPN', // 'RPN' ou 'ALG'
            shiftActive: false,
            decimals: 2,
            currentMenu: 'SOLVE', // 'MAIN', 'MATH', 'MODES', 'SOLVE'

            // Feedback Tátil e Sonoro (apenas em modo celular)
            audioCtx: null,
            mobileFeedbackEnabled: true,
            _lastFeedbackTime: 0,
            
            // Pilha RPN (X, Y, Z, T, LastX)
            stack: {
                x: 0,
                y: 0,
                z: 0,
                t: 0,
                lastX: 0
            },
            
            // Estado de Digitação
            entry: {
                buffer: '0',
                isEntering: false,
                hasDot: false
            },

            // Modo Algébrico
            alg: {
                pendingOp: null,
                operand1: 0
            },'''

    new_app_header = '''        const app = {
            // Configurações e Registradores Oficiais HP 17bII+
            mode: 'RPN', // 'RPN' ou 'ALG'
            shiftActive: false,
            decimals: 2,
            currentMenu: 'SOLVE', // 'MAIN', 'MATH', 'MODES', 'SOLVE'
            registers: new Array(10).fill(0), // Registradores 0 a 9 de armazenamento oficial
            stoState: null, // null ou 'pending'
            stoOp: null, // null, '+', '-', '*', '/'
            rclState: false, // true quando aguarda dígito de registrador 0-9
            stackLift: true, // Controle de Stack Lift da pilha RPN

            // Feedback Tátil e Sonoro (apenas em modo celular)
            audioCtx: null,
            mobileFeedbackEnabled: true,
            _lastFeedbackTime: 0,
            
            // Pilha RPN (X, Y, Z, T, LastX)
            stack: {
                x: 0,
                y: 0,
                z: 0,
                t: 0,
                lastX: 0
            },
            
            // Estado de Digitação
            entry: {
                buffer: '0',
                isEntering: false,
                hasDot: false
            },

            // Modo Algébrico Oficial com Suporte a Parênteses
            alg: {
                pendingOp: null,
                operand1: 0,
                parenStack: []
            },'''

    if old_app_header in content:
        content = content.replace(old_app_header, new_app_header)
        print("✓ Block 2: app header updated")
    else:
        print("✗ Block 2: old_app_header not found!")
        return False

    # 3. Chamar renderTapeRegisters em init()
    old_init_render = '''                this.renderCatalog();
                this.renderCashFlows();
                this.renderStatPairsList();'''

    new_init_render = '''                this.renderCatalog();
                this.renderCashFlows();
                this.renderStatPairsList();
                this.renderTapeRegisters();'''

    if old_init_render in content:
        content = content.replace(old_init_render, new_init_render)
        print("✓ Block 3: init renderTapeRegisters added")
    else:
        print("✗ Block 3: old_init_render not found!")
        return False

    # 4. Métodos centrais: pressDigit até toggleShift
    key_methods_match = re.search(r'            // Entrada Num[^\n]*\n\s*pressDigit\(d\) \{[\s\S]*?\n\s*toggleShift\(\) \{', content)
    if not key_methods_match:
        print("✗ Block 4: key methods block not found via regex!")
        return False

    matched_text = key_methods_match.group(0)

    middle_match = re.search(r'(renderResultPanel\(\) \{[\s\S]*?recalculateLastResult\(\) \{[\s\S]*?\n\s*\},)', matched_text)
    if not middle_match:
        print("✗ Block 4: middle methods (result panel) not found!")
        return False
    middle_methods = middle_match.group(1)

    part1 = '''            // Entrada Numérica Oficial HP 17bII+
            pressDigit(d) {
                this.triggerKeyFeedback();

                // Armazenamento em Registrador: STO [0-9] ou STO [op] [0-9]
                if (this.stoState === 'pending') {
                    const regIdx = parseInt(d, 10);
                    const x = this.getDisplayValue();
                    if (this.stoOp) {
                        let oldVal = this.registers[regIdx] || 0;
                        let newVal = oldVal;
                        if (this.stoOp === '+') newVal = oldVal + x;
                        else if (this.stoOp === '-') newVal = oldVal - x;
                        else if (this.stoOp === '*') newVal = oldVal * x;
                        else if (this.stoOp === '/') {
                            if (x === 0) {
                                this.setError('Divisão por zero em STO');
                                this.stoState = null;
                                this.stoOp = null;
                                return;
                            }
                            newVal = oldVal / x;
                        }
                        this.registers[regIdx] = this.cleanFloat(newVal, 10, newVal);
                        const desc = `STO ${this.stoOp} R${regIdx} = ${this.formatNum(newVal)}`;
                        document.getElementById('lcdLine1').textContent = desc;
                        this.addTapeEntry(desc);
                    } else {
                        this.registers[regIdx] = x;
                        const desc = `STO R${regIdx} = ${this.formatNum(x)}`;
                        document.getElementById('lcdLine1').textContent = desc;
                        this.addTapeEntry(desc);
                    }
                    this.stoState = null;
                    this.stoOp = null;
                    this.renderTapeRegisters();
                    this.saveWorkspaceState();
                    this.updateLCD();
                    return;
                }

                // Recuperação de Registrador: RCL [0-9]
                if (this.rclState) {
                    const regIdx = parseInt(d, 10);
                    const val = this.registers[regIdx] || 0;
                    this.rclState = false;
                    if (this.mode === 'RPN') {
                        if (this.entry.isEntering) {
                            this.stack.t = this.stack.z;
                            this.stack.z = this.stack.y;
                            this.stack.y = this.getDisplayValue();
                        } else if (this.stackLift) {
                            this.stack.t = this.stack.z;
                            this.stack.z = this.stack.y;
                            this.stack.y = this.stack.x;
                        }
                        this.stack.x = val;
                        this.stackLift = true;
                    } else {
                        this.stack.x = val;
                    }
                    this.entry.buffer = String(val).replace('.', ',');
                    this.entry.isEntering = false;
                    this.entry.hasDot = String(val).includes('.');
                    const desc = `RCL R${regIdx} = ${this.formatNum(val)}`;
                    document.getElementById('lcdLine1').textContent = desc;
                    this.addTapeEntry(desc);
                    this.updateLCD();
                    return;
                }

                // Sub-função MEM (Shift + 0)
                if (d === '0' && this.shiftActive) {
                    this.shiftActive = false;
                    document.getElementById('lcdLine1').textContent = 'Memória HP 17bII+';
                    const line2 = document.getElementById('lcdLine2');
                    if (line2) line2.textContent = 'MEM: 10 REG | DISP 100%';
                    this.addTapeEntry('MEM: 10 Registradores Disponíveis (R0-R9)');
                    this.updateLCD();
                    return;
                }

                // Digitação regular com controle de Stack Lift
                if (!this.entry.isEntering) {
                    if (this.mode === 'RPN') {
                        if (this.stackLift) {
                            this.stack.t = this.stack.z;
                            this.stack.z = this.stack.y;
                            this.stack.y = this.stack.x;
                        }
                        this.stackLift = true;
                    }
                    this.entry.buffer = d;
                    this.entry.isEntering = true;
                    this.entry.hasDot = false;
                } else {
                    if (this.entry.buffer === '0') {
                        this.entry.buffer = d;
                    } else if (this.entry.buffer.length < 16) {
                        this.entry.buffer += d;
                    }
                }
                this.updateLCD();
            },

            pressDot() {
                this.triggerKeyFeedback();
                // Sub-função SHOW (Shift + .) - Exibe os 12 dígitos reais sem formatação
                if (this.shiftActive) {
                    this.shiftActive = false;
                    const x = this.getDisplayValue();
                    document.getElementById('lcdLine1').textContent = 'SHOW (Precisão Total 12 dígitos)';
                    const fullStr = Number.isFinite(x) ? String(x).replace('.', ',') : '0';
                    const line2 = document.getElementById('lcdLine2');
                    if (line2) line2.textContent = fullStr;
                    this.addTapeEntry(`SHOW: ${fullStr}`);
                    return;
                }
                if (this.stoState === 'pending') return;

                if (!this.entry.isEntering) {
                    if (this.mode === 'RPN') {
                        if (this.stackLift) {
                            this.stack.t = this.stack.z;
                            this.stack.z = this.stack.y;
                            this.stack.y = this.stack.x;
                        }
                        this.stackLift = true;
                    }
                    this.entry.buffer = '0,';
                    this.entry.isEntering = true;
                    this.entry.hasDot = true;
                } else if (!this.entry.hasDot && !this.entry.buffer.includes('E')) {
                    this.entry.buffer += ',';
                    this.entry.hasDot = true;
                }
                this.updateLCD();
            },

            getDisplayValue() {
                if (this.entry.isEntering) {
                    let str = this.entry.buffer.replace(',', '.');
                    if (str.endsWith('E') || str.endsWith('E-') || str.endsWith('E+')) {
                        str = str.replace(/E.*$/, '');
                    }
                    const val = parseFloat(str);
                    return isNaN(val) ? 0 : val;
                }
                return this.stack.x;
            },

            setError(msg, description = '') {
                this.entry.isEntering = false;
                this.entry.buffer = '0';
                this.entry.hasDot = false;
                this.stack.lastX = this.stack.x;
                this.stack.x = NaN;
                const descText = description || msg;
                document.getElementById('lcdLine1').textContent = msg;
                this.addTapeEntry(`${descText} => Erro (${msg})`);
                this.lastResult = {
                    value: NaN,
                    description: msg,
                    unit: '',
                    recalculate: null
                };
                this.renderResultPanel();
                this.updateLCD();
                this.saveWorkspaceState();
            },

            setResult(val, description = '', recalculate = null, unit = '', explicitLastX = null) {
                val = this.cleanFloat(val, Math.max(this.decimals, 6), NaN);
                if (explicitLastX !== null && !isNaN(explicitLastX)) {
                    this.stack.lastX = explicitLastX;
                } else if (this.stack.lastX === undefined || isNaN(this.stack.lastX)) {
                    this.stack.lastX = this.stack.x;
                }
                this.stack.x = val;
                this.entry.isEntering = false;
                this.entry.buffer = '0';
                this.entry.hasDot = false;

                if (description) {
                    document.getElementById('lcdLine1').textContent = description;
                    const formatted = this.formatNum(val);
                    this.addTapeEntry(`${description} => ${formatted}${unit && formatted !== 'Erro' ? ' ' + unit : ''}`);
                }
                this.lastResult = {
                    value: val,
                    description: description || 'Resultado da calculadora',
                    unit: unit || '',
                    recalculate: typeof recalculate === 'function' ? recalculate : null
                };
                this.renderResultPanel();
                this.updateLCD();
                this.saveWorkspaceState();
            },

            '''

    part2 = '''

            pressEnter() {
                this.triggerKeyFeedback();
                // Sub-função LAST (Shift + = ou Shift + INPUT)
                if (this.shiftActive) {
                    this.shiftActive = false;
                    const lastVal = Number.isFinite(this.stack.lastX) ? this.stack.lastX : 0;
                    if (this.mode === 'RPN') {
                        if (this.entry.isEntering) {
                            this.stack.t = this.stack.z;
                            this.stack.z = this.stack.y;
                            this.stack.y = this.getDisplayValue();
                        } else if (this.stackLift) {
                            this.stack.t = this.stack.z;
                            this.stack.z = this.stack.y;
                            this.stack.y = this.stack.x;
                        }
                        this.stack.x = lastVal;
                        this.stackLift = true;
                    } else {
                        this.stack.x = lastVal;
                    }
                    this.entry.isEntering = false;
                    this.entry.buffer = String(lastVal).replace('.', ',');
                    this.entry.hasDot = String(lastVal).includes('.');
                    document.getElementById('lcdLine1').textContent = `LAST X = ${this.formatNum(lastVal)}`;
                    this.addTapeEntry(`LAST X = ${this.formatNum(lastVal)}`);
                    this.updateLCD();
                    return;
                }

                if (this.mode === 'RPN') {
                    const val = this.getDisplayValue();
                    this.stack.t = this.stack.z;
                    this.stack.z = this.stack.y;
                    this.stack.y = val;
                    this.stack.x = val;
                    this.entry.isEntering = false;
                    this.entry.buffer = '0';
                    this.entry.hasDot = false;
                    this.stackLift = false; // Desativa elevação automática para o próximo número imediato (HP standard)
                    document.getElementById('lcdLine1').textContent = `RPN: Enter ${this.formatNum(val)}`;
                    this.addTapeEntry(`ENTER: ${this.formatNum(val)}`);
                } else {
                    let currentVal = this.getDisplayValue();
                    if (Array.isArray(this.alg.parenStack)) {
                        while (this.alg.parenStack.length > 0) {
                            if (this.alg.pendingOp) {
                                currentVal = this.computeAlgOp(this.alg.pendingOp, this.alg.operand1, currentVal);
                            }
                            const parent = this.alg.parenStack.pop();
                            this.alg.operand1 = parent.operand1;
                            this.alg.pendingOp = parent.pendingOp;
                        }
                    }
                    if (this.alg.pendingOp) {
                        currentVal = this.computeAlgOp(this.alg.pendingOp, this.alg.operand1, currentVal);
                        this.alg.pendingOp = null;
                    }
                    this.stack.lastX = this.alg.operand1;
                    this.alg.operand1 = currentVal;
                    this.setResult(currentVal, `= ${this.formatNum(currentVal)}`);
                }
                this.updateLCD();
            },

            pressOp(op) {
                this.triggerKeyFeedback();

                // Aritmética de Registrador: STO + [0-9], STO - [0-9], STO * [0-9], STO / [0-9]
                if (this.stoState === 'pending' && !this.stoOp) {
                    if (['+', '-', '*', '/'].includes(op)) {
                        this.stoOp = op;
                        document.getElementById('lcdLine1').textContent = `STO ${op} _ (Digite 0-9)`;
                        this.updateLCD();
                        return;
                    }
                }

                // Funções Secundárias / Unárias com Shift (1/x, yˣ, √x, x²)
                if (this.shiftActive) {
                    this.shiftActive = false;
                    const x = this.getDisplayValue();
                    this.stack.lastX = x;
                    this.stackLift = true;
                    if (op === '/') {
                        if (x === 0) {
                            this.setError('Divisão por zero', '1/0');
                            return;
                        }
                        this.setResult(1 / x, `1/${this.formatNum(x)}`, null, '', x);
                        return;
                    }
                    if (op === '*') {
                        const y = this.stack.y;
                        if (y === 0 && x <= 0) {
                            this.setError('Indeterminação matemática', `0 ^ ${this.formatNum(x)}`);
                            return;
                        }
                        if (y < 0 && !Number.isInteger(x)) {
                            this.setError('Expoente não inteiro', `${this.formatNum(y)} ^ ${this.formatNum(x)}`);
                            return;
                        }
                        const res = Math.pow(y, x);
                        if (!isFinite(res) || isNaN(res)) {
                            this.setError('Indeterminação matemática', `${this.formatNum(y)} ^ ${this.formatNum(x)}`);
                            return;
                        }
                        this.setResult(res, `${this.formatNum(y)} ^ ${this.formatNum(x)}`, null, '', x);
                        return;
                    }
                    if (op === '-') {
                        if (x < 0) {
                            this.setError('Raiz de número negativo', `√(${this.formatNum(x)})`);
                            return;
                        }
                        this.setResult(Math.sqrt(x), `√(${this.formatNum(x)})`, null, '', x);
                        return;
                    }
                    if (op === '+') {
                        const res = x * x;
                        if (!isFinite(res)) {
                            this.setError('Overflow', `(${this.formatNum(x)})²`);
                            return;
                        }
                        this.setResult(res, `(${this.formatNum(x)})²`, null, '', x);
                        return;
                    }
                }

                if (this.mode === 'RPN') {
                    const x = this.getDisplayValue();
                    const y = this.stack.y;
                    this.stack.lastX = x;
                    this.stackLift = true;
                    if (op === '/' && x === 0) {
                        this.setError('Divisão por zero', `${this.formatNum(y)} / 0`);
                        return;
                    }
                    let res = 0;
                    switch (op) {
                        case '+': res = y + x; break;
                        case '-': res = y - x; break;
                        case '*': res = y * x; break;
                        case '/': res = y / x; break;
                    }
                    if (!isFinite(res) || isNaN(res)) {
                        this.setError('Indeterminação matemática', `${this.formatNum(y)} ${op} ${this.formatNum(x)}`);
                        return;
                    }
                    this.stack.x = res;
                    this.stack.y = this.stack.z;
                    this.stack.z = this.stack.t;
                    // Stack drop oficial HP: topo T permanece duplicado/preservado no registrador T
                    this.setResult(res, `${this.formatNum(y)} ${op} ${this.formatNum(x)}`, null, '', x);
                } else {
                    const currentVal = this.getDisplayValue();
                    this.stackLift = true;
                    if (this.alg.pendingOp) {
                        if (this.alg.pendingOp === '/' && currentVal === 0) {
                            this.setError('Divisão por zero', `${this.formatNum(this.alg.operand1)} / 0`);
                            this.alg.pendingOp = null;
                            return;
                        }
                        this.executeAlgOp(this.alg.pendingOp, this.alg.operand1, currentVal);
                    } else {
                        this.alg.operand1 = currentVal;
                    }
                    this.alg.pendingOp = op;
                    this.entry.isEntering = false;
                    document.getElementById('lcdLine1').textContent = `${this.formatNum(this.alg.operand1)} ${op}`;
                }
                this.updateLCD();
            },

            computeAlgOp(op, a, b) {
                if (op === '/' && b === 0) {
                    this.setError('Divisão por zero', `${this.formatNum(a)} / 0`);
                    return NaN;
                }
                let res = 0;
                switch (op) {
                    case '+': res = a + b; break;
                    case '-': res = a - b; break;
                    case '*': res = a * b; break;
                    case '/': res = a / b; break;
                    default: res = b; break;
                }
                if (!isFinite(res) || isNaN(res)) {
                    this.setError('Indeterminação matemática', `${this.formatNum(a)} ${op} ${this.formatNum(b)}`);
                    return NaN;
                }
                return this.cleanFloat(res, Math.max(this.decimals, 6), res);
            },

            executeAlgOp(op, a, b) {
                const res = this.computeAlgOp(op, a, b);
                if (!isNaN(res)) {
                    this.alg.operand1 = res;
                    this.setResult(res, `${this.formatNum(a)} ${op} ${this.formatNum(b)}`);
                }
            },

            pressKey(key) {
                this.triggerKeyFeedback();

                if (key === 'EXIT') {
                    this.stoState = null;
                    this.stoOp = null;
                    this.rclState = false;
                    if (this.shiftActive) {
                        this.shiftActive = false;
                        this.currentMenu = 'MAIN';
                        document.getElementById('lcdLine1').textContent = 'HP 17bII+ Menu Principal';
                    } else {
                        this.currentMenu = 'MAIN';
                        document.getElementById('lcdLine1').textContent = 'Menu Principal';
                    }
                    this.updateLCD();
                    return;
                }

                if (key === 'DSP') {
                    if (this.shiftActive) {
                        this.shiftActive = false;
                        this.currentMenu = 'MODES';
                    } else {
                        this.setDecimals(this.decimals === 2 ? 4 : (this.decimals === 4 ? 0 : 2));
                    }
                    this.updateLCD();
                    return;
                }

                if (key === '%') {
                    if (this.shiftActive) {
                        this.shiftActive = false;
                        this.currentMenu = 'MATH';
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

                if (key === 'CLR') {
                    this.stoState = null;
                    this.stoOp = null;
                    this.rclState = false;
                    if (this.shiftActive) {
                        this.shiftActive = false;
                        document.getElementById('lcdLine1').textContent = 'HP 17bII+ Desligada (OFF / Standby)';
                        this.updateLCD();
                        return;
                    }
                    this.entry.buffer = '0';
                    this.entry.isEntering = false;
                    this.entry.hasDot = false;
                    this.stack.x = 0;
                    this.stackLift = false;
                    if (this.mode === 'ALG') {
                        this.alg.pendingOp = null;
                        this.alg.operand1 = 0;
                        this.alg.parenStack = [];
                    }
                    document.getElementById('lcdLine1').textContent = 'Visor Limpo (CLR)';
                    this.updateLCD();
                    return;
                }

                if (key === 'BACKSPACE') {
                    if (this.stoState || this.rclState) {
                        this.stoState = null;
                        this.stoOp = null;
                        this.rclState = false;
                        document.getElementById('lcdLine1').textContent = 'Operação cancelada';
                        this.updateLCD();
                        return;
                    }
                    if (this.entry.isEntering) {
                        if (this.entry.buffer.length > 1) {
                            if (this.entry.buffer.slice(-1) === ',') this.entry.hasDot = false;
                            this.entry.buffer = this.entry.buffer.slice(0, -1);
                        } else {
                            this.entry.buffer = '0';
                            this.entry.isEntering = false;
                        }
                    } else {
                        this.stack.x = 0;
                    }
                    this.updateLCD();
                    return;
                }

                if (key === '+/-') {
                    // Sub-função E (Shift + +/-) - Expoente científico
                    if (this.shiftActive) {
                        this.shiftActive = false;
                        if (!this.entry.isEntering) {
                            this.entry.buffer = (this.stack.x ? String(this.stack.x).replace('.', ',') : '1') + 'E';
                            this.entry.isEntering = true;
                        } else if (!this.entry.buffer.includes('E')) {
                            this.entry.buffer += 'E';
                        }
                        document.getElementById('lcdLine1').textContent = 'Expoente Científico (E)';
                        this.updateLCD();
                        return;
                    }
                    if (this.entry.isEntering) {
                        if (this.entry.buffer.includes('E')) {
                            const parts = this.entry.buffer.split('E');
                            let exp = parts[1] || '';
                            if (exp.startsWith('-')) exp = exp.substring(1);
                            else exp = '-' + exp;
                            this.entry.buffer = parts[0] + 'E' + exp;
                        } else {
                            if (this.entry.buffer.startsWith('-')) this.entry.buffer = this.entry.buffer.substring(1);
                            else this.entry.buffer = '-' + this.entry.buffer;
                        }
                    } else {
                        this.setResult(-this.stack.x);
                    }
                    this.updateLCD();
                    return;
                }

                if (key === 'INPUT') {
                    // Sub-função CLR DATA (Shift + INPUT)
                    if (this.shiftActive) {
                        this.shiftActive = false;
                        this.clearActiveModuleFields();
                        document.getElementById('lcdLine1').textContent = 'DADOS LIMPOS (CLR DATA)';
                        this.addTapeEntry('CLR DATA: Dados do módulo limpos');
                        this.updateLCD();
                        return;
                    }
                    this.pressEnter();
                    return;
                }

                if (key === '(') {
                    if (this.shiftActive) {
                        this.shiftActive = false;
                        // Roll Down da pilha RPN
                        const oldX = this.stack.x;
                        this.stack.x = this.stack.y;
                        this.stack.y = this.stack.z;
                        this.stack.z = this.stack.t;
                        this.stack.t = oldX;
                        document.getElementById('lcdLine1').textContent = `Pilha R↓ (Roll Down): X=${this.formatNum(this.stack.x)}`;
                        this.updateLCD();
                        return;
                    }
                    if (this.mode === 'ALG') {
                        if (!Array.isArray(this.alg.parenStack)) this.alg.parenStack = [];
                        this.alg.parenStack.push({
                            operand1: this.alg.operand1,
                            pendingOp: this.alg.pendingOp
                        });
                        this.alg.operand1 = 0;
                        this.alg.pendingOp = null;
                        this.entry.buffer = '0';
                        this.entry.isEntering = false;
                        this.entry.hasDot = false;
                        const depth = this.alg.parenStack.length;
                        document.getElementById('lcdLine1').textContent = `( nível ${depth}`;
                        this.updateLCD();
                    }
                    return;
                }

                if (key === ')') {
                    if (this.shiftActive) {
                        this.shiftActive = false;
                        // SWAP X e Y
                        const tmp = this.stack.x;
                        this.stack.x = this.stack.y;
                        this.stack.y = tmp;
                        document.getElementById('lcdLine1').textContent = `Troca X⇄Y (SWAP): X=${this.formatNum(this.stack.x)} Y=${this.formatNum(this.stack.y)}`;
                        this.updateLCD();
                        return;
                    }
                    if (this.mode === 'ALG') {
                        if (!Array.isArray(this.alg.parenStack) || this.alg.parenStack.length === 0) {
                            document.getElementById('lcdLine1').textContent = 'Nenhum parêntese aberto';
                            return;
                        }
                        let currentVal = this.getDisplayValue();
                        if (this.alg.pendingOp) {
                            currentVal = this.computeAlgOp(this.alg.pendingOp, this.alg.operand1, currentVal);
                        }
                        const parent = this.alg.parenStack.pop();
                        this.alg.operand1 = parent.operand1;
                        this.alg.pendingOp = parent.pendingOp;
                        this.stack.x = currentVal;
                        this.entry.buffer = String(currentVal).replace('.', ',');
                        this.entry.isEntering = false;
                        this.entry.hasDot = String(currentVal).includes('.');
                        document.getElementById('lcdLine1').textContent = `) resultado: ${this.formatNum(currentVal)}`;
                        this.updateLCD();
                    }
                    return;
                }

                if (key === 'UP') {
                    if (this.mode === 'RPN') {
                        // Roll Up (R↑) da pilha RPN
                        const oldX = this.stack.x;
                        this.stack.x = this.stack.t;
                        this.stack.t = this.stack.z;
                        this.stack.z = this.stack.y;
                        this.stack.y = oldX;
                        document.getElementById('lcdLine1').textContent = `Pilha R↑ (Roll Up): X=${this.formatNum(this.stack.x)}`;
                        this.updateLCD();
                    }
                    return;
                }

                if (key === 'DOWN') {
                    if (this.mode === 'RPN') {
                        // Roll Down (R↓) da pilha RPN
                        const oldX = this.stack.x;
                        this.stack.x = this.stack.y;
                        this.stack.y = this.stack.z;
                        this.stack.z = this.stack.t;
                        this.stack.t = oldX;
                        document.getElementById('lcdLine1').textContent = `Pilha R↓ (Roll Down): X=${this.formatNum(this.stack.x)}`;
                        this.updateLCD();
                    }
                    return;
                }

                if (key === 'STO') {
                    this.stoState = 'pending';
                    this.stoOp = null;
                    this.rclState = false;
                    document.getElementById('lcdLine1').textContent = 'STO _ (Digite 0-9 ou +, -, *, /)';
                    this.updateLCD();
                    return;
                }

                if (key === 'RCL') {
                    // Sub-função RND (Shift + RCL) - Arredonda X para as casas decimais ativas
                    if (this.shiftActive) {
                        this.shiftActive = false;
                        const x = this.getDisplayValue();
                        const rounded = this.cleanFloat(x, this.decimals, x);
                        this.setResult(rounded, `RND: ${this.formatNum(rounded)}`);
                        return;
                    }
                    this.rclState = true;
                    this.stoState = null;
                    this.stoOp = null;
                    document.getElementById('lcdLine1').textContent = 'RCL _ (Digite 0-9)';
                    this.updateLCD();
                    return;
                }
            },

            toggleShift() {'''

    new_key_methods = part1 + middle_methods + part2
    content = content.replace(matched_text, new_key_methods)
    print("✓ Block 4: key methods overhaul applied")

    # 5. Adicionar renderTapeRegisters, storeToRegister, recallFromRegister, clearRegisters
    old_clear_tape = '''            clearTape() {
                this.tape = [];
                const container = document.getElementById('tape-content');
                if (container) container.innerHTML = '';
                this.saveWorkspaceState();
            },'''

    new_clear_tape = '''            clearTape() {
                this.tape = [];
                const container = document.getElementById('tape-content');
                if (container) container.innerHTML = '';
                this.saveWorkspaceState();
            },

            // Gestão dos 10 Registradores de Armazenamento Oficial (R0 a R9)
            renderTapeRegisters() {
                const grid = document.getElementById('tape-registers-grid');
                if (!grid) return;
                if (!Array.isArray(this.registers) || this.registers.length < 10) {
                    this.registers = new Array(10).fill(0);
                }
                grid.innerHTML = this.registers.map((val, i) => `
                    <div class="bg-slate-900/90 border border-slate-800 rounded-lg p-1.5 flex flex-col justify-between">
                        <div class="flex items-center justify-between text-[10px] text-slate-400 font-bold mb-1">
                            <span class="text-amber-400 font-mono">R${i}</span>
                            <div class="flex items-center gap-1">
                                <button type="button" onclick="app.storeToRegister(${i})" title="Armazenar valor de X no registrador R${i}" class="px-1 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-sky-400 text-[9px] font-mono transition">STO</button>
                                <button type="button" onclick="app.recallFromRegister(${i})" title="Recuperar registrador R${i} para o visor" class="px-1 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-emerald-400 text-[9px] font-mono transition">RCL</button>
                            </div>
                        </div>
                        <div class="text-right text-xs font-mono text-slate-200 truncate" title="${val}">
                            ${this.formatNum(val)}
                        </div>
                    </div>
                `).join('');
            },

            storeToRegister(i) {
                const x = this.getDisplayValue();
                this.registers[i] = x;
                const msg = `STO R${i} = ${this.formatNum(x)}`;
                document.getElementById('lcdLine1').textContent = msg;
                this.addTapeEntry(msg);
                this.renderTapeRegisters();
                this.saveWorkspaceState();
                this.updateLCD();
            },

            recallFromRegister(i) {
                const val = this.registers[i] || 0;
                if (this.mode === 'RPN') {
                    if (this.entry.isEntering) {
                        this.stack.t = this.stack.z;
                        this.stack.z = this.stack.y;
                        this.stack.y = this.getDisplayValue();
                    } else if (this.stackLift) {
                        this.stack.t = this.stack.z;
                        this.stack.z = this.stack.y;
                        this.stack.y = this.stack.x;
                    }
                    this.stack.x = val;
                    this.stackLift = true;
                } else {
                    this.stack.x = val;
                }
                this.entry.buffer = String(val).replace('.', ',');
                this.entry.isEntering = false;
                this.entry.hasDot = String(val).includes('.');
                const msg = `RCL R${i} = ${this.formatNum(val)}`;
                document.getElementById('lcdLine1').textContent = msg;
                this.addTapeEntry(msg);
                this.updateLCD();
            },

            clearRegisters() {
                this.registers = new Array(10).fill(0);
                this.renderTapeRegisters();
                this.saveWorkspaceState();
                document.getElementById('lcdLine1').textContent = 'Registradores R0 a R9 zerados';
                this.addTapeEntry('Registradores R0-R9 zerados');
                this.updateLCD();
            },'''

    if old_clear_tape in content:
        content = content.replace(old_clear_tape, new_clear_tape)
        print("✓ Block 5: register helper methods added")
    else:
        print("✗ Block 5: old_clear_tape not found!")
        return False

    # 6. Salvar e carregar registradores em saveWorkspaceState e loadWorkspaceState
    old_save_state = '''                        tape: Array.isArray(this.tape) ? this.tape.slice(0, 50) : [],
                        favorites: this.favoriteFormulas ? [...this.favoriteFormulas] : [],'''

    new_save_state = '''                        tape: Array.isArray(this.tape) ? this.tape.slice(0, 50) : [],
                        favorites: this.favoriteFormulas ? [...this.favoriteFormulas] : [],
                        registers: Array.isArray(this.registers) ? this.registers.slice(0, 10).map(v => Number.isFinite(v) ? v : 0) : new Array(10).fill(0),'''

    if old_save_state in content:
        content = content.replace(old_save_state, new_save_state)
        print("✓ Block 6: saveWorkspaceState registers added")
    else:
        print("✗ Block 6: old_save_state not found!")
        return False

    old_load_state = '''                    if (Array.isArray(state.tape)) {
                        this.tape = state.tape;
                    }'''

    new_load_state = '''                    if (Array.isArray(state.tape)) {
                        this.tape = state.tape;
                    }
                    if (Array.isArray(state.registers)) {
                        this.registers = state.registers.slice(0, 10).map(v => Number.isFinite(v) ? v : 0);
                        while (this.registers.length < 10) this.registers.push(0);
                    } else {
                        this.registers = new Array(10).fill(0);
                    }'''

    if old_load_state in content:
        content = content.replace(old_load_state, new_load_state)
        print("✓ Block 7: loadWorkspaceState registers added")
    else:
        print("✗ Block 7: old_load_state not found!")
        return False

    # 7. Atualizar resetToFactoryDefaults
    old_reset = '''                this.mode = 'RPN';
                this.decimals = 2;'''

    new_reset = '''                this.mode = 'RPN';
                this.decimals = 2;
                this.registers = new Array(10).fill(0);
                this.renderTapeRegisters();'''

    if old_reset in content:
        content = content.replace(old_reset, new_reset, 1)
        print("✓ Block 8: resetToFactoryDefaults updated")
    else:
        print("✗ Block 8: old_reset not found!")
        return False

    # 8. Atualizar ouvintes de teclado em setupKeyboardListeners
    old_keyboard = '''                    if (e.key >= '0' && e.key <= '9') {
                        e.preventDefault(); this.pressDigit(e.key);
                    } else if (e.key === '.' || e.key === ',') {
                        e.preventDefault(); this.pressDot();
                    } else if (e.key === 'Enter') {
                        // Enter em botões e links mantém sua ação nativa; no fundo da página opera a calculadora.
                        if (active && ['BUTTON', 'A', 'SUMMARY'].includes(activeTag)) return;
                        e.preventDefault(); this.pressEnter();
                    } else if (['+', '-', '*', '/'].includes(e.key)) {
                        e.preventDefault(); this.pressOp(e.key);
                    } else if (e.key === 'Backspace') {
                        e.preventDefault(); this.pressKey('BACKSPACE');
                    } else if (e.key === 'Escape') {
                        e.preventDefault(); this.pressKey('EXIT');
                    } else if (e.key.toLowerCase() === 'c' || e.key === 'Delete') {
                        e.preventDefault(); this.pressKey('CLR');
                    } else if (/^F[1-6]$/.test(e.key)) {
                        e.preventDefault(); this.pressSoftkey(Number(e.key.slice(1)) - 1);
                    } else if (e.key === '(' || e.key === ')') {
                        e.preventDefault(); this.pressKey(e.key);
                    }'''

    new_keyboard = '''                    if (e.key >= '0' && e.key <= '9') {
                        e.preventDefault(); this.pressDigit(e.key);
                    } else if (e.key === '.' || e.key === ',') {
                        e.preventDefault(); this.pressDot();
                    } else if (e.key === 'Enter' || e.key === '=') {
                        // Enter e igual (=) mantém ação nativa em botões/links; na calculadora executam a operação.
                        if (active && ['BUTTON', 'A', 'SUMMARY'].includes(activeTag)) return;
                        e.preventDefault(); this.pressEnter();
                    } else if (['+', '-', '*', '/'].includes(e.key)) {
                        e.preventDefault(); this.pressOp(e.key);
                    } else if (e.key === 'Backspace') {
                        e.preventDefault(); this.pressKey('BACKSPACE');
                    } else if (e.key === 'Escape') {
                        e.preventDefault(); this.pressKey('EXIT');
                    } else if (e.key.toLowerCase() === 'c' || e.key === 'Delete') {
                        e.preventDefault(); this.pressKey('CLR');
                    } else if (/^F[1-6]$/.test(e.key)) {
                        e.preventDefault(); this.pressSoftkey(Number(e.key.slice(1)) - 1);
                    } else if (e.key === '(' || e.key === ')') {
                        e.preventDefault(); this.pressKey(e.key);
                    } else if (e.key === 'ArrowUp') {
                        e.preventDefault(); this.pressKey('UP');
                    } else if (e.key === 'ArrowDown') {
                        e.preventDefault(); this.pressKey('DOWN');
                    }'''

    if old_keyboard in content:
        content = content.replace(old_keyboard, new_keyboard)
        print("✓ Block 9: setupKeyboardListeners updated (ArrowUp, ArrowDown, =)")
    else:
        print("✗ Block 9: old_keyboard not found!")
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
