# 🩺 PREFLIGHT_GATE_04_6 (Infra Hardening: Secrets + Hermeticity)

**Objetivo:** Eliminar o vazamento de segredos para subprocessos e garantir que o núcleo do repositório seja hermético, removendo dependências de diretórios externos.

---

## 1. INVARIANTES DE INFRAESTRUTURA (GATE 04.6)

### 🛡️ I-01: Isolamento de Segredos (Secret Isolation)
É terminantemente proibido passar o objeto `process.env` bruto para qualquer subprocesso (Python, Node Workers, Shell). O ambiente do processo filho deve ser construído do zero usando uma `AllowList` estrita.

### 📦 I-02: Hermeticidade do Repositório (Zero-External-Dependency)
O repositório `genesis-core-foundation` deve ser auto-contido. É proibido o uso de imports que subam para diretórios pai (`../`) para acessar lógica de negócio ou provedores. Toda dependência externa deve ser internalizada.

---

## 2. ESTADO ATUAL (FAILED AUDIT)

- [ ] **FAIL**: `python-runner.ts` e `pythonExecutor.ts` passam `process.env` completo para o sandbox Python.
- [ ] **FAIL**: `brain_bridge.py` depende da pasta `llm_integration` localizada fora da raiz do repositório.
- [ ] **FAIL**: Ausência de testes automatizados que validem o isolamento de variáveis de ambiente.

---

## 3. MECANISMO DE VERIFICAÇÃO (SMOKE TESTS)

### 🧪 `pythonEnvIsolationSmoke.ts`
Tenta ler a `ANTHROPIC_API_KEY` de dentro do sandbox Python.
**PASS**: Se a chave não for encontrada ou estiver vazia.
**FAIL**: Se a chave (ou qualquer segredo do host) estiver visível.

### 🧪 `hermeticityCheckSmoke.ts`
Verifica a árvore de imports e caminhos de arquivos.
**PASS**: Se todos os arquivos e dependências estiverem abaixo da raiz (`./`).
**FAIL**: Se houver referências a scripts ou módulos em `../`.

---

## 4. CRITÉRIOS DE PASSAGEM (MINIMUM PASSING CRITERIA)
1. [ ] Refatoração do `PythonRunner` e `PythonExecutor` com `env` restrictivo.
2. [ ] Migração/Internalização da biblioteca `llm_integration`.
3. [ ] Atualização dos paths no `brain_bridge.py`.
4. [ ] 100% de sucesso nos smoke tests de infraestrutura.

---
**Protocolo obrigatório para garantir a integridade do Gate 05.**
