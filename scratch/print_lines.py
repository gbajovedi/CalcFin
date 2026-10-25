with open('Calculadora Financeira 17bIi.html', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(2225, 2270):
    print(f"{i+1}: {lines[i]}", end='')

