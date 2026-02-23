# Plano de Implementação: Evolução "Clawd-Inspired" do Antigravity

Este plano detalha a implementação de novas capacidades de execução, memória e orquestração no Antigravity Kit, inspiradas na análise do projeto Clawdbot.

## User Review Required

> [!IMPORTANT]
> A funcionalidade de **Sandbox** requer que o Docker esteja rodando e que o usuário aceite a criação de containers temporários.
> A função de **Memória Cross-Session** salvará informações estruturadas em `.agent/memory/`. Informe se houver restrições de privacidade para certos dados.

## Proposed Changes

### Componente: Fundação de Memória (Knowledge Vault)

#### [NEW] [knowledge-vault/SKILL.md](file:///c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/.agent/skills/knowledge-vault/SKILL.md)
Define os padrões de armazenamento de memória em JSON/Markdown dentro de `.agent/memory/`.

#### [NEW] [historian.md](file:///c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/.agent/agents/historian.md)
Agente especialista em vasculhar o vault e sintetizar contextos passados para a sessão atual.

---

### Componente: Execução Segura (Sandbox)

#### [NEW] [sandbox-executor/SKILL.md](file:///c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/.agent/skills/sandbox-executor/SKILL.md)
Provê ferramentas para envolver comandos `run_command` em um ambiente Docker `alpine` ou `node:slim`.

#### [NEW] [sandbox_run.py](file:///c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/.agent/skills/sandbox-executor/scripts/sandbox_run.py)
Script Python auxiliar para gerenciar o ciclo de vida do container e extração de logs.

---

### Componente: Interface e Orquestração

#### [NEW] [canvas/SKILL.md](file:///c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/.agent/skills/canvas/SKILL.md)
Gerencia a geração de arquivos HTML dinâmicos para visualização de arquitetura e UI.

#### [NEW] [canvas.md](file:///c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/.agent/workflows/canvas.md)
Workflow para o comando `/canvas`.

#### [NEW] [evolve.md](file:///c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/.agent/workflows/evolve.md)
Workflow para o comando `/evolve`, que automatiza a verificação de novas habilidades.

#### [MODIFY] [ARCHITECTURE.md](file:///c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/.agent/ARCHITECTURE.md)
Atualização do mapa do sistema com os novos componentes.

## Verification Plan

### Automated Tests
- Execução do `sandbox_run.py` com um comando de teste (`echo hello`) para verificar se o Docker responde corretamente.
- Teste de escrita e leitura no `knowledge-vault` via script Python.
- Validação dos schemas dos novos Agentes via linting.

### Manual Verification
- O usuário deve rodar `/evolve` para ver se as novas habilidades são listadas corretamente.
- O usuário deve testar `/canvas` para gerar um diagrama de teste e ver se o arquivo HTML é aberto no browser.
