import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Calculadora Financeira 17bIi.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

print("=== HTML containing sound-toggle / mobileFeedback ===")
for m in re.finditer(r'<[^>]*toggleMobileFeedback[^>]*>', text):
    start = max(0, m.start() - 200)
    end = min(len(text), m.end() + 200)
    print(text[start:end])
    print("-" * 50)

print("\n=== JS methods around mobileFeedback ===")
idx = text.find('initMobileFeedback() {')
if idx != -1:
    print(text[idx-100:idx+1500])
