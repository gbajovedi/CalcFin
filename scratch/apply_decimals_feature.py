# -*- coding: utf-8 -*-
import hashlib

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Header controls: Add decimals-control-group next to TVM button
    target_tvm_btn = """                <button id="btn-tvm-toggle" type="button" aria-pressed="false" onclick="app.toggleBgnEnd()" class="px-2.5 py-1 sm:px-3 sm:py-1.5 rounded-lg text-[11px] sm:text-xs font-mono font-bold bg-slate-800/90 hover:bg-slate-700 border border-slate-700 text-sky-400 transition">
                    <span id="label-tvm-indicator">TVM: END</span>
                </button>"""

    replacement_tvm_btn = """                <button id="btn-tvm-toggle" type="button" aria-pressed="false" onclick="app.toggleBgnEnd()" class="px-2.5 py-1 sm:px-3 sm:py-1.5 rounded-lg text-[11px] sm:text-xs font-mono font-bold bg-slate-800/90 hover:bg-slate-700 border border-slate-700 text-sky-400 transition">
                    <span id="label-tvm-indicator">TVM: END</span>
                </button>
                <div id="decimals-control-group" class="inline-flex items-center rounded-lg border border-slate-700 bg-slate-800/90 p-0.5 text-[11px] sm:text-xs font-mono font-bold shadow-sm" role="group" aria-label="Controle de casas decimais">
                    <button id="btn-dec-decrease" type="button" onclick="app.decrementDecimals()" class="h-6 w-6 sm:h-7 sm:w-7 rounded-md bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition flex items-center justify-center font-bold text-sm leading-none focus:outline-none focus:ring-1 focus:ring-amber-400" title="Diminuir casas decimais" aria-label="Diminuir casas decimais">
                        −
                    </button>
                    <span id="label-decimals-indicator" class="px-2 text-slate-200 select-none text-center whitespace-nowrap min-w-[3.5rem]" title="Quantidade de dígitos após a vírgula">
                        4 casas
                    </span>
                    <button id="btn-dec-increase" type="button" onclick="app.incrementDecimals()" class="h-6 w-6 sm:h-7 sm:w-7 rounded-md bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition flex items-center justify-center font-bold text-sm leading-none focus:outline-none focus:ring-1 focus:ring-amber-400" title="Aumentar casas decimais" aria-label="Aumentar casas decimais">
                        +
                    </button>
                </div>"""

    assert target_tvm_btn in content, f"target_tvm_btn not found in {filepath}"
    content = content.replace(target_tvm_btn, replacement_tvm_btn)
    print(f"Added decimals-control-group to {filepath}")

    # 2. LCD dec badge and initial line 2 value
    target_lcd_badge = """<span id="lcdDecBadge" class="font-bold">2 DEC</span>"""
    repl_lcd_badge = """<span id="lcdDecBadge" class="font-bold">4 DEC</span>"""
    assert target_lcd_badge in content, f"target_lcd_badge not found in {filepath}"
    content = content.replace(target_lcd_badge, repl_lcd_badge)

    target_lcd_line2 = """                            <div id="lcdLine2" class="text-right text-2xl sm:text-4xl font-black tracking-tight text-slate-950 my-1 leading-tight">
                                0,00
                            </div>"""
    repl_lcd_line2 = """                            <div id="lcdLine2" class="text-right text-2xl sm:text-4xl font-black tracking-tight text-slate-950 my-1 leading-tight">
                                0,0000
                            </div>"""
    if target_lcd_line2 in content:
        content = content.replace(target_lcd_line2, repl_lcd_line2)

    # 3. Initial state decimals: 4
    target_state_dec = """            shiftActive: false,
            decimals: 2,"""
    repl_state_dec = """            shiftActive: false,
            decimals: 4,"""
    assert target_state_dec in content, f"target_state_dec not found in {filepath}"
    content = content.replace(target_state_dec, repl_state_dec)

    # 4. cleanFloat fallback
    target_clean_float = """const d = (decimals !== null && decimals !== undefined) ? decimals : 2;"""
    repl_clean_float = """const d = (decimals !== null && decimals !== undefined) ? decimals : 4;"""
    assert target_clean_float in content, f"target_clean_float not found in {filepath}"
    content = content.replace(target_clean_float, repl_clean_float)

    # 5. setDecimals and new methods: updateDecimalsUI, incrementDecimals, decrementDecimals
    target_set_dec = """            setDecimals(d) {
                this.decimals = d;
                document.getElementById('lcdLine1').textContent = `Exibição fixada em ${d} casas decimais`;
                this.renderSolveVariables();
                this.syncStateToInputs();
                this.updateLCD();
                this.saveWorkspaceState();
            },"""

    repl_set_dec = """            updateDecimalsUI() {
                const decEl = document.getElementById('lcdDecBadge');
                if (decEl) decEl.textContent = `${this.decimals} DEC`;

                const decInd = document.getElementById('label-decimals-indicator');
                if (decInd) decInd.textContent = `${this.decimals} ${this.decimals === 1 ? 'casa' : 'casas'}`;

                const btnDec = document.getElementById('btn-dec-decrease');
                if (btnDec) {
                    btnDec.disabled = this.decimals <= 0;
                    btnDec.classList.toggle('opacity-40', this.decimals <= 0);
                    btnDec.classList.toggle('cursor-not-allowed', this.decimals <= 0);
                }

                const btnInc = document.getElementById('btn-dec-increase');
                if (btnInc) {
                    btnInc.disabled = this.decimals >= 11;
                    btnInc.classList.toggle('opacity-40', this.decimals >= 11);
                    btnInc.classList.toggle('cursor-not-allowed', this.decimals >= 11);
                }
            },

            setDecimals(d) {
                this.decimals = Math.max(0, Math.min(11, d));
                const lcd1 = document.getElementById('lcdLine1');
                if (lcd1) lcd1.textContent = `Exibição fixada em ${this.decimals} casas decimais`;
                this.updateDecimalsUI();
                this.renderSolveVariables();
                this.syncStateToInputs();
                this.updateLCD();
                this.saveWorkspaceState();
            },

            incrementDecimals() {
                this.triggerKeyFeedback();
                if (this.decimals < 11) {
                    this.setDecimals(this.decimals + 1);
                }
            },

            decrementDecimals() {
                this.triggerKeyFeedback();
                if (this.decimals > 0) {
                    this.setDecimals(this.decimals - 1);
                }
            },"""

    assert target_set_dec in content, f"target_set_dec not found in {filepath}"
    content = content.replace(target_set_dec, repl_set_dec)

    # 6. init visual indicators sync
    target_init_sync = """                const modeInd = document.getElementById('label-mode-indicator');
                if (modeInd) modeInd.textContent = `MODO: ${this.mode}`;
                this.setTvmMode(this.tvm.isBegin);"""

    repl_init_sync = """                const modeInd = document.getElementById('label-mode-indicator');
                if (modeInd) modeInd.textContent = `MODO: ${this.mode}`;
                this.setTvmMode(this.tvm.isBegin);
                this.updateDecimalsUI();"""

    assert target_init_sync in content, f"target_init_sync not found in {filepath}"
    content = content.replace(target_init_sync, repl_init_sync)

    # 7. resetToFactoryDefaults
    target_factory_dec = """                this.mode = 'RPN';
                this.decimals = 2;"""
    repl_factory_dec = """                this.mode = 'RPN';
                this.decimals = 4;"""
    assert target_factory_dec in content, f"target_factory_dec not found in {filepath}"
    content = content.replace(target_factory_dec, repl_factory_dec)

    target_factory_end = """                this.saveWorkspaceState();
                this.updateLCD();
                this.showFactoryResetModal();"""
    repl_factory_end = """                this.saveWorkspaceState();
                this.updateLCD();
                this.updateDecimalsUI();
                this.showFactoryResetModal();"""
    if target_factory_end in content:
        content = content.replace(target_factory_end, repl_factory_end)

    # 8. saveWorkspaceState & loadWorkspaceState migration
    target_save_ws = """                        mode: this.mode,
                        decimals: this.decimals,"""
    repl_save_ws = """                        mode: this.mode,
                        decimals: this.decimals,
                        hasCustomDecimals: true,"""
    if target_save_ws in content:
        content = content.replace(target_save_ws, repl_save_ws)

    target_load_ws = """                    if (typeof state.decimals === 'number' && state.decimals >= 0 && state.decimals <= 11) {
                        this.decimals = state.decimals;
                    }"""
    repl_load_ws = """                    if (typeof state.decimals === 'number' && state.decimals >= 0 && state.decimals <= 11) {
                        if (state.decimals === 2 && !state.hasCustomDecimals) {
                            this.decimals = 4;
                        } else {
                            this.decimals = state.decimals;
                        }
                    } else {
                        this.decimals = 4;
                    }"""
    assert target_load_ws in content, f"target_load_ws not found in {filepath}"
    content = content.replace(target_load_ws, repl_load_ws)

    # 9. Light mode styling
    target_light_css = """        body.light-mode header [class*="bg-slate-800"],
        body.light-mode header [class*="bg-slate-900"] {
            background: #eef2f7 !important;
            border-color: #cbd5e1 !important;
            color: #1e293b !important;
        }"""

    repl_light_css = """        body.light-mode header [class*="bg-slate-800"],
        body.light-mode header [class*="bg-slate-900"] {
            background: #eef2f7 !important;
            border-color: #cbd5e1 !important;
            color: #1e293b !important;
        }
        body.light-mode #label-decimals-indicator {
            color: #1e293b !important;
        }
        body.light-mode #decimals-control-group button {
            background: #e2e8f0 !important;
            color: #1e293b !important;
        }
        body.light-mode #decimals-control-group button:hover {
            background: #cbd5e1 !important;
        }"""

    if target_light_css in content:
        content = content.replace(target_light_css, repl_light_css)

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

