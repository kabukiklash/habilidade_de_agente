# 🛫 PREFLIGHT_GATE_00.md (AGNOSTIC SCHEMA FACTORY)

**Auditor:** Antigravity  
**Alvo:** `server/db/schema.ts`  
**Objetivo:** Neutralizar a divergência de dialeto (SQLite vs PG) no nível de definição de tabelas.

---

## 1. 🧠 DRY-RUN MENTAL (O CAMINHO DO DADO)
O arquivo `schema.ts` deixará de ter exportações estáticas de `sqliteTable`. Em vez disso, ele usará uma abstração (ex: `pgTable` ou `sqliteTable` injetado) ou exportará esquemas compatíveis com ambos. 
- **Entrada:** O `DatabaseProvider` (Gate 01) solicitará o esquema.
- **Processamento:** O Drizzle resolverá as colunas (`text`, `integer`, `timestamp`) usando o driver correto.
- **Saída:** Objetos de tabela tipados que o Drizzle consiga usar em `db.insert()` ou `db.select()` sem erros de "Dialect mismatch".

## 2. ⚡ TRÍADE DE FALHAS ANTECIPÁVEIS
1.  **Serialization Paradox:** SQLite retornar string JSON em vez de objeto, quebrando o `IntentService` (Mitigação: `customType` wrapper).
2.  **FK Reference Break:** As chaves estrangeiras (`.references()`) falharem ao tentar cruzar definições de dialetos diferentes (Mitigação: Travar todas as refs no mesmo contexto de dialect).
3.  **Timestamp Mismatch:** SQLite (`integer`) vs PG (`timestamp`) causando erros de comparação de data (Mitigação: Normalização via helper de coluna).

## 3. 🛡️ INVARIANTES DE PROTEÇÃO
- **Nomes de Tabela:** Devem permanecer exatamente `intents`, `events`, `approval_requests`, etc.
- **Nomes de Coluna:** Devem permanecer em `camelCase` no TS e `snake_case` no SQL (onde aplicável).
- **Tipagem TS:** O tipo exportado pelo Drizzle (`InferSelectModel`) deve ser idêntico para ambos os bancos para não quebrar os serviços (`IntentService`, `ApprovalService`).

---
**ESTADO:** PRONTO PARA EXECUÇÃO MÍNIMA.
**AUTORIZAÇÃO REQUERIDA:** Nenhuma (Autorizado pelo Engenheiro em Step 475).
