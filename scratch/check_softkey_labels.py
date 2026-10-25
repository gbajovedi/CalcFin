import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Calculadora Financeira 17bIi.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("renderSoftkeyLabels()")
print(text[idx:idx+2500])

