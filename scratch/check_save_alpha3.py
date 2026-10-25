import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Calculadora Financeira 17bIi.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'alphaBuffer', text)]
for idx in matches[-3:]:
    print(text[idx-100:idx+400])
    print('===')

