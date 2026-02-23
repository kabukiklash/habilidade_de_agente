# Case: Infra Hardening (Gate 04.6)

Este plano detalha a sequência de execução para isolar segredos e garantir a hermeticidade do repositório antes da implementação da Sandbox WASM (Gate 05).

## Alterações Propostas

### 🛡️ Componente: Execution Layer (Secret Isolation)

#### [MODIFY] [python-runner.ts](file:///C:/Users/RobsonSilva-AfixGraf/.gemini/antigravity/scratch/GenesisCoreFoundation/genesis-core-foundation/server/execution/python-runner.ts)
- Definir `SANDBOX_ENV_ALLOWLIST = ['PATH', 'PYTHONPATH', 'PYTHONDONTWRITEBYTECODE']`.
- No método `spawnWithSafety`, substituir `env: { ...process.env, ... }` por um filtro que inclua apenas as chaves autorizadas.

#### [MODIFY] [pythonExecutor.ts](file:///C:/Users/RobsonSilva-AfixGraf/.gemini/antigravity/scratch/GenesisCoreFoundation/genesis-core-foundation/server/core/pythonExecutor.ts)
- Aplicar o mesmo filtro de `env` preventivamente.

### 📦 Componente: LLM Architecture (Hermeticity)

#### [INTERNALIZE] `llm_integration/`
- Copiar o conteúdo de `c:\Users\RobsonSilva-AfixGraf\Habilidade_de_agente\llm_integration\` para `C:\Users\RobsonSilva-AfixGraf\.gemini\antigravity\scratch\GenesisCoreFoundation\genesis-core-foundation\server\llm\power_kit\llm_integration\`.
- Deletar referências externas.

#### [MODIFY] [brain_bridge.py](file:///C:/Users/RobsonSilva-AfixGraf/.gemini/antigravity/scratch/GenesisCoreFoundation/genesis-core-foundation/server/llm/power_kit/brain_bridge.py)
- Alterar `from llm_integration import ...` para os caminhos relativos internos.

---

## Sequência de Execução

1. **Internalização:** Mover arquivos e ajustar imports do Python.
2. **Hardening:** Refatorar runners TS para restringir `env`.
3. **Verificação:** Executar smoke tests de isolamento e integridade.

---

## Smoke Tests

| Teste | Objetivo |
| :--- | :--- |
| `pythonEnvIsolationSmoke.ts` | Validar que segredos do host são invisíveis no sandbox. |
| `hermeticityCheckSmoke.ts` | Validar que não existem dependências de arquivos externos (`../`). |
