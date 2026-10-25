# -*- coding: utf-8 -*-
import hashlib

def apply_fix():
    with open('Calculadora Financeira 17bIi.html', 'r', encoding='utf-8') as f:
        content = f.read()

    target = '''                this.activeTab = 'SOLVE';
                this.mobileView = 'calculator';
                this.favoriteFormulas = new Set(['coef_financiamento_carencia_premio', 'converter_taxas_equivalentes', 'taxa_pro_rata_die']);'''
    replacement = '''                this.activeTab = 'SOLVE';
                this.mobileView = 'calculator';
                this.switchTab('SOLVE');
                this.setMobileView('calculator', false);
                this.favoriteFormulas = new Set(['coef_financiamento_carencia_premio', 'converter_taxas_equivalentes', 'taxa_pro_rata_die']);'''
    assert target in content, "target not found"
    content = content.replace(target, replacement, 1)

    # Ensure CRLF line endings
    content_crlf = content.replace('\r\n', '\n').replace('\n', '\r\n')

    with open('Calculadora Financeira 17bIi.html', 'wb') as f:
        f.write(content_crlf.encode('utf-8'))

    with open('index.html', 'wb') as f:
        f.write(content_crlf.encode('utf-8'))

    h1 = hashlib.sha256(open('Calculadora Financeira 17bIi.html', 'rb').read()).hexdigest()
    h2 = hashlib.sha256(open('index.html', 'rb').read()).hexdigest()
    print(f"SHA-256 Calculadora Financeira 17bIi.html: {h1}")
    print(f"SHA-256 index.html:                       {h2}")
    assert h1 == h2, "Hashes do not match!"
    print("FIX APPLIED AND PARITY VERIFIED!")

if __name__ == '__main__':
    apply_fix()
