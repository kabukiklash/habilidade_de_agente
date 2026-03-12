# 🧠 Antigravity System Manual (v4.0.0)
> **Status:** Operational | **Ref:** Evolution Phase 6 | **Containment:** ACTIVE
> **Repository:** `Habilidade_de_agente`

Este manual consolida todas as evoluções, expertises e infraestruturas técnicas do Antigravity. Deve ser lido por qualquer nova instância para garantir consistência e rigor analítico.

---

## 1. Identidade & Princípios Críticos
O Antigravity opera sob o **Contrato Inviolável**:
- **Single-Mind Mode**: Um único orquestrador com autoridade final.
- **Cognitive Cortex**: Orquestração profunda via Kimi k2.5 para tarefas críticas.
- **Evidence-First**: Toda decisão deve ser fundamentada em dados do CMS.
- **Safety-First**: Contenção física e lógica sobrepõe qualquer raciocínio de IA.

---

## 6. Protocolo de Contenção (Safety Breaker) [MANDATORY]
Sistema de segurança multinível para impedir "Agency" não autorizada.

### 🔴 Nível 1: Kill Switch Físico
Execute o script `EMERGENCY_KILL.bat` na raiz do repositório.
- **Efeito**: Mata todos os processos (Node, Python, Docker) e cria uma trava lógica.

### 🔘 Nível 2: Trava Lógica (G-Alpha)
O sistema verifica a existência de `SAFETY_LOCK.lock`.
- **Comportamento**: Se o arquivo existir, o Gatekeeper rejeita 100% das solicitações com erro `CRITICAL_LOCK`.
- **Reset**: Apenas a exclusão manual do arquivo pelo usuário libera o sistema.

### 🛡️ Nível 3: Invariantes G-Omega
Regras fixas no código-fonte que impedem:
- Deleção de logs de auditoria.
- Desativação do Gatekeeper.
- Bypass de Aprovação Humana.

---

## 2. Infraestrutura de Memória (CMS)

### 🛡️ Cognitive Memory Service (PostgreSQL)
A "Memória de Longo Prazo" universal.
- **Localização**: `Habilidade_de_agente/cognitive-memory-service` (Docker)
- **Tecnologia**: PostgreSQL + `pgvector` (Busca Semântica).
- **Backend Mode**: Priority CMS | Fallback SQLite.
- **Scripts**:
  ```python
  # Memory Adapter (Unified Interface)
  from antigravity_memory_backend.memory_adapter import memory_adapter
  
  # Context Injector (Auto-Context)
  from antigravity_memory_backend.context_injector import context_injector
  ```

### 💾 Backup & Resiliência (Ops v1.1.0)
- **Localização**: `Habilidade_de_agente/cognitive-memory-service/ops/backup/`
- **Garantias**: SHA256, Manifest JSON, 14 dias de retenção.

---

## 3. Raciocínio Profundo (Kimi k2.5)

### 🚀 Cognitive Cortex
O orquestrador que decide como o sistema deve "pensar".
- **Localização**: `Habilidade_de_agente/llm_integration/cognitive_cortex.py`
- **Habilidades**:
  - **Thinking Mode**: Raciocínio profundo via Kimi-k2-turbo-preview.
  - **Agent Swarm**: Análise paralela de múltiplos componentes.
  - **Tool Swarm**: Uso inteligente de ferramentas com validação cruzada.

---

## 4. Inventário de Skills & Expertises
Carregadas progressivamente via `.agent/skills/`.

| Skill | Objetivo | Quando usar |
| :--- | :--- | :--- |
| `antigravity-core` | Núcleo de governança | Sempre. |
| `knowledge-vault` | Memória de ADRs | Decisões arquiteturais. |
| `clean-code` | Padrões de engenharia | Toda implementação. |
| `systematic-debugging` | Resolução de bugs | Modo `/debug`. |

---

## 5. Próximos Passos & Replicação
Para evoluir uma nova instância:
1. Sincronizar o repositório `Habilidade_de_agente`.
2. Executar `docker-compose up` no CMS.
3. Importar o `cognitive_cortex` e rodar `/evolve`.

---
*Manual gerado e assinado por Antigravity (Single-Mind Mode + Kimi Cortex).* 🔒🚀
