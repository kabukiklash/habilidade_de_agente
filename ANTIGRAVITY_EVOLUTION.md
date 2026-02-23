# ANTIGRAVITY EVOLUTION PLAN (RFC-001)
> **Status:** PROPOSAL  
> **Type:** Architecture Evolution  
> **Goal:** State of the Art Auditability & Consistency (Passive Mode)

Este documento define o roadmap técnico para elevar o Antigravity a um sistema de governança auditável, determinístico e com memória técnica, respeitando estritamente o princípio de **Non-Agency** (Passive Only).

---

## 1. Persistência & Memória (The Immutable Ledger)

### Diagnóstico Atual
O sistema utiliza arquivos JSON (`data/conversations/`) que são mutáveis e difíceis de auditar granularmente. A recuperação de contexto é limitada a "Keyword Match" (Blind Indexing).

### Arquitetura Proposta: Event Sourcing Híbrido
Migração para um modelo onde a "Verdade" é um log de eventos imutável.

#### Fase 1: SQLite (Platform-Grade Immutable Ledger)
Implementação de um banco `antigravity.db` com esquema estrito e imutabilidade forçada por triggers.

**Schema Core (`audit_ledger`):**
- **Append-Only**: Protegido por triggers `BEFORE UPDATE` e `BEFORE DELETE`.
- **Integridade**: Encadeamento de hashes SHA-256 e Assinatura HMAC-SHA256.
- **Determinismo**: Canonicalização de JSON para payloads.
> **Benefício Principal:** Replayability. Podemos reconstruir o estado de qualquer conversa reprocessando os eventos. Se o código do sistema mudar, podemos rodar os eventos antigos para ver se o resultado diverge (Teste de Regressão Cognitiva).

#### Fase 2: Snapshotting & Read Models
Para performance, manteremos tabelas de leitura (`conversations`, `summaries`) que são *projeções* da tabela de eventos. Se o banco corromper, ele pode ser reconstruído do zero apenas com a tabela `events`.

#### Fase 3: Camada Semântica (Futuro: Postgres + pgvector)
Adicionar `embeddings` vetoriais vinculados aos eventos de `CONSENSUS_REACHED`. Isso permite que o Antigravity "lembre" de decisões passadas baseadas no *conceito* e não apenas palavras-chave.

---

## 2. Tools / MCP (Governança: Passive Intent Protocol)

### O Paradigma "Intent, not Action"
Para garantir **Non-Agency**, o Antigravity nunca invoca `exec()`. Ele emite **Intenções**.

#### Fluxo de Execução Seguro
1.  **Antigravity:** Analisa necessidade e emite evento `TOOL_INTENT_CREATED`.
    ```json
    {
      "tool": "read_file",
      "args": {"path": "config.json"},
      "risk": "READ_ONLY",
      "rationale": "Verificar parâmetros de criptografia"
    }
    ```
2.  **Kernel (Policy Engine):** Intercepta a intenção.
    *   *Check 1:* A ferramenta está na `ALLOWLIST`?
    *   *Check 2:* O argumento `path` está dentro do escopo permitido?
    *   *Check 3:* O risco requer aprovação humana?
3.  **Kernel:** Se aprovado, executa e emite `TOOL_RESULT_CAPTURED`. Se negado, emite `TOOL_DENIED`.

#### Especificação do Sandbox
*   **Python:** Execução via ambiente isolado (ex: `venv` descartável ou container efêmero) sem acesso à rede externa, exceto endpoints permitidos.
*   **Filesystem:** Acesso `READ` restrito a uma whitelist de diretórios. Acesso `WRITE` bloqueado por padrão ou restrito a diretórios temporários.

---

## 3. Reprodutibilidade & Infraestrutura

### Dev Container Philosophy
O ambiente deve ser idêntico para todos os desenvolvedores e para o CI.

**Estrutura Docker Compose:**
```yaml
services:
  antigravity-core:
    image: python:3.12-slim
    volumes:
      - ./data:/app/data  # Dados persistentes (SQLite)
      - ./logs:/app/logs  # Logs estruturados
    environment:
      - EXECUTION_MODE=PASSIVE
      - DB_URL=sqlite:////app/data/antigravity.db
```

**Comandos Padronizados (Makefile):**
*   `make start`: Sobe containers.
*   `make replay id={ulid}`: Re-executa uma cadeia de eventos para debug.
*   `make audit`: Gera relatório de integridade dos hashes do banco.

---

## 4. Observabilidade Cognitiva

### Estrutura de Log Semântica
Logs de texto não são suficientes. Usaremos logs estruturados (`structlog`) que podem ser visualizados como grafos.

**Exemplo de Log de Raciocínio:**
```json
{
  "level": "INFO",
  "event": "cognitive_divergence_detected",
  "stage": "2",
  "kpi_divergence": 0.45,
  "consensus_status": "FRAGILE",
  "participating_models": ["gpt-4", "claude-3", "mistral"],
  "outliers": ["mistral"]
}
```

**Artefatos de Visualização:**
Gerar ao final de cada ciclo um arquivo `reasoning_graph.json` que a UI possa renderizar, mostrando como o consenso convergiu (quem influenciou quem).

---

## 5. Qualidade & Testes (The Guardian Suite)

### Estratégia de Testes

1.  **Contract Tests (Integridade):**
    *   Garantir que os hashes da `events` chain sejam matematicamente válidos.
    *   Garantir que nenhum dado "Sensitive" (marcado via PII tag) seja gravado em plain text.

2.  **Cognitive Replay Tests (Determinismo):**
    *   *Cenário:* "Dada a entrada X e as Tools Y e Z retornando valores fixos (mock), o Antigravity DEVE chegar à conclusão W."
    *   Isso evita "drift" de personalidade ou lógica.

3.  **Security Regression:**
    *   Pipeline automatizado que tenta injetar comandos proibidos nas ferramentas. O teste passa se o `Policy Engine` bloquear.

---

## 6. Coprocessamento Cognitivo (Token Optimization)

### Desafio
O uso intensivo de LLMs de alto nível (ex: Gemini 1.5 Pro) em sessões longas consome tokens de contexto rapidamente, elevando o custo e reduzindo a janela de memória útil.

### Solução: Brain Bridge
Uso da Anthropic (Claude 3.5 Haiku/Sonnet) como coprocessador auxiliar para tarefas de alta densidade de dados e baixa necessidade de poder orquestrador.

#### Casos de Uso
1.  **Compressão de Contexto**: Enviar logs extensos ou bases de código para o Claude e receber apenas o "Summary Semântico" para o Gemini.
2.  **Análise de Dados Isolada**: Processamento de arquivos gigantes sem poluir o histórico de chat principal.
3.  **Drafting Técnico**: Geração de documentação extensa (Audit Reports, RFCs) delegada à ponte.

#### Implementação (`brain_bridge.py`)
```python
# Exemplo de uso via CLI
python brain_bridge.py "Analise este log de erro e resuma a causa raiz" server_error.log
```

---

## Roadmap de Implementação

### Ordem Sugerida

1.  **Fundação (Week 1):**
    *   [x] Setup do adaptador Anthropic e provedores genéricos.
    *   [x] Implementação do `brain_bridge.py` para economia de tokens.
    *   [x] Implementação do `antigravity.db` (SQLite) e classe `LedgerManager`.
    *   [x] Persistência Semântica (Fase 4): `semantic_memory.py`.
    *   [x] Verificação Formal (Fase 5): `formal_verifier.py`.
    *   [ ] Migrador de dados (JSON legado -> Eventos SQLite).

2.  **Segurança & Policy (Week 2):**
    *   [x] Implementação do `PolicyEngine` (Middleware de ferramentas).
    *   [x] Definição do Schema de `Intent`.

3.  **Observabilidade (Week 3):**
    *   [x] Setup do `structlog` e exportação de traces (logger.py).
    *   [x] Criação do comando `make audit` (audit_tool.py).

4.  **Consolidação (Week 4):**
    *   [x] Escrita dos testes de Replay (Simulados via LedgerManager).
    *   [x] Documentação final de arquitetura (ANTIGRAVITY_MANUAL.md).

---

## Riscos & Mitigações

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| **Inchaço do Banco** | SQLite ficar lento com milhões de eventos | Snapshots periódicos e arquivamento de eventos antigos (Cold Storage). |
| **Complexidade de Queries** | SQL se tornar complexo para ler eventos JSON | Uso de colunas geradas/virtuais no SQLite para indexar campos JSON frequentes. |
| **Rigidez** | Policy Engine bloquear usos legítimos | Implementar modo "Dry Run" onde violações apenas loggam WARNINGs durante a fase de ajuste. |
