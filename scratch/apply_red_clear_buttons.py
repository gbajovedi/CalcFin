# -*- coding: utf-8 -*-
import hashlib

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update CSS
    css_target = """        #solve-clear-variables,
        #module-clear-fields-btn,
        .btn-clear-module {
            border: 1px solid #b91c1c;
            background: #b91c1c;
            color: #ffffff;
            font-weight: 700;
            text-decoration: none;
            cursor: pointer;
            transition: background-color .15s ease, border-color .15s ease, box-shadow .15s ease;
        }
        #solve-clear-variables:hover,
        #module-clear-fields-btn:hover,
        .btn-clear-module:hover {
            background: #991b1b;
            border-color: #991b1b;
            color: #ffffff;
        }
        #solve-clear-variables:focus-visible,
        #module-clear-fields-btn:focus-visible,
        .btn-clear-module:focus-visible {
            outline: 3px solid #fbbf24;
            outline-offset: 2px;
        }"""

    css_replacement = """        #solve-clear-variables,
        #module-clear-fields-btn,
        .btn-clear-module {
            border: 1px solid #b91c1c !important;
            background: #b91c1c !important;
            color: #ffffff !important;
            font-weight: 700;
            text-decoration: none;
            cursor: pointer;
            transition: background-color .15s ease, border-color .15s ease, box-shadow .15s ease;
        }
        #solve-clear-variables:hover,
        #module-clear-fields-btn:hover,
        .btn-clear-module:hover {
            background: #991b1b !important;
            border-color: #991b1b !important;
            color: #ffffff !important;
        }
        #solve-clear-variables:focus-visible,
        #module-clear-fields-btn:focus-visible,
        .btn-clear-module:focus-visible {
            outline: 3px solid #fbbf24;
            outline-offset: 2px;
        }
        body.light-mode #solve-clear-variables,
        body.light-mode #module-clear-fields-btn,
        body.light-mode .btn-clear-module {
            border-color: #b91c1c !important;
            background: #b91c1c !important;
            color: #ffffff !important;
        }
        body.light-mode #solve-clear-variables:hover,
        body.light-mode #module-clear-fields-btn:hover,
        body.light-mode .btn-clear-module:hover {
            border-color: #991b1b !important;
            background: #991b1b !important;
            color: #ffffff !important;
        }"""

    if css_target in content:
        content = content.replace(css_target, css_replacement)
        print(f"Updated CSS in {filepath}")
    else:
        print(f"WARNING: CSS target not found in {filepath}")

    # Remove text-white from module-clear-fields-btn and panel clear buttons to avoid light-mode text-white override
    old_mod_btn = 'class="btn-clear-module px-2.5 py-1 rounded-lg border border-red-700 bg-red-700 hover:bg-red-800 text-white text-[11px] font-bold transition flex items-center justify-center shrink-0 shadow-sm"'
    new_mod_btn = 'class="btn-clear-module px-2.5 py-1 rounded-lg border border-red-700 bg-red-700 hover:bg-red-800 text-[11px] font-bold transition flex items-center justify-center shrink-0 shadow-sm"'
    if old_mod_btn in content:
        content = content.replace(old_mod_btn, new_mod_btn)
        print(f"Updated module btn classes in {filepath}")

    old_tvm_btn = 'class="btn-clear-module inline-flex items-center justify-center px-2.5 py-1 rounded-lg text-xs font-bold bg-red-700 hover:bg-red-800 text-white border border-red-700 transition shadow-sm"'
    new_tvm_btn = 'class="btn-clear-module inline-flex items-center justify-center px-2.5 py-1 rounded-lg text-xs font-bold bg-red-700 hover:bg-red-800 border border-red-700 transition shadow-sm"'
    if old_tvm_btn in content:
        content = content.replace(old_tvm_btn, new_tvm_btn)
        print(f"Updated TVM btn classes in {filepath}")

    old_cflo_btn = 'class="btn-clear-module inline-flex items-center justify-center px-2.5 py-1 rounded-lg text-xs font-bold bg-red-700 hover:bg-red-800 text-white border border-red-700 transition shadow-sm"'
    new_cflo_btn = 'class="btn-clear-module inline-flex items-center justify-center px-2.5 py-1 rounded-lg text-xs font-bold bg-red-700 hover:bg-red-800 border border-red-700 transition shadow-sm"'
    if old_cflo_btn in content:
        content = content.replace(old_cflo_btn, new_cflo_btn)
        print(f"Updated CFLO btn classes in {filepath}")

    # Ensure CRLF
    content = content.replace('\r\n', '\n').replace('\n', '\r\n')

    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        f.write(content)

update_file("Calculadora Financeira 17bIi.html")
update_file("index.html")

# Check hashes
h1 = hashlib.sha256(open("Calculadora Financeira 17bIi.html", "rb").read()).hexdigest()
h2 = hashlib.sha256(open("index.html", "rb").read()).hexdigest()
print(f"SHA-256 Calculadora Financeira 17bIi.html: {h1}")
print(f"SHA-256 index.html:                       {h2}")
assert h1 == h2, "Hashes do not match!"
print("PARITY VERIFIED: Both files are 100% byte-for-byte identical!")

