# Plano de Implementação: Operação Limpeza Estelar 🧹🌟

Este plano detalha a migração de todos os arquivos e pastas "não-core" da raiz para um diretório unificado chamado `WORKSPACE`, mantendo a raiz exclusiva para as 10 Tecnologias Soberanas.

## User Review Required

> [!IMPORTANT]
> Esta operação alterará a estrutura de diretórios raiz. Embora não afete os Masters (Tecnologias 01-10), ferramentas externas ou scripts legados fora das pastas soberanas podem precisar de ajustes de caminho se forem executados manualmente.

## Proposed Changes

### [WORKSPACE]
#### [NEW] [WORKSPACE](file:///c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/WORKSPACE)
Criar a pasta que servirá de "storage" para todo o ecossistema satélite.

---

### [Movimentação de Satélites]
Os seguintes diretórios serão movidos para `WORKSPACE/`:

- `cognitive-memory-service` -> `WORKSPACE/SATELLITES/01_CMS`
- `CONSILIUM_ENGINE` -> `WORKSPACE/SATELLITES/02_CORTEX`
- `moltbot-governed-bridge` -> `WORKSPACE/SATELLITES/07_BRIDGE`
- `investor-dashboard` -> `WORKSPACE/SATELLITES/08_VISUAL`
- `PROJETOS` -> `WORKSPACE/PROJETOS`
- `EVOLUTION_SOVEREIGN_TEMPLATE` -> `WORKSPACE/INFRA/TEMPLATES`
- `QUARENTENA_ANTIGRAVITY` -> `WORKSPACE/INFRA/QUARENTENA`
- `_QUARANTINE_ZOMBIES` -> `WORKSPACE/INFRA/ZOMBIES`
- `scripts` -> `WORKSPACE/INFRA/SCRIPTS_LEGACY`
- `UTILIDADES` -> `WORKSPACE/INFRA/UTILIDADES`
- `tests` & `TESTER` -> `WORKSPACE/DEVELOPMENT/TESTING`
- `examples` -> `WORKSPACE/DEVELOPMENT/EXAMPLES`
- `workspaces` (antigo) -> `WORKSPACE/DEVELOPMENT/LEGACY_WORKSPACES`
- `ops` -> `WORKSPACE/INFRA/OPS`

### [Arquivos Raiz (Files)]
Arquivos soltos na raiz (.py, .md, .db) serão movidos para `WORKSPACE/RAIZ_ARCHIVE/` para limpeza total.

## Verification Plan

### Automated Tests
- Verificar se as 10 pastas Soberanas permanecem na raiz.
- Verificar se o `sys.path` dos Masters continua funcionando (eles usam caminhos absolutos baseados na raiz, então não devem quebrar).

### Manual Verification
- O usuário deve confirmar a limpeza visual da raiz.
