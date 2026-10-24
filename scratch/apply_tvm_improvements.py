# -*- coding: utf-8 -*-
"""
Applies all 6 UI/UX improvements to TVM & Amortization:
1. Symmetry of TVM Cards (Recalcular + Copiar side-by-side in grid-cols-2)
2. Card P/YR with segmented control [ END | BGN ]
3. High contrast headers for Amortization table in light mode
4. Clear TVM quick action button
5. Copy Table (TSV) and Export CSV buttons for Amortization
6. Measurement units displayed in all TVM cards
"""

import sys

def update_file(path):
    with open(path, 'rb') as f:
        content = f.read().decode('utf-8')

    # Normalize to \n for uniform matching
    content = content.replace('\r\n', '\n')

    # 1. CSS update for thead and segmented buttons in light mode
    target_css = """        body.light-mode #workstation-left-wrapper #amort-table-foot {
            background-color: #f1f5f9 !important;
            border-top-color: #cbd5e1 !important;
            color: #0f172a !important;
        }"""

    replacement_css = """        body.light-mode #workstation-left-wrapper #panel-TVM table thead,
        body.light-mode #workstation-left-wrapper table thead {
            background-color: #f1f5f9 !important;
            border-bottom: 2px solid #cbd5e1 !important;
        }
        body.light-mode #workstation-left-wrapper #panel-TVM table thead th,
        body.light-mode #workstation-left-wrapper table thead th {
            color: #0f172a !important;
            font-weight: 700 !important;
            font-size: 11px !important;
        }
        body.light-mode #workstation-left-wrapper #tvm-regime-container > div:last-child {
            background-color: #e2e8f0 !important;
            border-color: #cbd5e1 !important;
        }
        body.light-mode #workstation-left-wrapper #btn-tvm-mode-end:not([class*="bg-sky-600"]),
        body.light-mode #workstation-left-wrapper #btn-tvm-mode-bgn:not([class*="bg-amber-600"]) {
            color: #64748b !important;
        }
        body.light-mode #workstation-left-wrapper #btn-tvm-mode-end:not([class*="bg-sky-600"]):hover,
        body.light-mode #workstation-left-wrapper #btn-tvm-mode-bgn:not([class*="bg-amber-600"]):hover {
            color: #0f172a !important;
        }
        body.light-mode #workstation-left-wrapper #btn-copy-amort,
        body.light-mode #workstation-left-wrapper #btn-csv-amort {
            background-color: #f1f5f9 !important;
            border-color: #cbd5e1 !important;
            color: #1e293b !important;
        }
        body.light-mode #workstation-left-wrapper #btn-copy-amort:hover,
        body.light-mode #workstation-left-wrapper #btn-csv-amort:hover {
            background-color: #e2e8f0 !important;
        }
        body.light-mode #workstation-left-wrapper #amort-table-foot {
            background-color: #f1f5f9 !important;
            border-top-color: #cbd5e1 !important;
            color: #0f172a !important;
        }"""

    if target_css not in content:
        print(f"Error: target_css not found in {path}")
        return False
    content = content.replace(target_css, replacement_css, 1)

    # 2. HTML update for panel-TVM
    target_tvm_html = """                                <div class="flex items-center justify-between border-b border-slate-800 pb-2">
                                    <div>
                                        <h2 class="text-sm font-bold text-sky-400">Matemática financeira</h2>
                                        <p class="text-[11px] text-slate-500 font-mono mt-0.5">TVM · Valor do dinheiro no tempo e amortização</p>
                                    </div>
                                    <span class="text-xs text-slate-400 font-mono">Softkeys F1–F5</span>
                                </div>
                                <div class="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
                                    <div id="card-tvm-N" class="calc-card-result bg-slate-950 p-2.5 rounded-xl border border-slate-800 transition-all flex flex-col justify-between">
                                        <div>
                                            <div class="flex items-center justify-between mb-1">
                                                <label for="input-tvm-N" class="text-[11px] font-mono text-sky-400 font-bold block">N (Períodos / F1)</label>
                                                <span id="role-tvm-N" class="text-[10px] font-semibold text-slate-500">Dado TVM</span>
                                            </div>
                                            <input type="text" inputmode="decimal" maxlength="10" autocomplete="off" spellcheck="false" id="input-tvm-N" placeholder="Insira os dados" value="" oninput="app.handleNumericInput(this, {allowNegative:false, allowDecimal:true, maxLength:10}); app.syncInputToState('tvm', 'N', this.value)" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-sm font-mono text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-sky-500/50">
                                        </div>
                                        <div class="grid grid-cols-1 gap-1.5 mt-2" id="actions-tvm-N">
                                            <button id="btn-tvm-N" onclick="app.calculateTVM('N')" class="w-full py-1 bg-sky-600 hover:bg-sky-500 text-white rounded text-xs font-bold transition">Calcular N</button>
                                            <button id="copy-tvm-N" type="button" onclick="app.copyFieldValue('input-tvm-N', this)" class="hidden w-full py-1 inline-flex items-center justify-center gap-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded transition shadow-sm">
                                                <span aria-hidden="true">⧉</span> Copiar
                                            </button>
                                        </div>
                                    </div>
                                    <div id="card-tvm-I" class="calc-card-result bg-slate-950 p-2.5 rounded-xl border border-slate-800 transition-all flex flex-col justify-between">
                                        <div>
                                            <div class="flex items-center justify-between mb-1">
                                                <label for="input-tvm-I" class="text-[11px] font-mono text-sky-400 font-bold block">I%YR (Taxa / F2)</label>
                                                <span id="role-tvm-I" class="text-[10px] font-semibold text-slate-500">Dado TVM</span>
                                            </div>
                                            <input type="text" inputmode="decimal" maxlength="10" autocomplete="off" spellcheck="false" id="input-tvm-I" placeholder="Insira os dados" value="" oninput="app.handleNumericInput(this, {allowNegative:true, allowDecimal:true, maxLength:10}); app.syncInputToState('tvm', 'I', this.value)" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-sm font-mono text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-sky-500/50">
                                        </div>
                                        <div class="grid grid-cols-1 gap-1.5 mt-2" id="actions-tvm-I">
                                            <button id="btn-tvm-I" onclick="app.calculateTVM('I')" class="w-full py-1 bg-sky-600 hover:bg-sky-500 text-white rounded text-xs font-bold transition">Calcular I%</button>
                                            <button id="copy-tvm-I" type="button" onclick="app.copyFieldValue('input-tvm-I', this)" class="hidden w-full py-1 inline-flex items-center justify-center gap-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded transition shadow-sm">
                                                <span aria-hidden="true">⧉</span> Copiar
                                            </button>
                                        </div>
                                    </div>
                                    <div id="card-tvm-PV" class="calc-card-result bg-slate-950 p-2.5 rounded-xl border border-slate-800 transition-all flex flex-col justify-between">
                                        <div>
                                            <div class="flex items-center justify-between mb-1">
                                                <label for="input-tvm-PV" class="text-[11px] font-mono text-sky-400 font-bold block">PV (Valor Pres. / F3)</label>
                                                <span id="role-tvm-PV" class="text-[10px] font-semibold text-slate-500">Dado TVM</span>
                                            </div>
                                            <input type="text" inputmode="decimal" maxlength="18" autocomplete="off" spellcheck="false" id="input-tvm-PV" placeholder="Insira os dados" value="" oninput="app.handleNumericInput(this, {allowNegative:true, allowDecimal:true, maxLength:18}); app.syncInputToState('tvm', 'PV', this.value)" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-sm font-mono text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-sky-500/50">
                                        </div>
                                        <div class="grid grid-cols-1 gap-1.5 mt-2" id="actions-tvm-PV">
                                            <button id="btn-tvm-PV" onclick="app.calculateTVM('PV')" class="w-full py-1 bg-sky-600 hover:bg-sky-500 text-white rounded text-xs font-bold transition">Calcular PV</button>
                                            <button id="copy-tvm-PV" type="button" onclick="app.copyFieldValue('input-tvm-PV', this)" class="hidden w-full py-1 inline-flex items-center justify-center gap-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded transition shadow-sm">
                                                <span aria-hidden="true">⧉</span> Copiar
                                            </button>
                                        </div>
                                    </div>
                                    <div id="card-tvm-PMT" class="calc-card-result bg-slate-950 p-2.5 rounded-xl border border-slate-800 transition-all flex flex-col justify-between">
                                        <div>
                                            <div class="flex items-center justify-between mb-1">
                                                <label for="input-tvm-PMT" class="text-[11px] font-mono text-sky-400 font-bold block">PMT (Parcela / F4)</label>
                                                <span id="role-tvm-PMT" class="text-[10px] font-semibold text-slate-500">Dado TVM</span>
                                            </div>
                                            <input type="text" inputmode="decimal" maxlength="18" autocomplete="off" spellcheck="false" id="input-tvm-PMT" placeholder="Insira os dados" value="" oninput="app.handleNumericInput(this, {allowNegative:true, allowDecimal:true, maxLength:18}); app.syncInputToState('tvm', 'PMT', this.value)" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-sm font-mono text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-sky-500/50">
                                        </div>
                                        <div class="grid grid-cols-1 gap-1.5 mt-2" id="actions-tvm-PMT">
                                            <button id="btn-tvm-PMT" onclick="app.calculateTVM('PMT')" class="w-full py-1 bg-sky-600 hover:bg-sky-500 text-white rounded text-xs font-bold transition">Calcular PMT</button>
                                            <button id="copy-tvm-PMT" type="button" onclick="app.copyFieldValue('input-tvm-PMT', this)" class="hidden w-full py-1 inline-flex items-center justify-center gap-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded transition shadow-sm">
                                                <span aria-hidden="true">⧉</span> Copiar
                                            </button>
                                        </div>
                                    </div>
                                    <div id="card-tvm-FV" class="calc-card-result bg-slate-950 p-2.5 rounded-xl border border-slate-800 transition-all flex flex-col justify-between">
                                        <div>
                                            <div class="flex items-center justify-between mb-1">
                                                <label for="input-tvm-FV" class="text-[11px] font-mono text-sky-400 font-bold block">FV (Valor Futuro / F5)</label>
                                                <span id="role-tvm-FV" class="text-[10px] font-semibold text-slate-500">Dado TVM</span>
                                            </div>
                                            <input type="text" inputmode="decimal" maxlength="18" autocomplete="off" spellcheck="false" id="input-tvm-FV" placeholder="Insira os dados" value="" oninput="app.handleNumericInput(this, {allowNegative:true, allowDecimal:true, maxLength:18}); app.syncInputToState('tvm', 'FV', this.value)" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-sm font-mono text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-sky-500/50">
                                        </div>
                                        <div class="grid grid-cols-1 gap-1.5 mt-2" id="actions-tvm-FV">
                                            <button id="btn-tvm-FV" onclick="app.calculateTVM('FV')" class="w-full py-1 bg-sky-600 hover:bg-sky-500 text-white rounded text-xs font-bold transition">Calcular FV</button>
                                            <button id="copy-tvm-FV" type="button" onclick="app.copyFieldValue('input-tvm-FV', this)" class="hidden w-full py-1 inline-flex items-center justify-center gap-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded transition shadow-sm">
                                                <span aria-hidden="true">⧉</span> Copiar
                                            </button>
                                        </div>
                                    </div>
                                    <div class="bg-slate-950 p-2.5 rounded-xl border border-slate-800 flex flex-col justify-between">
                                        <div>
                                            <div class="flex items-center justify-between mb-1">
                                                <label for="input-tvm-PYR" class="text-[11px] font-mono text-slate-300 font-bold block">P/YR (Períodos/Ano)</label>
                                                <span class="text-[10px] font-semibold text-slate-500">Config.</span>
                                            </div>
                                            <input type="text" inputmode="numeric" maxlength="3" autocomplete="off" spellcheck="false" id="input-tvm-PYR" placeholder="Insira os dados" value="12" oninput="app.handleNumericInput(this, {allowNegative:false, allowDecimal:false, maxLength:3}); app.syncInputToState('tvm', 'PYR', this.value)" onblur="if(!this.value||parseInt(this.value,10)<1){this.value='12';app.syncInputToState('tvm','PYR','12');}" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-sm font-mono text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-sky-500/50">
                                        </div>
                                        <button onclick="app.toggleBgnEnd()" class="w-full mt-2 py-1 bg-slate-800 hover:bg-slate-700 text-amber-400 rounded text-xs font-mono font-bold" id="btn-amort-mode-label">Modo: END</button>
                                    </div>
                                </div>
                                <div id="tvm-feedback" role="status" aria-live="polite" class="hidden rounded-lg border border-rose-500/30 bg-rose-950/20 px-3 py-2 text-xs text-rose-300"></div>

                                <!-- Tabela de Amortização -->
                                <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 mt-1">
                                    <div class="flex flex-wrap items-center justify-between gap-2 mb-2">
                                        <div class="flex items-center gap-2">
                                            <h3 class="text-xs font-mono font-bold text-emerald-400">Tabela de Amortização (AMRT)</h3>
                                            <span id="amort-bgn-indicator" class="text-[10px] font-mono font-bold px-1.5 py-0.5 rounded bg-slate-800 text-slate-300">Modo: END (Postecipado)</span>
                                        </div>
                                        <div class="flex items-center gap-2">
                                            <label class="text-[11px] font-mono text-slate-400 flex items-center gap-1">
                                                Exibir:
                                                <select id="amort-limit-select" onchange="app.generateAmortizationTable()" class="bg-slate-900 border border-slate-700 text-slate-200 rounded px-2 py-1 text-xs font-mono">
                                                    <option value="60" selected>60 parcelas</option>
                                                    <option value="120">120 parcelas</option>
                                                    <option value="360">360 parcelas</option>
                                                    <option value="all">Todas as parcelas</option>
                                                </select>
                                            </label>
                                            <button onclick="app.generateAmortizationTable()" class="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-xs font-bold transition">Gerar Tabela</button>
                                        </div>
                                    </div>"""

    replacement_tvm_html = """                                <div class="flex items-center justify-between border-b border-slate-800 pb-2">
                                    <div>
                                        <h2 class="text-sm font-bold text-sky-400">Matemática financeira</h2>
                                        <p class="text-[11px] text-slate-500 font-mono mt-0.5">TVM · Valor do dinheiro no tempo e amortização</p>
                                    </div>
                                    <div class="flex items-center gap-2">
                                        <button type="button" onclick="app.clearTvmModule()" title="Limpar todos os campos de TVM e amortização" class="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-mono font-semibold bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-white border border-slate-700 transition">
                                            <span aria-hidden="true">↺</span> Limpar TVM
                                        </button>
                                        <span class="text-xs text-slate-400 font-mono hidden sm:inline">Softkeys F1–F5</span>
                                    </div>
                                </div>
                                <div class="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
                                    <div id="card-tvm-N" class="calc-card-result bg-slate-950 p-2.5 rounded-xl border border-slate-800 transition-all flex flex-col justify-between">
                                        <div>
                                            <div class="flex items-start justify-between mb-1 gap-1">
                                                <div class="min-w-0">
                                                    <label for="input-tvm-N" class="text-[11px] font-mono text-sky-400 font-bold block truncate">N (Períodos / F1)</label>
                                                    <span class="text-[10px] text-slate-400 font-mono">Unid: <strong class="text-slate-300 font-normal">períodos</strong></span>
                                                </div>
                                                <span id="role-tvm-N" class="text-[10px] font-semibold text-slate-500 shrink-0 text-right mt-0.5">Dado TVM</span>
                                            </div>
                                            <input type="text" inputmode="decimal" maxlength="10" autocomplete="off" spellcheck="false" id="input-tvm-N" placeholder="Insira os dados" value="" oninput="app.handleNumericInput(this, {allowNegative:false, allowDecimal:true, maxLength:10}); app.syncInputToState('tvm', 'N', this.value)" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-sm font-mono text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-sky-500/50">
                                        </div>
                                        <div class="grid grid-cols-1 gap-1.5 mt-2" id="actions-tvm-N">
                                            <button id="btn-tvm-N" onclick="app.calculateTVM('N')" class="w-full py-1 bg-sky-600 hover:bg-sky-500 text-white rounded text-xs font-bold transition">Calcular N</button>
                                            <button id="copy-tvm-N" type="button" onclick="app.copyFieldValue('input-tvm-N', this)" class="hidden w-full py-1 px-1 inline-flex items-center justify-center gap-1 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-[11px] sm:text-xs rounded transition shadow-sm text-center truncate">
                                                <span aria-hidden="true">⧉</span> Copiar
                                            </button>
                                        </div>
                                    </div>
                                    <div id="card-tvm-I" class="calc-card-result bg-slate-950 p-2.5 rounded-xl border border-slate-800 transition-all flex flex-col justify-between">
                                        <div>
                                            <div class="flex items-start justify-between mb-1 gap-1">
                                                <div class="min-w-0">
                                                    <label for="input-tvm-I" class="text-[11px] font-mono text-sky-400 font-bold block truncate">I%YR (Taxa / F2)</label>
                                                    <span class="text-[10px] text-slate-400 font-mono">Unid: <strong class="text-slate-300 font-normal">% a.a.</strong></span>
                                                </div>
                                                <span id="role-tvm-I" class="text-[10px] font-semibold text-slate-500 shrink-0 text-right mt-0.5">Dado TVM</span>
                                            </div>
                                            <input type="text" inputmode="decimal" maxlength="10" autocomplete="off" spellcheck="false" id="input-tvm-I" placeholder="Insira os dados" value="" oninput="app.handleNumericInput(this, {allowNegative:true, allowDecimal:true, maxLength:10}); app.syncInputToState('tvm', 'I', this.value)" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-sm font-mono text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-sky-500/50">
                                        </div>
                                        <div class="grid grid-cols-1 gap-1.5 mt-2" id="actions-tvm-I">
                                            <button id="btn-tvm-I" onclick="app.calculateTVM('I')" class="w-full py-1 bg-sky-600 hover:bg-sky-500 text-white rounded text-xs font-bold transition">Calcular I%</button>
                                            <button id="copy-tvm-I" type="button" onclick="app.copyFieldValue('input-tvm-I', this)" class="hidden w-full py-1 px-1 inline-flex items-center justify-center gap-1 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-[11px] sm:text-xs rounded transition shadow-sm text-center truncate">
                                                <span aria-hidden="true">⧉</span> Copiar
                                            </button>
                                        </div>
                                    </div>
                                    <div id="card-tvm-PV" class="calc-card-result bg-slate-950 p-2.5 rounded-xl border border-slate-800 transition-all flex flex-col justify-between">
                                        <div>
                                            <div class="flex items-start justify-between mb-1 gap-1">
                                                <div class="min-w-0">
                                                    <label for="input-tvm-PV" class="text-[11px] font-mono text-sky-400 font-bold block truncate">PV (Valor Pres. / F3)</label>
                                                    <span class="text-[10px] text-slate-400 font-mono">Unid: <strong class="text-slate-300 font-normal">R$</strong></span>
                                                </div>
                                                <span id="role-tvm-PV" class="text-[10px] font-semibold text-slate-500 shrink-0 text-right mt-0.5">Dado TVM</span>
                                            </div>
                                            <input type="text" inputmode="decimal" maxlength="18" autocomplete="off" spellcheck="false" id="input-tvm-PV" placeholder="Insira os dados" value="" oninput="app.handleNumericInput(this, {allowNegative:true, allowDecimal:true, maxLength:18}); app.syncInputToState('tvm', 'PV', this.value)" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-sm font-mono text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-sky-500/50">
                                        </div>
                                        <div class="grid grid-cols-1 gap-1.5 mt-2" id="actions-tvm-PV">
                                            <button id="btn-tvm-PV" onclick="app.calculateTVM('PV')" class="w-full py-1 bg-sky-600 hover:bg-sky-500 text-white rounded text-xs font-bold transition">Calcular PV</button>
                                            <button id="copy-tvm-PV" type="button" onclick="app.copyFieldValue('input-tvm-PV', this)" class="hidden w-full py-1 px-1 inline-flex items-center justify-center gap-1 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-[11px] sm:text-xs rounded transition shadow-sm text-center truncate">
                                                <span aria-hidden="true">⧉</span> Copiar
                                            </button>
                                        </div>
                                    </div>
                                    <div id="card-tvm-PMT" class="calc-card-result bg-slate-950 p-2.5 rounded-xl border border-slate-800 transition-all flex flex-col justify-between">
                                        <div>
                                            <div class="flex items-start justify-between mb-1 gap-1">
                                                <div class="min-w-0">
                                                    <label for="input-tvm-PMT" class="text-[11px] font-mono text-sky-400 font-bold block truncate">PMT (Parcela / F4)</label>
                                                    <span class="text-[10px] text-slate-400 font-mono">Unid: <strong class="text-slate-300 font-normal">R$</strong></span>
                                                </div>
                                                <span id="role-tvm-PMT" class="text-[10px] font-semibold text-slate-500 shrink-0 text-right mt-0.5">Dado TVM</span>
                                            </div>
                                            <input type="text" inputmode="decimal" maxlength="18" autocomplete="off" spellcheck="false" id="input-tvm-PMT" placeholder="Insira os dados" value="" oninput="app.handleNumericInput(this, {allowNegative:true, allowDecimal:true, maxLength:18}); app.syncInputToState('tvm', 'PMT', this.value)" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-sm font-mono text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-sky-500/50">
                                        </div>
                                        <div class="grid grid-cols-1 gap-1.5 mt-2" id="actions-tvm-PMT">
                                            <button id="btn-tvm-PMT" onclick="app.calculateTVM('PMT')" class="w-full py-1 bg-sky-600 hover:bg-sky-500 text-white rounded text-xs font-bold transition">Calcular PMT</button>
                                            <button id="copy-tvm-PMT" type="button" onclick="app.copyFieldValue('input-tvm-PMT', this)" class="hidden w-full py-1 px-1 inline-flex items-center justify-center gap-1 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-[11px] sm:text-xs rounded transition shadow-sm text-center truncate">
                                                <span aria-hidden="true">⧉</span> Copiar
                                            </button>
                                        </div>
                                    </div>
                                    <div id="card-tvm-FV" class="calc-card-result bg-slate-950 p-2.5 rounded-xl border border-slate-800 transition-all flex flex-col justify-between">
                                        <div>
                                            <div class="flex items-start justify-between mb-1 gap-1">
                                                <div class="min-w-0">
                                                    <label for="input-tvm-FV" class="text-[11px] font-mono text-sky-400 font-bold block truncate">FV (Valor Futuro / F5)</label>
                                                    <span class="text-[10px] text-slate-400 font-mono">Unid: <strong class="text-slate-300 font-normal">R$</strong></span>
                                                </div>
                                                <span id="role-tvm-FV" class="text-[10px] font-semibold text-slate-500 shrink-0 text-right mt-0.5">Dado TVM</span>
                                            </div>
                                            <input type="text" inputmode="decimal" maxlength="18" autocomplete="off" spellcheck="false" id="input-tvm-FV" placeholder="Insira os dados" value="" oninput="app.handleNumericInput(this, {allowNegative:true, allowDecimal:true, maxLength:18}); app.syncInputToState('tvm', 'FV', this.value)" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-sm font-mono text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-sky-500/50">
                                        </div>
                                        <div class="grid grid-cols-1 gap-1.5 mt-2" id="actions-tvm-FV">
                                            <button id="btn-tvm-FV" onclick="app.calculateTVM('FV')" class="w-full py-1 bg-sky-600 hover:bg-sky-500 text-white rounded text-xs font-bold transition">Calcular FV</button>
                                            <button id="copy-tvm-FV" type="button" onclick="app.copyFieldValue('input-tvm-FV', this)" class="hidden w-full py-1 px-1 inline-flex items-center justify-center gap-1 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-[11px] sm:text-xs rounded transition shadow-sm text-center truncate">
                                                <span aria-hidden="true">⧉</span> Copiar
                                            </button>
                                        </div>
                                    </div>
                                    <div id="card-tvm-PYR" class="bg-slate-950 p-2.5 rounded-xl border border-slate-800 flex flex-col justify-between">
                                        <div>
                                            <div class="flex items-start justify-between mb-1 gap-1">
                                                <div class="min-w-0">
                                                    <label for="input-tvm-PYR" class="text-[11px] font-mono text-slate-300 font-bold block truncate">P/YR (Períodos/Ano)</label>
                                                    <span class="text-[10px] text-slate-400 font-mono">Unid: <strong class="text-slate-300 font-normal">per./ano</strong></span>
                                                </div>
                                                <span class="text-[10px] font-semibold text-slate-500 shrink-0 text-right mt-0.5">Config.</span>
                                            </div>
                                            <input type="text" inputmode="numeric" maxlength="3" autocomplete="off" spellcheck="false" id="input-tvm-PYR" placeholder="Insira os dados" value="12" oninput="app.handleNumericInput(this, {allowNegative:false, allowDecimal:false, maxLength:3}); app.syncInputToState('tvm', 'PYR', this.value)" onblur="if(!this.value||parseInt(this.value,10)<1){this.value='12';app.syncInputToState('tvm','PYR','12');}" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-sm font-mono text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-sky-500/50">
                                        </div>
                                        <div class="mt-2" id="tvm-regime-container">
                                            <div class="flex items-center justify-between mb-1">
                                                <span class="text-[10px] font-mono font-bold text-slate-400 uppercase tracking-wider">Regime</span>
                                                <span id="tvm-mode-badge" class="text-[10px] font-mono font-bold text-slate-300">Postecipado</span>
                                            </div>
                                            <div class="grid grid-cols-2 p-0.5 rounded-lg bg-slate-900 border border-slate-700/80 text-xs font-mono font-bold" role="group" aria-label="Regime de Pagamento">
                                                <button type="button" id="btn-tvm-mode-end" onclick="app.setTvmMode(false)" class="py-1 rounded text-center transition-all bg-sky-600 text-white font-bold shadow-sm">END</button>
                                                <button type="button" id="btn-tvm-mode-bgn" onclick="app.setTvmMode(true)" class="py-1 rounded text-center transition-all text-slate-400 hover:text-slate-200 font-bold">BGN</button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div id="tvm-feedback" role="status" aria-live="polite" class="hidden rounded-lg border border-rose-500/30 bg-rose-950/20 px-3 py-2 text-xs text-rose-300"></div>

                                <!-- Tabela de Amortização -->
                                <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 mt-1">
                                    <div class="flex flex-wrap items-center justify-between gap-2 mb-2">
                                        <div class="flex items-center gap-2">
                                            <h3 class="text-xs font-mono font-bold text-emerald-400">Tabela de Amortização (AMRT)</h3>
                                            <span id="amort-bgn-indicator" class="text-[10px] font-mono font-bold px-1.5 py-0.5 rounded bg-slate-800 text-slate-300">Modo: END (Postecipado)</span>
                                        </div>
                                        <div class="flex flex-wrap items-center gap-2">
                                            <div class="flex items-center gap-1.5">
                                                <button type="button" id="btn-copy-amort" onclick="app.copyAmortizationTable(this)" title="Copiar cronograma para a área de transferência (Excel / Planilhas)" class="px-2 py-1 bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 rounded text-xs font-mono font-bold inline-flex items-center gap-1 transition">
                                                    <span aria-hidden="true">⧉</span> Copiar Tabela
                                                </button>
                                                <button type="button" id="btn-csv-amort" onclick="app.exportAmortizationCsv()" title="Baixar cronograma em formato CSV" class="px-2 py-1 bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 rounded text-xs font-mono font-bold inline-flex items-center gap-1 transition">
                                                    <span aria-hidden="true">⬇</span> CSV
                                                </button>
                                            </div>
                                            <label class="text-[11px] font-mono text-slate-400 flex items-center gap-1">
                                                Exibir:
                                                <select id="amort-limit-select" onchange="app.generateAmortizationTable()" class="bg-slate-900 border border-slate-700 text-slate-200 rounded px-2 py-1 text-xs font-mono">
                                                    <option value="60" selected>60 parcelas</option>
                                                    <option value="120">120 parcelas</option>
                                                    <option value="360">360 parcelas</option>
                                                    <option value="all">Todas as parcelas</option>
                                                </select>
                                            </label>
                                            <button onclick="app.generateAmortizationTable()" class="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-xs font-bold transition">Gerar Tabela</button>
                                        </div>
                                    </div>"""

    if target_tvm_html not in content:
        print(f"Error: target_tvm_html not found in {path}")
        return False
    content = content.replace(target_tvm_html, replacement_tvm_html, 1)

    # 3. JS update in init()
    target_init_bgn = """                // Sincronizar indicadores visuais
                const modeInd = document.getElementById('label-mode-indicator');
                if (modeInd) modeInd.textContent = `MODO: ${this.mode}`;
                const tvmInd = document.getElementById('label-tvm-indicator');
                if (tvmInd) tvmInd.textContent = `TVM: ${this.tvm.isBegin ? 'BGN' : 'END'}`;
                const btnAmort = document.getElementById('btn-amort-mode-label');
                if (btnAmort) btnAmort.textContent = `Modo: ${this.tvm.isBegin ? 'BGN' : 'END'}`;
                const indAmort = document.getElementById('amort-bgn-indicator');
                if (indAmort) {
                    indAmort.textContent = this.tvm.isBegin ? 'Modo: BGN (Antecipado)' : 'Modo: END (Postecipado)';
                    indAmort.className = this.tvm.isBegin
                        ? 'text-[10px] font-mono font-bold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/40'
                        : 'text-[10px] font-mono font-bold px-1.5 py-0.5 rounded bg-slate-800 text-slate-300';
                }"""

    replacement_init_bgn = """                // Sincronizar indicadores visuais
                const modeInd = document.getElementById('label-mode-indicator');
                if (modeInd) modeInd.textContent = `MODO: ${this.mode}`;
                this.setTvmMode(this.tvm.isBegin);"""

    if target_init_bgn not in content:
        print(f"Error: target_init_bgn not found in {path}")
        return False
    content = content.replace(target_init_bgn, replacement_init_bgn, 1)

    # 4. JS update for toggleBgnEnd & setTvmMode
    target_toggle = """            toggleBgnEnd() {
                this.tvm.isBegin = !this.tvm.isBegin;
                const lbl = this.tvm.isBegin ? 'BGN' : 'END';
                const modeButton = document.getElementById('btn-tvm-toggle');
                if (modeButton) modeButton.setAttribute('aria-pressed', this.tvm.isBegin ? 'true' : 'false');
                const tvmInd = document.getElementById('label-tvm-indicator');
                if (tvmInd) tvmInd.textContent = `TVM: ${lbl}`;
                const btnAmort = document.getElementById('btn-amort-mode-label');
                if (btnAmort) btnAmort.textContent = `Modo: ${lbl}`;
                const indAmort = document.getElementById('amort-bgn-indicator');
                if (indAmort) {
                    indAmort.textContent = this.tvm.isBegin ? 'Modo: BGN (Antecipado)' : 'Modo: END (Postecipado)';
                    indAmort.className = this.tvm.isBegin
                        ? 'text-[10px] font-mono font-bold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/40'
                        : 'text-[10px] font-mono font-bold px-1.5 py-0.5 rounded bg-slate-800 text-slate-300';
                }
                this.updateLCD();
                this.saveWorkspaceState();
            },"""

    replacement_toggle = """            setTvmMode(isBegin) {
                this.tvm.isBegin = !!isBegin;
                const lbl = this.tvm.isBegin ? 'BGN' : 'END';
                const modeButton = document.getElementById('btn-tvm-toggle');
                if (modeButton) modeButton.setAttribute('aria-pressed', this.tvm.isBegin ? 'true' : 'false');
                const tvmInd = document.getElementById('label-tvm-indicator');
                if (tvmInd) tvmInd.textContent = `TVM: ${lbl}`;
                const btnAmort = document.getElementById('btn-amort-mode-label');
                if (btnAmort) btnAmort.textContent = `Modo: ${lbl}`;
                const btnEnd = document.getElementById('btn-tvm-mode-end');
                const btnBgn = document.getElementById('btn-tvm-mode-bgn');
                const badge = document.getElementById('tvm-mode-badge');
                if (btnEnd && btnBgn) {
                    if (this.tvm.isBegin) {
                        btnEnd.className = 'py-1 rounded text-center transition-all text-slate-400 hover:text-slate-200 font-bold';
                        btnBgn.className = 'py-1 rounded text-center transition-all bg-amber-600 text-white font-bold shadow-sm';
                    } else {
                        btnEnd.className = 'py-1 rounded text-center transition-all bg-sky-600 text-white font-bold shadow-sm';
                        btnBgn.className = 'py-1 rounded text-center transition-all text-slate-400 hover:text-slate-200 font-bold';
                    }
                }
                if (badge) {
                    badge.textContent = this.tvm.isBegin ? 'Antecipado' : 'Postecipado';
                    badge.className = this.tvm.isBegin
                        ? 'text-[10px] font-mono font-bold text-amber-400'
                        : 'text-[10px] font-mono font-bold text-slate-300';
                }
                const indAmort = document.getElementById('amort-bgn-indicator');
                if (indAmort) {
                    indAmort.textContent = this.tvm.isBegin ? 'Modo: BGN (Antecipado)' : 'Modo: END (Postecipado)';
                    indAmort.className = this.tvm.isBegin
                        ? 'text-[10px] font-mono font-bold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/40'
                        : 'text-[10px] font-mono font-bold px-1.5 py-0.5 rounded bg-slate-800 text-slate-300';
                }
                this.updateLCD();
                this.saveWorkspaceState();
            },

            toggleBgnEnd() {
                this.setTvmMode(!this.tvm.isBegin);
            },"""

    if target_toggle not in content:
        print(f"Error: target_toggle not found in {path}")
        return False
    content = content.replace(target_toggle, replacement_toggle, 1)

    # 5. JS update for setTvmCalculatedCard & clearTvmCalculatedCard
    target_cards_js = """            setTvmCalculatedCard(target) {
                const keys = ['N', 'I', 'PV', 'PMT', 'FV'];
                keys.forEach(k => {
                    const card = document.getElementById(`card-tvm-${k}`);
                    const input = document.getElementById(`input-tvm-${k}`);
                    const role = document.getElementById(`role-tvm-${k}`);
                    const btn = document.getElementById(`btn-tvm-${k}`);
                    const copyBtn = document.getElementById(`copy-tvm-${k}`);
                    const defaultBtnText = k === 'I' ? 'Calcular I%' : `Calcular ${k}`;

                    if (k === target) {
                        if (card) card.classList.add('is-result');
                        if (input) input.classList.add('is-result-field');
                        if (role) {
                            role.textContent = '✓ Resultado calculado';
                            role.className = 'text-[10px] font-bold text-emerald-400';
                        }
                        if (btn) {
                            btn.textContent = '↻ Recalcular';
                            btn.className = 'w-full py-1 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded text-xs font-bold transition';
                        }
                        if (copyBtn) copyBtn.classList.remove('hidden');
                    } else {
                        if (card) card.classList.remove('is-result');
                        if (input) input.classList.remove('is-result-field');
                        if (role) {
                            role.textContent = 'Dado TVM';
                            role.className = 'text-[10px] font-semibold text-slate-500';
                        }
                        if (btn) {
                            btn.textContent = defaultBtnText;
                            btn.className = 'w-full py-1 bg-sky-600 hover:bg-sky-500 text-white rounded text-xs font-bold transition';
                        }
                        if (copyBtn) copyBtn.classList.add('hidden');
                    }
                });
            },

            clearTvmCalculatedCard(key) {
                const card = document.getElementById(`card-tvm-${key}`);
                const input = document.getElementById(`input-tvm-${key}`);
                const role = document.getElementById(`role-tvm-${key}`);
                const btn = document.getElementById(`btn-tvm-${key}`);
                const copyBtn = document.getElementById(`copy-tvm-${key}`);
                const defaultBtnText = key === 'I' ? 'Calcular I%' : `Calcular ${key}`;

                if (card) card.classList.remove('is-result');
                if (input) input.classList.remove('is-result-field');
                if (role) {
                    role.textContent = 'Dado TVM';
                    role.className = 'text-[10px] font-semibold text-slate-500';
                }
                if (btn) {
                    btn.textContent = defaultBtnText;
                    btn.className = 'w-full py-1 bg-sky-600 hover:bg-sky-500 text-white rounded text-xs font-bold transition';
                }
                if (copyBtn) copyBtn.classList.add('hidden');
            },"""

    replacement_cards_js = """            setTvmCalculatedCard(target) {
                const keys = ['N', 'I', 'PV', 'PMT', 'FV'];
                keys.forEach(k => {
                    const card = document.getElementById(`card-tvm-${k}`);
                    const input = document.getElementById(`input-tvm-${k}`);
                    const role = document.getElementById(`role-tvm-${k}`);
                    const btn = document.getElementById(`btn-tvm-${k}`);
                    const copyBtn = document.getElementById(`copy-tvm-${k}`);
                    const actions = document.getElementById(`actions-tvm-${k}`);
                    const defaultBtnText = k === 'I' ? 'Calcular I%' : `Calcular ${k}`;

                    if (k === target) {
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
                            btn.className = 'w-full py-1 px-1 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded text-[11px] sm:text-xs font-bold transition text-center truncate';
                        }
                        if (copyBtn) {
                            copyBtn.classList.remove('hidden');
                            copyBtn.className = 'w-full py-1 px-1 inline-flex items-center justify-center gap-1 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-[11px] sm:text-xs rounded transition shadow-sm text-center truncate';
                        }
                    } else {
                        if (card) card.classList.remove('is-result');
                        if (input) input.classList.remove('is-result-field');
                        if (role) {
                            role.textContent = 'Dado TVM';
                            role.className = 'text-[10px] font-semibold text-slate-500 shrink-0 text-right mt-0.5';
                        }
                        if (actions) {
                            actions.className = 'grid grid-cols-1 gap-1.5 mt-2';
                        }
                        if (btn) {
                            btn.textContent = defaultBtnText;
                            btn.className = 'w-full py-1 bg-sky-600 hover:bg-sky-500 text-white rounded text-xs font-bold transition';
                        }
                        if (copyBtn) copyBtn.classList.add('hidden');
                    }
                });
            },

            clearTvmCalculatedCard(key) {
                const card = document.getElementById(`card-tvm-${key}`);
                const input = document.getElementById(`input-tvm-${key}`);
                const role = document.getElementById(`role-tvm-${key}`);
                const btn = document.getElementById(`btn-tvm-${key}`);
                const copyBtn = document.getElementById(`copy-tvm-${key}`);
                const actions = document.getElementById(`actions-tvm-${key}`);
                const defaultBtnText = key === 'I' ? 'Calcular I%' : `Calcular ${key}`;

                if (card) card.classList.remove('is-result');
                if (input) input.classList.remove('is-result-field');
                if (role) {
                    role.textContent = 'Dado TVM';
                    role.className = 'text-[10px] font-semibold text-slate-500 shrink-0 text-right mt-0.5';
                }
                if (actions) {
                    actions.className = 'grid grid-cols-1 gap-1.5 mt-2';
                }
                if (btn) {
                    btn.textContent = defaultBtnText;
                    btn.className = 'w-full py-1 bg-sky-600 hover:bg-sky-500 text-white rounded text-xs font-bold transition';
                }
                if (copyBtn) copyBtn.classList.add('hidden');
            },

            clearTvmModule() {
                ['N', 'I', 'PV', 'PMT', 'FV'].forEach(k => {
                    this.tvm[k] = null;
                    this.clearTvmCalculatedCard(k);
                    const input = document.getElementById(`input-tvm-${k}`);
                    if (input) input.value = '';
                });
                this.tvm.PYR = 12;
                const pyr = document.getElementById('input-tvm-PYR');
                if (pyr) pyr.value = '12';
                this.setTvmMode(false);
                const tbody = document.getElementById('amort-table-body');
                if (tbody) tbody.innerHTML = '<tr><td colspan="5" class="p-2 text-center text-slate-500">Clique em "Gerar Tabela" para listar os períodos calculados.</td></tr>';
                const tfoot = document.getElementById('amort-table-foot');
                if (tfoot) { tfoot.innerHTML = ''; tfoot.classList.add('hidden'); }
                const notice = document.getElementById('amort-notice');
                if (notice) { notice.innerHTML = ''; notice.classList.add('hidden'); }
                this._currentAmortSchedule = [];
                this._currentAmortTotals = null;
                this.setTvmFeedback('');
                this.updateTvmLcdHeader();
                const resPanel = document.getElementById('result-panel');
                if (resPanel) resPanel.classList.add('hidden');
                this.saveWorkspaceState();
                this.setModuleActionFeedback('Valores de TVM e amortização limpos com sucesso.', 'info');
            },"""

    if target_cards_js not in content:
        print(f"Error: target_cards_js not found in {path}")
        return False
    content = content.replace(target_cards_js, replacement_cards_js, 1)

    # 6. JS update in generateAmortizationTable + copy/csv helpers
    target_amort_js = """            generateAmortizationTable() {
                const tbody = document.getElementById('amort-table-body');
                const tfoot = document.getElementById('amort-table-foot');
                const notice = document.getElementById('amort-notice');
                if (!tbody) return;
                tbody.innerHTML = '';
                if (tfoot) {
                    tfoot.innerHTML = '';
                    tfoot.classList.add('hidden');
                }
                if (notice) {
                    notice.innerHTML = '';
                    notice.classList.add('hidden');
                }"""

    replacement_amort_js = """            generateAmortizationTable() {
                const tbody = document.getElementById('amort-table-body');
                const tfoot = document.getElementById('amort-table-foot');
                const notice = document.getElementById('amort-notice');
                if (!tbody) return;
                tbody.innerHTML = '';
                this._currentAmortSchedule = [];
                this._currentAmortTotals = null;
                if (tfoot) {
                    tfoot.innerHTML = '';
                    tfoot.classList.add('hidden');
                }
                if (notice) {
                    notice.innerHTML = '';
                    notice.classList.add('hidden');
                }"""

    if target_amort_js not in content:
        print(f"Error: target_amort_js not found in {path}")
        return False
    content = content.replace(target_amort_js, replacement_amort_js, 1)

    # In loop of generateAmortizationTable
    target_row_append = """                    tbody.appendChild(tr);

                    if (balance <= residualFV && period < displayN && residualFV === 0) {
                        break;
                    }
                }

                if (tfoot) {"""

    replacement_row_append = """                    tbody.appendChild(tr);

                    this._currentAmortSchedule.push({
                        period,
                        label: `${period}${isBegin && period === 1 ? ' (Entrada)' : ''}`,
                        pmt: actualPmt,
                        interest,
                        principal,
                        balance
                    });

                    if (balance <= residualFV && period < displayN && residualFV === 0) {
                        break;
                    }
                }

                this._currentAmortTotals = {
                    count: actualRows,
                    pmt: totPmt,
                    interest: totInt,
                    principal: totPrin,
                    balance
                };

                if (tfoot) {"""

    if target_row_append not in content:
        print(f"Error: target_row_append not found in {path}")
        return False
    content = content.replace(target_row_append, replacement_row_append, 1)

    # Export & Copy functions after generateAmortizationTable
    target_after_amort = """                if (tfoot) {
                    tfoot.innerHTML = `
                        <tr>
                            <td class="p-1.5 font-bold">TOTAL (${actualRows})</td>
                            <td class="p-1.5 text-white">${this.formatNum(totPmt)}</td>
                            <td class="p-1.5 text-rose-300">${this.formatNum(totInt)}</td>
                            <td class="p-1.5 text-emerald-300">${this.formatNum(totPrin)}</td>
                            <td class="p-1.5 text-right font-bold text-sky-300">${this.formatNum(balance)}</td>
                        </tr>
                    `;
                    tfoot.classList.remove('hidden');
                }
            },"""

    replacement_after_amort = """                if (tfoot) {
                    tfoot.innerHTML = `
                        <tr>
                            <td class="p-1.5 font-bold">TOTAL (${actualRows})</td>
                            <td class="p-1.5 text-white">${this.formatNum(totPmt)}</td>
                            <td class="p-1.5 text-rose-300">${this.formatNum(totInt)}</td>
                            <td class="p-1.5 text-emerald-300">${this.formatNum(totPrin)}</td>
                            <td class="p-1.5 text-right font-bold text-sky-300">${this.formatNum(balance)}</td>
                        </tr>
                    `;
                    tfoot.classList.remove('hidden');
                }
            },

            copyAmortizationTable(btnEl) {
                if (!this._currentAmortSchedule || !this._currentAmortSchedule.length) {
                    this.setModuleActionFeedback('Gere a tabela de amortização antes de copiar.', 'error');
                    return;
                }
                const lines = [];
                lines.push(['# Per.', 'Pagamento', 'Juros', 'Principal', 'Saldo Devedor'].join('\\t'));
                this._currentAmortSchedule.forEach(r => {
                    lines.push([r.label, this.formatNum(r.pmt), this.formatNum(r.interest), this.formatNum(r.principal), this.formatNum(r.balance)].join('\\t'));
                });
                if (this._currentAmortTotals) {
                    const t = this._currentAmortTotals;
                    lines.push([`TOTAL (${t.count})`, this.formatNum(t.pmt), this.formatNum(t.interest), this.formatNum(t.principal), this.formatNum(t.balance)].join('\\t'));
                }
                const text = lines.join('\\r\\n');
                const onDone = () => {
                    if (btnEl) {
                        const orig = btnEl.innerHTML;
                        btnEl.innerHTML = '<span aria-hidden="true">✓</span> Copiado!';
                        setTimeout(() => { if (btnEl) btnEl.innerHTML = orig; }, 1500);
                    }
                    this.setModuleActionFeedback('Tabela de amortização copiada para a área de transferência (formato Excel / Planilhas).', 'success');
                };

                if (navigator.clipboard && navigator.clipboard.writeText) {
                    navigator.clipboard.writeText(text).then(onDone).catch(() => {
                        this.fallbackCopyText(text);
                        onDone();
                    });
                } else {
                    this.fallbackCopyText(text);
                    onDone();
                }
            },

            exportAmortizationCsv() {
                if (!this._currentAmortSchedule || !this._currentAmortSchedule.length) {
                    this.setModuleActionFeedback('Gere a tabela de amortização antes de exportar.', 'error');
                    return;
                }
                const lines = [];
                lines.push(['"Período"', '"Pagamento"', '"Juros"', '"Principal"', '"Saldo Devedor"'].join(';'));
                this._currentAmortSchedule.forEach(r => {
                    lines.push([`"${r.label}"`, `"${this.formatNum(r.pmt)}"`, `"${this.formatNum(r.interest)}"`, `"${this.formatNum(r.principal)}"`, `"${this.formatNum(r.balance)}"`].join(';'));
                });
                if (this._currentAmortTotals) {
                    const t = this._currentAmortTotals;
                    lines.push([`"TOTAL (${t.count})"`, `"${this.formatNum(t.pmt)}"`, `"${this.formatNum(t.interest)}"`, `"${this.formatNum(t.principal)}"`, `"${this.formatNum(t.balance)}"`].join(';'));
                }
                const csvContent = '\\uFEFF' + lines.join('\\r\\n');
                const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `cronograma_amortizacao_${Date.now()}.csv`;
                document.body.appendChild(a);
                a.click();
                setTimeout(() => {
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                }, 200);
                this.setModuleActionFeedback('Arquivo CSV da tabela de amortização gerado com sucesso.', 'success');
            },

            fallbackCopyText(text) {
                try {
                    const temp = document.createElement('textarea');
                    temp.value = text;
                    temp.setAttribute('readonly', '');
                    temp.style.position = 'absolute';
                    temp.style.left = '-9999px';
                    document.body.appendChild(temp);
                    temp.select();
                    document.execCommand('copy');
                    document.body.removeChild(temp);
                } catch (_) {}
            },"""

    if target_after_amort not in content:
        print(f"Error: target_after_amort not found in {path}")
        return False
    content = content.replace(target_after_amort, replacement_after_amort, 1)

    # 7. Update resetDefaults() TVM mode
    target_reset_bgn = """                const lbl = this.tvm.isBegin ? 'BGN' : 'END';
                const tvmInd = document.getElementById('label-tvm-indicator');
                if (tvmInd) tvmInd.textContent = `TVM: ${lbl}`;
                const modeInd = document.getElementById('label-mode-indicator');
                if (modeInd) modeInd.textContent = `MODO: ${this.mode}`;
                const btnAmort = document.getElementById('btn-amort-mode-label');
                if (btnAmort) btnAmort.textContent = `Modo: ${lbl}`;
                const indAmort = document.getElementById('amort-bgn-indicator');
                if (indAmort) {
                    indAmort.textContent = 'Modo: END (Postecipado)';
                    indAmort.className = 'text-[10px] font-mono font-bold px-1.5 py-0.5 rounded bg-slate-800 text-slate-300';
                }"""

    replacement_reset_bgn = """                const modeInd = document.getElementById('label-mode-indicator');
                if (modeInd) modeInd.textContent = `MODO: ${this.mode}`;
                this.setTvmMode(false);"""

    if target_reset_bgn not in content:
        print(f"Error: target_reset_bgn not found in {path}")
        return False
    content = content.replace(target_reset_bgn, replacement_reset_bgn, 1)

    # 8. Update clearActiveModule('TVM')
    target_clear_active = """                if (module === 'TVM') {
                    ['N','I','PV','PMT','FV'].forEach(k => {
                        this.tvm[k] = null;
                        this.clearTvmCalculatedCard(k);
                    });
                    this.tvm.PYR = 12;
                    const pyr = document.getElementById('input-tvm-PYR'); if (pyr) pyr.value = '12';
                    const feedback = document.getElementById('tvm-feedback'); if (feedback) feedback.classList.add('hidden');
                    const amortBody = document.getElementById('amort-table-body');
                    if (amortBody) amortBody.innerHTML = '<tr><td colspan="5" class="p-2 text-center text-slate-500">Clique em "Gerar Tabela" para listar os períodos calculados.</td></tr>';
                    const amortFoot = document.getElementById('amort-table-foot');
                    if (amortFoot) amortFoot.classList.add('hidden');
                }"""

    replacement_clear_active = """                if (module === 'TVM') {
                    this.clearTvmModule();
                    return;
                }"""

    if target_clear_active not in content:
        print(f"Error: target_clear_active not found in {path}")
        return False
    content = content.replace(target_clear_active, replacement_clear_active, 1)

    # Convert to CRLF for writing
    crlf_content = content.replace('\n', '\r\n')
    with open(path, 'wb') as f:
        f.write(crlf_content.encode('utf-8'))

    print(f"Successfully updated {path}")
    return True

if __name__ == '__main__':
    ok1 = update_file("Calculadora Financeira 17bIi.html")
    ok2 = update_file("index.html")
    if not (ok1 and ok2):
        sys.exit(1)
    print("All files updated successfully.")

