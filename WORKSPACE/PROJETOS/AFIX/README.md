# Afix — Plataforma de Gestão Inteligente de Atendimento via WhatsApp

> Parceira Oficial Meta (WhatsApp Business API) | Clean Architecture | ISO 25010 Compliant | White-Label

## 📋 Visão Geral

Plataforma SaaS multi-tenant de gestão inteligente de atendimento via WhatsApp, com IA preditiva exclusiva (função "Afix") com 95% de precisão em análise comportamental, atendimento automatizado humanizado e gestão completa do ciclo de vida do cliente.

## 📁 Documentação

| Documento | Descrição |
|-----------|-----------|
| [PADRAO_CRIACAO_PLATAFORMA.md](./docs/PADRAO_CRIACAO_PLATAFORMA.md) | **Padrão de Processo** — Guia para criação de plataformas (usar para construir AFIX) |
| [MANIFESTO_APLICACAO_ISO_25010.md](./docs/MANIFESTO_APLICACAO_ISO_25010.md) | **Manifesto de Aplicação** — Declaração formal de conformidade com ISO/IEC 25010:2023 |
| [ESPECIFICACAO_SISTEMA.md](./docs/ESPECIFICACAO_SISTEMA.md) | Especificação completa dos 12 módulos funcionais |

## 🎯 Módulos Principais

1. **Análise Preditiva (IA Afix)** — Predição de insatisfação, padrões de compra, Afix Score
2. **Atendimento Automatizado** — IA humanizada, handoff humano, integração WhatsApp Business API
3. **Gestão de Leads & CRM** — Kanban visual, jornada do cliente, classificação por IA
4. **Automações Inteligentes** — Builder visual tipo Zapier/IFTTT
5. **Afix Oficial Meta** — Integração certificada, anti-banimento, múltiplos números
6. **Afix Copilot** — Sugestão de respostas, gatilhos de vendas, aprendizado contínuo
7. **Relatórios e Dashboards** — WebSocket em tempo real, templates ISO
8. **Agendamento de Mensagens** — Fila inteligente, lembretes automáticos
9. **Chat Interno** — Comunicação de equipes separada do WhatsApp
10. **Abertura de Chamados** — Ticketing com SLA e escalonamento
11. **Campanhas** — Segmentação, broadcast, métricas
12. **Relacionamento com Cliente** — Surveys, aniversários, programa de fidelidade

## 🚀 Como Executar

```bash
# Instalar dependências
npm install

# Desenvolvimento (backend + frontend)
npm run dev
```

- **Frontend:** http://localhost:5174
- **Backend API:** http://localhost:3002
- **Health check:** http://localhost:3002/health

### Docker (PostgreSQL + Redis)

O backend usa PostgreSQL. Suba os serviços antes de rodar:

```bash
npm run docker:up
```

Depois inicie o backend: `npm run dev:backend`

## 🏛️ Arquitetura

- **Frontend:** React 18+ | TypeScript 5+ | FSD (Feature-Sliced Design) | Clean Architecture
- **Backend:** Node.js/NestJS | PostgreSQL | Redis | RabbitMQ/Kafka
- **IA/ML:** Python/FastAPI | Modelos preditivos próprios (GDPR/LGPD compliant)

### Estrutura do Monorepo

```
AFIX/
├── apps/
│   ├── frontend/     # React + Vite + FSD
│   └── backend/      # NestJS + TypeScript
├── packages/
│   └── shared/       # Entidades e tipos (Lead, Conversa, etc.)
└── docs/             # Documentação
```

## 📜 Conformidade

- **ISO/IEC 25010:2023** — Qualidade de software
- **ISO 27001** — Segurança da informação
- **LGPD/GDPR** — Privacidade de dados
- **WCAG 2.1 AA** — Acessibilidade

---

*Projeto Afix — Habilidade de Agente | 2026*
