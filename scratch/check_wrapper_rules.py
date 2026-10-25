import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('Calculadora Financeira 17bIi.html', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'#workstation-left-wrapper[^{]+{[^}]+}', text):
    print(m.group(0))
    print('-'*40)

