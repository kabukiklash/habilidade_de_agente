# implementation_plan_gate_06.md (Sovereign Data Unification)

Este plano detalha a migração técnica do estado legado para a infraestrutura unificada do Drizzle.

## Proposed Changes

### [Component: Database Schema]

#### [MODIFY] [schema.ts](file:///C:/Users/RobsonSilva-AfixGraf/.gemini/antigravity/scratch/GenesisCoreFoundation/genesis-core-foundation/server/db/schema.ts)
- Adicionar tabelas: `decision_proposals`, `approvals`, `execution_plans`, `execution_results`.
- Garantir relações de Foreign Key entre as novas tabelas.

### [Component: Kernel & Services]

#### [MODIFY] [execution-kernel.ts](file:///C:/Users/RobsonSilva-AfixGraf/.gemini/antigravity/scratch/GenesisCoreFoundation/genesis-core-foundation/server/execution/execution-kernel.ts)
- Remover dependência de `../db.js` e `prepareStatements`.
- Migrar métodos `executeApprovedProposal` e `executeCell` para usar o `db` do Drizzle.

#### [MODIFY] [repository.ts](file:///C:/Users/RobsonSilva-AfixGraf/.gemini/antigravity/scratch/GenesisCoreFoundation/genesis-core-foundation/server/db/repository.ts)
- Adicionar métodos utilitários para busca e inserção de propostas e planos.

### [Component: Cleanup]

#### [DELETE] [db.ts](file:///C:/Users/RobsonSilva-AfixGraf/.gemini/antigravity/scratch/GenesisCoreFoundation/genesis-core-foundation/server/db.ts)
- Eliminar o adaptador legacy.

#### [DELETE] genesis.db
- Remoção física do arquivo `server/genesis.db`.

## Verification Plan

### Smoke Tests
- `npx tsx tests/smoke/sovereignPersistenceSmoke.ts`: Validar fluxo completo (Intent -> Proposal -> Execution) em um único banco.
- `ls server/genesis.db`: Verificar erro de "File not found".

### Automated Audit
- Executar `check_schema.ts` para validar integridade das tabelas Drizzle.
