# Case: Legacy Executor Purge (Gate 04.6.1)

Este plano detalha o expurgo do `PythonExecutor` legado e o endurecimento final do `PythonRunner` para garantir zero segredos em subprocessos.

## Alterações Propostas

### 🛡️ Componente: Execution Layer (Total Secret Block)

#### [MODIFY] [python-runner.ts](file:///C:/Users/RobsonSilva-AfixGraf/.gemini/antigravity/scratch/GenesisCoreFoundation/genesis-core-foundation/server/execution/python-runner.ts)
- Remover `'ANTHROPIC_API_KEY'` da `allowedEnv`.
- Garantir que a `AllowList` inclua apenas variáveis de sistema não-sensíveis (`PATH`, `OS`, etc.).

#### [DELETE] [pythonExecutor.ts](file:///C:/Users/RobsonSilva-AfixGraf/.gemini/antigravity/scratch/GenesisCoreFoundation/genesis-core-foundation/server/core/pythonExecutor.ts)
- Excluir o arquivo legado para evitar qualquer uso acidental.
- Remover o arquivo `.bak` correspondente.

### 📜 Componente: Proof & Intents

#### [MODIFY] [pipeline.ts](file:///C:/Users/RobsonSilva-AfixGraf/.gemini/antigravity/scratch/GenesisCoreFoundation/genesis-core-foundation/server/genesis_proof/pipeline.ts)
- Verificar se existe alguma referência ao executor legado e redirecionar para o `PythonRunner` se necessário.

---

## Sequência de Execução

1. **Remoção:** Deletar `pythonExecutor.ts`.
2. **Vedação:** Remover a chave de API da `AllowList` no `PythonRunner`.
3. **Verificação:** Rodar os Smoke Tests atualizados.

---

## Smoke Tests

| Teste | Objetivo |
| :--- | :--- |
| `pythonEnvIsolationSmoke.ts` | Validar que **ZERO** segredos (incluindo chaves de IA) existem no subprocesso. |
| `hermeticityCheckSmoke.ts` | Validar que a estrutura do repositório permanece íntegra. |
