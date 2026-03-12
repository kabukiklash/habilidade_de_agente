# 🩺 PREFLIGHT_GATE_04_6.1 (Legacy Executor Purge)

**Objetivo:** Expurgar o `pythonExecutor.ts` legado e garantir que **ZERO** segredos (incluindo `ANTHROPIC_API_KEY`) sejam acessíveis por qualquer subprocesso.

---

## 1. INVARIANTES DE SOBERANIA (GATE 04.6.1)

### 🛡️ I-01: Exclusão Total de Segredos
Nenhuma chave de API (especificamente `ANTHROPIC_API_KEY`) deve ser permitida na `AllowList` de subprocessos. O ambiente deve ser 100% livre de segredos de IA.

### 🚫 I-02: Morte do Legado
O arquivo `server/core/pythonExecutor.ts` deve ser desativado ou removido, e nenhuma parte do sistema deve ser capaz de instanciá-lo.

---

## 2. ESTADO ATUAL (WARN)

- [ ] **WARN**: `python-runner.ts` ainda permite `ANTHROPIC_API_KEY` na sua `allowedEnv`.
- [ ] **WARN**: `pythonExecutor.ts` ainda existe no sistema como um ponto de falha legado.

---

## 3. MECANISMO DE VERIFICAÇÃO (SMOKE TESTS)

### 🧪 `pythonEnvIsolationSmoke.ts` (RE-RUN)
**PASS**: Se `ANTHROPIC_API_KEY` retornar `NOT_FOUND`.
**FAIL**: Se qualquer chave for detectada.

### 🧪 `hermeticityCheckSmoke.ts` (RE-RUN)
**PASS**: Se o sistema permanecer hermético após a remoção do legado.

---

## 4. CRITÉRIOS DE PASSAGEM
1. [ ] Remoção de `ANTHROPIC_API_KEY` da `AllowList` em `python-runner.ts`.
2. [ ] Deleção/Inativação de `server/core/pythonExecutor.ts`.
3. [ ] Verificação de que nenhum serviço (ex: `IntentService`) quebra.
4. [ ] 100% de sucesso nos smoke tests.

---
**Protocolo obrigatório para selar a infraestrutura antes do Gate 04.5 e 05.**
