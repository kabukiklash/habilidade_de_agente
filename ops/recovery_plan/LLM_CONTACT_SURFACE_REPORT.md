# 🦅 LLM_CONTACT_SURFACE_REPORT.md (MILITARY GRADE)

**Status:** 🛡️ **FORENSIC AUDIT COMPLETE**  
**Data:** 2026-02-02T19:15:00Z  
**Engenheiro:** Antigravity  
**Veredito Geral:** 🔴 **FAIL** (Soberania Comprometida por Vazamento de Contexto)

---

## 1. MAPA DE SUPERFÍCIE LLM (100% COBERTURA)

| Location | Symbol/Function | Type of Contact | Data In/Out | Context Leak? | Env Leak? | Hermetic? | Sovereignty Risk | Suggested Fix |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| `server/cognitiveService.ts` | `CognitiveEngine.execute` | Async/Network (via internal LLM call) | **IN**: Entire `CognitiveContext` (cells, events, metrics) / **OUT**: Unstructured Text | 🔴 **FAIL** | ✅ SAFE | ❌ NO | 🔴 **FAIL** | **Cripple Context**: LLM deve receber apenas resumos (hashes) ou metadados, nunca o estado bruto do banco. |
| `server/llm/anthropic.ts` | `AnthropicProvider.generate` | Async/Network (HTTP Fetch) | **IN**: LLMRequest (Prompt) / **OUT**: LLMResponse | ✅ SAFE | 🟠 WARN (Reads Key) | ❌ NO | 🟠 WARN | **Vault Injection**: Chave deve ser injetada via Secret Manager, não lida de `process.env` global. |
| `server/llm/power_kit/brain_bridge.py` | `brain_bridge` | Sync/Network (Python Subprocess) | **IN**: `target_data` (strings/files) / **OUT**: Analysis result | 🔴 **FAIL** | ✅ SAFE | ❌ NO | 🟠 WARN | **Pre-processor Gate**: Dados devem ser filtrados por uma camada de PI (Personal Information) antes do bridge. |
| `server/llm/power_kit/anthropic_provider.py` | `AnthropicProvider.generate` | Sync/Network (urllib.request) | **IN**: Prompt / **OUT**: Text Response | ✅ SAFE | 🟠 WARN (os.environ) | ❌ NO | 🟠 WARN | **Standardize Provider**: Unificar com o provider TypeScript para auditoria centralizada. |
| `server/execution/python-runner.ts` | `PythonRunner.run` | Background Subprocess (spawn) | **IN**: User Python code / **OUT**: stdout/stderr | ✅ SAFE | ✅ **SAFE** | ✅ YES | ✅ SAFE | Nenhuma (A isolação via `env: { PYTHONDONTWRITEBYTECODE: '1' }` é efetiva contra vazamento de `process.env`). |
| `server/llm/power_kit/ledger_manager.py` | (Internal Logic) | Local DB (SQLite) | N/A | ✅ SAFE | ✅ SAFE | ✅ YES | ✅ SAFE | Nenhuma (Garante a integridade do audit log). |

---

## 2. ANÁLISE DE VAZAMENTO DE CONTEXTO (CRÍTICO)

### 🔴 FAIL: [Context Leak] `server/cognitiveService.ts:43-68`
O método `CognitiveEngine.execute` realiza uma operação de "Extreme Dumping":
```typescript
const prompt = `Context: ${JSON.stringify(context)}. Query: ${ast.query}`;
```
Isso expõe o **Aggregate State** completo (Cells e Audit Log) para um provider externo (Anthropic). Qualquer falha de segurança no provider ou interceptação de rede resulta em exposição total da memória do sistema. 

### 🔴 FAIL: [Context Leak] `server/llm/power_kit/brain_bridge.py:6-42`
O `brain_bridge` injeta `target_data` (muitas vezes conteúdo bruto de arquivos ou logs) diretamente no prompt:
```python
prompt = f"""... Data/Context: {target_data if target_data else "No additional data provided."} """
```

---

## 3. SOBERANIA / VERDADE ÚNICA

### 🔴 FAIL: Dual Truth Risk
O sistema permite que o `CognitiveEngine` retorne textos que são exibidos na UI como "Realidade", mas essa realidade é gerada por inferência (`claude-3-haiku-mock` ou real) e não é reconciliada com o Ledger antes da exibição. O LLM atua como uma **Autoridade de Interpretação** sobre o banco.

---

## 4. ANEXO: CALL GRAPH DOS 10 CAMINHOS CRÍTICOS

1.  **Sovereign Data Leak Path:**
    `Sovereign DB` → `routes/cognitive.ts` → `CognitiveEngine.execute` → `JSON.stringify(Context)` → `Anthropic API` (FAIL)

2.  **External Audit Path (Python):**
    `User Task` → `power_kit/brain_bridge.py` → `os.environ[SECRET]` → `Anthropic API` (WARN)

3.  **Governance Path:**
    `Human Approval` → `ApprovalService.decideApproval` → `LedgerRepo.append` → `Sovereign DB` (SAFE)

4.  **Execution Path:**
    `ExecutionKernel` → `KernelGate` → `BudgetToken` → `PythonRunner` → `Child Process (Clean Env)` (SAFE)

5.  **Audit Integrity Path:**
    `LedgerRepo` → `Sovereign DB` (Trigger Append-Only) → `Immutability` (SAFE)

6.  **Cognitive Bridge Path:**
    `Frontend (CognitivePage)` → `POST /v1/cognitive/query` → `CognitiveEngine` → `MockLLM` (WARN-FALLBACK)

7.  **Resource Control Path:**
    `ExecutionKernel` → `BudgetToken` → `LLM_USAGE_COUNTER` (MISSING - WARN)

8.  **Secret Access Path:**
    `App Start` → `process.env.ANTHROPIC_API_KEY` → `AnthropicProvider` (WARN)

9.  **Data Persistence Path:**
    `Intent Lifecycle` → `IntentService` → `db.transaction` → `Sovereign DB` (SAFE)

10. **Sandbox Violation Detection:**
    `Worker Runner` → `WebAssembly.instantiate` → `Fuel Metering` (GATE 05 PREFLIGHT) (WARN)

---

## 5. RECOMENDAÇÕES PARA GATE 05 (APPROVAL BLOCKED)

1.  **Remediação de Leak de Contexto**: Implementar `ContextTransformer` que converte objetos complexos em resumos estatísticos ou hashes antes de enviar ao LLM.
2.  **Sovereign Reconciliation**: Toda resposta de IA que pretenda descrever o estado do sistema deve ser validada contra um "Receipt of Truth" ( hashes de cells).
3.  **Secret Isolation**: Mover chaves de API para o `SecretManager` (ResistGate) em vez de `process.env` bruto.
4.  **Audit Log for Brain Bridge**: Registrar cada execução do `brain_bridge` com o hash do `target_data` enviado.

---
**VEREDITO FINAL:** O sistema é **SEGURO** no nível de execução (Kernel), mas **VULNERÁVEL** no nível cognitivo (Leak de Contexto). O Gate 05 deve incluir a remediação do `CognitiveEngine` antes de ser certificado.
