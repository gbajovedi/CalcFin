# Calculadora Financeira HP 17bII+ Silver — PWA

🌐 **Acesse online:** [https://gbajovedi.github.io/CalcFin/](https://gbajovedi.github.io/CalcFin/)

Emulador completo da clássica calculadora financeira **HP 17bII+ Silver** desenvolvido para a web como um **Progressive Web App (PWA)** instalável no **Android**, **iOS** e **Windows/macOS**, com funcionamento **100% offline** e atualização automática.

---

## 🚀 Como Instalar no Celular

### No Android (Google Chrome)
1. Acesse o link do projeto no navegador.
2. Toque no menu de três pontos (`⋮`) no canto superior direito.
3. Selecione **"Instalar aplicativo"** (ou **"Adicionar à tela inicial"**).
4. O app será adicionado à sua tela inicial e à gaveta de aplicativos, abrindo em tela cheia sem barra de navegador.

### No iPhone / iPad (Safari)
1. Acesse o link do projeto pelo navegador **Safari**.
2. Toque no botão **Compartilhar** (ícone do quadrado com a seta para cima).
3. Role para baixo e selecione **"Adicionar à Tela de Início"**.
4. Toque em **Adicionar**. O ícone da HP 17bII+ aparecerá na sua tela de início como um app nativo.

---

## 💻 Como Instalar no Computador (PC / Mac)

### No Google Chrome (e Microsoft Edge / Brave)
Os navegadores baseados em Chromium oferecem suporte nativo à instalação de Progressive Web Apps no Windows, macOS e Linux:

1. Acesse o site no navegador: [https://gbajovedi.github.io/CalcFin/](https://gbajovedi.github.io/CalcFin/)
2. **Pela barra de endereços (Mais rápido):** No canto direito da barra de URLs (ao lado da estrela de favoritos), clique no ícone de instalação (computador com seta para baixo ou botão **"Instalar aplicativo"**).
3. **Ou pelo menu do Chrome:** Clique no menu de três pontos (`⋮`) no canto superior direito $\rightarrow$ **"Salvar e compartilhar"** (ou **"Transmitir, salvar e compartilhar"**) $\rightarrow$ **"Instalar Calculadora Financeira..."**.
4. Clique em **"Instalar"** na janela de confirmação.
5. O aplicativo abrirá imediatamente em uma **janela própria dedicada** (sem barra de URL do navegador) e você terá um ícone na sua **Área de Trabalho**, no **Menu Iniciar** e poderá fixá-lo na **Barra de Tarefas**.

### No Mozilla Firefox
O Firefox de desktop não possui o botão nativo de instalação de PWA na barra de endereços (recurso descontinuado pela Mozilla em navegadores para PC). Você pode criar um atalho de fácil acesso das seguintes maneiras:

#### Método 1: Atalho Direto na Área de Trabalho (Rápido e nativo)
1. Acesse o site no Firefox: [https://gbajovedi.github.io/CalcFin/](https://gbajovedi.github.io/CalcFin/)
2. Reduza ligeiramente a janela do Firefox para deixar a sua **Área de Trabalho** visível.
3. Clique e segure no ícone de **cadeado** 🔒 (à esquerda do endereço `https://...`) e **arraste-o** diretamente para a sua Área de Trabalho.
4. O atalho para a calculadora será criado instantaneamente.
   > **Dica para abrir em janela própria de app:** Clique com o botão direito no atalho criado $\rightarrow$ **Propriedades** $\rightarrow$ no campo **Destino**, adicione `-ssb` ou `--kiosk` (ex.: `"C:\...\firefox.exe" -ssb "https://gbajovedi.github.io/CalcFin/"`).

#### Método 2: Extensão PWA para Firefox (Experiência de App Independente)
1. Instale a extensão de código aberto **[PWAsForFirefox](https://github.com/filips123/PWAsForFirefox)** (Progressive Web Apps for Firefox).
2. Acesse a página da calculadora e clique no ícone de instalação gerado pela extensão na barra de ferramentas.
3. O app será executado em janela exclusiva e limpa, idêntico a um aplicativo nativo.

---

## ✨ Principais Funcionalidades

* **Modos RPN e Algébrico (ALG):** Pilha RPN completa (X, Y, Z, T e Last X) com comandos `ROLL`, `SWAP`, `LAST` e `DROP`.
* **Módulo TVM (Juros Compostos):** `N`, `I%YR`, `PV`, `PMT`, `FV`, `P/YR` e alternância entre início (`BGN`) e final de período (`END`).
* **Fluxo de Caixa Descontado (CFLO):** Cálculo de `VPL` (NPV), `TIR` (IRR), `NFV` e `PAYBACK` com agrupamento de frequências e edição rápida.
* **HP SOLVE & Catálogo Financeiro:** Mais de 20 fórmulas financeiras e comerciais integradas com pesquisa rápida e **sistema de favoritas persistente**.
* **Estatística Bi-variada (BUS/SUM):** Regressão linear, média ponderada e projeções financeiras.
* **Fita Contábil (Audit Tape):** Registro completo de operações com exportação e limpeza.
* **Visual e Usabilidade:** Modos Claro e Escuro com alto contraste WCAG AA, sons táteis opcionais e atalhos completos de teclado.
* **PWA Offline-First:** Funciona sem internet após o primeiro acesso com atualização automática a cada `git push`.
