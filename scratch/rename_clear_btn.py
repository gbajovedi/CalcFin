# -*- coding: utf-8 -*-
import hashlib

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

target = '<button id="solve-clear-variables" type="button" onclick="app.clearSolveVariables()" class="utility-control" aria-label="Limpar variáveis da fórmula atual">Limpar variáveis</button>'
replacement = '<button id="solve-clear-variables" type="button" onclick="app.clearSolveVariables()" class="utility-control" aria-label="Limpar campos da fórmula atual" title="Limpar todos os campos da fórmula atual">Limpar Campo</button>'

for fn in ['Calculadora Financeira 17bIi.html', 'index.html']:
    with open(fn, 'r', encoding='utf-8') as f:
        text = f.read()
    if target not in text:
        raise ValueError(f"Target not found in {fn}")
    text = text.replace(target, replacement, 1)
    with open(fn, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(text)
    print(f"Updated {fn}")

h1 = sha256_file('Calculadora Financeira 17bIi.html')
h2 = sha256_file('index.html')
print(f"Calculadora Financeira 17bIi.html SHA256: {h1}")
print(f"index.html SHA256:                        {h2}")
assert h1 == h2, "Hash mismatch"
print("PERFECT MATCH")

