# -*- coding: utf-8 -*-
"""
Applies CFLO improvements:
1. Card 1 (Taxa Desconto I%): Unit (% a.a.), amber title, structured footer badge
2. Card 2 (VPL) & Card 3 (TIR): 2-line header with units, side-by-side recalculate/copy buttons
3. Header: Quick action button '↺ Limpar CFLO'
4. JS updates: setCfloNpvCalculated, setCfloIrrCalculated, clearCfloResults
5. Light mode CSS additions
"""

def update_cflo(path):
    with open(path, 'rb') as f:
        content = f.read().decode('utf-8')

    norm_c = content.replace('\r\n', '\n')

    # 1. Light mode CSS
    target_css = """        body.light-mode #workstation-left-wrapper #btn-copy-amort:hover,
        body.light-mode #workstation-left-wrapper #btn-csv-amort:hover {
            background-color: #e2e8f0 !important;
        }"""

    replacement_css = """        body.light-mode #workstation-left-wrapper #btn-copy-amort:hover,
        body.light-mode #workstation-left-wrapper #btn-csv-amort:hover {
            background-color: #e2e8f0 !important;
        }
        body.light-mode #workstation-left-wrapper #card-cflo-rate > div:last-child {
            background-color: #f1f5f9 !important;
            border-color: #cbd5e1 !important;
        }"""

    if target_css not in norm_c:
        print(f"Error: target_css not found in {path}")
        return False
    norm_c = norm_c.replace(target_css, replacement_css, 1)

    # 2. HTML panel-CFLO
    target_cflo_html = """                            <!-- PAINEL FLUXO DE CAIXA (CFLO) -->
                            <div id="panel-CFLO" role="tabpanel" aria-labelledby="tab-CFLO" tabindex="0" class="module-panel hidden flex flex-col gap-3">
                                <div class="flex items-center justify-between border-b border-slate-800 pb-2">
                                    <div>
                                        <h2 class="text-sm font-bold text-amber-400">Fluxo de caixa descontado</h2>
                                        <p class="text-[11px] text-slate-500 font-mono mt-0.5">CFLO · VPL e TIR</p>
                                    </div>
                                    <span class="text-xs text-slate-400 font-mono">Análise de investimento</span>
                                </div>
                                <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
                                    <div class="bg-slate-950 p-2.5 rounded-xl border border-slate-800 flex flex-col justify-between">
                                        <div>
                                            <div class="flex items-center justify-between mb-1">
                                                <label for="input-cflo-rate" class="text-[11px] font-mono text-slate-400 block font-bold">Taxa Desconto I% (Ano)</label>
                                                <span class="text-[10px] font-semibold text-slate-500">Dado CFLO</span>
                                            </div>
                                            <input type="text" inputmode="decimal" maxlength="10" autocomplete="off" spellcheck="false" id="input-cflo-rate" placeholder="Insira os dados" value="" oninput="app.handleNumericInput(this, {allowNegative:true, allowDecimal:true, maxLength:10}); app.syncCfloRate(this.value)" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-sm font-mono text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-amber-500/50">
                                        </div>
                                        <p class="text-[10px] text-slate-500 mt-2">Usada para calcular o VPL do fluxo.</p>
                                    </div>
                                    <div id="card-cflo-npv" class="calc-card-result bg-slate-950 p-2.5 rounded-xl border border-slate-800 transition-all flex flex-col justify-between">
                                        <div>
                                            <div class="flex items-center justify-between mb-1">
                                                <label for="input-cflo-npv" class="text-[11px] font-mono text-amber-400 font-bold block">VPL (NPV) · Valor Presente</label>
                                                <span id="role-cflo-npv" class="text-[10px] font-semibold text-slate-500">Métrica CFLO</span>
                                            </div>
                                            <input type="text" readonly id="input-cflo-npv" placeholder="Aguardando cálculo..." class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-sm font-mono text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-amber-500/50">
                                        </div>
                                        <div class="grid grid-cols-1 gap-1.5 mt-2">
                                            <button id="btn-cflo-npv" onclick="app.computeNPV()" class="w-full py-1.5 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold rounded text-xs font-mono transition">Calcular VPL (NPV)</button>
                                            <button id="copy-cflo-npv" type="button" onclick="app.copyFieldValue('input-cflo-npv', this)" class="hidden w-full py-1.5 inline-flex items-center justify-center gap-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded transition shadow-sm">
                                                <span aria-hidden="true">⧉</span> Copiar
                                            </button>
                                        </div>
                                    </div>
                                    <div id="card-cflo-irr" class="calc-card-result bg-slate-950 p-2.5 rounded-xl border border-slate-800 transition-all flex flex-col justify-between">
                                        <div>
                                            <div class="flex items-center justify-between mb-1">
                                                <label for="input-cflo-irr" class="text-[11px] font-mono text-sky-400 font-bold block">TIR (IRR) · Taxa Retorno</label>
                                                <span id="role-cflo-irr" class="text-[10px] font-semibold text-slate-500">Métrica CFLO</span>
                                            </div>
                                            <input type="text" readonly id="input-cflo-irr" placeholder="Aguardando cálculo..." class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-sm font-mono text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-sky-500/50">
                                        </div>
                                        <div class="grid grid-cols-1 gap-1.5 mt-2">
                                            <button id="btn-cflo-irr" onclick="app.computeIRR()" class="w-full py-1.5 bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold rounded text-xs font-mono transition">Calcular TIR (IRR)</button>
                                            <button id="copy-cflo-irr" type="button" onclick="app.copyFieldValue('input-cflo-irr', this)" class="hidden w-full py-1.5 inline-flex items-center justify-center gap-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded transition shadow-sm">
                                                <span aria-hidden="true">⧉</span> Copiar
                                            </button>
                                        </div>
                                    </div>
                                </div>"""

    replacement_cflo_html = """                            <!-- PAINEL FLUXO DE CAIXA (CFLO) -->
                            <div id="panel-CFLO" role="tabpanel" aria-labelledby="tab-CFLO" tabindex="0" class="module-panel hidden flex flex-col gap-3">
                                <div class="flex items-center justify-between border-b border-slate-800 pb-2">
                                    <div>
                                        <h2 class="text-sm font-bold text-amber-400">Fluxo de caixa descontado</h2>
                                        <p class="text-[11px] text-slate-500 font-mono mt-0.5">CFLO · VPL e TIR</p>
                                    </div>
                                    <div class="flex items-center gap-2">
                                        <button type="button" onclick="app.clearActiveModule('CFLO')" title="Limpar taxa de desconto, fluxos e resultados de CFLO" class="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-mono font-semibold bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-white border border-slate-700 transition">
                                            <span aria-hidden="true">↺</span> Limpar CFLO
                                        </button>
                                        <span class="text-xs text-slate-400 font-mono hidden sm:inline">Análise de investimento</span>
                                    </div>
                                </div>
                                <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
                                    <div id="card-cflo-rate" class="bg-slate-950 p-2.5 rounded-xl border border-slate-800 flex flex-col justify-between">
                                        <div>
                                            <div class="flex items-start justify-between mb-1 gap-1">
                                                <div class="min-w-0">
                                                    <label for="input-cflo-rate" class="text-[11px] font-mono text-amber-400 font-bold block truncate">Taxa Desconto (I%)</label>
                                                    <span class="text-[10px] text-slate-400 font-mono">Unid: <strong class="text-slate-300 font-normal">% a.a.</strong></span>
                                                </div>
                                                <span class="text-[10px] font-semibold text-slate-500 shrink-0 text-right mt-0.5">Dado CFLO</span>
                                            </div>
                                            <input type="text" inputmode="decimal" maxlength="10" autocomplete="off" spellcheck="false" id="input-cflo-rate" placeholder="Insira os dados" value="" oninput="app.handleNumericInput(this, {allowNegative:true, allowDecimal:true, maxLength:10}); app.syncCfloRate(this.value)" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-sm font-mono text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-amber-500/50">
                                        </div>
                                        <div class="mt-2 py-1 px-2 rounded-lg bg-slate-900 border border-slate-800 text-[11px] font-mono text-slate-400 flex items-center justify-between">
                                            <span class="text-slate-400">Aplicação</span>
                                            <span class="text-amber-400 font-semibold text-[10px]">Cálculo do VPL</span>
                                        </div>
                                    </div>
                                    <div id="card-cflo-npv" class="calc-card-result bg-slate-950 p-2.5 rounded-xl border border-slate-800 transition-all flex flex-col justify-between">
                                        <div>
                                            <div class="flex items-start justify-between mb-1 gap-1">
                                                <div class="min-w-0">
                                                    <label for="input-cflo-npv" class="text-[11px] font-mono text-amber-400 font-bold block truncate">VPL (NPV)</label>
                                                    <span class="text-[10px] text-slate-400 font-mono">Unid: <strong class="text-slate-300 font-normal">R$</strong></span>
                                                </div>
                                                <span id="role-cflo-npv" class="text-[10px] font-semibold text-slate-500 shrink-0 text-right mt-0.5">Métrica CFLO</span>
                                            </div>
                                            <input type="text" readonly id="input-cflo-npv" placeholder="Aguardando cálculo..." class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-sm font-mono text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-amber-500/50">
                                        </div>
                                        <div class="grid grid-cols-1 gap-1.5 mt-2" id="actions-cflo-npv">
                                            <button id="btn-cflo-npv" onclick="app.computeNPV()" class="w-full py-1 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold rounded text-xs font-mono transition">Calcular VPL</button>
                                            <button id="copy-cflo-npv" type="button" onclick="app.copyFieldValue('input-cflo-npv', this)" class="hidden w-full py-1 px-1 inline-flex items-center justify-center gap-1 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-[11px] sm:text-xs rounded transition shadow-sm text-center truncate">
                                                <span aria-hidden="true">⧉</span> Copiar
                                            </button>
                                        </div>
                                    </div>
                                    <div id="card-cflo-irr" class="calc-card-result bg-slate-950 p-2.5 rounded-xl border border-slate-800 transition-all flex flex-col justify-between">
                                        <div>
                                            <div class="flex items-start justify-between mb-1 gap-1">
                                                <div class="min-w-0">
                                                    <label for="input-cflo-irr" class="text-[11px] font-mono text-sky-400 font-bold block truncate">TIR (IRR)</label>
                                                    <span class="text-[10px] text-slate-400 font-mono">Unid: <strong class="text-slate-300 font-normal">%</strong></span>
                                                </div>
                                                <span id="role-cflo-irr" class="text-[10px] font-semibold text-slate-500 shrink-0 text-right mt-0.5">Métrica CFLO</span>
                                            </div>
                                            <input type="text" readonly id="input-cflo-irr" placeholder="Aguardando cálculo..." class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-sm font-mono text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-sky-500/50">
                                        </div>
                                        <div class="grid grid-cols-1 gap-1.5 mt-2" id="actions-cflo-irr">
                                            <button id="btn-cflo-irr" onclick="app.computeIRR()" class="w-full py-1 bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold rounded text-xs font-mono transition">Calcular TIR</button>
                                            <button id="copy-cflo-irr" type="button" onclick="app.copyFieldValue('input-cflo-irr', this)" class="hidden w-full py-1 px-1 inline-flex items-center justify-center gap-1 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-[11px] sm:text-xs rounded transition shadow-sm text-center truncate">
                                                <span aria-hidden="true">⧉</span> Copiar
                                            </button>
                                        </div>
                                    </div>
                                </div>"""

    if target_cflo_html not in norm_c:
        print(f"Error: target_cflo_html not found in {path}")
        return False
    norm_c = norm_c.replace(target_cflo_html, replacement_cflo_html, 1)

    # 3. JS methods
    target_cflo_js = """            setCfloNpvCalculated(npv) {
                const card = document.getElementById('card-cflo-npv');
                const input = document.getElementById('input-cflo-npv');
                const role = document.getElementById('role-cflo-npv');
                const btn = document.getElementById('btn-cflo-npv');
                const copyBtn = document.getElementById('copy-cflo-npv');
                if (input) input.value = `R$ ${this.formatNum(npv)}`;
                if (card) card.classList.add('is-result');
                if (input) input.classList.add('is-result-field');
                if (role) {
                    role.textContent = '✓ Resultado calculado';
                    role.className = 'text-[10px] font-bold text-emerald-400';
                }
                if (btn) {
                    btn.textContent = '↻ Recalcular VPL';
                    btn.className = 'w-full py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded text-xs font-mono font-bold transition';
                }
                if (copyBtn) copyBtn.classList.remove('hidden');
            },

            setCfloIrrCalculated(irrPct) {
                const card = document.getElementById('card-cflo-irr');
                const input = document.getElementById('input-cflo-irr');
                const role = document.getElementById('role-cflo-irr');
                const btn = document.getElementById('btn-cflo-irr');
                const copyBtn = document.getElementById('copy-cflo-irr');
                if (input) input.value = `${this.formatNum(irrPct)}%`;
                if (card) card.classList.add('is-result');
                if (input) input.classList.add('is-result-field');
                if (role) {
                    role.textContent = '✓ Resultado calculado';
                    role.className = 'text-[10px] font-bold text-emerald-400';
                }
                if (btn) {
                    btn.textContent = '↻ Recalcular TIR';
                    btn.className = 'w-full py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded text-xs font-mono font-bold transition';
                }
                if (copyBtn) copyBtn.classList.remove('hidden');
            },

            clearCfloResults() {
                ['npv', 'irr'].forEach(type => {
                    const card = document.getElementById(`card-cflo-${type}`);
                    const input = document.getElementById(`input-cflo-${type}`);
                    const role = document.getElementById(`role-cflo-${type}`);
                    const btn = document.getElementById(`btn-cflo-${type}`);
                    const copyBtn = document.getElementById(`copy-cflo-${type}`);
                    if (card) card.classList.remove('is-result');
                    if (input) {
                        input.classList.remove('is-result-field');
                        input.value = '';
                    }
                    if (role) {
                        role.textContent = 'Métrica CFLO';
                        role.className = 'text-[10px] font-semibold text-slate-500';
                    }
                    if (btn) {
                        btn.textContent = type === 'npv' ? 'Calcular VPL (NPV)' : 'Calcular TIR (IRR)';
                        btn.className = `w-full py-1.5 ${type === 'npv' ? 'bg-amber-500 hover:bg-amber-400' : 'bg-sky-500 hover:bg-sky-400'} text-slate-950 font-bold rounded text-xs font-mono transition`;
                    }
                    if (copyBtn) copyBtn.classList.add('hidden');
                });
            },"""

    replacement_cflo_js = """            setCfloNpvCalculated(npv) {
                const card = document.getElementById('card-cflo-npv');
                const input = document.getElementById('input-cflo-npv');
                const role = document.getElementById('role-cflo-npv');
                const btn = document.getElementById('btn-cflo-npv');
                const copyBtn = document.getElementById('copy-cflo-npv');
                const actions = document.getElementById('actions-cflo-npv');
                if (input) input.value = `R$ ${this.formatNum(npv)}`;
                if (card) card.classList.add('is-result');
                if (input) input.classList.add('is-result-field');
                if (role) {
                    role.textContent = '✓ Resultado';
                    role.className = 'text-[10px] font-bold text-emerald-400 shrink-0 text-right mt-0.5';
                }
                if (actions) {
                    actions.className = 'grid grid-cols-2 gap-1.5 mt-2';
                }
                if (btn) {
                    btn.textContent = '↻ Recalcular';
                    btn.className = 'w-full py-1 px-1 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded text-[11px] sm:text-xs font-bold font-mono transition text-center truncate';
                }
                if (copyBtn) {
                    copyBtn.classList.remove('hidden');
                    copyBtn.className = 'w-full py-1 px-1 inline-flex items-center justify-center gap-1 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-[11px] sm:text-xs rounded transition shadow-sm text-center truncate';
                }
            },

            setCfloIrrCalculated(irrPct) {
                const card = document.getElementById('card-cflo-irr');
                const input = document.getElementById('input-cflo-irr');
                const role = document.getElementById('role-cflo-irr');
                const btn = document.getElementById('btn-cflo-irr');
                const copyBtn = document.getElementById('copy-cflo-irr');
                const actions = document.getElementById('actions-cflo-irr');
                if (input) input.value = `${this.formatNum(irrPct)}%`;
                if (card) card.classList.add('is-result');
                if (input) input.classList.add('is-result-field');
                if (role) {
                    role.textContent = '✓ Resultado';
                    role.className = 'text-[10px] font-bold text-emerald-400 shrink-0 text-right mt-0.5';
                }
                if (actions) {
                    actions.className = 'grid grid-cols-2 gap-1.5 mt-2';
                }
                if (btn) {
                    btn.textContent = '↻ Recalcular';
                    btn.className = 'w-full py-1 px-1 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded text-[11px] sm:text-xs font-bold font-mono transition text-center truncate';
                }
                if (copyBtn) {
                    copyBtn.classList.remove('hidden');
                    copyBtn.className = 'w-full py-1 px-1 inline-flex items-center justify-center gap-1 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-[11px] sm:text-xs rounded transition shadow-sm text-center truncate';
                }
            },

            clearCfloResults() {
                ['npv', 'irr'].forEach(type => {
                    const card = document.getElementById(`card-cflo-${type}`);
                    const input = document.getElementById(`input-cflo-${type}`);
                    const role = document.getElementById(`role-cflo-${type}`);
                    const btn = document.getElementById(`btn-cflo-${type}`);
                    const copyBtn = document.getElementById(`copy-cflo-${type}`);
                    const actions = document.getElementById(`actions-cflo-${type}`);
                    if (card) card.classList.remove('is-result');
                    if (input) {
                        input.classList.remove('is-result-field');
                        input.value = '';
                    }
                    if (role) {
                        role.textContent = 'Métrica CFLO';
                        role.className = 'text-[10px] font-semibold text-slate-500 shrink-0 text-right mt-0.5';
                    }
                    if (actions) {
                        actions.className = 'grid grid-cols-1 gap-1.5 mt-2';
                    }
                    if (btn) {
                        btn.textContent = type === 'npv' ? 'Calcular VPL' : 'Calcular TIR';
                        btn.className = `w-full py-1 ${type === 'npv' ? 'bg-amber-500 hover:bg-amber-400' : 'bg-sky-500 hover:bg-sky-400'} text-slate-950 font-bold rounded text-xs font-mono transition`;
                    }
                    if (copyBtn) copyBtn.classList.add('hidden');
                });
            },"""

    if target_cflo_js not in norm_c:
        print(f"Error: target_cflo_js not found in {path}")
        return False
    norm_c = norm_c.replace(target_cflo_js, replacement_cflo_js, 1)

    with open(path, 'wb') as f:
        f.write(norm_c.replace('\n', '\r\n').encode('utf-8'))

    print(f"Successfully updated {path}")
    return True

ok1 = update_cflo("Calculadora Financeira 17bIi.html")
ok2 = update_cflo("index.html")
if not (ok1 and ok2):
    import sys
    sys.exit(1)
print("CFLO updates applied to both files.")

