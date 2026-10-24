# -*- coding: utf-8 -*-

def update_pyr(path):
    with open(path, 'rb') as f:
        content = f.read().decode('utf-8')

    target = """                                                    <label for="input-tvm-PYR" class="text-[11px] font-mono text-slate-300 font-bold block truncate">P/YR (Períodos/Ano)</label>
                                                    <span class="text-[10px] text-slate-400 font-mono">Unid: <strong class="text-slate-300 font-normal">per./ano</strong></span>"""

    replacement = """                                                    <label for="input-tvm-PYR" class="text-[11px] font-mono text-slate-300 font-bold block truncate">P/YR (Pagtos/ano)</label>
                                                    <span class="text-[10px] text-slate-400 font-mono">Unid: <strong class="text-slate-300 font-normal">pagtos/ano</strong></span>"""

    norm_c = content.replace('\r\n', '\n')
    norm_t = target.replace('\r\n', '\n')
    norm_r = replacement.replace('\r\n', '\n')

    if norm_t not in norm_c:
        print(f"Error: target not found in {path}")
        return False

    norm_c = norm_c.replace(norm_t, norm_r, 1)
    with open(path, 'wb') as f:
        f.write(norm_c.replace('\n', '\r\n').encode('utf-8'))

    print(f"Successfully updated {path}")
    return True

ok1 = update_pyr('Calculadora Financeira 17bIi.html')
ok2 = update_pyr('index.html')
if not (ok1 and ok2):
    import sys
    sys.exit(1)

