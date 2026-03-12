# 🩺# [REF-EXTERNA — GENESISCORE] PREFLIGHT_GATE_05.md

**Objetivo:** Criar a "Jaula de Ouro" (Sovereign Sandbox) para execução de artefatos externos e prompts de LLM, garantindo isolamento absoluto, controle de recursos e proveniência comprovável via WASM.

---

## 1. INVARIANTES DE SOBERANIA (GATE 05)

### 🛡️ I-01: Black-Box Execution
O ambiente WASM deve operar em isolamento total:
- **Zero Filesystem**: Sem acesso ao disco do host.
- **Zero Network**: Sem acesso a sockets ou rede externa.
- **Zero Env**: Nenhuma variável de ambiente do host deve vazar para o sandbox.

### ⛽ I-02: Fuel Budget
Cada execução possui um limite rígido e determinístico de recursos:
- **Limite Fixo**: Ex: 5.000.000 unidades de fuel.
- **Interrupt**: A execução deve ser abortada imediatamente ao atingir o limite.

### 🔑 I-03: Capability Tokens
Nenhuma syscall ou acesso a funções de host é permitido sem um token explícito:
- **Permissions**: `READ_LEDGER_SUMMARY`, `EMIT_RECEIPT`.
- **Default Deny**: Se não houver token, o acesso é negado silenciosamente ou gera erro de runtime.

### 📜 I-04: Deterministic Receipt
Toda execução deve gerar um recibo assinado contendo:
- `execution_id`: UUID único da execução.
- `fuel_used`: Consumo exato de fuel.
- `capabilities`: Lista de permissões utilizadas.
- `artifact_hash`: SHA256 do código executado.

### 🚫 I-05: Kill Switch
Qualquer tentativa de violação de segmentação ou abuso de recursos deve resultar em:
- **Abort**: Interrupção imediata da instância.
- **Audit**: Registro obrigatório no Ledger de um evento `SANDBOX_VIOLATION`.

---

## 2. MECANISMO DE VERIFICAÇÃO (SMOKE TESTS)

### 🧪 `wasmFuelLimitSmoke.ts`
Provoca um loop infinito no WASM e valida se o Sandbox interrompe a execução EXATAMENTE no limite de fuel.

### 🧪 `wasmCapabilityDenySmoke.ts`
Tenta realizar uma operação privilegiada (ex: ler Ledger) sem o token necessário e valida o bloqueio.

### 🧪 `wasmReceiptDeterminismSmoke.ts`
Executa o mesmo artefato 3 vezes e valida se o `artifact_hash` e a estrutura do recibo permanecem idênticos.

---

## 3. CRITÉRIOS DE PASSAGEM
1. [ ] Implementação do `WasmRunner` (Rust-based ou Node VM Isolada).
2. [ ] Sistema de medição de Fuel ativo e funcional.
3. [ ] Ledger persistindo o evento `RUNTIME_RUN_FINISHED` com o Recibo Determinístico.
4. [ ] 100% de sucesso nos smoke tests.

---
**Bloqueio de Segurança:** Ninguém atravessa o Gate 05 sem provar que a "Jaula de Ouro" é inviolável.
