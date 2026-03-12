# Plano de Reorganização: Fase 1 (Quarentena)

Mover arquivos de documentação, planos e relatórios históricos para uma pasta isolada para reduzir ruído visual na raiz.

## User Review Required

> [!IMPORTANT]
> Apenas arquivos de DOCUMENTAÇÃO e PLANOS serão movidos nesta etapa. Código ativo e configurações de sistema (.env, tsconfig, etc.) permanecerão na raiz até a próxima fase de organização de Backend/Frontend.

## Proposed Changes

### [QUARENTENA_ANTIGRAVITY]
- **Objetivo**: Repositor de planos de "Desejo" vs "Realidade".
- **Ação**: Criar pasta e mover arquivos soltos.

#### Arquivos para Quarentena (Raiz):
- `ACE_PLAN.md`
- `ANTIGRAVITY_CAPABILITY_REPORT.md`
- `ANTIGRAVITY_EVOLUTION.md`
- `ANTIGRAVITY_EVOLUTION_BIBLE.md`
- `ANTIGRAVITY_MANUAL.md`
- `ANTIGRAVITY_MASTER_INVENTORY.md`
- `ANTIGRAVITY_SOVEREIGN_CAPABILITY_MAP.md`
- `ANTIGRAVITY_SYSTEM_REPORT_2026.md`
- `CodeForge_Manifesto_Fundador_CleanArch-8.txt`
- `CodeForge_Manifesto_Fundador_CleanArch.docx`
- `NEURO_FLOW_Requirements_Ledger.md`
- `RELATORIO_CIRCUIT_BREAKER_V2.md`
- `REPLICATE_EVOLUTION.md`
- `REPLICATION.md`
- `SAR_CIRCUIT_BREAKER_V3.md`
- `SECURITY_AUDIT.md`

## Verification Plan

### Automated Tests
1. **Baseline**: Rodar `python verify_fixes_final.py` antes de mover.
2. **Post-Move**: Rodar `python verify_fixes_final.py` após a movimentação.
3. **Health Check**: `curl http://localhost:8000/health` (se o CMS estiver rodando).
