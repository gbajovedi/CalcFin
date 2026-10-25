with open('Calculadora Financeira 17bIi.html', encoding='utf-8') as f:
    text = f.read()

idx = text.find('#workstation-left-wrapper {\n            color: #1e293b !important;')
if idx != -1:
    print("Found at index", idx)
    print(text[idx-200:idx+300])
else:
    print("Not found exact, searching partial")
    for m in re.finditer(r'#workstation-left-wrapper\s*{\s*color:\s*#1e293b', text):
        print(text[m.start()-200:m.start()+300])

