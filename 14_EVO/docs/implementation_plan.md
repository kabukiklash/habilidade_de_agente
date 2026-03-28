# [RM-000] Arquitetura Orientada a Sensores: CMS Cloudflare + Painel Unificado

Este documento é a nossa "Bíblia Arquitetural". Ele materializa o checklist do Arquiteto-Chefe e mapeia cada nova funcionalidade a um Sensor de Observabilidade (ODD - Observability-Driven Development). **Nenhum código será escrito se não estiver amparado por uma Fase deste documento.**

## User Review Required
> [!IMPORTANT]
> Avalie este roteiro. Se aprovado, ele guiará rigorosamente nossa execução técnica, garantindo que não pulemos etapas de segurança ou dados.

---

## O Checklist do Arquiteto (Roteiro de Execução)

### Fase 1: Descoberta e Invariantes (A Bússola)
**Regras de Ouro Inegociáveis para este Épico:**
1. **Invariante 1 (Efemeridade):** A exposição à internet será temporária (via Cloudflare Quick Tunnels), nunca permanente.
2. **Invariante 2 (Transparência):** O programador deve visualizar em tempo real o que o ACE está aprendendo e enviando para o CMS.
3. **Invariante 3 (Trilha de Auditoria):** As trocas de contexto devem ser salvas para posterior estudo analítico.

### Fase 2: Arquitetura de Portas e Sensores (O Mapa)
Definimos aqui as fronteiras físicas e os sensores (Roadmap Codes).

*   **[RM-001] O Túnel Efêmero**
    *   **Descrição:** Script responsável por expor a porta local (8090) para o mundo de forma encriptada via Cloudflare.
    *   **Sensor Mapeado:** `sensor_CF_TUNNEL` (Verifica se a URL pública existe e se o processo está vivo).
*   **[RM-002] O ACE Nômade (Fallback Bridge)**
    *   **Descrição:** O cliente ACE local passa a suportar uma URL externa caso o `localhost` falhe.
    *   **Sensor Mapeado:** `sensor_ACE_UPLINK` (Monitora o handshake 200 OK com o CMS remoto).
*   **[RM-003] Interface de Comando Unificada (Glass Brain)**
    *   **Descrição:** Dashboard do CMS atuando como painel de monitoramento do ecossistema inteiro.
    *   **Sensor Mapeado:** `sensor_DASHBOARD_HEARTBEAT` (Garante que os WebSockets de tradução em tempo real estão ativos).

### Fase 3: Arquitetura de Dados e Estado (A Memória)
A estrutura que armazenará o raciocínio da máquina.

*   **[RM-004] Tabela de Auditoria Cognitiva**
    *   **Descrição:** Migração/Criação no SQLite de uma tabela (`ai_reasoning_audits`) imutável (APPEND-ONLY) para rastro das injecões de inteligência. A conexão obrigatoriamente forçará `PRAGMA journal_mode=WAL;` para mitigar travas de concorrência (`database is locked`).
    *   **Esquema Básico:** `id, timestamp, fonte (PC1/PC2), acao_tomada, tokens_economizados, traducao_humanizada`.

### Fase 4: Segurança, Identidade e Governança (Zero-Trust)
*   **[RM-005] Barreira de Borda (API Key)**
    *   **Descrição:** Middleware no FastAPI do CMS que exige um header `X-ACE-API-KEY` para aceitar qualquer payload externo proveniente do Túnel Cloudflare. Inclui validação de WebSocket via Handshake Criptografado (sem chave na URL) e Rate Limiting Anti-DoS (bloqueio por IP em memória RAM após tentativas excessivas).
*   **[RM-006] Prevenção Cross-Site Scripting (XSS)**
    *   **Descrição:** Renderização estrita no frontend do Glass Brain convertendo payloads semânticos apenas via mapeamentos textuais (`textContent`), banindo renderizações DOM (`innerHTML`).

### Fase 5: Contratos de Comunicação
*   **Contrato de Envio (ACE -> CMS):** JSON com `{"local_auth": "...", "payload": "..."}`.
*   **Contrato de Autenticação Híbrida (ACE):** O cliente salvará as credenciais no `.env` local com validação automática de `.gitignore`. Hot-Reload de variáveis em RAM (sem restart). Fila Outbox local para resiliência offline.
*   **Contrato de WebSocket (CMS Backend -> Dashboard HTML):** `{"tipo": "log_traduzido", "mensagem": "O Agente do Notebook 2 salvou 1200 tokens ao corrigir a rota de login."}`.

### Fase 6: Engenharia de Confiabilidade (CI/CD Local)
*   Modificaremos o `Pattern-Enforcer` atual (Git Hook) para alertar se tentarem subir credenciais do túnel para repositórios.

---

## Proposed Changes (Onde vamos mexer no código)

1.  #### [NEW] `root/ops/expor_cms_cloudflared.bat`
    *   Script PowerShell/Batch encapsulado para baixar o `cloudflared` de fontes nativas oficiais.

2.  #### [MODIFY] `cognitive-memory-service/app/main.py`
    *   Adição do Middleware de API Key (Segurança REST e WebSocket).

3.  #### [MODIFY] `cognitive-memory-service/dashboard/index.html` (e relacionados)
    *   Remodelagem completa do Dashboard para incluir o semáforo de Sensores (CF_TUNNEL, ACE_UPLINK), a Animação e os Logs Traduzidos.

4.  #### [MODIFY] `ace-installer-kit/ace_server.py`
    *   Lógica para perguntar/aceitar a URL do Cloudflare quando o localhost falhar. Lógica para injetar o header de autenticação.

5.  #### [MODIFY] `cognitive-memory-service/app/db.py` & `sql/001_init.sql`
    *   Criação da tabela de auditoria `ai_reasoning_audits`.

## Verification Plan
1.  **Auditoria do Túnel:** Rodar o arquivo `.bat`, verificar se a URL é gerada e se aponta corretamente para o FastAPI local.
2.  **Auditoria de Segurança:** Tentar fazer POSTs manuais na URL gerada pelo Cloudflare sem a API KEY e verificar se o FastAPI retorna `401 Unauthorized`.
3.  **Auditoria de Sensores:** Abrir o novo Dashboard do CMS e verificar se os semáforos dos Sensores (RM-001 e RM-002) respondem às quedas propositais da rede.
