# Especificação do Sistema Afix

## Sistema de Gestão de Atendimento WhatsApp com IA Preditiva

**Arquitetura Clean Architecture | ISO 25010 Compliant | Frontend Totalmente Personalizável**

---

## 📋 Visão Geral do Sistema

Plataforma SaaS multi-tenant de gestão inteligente de atendimento via WhatsApp, denominada **"Afix"**, posicionada como Parceira Oficial Meta (WhatsApp Business API). O sistema atende requisitos enterprise com arquitetura limpa (Clean Architecture), conformidade total com ISO/IEC 25010:2023, e capacidade de personalização white-label para qualquer empresa.

A plataforma integra IA exclusiva preditiva (função "Afix") com 95% de precisão em análise comportamental, atendimento automatizado humanizado e gestão completa do ciclo de vida do cliente (CRM, funil de vendas, automações).

---

## 🎯 Requisitos Funcionais por Módulo

### 1. MÓDULO: ANÁLISE PREDITIVA DE ATENDIMENTO (IA AFIX)

| Componente | Descrição Técnica | Requisito ISO 25010 |
|------------|-------------------|---------------------|
| Predição de Insatisfação | Algoritmo de ML/NLP processando sentiment analysis em tempo real nas conversas WhatsApp | Functional Suitability, Performance Efficiency |
| Padrões de Compra | Modelo preditivo identificando intenção de compra através de análise de histórico e comportamento conversacional | Functional Correctness |
| Precisão 95% | Métrica obrigatória de acurácia do modelo, com feedback loop para retraining contínuo | Reliability, Maintainability |
| Afix Score | Índice numérico 0-100 de propensão à conversão/insatisfação por cliente | Usability (appropriateness recognizability) |

**Requisitos Técnicos Específicos:**
- Processamento de linguagem natural (NLP) em português, inglês e espanhol
- Latência máxima de 500ms para análise preditiva por mensagem
- Modelo treinado com dados próprios da plataforma (GDPR/LGPD compliant)
- API interna para consumo das predições por outros módulos

---

### 2. MÓDULO: ATENDIMENTO AUTOMATIZADO

| Componente | Descrição Técnica | Requisito ISO |
|------------|-------------------|---------------|
| IA Humanizada | GPT-4/Claude fine-tuned com tom de voz configurável por empresa | Functional Suitability |
| Compreensão Contextual | Manutenção de contexto conversacional por até 30 dias | Reliability |
| Handoff Humano | Transferência automática para atendente humano baseada em gatilhos de complexidade ou solicitação | Operability |
| Treinamento por Empresa | Sistema de fine-tuning com base em conversas históricas aprovadas da empresa cliente | Modifiability |

**Integração WhatsApp Business API (Meta Oficial):**
- Webhooks para recebimento de mensagens em tempo real
- Templates de mensagem aprovados pré-cadastrados
- Gerenciamento de opt-in/opt-out automático
- Rate limiting e filas de mensagens por número comercial

---

### 3. MÓDULO: GESTÃO DE LEADS & FUNIL DE VENDAS (CRM VISUAL)

| Componente | Descrição Técnica | Requisito ISO |
|------------|-------------------|---------------|
| Kanban Visual | Interface drag-and-drop de estágios do funil personalizáveis por empresa | Usability (learnability, operability) |
| Jornada do Cliente | Timeline visual de todos os touchpoints (WhatsApp, email, telefone) | Functional Completeness |
| Classificação de Oportunidades | Tags, scoring e priorização automática baseada na IA Afix | Functional Appropriateness |
| Acompanhamento de Valores | Campos monetários com multi-moeda e projeção de receita | Functional Correctness |

**Estrutura de Dados:**
- **Lead:** id, nome, telefone, email, origem, tags[], score, estágio_funil, valor_potencial, responsavel_id, empresa_id, created_at, updated_at
- **EstagioFunil:** id, nome, ordem, cor, empresa_id, probabilidade_conversao
- **Atividade:** id, lead_id, tipo, descricao, data_agendada, status, created_by

---

### 4. MÓDULO: AUTOMAÇÕES INTELIGENTES

| Componente | Descrição Técnica | Requisito ISO |
|------------|-------------------|---------------|
| Builder de Fluxos | Interface visual tipo "Zapier/IFTTT" para criação de automações | Usability (user assistance) |
| Gatilhos | Eventos: mensagem recebida, lead criado, estágio alterado, tempo sem interação, aniversário | Functional Completeness |
| Condições | Regras IF/ELSE baseadas em dados do lead, comportamento ou predições IA | Functional Correctness |
| Ações | Enviar mensagem, mover kanban, criar tarefa, notificar, agendar, taggear | Functional Appropriateness |

**Motor de Automação:**
- Engine de processamento de eventos assíncrono (CQRS/Event Sourcing)
- Fila de execução com retry policy e dead letter queue
- Logs completos de execução para auditoria

---

### 5–12. Demais Módulos

*(Afix Oficial Meta, Copilot, Relatórios, Agendamento, Chat Interno, Chamados, Campanhas, Relacionamento)*

*Ver documento completo de requisitos para detalhamento de cada módulo.*

---

## 🏛️ Arquitetura Técnica: Clean Architecture + FSD

```
src/
├── app/                    # Composition root, providers, routing
├── processes/              # Fluxos cross-page
├── pages/                  # Route-level pages (views)
├── widgets/                # Blocos UI compostos
├── features/               # Casos de uso e UI bindings
├── entities/               # Domain models, regras de negócio
└── shared/                 # UI kit, utilities, API clients
```

**Regra de Dependência:** Dependências apontam sempre para dentro (domain → use cases → adapters → frameworks)

---

## 🎨 Personalização White-Label

Sistema de temas dinâmicos com `EmpresaTheme` configurável:
- Identidade visual (cores, logo, tipografia)
- Layout (densidade, sidebar, border-radius)
- Componentes (botões, cards, tabelas)
- Módulos ativos e features de IA
- Nomenclaturas customizadas (lead, atendente, funil)

---

## 🔧 Stack Tecnológico Recomendado

**Frontend:** React 18+ | TypeScript 5+ | Zustand + React Query | Radix UI | Recharts | Vite | Vitest + Playwright

**Backend:** Node.js/NestJS ou Go | PostgreSQL | Redis | ClickHouse | RabbitMQ/Kafka | Python/FastAPI (IA)

---

## ⚠️ Restrições e Diretrizes

- ❌ NÃO usar jQuery ou bibliotecas legadas
- ❌ NÃO armazenar tokens no localStorage (usar httpOnly cookies)
- ✅ SEMPRE validar inputs no frontend E backend
- ✅ SEMPRE usar loading states e skeleton screens
- ❌ NUNCA expor dados de outros tenants na UI
- ✅ OBRIGATÓRIO logging de ações para auditoria

---

*Documento de referência para o Manifesto de Aplicação ISO 25010 — Afix Platform*
