# Case: Cognitive Sovereignty Hardening (Gate 04.5)

Este plano detalha a remediação imediata dos vazamentos de contexto (Context Leak) identificados na auditoria forense, garantindo que nenhum LLM receba o estado bruto do Sovereign DB.

## Contexto e Objetivos
A auditoria revelou que o `CognitiveEngine` e o `brain_bridge` enviam dumps completos do banco para o Anthropic. Este gate implementa uma camada de "Cripple Context" (ContextTransformer) e obriga o uso de um Envelope Soberano para toda interação cognitiva.

---

## Alterações Propostas

### 🛡️ Componente: Cognitive Layer (Cripple Context)

#### [NEW] [ContextTransformer.ts](file:///c:/Users/RobsonSilva-AfixGraf/.gemini/antigravity/scratch/GenesisCoreFoundation/genesis-core-foundation/server/ContextTransformer.ts)
- Implementar função `transformToSovereignEnvelope(context: CognitiveContext): SovereignEnvelope`.
- A função deve extrair apenas metadados (contagem de células, IDs afetados, hashes de conteúdo) e um resumo estatístico, eliminando o estado bruto.

#### [MODIFY] [cognitiveService.ts](file:///c:/Users/RobsonSilva-AfixGraf/.gemini/antigravity/scratch/GenesisCoreFoundation/genesis-core-foundation/server/cognitiveService.ts)
- Refatorar `CognitiveEngine.execute` para invocar o `ContextTransformer`.
- Substituir o prompt que contém `JSON.stringify(context)` pelo prompt baseado no Envelope Soberano.
- Integrar validação de recibo: a resposta deve ser marcada com os hashes/IDs observados.

### 🐍 Componente: Python Bridge (Shadow Channel Fix)

#### [MODIFY] [brain_bridge.py](file:///c:/Users/RobsonSilva-AfixGraf/.gemini/antigravity/scratch/GenesisCoreFoundation/genesis-core-foundation/server/llm/power_kit/brain_bridge.py)
- Proibir o envio de `target_data` bruto se este exceder um limite de segurança ou contiver padrões de dados sensíveis.
- Implementar chamada via `ledger_manager` para registrar o evento `BRAIN_BRIDGE_CALL` com o hash do processo.

### 📜 Componente: Infrastructure & Types

#### [MODIFY] [types.ts](file:///c:/Users/RobsonSilva-AfixGraf/.gemini/antigravity/scratch/GenesisCoreFoundation/genesis-core-foundation/server/types.ts)
- Adicionar `BRAIN_BRIDGE_CALL` e `COGNITIVE_TRANSFORMATION` ao enum `EventTypes`.

#### [MODIFY] [ledgerRepo.ts](file:///c:/Users/RobsonSilva-AfixGraf/.gemini/antigravity/scratch/GenesisCoreFoundation/genesis-core-foundation/server/db/ledgerRepo.ts)
- Garantir suporte à persistência dos novos tipos de eventos de auditoria cognitiva.

---

## Plano de Verificação

### Testes Automatizados (Smoke Tests)
Os testes serão salvos em `server/db/` para execução direta via `tsx`.

1. **`contextLeakSmoke.ts`**:
   - `npx tsx server/db/contextLeakSmoke.ts`
   - **PASS**: Se o prompt gerado interceptado NÃO contiver a string `"cells":[` com dados reais.
   - **FAIL**: Se houver qualquer indício de dump bruto no prompt.

2. **`brainBridgeReceiptSmoke.ts`**:
   - `npx tsx server/db/brainBridgeReceiptSmoke.ts`
   - **PASS**: Se após disparar o bridge Python, o Ledger (SQLite) contiver um evento `BRAIN_BRIDGE_CALL`.

3. **`dualTruthBlockSmoke.ts`**:
   - `npx tsx server/db/dualTruthBlockSmoke.ts`
   - **PASS**: Se a API rejeitar uma resposta cognitiva que não correlacione com os hashes de recibo gerados pelo transformador.

### Verificação Manual
- Inspecionar os logs do `AnthropicProvider` (que já possui sanitização) para confirmar que o volume de dados enviados diminuiu drasticamente e agora segue o formato de envelope.
