# -*- coding: utf-8 -*-

def fix(path):
    with open(path, 'rb') as f:
        c = f.read().decode('utf-8')
    t = """            copyAmortizationTable(btnEl) {
                if (!this._currentAmortSchedule || !this._currentAmortSchedule.length) {
                    this.setModuleActionFeedback('Gere a tabela de amortização antes de copiar.', 'error');
                    return;
                }
                const lines = [];
                lines.push(['# Per.', 'Pagamento', 'Juros', 'Principal', 'Saldo Devedor'].join('\\t'));
                this._currentAmortSchedule.forEach(r => {
                    lines.push([r.label, this.formatNum(r.pmt), this.formatNum(r.interest), this.formatNum(r.principal), this.formatNum(r.balance)].join('\\t'));
                });
                if (this._currentAmortTotals) {
                    const t = this._currentAmortTotals;
                    lines.push([`TOTAL (${t.count})`, this.formatNum(t.pmt), this.formatNum(t.interest), this.formatNum(t.principal), this.formatNum(t.balance)].join('\\t'));
                }
                const text = lines.join('\\r\\n');
                const onDone = () => {
                    if (btnEl) {
                        const orig = btnEl.innerHTML;
                        btnEl.innerHTML = '<span aria-hidden="true">✓</span> Copiado!';
                        setTimeout(() => { if (btnEl) btnEl.innerHTML = orig; }, 1500);
                    }
                    this.setModuleActionFeedback('Tabela de amortização copiada para a área de transferência (formato Excel / Planilhas).', 'success');
                };

                if (navigator.clipboard && navigator.clipboard.writeText) {
                    navigator.clipboard.writeText(text).then(onDone).catch(() => {
                        this.fallbackCopyText(text);
                        onDone();
                    });
                } else {
                    this.fallbackCopyText(text);
                    onDone();
                }
            },"""

    r = """            async copyAmortizationTable(btnEl) {
                if (!this._currentAmortSchedule || !this._currentAmortSchedule.length) {
                    this.setModuleActionFeedback('Gere a tabela de amortização antes de copiar.', 'error');
                    return;
                }
                const lines = [];
                lines.push(['# Per.', 'Pagamento', 'Juros', 'Principal', 'Saldo Devedor'].join('\\t'));
                this._currentAmortSchedule.forEach(r => {
                    lines.push([r.label, this.formatNum(r.pmt), this.formatNum(r.interest), this.formatNum(r.principal), this.formatNum(r.balance)].join('\\t'));
                });
                if (this._currentAmortTotals) {
                    const t = this._currentAmortTotals;
                    lines.push([`TOTAL (${t.count})`, this.formatNum(t.pmt), this.formatNum(t.interest), this.formatNum(t.principal), this.formatNum(t.balance)].join('\\t'));
                }
                const text = lines.join('\\r\\n');
                let copied = false;
                try {
                    if (navigator.clipboard && navigator.clipboard.writeText) {
                        await navigator.clipboard.writeText(text);
                        copied = true;
                    }
                } catch (_) {}
                if (!copied) {
                    this.fallbackCopyText(text);
                }
                if (btnEl) {
                    const orig = btnEl.innerHTML;
                    btnEl.innerHTML = '<span aria-hidden="true">✓</span> Copiado!';
                    setTimeout(() => { if (btnEl) btnEl.innerHTML = orig; }, 1500);
                }
                this.setModuleActionFeedback('Tabela de amortização copiada para a área de transferência (formato Excel / Planilhas).', 'success');
            },"""
    norm_c = c.replace('\r\n', '\n')
    norm_t = t.replace('\r\n', '\n')
    norm_r = r.replace('\r\n', '\n')
    if norm_t not in norm_c:
        print('Not found in', path)
        return
    norm_c = norm_c.replace(norm_t, norm_r, 1)
    with open(path, 'wb') as f:
        f.write(norm_c.replace('\n', '\r\n').encode('utf-8'))
    print('Updated', path)

fix('Calculadora Financeira 17bIi.html')
fix('index.html')

