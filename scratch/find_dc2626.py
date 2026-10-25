import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('Calculadora Financeira 17bIi.html', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'#dc2626|rgb\(220,\s*38,\s*38\)', text):
    line_no = text[:m.start()].count('\n') + 1
    print(f"Line {line_no}:")
    print(text[max(0, m.start() - 150):min(len(text), m.end() + 150)])
    print('='*50)

