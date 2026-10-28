# -*- coding: utf-8 -*-
import hashlib

def apply_pyr_autofill():
    with open('Calculadora Financeira 17bIi.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update calculateTVM step 1
    target1 = '''                // 1. Ler e validar P/YR (não auto-preenche 12 na interface)
                const pyrField = document.getElementById('input-tvm-PYR');
                const rawPyr = (pyrField && pyrField.value.trim() !== '') ? this.parseNumericValue(pyrField.value) : null;
                const pyr = (rawPyr && rawPyr > 0) ? rawPyr : 12;
                this.tvm.PYR = rawPyr;'''

    replacement1 = '''                // 1. Ler e validar P/YR (se não preenchido, preenche automaticamente com 1)
                const pyrField = document.getElementById('input-tvm-PYR');
                let rawPyr = (pyrField && pyrField.value.trim() !== '') ? this.parseNumericValue(pyrField.value) : null;
                if (rawPyr === null || !Number.isFinite(rawPyr) || rawPyr <= 0) {
                    rawPyr = 1;
                    if (pyrField) pyrField.value = '1';
                }
                this.tvm.PYR = rawPyr;
                const pyr = rawPyr;'''

    assert target1 in content, "target1 not found in content"
    content = content.replace(target1, replacement1, 1)

    # 2. Update generateAmortizationTable P/YR handling
    target2 = '''                let balance = Math.abs(this.tvm.PV !== null ? this.tvm.PV : (pvField ? this.parseNumericValue(pvField.value) || 0 : 0));
                const pyr = this.tvm.PYR || 12;'''

    replacement2 = '''                let balance = Math.abs(this.tvm.PV !== null ? this.tvm.PV : (pvField ? this.parseNumericValue(pvField.value) || 0 : 0));
                let pyrVal = (this.tvm.PYR !== null && this.tvm.PYR !== undefined && this.tvm.PYR > 0) ? this.tvm.PYR : (pyrField ? this.parseNumericValue(pyrField.value) : null);
                if (pyrVal === null || !Number.isFinite(pyrVal) || pyrVal <= 0) {
                    pyrVal = 1;
                    if (pyrField && pyrField.value.trim() === '') pyrField.value = '1';
                    this.tvm.PYR = 1;
                }
                const pyr = pyrVal;'''

    assert target2 in content, "target2 not found in content"
    content = content.replace(target2, replacement2, 1)

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
    print("REPLACEMENTS APPLIED AND PARITY VERIFIED!")

if __name__ == '__main__':
    apply_pyr_autofill()
