# Antigravity Context Engine (ACE) - Plano de Implementação

## 1. Visão Geral (O que é o ACE?)
O **Antigravity Context Engine (ACE)** é um serviço em background (daemon) rodando localmente na máquina do desenvolvedor. Ele atua como uma "ponte cognitiva" entre o **CMS (Cognitive Memory Service)** e qualquer IDE baseada em IA (como Cursor, VS Code via Cline/Roo Code, etc).

**Objetivo Principal:** Fornecer contexto arquitetural dinâmico e preciso para a IDE no momento da codificação, e capturar os "aprendizados táticos" gerados pela IA local para transformá-los em memória de longo prazo no CMS.

---

## 2. Arquitetura do Sistema

A arquitetura do ACE é dividida em 3 pilares fundamentais, garantindo total desacoplamento:

1. **O Motor de Eventos (Daemon):** Monitora o sistema de arquivos aguardando mudanças (salvamentos) e organiza a fila de processamento térmico (evitando gargalos de CPU).
2. **A Ponte do CMS (Cérebro):** Lê e escreve na base SQLite oficial do projeto `Habilidade_de_agente`, garantindo que o Manifesto do Fundador e as Regras Arquiteturais sejam respeitadas.
3. **Os Adaptadores (IDE Adapters):** O componente de "entrega". Formata e cospe o conhecimento gerado no padrão exigido por cada IDE (ex: `.cursorrules` ou `.clinerules`).

---

## 3. Fases de Implementação (Passo a Passo)

### Fase 1: O Coração do Sistema (Daemon e Eventos)
Nesta fase inicial, garantimos que o ACE "enxergue" o projeto sem consumir recursos excessivos da máquina.

- [ ] **Criar `ace_daemon.py`:** Um script Python utilizando a biblioteca `watchdog` para monitorar a pasta do projeto.
- [ ] **Configurar Filtros de Monitoramento:** Ignorar subpastas pesadas/irrelevantes como `node_modules`, `.git`, `.venv` e `.cursor`.
- [ ] **Implementar Fila de *Debounce*:** Criar um mecanismo temporal (ex: 5 segundos) que agrupa múltiplos saves do mesmo arquivo em um único evento analítico.

### Fase 2: O Cérebro (Integração de Leitura/Escrita com o CMS)
A fase responsável por conectar o serviço de eventos aos bancos de dados SQLite do CMS.

- [ ] **Criar a classe `CMSKnowledgeBridge`:** Responsável por conectar via Python ao banco local do CMS.
- [ ] **Serviço de Extração (Leitura):** Capacidade de buscar as Regras de Negócio e o Manifesto do Fundador no banco mediante solicitação.
- [ ] **Serviço Digestor (Escrita):** Criação do Scratchpad do Cursor (`.cursor/aprendizados_brutos.md`). Quando este arquivo for modificado, invocar o LLM local (Cortex/Kimi) para formatar o texto bruto em JSON rigoroso e persistir essa nova inteligência na tabela de memórias do CMS, apagando o arquivo em seguida.

### Fase 3: As Entregas Universais (Adapters para IDEs)
Nesta fase, a inteligência extraída do CMS é entregue exatamente onde o Cursor (ou o VS Code) consegue ler nativamente.

- [ ] **Criar `CursorAdapter`:** Sempre que um arquivo principal do projeto for modificado, este adapter pede um contexto ao CMS e gera/atualiza um arquivo em `.cursor/rules/dynamic_context.mdc`.
- [ ] **Criar `VSCodeAdapter`:** Faz a mesma operação estrutural do CursorAdapter, porém despejando a saída em `.clinerules` ou num arquivo `prompt_instructions.md` designado.

### Fase 4: O Arsenal de Habilidades (As Skills Iniciais)
Plugins ativos agregados ao pacote para conferir "superpoderes" à IDE.

- [x] **Context-Weaver (Tecelão de Contexto):** A habilidade basal que lê o arquivo em edição e pesquisa vetorialmente no CMS apenas a arquitetura relacionada àquele tema, mantendo o `.cursorrules` sempre dinâmico, limpo e enxuto.
- [x] **Pattern-Enforcer (Árbitro de Arquitetura):** Hook de `git pre-commit` que intercepta códigos antes de irem pro versionamento, compara as decisões com o CMS e barra commits que violam as regras arquiteturais.

---

## 4. Regras de Segurança e Invariantes

- **Isolamento Absoluto (Zero Contaminação):** A IDE NUNCA terá acesso direto ao banco SQLite do CMS. Todo o tráfego de conhecimento passa pelas strings e formatações do ACE.
- **Local First:** Operação 100% confinada na máquina local.
- **Modularidade Universal:** O pacote pode ser instalado e operado independente da IDE, funcionando como um processo fantasma no OS.

---
> Aguardando aprovação ou ajustes para iniciar o "Passo 1.1" da Fase 1.
