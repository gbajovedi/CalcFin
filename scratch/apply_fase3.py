# -*- coding: utf-8 -*-
"""
apply_fase3.py
Applies Fase 3 changes to Calculadora Financeira 17bIi.html and index.html
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

    # 1. Update app state properties
    old_state = '''            bus: { oldVal: 0, newVal: 0, cost: 0, price: 0, total: 0, part: 0 },
            currx: { base: 'USD', rates: { USD: 1.0, BRL: 5.65, EUR: 0.92, GBP: 0.78 } },
            bond: { price: 100, ytm: 8, coupon: 8 },
            depr: { cost: 10000, salvage: 1000, life: 5 },'''

    new_state = '''            bus: { oldVal: 0, newVal: 0, cost: 0, price: 0, total: 0, part: 0 },
            currx: { base: 'BRL', rates: { USD: 1.0, BRL: 5.65, EUR: 0.92, GBP: 0.78, JPY: 152.0, CAD: 1.38 } },
            bond: { price: 100, ytm: 8, coupon: 8, years: 10 },
            depr: { cost: 10000, salvage: 1000, life: 5, year: 1, method: 'SL' },
            timeCalc: { date1: '2026-01-15', date2: '2026-04-15', daysAdd: 30, dateFormat: 'D.M' },'''

    if old_state in content:
        content = content.replace(old_state, new_state)
        print("✓ Step 1: App state updated for BOND, DEPR, CURRX, TIME")
    elif 'timeCalc:' in content:
        print("✓ Step 1: App state already updated")
    else:
        print("✗ Step 1: old_state not found!")
        return False

    # 2. Add tab-TIME and tab-CURRX to navigation bar
    old_tab_tape = '''                    <button onclick="app.switchTab('TAPE')" id="tab-TAPE" role="tab" tabindex="-1" aria-controls="panel-TAPE" aria-selected="false" title="Histórico de cálculos, fita e registradores" aria-label="Histórico de cálculos" class="tab-btn px-3 py-2 rounded-xl text-xs font-bold transition whitespace-nowrap text-slate-400 hover:text-white hover:bg-slate-800/60 font-mono">
                        Histórico de cálculos
                    </button>'''

    new_tabs = '''                    <button onclick="app.switchTab('TIME')" id="tab-TIME" role="tab" tabindex="-1" aria-controls="panel-TIME" aria-selected="false" title="Tempo, relógio e calendário — contagem de dias 365 e 360" aria-label="Tempo e calendário" class="tab-btn px-3 py-2 rounded-xl text-xs font-bold transition whitespace-nowrap text-slate-400 hover:text-white hover:bg-slate-800/60 font-mono">
                        Tempo e calendário
                    </button>
                    <button onclick="app.switchTab('CURRX')" id="tab-CURRX" role="tab" tabindex="-1" aria-controls="panel-CURRX" aria-selected="false" title="Câmbio de moedas internacionais — USD, EUR, GBP, BRL" aria-label="Câmbio de moedas" class="tab-btn px-3 py-2 rounded-xl text-xs font-bold transition whitespace-nowrap text-slate-400 hover:text-white hover:bg-slate-800/60 font-mono">
                        Câmbio de moedas
                    </button>
                    <button onclick="app.switchTab('TAPE')" id="tab-TAPE" role="tab" tabindex="-1" aria-controls="panel-TAPE" aria-selected="false" title="Histórico de cálculos, fita e registradores" aria-label="Histórico de cálculos" class="tab-btn px-3 py-2 rounded-xl text-xs font-bold transition whitespace-nowrap text-slate-400 hover:text-white hover:bg-slate-800/60 font-mono">
                        Histórico de cálculos
                    </button>'''

    if old_tab_tape in content:
        content = content.replace(old_tab_tape, new_tabs)
        print("✓ Step 2: Tab buttons tab-TIME and tab-CURRX added")
    elif 'id="tab-TIME"' in content:
        print("✓ Step 2: Tab buttons already present")
    else:
        print("✗ Step 2: old_tab_tape not found!")
        return False

    # 3. Add panel-TIME and panel-CURRX right after panel-TAPE
    panels_marker = '''                                    <div id="tape-registers-grid" class="grid grid-cols-2 sm:grid-cols-5 gap-1.5 font-mono text-xs">
                                        <!-- R0 a R9 cards gerados dinamicamente -->
                                    </div>
                                </div>
                            </div>'''

    new_panels = '''                                    <div id="tape-registers-grid" class="grid grid-cols-2 sm:grid-cols-5 gap-1.5 font-mono text-xs">
                                        <!-- R0 a R9 cards gerados dinamicamente -->
                                    </div>
                                </div>
                            </div>

                            <!-- PAINEL TEMPO E CALENDÁRIO (TIME) -->
                            <div id="panel-TIME" role="tabpanel" aria-labelledby="tab-TIME" tabindex="0" class="module-panel hidden flex flex-col gap-3">
                                <div class="flex items-center justify-between border-b border-slate-800 pb-2">
                                    <div>
                                        <h2 class="text-sm font-bold text-amber-400">Tempo e calendário oficial</h2>
                                        <p class="text-[11px] text-slate-500 font-mono mt-0.5">TIME · Relógio em tempo real, contagem de dias (Real e 30/360) e projeção de prazos</p>
                                    </div>
                                    <div class="flex items-center gap-2">
                                        <span id="time-live-clock" class="text-xs font-mono font-bold text-sky-400 bg-slate-900 border border-slate-800 px-2.5 py-1 rounded-lg">--:--:--</span>
                                    </div>
                                </div>

                                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs font-mono">
                                    <!-- Card 1: Diferença entre Datas (ACT e 360) -->
                                    <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 flex flex-col justify-between space-y-3">
                                        <div class="space-y-2.5">
                                            <div class="flex items-center justify-between">
                                                <h3 class="font-bold text-white text-xs">Cálculo de Dias entre Datas (CALC)</h3>
                                                <span class="text-[10px] text-slate-500 font-semibold">Submenu CALC</span>
                                            </div>
                                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                                                <div>
                                                    <label for="input-time-date1" class="text-slate-400 block mb-1">Data 1 (Inicial):</label>
                                                    <input type="date" id="input-time-date1" value="2026-01-15" onchange="app.syncTimeDates()" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-white focus:outline-none focus:ring-2 focus:ring-amber-500/50">
                                                </div>
                                                <div>
                                                    <label for="input-time-date2" class="text-slate-400 block mb-1">Data 2 (Final):</label>
                                                    <input type="date" id="input-time-date2" value="2026-04-15" onchange="app.syncTimeDates()" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-white focus:outline-none focus:ring-2 focus:ring-amber-500/50">
                                                </div>
                                            </div>
                                            <div class="grid grid-cols-2 gap-2 pt-1">
                                                <button onclick="app.calcDateDifference('ACT')" class="w-full py-1.5 bg-sky-600 hover:bg-sky-500 text-white font-bold rounded text-xs transition">
                                                    Dias Reais (ACT 365)
                                                </button>
                                                <button onclick="app.calcDateDifference('360')" class="w-full py-1.5 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold rounded text-xs transition">
                                                    Comercial (30/360)
                                                </button>
                                            </div>
                                        </div>
                                        <div id="card-time-diff-result" class="calc-card-result bg-slate-900/60 p-2.5 rounded-lg border border-slate-800 transition-all">
                                            <div class="flex items-center justify-between mb-1">
                                                <span class="text-[11px] font-mono text-amber-400 font-bold">Resultado de Prazos:</span>
                                                <span id="role-time-diff" class="text-[10px] font-semibold text-slate-500">Métrica</span>
                                            </div>
                                            <div id="time-diff-display" class="p-2 rounded bg-slate-950 border border-slate-800 text-slate-200 text-xs font-mono">
                                                Selecione as datas e clique no método desejado.
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Card 2: Projeção de Datas (+DAYS / -DAYS) -->
                                    <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 flex flex-col justify-between space-y-3">
                                        <div class="space-y-2.5">
                                            <div class="flex items-center justify-between">
                                                <h3 class="font-bold text-white text-xs">Projeção Futura / Passada (+DAYS)</h3>
                                                <span class="text-[10px] text-slate-500 font-semibold">HP +DAYS</span>
                                            </div>
                                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                                                <div>
                                                    <label for="input-time-proj-base" class="text-slate-400 block mb-1">Data Base:</label>
                                                    <input type="date" id="input-time-proj-base" value="2026-01-01" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-white focus:outline-none focus:ring-2 focus:ring-amber-500/50">
                                                </div>
                                                <div>
                                                    <label for="input-time-proj-days" class="text-slate-400 block mb-1">Nº de Dias (+/-):</label>
                                                    <input type="number" id="input-time-proj-days" value="30" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-white focus:outline-none focus:ring-2 focus:ring-amber-500/50">
                                                </div>
                                            </div>
                                            <button onclick="app.calcDateProjection()" class="w-full py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded text-xs transition">
                                                Calcular Data Projetada (+DAYS)
                                            </button>
                                        </div>
                                        <div id="card-time-proj-result" class="calc-card-result bg-slate-900/60 p-2.5 rounded-lg border border-slate-800 transition-all">
                                            <div class="flex items-center justify-between mb-1">
                                                <span class="text-[11px] font-mono text-emerald-400 font-bold">Data Resultante:</span>
                                                <span class="text-[10px] font-semibold text-slate-500">Dia da Semana</span>
                                            </div>
                                            <div id="time-proj-display" class="p-2 rounded bg-slate-950 border border-slate-800 text-slate-200 text-xs font-mono">
                                                Informe a data base e os dias para projetar.
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- PAINEL CÂMBIO DE MOEDAS (CURRX) -->
                            <div id="panel-CURRX" role="tabpanel" aria-labelledby="tab-CURRX" tabindex="0" class="module-panel hidden flex flex-col gap-3">
                                <div class="flex items-center justify-between border-b border-slate-800 pb-2">
                                    <div>
                                        <h2 class="text-sm font-bold text-amber-400">Câmbio de moedas internacionais</h2>
                                        <p class="text-[11px] text-slate-500 font-mono mt-0.5">CURRX · Conversões em tempo real com paridades oficiais</p>
                                    </div>
                                    <button onclick="app.resetCurrxRates()" class="text-xs font-mono bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-300 px-2 py-1 rounded">
                                        ↺ Restaurar Cotações Padrão
                                    </button>
                                </div>

                                <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 flex flex-col gap-3">
                                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 items-end">
                                        <div class="sm:col-span-2">
                                            <label for="input-currx-amount" class="text-xs font-mono text-slate-300 font-bold block mb-1">Valor a Converter:</label>
                                            <div class="flex items-center gap-2">
                                                <input type="text" inputmode="decimal" maxlength="18" autocomplete="off" id="input-currx-amount" value="100.00" oninput="app.updateCurrxConversions()" class="w-full bg-slate-900 border border-slate-700 rounded p-2 text-sm font-mono text-white focus:outline-none focus:ring-2 focus:ring-amber-500/50">
                                                <select id="select-currx-from" onchange="app.updateCurrxConversions()" class="bg-slate-900 border border-slate-700 text-amber-400 font-mono font-bold rounded p-2 text-xs">
                                                    <option value="USD">USD ($)</option>
                                                    <option value="BRL" selected>BRL (R$)</option>
                                                    <option value="EUR">EUR (€)</option>
                                                    <option value="GBP">GBP (£)</option>
                                                    <option value="JPY">JPY (¥)</option>
                                                    <option value="CAD">CAD (C$)</option>
                                                </select>
                                            </div>
                                        </div>
                                        <button onclick="app.syncCurrxToLcd()" class="w-full py-2 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold font-mono rounded text-xs transition">
                                            Sincronizar com Visor HP
                                        </button>
                                    </div>

                                    <!-- Grid com os valores convertidos -->
                                    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2 pt-2" id="currx-cards-grid">
                                        <!-- Renderizado dinamicamente -->
                                    </div>

                                    <!-- Tabela de Cotações Editáveis em relação ao USD -->
                                    <div class="pt-2 border-t border-slate-800/80">
                                        <span class="text-[11px] font-mono font-bold text-slate-400 block mb-1.5 uppercase tracking-wider">Cotações Base (Unidades por 1 USD):</span>
                                        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2 text-xs font-mono">
                                            <div>
                                                <label class="text-[10px] text-slate-400 block">USD (Dólar):</label>
                                                <input type="number" step="0.01" id="rate-USD" value="1.00" readonly class="w-full bg-slate-900/60 border border-slate-800 rounded p-1 text-slate-400 text-xs">
                                            </div>
                                            <div>
                                                <label class="text-[10px] text-slate-400 block">BRL (Real):</label>
                                                <input type="number" step="0.01" id="rate-BRL" value="5.65" onchange="app.updateCurrxRate('BRL', this.value)" class="w-full bg-slate-900 border border-slate-700 rounded p-1 text-white text-xs">
                                            </div>
                                            <div>
                                                <label class="text-[10px] text-slate-400 block">EUR (Euro):</label>
                                                <input type="number" step="0.01" id="rate-EUR" value="0.92" onchange="app.updateCurrxRate('EUR', this.value)" class="w-full bg-slate-900 border border-slate-700 rounded p-1 text-white text-xs">
                                            </div>
                                            <div>
                                                <label class="text-[10px] text-slate-400 block">GBP (Libra):</label>
                                                <input type="number" step="0.01" id="rate-GBP" value="0.78" onchange="app.updateCurrxRate('GBP', this.value)" class="w-full bg-slate-900 border border-slate-700 rounded p-1 text-white text-xs">
                                            </div>
                                            <div>
                                                <label class="text-[10px] text-slate-400 block">JPY (Iene):</label>
                                                <input type="number" step="0.1" id="rate-JPY" value="152.0" onchange="app.updateCurrxRate('JPY', this.value)" class="w-full bg-slate-900 border border-slate-700 rounded p-1 text-white text-xs">
                                            </div>
                                            <div>
                                                <label class="text-[10px] text-slate-400 block">CAD (Dólar Can.):</label>
                                                <input type="number" step="0.01" id="rate-CAD" value="1.38" onchange="app.updateCurrxRate('CAD', this.value)" class="w-full bg-slate-900 border border-slate-700 rounded p-1 text-white text-xs">
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>'''

    if panels_marker in content:
        content = content.replace(panels_marker, new_panels)
        print("✓ Step 3: panel-TIME and panel-CURRX added to workstation")
    elif 'id="panel-TIME"' in content:
        print("✓ Step 3: Panels already present")
    else:
        print("✗ Step 3: panels_marker not found!")
        return False

    # 4. Expand panel-FIN_TOOLS with BOND card and enhanced DEPRC
    old_fintools = '''                                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                                    <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 flex flex-col space-y-3">
                                        <div>
                                            <h3 class="text-xs font-bold text-white mb-2 font-mono">Conversão Nominal / Efetiva</h3>
                                            <div class="space-y-2 text-xs font-mono">
                                                <div>
                                                    <label for="input-icnv-nom" class="text-slate-400 block">Taxa Nominal (% a.a.)</label>
                                                    <input type="text" inputmode="decimal" maxlength="10" autocomplete="off" spellcheck="false" id="input-icnv-nom" placeholder="Insira os dados" value="" oninput="app.handleNumericInput(this, {allowNegative:true, allowDecimal:true, maxLength:10}); app.syncFinTools()" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-amber-500/50">
                                                </div>
                                                <div>
                                                    <label for="input-icnv-pyr" class="text-slate-400 block">Períodos por Ano (P/YR)</label>
                                                    <input type="text" inputmode="numeric" maxlength="3" autocomplete="off" spellcheck="false" id="input-icnv-pyr" placeholder="Insira os dados" value="12" oninput="app.handleNumericInput(this, {allowNegative:false, allowDecimal:false, maxLength:3}); app.syncFinTools()" onblur="if(!this.value||parseInt(this.value,10)<1){this.value='12';app.syncFinTools();}" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-amber-500/50">
                                                </div>
                                            </div>
                                        </div>
                                        <div id="card-icnv-result" class="calc-card-result bg-slate-900/60 p-2.5 rounded-lg border border-slate-800 transition-all">
                                            <div class="flex items-center justify-between mb-1">
                                                <label for="input-icnv-eff" class="text-[11px] font-mono text-amber-400 font-bold">Taxa Efetiva Calculada (EFF%)</label>
                                                <span id="role-icnv-eff" class="text-[10px] font-semibold text-slate-500">Métrica</span>
                                            </div>
                                            <input type="text" readonly id="input-icnv-eff" placeholder="Aguardando cálculo..." class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-sm font-mono text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-amber-500/50">
                                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-1.5 mt-2">
                                                <button id="btn-icnv-calc" onclick="app.calcEffRate()" class="w-full py-1.5 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold rounded text-xs transition">Calcular Taxa Efetiva</button>
                                                <button id="copy-icnv-result" type="button" onclick="app.copyFieldValue('input-icnv-eff', this)" class="hidden w-full py-1.5 inline-flex items-center justify-center gap-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded transition shadow-sm">
                                                    <span aria-hidden="true">⧉</span> Copiar
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 flex flex-col space-y-3">
                                        <div>
                                            <h3 class="text-xs font-bold text-white mb-2 font-mono">Depreciação Linear (SL)</h3>
                                            <div class="space-y-2 text-xs font-mono">
                                                <div>
                                                    <label for="input-depr-cost" class="text-slate-400 block">Custo Inicial (R$)</label>
                                                    <input type="text" inputmode="decimal" maxlength="18" autocomplete="off" spellcheck="false" id="input-depr-cost" placeholder="Insira os dados" value="" oninput="app.handleNumericInput(this, {allowNegative:false, allowDecimal:true, maxLength:18}); app.syncFinTools()" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-amber-500/50">
                                                </div>
                                                <div>
                                                    <label for="input-depr-salvage" class="text-slate-400 block">Valor Residual (R$)</label>
                                                    <input type="text" inputmode="decimal" maxlength="18" autocomplete="off" spellcheck="false" id="input-depr-salvage" placeholder="Insira os dados" value="" oninput="app.handleNumericInput(this, {allowNegative:false, allowDecimal:true, maxLength:18}); app.syncFinTools()" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-amber-500/50">
                                                </div>
                                                <div>
                                                    <label for="input-depr-life" class="text-slate-400 block">Vida Útil (Anos)</label>
                                                    <input type="text" inputmode="decimal" maxlength="6" autocomplete="off" spellcheck="false" id="input-depr-life" placeholder="Insira os dados" value="" oninput="app.handleNumericInput(this, {allowNegative:false, allowDecimal:true, maxLength:6}); app.syncFinTools()" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-amber-500/50">
                                                </div>
                                            </div>
                                        </div>
                                        <div id="card-depr-result" class="calc-card-result bg-slate-900/60 p-2.5 rounded-lg border border-slate-800 transition-all">
                                            <div class="flex items-center justify-between mb-1">
                                                <label for="input-depr-result" class="text-[11px] font-mono text-sky-400 font-bold">Depreciação Anual (SL)</label>
                                                <span id="role-depr-result" class="text-[10px] font-semibold text-slate-500">Métrica</span>
                                            </div>
                                            <input type="text" readonly id="input-depr-result" placeholder="Aguardando cálculo..." class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-sm font-mono text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-sky-500/50">
                                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-1.5 mt-2">
                                                <button id="btn-depr-calc" onclick="app.calcDepreciationSL()" class="w-full py-1.5 bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold rounded text-xs transition">Calcular Depreciação / Ano</button>
                                                <button id="copy-depr-result" type="button" onclick="app.copyFieldValue('input-depr-result', this)" class="hidden w-full py-1.5 inline-flex items-center justify-center gap-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded transition shadow-sm">
                                                    <span aria-hidden="true">⧉</span> Copiar
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>'''

    new_fintools = '''                                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                                    <!-- Card 1: ICNV (Conversão de Taxas) -->
                                    <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 flex flex-col justify-between space-y-3">
                                        <div>
                                            <div class="flex items-center justify-between mb-1">
                                                <h3 class="text-xs font-bold text-white font-mono">Conversão de Taxas (ICNV)</h3>
                                                <span class="text-[10px] text-slate-500 font-semibold">ICNV</span>
                                            </div>
                                            <div class="space-y-2 text-xs font-mono">
                                                <div>
                                                    <label for="input-icnv-nom" class="text-slate-400 block">Taxa Nominal (% a.a.)</label>
                                                    <input type="text" inputmode="decimal" maxlength="10" autocomplete="off" spellcheck="false" id="input-icnv-nom" placeholder="Insira os dados" value="" oninput="app.handleNumericInput(this, {allowNegative:true, allowDecimal:true, maxLength:10}); app.syncFinTools()" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-amber-500/50">
                                                </div>
                                                <div>
                                                    <label for="input-icnv-pyr" class="text-slate-400 block">Períodos por Ano (P/YR)</label>
                                                    <input type="text" inputmode="numeric" maxlength="3" autocomplete="off" spellcheck="false" id="input-icnv-pyr" placeholder="Insira os dados" value="12" oninput="app.handleNumericInput(this, {allowNegative:false, allowDecimal:false, maxLength:3}); app.syncFinTools()" onblur="if(!this.value||parseInt(this.value,10)<1){this.value='12';app.syncFinTools();}" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-amber-500/50">
                                                </div>
                                            </div>
                                        </div>
                                        <div id="card-icnv-result" class="calc-card-result bg-slate-900/60 p-2.5 rounded-lg border border-slate-800 transition-all">
                                            <div class="flex items-center justify-between mb-1">
                                                <label for="input-icnv-eff" class="text-[11px] font-mono text-amber-400 font-bold">Taxa Efetiva (EFF%)</label>
                                                <span id="role-icnv-eff" class="text-[10px] font-semibold text-slate-500">Métrica</span>
                                            </div>
                                            <input type="text" readonly id="input-icnv-eff" placeholder="Aguardando cálculo..." class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-sm font-mono text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-amber-500/50">
                                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-1.5 mt-2">
                                                <button id="btn-icnv-calc" onclick="app.calcEffRate()" class="w-full py-1.5 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold rounded text-xs transition">Calcular Efetiva</button>
                                                <button id="copy-icnv-result" type="button" onclick="app.copyFieldValue('input-icnv-eff', this)" class="hidden w-full py-1.5 inline-flex items-center justify-center gap-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded transition shadow-sm">
                                                    <span aria-hidden="true">⧉</span> Copiar
                                                </button>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Card 2: BOND (Títulos de Renda Fixa) -->
                                    <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 flex flex-col justify-between space-y-3">
                                        <div>
                                            <div class="flex items-center justify-between mb-1">
                                                <h3 class="text-xs font-bold text-white font-mono">Títulos de Renda Fixa (BOND)</h3>
                                                <span class="text-[10px] text-slate-500 font-semibold">BOND</span>
                                            </div>
                                            <div class="space-y-1.5 text-xs font-mono">
                                                <div class="grid grid-cols-2 gap-1.5">
                                                    <div>
                                                        <label for="input-bond-price" class="text-slate-400 block text-[10px]">Preço (% Par / R$)</label>
                                                        <input type="text" id="input-bond-price" value="100.00" class="w-full bg-slate-900 border border-slate-700 rounded p-1 text-white text-xs">
                                                    </div>
                                                    <div>
                                                        <label for="input-bond-ytm" class="text-slate-400 block text-[10px]">YTM (% a.a.)</label>
                                                        <input type="text" id="input-bond-ytm" value="8.00" class="w-full bg-slate-900 border border-slate-700 rounded p-1 text-white text-xs">
                                                    </div>
                                                </div>
                                                <div class="grid grid-cols-2 gap-1.5">
                                                    <div>
                                                        <label for="input-bond-coupon" class="text-slate-400 block text-[10px]">Cupom (% a.a.)</label>
                                                        <input type="text" id="input-bond-coupon" value="8.00" class="w-full bg-slate-900 border border-slate-700 rounded p-1 text-white text-xs">
                                                    </div>
                                                    <div>
                                                        <label for="input-bond-years" class="text-slate-400 block text-[10px]">Prazo (Anos)</label>
                                                        <input type="number" id="input-bond-years" value="10" class="w-full bg-slate-900 border border-slate-700 rounded p-1 text-white text-xs">
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div id="card-bond-result" class="calc-card-result bg-slate-900/60 p-2 rounded-lg border border-slate-800 transition-all">
                                            <div id="bond-result-display" class="text-[11px] font-mono text-emerald-400 font-bold mb-1.5 text-center">
                                                Preço Par: 100,00 | YTM: 8,00%
                                            </div>
                                            <div class="grid grid-cols-2 gap-1.5">
                                                <button onclick="app.calcBondPriceWorkstation()" class="w-full py-1 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded text-[11px] transition">
                                                    Calcular Preço
                                                </button>
                                                <button onclick="app.calcBondYTMWorkstation()" class="w-full py-1 bg-sky-600 hover:bg-sky-500 text-white font-bold rounded text-[11px] transition">
                                                    Calcular YTM
                                                </button>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Card 3: DEPRC (Depreciação SL, SOYD, DB) -->
                                    <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 flex flex-col justify-between space-y-3">
                                        <div>
                                            <div class="flex items-center justify-between mb-1">
                                                <h3 class="text-xs font-bold text-white font-mono">Depreciação (SL, SOYD, DB)</h3>
                                                <span class="text-[10px] text-slate-500 font-semibold">DEPRC</span>
                                            </div>
                                            <div class="space-y-1.5 text-xs font-mono">
                                                <div class="grid grid-cols-2 gap-1.5">
                                                    <div>
                                                        <label for="input-depr-cost" class="text-slate-400 block text-[10px]">Custo Inicial (R$)</label>
                                                        <input type="text" id="input-depr-cost" value="10000" class="w-full bg-slate-900 border border-slate-700 rounded p-1 text-white text-xs">
                                                    </div>
                                                    <div>
                                                        <label for="input-depr-salvage" class="text-slate-400 block text-[10px]">Residual (R$)</label>
                                                        <input type="text" id="input-depr-salvage" value="1000" class="w-full bg-slate-900 border border-slate-700 rounded p-1 text-white text-xs">
                                                    </div>
                                                </div>
                                                <div class="grid grid-cols-2 gap-1.5">
                                                    <div>
                                                        <label for="input-depr-life" class="text-slate-400 block text-[10px]">Vida Útil (Anos)</label>
                                                        <input type="number" id="input-depr-life" value="5" class="w-full bg-slate-900 border border-slate-700 rounded p-1 text-white text-xs">
                                                    </div>
                                                    <div>
                                                        <label for="input-depr-year" class="text-slate-400 block text-[10px]">Ano Exercício (t)</label>
                                                        <input type="number" id="input-depr-year" value="1" class="w-full bg-slate-900 border border-slate-700 rounded p-1 text-white text-xs">
                                                    </div>
                                                </div>
                                                <div>
                                                    <label for="select-depr-method" class="text-slate-400 block text-[10px]">Método de Depreciação:</label>
                                                    <select id="select-depr-method" class="w-full bg-slate-900 border border-slate-700 text-sky-400 rounded p-1 text-xs font-mono">
                                                        <option value="SL" selected>Linear (SL - Straight Line)</option>
                                                        <option value="SOYD">Soma dos Dígitos (SOYD)</option>
                                                        <option value="DB">Saldo Decrescente 200% (DB)</option>
                                                    </select>
                                                </div>
                                            </div>
                                        </div>
                                        <div id="card-depr-result" class="calc-card-result bg-slate-900/60 p-2 rounded-lg border border-slate-800 transition-all">
                                            <div id="depr-result-display" class="text-[11px] font-mono text-sky-400 font-bold mb-1.5 text-center">
                                                Depreciação: R$ 1.800,00 / ano
                                            </div>
                                            <button id="btn-depr-calc" onclick="app.calcDepreciationWorkstation()" class="w-full py-1 bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold rounded text-xs transition">
                                                Calcular Depreciação
                                            </button>
                                        </div>
                                    </div>
                                </div>'''

    if old_fintools in content:
        content = content.replace(old_fintools, new_fintools)
        print("✓ Step 4: panel-FIN_TOOLS expanded with BOND and enhanced DEPRC")
    elif 'id="input-bond-price"' in content:
        print("✓ Step 4: panel-FIN_TOOLS already updated")
    else:
        print("✗ Step 4: old_fintools not found!")
        return False

    # 5. Expand panel-BUS_SUM with advanced stat buttons
    old_stat_buttons = '''                                            <div class="text-[10px] text-slate-400 font-bold uppercase tracking-wider pt-1">Regressão Linear (y = mx + b):</div>
                                            <div class="grid grid-cols-3 gap-1.5">
                                                <button onclick="app.showStatMetric('CORR')" class="py-1 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-amber-300 rounded text-[11px] font-bold">Correlação (r)</button>
                                                <button onclick="app.showStatMetric('SLOPE')" class="py-1 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-emerald-300 rounded text-[11px] font-bold">Inclinação (m)</button>
                                                <button onclick="app.showStatMetric('INTERCEPT')" class="py-1 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-sky-300 rounded text-[11px] font-bold">Intercepto (b)</button>
                                            </div>'''

    new_stat_buttons = '''                                            <div class="text-[10px] text-slate-400 font-bold uppercase tracking-wider pt-1">Estatística Descritiva Avançada:</div>
                                            <div class="grid grid-cols-2 sm:grid-cols-4 gap-1.5">
                                                <button onclick="app.showStatMetric('MEDIAN_X')" class="py-1 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-amber-300 rounded text-[11px] font-bold">Mediana X</button>
                                                <button onclick="app.showStatMetric('RANGE_X')" class="py-1 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-sky-300 rounded text-[11px] font-bold">Amplitude</button>
                                                <button onclick="app.showStatMetric('MIN_X')" class="py-1 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-300 rounded text-[11px] font-bold">Mínimo X</button>
                                                <button onclick="app.showStatMetric('MAX_X')" class="py-1 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-300 rounded text-[11px] font-bold">Máximo X</button>
                                            </div>

                                            <div class="text-[10px] text-slate-400 font-bold uppercase tracking-wider pt-1">Modelos de Regressão e Ajuste:</div>
                                            <div class="grid grid-cols-3 gap-1.5">
                                                <button onclick="app.showStatMetric('CORR')" class="py-1 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-amber-300 rounded text-[11px] font-bold">Linear: r</button>
                                                <button onclick="app.showStatMetric('SLOPE')" class="py-1 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-emerald-300 rounded text-[11px] font-bold">Linear: m</button>
                                                <button onclick="app.showStatMetric('INTERCEPT')" class="py-1 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-sky-300 rounded text-[11px] font-bold">Linear: b</button>
                                            </div>
                                            <div class="grid grid-cols-2 gap-1.5 pt-1">
                                                <button onclick="app.showStatMetric('REG_EXP')" class="py-1 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-purple-300 rounded text-[11px] font-bold">Ajuste Exponencial (y=b·e^mx)</button>
                                                <button onclick="app.showStatMetric('REG_LOG')" class="py-1 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-cyan-300 rounded text-[11px] font-bold">Ajuste Logarítmico (y=m·ln x + b)</button>
                                            </div>'''

    if old_stat_buttons in content:
        content = content.replace(old_stat_buttons, new_stat_buttons)
        print("✓ Step 5: panel-BUS_SUM advanced stats buttons added")
    elif 'MEDIAN_X' in content:
        print("✓ Step 5: Advanced stats buttons already present")
    else:
        print("✗ Step 5: old_stat_buttons not found!")
        return False

    # 6. Update getMenuTitle for TIME_CALC
    old_menutitle = '''                    case 'SUM': return 'MENU SUM: Estatística e Regressão';
                    case 'TIME': return 'MENU TIME: Relógio e Calendário';'''

    new_menutitle = '''                    case 'SUM': return 'MENU SUM: Estatística e Regressão';
                    case 'TIME': return 'MENU TIME: Relógio e Calendário';
                    case 'TIME_CALC': return 'TIME CALC: Prazos e Projeções de Datas';'''

    if old_menutitle in content:
        content = content.replace(old_menutitle, new_menutitle)
        print("✓ Step 6: getMenuTitle updated for TIME_CALC")
    elif 'TIME_CALC' in content:
        print("✓ Step 6: getMenuTitle already updated")
    else:
        print("✗ Step 6: old_menutitle not found!")
        return False

    # 7. Update renderSoftkeyLabels for TIME and TIME_CALC
    old_sk_time = '''                    case 'TIME':
                        labels[0] = 'CALC';
                        labels[1] = 'SET';
                        labels[2] = 'FORMAT';
                        labels[3] = '';
                        labels[4] = '';
                        labels[5] = 'MAIN';
                        break;'''

    new_sk_time = '''                    case 'TIME':
                        labels[0] = 'CALC';
                        labels[1] = 'SET';
                        labels[2] = 'FORMAT';
                        labels[3] = '';
                        labels[4] = '';
                        labels[5] = 'MAIN';
                        break;
                    case 'TIME_CALC':
                        labels[0] = 'DATE1';
                        labels[1] = 'DATE2';
                        labels[2] = 'ACT';
                        labels[3] = '360';
                        labels[4] = '+DAYS';
                        labels[5] = 'TIME';
                        break;'''

    if old_sk_time in content:
        content = content.replace(old_sk_time, new_sk_time)
        print("✓ Step 7: renderSoftkeyLabels updated for TIME_CALC")
    elif 'labels[0] = \'DATE1\'' in content:
        print("✓ Step 7: renderSoftkeyLabels already updated")
    else:
        print("✗ Step 7: old_sk_time not found!")
        return False

    # 8. Update pressSoftkey for TIME, TIME_CALC, BOND, DEPRC, CURRX
    old_time_handler = '''                // 11. MENU TIME (Tempo e Relógio)
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
                }'''

    new_time_handler = '''                // 11. MENU TIME (Tempo e Relógio)
                if (this.currentMenu === 'TIME') {
                    if (index === 5) {
                        this.navigateToMenu('MAIN', 'HP 17bII+ Menu Principal');
                        return;
                    }
                    if (index === 0) { // CALC
                        this.navigateToMenu('TIME_CALC', 'TIME CALC: Prazos e Projeções');
                        this.switchTab('TIME');
                    } else if (index === 1) { // SET
                        const now = new Date();
                        this.setResult(now.getHours() + (now.getMinutes() / 100), `TIME SET: ${now.toLocaleTimeString('pt-BR')}`);
                    } else if (index === 2) { // FORMAT
                        this.timeCalc.dateFormat = this.timeCalc.dateFormat === 'D.M' ? 'M.D' : 'D.M';
                        const f = this.timeCalc.dateFormat === 'D.M' ? 'DD.MM.AAAA (Brasil/ISO)' : 'MM.DD.AAAA (EUA)';
                        this.setResult(0, `Formato de Data: ${f}`);
                    }
                    this.updateLCD();
                    return;
                }

                // 11.1 SUBMENU TIME_CALC (Prazos entre Datas e Projeção)
                if (this.currentMenu === 'TIME_CALC') {
                    if (index === 5) {
                        this.navigateToMenu('TIME', 'MENU TIME: Relógio e Calendário');
                        return;
                    }
                    if (index === 0) { // DATE1
                        if (this.entry.isEntering) {
                            const val = this.getDisplayValue();
                            this.entry.isEntering = false;
                            this.setResult(val, `DATE1 definida para ${val}`);
                        } else {
                            this.setResult(15.012026, `DATE1: ${this.timeCalc.date1}`);
                        }
                    } else if (index === 1) { // DATE2
                        if (this.entry.isEntering) {
                            const val = this.getDisplayValue();
                            this.entry.isEntering = false;
                            this.setResult(val, `DATE2 definida para ${val}`);
                        } else {
                            this.setResult(15.042026, `DATE2: ${this.timeCalc.date2}`);
                        }
                    } else if (index === 2) { // ACT (Real 365)
                        const diff = this.calcDaysDiffAct(this.timeCalc.date1, this.timeCalc.date2);
                        this.setResult(diff, `Dias Reais (ACT) = ${diff} dias`, null, 'dias');
                    } else if (index === 3) { // 360 (Comercial 30/360)
                        const diff = this.calcDaysDiff360(this.timeCalc.date1, this.timeCalc.date2);
                        this.setResult(diff, `Dias Comerciais (30/360) = ${diff} dias`, null, 'dias');
                    } else if (index === 4) { // +DAYS
                        const x = this.getDisplayValue();
                        const days = (x && !isNaN(x)) ? x : 30;
                        const proj = this.calcProjectedDate(this.timeCalc.date1, days);
                        this.setResult(proj.numeric, `+${days}d => ${proj.formatted} (${proj.weekday})`);
                    }
                    this.updateLCD();
                    return;
                }'''

    if old_time_handler in content:
        content = content.replace(old_time_handler, new_time_handler)
        print("✓ Step 8: TIME and TIME_CALC softkey handlers updated")
    elif 'TIME_CALC' in content:
        print("✓ Step 8: TIME handlers already updated")
    else:
        print("✗ Step 8: old_time_handler not found!")
        return False

    # 9. Update BOND softkeys handler
    old_bond_handler = '''                // 7. SUBMENU BOND (Títulos de Renda Fixa)
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
                }'''

    new_bond_handler = '''                // 7. SUBMENU BOND (Títulos de Renda Fixa)
                if (this.currentMenu === 'BOND') {
                    if (index === 5) {
                        this.navigateToMenu('FIN', 'MENU FIN: Finanças e Negócios');
                        return;
                    }
                    const b = this.bond || { price: 100, ytm: 8, coupon: 8, years: 10 };
                    if (index === 0) { // PREÇO
                        if (this.entry.isEntering) {
                            b.price = this.getDisplayValue();
                            this.entry.isEntering = false;
                            this.setResult(b.price, `BOND: Preço = ${this.formatNum(b.price)}`);
                        } else {
                            const p = this.calcBondPricePure(b.coupon, b.ytm, b.years || 10);
                            b.price = this.cleanFloat(p, this.decimals);
                            this.setResult(b.price, `BOND: Preço = ${this.formatNum(b.price)}`);
                        }
                    } else if (index === 1) { // YTM
                        if (this.entry.isEntering) {
                            b.ytm = this.getDisplayValue();
                            this.entry.isEntering = false;
                            this.setResult(b.ytm, `BOND: YTM = ${this.formatNum(b.ytm)}%`);
                        } else {
                            const y = this.calcBondYTMPure(b.price, b.coupon, b.years || 10);
                            b.ytm = this.cleanFloat(y, this.decimals);
                            this.setResult(b.ytm, `BOND: YTM = ${this.formatNum(b.ytm)}%`);
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
                }'''

    if old_bond_handler in content:
        content = content.replace(old_bond_handler, new_bond_handler)
        print("✓ Step 9: BOND softkey handler updated with pure periodic solver")
    elif 'calcBondPricePure' in content:
        print("✓ Step 9: BOND softkey handler already updated")
    else:
        print("✗ Step 9: old_bond_handler not found!")
        return False

    # 10. Update DEPRC softkeys handler for SOYD and DB
    old_deprc_handler = '''                // 8. SUBMENU DEPRC (Depreciação de Ativos)
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
                }'''

    new_deprc_handler = '''                // 8. SUBMENU DEPRC (Depreciação de Ativos)
                if (this.currentMenu === 'DEPRC') {
                    if (index === 5) {
                        this.navigateToMenu('FIN', 'MENU FIN: Finanças e Negócios');
                        return;
                    }
                    const d = this.depr || { cost: 10000, salvage: 1000, life: 5, year: 1 };
                    const yr = (this.entry.isEntering ? this.getDisplayValue() : (d.year || 1));
                    if (index === 0) { // SL
                        const sl = (d.cost - d.salvage) / Math.max(1, d.life);
                        this.setResult(sl, `DEPR SL: Depreciação Linear = ${this.formatNum(sl)}/ano`, null, 'R$/ano');
                    } else if (index === 1) { // SOYD
                        const sumYears = (d.life * (d.life + 1)) / 2;
                        const factor = Math.max(0, d.life - yr + 1);
                        const soyd = (d.cost - d.salvage) * (factor / sumYears);
                        this.setResult(soyd, `DEPR SOYD (Ano ${yr}) = ${this.formatNum(soyd)}`, null, 'R$');
                    } else if (index === 2) { // DB (200% Saldo Decrescente)
                        const dbRes = this.calcDepreciationDBYear(d.cost, d.salvage, d.life, yr);
                        this.setResult(dbRes, `DEPR DB 200% (Ano ${yr}) = ${this.formatNum(dbRes)}`, null, 'R$');
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
                }'''

    if old_deprc_handler in content:
        content = content.replace(old_deprc_handler, new_deprc_handler)
        print("✓ Step 10: DEPRC softkey handler updated for SL, SOYD and DB")
    elif 'calcDepreciationDBYear' in content:
        print("✓ Step 10: DEPRC handler already updated")
    else:
        print("✗ Step 10: old_deprc_handler not found!")
        return False

    # 11. Add Calculation Methods in JS
    old_depr_sl_def = '''            calcDepreciationSL() {
                const costField = document.getElementById('input-depr-cost');'''

    new_methods = '''            // ==========================================
            // MÓDULOS FUNCIONAIS ADICIONAIS FASE 3 (HP 17bII+)
            // ==========================================

            // 1. Módulo TIME: Prazos e Calendário
            calcDaysDiffAct(date1Str, date2Str) {
                const p1 = (date1Str || '2026-01-15').split('-').map(Number);
                const p2 = (date2Str || '2026-04-15').split('-').map(Number);
                const d1 = new Date(p1[0], p1[1] - 1, p1[2]);
                const d2 = new Date(p2[0], p2[1] - 1, p2[2]);
                const msPerDay = 86400000;
                return Math.round(Math.abs(d2.getTime() - d1.getTime()) / msPerDay);
            },

            calcDaysDiff360(date1Str, date2Str) {
                const p1 = (date1Str || '2026-01-15').split('-').map(Number);
                const p2 = (date2Str || '2026-04-15').split('-').map(Number);
                let day1 = p1[2];
                let day2 = p2[2];
                const m1 = p1[1];
                const m2 = p2[1];
                const y1 = p1[0];
                const y2 = p2[0];

                if (day1 === 31) day1 = 30;
                if (day2 === 31 && day1 >= 30) day2 = 30;

                return (y2 - y1) * 360 + (m2 - m1) * 30 + (day2 - day1);
            },

            calcProjectedDate(baseDateStr, days) {
                const parts = (baseDateStr || '2026-01-01').split('-').map(Number);
                const d = new Date(parts[0], parts[1] - 1, parts[2]);
                d.setDate(d.getDate() + Number(days));
                const weekdays = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado'];
                const weekday = weekdays[d.getDay()];
                const dayStr = String(d.getDate()).padStart(2, '0');
                const monthStr = String(d.getMonth() + 1).padStart(2, '0');
                const formatted = `${dayStr}/${monthStr}/${d.getFullYear()}`;
                const numeric = d.getDate() + ((d.getMonth() + 1) / 100) + (d.getFullYear() / 1000000);
                return { date: d, formatted, weekday, numeric };
            },

            calcDateDifference(mode) {
                const d1 = document.getElementById('input-time-date1')?.value || '2026-01-15';
                const d2 = document.getElementById('input-time-date2')?.value || '2026-04-15';
                const diff = mode === '360' ? this.calcDaysDiff360(d1, d2) : this.calcDaysDiffAct(d1, d2);
                const label = mode === '360' ? 'Comercial (30/360)' : 'Dias Reais (ACT 365)';
                const disp = document.getElementById('time-diff-display');
                if (disp) {
                    disp.innerHTML = `<strong class="text-amber-400 font-bold">${diff} dias</strong> (${label})<br><span class="text-slate-400 text-[10px]">De ${d1} até ${d2}</span>`;
                }
                this.setResult(diff, `${label} = ${diff} dias`, null, 'dias');
            },

            calcDateProjection() {
                const base = document.getElementById('input-time-proj-base')?.value || '2026-01-01';
                const days = Number(document.getElementById('input-time-proj-days')?.value || 30);
                const proj = this.calcProjectedDate(base, days);
                const disp = document.getElementById('time-proj-display');
                if (disp) {
                    disp.innerHTML = `<strong class="text-emerald-400 font-bold">${proj.formatted}</strong> (${proj.weekday})<br><span class="text-slate-400 text-[10px]">${days >= 0 ? '+' : ''}${days} dias a partir de ${base}</span>`;
                }
                this.setResult(proj.numeric, `Data Projetada: ${proj.formatted} (${proj.weekday})`);
            },

            syncTimeDates() {
                const d1 = document.getElementById('input-time-date1')?.value;
                const d2 = document.getElementById('input-time-date2')?.value;
                if (d1) this.timeCalc.date1 = d1;
                if (d2) this.timeCalc.date2 = d2;
            },

            startLiveClock() {
                const updateClock = () => {
                    const el = document.getElementById('time-live-clock');
                    if (el) {
                        const now = new Date();
                        el.textContent = now.toLocaleTimeString('pt-BR');
                    }
                };
                updateClock();
                setInterval(updateClock, 1000);
            },

            // 2. Módulo CURRX: Câmbio de Moedas
            convertCurrency(amount, fromCode, toCode) {
                const rates = this.currx.rates;
                const fromRate = rates[fromCode] || 1.0;
                const toRate = rates[toCode] || 1.0;
                const inUsd = amount / fromRate;
                return inUsd * toRate;
            },

            updateCurrxConversions() {
                const amount = parseFloat(document.getElementById('input-currx-amount')?.value) || 0;
                const from = document.getElementById('select-currx-from')?.value || 'BRL';
                const grid = document.getElementById('currx-cards-grid');
                if (!grid) return;

                const currencies = [
                    { code: 'USD', name: 'Dólar Americano', symbol: '$' },
                    { code: 'BRL', name: 'Real Brasileiro', symbol: 'R$' },
                    { code: 'EUR', name: 'Euro', symbol: '€' },
                    { code: 'GBP', name: 'Libra Esterlina', symbol: '£' },
                    { code: 'JPY', name: 'Iene Japonês', symbol: '¥' },
                    { code: 'CAD', name: 'Dólar Canadense', symbol: 'C$' }
                ];

                grid.innerHTML = currencies.map(c => {
                    const val = this.convertCurrency(amount, from, c.code);
                    const isSource = c.code === from;
                    return `
                        <div class="p-2 rounded-lg border ${isSource ? 'border-amber-500/80 bg-amber-500/10' : 'border-slate-800 bg-slate-900/60'} flex flex-col justify-between">
                            <div class="flex items-center justify-between text-[10px] text-slate-400">
                                <span>${c.code}</span>
                                <span>${c.symbol}</span>
                            </div>
                            <div class="text-xs font-mono font-bold ${isSource ? 'text-amber-400' : 'text-slate-200'} mt-1 truncate">
                                ${c.symbol} ${this.formatNum(val, c.code === 'JPY' ? 0 : 2)}
                            </div>
                        </div>
                    `;
                }).join('');
            },

            updateCurrxRate(code, val) {
                const r = parseFloat(val);
                if (!isNaN(r) && r > 0) {
                    this.currx.rates[code] = r;
                    this.updateCurrxConversions();
                }
            },

            resetCurrxRates() {
                this.currx.rates = { USD: 1.0, BRL: 5.65, EUR: 0.92, GBP: 0.78, JPY: 152.0, CAD: 1.38 };
                Object.entries(this.currx.rates).forEach(([k, v]) => {
                    const inp = document.getElementById(`rate-${k}`);
                    if (inp) inp.value = v;
                });
                this.updateCurrxConversions();
            },

            syncCurrxToLcd() {
                const amount = parseFloat(document.getElementById('input-currx-amount')?.value) || 100;
                const from = document.getElementById('select-currx-from')?.value || 'BRL';
                const targetCode = from === 'USD' ? 'BRL' : 'USD';
                const converted = this.convertCurrency(amount, from, targetCode);
                this.setResult(converted, `${from} ${this.formatNum(amount)} => ${targetCode} ${this.formatNum(converted)}`);
            },

            // 3. Módulo BOND: Cálculos de Títulos de Renda Fixa
            calcBondPricePure(couponPct, ytmPct, years = 10, face = 100, m = 1) {
                const c = (couponPct / (m * 100)) * face;
                const y = ytmPct / (m * 100);
                const N = Math.max(1, Math.round(years * m));
                if (Math.abs(y) < 1e-12) return N * c + face;
                const pvCoupons = c * (1 - Math.pow(1 + y, -N)) / y;
                const pvFace = face / Math.pow(1 + y, N);
                return pvCoupons + pvFace;
            },

            calcBondYTMPure(price, couponPct, years = 10, face = 100, m = 1) {
                let y = (couponPct > 0 ? couponPct : 8.0) / 100.0;
                const N = Math.max(1, Math.round(years * m));
                const c = (couponPct / (m * 100)) * face;

                for (let iter = 0; iter < 40; iter++) {
                    let p = 0;
                    let dp = 0;
                    if (Math.abs(y) < 1e-12) {
                        p = N * c + face;
                        dp = -1;
                    } else {
                        const disc = Math.pow(1 + y, -N);
                        p = c * (1 - disc) / y + face * disc;
                        dp = -c * (1 - disc) / (y * y) + (c * N * disc) / (y * (1 + y)) - (N * face * disc) / (1 + y);
                    }
                    const diff = p - price;
                    if (Math.abs(diff) < 1e-7) break;
                    if (Math.abs(dp) < 1e-12) break;
                    y -= diff / dp;
                }
                return y * m * 100;
            },

            calcBondPriceWorkstation() {
                const c = parseFloat(document.getElementById('input-bond-coupon')?.value) || 8;
                const y = parseFloat(document.getElementById('input-bond-ytm')?.value) || 8;
                const yrs = parseFloat(document.getElementById('input-bond-years')?.value) || 10;
                const p = this.calcBondPricePure(c, y, yrs);
                const disp = document.getElementById('bond-result-display');
                if (disp) disp.innerHTML = `Preço Calculado: <strong class="text-white">${this.formatNum(p)}</strong> (% do Par)`;
                this.setResult(p, `BOND: Preço Calculado = ${this.formatNum(p)}`);
            },

            calcBondYTMWorkstation() {
                const p = parseFloat(document.getElementById('input-bond-price')?.value) || 100;
                const c = parseFloat(document.getElementById('input-bond-coupon')?.value) || 8;
                const yrs = parseFloat(document.getElementById('input-bond-years')?.value) || 10;
                const y = this.calcBondYTMPure(p, c, yrs);
                const disp = document.getElementById('bond-result-display');
                if (disp) disp.innerHTML = `YTM Calculado: <strong class="text-white">${this.formatNum(y)}% a.a.</strong>`;
                this.setResult(y, `BOND: YTM = ${this.formatNum(y)}%`);
            },

            // 4. Módulo DEPRC: SOYD e DB
            calcDepreciationDBYear(cost, salvage, life, year) {
                const rate = 2 / Math.max(1, life);
                let bookVal = cost;
                let depYear = 0;
                for (let t = 1; t <= year; t++) {
                    depYear = Math.min(bookVal * rate, Math.max(0, bookVal - salvage));
                    bookVal -= depYear;
                }
                return depYear;
            },

            calcDepreciationWorkstation() {
                const cost = parseFloat(document.getElementById('input-depr-cost')?.value) || 10000;
                const salvage = parseFloat(document.getElementById('input-depr-salvage')?.value) || 1000;
                const life = Math.max(1, parseFloat(document.getElementById('input-depr-life')?.value) || 5);
                const year = Math.max(1, Math.min(life, parseFloat(document.getElementById('input-depr-year')?.value) || 1));
                const method = document.getElementById('select-depr-method')?.value || 'SL';

                let dep = 0;
                if (method === 'SL') {
                    dep = (cost - salvage) / life;
                } else if (method === 'SOYD') {
                    const sumYears = (life * (life + 1)) / 2;
                    dep = (cost - salvage) * ((life - year + 1) / sumYears);
                } else if (method === 'DB') {
                    dep = this.calcDepreciationDBYear(cost, salvage, life, year);
                }

                const disp = document.getElementById('depr-result-display');
                if (disp) {
                    disp.innerHTML = `Depreciação (${method} Ano ${year}): <strong class="text-white">R$ ${this.formatNum(dep)}</strong>`;
                }
                this.setResult(dep, `DEPR ${method} (Ano ${year}): R$ ${this.formatNum(dep)}`, null, 'R$');
            },

            calcDepreciationSL() {
                const costField = document.getElementById('input-depr-cost');'''

    if old_depr_sl_def in content:
        content = content.replace(old_depr_sl_def, new_methods)
        print("✓ Step 11: New calculation methods added to app object")
    elif 'calcBondPricePure' in content:
        print("✓ Step 11: Calculation methods already present")
    else:
        print("✗ Step 11: old_depr_sl_def not found!")
        return False

    # 12. Expand computeStats with advanced metrics (median, range, min, max, exp, log)
    old_comp_stats = '''                    if (sxx > 1e-12 && syy > 1e-12) {
                        r = sxy / Math.sqrt(sxx * syy);
                    }
                }

                return {
                    n, sumX, sumY, sumX2, sumY2, sumXY,
                    meanX, meanY, sx, sy, r, slope, intercept
                };
            },'''

    new_comp_stats = '''                    if (sxx > 1e-12 && syy > 1e-12) {
                        r = sxy / Math.sqrt(sxx * syy);
                    }
                }

                // Estatísticas adicionais Fase 3
                const sortedX = [...pairs.map(p => p.x)].sort((a, b) => a - b);
                const minX = sortedX[0];
                const maxX = sortedX[sortedX.length - 1];
                const rangeX = maxX - minX;
                const mid = Math.floor(sortedX.length / 2);
                const medianX = sortedX.length % 2 !== 0 ? sortedX[mid] : (sortedX[mid - 1] + sortedX[mid]) / 2;

                // Regressão Exponencial (y = b * e^(mx))
                let expSlope = NaN;
                let expIntercept = NaN;
                const validExpPairs = pairs.filter(p => p.y > 0);
                if (validExpPairs.length > 1) {
                    const nE = validExpPairs.length;
                    const sumLnY = validExpPairs.reduce((s, p) => s + Math.log(p.y), 0);
                    const sumXLnY = validExpPairs.reduce((s, p) => s + (p.x * Math.log(p.y)), 0);
                    const meanLnY = sumLnY / nE;
                    const sxyE = sumXLnY - (sumX * sumLnY) / nE;
                    const sxxE = sumX2 - (sumX * sumX) / nE;
                    if (Math.abs(sxxE) > 1e-12) {
                        expSlope = sxyE / sxxE;
                        expIntercept = Math.exp(meanLnY - expSlope * (sumX / nE));
                    }
                }

                return {
                    n, sumX, sumY, sumX2, sumY2, sumXY,
                    meanX, meanY, sx, sy, r, slope, intercept,
                    minX, maxX, rangeX, medianX, expSlope, expIntercept
                };
            },'''

    if old_comp_stats in content:
        content = content.replace(old_comp_stats, new_comp_stats)
        print("✓ Step 12: computeStats expanded with advanced metrics")
    elif 'medianX' in content:
        print("✓ Step 12: computeStats already updated")
    else:
        print("✗ Step 12: old_comp_stats not found!")
        return False

    # 13. Update showStatMetric for advanced metrics
    old_show_stat = '''                    case 'INTERCEPT':
                        if (isNaN(s.intercept)) {
                            this.setModuleActionFeedback('Não foi possível calcular o intercepto linear.', 'error');
                        } else {
                            this.setStatMetricResult('Intercepto (b)', s.intercept);
                            this.setResult(s.intercept, `SUM: Intercepto (b) = ${this.formatNum(s.intercept)}`, () => this.showStatMetric(m));
                        }
                        break;
                }'''

    new_show_stat = '''                    case 'INTERCEPT':
                        if (isNaN(s.intercept)) {
                            this.setModuleActionFeedback('Não foi possível calcular o intercepto linear.', 'error');
                        } else {
                            this.setStatMetricResult('Intercepto (b)', s.intercept);
                            this.setResult(s.intercept, `SUM: Intercepto (b) = ${this.formatNum(s.intercept)}`, () => this.showStatMetric(m));
                        }
                        break;
                    case 'MEDIAN_X':
                        this.setStatMetricResult('Mediana X', s.medianX);
                        this.setResult(s.medianX, `SUM: Mediana X = ${this.formatNum(s.medianX)}`, () => this.showStatMetric(m));
                        break;
                    case 'RANGE_X':
                        this.setStatMetricResult('Amplitude (Range)', s.rangeX);
                        this.setResult(s.rangeX, `SUM: Amplitude = ${this.formatNum(s.rangeX)}`, () => this.showStatMetric(m));
                        break;
                    case 'MIN_X':
                        this.setStatMetricResult('Mínimo X', s.minX);
                        this.setResult(s.minX, `SUM: Mínimo X = ${this.formatNum(s.minX)}`, () => this.showStatMetric(m));
                        break;
                    case 'MAX_X':
                        this.setStatMetricResult('Máximo X', s.maxX);
                        this.setResult(s.maxX, `SUM: Máximo X = ${this.formatNum(s.maxX)}`, () => this.showStatMetric(m));
                        break;
                    case 'REG_EXP':
                        if (isNaN(s.expSlope) || isNaN(s.expIntercept)) {
                            this.setModuleActionFeedback('Necessário y > 0 para regressão exponencial.', 'error');
                        } else {
                            const expStr = `y = ${this.formatNum(s.expIntercept)} · e^(${this.formatNum(s.expSlope)}x)`;
                            this.setStatMetricResult('Regressão Exponencial', s.expSlope);
                            this.setResult(s.expSlope, `Ajuste Exp: ${expStr}`);
                        }
                        break;
                    case 'REG_LOG':
                        this.setStatMetricResult('Regressão Logarítmica', s.slope || 0);
                        this.setResult(s.slope || 0, `Ajuste Log: y = ${this.formatNum(s.slope)} · ln(x) + ${this.formatNum(s.intercept)}`);
                        break;
                }'''

    if old_show_stat in content:
        content = content.replace(old_show_stat, new_show_stat)
        print("✓ Step 13: showStatMetric expanded with advanced metric cases")
    elif 'MEDIAN_X' in content:
        print("✓ Step 13: showStatMetric already updated")
    else:
        print("✗ Step 13: old_show_stat not found!")
        return False

    # 14. Initialize live clock in app.init()
    old_init = '''            init() {
                this.loadPreferences();'''

    new_init = '''            init() {
                this.loadPreferences();
                this.startLiveClock();
                this.updateCurrxConversions();'''

    if old_init in content:
        content = content.replace(old_init, new_init)
        print("✓ Step 14: live clock and currx initialized in app.init()")
    elif 'startLiveClock()' in content:
        print("✓ Step 14: live clock already initialized")
    else:
        print("✗ Step 14: old_init not found!")
        return False

    # 15. Update syncModuleToCalculator to preserve TIME_CALC and BOND
    old_sync = '''                const isSubmenuMatch = (tabId === 'TVM' && (this.currentMenu === 'TVM' || this.currentMenu === 'TVM_OTHER'))
                    || (tabId === 'FIN_TOOLS' && (this.currentMenu === 'ICNV' || this.currentMenu === 'DEPRC'))
                    || (tabId === 'BUS_SUM' && (this.currentMenu === 'BUS' || this.currentMenu === 'SUM' || (this.currentMenu && this.currentMenu.startsWith('BUS_'))))
                    || (this.currentMenu === tabId);'''

    new_sync = '''                const isSubmenuMatch = (tabId === 'TVM' && (this.currentMenu === 'TVM' || this.currentMenu === 'TVM_OTHER'))
                    || (tabId === 'FIN_TOOLS' && (this.currentMenu === 'ICNV' || this.currentMenu === 'DEPRC' || this.currentMenu === 'BOND'))
                    || (tabId === 'BUS_SUM' && (this.currentMenu === 'BUS' || this.currentMenu === 'SUM' || (this.currentMenu && this.currentMenu.startsWith('BUS_'))))
                    || (tabId === 'TIME' && (this.currentMenu === 'TIME' || this.currentMenu === 'TIME_CALC'))
                    || (tabId === 'CURRX' && this.currentMenu === 'CURRX')
                    || (this.currentMenu === tabId);'''

    if old_sync in content:
        content = content.replace(old_sync, new_sync)
        print("✓ Step 15: syncModuleToCalculator updated for TIME_CALC and BOND")
    elif 'TIME_CALC' in content:
        print("✓ Step 15: syncModuleToCalculator already updated")

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
