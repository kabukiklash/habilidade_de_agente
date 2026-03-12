# 🩺 PREFLIGHT_GATE_06.md (Sovereign Data Unification)

**Status:** 🟡 **WAITING_AUTHORIZATION**  
**Gate:** 06 — Data Sovereignty  
**Objetivo:** Eliminar definitivamente o banco fantasma (`server/genesis.db`) e unificar todo o estado no Provedor Soberano (`data/genesis.sqlite`).

---

## 🛡️ 1. INVARIANTES TÉCNICAS (I-06)

| ID | Invariante | Descrição |
| :--- | :--- | :--- |
| **I-06.1** | **Single Source of Truth** | Apenas UM banco de dados operacional (`data/genesis.sqlite`) deve existir no Foundation. |
| **I-06.2** | **ORM Lockdown** | Toda interação com DB deve passar pelo Drizzle ORM. Proibido o uso de `better-sqlite3` direto fora do provider. |
| **I-06.3** | **Schema Parity** | O `server/db/schema.ts` deve conter 100% das tabelas necessárias para Intents, Approvals e Execuções. |
| **I-06.4** | **Data Hermeticity** | O banco físico deve residir em `data/`, protegido de deleções acidentais durante build/purge de `server/`. |
| **I-06.5** | **Legacy Zero-Tolerance** | O arquivo `server/db.ts` e o banco `server/genesis.db` devem ser deletados após a migração. |

---

## 🏗️ 2. PLANO DE ATAQUE

1.  **Refatoração de Schema**: Migrar as definições de `schema.sql` para `server/db/schema.ts`.
2.  **Expansão do Repository**: Adicionar suporte no `ledgerRepository` (ou novo `intentRepository`) para as tabelas migradas.
3.  **Harden Kernel**: Atualizar o `ExecutionKernel` para não depender mais de `db.ts` legado.
4.  **Purge**: Deletar `server/genesis.db` e `server/db.ts`.
5.  **Audit**: Garantir que o `LedgerManager` em Python continue registrando no Ledger Cross-Agent.

---

## 🧪 3. CRITÉRIOS DE LIBERAÇÃO (SMOKE TESTS)

A Fase 6 só será considerada **PASS** quando:
- [ ] `sovereignPersistenceSmoke.ts` confirmar que Intents e Recibos estão no mesmo arquivo SQLite.
- [ ] `legacyPurgeVerificationSmoke.ts` confirmar a ausência física de `server/genesis.db`.
- [ ] O sistema iniciar sem avisos de "Schema initialized" do banco legado.

---
**EMITIDO POR:** Antigravity (security-auditor)  
**COMANDO:** `autorizar Fase 6`
