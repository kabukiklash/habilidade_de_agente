# Padrão de Criação de Plataforma

## Guia para Desenvolvimento de Plataformas Complexas com IA

**Versão**: 1.0  
**Data**: Março 2026  
**Aplicável a**: AFIX e futuras plataformas enterprise

---

## 1. PROPÓSITO

Este documento define o **padrão de processo** para criação de plataformas de software complexas, incorporando:

- Filosofia **Design-First, Code-Last**
- Manifesto como **fonte única de verdade**
- **Validação com usuários e stakeholders** antes de congelar escopo
- Suporte a **multi-stack** (Node.js, Python, Go, etc.)
- Integração com **conformidade** (ISO 25010, LGPD, GDPR)
- **Flexibilidade controlada** no manifesto (revisões documentadas)
- **Revisão de segurança** explícita

---

## 2. PRINCÍPIOS FUNDAMENTAIS

| Princípio | Descrição |
|-----------|-----------|
| **Manifesto como Verdade** | Todas as decisões documentadas. Antes de cada ação, consultar o manifesto. |
| **Design-First, Code-Last** | Arquitetura e planejamento completos antes de gerar código. |
| **Rastreabilidade** | Cada decisão com alternativas consideradas e justificativa. |
| **Validação Humana** | IA sugere; humano valida decisões críticas de arquitetura e negócio. |
| **Validação com Usuário** | Validar com stakeholders/usuários reais antes de congelar manifesto. |
| **Conformidade desde o Início** | ISO 25010, LGPD, GDPR considerados na fase de design. |
| **Flexibilidade Controlada** | Manifesto pode ser revisado com processo documentado; não é rígido demais. |
| **Validação em Checkpoints** | Em cada fase, validar contra manifesto e corrigir desvios. |

---

## 3. FLUXO GERAL: 10 FASES

O processo é dividido em **10 fases** (evolução do 9-sprint original):

```
┌─────────────────────────────────────────────────────────────────────────┐
│  FASE 0: KICKOFF          │  Definição inicial, stakeholders, escopo     │
├─────────────────────────────────────────────────────────────────────────┤
│  FASES 1-2: PESQUISA      │  Domínio, requisitos, validação com usuário │
├─────────────────────────────────────────────────────────────────────────┤
│  FASES 3-4: DESIGN        │  Manifesto, arquitetura, conformidade       │
├─────────────────────────────────────────────────────────────────────────┤
│  FASES 5-7: IMPLEMENTAÇÃO │  Diagramas, código, ambiente               │
├─────────────────────────────────────────────────────────────────────────┤
│  FASES 8-9: VALIDAÇÃO     │  Testes, segurança, deploy                  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. DETALHAMENTO DAS FASES

### Fase 0: Kickoff e Alinhamento (1 dia)

**Objetivo**: Alinhar expectativas e definir escopo inicial.

**Atividades**:
- Identificar stakeholders e responsáveis
- Definir objetivos de negócio e sucesso
- Mapear requisitos de conformidade (ISO, LGPD, etc.)
- Definir stack preferencial (ou deixar para Fase 1)
- Criar documento de visão inicial

**Deliverables**:
- [ ] Documento de Kickoff
- [ ] Lista de stakeholders
- [ ] Requisitos de conformidade
- [ ] Escopo inicial (o que está dentro/fora)

**Validação**: Aprovação dos stakeholders no escopo.

---

### Fase 1: Pesquisa e Análise de Domínio (2-3 dias)

**Objetivo**: Entender profundamente o problema e o domínio.

**Atividades**:
- Pesquisar melhores práticas no domínio
- Identificar padrões e anti-patterns
- Avaliar tecnologias (multi-stack: Node, Python, Go, etc.)
- Documentar requisitos funcionais e não-funcionais
- Mapear integrações externas obrigatórias

**Deliverables**:
- [ ] Documento de pesquisa
- [ ] Matriz de tecnologias recomendadas
- [ ] Lista de requisitos priorizados
- [ ] Riscos e dependências identificados

---

### Fase 2: Validação com Usuários e Stakeholders (1-2 dias)

**Objetivo**: Validar requisitos com quem vai usar o sistema.

**Atividades**:
- Apresentar pesquisa e requisitos iniciais
- Coletar feedback (entrevistas, workshops, surveys)
- Priorizar funcionalidades com base em valor real
- Identificar gaps e ambiguidades
- Ajustar escopo conforme feedback

**Deliverables**:
- [ ] Registro de validação com usuários
- [ ] Requisitos priorizados e validados
- [ ] Lista de dúvidas resolvidas
- [ ] Aprovação para prosseguir ao design

**Validação**: Stakeholders aprovam que requisitos refletem necessidades reais.

---

### Fase 3: Arquitetura de Alto Nível (2-3 dias)

**Objetivo**: Definir estrutura geral do sistema.

**Atividades**:
- Criar diagramas C4 (Context, Container, Component)
- Definir módulos principais e responsabilidades
- Especificar comunicação entre módulos (REST, gRPC, eventos)
- Documentar decisões arquiteturais com justificativas
- Considerar multi-tenant, escalabilidade, isolamento

**Deliverables**:
- [ ] Diagramas C4
- [ ] Documento de arquitetura
- [ ] Matriz de decisões (decisão | alternativas | justificativa)
- [ ] Diagrama ER preliminar

---

### Fase 4: Manifesto e Conformidade (2-3 dias)

**Objetivo**: Criar documento único de verdade e validar conformidade.

**Atividades**:
- Gerar manifesto completo (usar template ou MANIFESTO_APLICACAO_ISO_25010)
- Documentar todas as decisões com justificativas
- Validar contra requisitos de conformidade (ISO 25010, LGPD)
- **Congelar manifesto** (ou marcar como "Aprovado para Desenvolvimento")
- Definir processo de revisão do manifesto (quando e como alterar)

**Deliverables**:
- [ ] Manifesto completo e aprovado
- [ ] Histórico de decisões
- [ ] Checklist de conformidade preenchido
- [ ] Definição de processo de revisão do manifesto

**Regra de Revisão**: Alterações no manifesto exigem documentação (o quê, por quê, aprovado por quem).

---

### Fase 5: Diagramas Detalhados (1-2 dias)

**Objetivo**: Visualizar arquitetura em múltiplos níveis.

**Atividades**:
- Gerar C4 detalhado (nível Component)
- Gerar ER (Entidade-Relacionamento)
- Gerar diagramas de sequência (fluxos principais)
- Gerar diagrama de dependências entre módulos
- Validar consistência entre diagramas e manifesto

**Deliverables**:
- [ ] 4+ tipos de diagramas
- [ ] Documentação de cada diagrama
- [ ] Validação de consistência

---

### Fase 6: Geração de Código (3-5 dias)

**Objetivo**: Implementar conforme manifesto e arquitetura.

**Atividades**:
- Gerar código seguindo stack definida (Node/Python/Go, React/Vue, etc.)
- Implementar camadas: Controllers, Services, Repositories (ou equivalente)
- Gerar tipos/interfaces
- Implementar testes unitários (TDD, 80%+ cobertura)
- Validar que código segue padrões do manifesto

**Deliverables**:
- [ ] Código completo e estruturado
- [ ] Testes unitários (80%+ cobertura)
- [ ] Documentação de API (OpenAPI/Swagger)
- [ ] Validação contra manifesto

**Nota**: Adaptar para stack do projeto (TypeScript, Python, Go, etc.).

---

### Fase 7: Ambiente e Infraestrutura (1-2 dias)

**Objetivo**: Criar ambiente de desenvolvimento e staging.

**Atividades**:
- Criar Dockerfile(s) para cada serviço
- Criar docker-compose com todos os serviços (DB, cache, fila, etc.)
- Configurar health checks
- Configurar CI/CD (GitHub Actions, GitLab CI, etc.)
- Documentar setup e deploy

**Deliverables**:
- [ ] Docker Compose completo
- [ ] CI/CD configurado
- [ ] Documentação de setup
- [ ] Guia de deploy em staging

---

### Fase 8: Revisão de Segurança e Testes (2-3 dias)

**Objetivo**: Garantir segurança e qualidade antes do deploy.

**Atividades**:
- Executar testes unitários, integração e E2E
- Revisão de segurança (OWASP Top 10, validação de entrada, autenticação)
- Threat modeling simplificado (opcional para projetos menores)
- Validar conformidade LGPD/GDPR em fluxos de dados
- Corrigir vulnerabilidades identificadas

**Deliverables**:
- [ ] Testes passando (100%)
- [ ] Cobertura 80%+
- [ ] Relatório de revisão de segurança
- [ ] Checklist OWASP preenchido

---

### Fase 9: Documentação e Preparação para Produção (1-2 dias)

**Objetivo**: Documentar tudo e preparar para produção.

**Atividades**:
- Criar documentação técnica completa
- Criar guia de deployment para produção
- Criar guia de usuário (se aplicável)
- Preparar runbooks operacionais
- Validar checklist final de qualidade

**Deliverables**:
- [ ] Documentação técnica
- [ ] Guia de deployment
- [ ] Runbooks operacionais
- [ ] Aplicação pronta para produção

---

## 5. INTEGRAÇÃO COM CONFORMIDADE

### ISO 25010

- **Fase 0**: Mapear características ISO relevantes (Functional Suitability, Security, Performance, etc.)
- **Fase 4**: Incluir no manifesto compromissos por característica ISO
- **Fase 8**: Validar métricas de qualidade (LCP, TTI, cobertura de testes, etc.)

### LGPD/GDPR

- **Fase 1**: Identificar dados pessoais e fluxos
- **Fase 4**: Documentar tratamento de dados no manifesto
- **Fase 6**: Implementar consentimento, anonimização, direito ao esquecimento
- **Fase 8**: Validar conformidade em fluxos críticos

---

## 6. MULTI-STACK: ADAPTAÇÕES

O padrão não assume stack fixa. Adaptar conforme projeto:

| Componente | Opções | Quando usar |
|------------|--------|-------------|
| Backend API | Node.js/NestJS, Python/FastAPI, Go/Fiber | Node: ecossistema JS; Python: IA/ML; Go: performance |
| Frontend | React, Vue, Svelte | Conforme preferência e equipe |
| Banco de Dados | PostgreSQL, MongoDB, etc. | Relacional vs documental |
| Cache | Redis, Memcached | Sessões, rate limiting |
| Fila | RabbitMQ, Kafka | Eventos assíncronos |
| IA/ML | Python, TensorFlow, etc. | Módulos preditivos |

**Regra**: O manifesto define a stack. O script de inicialização deve ser adaptado ou criado para o projeto.

---

## 7. CHECKLIST DE QUALIDADE FINAL

- [ ] Manifesto completo e aprovado
- [ ] Validação com usuários/stakeholders realizada
- [ ] Diagramas consistentes com manifesto
- [ ] Código segue padrões definidos
- [ ] Testes com 80%+ cobertura
- [ ] Revisão de segurança realizada
- [ ] Conformidade ISO/LGPD validada
- [ ] CI/CD configurado
- [ ] Docker Compose funcionando
- [ ] Documentação completa
- [ ] Aplicação pronta para produção

---

## 8. DURAÇÃO ESTIMADA

| Cenário | Duração Total |
|---------|---------------|
| Mínimo (1 dia por fase) | 10-12 dias |
| Recomendado (2-3 dias por fase) | 20-28 dias |
| Com revisões e validações | 30-45 dias |

---

## 9. USO PARA A PLATAFORMA AFIX

Para construir a plataforma AFIX, seguir este padrão com as seguintes referências:

1. **Manifesto**: `MANIFESTO_APLICACAO_ISO_25010.md` (já existe)
2. **Especificação**: `ESPECIFICACAO_SISTEMA.md` (já existe)
3. **Stack**: React + TypeScript (frontend), Node.js/NestJS ou Go (backend), Python/FastAPI (IA)
4. **Conformidade**: ISO 25010, LGPD, Meta Commerce Policies
5. **Fase 0**: AFIX já tem kickoff implícito; iniciar pela Fase 1 ou validar Fase 0

**Ordem sugerida para AFIX**:
- Fase 0: Validar escopo e stakeholders
- Fase 1: Pesquisa (WhatsApp API, IA preditiva, CRM)
- Fase 2: Validação com potenciais clientes/atendentes
- Fase 3: Arquitetura (Clean Architecture + FSD)
- Fase 4: Consolidar manifesto (já existe; validar completude)
- Fases 5-9: Seguir fluxo padrão

---

## 10. RECURSOS E REFERÊNCIAS

| Recurso | Localização |
|---------|-------------|
| Manifesto ISO 25010 | `docs/MANIFESTO_APLICACAO_ISO_25010.md` |
| Especificação do Sistema | `docs/ESPECIFICACAO_SISTEMA.md` |
| Workflow original (9 sprints) | `docs/skill_extracted/references/9-sprint-workflow.md` |
| Template de Manifesto | `docs/skill_extracted/templates/MANIFESTO_TEMPLATE.md` |

---

*Padrão de Criação de Plataforma — Afix | Versão 1.0 — Março 2026*
