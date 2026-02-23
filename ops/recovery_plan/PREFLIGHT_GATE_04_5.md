# 🩺 PREFLIGHT_GATE_04_5 (Context Sanitizer: Anti-Leak Cognitivo)

**Objetivo:** Eliminar o vazamento de dados brutos (Context Leak) do Sovereign DB para LLMs (Claude/Kimi), garantindo que apenas representações estatísticas e metadados (Envelope Soberano) sejam transmitidos.

---

## 1. INVARIANTES DE SOBERANIA (GATE 04.5)

### 🛡️ I-01: Proibição de Raw Dumps (Anti-Leak)
É terminantemente proibido o uso de `JSON.stringify(context)` ou qualquer método que envie o estado bruto das células do Ledger para o prompt do LLM.

### 🍱 I-02: Uso Mandatório de Sovereign Envelope
Toda interação cognitiva deve passar pelo `ContextTransformer`, que converte o contexto em um `SovereignEnvelope` contendo:
- Metadados de integridade (Hashes de estado).
- Estatísticas de agregação (Contagem de eventos, tipos dominantes).
- Resumos sanitizados (Sem PII ou dados brutos).

### 🖋️ I-03: Proveniência e Recibo
A resposta do LLM deve ser validada contra o recibo gerado pelo `ContextTransformer`, garantindo que a "verdade" gerada pelo LLM está ancorada na observação do Ledger.

---

## 2. PONTOS DE INTERVENÇÃO (FAIL ATUAL)

- [ ] **FAIL**: `CognitiveEngine.execute` em `server/cognitiveService.ts` envia dump bruto no prompt.
- [ ] **FAIL**: `brain_bridge.py` em `server/llm/power_kit/` permite envio de `target_data` sem sanitização.

---

## 3. MECANISMO DE VERIFICAÇÃO (SMOKE TESTS)

### 🧪 `contextLeakSmoke.ts` (NEW)
**PASS**: Se o prompt capturado NÃO contiver dados brutos das células/eventos.
**FAIL**: Se houver qualquer indício de dump bruto.

### 🧪 `brainBridgeReceiptSmoke.ts` (NEW)
**PASS**: Se o Ledger registrar um evento `BRAIN_BRIDGE_CALL` com o hash do contexto sanitizado.

---

## 4. CRITÉRIOS DE PASSAGEM
1. [ ] Criação do `ContextTransformer.ts`.
2. [ ] Refatoração do `CognitiveEngine` para usar o Envelope.
3. [ ] Hardening do `brain_bridge.py` com limite de volume e registro em Ledger.
4. [ ] 100% de sucesso nos smoke tests.

---
**Bloqueio de Segurança:** O Gate 05 (WASM) permanece bloqueado até que a soberania cognitiva seja restabelecida em 04.5.
