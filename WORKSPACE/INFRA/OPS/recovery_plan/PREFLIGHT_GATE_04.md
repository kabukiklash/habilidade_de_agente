# 📜 PREFLIGHT_GATE_04.md (HARDENED EVENT INTEGRITY)

**Auditor:** Antigravity  
**Alvo:** `server/db/ledgerRepo.ts` & `server/cognitiveStreamAdapter.ts`  
**Objetivo:** Blindar o Ledger contra perdas de dados, duplicidade e inconsistência entre o log de auditoria e o envio de eventos.

---

## 1. 🛡️ INVARIANTES DE ENDURECIMENTO
Para garantir a integridade absoluta, aplicaremos:

- **Append-Only Sagrado**: A camada de repositório (`LedgerRepo`) será restrita à operação `insert` para as tabelas `events` e `event_outbox`. Qualquer código de `UPDATE/DELETE` nessas tabelas será considerado uma violação de segurança.
- **Atomicidade de Outbox**: O registro de um evento no Ledger (`events`) e sua entrada na fila de despacho (`event_outbox`) ocorrerão dentro da mesma transação de banco de dados. 
    - *Vibe:* "Se o evento não foi gravado, ele nunca sai. Se ele saiu, ele está gravado."
- **Idempotência por DedupeKey**: Cada intenção gerará uma `dedupeKey` determinística (ex: `correlationId + eventType`). O `appendEventAtomic` verificará se essa chave já existe antes de prosseguir, evitando duplicidade em retries de rede.

---

## 2. 🧠 UNIFICAÇÃO DO STREAM (PROVENANCE RECOVERY)
O `CognitiveStreamAdapter` será desconectado do `eventBus` (volátil) e passará a:
1. Manter um cursor de `createdAt` local.
2. Consultar periodicamente (ou via trigger de polling) a tabela `events` do Sovereign DB.
3. Isso garante que o Dashboard mostre a **verdade gravada**, não apenas o que passou pela memória RAM.

---

## 3. ⚡ TRÍADE DE FALHAS ANTECIPÁVEIS
1. **Transaction Bloat**: Se o banco estiver lento, transações atômicas de escrita podem enfileirar. (Mitigação: Manter a transação mínima, apenas os dois inserts).
2. **Cursor Drift**: O cursor do SSE pode "pular" eventos se múltiplos eventos tiverem o mesmo timestamp exato em alta concorrência. (Mitigação: Usar combinação de `createdAt` + ID sequencial se necessário).
3. **Double Dispatch**: Se a idempotência falhar, o Outbox pode enviar o mesmo evento duas vezes. (Mitigação: Constraint de `UNIQUE` na `dedupe_key` no banco).

---

## 4. ✅ CRITÉRIOS DE SUCESSO (PASS/FAIL)
- **outboxAtomicitySmoke.ts**: 
    - Simular erro forçado após o insert em `events`.
    - **PASS**: 0 registros órfãos em ambas as tabelas (rollback completo).
- **retryIdempotencySmoke.ts**: 
    - Chamar `appendEventAtomic` 10 vezes seguidas com a mesma `correlationId`.
    - **PASS**: Exatamente 1 registro gravado no banco.
- **sseSourceSmoke.ts**: 
    - Dashboard/Stream prova que `provenance == sovereign_db`.
    - **PASS**: Eventos injetados diretamente no banco aparecem no stream sem passar pelo bus de memória.

---
**ESTADO:** AGUARDANDO AUTORIZAÇÃO.
