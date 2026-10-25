# -*- coding: utf-8 -*-
import hashlib

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update CSS
    old_css = """/* Botão de Excluir Fórmula Personalizada */
        .custom-formula-delete-btn {
            background: transparent;
            border: none;
            padding: 0.25rem 0.35rem;
            cursor: pointer;
            line-height: 1;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 0.375rem;
            transition: transform 0.15s ease, color 0.15s ease;
        }
        .custom-formula-delete-btn:hover {
            transform: scale(1.18);
        }
        body.light-mode .custom-formula-delete-btn {
            color: #94a3b8;
        }
        body.light-mode .custom-formula-delete-btn:hover {
            color: #e11d48 !important;
        }"""

    new_css = """/* Botão de Excluir Fórmula Personalizada */
        .custom-formula-delete-btn {
            background: transparent;
            border: none;
            padding: 0.25rem 0.35rem;
            cursor: pointer;
            line-height: 1;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 0.375rem;
            color: #f87171;
            transition: transform 0.15s ease, color 0.15s ease, background-color 0.15s ease;
        }
        .custom-formula-delete-btn svg {
            width: 17px;
            height: 17px;
            display: block;
            stroke: currentColor;
            fill: none;
        }
        .custom-formula-delete-btn:hover {
            color: #ef4444 !important;
            background-color: rgba(239, 68, 68, 0.15);
            transform: scale(1.18);
        }
        .custom-formula-delete-btn:focus-visible {
            outline: 2px solid #ef4444;
            outline-offset: 2px;
        }
        body.light-mode .custom-formula-delete-btn {
            color: #dc2626 !important;
        }
        body.light-mode .custom-formula-delete-btn:hover {
            color: #b91c1c !important;
            background-color: rgba(220, 38, 38, 0.12);
        }"""

    assert old_css in content, f"old_css not found in {filepath}"
    content = content.replace(old_css, new_css)
    print(f"Updated delete button CSS in {filepath}")

    # 2. Update JS (place delBtn to the left of starBtn, and ensure SVG has width/height)
    old_js = """                    const actionsWrap = document.createElement('div');
                    actionsWrap.className = 'flex items-center gap-1.5 shrink-0';

                    const starBtn = document.createElement('button');
                    starBtn.type = 'button';
                    starBtn.className = `favorite-star-btn p-1 -m-1 ${isFav ? 'is-fav text-amber-400' : 'text-slate-500 hover:text-amber-300'}`;
                    starBtn.setAttribute('aria-label', isFav ? `Remover ${f.title} dos favoritos` : `Favoritar ${f.title}`);
                    starBtn.setAttribute('title', isFav ? 'Remover dos favoritos' : 'Favoritar fórmula');
                    starBtn.innerHTML = `<span class="text-xl leading-none" aria-hidden="true">${isFav ? '★' : '☆'}</span>`;
                    starBtn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        e.preventDefault();
                        this.toggleFavorite(f.id, e);
                    });
                    actionsWrap.appendChild(starBtn);

                    if (isCustomFormula) {
                        const delBtn = document.createElement('button');
                        delBtn.type = 'button';
                        delBtn.className = 'custom-formula-delete-btn p-1 -m-1 text-slate-400 hover:text-rose-400 transition focus:outline-none focus:ring-1 focus:ring-rose-500 rounded';
                        delBtn.title = `Excluir fórmula personalizada "${f.title}"`;
                        delBtn.setAttribute('aria-label', `Excluir fórmula personalizada ${f.title}`);
                        delBtn.innerHTML = `<svg aria-hidden="true" class="w-3.5 h-3.5 pointer-events-none" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"></path><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>`;
                        delBtn.addEventListener('click', (e) => {
                            e.stopPropagation();
                            e.preventDefault();
                            this.deleteCustomFormula(f.id);
                        });
                        actionsWrap.appendChild(delBtn);
                    }

                    top.append(leftTop, actionsWrap);"""

    new_js = """                    const actionsWrap = document.createElement('div');
                    actionsWrap.className = 'flex items-center gap-1.5 shrink-0';

                    if (isCustomFormula) {
                        const delBtn = document.createElement('button');
                        delBtn.type = 'button';
                        delBtn.className = 'custom-formula-delete-btn p-1 -m-1 focus:outline-none focus:ring-1 focus:ring-rose-500 rounded';
                        delBtn.title = `Excluir fórmula personalizada "${f.title}"`;
                        delBtn.setAttribute('aria-label', `Excluir fórmula personalizada ${f.title}`);
                        delBtn.innerHTML = `<svg aria-hidden="true" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"></path><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>`;
                        delBtn.addEventListener('click', (e) => {
                            e.stopPropagation();
                            e.preventDefault();
                            this.deleteCustomFormula(f.id);
                        });
                        actionsWrap.appendChild(delBtn);
                    }

                    const starBtn = document.createElement('button');
                    starBtn.type = 'button';
                    starBtn.className = `favorite-star-btn p-1 -m-1 ${isFav ? 'is-fav text-amber-400' : 'text-slate-500 hover:text-amber-300'}`;
                    starBtn.setAttribute('aria-label', isFav ? `Remover ${f.title} dos favoritos` : `Favoritar ${f.title}`);
                    starBtn.setAttribute('title', isFav ? 'Remover dos favoritos' : 'Favoritar fórmula');
                    starBtn.innerHTML = `<span class="text-xl leading-none" aria-hidden="true">${isFav ? '★' : '☆'}</span>`;
                    starBtn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        e.preventDefault();
                        this.toggleFavorite(f.id, e);
                    });
                    actionsWrap.appendChild(starBtn);

                    top.append(leftTop, actionsWrap);"""

    assert old_js in content, f"old_js not found in {filepath}"
    content = content.replace(old_js, new_js)
    print(f"Updated JS in {filepath}")

    # Ensure CRLF line endings
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

