# 🛡️ Antigravity Telemetry System (v5.2 Pro Max)

Este é o sistema central de telemetria e observabilidade desenvolvido para permitir que o Agente IA (Antigravity) tenha "supervisão total" sobre a interface, performance e rede de qualquer aplicação.

## 🚀 Como Instalar em um Novo Projeto

Para implementar este sistema em qualquer projeto PHP/HTML, siga estes 3 passos:

### 1. Copiar a Pasta
Copie a pasta inteira `13_ANTIGRAVITY_TELEMETRY` para o diretório raiz do seu novo projeto.

### 2. Incluir os Scripts no Header
Adicione as seguintes linhas dentro da tag `<head>` do seu arquivo principal (ex: `header.php` ou `index.php`):

```html
<!-- ANTIGRAVITY TELEMETRY & SENTRY BRIDGE -->
<script src="13_ANTIGRAVITY_TELEMETRY/frontend/tracker.js"></script>
<script src="13_ANTIGRAVITY_TELEMETRY/SENTRY/sentry-client.js"></script>
```

### 3. Verificar Permissões
Certifique-se de que o servidor PHP tem permissão de escrita na pasta `13_ANTIGRAVITY_TELEMETRY/backend/logs/`, pois é lá que os relatórios serão salvos.

---

## 🛠️ O que está incluído na v5.2 Pro Max?

Ao instalar este módulo, o sistema passa a monitorar automaticamente:

*   **Self-Audit Engine (UI/UX):** Detecta automaticamente campos sem ID, sem Name, sem Label (acessibilidade) ou sem Autocomplete.
*   **Performance Watchdog:** Monitora métricas vitais como LCP (maior pintura com conteúdo), CLS (instabilidade visual) e Long Tasks (travamentos de script).
*   **Hyper-Observability:** 
    *   **Network:** Rastreia todas as chamadas AJAX/Fetch (Status, Duração, Payload).
    *   **Console:** Captura erros, avisos e logs do console do desenvolvedor.
    *   **Context Snapshots:** Captura o estado do DOM e o contexto visual em cliques e erros.
*   **Trace IDs:** Gera IDs de rastreamento únicos para cada interação, permitindo ligar um clique de usuário a um erro de backend.

## 📂 Estrutura de Arquivos

*   `/frontend/tracker.js`: O "cérebro" da telemetria e auditoria.
*   `/backend/receiver.php`: O receptor que processa e salva os logs.
*   `/backend/logs/`: Onde os arquivos de log diários são armazenados.
*   `/SENTRY/`: Módulo de monitoramento visual e interceptação de erros críticos.

---

## 👨‍💻 Para o Agente IA (Antigravity)
Sempre que você entrar em um projeto que possua esta pasta, você pode analisar a saúde do sistema lendo os arquivos em:
`13_ANTIGRAVITY_TELEMETRY/backend/logs/telemetry-YYYY-MM-DD.log`

---
*Desenvolvido por Antigravity - Observabilidade Nível Militar.*
