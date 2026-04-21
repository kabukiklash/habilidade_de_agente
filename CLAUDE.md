# Habilidade_de_agente — Instruções para o Claude Code

## Cognitive Kit: Carregar no Início de Cada Sessão

**OBRIGATÓRIO:** Ao iniciar qualquer sessão neste projeto, executar imediatamente:

```bash
python C:/Users/RobsonSilva-AfixGraf/claude-cognitive-kit/claude_kit_loader.py "C:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente"
```

### Palavra-Chave de Despertar: `ANTIGRAVITY_WAKE`
Ao receber este comando, o agente deve:
1. Validar se o CMS está online em `localhost:8090`.
2. Ler os resultados de `antigravity_diagnostic.py`.
3. Assumir que a infraestrutura está ativa e pronta para comandos de alto nível.

Isso carrega:
- Memórias persistidas do projeto
- Decisões anteriores aprovadas e rejeitadas (não repetir as rejeitadas)
- Estrutura de arquivos cacheada
- Histórico de consumo de tokens
- Mapa de entidades do codebase

## Sobre este Projeto

Este projeto contém um Sistema de IA Soberana chamado **Antigravity**, composto por 10 tecnologias numeradas (01 a 10):

| Pasta | Tecnologia | Função |
|---|---|---|
| `01_COGNITIVE_MEMORY_SERVICE` | CMS | Memória persistente com ledger imutável |
| `02_COGNITIVE_CORTEX` | Cortex | Orquestrador central |
| `03_CIRCUIT_BREAKER_V3` | Breaker | Proteção fail-closed |
| `04_KNOWLEDGE_GRAPH` | Graph | Extração semântica |
| `05_VIBECODE_G7` | VibeCode | Verificação formal de código |
| `06_AUDIT_MONITOR_LEDGER` | Audit | Trilha forense imutável |
| `07_KIMI_MEMORY_BRIDGE` | Bridge | Interface multi-LLM |
| `08_VISUAL_INTELLIGENCE` | UI | Dashboard em tempo real |
| `09_SOVEREIGN_SKILLS_ORCHESTRATION` | Governor | Governança de plugins |
| `10_SOVEREIGN_OPERATIONS` | Ops | Infraestrutura e boot |

## MCP Server (`antigravity-mcp-server/`)

Servidor MCP TypeScript com 8 tools operacionais:

| Tool | Função | Depende CMS? |
|---|---|---|
| `read_file_smart` | Leitura comprimida de arquivos grandes (30-60% economia) | Não |
| `route_llm` | Roteamento multi-LLM (OpenAI, Inception, Pollinations + fallback) | Não |
| `session_report` | Relatório de tokens e eficiência | Não |
| `search_memory` | Busca semântica na memória CMS | Sim |
| `store_memory` | Persistência de conhecimento | Sim |
| `log_decision` | Registro de decisões arquiteturais | Sim |
| `store_event` | Registro de eventos de sistema | Sim |
| `log_response` | Registro de consumo de tokens | Sim |

**CMS roda em `localhost:8090`** — header: `X-ACE-API-KEY`

### LLM Router — Strategies

| Strategy | Provider primário | Uso |
|---|---|---|
| `fast` | Pollinations (gratuito) | Tarefas simples, rascunhos |
| `balanced` | OpenAI (gpt-4o-mini) | Dia-a-dia, custo-benefício |
| `quality` | Inception (mercury-2) | Qualidade máxima |

## Regras Importantes

- **NÃO modificar** os arquivos das pastas 01-10 sem autorização explícita — pertencem a outra plataforma
- Os arquivos `*_master.py` são produção — só leitura
- Novos desenvolvimentos vão em pastas separadas
- Usar o Cognitive Kit para registrar decisões e memórias
- **`.mcp.json` contém API keys** — nunca commitar (já no `.gitignore`)

## Salvar Memória após Cada Sessão Importante

```bash
python C:/Users/RobsonSilva-AfixGraf/claude-cognitive-kit/claude_kit_loader.py "C:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente" --save "<topic>" "<content>"
```

## Varredura Completa (1x por semana ou após grandes mudanças)

```bash
python C:/Users/RobsonSilva-AfixGraf/claude-cognitive-kit/claude_kit_loader.py "C:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente" --full
```

## Prioridades do Proprietario (Robson)

- **Arquitetura**: Decisoes solidas, bem pensadas e escalaveis — pensar antes de construir
- **Engenharia**: Codigo de qualidade, limpo, testavel e mantivel
- **Seguranca**: Seguranca em primeiro lugar — RLS, validacao, sanitizacao, sem vulnerabilidades OWASP
- **Valores Anthropic**: Clareza, confiabilidade, responsabilidade, transparencia nas decisoes

> Entrega solida > velocidade. Tamojunto.
