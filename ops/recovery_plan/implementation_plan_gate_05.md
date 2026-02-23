# Case: Sovereign Runtime Sandbox (Gate 05)

Este plano detalha a implementação da "Jaula de Ouro" (Sandbox WASM) para garantir a execução segura de artefatos externos com isolamento total e controle de recursos.

## Alterações Propostas

### 🛡️ Componente: Execution Layer (Sandbox Core)

#### [NEW] [WasmRunner.ts](file:///c:/Users/RobsonSilva-AfixGraf/.gemini/antigravity/scratch/GenesisCoreFoundation/genesis-core-foundation/server/execution/WasmRunner.ts)
- Implementar executor baseado em `node:worker_threads` com memória compartilhada limitada.
- Adicionar lógica de **Fuel Metering**: decrementar contador a cada instrução/operação de host.
- Implementar **Capability Guard**: interceptor de syscalls que verifica tokens de permissão.

#### [MODIFY] [RuntimeClient.ts](file:///c:/Users/RobsonSilva-AfixGraf/.gemini/antigravity/scratch/GenesisCoreFoundation/genesis-core-foundation/server/core/RuntimeClient.ts)
- Refatorar para delegar execuções ao novo `WasmRunner`.
- Garantir a geração do **Sovereign Receipt** (JSON) após cada execução.
- Validar o `artifact_hash` antes e depois da execução.

### 📜 Componente: Infrastructure & Ledger

#### [MODIFY] [types.ts](file:///c:/Users/RobsonSilva-AfixGraf/.gemini/antigravity/scratch/GenesisCoreFoundation/genesis-core-foundation/server/types.ts)
- Adicionar `RUNTIME_RECEIPT_EMITTED` e `SANDBOX_VIOLATION` ao enum `EventTypes`.
- Definir interface `SovereignReceipt` para conformidade com a I-04.

#### [MODIFY] [ledgerRepo.ts](file:///c:/Users/RobsonSilva-AfixGraf/.gemini/antigravity/scratch/GenesisCoreFoundation/genesis-core-foundation/server/db/ledgerRepo.ts)
- Adicionar suporte para gravação de recibos e logs de violação no SQLite Soberano.

---

## Sequência de Execução

1. **Core**: Criar o `WasmRunner` com limites de memória e tempo (fuel simulado).
2. **Capability**: Implementar o sistema de tokens para `READ_LEDGER_SUMMARY`.
3. **Receipt**: Implementar a geração e assinatura do recibo determinístico.
4. **Kill Switch**: Validar abortagem imediata por estouro de memória ou fuel.

---

## Smoke Tests (MANDATÓRIOS)

| Teste | Objetivo |
| :--- | :--- |
| `wasmFuelLimitSmoke.ts` | Validar interrupção síncrona por consumo de recursos. |
| `wasmCapabilityDenySmoke.ts` | Validar bloqueio de acesso não autorizado ao Ledger. |
| `wasmReceiptDeterminismSmoke.ts` | Validar que o hash do artefato é imutável no recibo. |

---
**VEREDITO FINAL:** O sucesso deste gate permite a execução segura de qualquer código sugerido por LLMs (Kimi/Claude) sem risco para o host.
