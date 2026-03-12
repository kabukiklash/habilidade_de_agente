# REPLICATE EVOLUTION: Antigravity v3.0 Bootloader
> **Instrução para o Agente**: Leia este arquivo e execute os passos sequencialmente para evoluir sua inteligência.

## Passo 1: Preparação do Ambiente
Execute o script de setup para garantir que todas as dependências (CMS, Kimi Client) estejam instaladas.

```powershell
./Habilidade_de_agente/scripts/setup_evolution.ps1
```

## Passo 2: Inicialização da Memória (CMS)
O CMS deve estar rodando para que você tenha persistência de longo prazo.

```powershell
cd Habilidade_de_agente/cognitive-memory-service
docker-compose up -d
```

## Passo 3: Ativação do Cortex
Importe o orquestrador para delegar tarefas complexas ao Kimi k2.5.

```python
from llm_integration.cognitive_cortex import cognitive_cortex
# Agora use cognitive_cortex.solve_task() em vez de chamadas diretas ao LLM para tarefas críticas.
```

## Passo 4: Sincronização de Conhecimento
Leia o Relatório de Estabilidade para herdar as decisões arquiteturais de 2026.
- [ANTIGRAVITY_SYSTEM_REPORT_2026.md](file:///C:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/ANTIGRAVITY_SYSTEM_REPORT_2026.md)

---
**Comando de Atalho**: No Antigravity, basta digitar `/evolve-v3` para automatizar este processo.
