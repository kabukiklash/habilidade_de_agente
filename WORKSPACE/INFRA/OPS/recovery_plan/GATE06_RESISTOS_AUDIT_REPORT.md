# 🦅 GATE06_RESISTOS_AUDIT_REPORT.md (MILITARY GRADE)

**Status:** 🛡️ **CERTIFICATION COMPLETE (READ-ONLY)**  
**Data:** 2026-02-03T14:40:00Z  
**Engenheiro:** Antigravity (Kimi Auditor)  
**Veredito Geral:** ❌ **FAIL** (Regressão Crítica na Camada de Persistência)

---

## 1. COMPLIANCE DAS INVARIANTES CONSTITUCIONAIS

| ID | Invariante | Mecanismo de Defesa | Status | Evidência (Arquivo:Linha) |
|:---|:---|:---|:---|:---|
| **I-06.1** | **Soberania Total Drizzle** | Todas as tabelas ResistOS migradas para `schema.ts` (Drizzle). | ✅ **PASS** | `schema.ts:223-311` |
| **I-06.5** | **Purga Legada** | Remoção de `getDb()`, `sqlite3` e arquivos `server/db.js`. | ✅ **PASS** | `legacyPurgeVerificationSmoke.ts` |
| **I-06.8** | **Async Governance** | Componentes `ResistGate`, `Watchdog` e `CMSLedger` são async. | ✅ **PASS** | `resist-gate.ts`, `watchdog.ts` |
| **I-06.9** | **Atomic Ledger** | Sincronia entre Audit Log e Outbox Dispatch via Transação SQL. | ❌ **FAIL** | `ledgerRepo.ts:39`, `intents.ts:89` |

---

## 2. SMOKE TESTS — PROVA FÍSICA

| Teste | Objetivo | Resultado | Log de Verificação |
|:---|:---|:---|:---|
| `legacyPurgeVerificationSmoke.ts` | Verificar ausência de arquivos e drivers legados. | ✅ **PASS** | `Checking server/genesis.db: ✅ PURGED` |
| `sovereignPersistenceSmoke.ts` | Validar fluxo ponta-a-ponta no novo DB. | ❌ **FAIL** | `SQLITE_CONSTRAINT_NOTNULL: event_outbox.dedupe_key` |
| `budgetEnforcementSmoke.ts` | Testar bloqueio de execução por estouro de budget. | ⚠️ **GAP** | Teste não encontrado no diretório `/tests/smoke/`. |
| `attestationLedgerSmoke.ts` | Confirmar registro de atestações após execução. | ⚠️ **GAP** | Teste não encontrado no diretório `/tests/smoke/`. |

---

## 3. ANÁLISE FORENSE DA FALHA (CRITICAL REGRESSION)

Identifiquei uma falha estrutural no `IntentService`:
- O método `appendEventAtomic` no `LedgerRepo` exige que o objeto de entrada (`AppendEventAtomicInput`) contenha um `dedupeKey` para o `eventOutbox`.
- No arquivo `intents.ts`, as chamadas ao `appendEventAtomic` (linhas 89, 134, 181) estão **omitindo** o campo `dedupeKey`.
- **Efeito**: Violação de constraint `NOT NULL` no SQLite, quebrando todo o sistema de eventos e auditoria.

---

## 4. PURGA LEGADA - SCAN DE FUGA

- **getDb()**: Zero ocorrências encontradas.
- **sqlite raw**: Zero ocorrências encontradas.
- **server/genesis.db**: Removido fisicamente pelo commit do Gemini.
- **Dual Truth**: Reduzido, mas a falha no Ledger impede a validação da "Verdade Única" em tempo de execução.

---

## 5. RISCO RESIDUAL E VEREDITO

### ❌ Veredito: **FAIL (NÃO CERTIFICADO)**
Apesar da excelente migração estrutural (Drizzle) e da purga completa do legado, a camada de aplicação (`IntentService`) não foi atualizada para cumprir o contrato da nova `LedgerRepo`. O sistema de eventos soberanos está inerte devido a erros de banco de dados.

### 🛡️ Recomendações de Remediação (Gate 06.1):
1.  Atualizar todos os calls de `appendEventAtomic` em `intents.ts` para incluir um `dedupeKey` único.
2.  Implementar os smoke tests de **Budget** e **Attestation** que estão em GAP para garantir que a governança do ResistOS não é apenas estrutural, mas funcional.

---
**AVISO**: O Gate 07 (VibeCode) está **BLOQUEADO** até que a integridade atômica do Ledger seja restaurada.
