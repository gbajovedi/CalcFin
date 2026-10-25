import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Calculadora Financeira 17bIi.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'alphaBuffer', text)]
print(f"Total matches of alphaBuffer: {len(matches)}")
for idx in matches:
    print(text[max(0, idx-40):min(len(text), idx+100)])
    print('---')

