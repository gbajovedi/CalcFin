# -*- coding: utf-8 -*-
"""
fix_haptic_amber.py
Updates the haptic toggle to use amber color (identical to sound/theme toggles)
and adds haptic thump fallback + robust mobile mode vibration.
Maintains exact byte-for-byte CRLF synchronization between both HTML files.
"""

import os
import hashlib

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def transform_content(content):
    # 1. Update CSS around .sound-toggle and .haptic-toggle
    old_css_block = """        .sound-icon-off,
        .haptic-icon-off { color: #64748b; }
        .sound-icon-on { color: #fbbf24; }
        .haptic-icon-on { color: #38bdf8; }

        .sound-switch-track,
        .haptic-switch-track {
            width: 42px;
            height: 26px;
            padding: 2px;
            display: flex;
            align-items: center;
            flex: 0 0 42px;
            border-radius: 999px;
            background: #334155;
            border: 1px solid #64748b;
            transition: background-color .18s ease, border-color .18s ease;
        }
        .sound-switch-knob,
        .haptic-switch-knob {
            width: 18px;
            height: 18px;
            flex: 0 0 18px;
            border-radius: 50%;
            display: block;
            background: #f8fafc;
            box-shadow: 0 1px 3px rgba(0,0,0,.24);
            transform: translateX(0);
            transition: transform .18s ease, background-color .18s ease, color .18s ease;
        }
        /* Som ATIVADO (aria-checked="true") no modo escuro */
        .sound-toggle[aria-checked="true"] .sound-switch-track {
            background: #b45309;
            border-color: #f59e0b;
        }
        .sound-toggle[aria-checked="true"] .sound-switch-knob {
            transform: translateX(18px);
            background: #fffaf0;
        }
        .sound-toggle[aria-checked="true"] .sound-icon-on { color: #fbbf24; }
        .sound-toggle[aria-checked="true"] .sound-icon-off { color: #64748b; }

        /* Haptic ATIVADO (aria-checked="true") no modo escuro */
        .haptic-toggle[aria-checked="true"] .haptic-switch-track {
            background: #0284c7;
            border-color: #38bdf8;
        }
        .haptic-toggle[aria-checked="true"] .haptic-switch-knob {
            transform: translateX(18px);
            background: #f0f9ff;
        }
        .haptic-toggle[aria-checked="true"] .haptic-icon-on { color: #38bdf8; }
        .haptic-toggle[aria-checked="true"] .haptic-icon-off { color: #64748b; }

        /* Som DESATIVADO (aria-checked="false") no modo escuro */
        .sound-toggle[aria-checked="false"] .sound-switch-track {
            background: #1e293b;
            border-color: #475569;
        }
        .sound-toggle[aria-checked="false"] .sound-switch-knob {
            transform: translateX(0);
            background: #94a3b8;
        }
        .sound-toggle[aria-checked="false"] .sound-icon-on { color: #475569; }
        .sound-toggle[aria-checked="false"] .sound-icon-off { color: #f87171; }

        /* Haptic DESATIVADO (aria-checked="false") no modo escuro */
        .haptic-toggle[aria-checked="false"] .haptic-switch-track {
            background: #1e293b;
            border-color: #475569;
        }
        .haptic-toggle[aria-checked="false"] .haptic-switch-knob {
            transform: translateX(0);
            background: #94a3b8;
        }
        .haptic-toggle[aria-checked="false"] .haptic-icon-on { color: #475569; }
        .haptic-toggle[aria-checked="false"] .haptic-icon-off { color: #f87171; }

        /* Modo CLARO (body.light-mode) */
        body.light-mode .sound-toggle,
        body.light-mode .haptic-toggle {
            background: #ffffff;
            border-color: #cbd5e1;
        }
        body.light-mode .sound-toggle[aria-checked="true"] .sound-switch-track {
            background: #b7791f;
            border-color: #9a5800;
        }
        body.light-mode .sound-toggle[aria-checked="true"] .sound-switch-knob {
            transform: translateX(18px);
            background: #fffaf0;
        }
        body.light-mode .sound-toggle[aria-checked="true"] .sound-icon-on { color: #b7791f; }
        body.light-mode .sound-toggle[aria-checked="true"] .sound-icon-off { color: #94a3b8; }

        body.light-mode .haptic-toggle[aria-checked="true"] .haptic-switch-track {
            background: #0284c7;
            border-color: #0369a1;
        }
        body.light-mode .haptic-toggle[aria-checked="true"] .haptic-switch-knob {
            transform: translateX(18px);
            background: #f0f9ff;
        }
        body.light-mode .haptic-toggle[aria-checked="true"] .haptic-icon-on { color: #0284c7; }
        body.light-mode .haptic-toggle[aria-checked="true"] .haptic-icon-off { color: #94a3b8; }

        body.light-mode .sound-toggle[aria-checked="false"] .sound-switch-track,
        body.light-mode .haptic-toggle[aria-checked="false"] .haptic-switch-track {
            background: #e2e8f0;
            border-color: #cbd5e1;
        }
        body.light-mode .sound-toggle[aria-checked="false"] .sound-switch-knob,
        body.light-mode .haptic-toggle[aria-checked="false"] .haptic-switch-knob {
            transform: translateX(0);
            background: #cbd5e1;
        }
        body.light-mode .sound-toggle[aria-checked="false"] .sound-icon-on { color: #cbd5e1; }
        body.light-mode .sound-toggle[aria-checked="false"] .sound-icon-off { color: #dc2626; }
        body.light-mode .haptic-toggle[aria-checked="false"] .haptic-icon-on { color: #cbd5e1; }
        body.light-mode .haptic-toggle[aria-checked="false"] .haptic-icon-off { color: #dc2626; }

        .sound-toggle:hover,
        .haptic-toggle:hover {
            border-color: #64748b;
        }
        body.light-mode .sound-toggle:hover,
        body.light-mode .haptic-toggle:hover {
            border-color: #94a3b8;
        }
        .sound-toggle:focus-visible {
            outline: 3px solid #fbbf24;
            outline-offset: 3px;
        }
        .haptic-toggle:focus-visible {
            outline: 3px solid #38bdf8;
            outline-offset: 3px;
        }"""

    new_css_block = """        .sound-icon-off,
        .haptic-icon-off { color: #64748b; }
        .sound-icon-on,
        .haptic-icon-on { color: #fbbf24; }

        .sound-switch-track,
        .haptic-switch-track {
            width: 42px;
            height: 26px;
            padding: 2px;
            display: flex;
            align-items: center;
            flex: 0 0 42px;
            border-radius: 999px;
            background: #334155;
            border: 1px solid #64748b;
            transition: background-color .18s ease, border-color .18s ease;
        }
        .sound-switch-knob,
        .haptic-switch-knob {
            width: 18px;
            height: 18px;
            flex: 0 0 18px;
            border-radius: 50%;
            display: block;
            background: #f8fafc;
            box-shadow: 0 1px 3px rgba(0,0,0,.24);
            transform: translateX(0);
            transition: transform .18s ease, background-color .18s ease, color .18s ease;
        }
        /* Som e Haptic ATIVADO (aria-checked="true") no modo escuro (Âmbar HP) */
        .sound-toggle[aria-checked="true"] .sound-switch-track,
        .haptic-toggle[aria-checked="true"] .haptic-switch-track {
            background: #b45309;
            border-color: #f59e0b;
        }
        .sound-toggle[aria-checked="true"] .sound-switch-knob,
        .haptic-toggle[aria-checked="true"] .haptic-switch-knob {
            transform: translateX(18px);
            background: #fffaf0;
        }
        .sound-toggle[aria-checked="true"] .sound-icon-on,
        .haptic-toggle[aria-checked="true"] .haptic-icon-on { color: #fbbf24; }
        .sound-toggle[aria-checked="true"] .sound-icon-off,
        .haptic-toggle[aria-checked="true"] .haptic-icon-off { color: #64748b; }

        /* Som e Haptic DESATIVADO (aria-checked="false") no modo escuro */
        .sound-toggle[aria-checked="false"] .sound-switch-track,
        .haptic-toggle[aria-checked="false"] .haptic-switch-track {
            background: #1e293b;
            border-color: #475569;
        }
        .sound-toggle[aria-checked="false"] .sound-switch-knob,
        .haptic-toggle[aria-checked="false"] .haptic-switch-knob {
            transform: translateX(0);
            background: #94a3b8;
        }
        .sound-toggle[aria-checked="false"] .sound-icon-on,
        .haptic-toggle[aria-checked="false"] .haptic-icon-on { color: #475569; }
        .sound-toggle[aria-checked="false"] .sound-icon-off,
        .haptic-toggle[aria-checked="false"] .haptic-icon-off { color: #f87171; }

        /* Modo CLARO (body.light-mode) - Âmbar Ocre Oficial */
        body.light-mode .sound-toggle,
        body.light-mode .haptic-toggle {
            background: #ffffff;
            border-color: #cbd5e1;
        }
        body.light-mode .sound-toggle[aria-checked="true"] .sound-switch-track,
        body.light-mode .haptic-toggle[aria-checked="true"] .haptic-switch-track {
            background: #b7791f;
            border-color: #9a5800;
        }
        body.light-mode .sound-toggle[aria-checked="true"] .sound-switch-knob,
        body.light-mode .haptic-toggle[aria-checked="true"] .haptic-switch-knob {
            transform: translateX(18px);
            background: #fffaf0;
        }
        body.light-mode .sound-toggle[aria-checked="true"] .sound-icon-on,
        body.light-mode .haptic-toggle[aria-checked="true"] .haptic-icon-on { color: #b7791f; }
        body.light-mode .sound-toggle[aria-checked="true"] .sound-icon-off,
        body.light-mode .haptic-toggle[aria-checked="true"] .haptic-icon-off { color: #94a3b8; }

        body.light-mode .sound-toggle[aria-checked="false"] .sound-switch-track,
        body.light-mode .haptic-toggle[aria-checked="false"] .haptic-switch-track {
            background: #e2e8f0;
            border-color: #cbd5e1;
        }
        body.light-mode .sound-toggle[aria-checked="false"] .sound-switch-knob,
        body.light-mode .haptic-toggle[aria-checked="false"] .haptic-switch-knob {
            transform: translateX(0);
            background: #cbd5e1;
        }
        body.light-mode .sound-toggle[aria-checked="false"] .sound-icon-on,
        body.light-mode .haptic-toggle[aria-checked="false"] .haptic-icon-on { color: #cbd5e1; }
        body.light-mode .sound-toggle[aria-checked="false"] .sound-icon-off,
        body.light-mode .haptic-toggle[aria-checked="false"] .haptic-icon-off { color: #dc2626; }

        .sound-toggle:hover,
        .haptic-toggle:hover {
            border-color: #64748b;
        }
        body.light-mode .sound-toggle:hover,
        body.light-mode .haptic-toggle:hover {
            border-color: #94a3b8;
        }
        .sound-toggle:focus-visible,
        .haptic-toggle:focus-visible {
            outline: 3px solid #fbbf24;
            outline-offset: 3px;
        }"""

    if old_css_block not in content:
        raise ValueError("Could not find old_css_block in content")
    content = content.replace(old_css_block, new_css_block, 1)

    # 2. Update isMobileMode to include window.innerWidth < 1024
    old_is_mobile = """            // Verifica se a sessão atual está em modo celular / dispositivo móvel
            isMobileMode() {
                const isMobileUA = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
                const hasTouch = (typeof window !== 'undefined') && (('ontouchstart' in window) || (navigator.maxTouchPoints > 0));
                const isNarrow = (typeof window !== 'undefined') && (window.innerWidth < 1024);
                const isCoarse = (typeof window !== 'undefined') && window.matchMedia && window.matchMedia('(pointer: coarse)').matches;
                return isMobileUA || (hasTouch && isNarrow) || (isCoarse && isNarrow);
            },"""

    new_is_mobile = """            // Verifica se a sessão atual está em modo celular / dispositivo móvel
            isMobileMode() {
                const isNarrow = (typeof window !== 'undefined') && (window.innerWidth < 1024);
                const isMobileUA = (typeof navigator !== 'undefined') && /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
                const hasTouch = (typeof window !== 'undefined') && (('ontouchstart' in window) || (navigator.maxTouchPoints > 0));
                const isCoarse = (typeof window !== 'undefined') && window.matchMedia && window.matchMedia('(pointer: coarse)').matches;
                return isNarrow || isMobileUA || (hasTouch && isNarrow) || (isCoarse && isNarrow);
            },"""

    if old_is_mobile not in content:
        raise ValueError("Could not find old_is_mobile in content")
    content = content.replace(old_is_mobile, new_is_mobile, 1)

    # 3. Update feedback methods: add playHapticThump, update triggerHaptic, triggerKeyFeedback, toggleHapticFeedback
    old_feedback_methods = """            // Emite feedback tátil (vibração háptica) exclusivamente quando habilitado e em dispositivos compatíveis
            triggerHaptic(duration = 18) {
                if (!this.hapticFeedbackEnabled) return;
                if (typeof navigator !== 'undefined' && typeof navigator.vibrate === 'function') {
                    try {
                        navigator.vibrate(duration); // Simula switch mecânico
                    } catch (e) {
                        // Silencioso se bloqueado por permissão
                    }
                }
            },

            // Disparo de áudio (desktop e celular) e feedback tátil (apenas celular) EXCLUSIVAMENTE quando o botão é clicado/digitado
            triggerKeyFeedback() {
                if (this.mobileFeedbackEnabled) {
                    this.playKeyClick();
                }
                if (this.hapticFeedbackEnabled && this.isMobileMode()) {
                    this.triggerHaptic();
                }
            },

            // Inicialização do feedback de áudio/tátil e desbloqueio pró-ativo de áudio
            initMobileFeedback() {
                try {
                    const savedSound = localStorage.getItem('calcfin_mobile_feedback');
                    if (savedSound !== null) {
                        this.mobileFeedbackEnabled = (savedSound === 'true');
                    }
                    const savedHaptic = localStorage.getItem('calcfin_haptic_feedback');
                    if (savedHaptic !== null) {
                        this.hapticFeedbackEnabled = (savedHaptic === 'true');
                    }
                } catch (e) {}

                if (this.isMobileMode()) {
                    document.body.classList.add('is-mobile-device');
                }

                // Desbloqueia o AudioContext na primeira interação do usuário (clique, toque ou tecla digitada)
                const unlockAudio = () => {
                    try {
                        const AudioCtx = window.AudioContext || window.webkitAudioContext;
                        if (!this.audioCtx && AudioCtx) {
                            this.audioCtx = new AudioCtx();
                        }
                        if (this.audioCtx && this.audioCtx.state === 'suspended') {
                            this.audioCtx.resume();
                        }
                    } catch (e) {}
                    window.removeEventListener('pointerdown', unlockAudio, true);
                    window.removeEventListener('keydown', unlockAudio, true);
                    window.removeEventListener('touchstart', unlockAudio, true);
                };
                window.addEventListener('pointerdown', unlockAudio, { capture: true, passive: true });
                window.addEventListener('keydown', unlockAudio, { capture: true, passive: true });
                window.addEventListener('touchstart', unlockAudio, { capture: true, passive: true });

                this.updateFeedbackToggleUI();
            },

            // Alternância manual de som das teclas (desktop e celular)
            toggleMobileFeedback() {
                this.mobileFeedbackEnabled = !this.mobileFeedbackEnabled;
                try {
                    localStorage.setItem('calcfin_mobile_feedback', this.mobileFeedbackEnabled ? 'true' : 'false');
                } catch (e) {}
                this.updateFeedbackToggleUI();

                const status = this.mobileFeedbackEnabled ? 'ON' : 'OFF';
                const lcd1 = document.getElementById('lcdLine1');
                if (lcd1) lcd1.textContent = `Som: ${status}`;
                if (this.mobileFeedbackEnabled) {
                    this.playKeyClick();
                }
                this.updateLCD();
            },

            // Alternância manual de feedback tátil / vibração (exibido exclusivamente no modo celular)
            toggleHapticFeedback() {
                this.hapticFeedbackEnabled = !this.hapticFeedbackEnabled;
                try {
                    localStorage.setItem('calcfin_haptic_feedback', this.hapticFeedbackEnabled ? 'true' : 'false');
                } catch (e) {}
                this.updateFeedbackToggleUI();

                const status = this.hapticFeedbackEnabled ? 'ON' : 'OFF';
                const lcd1 = document.getElementById('lcdLine1');
                if (lcd1) lcd1.textContent = `Vibração: ${status}`;
                if (this.hapticFeedbackEnabled) {
                    this.triggerHaptic(25);
                }
                this.updateLCD();
            },"""

    new_feedback_methods = """            // Emite feedback tátil (vibração háptica em Android e pulso sub-grave para iOS/chassi)
            triggerHaptic(duration = 35) {
                if (!this.hapticFeedbackEnabled) return;
                // 1. Vibração de hardware nos dispositivos móveis compatíveis (Android)
                if (typeof navigator !== 'undefined' && typeof navigator.vibrate === 'function') {
                    try {
                        navigator.vibrate(duration);
                    } catch (e) {
                        // Silencioso se bloqueado por permissão
                    }
                }
                // 2. Pulso tátil acústico no chassi (resposta tátil real no diafragma do falante em iOS e desktop)
                this.playHapticThump();
            },

            // Emite pulso ultra-grave de curta duração que gera impacto tátil no falante do dispositivo
            playHapticThump() {
                try {
                    const AudioCtx = window.AudioContext || window.webkitAudioContext;
                    if (!AudioCtx) return;
                    if (!this.audioCtx) {
                        this.audioCtx = new AudioCtx();
                    }
                    if (this.audioCtx.state === 'suspended') {
                        this.audioCtx.resume();
                    }
                    const now = this.audioCtx.currentTime;
                    const osc = this.audioCtx.createOscillator();
                    const gain = this.audioCtx.createGain();
                    osc.type = 'sine';
                    // Onda senoidal de 65Hz a 32Hz (sub-graves puros em 24ms para impacto físico)
                    osc.frequency.setValueAtTime(65, now);
                    osc.frequency.exponentialRampToValueAtTime(32, now + 0.024);
                    gain.gain.setValueAtTime(0.35, now);
                    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.024);
                    osc.connect(gain);
                    gain.connect(this.audioCtx.destination);
                    osc.start(now);
                    osc.stop(now + 0.026);
                } catch (e) {}
            },

            // Disparo de áudio (desktop e celular) e feedback tátil (apenas celular) EXCLUSIVAMENTE quando o botão é clicado/digitado
            triggerKeyFeedback() {
                if (this.mobileFeedbackEnabled) {
                    this.playKeyClick();
                }
                if (this.hapticFeedbackEnabled && this.isMobileMode()) {
                    this.triggerHaptic(35);
                }
            },

            // Inicialização do feedback de áudio/tátil e desbloqueio pró-ativo de áudio
            initMobileFeedback() {
                try {
                    const savedSound = localStorage.getItem('calcfin_mobile_feedback');
                    if (savedSound !== null) {
                        this.mobileFeedbackEnabled = (savedSound === 'true');
                    }
                    const savedHaptic = localStorage.getItem('calcfin_haptic_feedback');
                    if (savedHaptic !== null) {
                        this.hapticFeedbackEnabled = (savedHaptic === 'true');
                    }
                } catch (e) {}

                if (this.isMobileMode()) {
                    document.body.classList.add('is-mobile-device');
                }

                // Desbloqueia o AudioContext na primeira interação do usuário (clique, toque ou tecla digitada)
                const unlockAudio = () => {
                    try {
                        const AudioCtx = window.AudioContext || window.webkitAudioContext;
                        if (!this.audioCtx && AudioCtx) {
                            this.audioCtx = new AudioCtx();
                        }
                        if (this.audioCtx && this.audioCtx.state === 'suspended') {
                            this.audioCtx.resume();
                        }
                    } catch (e) {}
                    window.removeEventListener('pointerdown', unlockAudio, true);
                    window.removeEventListener('keydown', unlockAudio, true);
                    window.removeEventListener('touchstart', unlockAudio, true);
                };
                window.addEventListener('pointerdown', unlockAudio, { capture: true, passive: true });
                window.addEventListener('keydown', unlockAudio, { capture: true, passive: true });
                window.addEventListener('touchstart', unlockAudio, { capture: true, passive: true });

                this.updateFeedbackToggleUI();
            },

            // Alternância manual de som das teclas (desktop e celular)
            toggleMobileFeedback() {
                this.mobileFeedbackEnabled = !this.mobileFeedbackEnabled;
                try {
                    localStorage.setItem('calcfin_mobile_feedback', this.mobileFeedbackEnabled ? 'true' : 'false');
                } catch (e) {}
                this.updateFeedbackToggleUI();

                const status = this.mobileFeedbackEnabled ? 'ON' : 'OFF';
                const lcd1 = document.getElementById('lcdLine1');
                if (lcd1) lcd1.textContent = `Som: ${status}`;
                if (this.mobileFeedbackEnabled) {
                    this.playKeyClick();
                }
                this.updateLCD();
            },

            // Alternância manual de feedback tátil / vibração (exibido exclusivamente no modo celular)
            toggleHapticFeedback() {
                this.hapticFeedbackEnabled = !this.hapticFeedbackEnabled;
                try {
                    localStorage.setItem('calcfin_haptic_feedback', this.hapticFeedbackEnabled ? 'true' : 'false');
                } catch (e) {}
                this.updateFeedbackToggleUI();

                const status = this.hapticFeedbackEnabled ? 'ON' : 'OFF';
                const lcd1 = document.getElementById('lcdLine1');
                if (lcd1) lcd1.textContent = `Vibração: ${status}`;
                if (this.hapticFeedbackEnabled) {
                    this.triggerHaptic(50);
                } else if (this.mobileFeedbackEnabled) {
                    this.playKeyClick();
                }
                this.updateLCD();
            },"""

    if old_feedback_methods not in content:
        raise ValueError("Could not find old_feedback_methods in content")
    content = content.replace(old_feedback_methods, new_feedback_methods, 1)

    return content

def main():
    files = ['Calculadora Financeira 17bIi.html', 'index.html']
    for fn in files:
        with open(fn, 'rb') as f:
            raw = f.read()
        text = raw.decode('utf-8')
        text_lf = text.replace('\r\n', '\n')
        transformed = transform_content(text_lf)
        transformed_crlf = transformed.replace('\n', '\r\n')
        with open(fn, 'wb') as f:
            f.write(transformed_crlf.encode('utf-8'))
        print(f"Updated {fn}")

    hash1 = sha256_file('Calculadora Financeira 17bIi.html')
    hash2 = sha256_file('index.html')
    print(f"Calculadora Financeira 17bIi.html SHA256: {hash1}")
    print(f"index.html SHA256:                        {hash2}")
    if hash1 == hash2:
        print("PERFEITO: Os dois arquivos estao 100% IDENTICOS!")
    else:
        print("ERRO: Divergencia nos hashes!")

if __name__ == '__main__':
    main()
