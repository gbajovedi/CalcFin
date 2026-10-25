# -*- coding: utf-8 -*-
import hashlib

def remove_duplicates(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove duplicate tab buttons
    old_tabs = """                    <button onclick="app.switchTab('TIME')" id="tab-TIME" role="tab" tabindex="-1" aria-controls="panel-TIME" aria-selected="false" title="Tempo, relógio e calendário — contagem de dias 365 e 360" aria-label="Tempo e calendário" class="tab-btn px-3 py-2 rounded-xl text-xs font-bold transition whitespace-nowrap text-slate-400 hover:text-white hover:bg-slate-800/60 font-mono">
                        Tempo e calendário
                    </button>
                    <button onclick="app.switchTab('CURRX')" id="tab-CURRX" role="tab" tabindex="-1" aria-controls="panel-CURRX" aria-selected="false" title="Câmbio de moedas internacionais — USD, EUR, GBP, BRL" aria-label="Câmbio de moedas" class="tab-btn px-3 py-2 rounded-xl text-xs font-bold transition whitespace-nowrap text-slate-400 hover:text-white hover:bg-slate-800/60 font-mono">
                        Câmbio de moedas
                    </button>
                    <button onclick="app.switchTab('TIME')" id="tab-TIME" role="tab" tabindex="-1" aria-controls="panel-TIME" aria-selected="false" title="Tempo, relógio e calendário — contagem de dias 365 e 360" aria-label="Tempo e calendário" class="tab-btn px-3 py-2 rounded-xl text-xs font-bold transition whitespace-nowrap text-slate-400 hover:text-white hover:bg-slate-800/60 font-mono">
                        Tempo e calendário
                    </button>
                    <button onclick="app.switchTab('CURRX')" id="tab-CURRX" role="tab" tabindex="-1" aria-controls="panel-CURRX" aria-selected="false" title="Câmbio de moedas internacionais — USD, EUR, GBP, BRL" aria-label="Câmbio de moedas" class="tab-btn px-3 py-2 rounded-xl text-xs font-bold transition whitespace-nowrap text-slate-400 hover:text-white hover:bg-slate-800/60 font-mono">
                        Câmbio de moedas
                    </button>"""

    new_tabs = """                    <button onclick="app.switchTab('TIME')" id="tab-TIME" role="tab" tabindex="-1" aria-controls="panel-TIME" aria-selected="false" title="Tempo, relógio e calendário — contagem de dias 365 e 360" aria-label="Tempo e calendário" class="tab-btn px-3 py-2 rounded-xl text-xs font-bold transition whitespace-nowrap text-slate-400 hover:text-white hover:bg-slate-800/60 font-mono">
                        Tempo e calendário
                    </button>
                    <button onclick="app.switchTab('CURRX')" id="tab-CURRX" role="tab" tabindex="-1" aria-controls="panel-CURRX" aria-selected="false" title="Câmbio de moedas internacionais — USD, EUR, GBP, BRL" aria-label="Câmbio de moedas" class="tab-btn px-3 py-2 rounded-xl text-xs font-bold transition whitespace-nowrap text-slate-400 hover:text-white hover:bg-slate-800/60 font-mono">
                        Câmbio de moedas
                    </button>"""

    assert old_tabs in content, f"old_tabs not found in {filepath}"
    content = content.replace(old_tabs, new_tabs)
    print(f"Cleaned duplicate tabs in {filepath}")

    # 2. Remove duplicate panels
    panel_snippet = """                            <!-- PAINEL TEMPO E CALENDÁRIO (TIME) -->\n                            <div id="panel-TIME" role="tabpanel" aria-labelledby="tab-TIME" tabindex="0" class="module-panel hidden flex flex-col gap-3">"""
    first_idx = content.find(panel_snippet)
    assert first_idx != -1, f"panel_snippet first not found in {filepath}"
    second_idx = content.find(panel_snippet, first_idx + 1)
    assert second_idx != -1, f"panel_snippet second not found in {filepath}"

    end_marker = "\n                        </div>\n                    </div>\n\n                </div>\n            </section>"
    end_idx = content.find(end_marker, second_idx)
    assert end_idx != -1, f"end_marker not found in {filepath}"

    # Remove the duplicate block from second_idx up to end_idx
    content = content[:second_idx] + content[end_idx:]
    print(f"Cleaned duplicate panel block in {filepath}")

    # Ensure CRLF
    content = content.replace('\r\n', '\n').replace('\n', '\r\n')

    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        f.write(content)

remove_duplicates("Calculadora Financeira 17bIi.html")
remove_duplicates("index.html")

# Check hashes
h1 = hashlib.sha256(open("Calculadora Financeira 17bIi.html", "rb").read()).hexdigest()
h2 = hashlib.sha256(open("index.html", "rb").read()).hexdigest()
print(f"SHA-256 Calculadora Financeira 17bIi.html: {h1}")
print(f"SHA-256 index.html:                       {h2}")
assert h1 == h2, "Hashes do not match!"
print("PARITY VERIFIED: Both files are 100% byte-for-byte identical!")

