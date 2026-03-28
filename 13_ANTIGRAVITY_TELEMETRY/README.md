# 🚀 Antigravity Telemetry Pro Max

O Antigravity Telemetry é um módulo universal para monitoramento em tempo real de interações e falhas no frontend. Ele é especialmente projetado para capturar erros silenciosos que não aparecem nos logs do servidor.

---

## 🛠️ Como Funciona
A ferramenta "grampeia" o navegador para registrar:
- **Cliques**: Mapeia exatamente onde o usuário clicou (ID, Classe, Texto).
- **Erros de JS**: Captura `window.onerror` com **Stack Traces** completos.
- **Falhas AJAX/Fetch**: Detecta quando uma requisição falha ou quando o PHP vaza HTML (`Unexpected token <`) em vez de JSON.
- **Contexto 360°**: Registra URL, Resolução de Tela e Sessão do Usuário.

---

## 📁 Estrutura de Arquivos
- `/frontend/tracker.js`: O "espião" que roda no navegador.
- `/backend/receiver.php`: O receptor que salva os dados no servidor.
- `/backend/logs/`: Pasta onde os arquivos `.log` diários são gerados.

---

## 📖 Como Ler os Logs
Os logs são salvos diariamente em `telemetry-YYYY-MM-DD.log`. Cada entrada segue este padrão:

```text
[2026-03-24 10:30:00] IP: 127.0.0.1
Session: sess_xyz123 | URL: http://afixcontrol.com/clientes
  -> [CLICK] ... : {"path": "button#save", "text": "Salvar"}
  -> [AJAX_ERROR] ... : {"url": "ajax/clientes.php", "status": 200, "response": "<b>Warning</b>: level undefined..."}
```

> [!TIP]
> **Dica de Debug:** Procure por `AJAX_ERROR` quando o usuário reclamar de erros de sintaxe ou comportamentos inesperados em formulários.

---

## ⚙️ Configuração
Para usar em outra parte do sistema, basta incluir o script no `<head>` ou final do `<body>`:

```html
<script src="/13_ANTIGRAVITY_TELEMETRY/frontend/tracker.js"></script>
```

**Configuração do Endpoint:**
Dentro do `tracker.js`, a variável `config.endpoint` deve apontar para o `receiver.php`.

---

**Status:** v2.0 Pro Max (Interception Active)
