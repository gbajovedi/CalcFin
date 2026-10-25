import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('Calculadora Financeira 17bIi.html', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'id=["\']solve-library-list["\']', text):
    print(m.start())
    print(text[m.start()-200:m.start()+400])
    print('='*50)

