# 🛫 PREFLIGHT_GATE_02.md (DISPATCH CONVERGENCE)

**Auditor:** Antigravity  
**Alvo:** `server/routes/intents.ts` & `server/adapters/express-host.ts`  
**Objetivo:** Eliminar escritas redundantes nas rotas e centralizar a autoridade de persistência nos Serviços (`IntentService` / `ApprovalService`).

---

## 1. 🔍 MAPEAMENTO DE AUTORIDADE (DUAL TRUTH AUDIT)

| Fluxo | Escrita na Rota (Divergente) | Escrita no Serviço (Soberano) | Status |
| :--- | :--- | :--- | :--- |
| **Executar Intenção** | `server/routes/intents.ts:29` (`db.insert`) | `server/core/intents.ts:34` (`tx.insert`) | 🚨 **DUAL TRUTH** |
| **Audit Log** | `server/routes/intents.ts:40` (`ledger.append`) | `server/core/intents.ts:88` (`LedgerRepo`) | 🚨 **REDUNDANTE** |
| **Update Status** | `server/routes/intents.ts:142` (`db.update`) | `server/core/intents.ts:185` (`db.update`) | 🚨 **DUAL TRUTH** |

**Autoridade Única Identificada:** `IntentService` (Core) e `ApprovalService` (Core).

---

## 2. 🧠 DRY-RUN MENTAL (O NOVO CAMINHO)
1.  **Request:** O Dashboard envia `POST /v1/intents/execute`.
2.  **Host:** `ExpressHost` recebe e chama **diretamente** `intentService.executeIntent(req.body)`.
3.  **Serviço:** O serviço abre uma **única transação**, grava o estado, o outbox e o ledger.
4.  **Resultado:** A rota retorna apenas o `IntentResponse`. Não há código de banco de dados no nível de roteamento.

---

## 3. ⚡ TRÍADE DE FALHAS ANTECIPÁVEIS
1.  **Orphaned Records:** Se o serviço falhar mas a rota (antes do refactor) tivesse gravado algo, teríamos orfandade. (Mitigação: Limpeza total de registros de teste antes da execução).
2.  **Missing Ledger Context:** A rota hoje injeta alguns metadados no Ledger que o serviço pode não ter. (Mitigação: Sincronizar os payloads no `intentService` antes de apagar a rota).
3.  **UI Break:** O Dashboard pode estar esperando um formato de erro específico da rota que o serviço não emite. (Mitigação: Manter o mapeador de status HTTP no `ExpressHost`).

---

## 4. 🛡️ INVARIANTES INTOCÁVEIS
- **ID de Correlação:** Deve ser passado do Host para o Serviço para manter o vínculo entre Request e Ledger.
- **Transação Atômica:** Toda escrita iniciada por uma intenção DEVE ocorrer dentro de um `db.transaction`.

---

## 5. ✅ CRITÉRIOS DE REGRESSÃO (ZERO DUAL TRUTH)
- **Teste:** Script `server/db/zeroDualTruthSmoke.ts`.
- **Pass:** Após um request de `/intents/execute`, a contagem de registros em `intents` e `events` para aquele `correlation_id` deve ser exatamente **1**.
- **Fail:** Se houver duplicidade ou se o Ledger registrar eventos disparados pela Rota e pelo Serviço simultaneamente.

---
**ESTADO:** AGUARDANDO REVISÃO DO ENGENHEIRO.
**AUTORIZAÇÃO:** Nenhuma mudança aplicada até confirmação.
