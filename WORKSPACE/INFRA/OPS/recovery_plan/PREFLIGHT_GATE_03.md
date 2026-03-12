# 🧠 PREFLIGHT_GATE_03.md (COGNITIVE CORTEX UNIFICATION)

**Auditor:** Antigravity  
**Alvo:** `server/cognitiveService.ts` & `server/routes/cognitive.ts`  
**Objetivo:** Unificar o Cortex Cognitivo, migrando a leitura de estado do Legacy SQLite para o Sovereign DB e integrando o `LLMProvider` real.

---

## 1. 🔍 FONTE SOBERANA DE "COGNITIVE STATE"
Para evitar a reintrodução de dados legados ou "alucinações" por descontinuidade, a unificação seguirá estes pilares:

- **Histórico (Audit Log)**: A autoridade absoluta é a tabela `events` do Sovereign DB (Postgres/SQLite Agnostic). O rastro de eventos é a "memória de longo prazo".
- **Estado Atual (Snapshot)**: Introduziremos a tabela `cells` no `server/db/schema.ts` (Sovereign). O estado de cada unidade de memória será projetado e lido exclusivamente via `DatabaseProvider`.
- **Provedor de IA**: A integração com o cérebro (Kimi/Anthropic) será mediada pelo `LLMProvider`, com fallback para `MockProvider` em ambientes de teste, garantindo que o motor cognitivo não dependa de chaves de API para as invariantes de fluxo.

---

## 2. 🧠 DRY-RUN MENTAL (O NOVO FLUXO)
1. **Request:** UI envia Query CQL para `/v1/cognitive/query`.
2. **Contexto:** O `CognitiveService` usa o `DatabaseProvider` para buscar eventos e células recentes no **Sovereign DB**.
3. **Reasoning:** O `CognitiveEngine` envia o contexto para o `LLMProvider`.
4. **Resilience:** Se o Sovereign DB estiver configurado para Postgres, o Cortex lê Postgres. Se estiver em SQLite (Sovereign), lê o arquivo centralizado. **Nunca** o `genesis.db` legado.

---

## 3. ⚡ TRÍADE DE FALHAS ANTECIPÁVEIS
1. **Legacy Leak**: O código antigo importa `server/db.ts`. (Mitigação: Remoção total de referências ao `db.ts` legado nas rotas cognitivas).
2. **Schema Mismatch**: A tabela `cells` no legada possui campos (`friction`, `retention`) que precisam ser mapeados para o Drizzle. (Mitigação: Update do `schema.ts` antes da unificação).
3. **Hallucination (Stale Data)**: O Cortex pode responder com base em mocks se a injeção de provedor falhar. (Mitigação: Requisitar `ok: true` e `provenance: 'sovereign_db'` no payload de resposta).

---

## 4. ✅ TESTE DE REGRESSÃO (CORTEX FRESHNESS - DETERMINÍSTICO)
- **Script**: `server/db/cortexFreshnessSmoke.ts`.
- **Lógica**:
    1. Injetar uma `cell` com um ID aleatório (`cortex_test_XXXX`) diretamente no Sovereign DB.
    2. Executar uma query cognitiva via `/cognitive/query`.
    3. O serviço deve retornar um objeto de debug opcional: `crm.debug.cells_seen_ids[]`.
- **PASS**: O ID `cortex_test_XXXX` está presente na lista `cells_seen_ids` **e** a `provenance` é `sovereign_db`. (Isso prova que o serviço leu o dado correto do banco soberano ANTES de enviar ao LLM).
- **FAIL**: O ID não aparece ou a lista está vazia, indicando que o Cortex falhou em recuperar a realidade atual do banco.

---
**ESTADO:** AGUARDANDO REVISÃO DO ENGENHEIRO.
**AUTORIZAÇÃO:** Nenhuma mudança aplicada até confirmação.
