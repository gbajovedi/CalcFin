import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('Calculadora Financeira 17bIi.html', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'computeTVM|calculateTVM|calcTVM|solveTVM|computeTvm', text, re.IGNORECASE):
    print(m.start())
    print(text[m.start()-50:m.start()+250])
    print('='*50)

