# -*- coding: utf-8 -*-
import hashlib

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- CSS: Estilos do botão de exclusão e badge de fórmula personalizada ---
    old_css_star = """        body.light-mode .favorite-star-btn:not(.is-fav):hover {
            color: #d97706 !important;
        }"""

    new_css_star = """        body.light-mode .favorite-star-btn:not(.is-fav):hover {
            color: #d97706 !important;
        }

        /* Botão de Excluir Fórmula Personalizada */
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
        }

        /* Badge de Fórmula Personalizada */
        .custom-formula-badge {
            background-color: rgba(14, 165, 233, 0.18);
            border: 1px solid rgba(14, 165, 233, 0.4);
            color: #38bdf8;
        }
        body.light-mode .custom-formula-badge {
            background-color: rgba(14, 165, 233, 0.12);
            border-color: rgba(14, 165, 233, 0.5);
            color: #0284c7;
        }"""

    assert old_css_star in content, f"old_css_star not found in {filepath}"
    content = content.replace(old_css_star, new_css_star)
    print(f"Added custom formula CSS in {filepath}")

    # --- TAREFA 1: Remover botões redundantes Limpar TVM e Limpar CFLO ---
    tvm_header_old = """                                    <div class="flex items-center gap-2">
                                        <button type="button" onclick="app.clearTvmModule()" title="Limpar todos os campos de TVM e amortização" class="btn-clear-module inline-flex items-center justify-center px-2.5 py-1 rounded-lg text-xs font-bold bg-red-700 hover:bg-red-800 border border-red-700 transition shadow-sm">Limpar TVM</button>
                                        <span class="text-xs text-slate-400 font-mono hidden sm:inline">Softkeys F1–F5</span>
                                    </div>"""

    tvm_header_new = """                                    <div class="flex items-center gap-2">
                                        <span class="text-xs text-slate-400 font-mono hidden sm:inline">Softkeys F1–F5</span>
                                    </div>"""

    assert tvm_header_old in content, f"tvm_header_old not found in {filepath}"
    content = content.replace(tvm_header_old, tvm_header_new)
    print(f"Removed redundant Limpar TVM button from {filepath}")

    cflo_header_old = """                                    <div class="flex items-center gap-2">
                                        <button type="button" onclick="app.clearCfloModule()" title="Limpar taxa de desconto, fluxos e resultados de CFLO" class="btn-clear-module inline-flex items-center justify-center px-2.5 py-1 rounded-lg text-xs font-bold bg-red-700 hover:bg-red-800 border border-red-700 transition shadow-sm">Limpar CFLO</button>
                                        <span class="text-xs text-slate-400 font-mono hidden sm:inline">Análise de investimento</span>
                                    </div>"""

    cflo_header_new = """                                    <div class="flex items-center gap-2">
                                        <span class="text-xs text-slate-400 font-mono hidden sm:inline">Análise de investimento</span>
                                    </div>"""

    assert cflo_header_old in content, f"cflo_header_old not found in {filepath}"
    content = content.replace(cflo_header_old, cflo_header_new)
    print(f"Removed redundant Limpar CFLO button from {filepath}")

    # --- TAREFAS 2 & 3: Métodos de fórmulas personalizadas, categoria e exclusão ---
    # 1. Update createCustomFormula to set category 'Personalizadas', isCustom: true, call saveCustomFormulas
    old_create_custom = """            createCustomFormula(eqStr) {
                const vars = this.extractVariablesFromEquation(eqStr);
                if (!vars || vars.length === 0) {
                    this.setError('Nenhuma variável válida');
                    return false;
                }
                const id = 'custom_' + Date.now();
                const title = eqStr.split('=')[0].trim() || 'Equação Custom';
                const compiled = this.compileEquation(eqStr, vars);

                const newForm = {
                    id,
                    title,
                    category: 'Personalizadas (ALPHA)',
                    equation: eqStr,
                    vars,
                    evalResidual: compiled
                };

                this.formulas.push(newForm);
                this.selectFormula(id);
                return true;
            },"""

    new_create_custom = """            createCustomFormula(eqStr) {
                const vars = this.extractVariablesFromEquation(eqStr);
                if (!vars || vars.length === 0) {
                    this.setError('Nenhuma variável válida');
                    return false;
                }
                const id = 'custom_' + Date.now();
                const title = eqStr.split('=')[0].trim() || 'Equação Custom';
                const compiled = this.compileEquation(eqStr, vars);

                const newForm = {
                    id,
                    title,
                    category: 'Personalizadas',
                    equation: eqStr,
                    vars,
                    isCustom: true,
                    evalResidual: compiled
                };

                this.formulas.push(newForm);
                this.saveCustomFormulas();
                this.selectFormula(id);
                this.renderCatalog();
                this.filterCatalog();
                return true;
            },

            saveCustomFormulas() {
                try {
                    const customList = this.formulas
                        .filter(f => f.isCustom || (f.id && f.id.startsWith('custom_')) || f.category === 'Personalizadas')
                        .map(f => ({
                            id: f.id,
                            title: f.title,
                            category: 'Personalizadas',
                            equation: f.equation,
                            vars: f.vars,
                            desc: f.desc || '',
                            isCustom: true
                        }));
                    localStorage.setItem('hp17bii-custom-formulas', JSON.stringify(customList));
                } catch (_) {}
            },

            loadCustomFormulas() {
                try {
                    const raw = localStorage.getItem('hp17bii-custom-formulas');
                    if (!raw) return;
                    const list = JSON.parse(raw);
                    if (!Array.isArray(list)) return;
                    list.forEach(item => {
                        if (!item.id || !item.equation || this.formulas.some(f => f.id === item.id)) return;
                        const vars = item.vars || this.extractVariablesFromEquation(item.equation);
                        const compiled = this.compileEquation(item.equation, vars);
                        this.formulas.push({
                            id: item.id,
                            title: item.title || item.equation.split('=')[0].trim() || 'Equação Custom',
                            category: 'Personalizadas',
                            equation: item.equation,
                            vars,
                            desc: item.desc || '',
                            isCustom: true,
                            evalResidual: compiled
                        });
                    });
                } catch (_) {}
            },

            deleteCustomFormula(id) {
                const form = this.formulas.find(f => f.id === id);
                if (!form || (!form.isCustom && !form.id.startsWith('custom_') && form.category !== 'Personalizadas')) {
                    this.setError('Apenas fórmulas personalizadas podem ser excluídas');
                    return;
                }

                const confirmed = window.confirm(`Deseja realmente excluir a fórmula personalizada "${form.title}"?`);
                if (!confirmed) return;

                // Remover da lista de fórmulas
                this.formulas = this.formulas.filter(f => f.id !== id);

                // Remover dos favoritos caso esteja favoritada
                if (this.favoriteFormulas && this.favoriteFormulas.has(id)) {
                    this.favoriteFormulas.delete(id);
                    this.saveFavoriteFormulas();
                }

                // Persistir nova lista no localStorage
                this.saveCustomFormulas();

                // Se a fórmula excluída era a ativa, volta para a primeira nativa
                if (this.solve && this.solve.activeFormulaId === id) {
                    const fallback = this.formulas[0] ? this.formulas[0].id : 'coef_financiamento_carencia_premio';
                    this.selectFormula(fallback);
                } else {
                    this.renderCatalog();
                    this.filterCatalog();
                }

                this.setModuleActionFeedback(`Fórmula "${form.title}" excluída com sucesso.`, 'info');
                this.updateLCD();
            },"""

    assert old_create_custom in content, f"old_create_custom not found in {filepath}"
    content = content.replace(old_create_custom, new_create_custom)
    print(f"Updated custom formula methods in {filepath}")

    # 2. Update init() to call loadCustomFormulas()
    old_init_load = """                this.initTheme();
                this.loadFavoriteFormulas();"""
    new_init_load = """                this.initTheme();
                this.loadCustomFormulas();
                this.loadFavoriteFormulas();"""
    assert old_init_load in content, f"old_init_load not found in {filepath}"
    content = content.replace(old_init_load, new_init_load)
    print(f"Updated init() to load custom formulas in {filepath}")

    # 3. Update renderCatalog(): category select always includes 'Personalizadas'
    old_cat_populate = """                // Popula as categorias uma única vez, mantendo a escolha do usuário nos rerenders.
                if (categorySelect && categorySelect.options.length <= 1) {
                    const categories = [...new Set(this.formulas.map(f => f.category))]
                        .sort((a, b) => a.localeCompare(b, 'pt-BR'));
                    categories.forEach(category => {
                        const option = document.createElement('option');
                        option.value = category;
                        option.textContent = category;
                        categorySelect.appendChild(option);
                    });
                }"""

    new_cat_populate = """                // Popula as categorias mantendo a escolha do usuário nos rerenders.
                if (categorySelect) {
                    const currentVal = categorySelect.value;
                    const catSet = new Set(this.formulas.map(f => f.category));
                    catSet.add('Personalizadas');
                    const categories = [...catSet].sort((a, b) => a.localeCompare(b, 'pt-BR'));
                    categorySelect.innerHTML = '<option value="">Todas as categorias</option>';
                    categories.forEach(category => {
                        const option = document.createElement('option');
                        option.value = category;
                        option.textContent = category;
                        categorySelect.appendChild(option);
                    });
                    if (currentVal && (categories.includes(currentVal) || currentVal === 'Personalizadas')) {
                        categorySelect.value = currentVal;
                    }
                }"""

    assert old_cat_populate in content, f"old_cat_populate not found in {filepath}"
    content = content.replace(old_cat_populate, new_cat_populate)
    print(f"Updated category populate in {filepath}")

    # 4. Update formula card DOM in renderCatalog():
    old_card_dom = """                    item.addEventListener('click', (e) => {
                        if (e.target.closest('.favorite-star-btn')) return;
                        this.selectFormula(f.id);
                    });
                    item.addEventListener('keydown', (e) => {
                        if (e.target.closest('.favorite-star-btn')) return;
                        if (e.key === 'Enter' || e.key === ' ') {
                            e.preventDefault();
                            this.selectFormula(f.id);
                        }
                    });

                    const top = document.createElement('div');
                    top.className = 'flex items-center justify-between gap-2 mb-1.5';
                    
                    const leftTop = document.createElement('div');
                    leftTop.className = 'flex items-center gap-2 min-w-0';
                    const category = document.createElement('span');
                    category.className = 'text-[11px] font-mono font-bold leading-snug text-amber-400/95 truncate';
                    category.textContent = f.category;
                    const badge = document.createElement('span');
                    badge.className = isActive
                        ? 'shrink-0 rounded-md bg-amber-400 px-1.5 py-0.5 text-[9px] font-black tracking-wide text-slate-950'
                        : 'hidden';
                    badge.textContent = 'ATIVA';
                    leftTop.append(category, badge);

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

                    top.append(leftTop, starBtn);"""

    new_card_dom = """                    item.addEventListener('click', (e) => {
                        if (e.target.closest('.favorite-star-btn') || e.target.closest('.custom-formula-delete-btn')) return;
                        this.selectFormula(f.id);
                    });
                    item.addEventListener('keydown', (e) => {
                        if (e.target.closest('.favorite-star-btn') || e.target.closest('.custom-formula-delete-btn')) return;
                        if (e.key === 'Enter' || e.key === ' ') {
                            e.preventDefault();
                            this.selectFormula(f.id);
                        }
                    });

                    const top = document.createElement('div');
                    top.className = 'flex items-center justify-between gap-2 mb-1.5';
                    
                    const leftTop = document.createElement('div');
                    leftTop.className = 'flex items-center gap-1.5 min-w-0';
                    const category = document.createElement('span');
                    category.className = 'text-[11px] font-mono font-bold leading-snug text-amber-400/95 truncate';
                    category.textContent = f.category;

                    const badgesWrap = document.createElement('div');
                    badgesWrap.className = 'flex items-center gap-1 shrink-0';

                    const isCustomFormula = Boolean(f.isCustom || (f.id && f.id.startsWith('custom_')) || f.category === 'Personalizadas');
                    if (isCustomFormula) {
                        const customBadge = document.createElement('span');
                        customBadge.className = 'custom-formula-badge shrink-0 rounded-md px-1.5 py-0.5 text-[9px] font-bold tracking-wide';
                        customBadge.textContent = 'USUÁRIO';
                        badgesWrap.appendChild(customBadge);
                    }

                    const badge = document.createElement('span');
                    badge.className = isActive
                        ? 'shrink-0 rounded-md bg-amber-400 px-1.5 py-0.5 text-[9px] font-black tracking-wide text-slate-950'
                        : 'hidden';
                    badge.textContent = 'ATIVA';
                    badgesWrap.appendChild(badge);

                    leftTop.append(category, badgesWrap);

                    const actionsWrap = document.createElement('div');
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

    assert old_card_dom in content, f"old_card_dom not found in {filepath}"
    content = content.replace(old_card_dom, new_card_dom)
    print(f"Updated formula card DOM in {filepath}")

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

