# -*- coding: utf-8 -*-
"""
apply_haptic_toggle.py
Applies dedicated haptic feedback toggle switch visible exclusively in mobile mode.
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
    # 1. Update CSS around .sound-toggle
    old_css = """        /* Alternância de som e feedback tátil das teclas no celular (toggle switch ao lado do tema) */
        .sound-toggle {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 5px;
            min-width: 88px;
            min-height: 40px;
            padding: 6px 8px;
            border: 1px solid #475569;
            border-radius: 999px;
            background: rgba(30, 41, 59, 0.92);
            cursor: pointer;
            transition: background-color .18s ease, border-color .18s ease, box-shadow .18s ease;
            touch-action: manipulation;
        }
        .sound-icon {
            width: 16px;
            height: 16px;
            flex: 0 0 16px;
            transition: color .18s ease, opacity .18s ease, transform .18s ease;
        }
        .sound-icon-off { color: #64748b; }
        .sound-icon-on { color: #fbbf24; }
        .sound-switch-track {
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
        .sound-switch-knob {
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

        /* Modo CLARO (body.light-mode) */
        body.light-mode .sound-toggle {
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

        body.light-mode .sound-toggle[aria-checked="false"] .sound-switch-track {
            background: #e2e8f0;
            border-color: #cbd5e1;
        }
        body.light-mode .sound-toggle[aria-checked="false"] .sound-switch-knob {
            transform: translateX(0);
            background: #cbd5e1;
        }
        body.light-mode .sound-toggle[aria-checked="false"] .sound-icon-on { color: #cbd5e1; }
        body.light-mode .sound-toggle[aria-checked="false"] .sound-icon-off { color: #dc2626; }

        .sound-toggle:hover {
            border-color: #64748b;
        }
        body.light-mode .sound-toggle:hover {
            border-color: #94a3b8;
        }
        .sound-toggle:focus-visible {
            outline: 3px solid #fbbf24;
            outline-offset: 3px;
        }"""

    new_css = """        /* Alternância de som e feedback tátil das teclas (toggle switches ao lado do tema) */
        .sound-toggle,
        .haptic-toggle {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 5px;
            min-width: 88px;
            min-height: 40px;
            padding: 6px 8px;
            border: 1px solid #475569;
            border-radius: 999px;
            background: rgba(30, 41, 59, 0.92);
            cursor: pointer;
            transition: background-color .18s ease, border-color .18s ease, box-shadow .18s ease;
            touch-action: manipulation;
        }

        /* O toggle de feedback tátil é exibido exclusivamente no modo celular */
        @media (min-width: 1024px) {
            .haptic-toggle {
                display: none !important;
            }
            body.is-mobile-device .haptic-toggle {
                display: inline-flex !important;
            }
        }

        .sound-icon,
        .haptic-icon {
            width: 16px;
            height: 16px;
            flex: 0 0 16px;
            transition: color .18s ease, opacity .18s ease, transform .18s ease;
        }
        .sound-icon-off,
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

    if old_css not in content:
        raise ValueError("Could not find old_css block")
    content = content.replace(old_css, new_css, 1)

    # 2. Update media queries in style for 540px and 380px
    old_mq = """.theme-toggle, .sound-toggle { min-width: 72px; min-height: 36px; gap: 4px; padding: 4px 6px; }
            .theme-icon, .sound-icon { width: 14px; height: 14px; flex-basis: 14px; }
            .theme-switch-track, .sound-switch-track { width: 36px; flex-basis: 36px; height: 22px; }
            .theme-switch-knob, .sound-switch-knob { width: 14px; height: 14px; flex-basis: 14px; }
            body.light-mode .theme-switch-knob { transform: translateX(16px); }
            .sound-toggle[aria-checked="true"] .sound-switch-knob { transform: translateX(16px); }
            body.light-mode .sound-toggle[aria-checked="true"] .sound-switch-knob { transform: translateX(16px); }
        }
        @media (max-width: 380px) {
            .header-theme { gap: 0.25rem; }
            .theme-toggle, .sound-toggle { min-width: 64px; padding: 3px 4px; gap: 3px; }
            .theme-switch-track, .sound-switch-track { width: 30px; flex-basis: 30px; height: 20px; }
            .theme-switch-knob, .sound-switch-knob { width: 12px; height: 12px; flex-basis: 12px; }
            body.light-mode .theme-switch-knob { transform: translateX(12px); }
            .sound-toggle[aria-checked="true"] .sound-switch-knob { transform: translateX(12px); }
            body.light-mode .sound-toggle[aria-checked="true"] .sound-switch-knob { transform: translateX(12px); }"""

    new_mq = """.theme-toggle, .sound-toggle, .haptic-toggle { min-width: 72px; min-height: 36px; gap: 4px; padding: 4px 6px; }
            .theme-icon, .sound-icon, .haptic-icon { width: 14px; height: 14px; flex-basis: 14px; }
            .theme-switch-track, .sound-switch-track, .haptic-switch-track { width: 36px; flex-basis: 36px; height: 22px; }
            .theme-switch-knob, .sound-switch-knob, .haptic-switch-knob { width: 14px; height: 14px; flex-basis: 14px; }
            body.light-mode .theme-switch-knob { transform: translateX(16px); }
            .sound-toggle[aria-checked="true"] .sound-switch-knob,
            .haptic-toggle[aria-checked="true"] .haptic-switch-knob { transform: translateX(16px); }
            body.light-mode .sound-toggle[aria-checked="true"] .sound-switch-knob,
            body.light-mode .haptic-toggle[aria-checked="true"] .haptic-switch-knob { transform: translateX(16px); }
        }
        @media (max-width: 380px) {
            .header-theme { gap: 0.25rem; }
            .theme-toggle, .sound-toggle, .haptic-toggle { min-width: 60px; padding: 3px 4px; gap: 3px; }
            .theme-switch-track, .sound-switch-track, .haptic-switch-track { width: 30px; flex-basis: 30px; height: 20px; }
            .theme-switch-knob, .sound-switch-knob, .haptic-switch-knob { width: 12px; height: 12px; flex-basis: 12px; }
            body.light-mode .theme-switch-knob { transform: translateX(12px); }
            .sound-toggle[aria-checked="true"] .sound-switch-knob,
            .haptic-toggle[aria-checked="true"] .haptic-switch-knob { transform: translateX(12px); }
            body.light-mode .sound-toggle[aria-checked="true"] .sound-switch-knob,
            body.light-mode .haptic-toggle[aria-checked="true"] .haptic-switch-knob { transform: translateX(12px); }"""

    if old_mq not in content:
        raise ValueError("Could not find old_mq block")
    content = content.replace(old_mq, new_mq, 1)

    # 3. Update HTML in header
    old_html_sound = """            <!-- Controles de Som (celular) e Alternância de Tema Claro/Escuro -->
            <div class="header-theme shrink-0 flex items-center gap-1.5 sm:gap-2">
                <!-- Botão Toggle Switch de Som das Teclas e Feedback Tátil -->
                <button id="sound-toggle" type="button" role="switch" aria-checked="true"
                    aria-label="Som e clique das teclas: ativado" title="Som e clique das teclas (Ativado)"
                    onclick="app.toggleMobileFeedback()" class="sound-toggle" aria-describedby="sound-toggle-description">
                    <svg class="sound-icon sound-icon-off" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                        <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                        <line x1="23" y1="9" x2="17" y2="15"></line>
                        <line x1="17" y1="9" x2="23" y2="15"></line>
                    </svg>
                    <span id="sound-switch-track" class="sound-switch-track" aria-hidden="true">
                        <span id="sound-switch-knob" class="sound-switch-knob"></span>
                    </span>
                    <svg class="sound-icon sound-icon-on" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                        <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                        <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
                        <path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path>
                    </svg>
                    <span id="sound-toggle-description" class="sr-only">Alto-falante mudo à esquerda e com som à direita. Liga e desliga o som mecânico e a vibração das teclas ao clicar ou digitar.</span>
                </button>

                <!-- Botão de Alternância de Tema Claro/Escuro -->"""

    new_html_sound = """            <!-- Controles de Som, Feedback Tátil (celular) e Alternância de Tema Claro/Escuro -->
            <div class="header-theme shrink-0 flex items-center gap-1.5 sm:gap-2">
                <!-- Botão Toggle Switch de Som das Teclas -->
                <button id="sound-toggle" type="button" role="switch" aria-checked="true"
                    aria-label="Som e clique das teclas: ativado" title="Som e clique das teclas (Ativado)"
                    onclick="app.toggleMobileFeedback()" class="sound-toggle" aria-describedby="sound-toggle-description">
                    <svg class="sound-icon sound-icon-off" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                        <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                        <line x1="23" y1="9" x2="17" y2="15"></line>
                        <line x1="17" y1="9" x2="23" y2="15"></line>
                    </svg>
                    <span id="sound-switch-track" class="sound-switch-track" aria-hidden="true">
                        <span id="sound-switch-knob" class="sound-switch-knob"></span>
                    </span>
                    <svg class="sound-icon sound-icon-on" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                        <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                        <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
                        <path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path>
                    </svg>
                    <span id="sound-toggle-description" class="sr-only">Alto-falante mudo à esquerda e com som à direita. Liga e desliga o som mecânico das teclas ao clicar ou digitar.</span>
                </button>

                <!-- Botão Toggle Switch de Feedback Tátil (apenas celular) -->
                <button id="haptic-toggle" type="button" role="switch" aria-checked="true"
                    aria-label="Feedback tátil (vibração): ativado" title="Feedback tátil / Vibração (Ativado)"
                    onclick="app.toggleHapticFeedback()" class="haptic-toggle" aria-describedby="haptic-toggle-description">
                    <svg class="haptic-icon haptic-icon-off" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                        <rect x="6" y="2" width="12" height="20" rx="2" ry="2"></rect>
                        <line x1="12" y1="18" x2="12.01" y2="18"></line>
                        <line x1="2" y1="2" x2="22" y2="22"></line>
                    </svg>
                    <span id="haptic-switch-track" class="haptic-switch-track" aria-hidden="true">
                        <span id="haptic-switch-knob" class="haptic-switch-knob"></span>
                    </span>
                    <svg class="haptic-icon haptic-icon-on" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                        <rect x="6" y="2" width="12" height="20" rx="2" ry="2"></rect>
                        <line x1="12" y1="18" x2="12.01" y2="18"></line>
                        <path d="M2 8a12 12 0 0 0 0 8"></path>
                        <path d="M22 8a12 12 0 0 1 0 8"></path>
                    </svg>
                    <span id="haptic-toggle-description" class="sr-only">Celular sem vibração à esquerda e com ondas de vibração à direita. Liga e desliga a vibração tátil das teclas no celular.</span>
                </button>

                <!-- Botão de Alternância de Tema Claro/Escuro -->"""

    if old_html_sound not in content:
        raise ValueError("Could not find old_html_sound block")
    content = content.replace(old_html_sound, new_html_sound, 1)

    # 4. Update JS app state declaration:
    old_state = """            // Feedback Tátil e Sonoro (apenas em modo celular)
            audioCtx: null,
            mobileFeedbackEnabled: true,
            _lastFeedbackTime: 0,"""

    new_state = """            // Feedback Tátil e Sonoro
            audioCtx: null,
            mobileFeedbackEnabled: true,
            hapticFeedbackEnabled: true,
            _lastFeedbackTime: 0,"""

    if old_state not in content:
        raise ValueError("Could not find old_state block")
    content = content.replace(old_state, new_state, 1)

    # 5. Update JS feedback methods:
    old_methods = """            // Emite feedback tátil (vibração háptica) exclusivamente em celulares compatíveis quando um botão é acionado
            triggerHaptic() {
                if (typeof navigator !== 'undefined' && typeof navigator.vibrate === 'function') {
                    try {
                        navigator.vibrate(18); // 18ms para simular switch mecânico
                    } catch (e) {
                        // Silencioso se bloqueado por permissão
                    }
                }
            },

            // Disparo de áudio (desktop e celular) e feedback tátil (apenas celular) EXCLUSIVAMENTE quando o botão é clicado/digitado
            triggerKeyFeedback() {
                if (!this.mobileFeedbackEnabled) return;
                this.playKeyClick();
                if (this.isMobileMode()) {
                    this.triggerHaptic();
                }
            },

            // Inicialização do feedback de áudio/tátil e desbloqueio pró-ativo de áudio
            initMobileFeedback() {
                try {
                    const saved = localStorage.getItem('calcfin_mobile_feedback');
                    if (saved !== null) {
                        this.mobileFeedbackEnabled = (saved === 'true');
                    }
                } catch (e) {}

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

            // Alternância manual de som (desktop e celular) e vibração (celular)
            toggleMobileFeedback() {
                this.mobileFeedbackEnabled = !this.mobileFeedbackEnabled;
                try {
                    localStorage.setItem('calcfin_mobile_feedback', this.mobileFeedbackEnabled ? 'true' : 'false');
                } catch (e) {}
                this.updateFeedbackToggleUI();

                const isMob = this.isMobileMode();
                const status = this.mobileFeedbackEnabled ? 'ON' : 'OFF';
                document.getElementById('lcdLine1').textContent = isMob ? `Som/Tátil: ${status}` : `Som: ${status}`;
                if (this.mobileFeedbackEnabled) {
                    this.playKeyClick();
                    if (isMob) {
                        this.triggerHaptic();
                    }
                }
                this.updateLCD();
            },

            // Atualização visual do toggle switch de som das teclas
            updateFeedbackToggleUI() {
                const btn = document.getElementById('sound-toggle');
                if (btn) {
                    const active = !!this.mobileFeedbackEnabled;
                    btn.setAttribute('aria-checked', active ? 'true' : 'false');
                    btn.setAttribute('aria-label', active ? 'Som e clique das teclas: ativado' : 'Som e clique das teclas: desativado');
                    btn.title = active ? 'Som e clique das teclas (Ativado)' : 'Som e clique das teclas (Desativado)';
                }

                // Compatibilidade caso algum elemento legado ainda esteja no DOM
                const legacyBtn = document.getElementById('mobile-feedback-toggle-btn');
                if (legacyBtn) {
                    const active = !!this.mobileFeedbackEnabled;
                    legacyBtn.setAttribute('aria-pressed', active ? 'true' : 'false');
                    const icon = document.getElementById('mobile-feedback-icon');
                    const label = document.getElementById('mobile-feedback-label');
                    if (icon) icon.textContent = active ? '🔔' : '🔕';
                    if (label) label.textContent = active ? 'Som' : 'Mudo';
                }
            },"""

    new_methods = """            // Emite feedback tátil (vibração háptica) exclusivamente quando habilitado e em dispositivos compatíveis
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
            },

            // Atualização visual dos toggle switches de som das teclas e feedback tátil
            updateFeedbackToggleUI() {
                const btnSound = document.getElementById('sound-toggle');
                if (btnSound) {
                    const active = !!this.mobileFeedbackEnabled;
                    btnSound.setAttribute('aria-checked', active ? 'true' : 'false');
                    btnSound.setAttribute('aria-label', active ? 'Som e clique das teclas: ativado' : 'Som e clique das teclas: desativado');
                    btnSound.title = active ? 'Som e clique das teclas (Ativado)' : 'Som e clique das teclas (Desativado)';
                }

                const btnHaptic = document.getElementById('haptic-toggle');
                if (btnHaptic) {
                    const activeHaptic = !!this.hapticFeedbackEnabled;
                    btnHaptic.setAttribute('aria-checked', activeHaptic ? 'true' : 'false');
                    btnHaptic.setAttribute('aria-label', activeHaptic ? 'Feedback tátil (vibração): ativado' : 'Feedback tátil (vibração): desativado');
                    btnHaptic.title = activeHaptic ? 'Feedback tátil / Vibração (Ativado)' : 'Feedback tátil / Vibração (Desativado)';
                }

                // Compatibilidade caso algum elemento legado ainda esteja no DOM
                const legacyBtn = document.getElementById('mobile-feedback-toggle-btn');
                if (legacyBtn) {
                    const active = !!this.mobileFeedbackEnabled;
                    legacyBtn.setAttribute('aria-pressed', active ? 'true' : 'false');
                    const icon = document.getElementById('mobile-feedback-icon');
                    const label = document.getElementById('mobile-feedback-label');
                    if (icon) icon.textContent = active ? '🔔' : '🔕';
                    if (label) label.textContent = active ? 'Som' : 'Mudo';
                }
            },"""

    if old_methods not in content:
        raise ValueError("Could not find old_methods block")
    content = content.replace(old_methods, new_methods, 1)

    return content

def main():
    files = ['Calculadora Financeira 17bIi.html', 'index.html']
    for fn in files:
        with open(fn, 'rb') as f:
            raw = f.read()
        # Decode CRLF
        text = raw.decode('utf-8')
        # Normalize newlines to \n for replacement
        has_crlf = '\r\n' in text
        text_lf = text.replace('\r\n', '\n')
        transformed = transform_content(text_lf)
        # Re-encode as CRLF
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
