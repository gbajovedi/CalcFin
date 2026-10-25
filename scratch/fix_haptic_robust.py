# -*- coding: utf-8 -*-
"""
fix_haptic_robust.py
Ensures haptic feedback is unconditionally triggered when enabled:
1. Removes any blocking conditions in triggerKeyFeedback (no dependence on isMobileMode).
2. Uses array pattern [duration] (40ms) with scalar fallback, which is optimal for Android.
3. Bulletproofs playHapticThump to handle suspended AudioContext asynchronously.
4. Adds diagnostic status to LCD on toggle so user can immediately see if hardware vibration was accepted, blocked by HTTPS/Android, or if running on iOS.
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
    old_methods = """            // Emite feedback tátil (vibração háptica em Android e pulso sub-grave para iOS/chassi)
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

    new_methods = """            // Emite feedback tátil (vibração háptica em Android e pulso sub-grave para iOS/chassi)
            triggerHaptic(duration = 40) {
                if (!this.hapticFeedbackEnabled) return false;
                let vibrated = false;
                // 1. Vibração de hardware nos dispositivos móveis compatíveis (Android)
                if (typeof navigator !== 'undefined' && typeof navigator.vibrate === 'function') {
                    try {
                        // Tenta array de pulso sólido (40ms-60ms) compatível com todas as marcas
                        vibrated = navigator.vibrate([duration]);
                        if (!vibrated) {
                            vibrated = navigator.vibrate(duration);
                        }
                    } catch (e) {
                        try { vibrated = navigator.vibrate(duration); } catch (err) {}
                    }
                }
                // 2. Pulso tátil acústico no chassi (resposta tátil real no diafragma do falante em iOS e desktop)
                this.playHapticThump();
                return vibrated;
            },

            // Emite pulso ultra-grave de curta duração que gera impacto tátil no falante do dispositivo
            playHapticThump() {
                try {
                    const AudioCtx = window.AudioContext || window.webkitAudioContext;
                    if (!AudioCtx) return;
                    if (!this.audioCtx) {
                        this.audioCtx = new AudioCtx();
                    }
                    const play = () => {
                        try {
                            const now = this.audioCtx.currentTime;
                            const osc = this.audioCtx.createOscillator();
                            const gain = this.audioCtx.createGain();
                            osc.type = 'sine';
                            // Onda senoidal de 70Hz a 35Hz (sub-graves puros em 25ms para impacto físico)
                            osc.frequency.setValueAtTime(70, now);
                            osc.frequency.exponentialRampToValueAtTime(35, now + 0.025);
                            gain.gain.setValueAtTime(0.4, now);
                            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.025);
                            osc.connect(gain);
                            gain.connect(this.audioCtx.destination);
                            osc.start(now);
                            osc.stop(now + 0.028);
                        } catch (e) {}
                    };

                    if (this.audioCtx.state === 'suspended') {
                        this.audioCtx.resume().then(play).catch(() => {});
                    } else {
                        play();
                    }
                } catch (e) {}
            },

            // Disparo de áudio e feedback tátil EXCLUSIVAMENTE quando o botão é clicado/digitado
            triggerKeyFeedback() {
                if (this.mobileFeedbackEnabled) {
                    this.playKeyClick();
                }
                if (this.hapticFeedbackEnabled) {
                    this.triggerHaptic(40);
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
                let diag = '';
                if (this.hapticFeedbackEnabled) {
                    const vibrated = this.triggerHaptic(50);
                    if (typeof navigator === 'undefined' || typeof navigator.vibrate !== 'function') {
                        diag = ' (Somente áudio - iOS sem vibração)';
                    } else if (vibrated === false) {
                        diag = ' (Verifique vibração do Android/HTTPS)';
                    }
                } else if (this.mobileFeedbackEnabled) {
                    this.playKeyClick();
                }
                const lcd1 = document.getElementById('lcdLine1');
                if (lcd1) lcd1.textContent = `Vibração: ${status}${diag}`;
                this.updateLCD();
            },"""

    if old_methods not in content:
        raise ValueError("Could not find old_methods in content")
    content = content.replace(old_methods, new_methods, 1)

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
