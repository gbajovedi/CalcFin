import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('Calculadora Financeira 17bIi.html', encoding='utf-8') as f:
    text = f.read()

idx = text.find('PADRÃO DE FÁBRICA RESTAURADO')
print(text[idx-400:idx+600])

