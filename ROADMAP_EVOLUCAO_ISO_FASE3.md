# 🚀 ROADMAP EVOLUCAO_ISO - FASE 3
## Implementação Segura de Features da Development Branch

**Data**: 2026-04-01
**Status**: Pronto para Implementação
**Metodologia**: Um por um, com testes, auditoria, telemetria
**Total de Features**: 27 codadas em development

---

## 📊 SUMÁRIO EXECUTIVO

- ✅ **27 features** completamente codadas em development
- 🔍 **Análise rigorosa** - verificadas no código fonte, não no README
- 🎯 **Priorização estratégica** - ordem recomendada de implementação
- 🛡️ **Segurança total** - testes, auditoria, telemetria para cada feature
- 📋 **Backlog organizado** - pronto para execução iterativa

---

## 🎯 FASES DE IMPLEMENTAÇÃO

### FASE 3.1: INFRAESTRUTURA & SEGURANÇA (Prioridade: CRÍTICA)
Implementar antes de qualquer outra feature

#### 3.1.1 - Sistema de Credenciais Seguras (.env)
- **Commit Original**: 5778f3f (development)
- **O que é**: Migração de credenciais hardcoded para .env
- **Status em Evolucao_ISO**: ⚠️ PRECISA VERIFICAR
- **Arquivos**:
  - `requires/load_env.php` (carregador customizado)
  - `.env.example` (template)
  - `.gitignore` (excluir .env)
- **Impacto**: CRÍTICO - afeta RD Station, ViPP, Correios, SMTP
- **Testes**: Verificar se credenciais carregam corretamente
- **Status**: 🟡 PRÉ-REQUISITO

#### 3.1.2 - Sistema de Índices no Banco
- **Problema**: idx_proposta_estado faltando (283 propostas)
- **O que fazer**:
  ```sql
  ALTER TABLE propostas ADD INDEX idx_proposta_estado (proposta_estado);
  ```
- **Impacto**: Performance de filtros
- **Status**: 🔴 BLOQUEADOR
- **Implementação**: Imediata

#### 3.1.3 - Arquivo authentication.php Faltando
- **Problema**: test-iso-shield.php quebra procurando requires/authentication.php
- **O que fazer**: Recuperar do git history ou criar stub
- **Status**: 🔴 BLOQUEADOR
- **Implementação**: Imediata

---

### FASE 3.2: RELATÓRIOS & DASHBOARDS (Prioridade: ALTA)

#### 3.2.1 - Dashboard Principal Avançado
- **Commit**: dedd7fe
- **O que é**: Relatórios e Insights em dashboard integrado
- **Arquivos a portar**:
  - `relatorios.php` (530 linhas)
  - `template/top_header.php`
  - `includes/relatorios.php`
- **Funcionalidades**:
  - Visualização de vendas por período
  - Relatório de produtos
  - KPIs em tempo real
- **Status em Evolucao_ISO**: ⚠️ Parcial (precisa verificar)
- **Prioridade**: ALTA
- **Implementação**: Semana 1

#### 3.2.2 - Relatório Pedidos de Venda
- **Commit**: 9052eeb
- **O que é**: Relatório agrupado por filial com subtotais
- **Arquivos a portar**:
  - `includes/pedidos_venda_relatorio.php`
  - `relatorio-pedidos-venda.php`
- **Funcionalidades**:
  - Agrupamento por filial
  - Subtotais por filial
  - Total geral
  - Filtros por período
- **Status em Evolucao_ISO**: ⚠️ Verificar
- **Prioridade**: ALTA
- **Implementação**: Semana 1

#### 3.2.3 - Relatório Produtos Mais Vendidos
- **Commit**: 1a0284c
- **O que é**: Análise de produtos com maior volume de vendas
- **Arquivos a portar**:
  - `includes/produtos_mais_vendidos.php`
  - `relatorio-produtos-mais-vendidos.php`
- **Prioridade**: ALTA
- **Implementação**: Semana 1

---

### FASE 3.3: SISTEMA RNC (Prioridade: ALTA)

#### 3.3.1 - RNC com Filtros Avançados
- **Commit**: c56f2a5
- **O que é**: Sistema de Não-Conformidade com busca/filtros
- **Arquivos a portar**:
  - `prodsis/rnc.php` (modificado)
  - `prodsis/api/rnc.php` (modificado)
  - `prodsis/assets/js/rnc.js` (modificado)
- **Funcionalidades**:
  - Filtros por status
  - Filtros por setor
  - Filtros por período
  - Busca texto
- **Status em Evolucao_ISO**: ⚠️ Estrutura existe, filtros podem estar diferentes
- **Prioridade**: ALTA
- **Implementação**: Semana 1

#### 3.3.2 - Classificação RNC e Custo Parcial
- **Commit**: df5e36c
- **O que é**: Categorização de RNC (Reclamação vs Retrabalho)
- **Arquivos a portar**:
  - `prodsis/migrations/add_classificacao_rnc.php`
  - Modificações em `prodsis/rnc.php`
- **Funcionalidades**:
  - Coluna ENUM (classificacao_rnc)
  - Cálculo de 50% do valor registrado
  - Dashboard com gráficos de evolução
- **Status em Evolucao_ISO**: ⚠️ Pode estar parcial
- **Prioridade**: ALTA
- **Implementação**: Semana 1-2

#### 3.3.3 - Gráficos de Evolução RNC (12 meses)
- **Commit**: 1516782
- **O que é**: Visualização de histórico RNC
- **Arquivos a portar**:
  - Modificações em `prodsis/rnc.php`
  - Scripts Chart.js
- **Funcionalidades**:
  - Gráfico evolução mensal (12 meses)
  - Indicadores de carregamento (spinners)
  - Compatibilidade Chart.js v2
- **Status em Evolucao_ISO**: ⚠️ Verificar
- **Prioridade**: MÉDIA
- **Implementação**: Semana 2

---

### FASE 3.4: INTEGRAÇÃO VITECH/VIAFRETE (Prioridade: CRÍTICA)

#### 3.4.1 - Classe ViPP Completa
- **Commit**: cad893a
- **O que é**: Integração com API ViPP para etiquetas Correios
- **Arquivos a portar**:
  - `classes/vipp.php` (516 linhas - NOVA CLASSE)
  - `database/migrations/add_vipp_fields_to_prepostagens.sql`
- **Funcionalidades**:
  - Autenticação ViPP
  - Requisições HTTP para gerar etiquetas
  - Tratamento de erros
  - Persistência de dados ViPP
- **Status em Evolucao_ISO**: ❌ PROVAVELMENTE FALTA
- **Prioridade**: CRÍTICA (bloqueia etiquetas Correios)
- **Implementação**: Semana 1 (imediata)
- **Testes**:
  - Autenticação ViPP
  - Geração de etiqueta de teste
  - Armazenamento de resposta

#### 3.4.2 - Bug Fix: Serviço AR Default ViPP
- **Commit**: 83368a1
- **O que é**: Fix crítico em lógica de AR (Aviso de Recebimento)
- **Arquivos a modificar**:
  - `ajax/pedidos-venda.php`
  - `ajax/prepostagem.php`
- **O problema**: Serviço AR sendo setado incorretamente como default
- **A solução**:
  - Verificar AdicionaisVolume antes de override
  - Tratamento especial de campos booleanos
  - Validação de estado do AR
- **Status em Evolucao_ISO**: ⚠️ Verificar se tem o bug
- **Prioridade**: CRÍTICA se bug existir
- **Implementação**: Logo após ViPP

#### 3.4.3 - Sistema Completo Prepostagem ViPP
- **Commit**: 1e44a96
- **O que é**: Integração ViPP em fluxo de prepostagem
- **Arquivos a modificar**:
  - `prepostagem.php` (modificado)
  - `pedido-venda.php` (modificado)
  - `ajax/prepostagem.php` (modificado)
- **Funcionalidades**:
  - Carregamento de contatos JSON da ViPP
  - Seleção de contato para etiqueta
  - Envio de dados para ViPP
  - Rastreamento de respostas
- **Status em Evolucao_ISO**: ⚠️ Verificar
- **Prioridade**: CRÍTICA
- **Implementação**: Semana 1-2

#### 3.4.4 - Documentação Interativa API ViPP
- **Commit**: ee41c87
- **O que é**: Documentação interativa com 51 endpoints
- **Arquivos a portar**:
  - `/vipp/` (17 arquivos, 776 KB)
  - `vipp/index.html` (documentação interativa)
  - `vipp/proxy.php` (proxy para testes)
- **Status em Evolucao_ISO**: ❌ PROVAVELMENTE FALTA
- **Prioridade**: MÉDIA (consulta, não crítica)
- **Implementação**: Semana 2

---

### FASE 3.5: INTEGRAÇÃO RD STATION (Prioridade: ALTA)

#### 3.5.1 - RD Station: Busca Empresa + Prevenção Duplicidade
- **Commit**: a479332
- **O que é**: Melhorias na integração RD Station
- **Arquivos a modificar**:
  - `classes/rdstation.php`
  - `ajax/clientes_otk.php`
- **Funcionalidades**:
  - Busca de empresas por nome na RD Station
  - Validação de duplicidade
  - Sincronização automática
- **Status em Evolucao_ISO**: ⚠️ Verificar
- **Prioridade**: ALTA
- **Implementação**: Semana 2

#### 3.5.2 - RD Station: Validação ID + Modal Mover Negociação
- **Commit**: cc711b0
- **O que é**: Validação de integração e flexibilidade de negociações
- **Arquivos a modificar**:
  - `ajax/novo-orcamento.php`
  - `template/proposta/modals.php`
- **Funcionalidades**:
  - Alertas de RD Station ID faltando
  - Modal para mover negociação entre clientes
  - Validação de sincronização
- **Status em Evolucao_ISO**: ⚠️ Verificar
- **Prioridade**: ALTA
- **Implementação**: Semana 2

#### 3.5.3 - RD Station: Criar Negociação Button
- **Commit**: b0cc8af
- **O que é**: Botão dedicated para criar negociação em RD Station
- **Arquivos a modificar**:
  - `ajax/novo-orcamento.php`
  - `classes/otkweb.php`
- **Funcionalidades**:
  - Botão "Criar Negociação" no novo orçamento
  - Integração com RD Station API
  - Vinculação automática
- **Status em Evolucao_ISO**: ⚠️ Verificar
- **Prioridade**: ALTA
- **Implementação**: Semana 2

---

### FASE 3.6: ETIQUETAS CORREIOS (Prioridade: ALTA)

#### 3.6.1 - Exportação Excel/CSV Etiquetas
- **Commit**: c034503 + 3311b5b
- **O que é**: Exportar etiquetas para Excel/CSV
- **Arquivos a modificar**:
  - `pedido-venda.php`
  - `modal` para exportação
- **Funcionalidades**:
  - Modal de exportação
  - Formato XLSX/CSV
  - Filtro de etiquetas
- **Status em Evolucao_ISO**: ⚠️ Verificar
- **Prioridade**: ALTA
- **Implementação**: Semana 2

#### 3.6.2 - Impressão em Lote de Etiquetas
- **Commit**: 7b0b835
- **O que é**: Imprimir múltiplas etiquetas de uma vez
- **Arquivos a portar**:
  - `imprimir-etiquetas-lote.php` (370 linhas - NOVO)
  - Modificações em `etiqueta-simples.php`
  - Modificações em `pedidos-venda.php`
- **Funcionalidades**:
  - CSS grid para múltiplas etiquetas na página
  - Seleção em lote
  - Otimização para impressora
- **Status em Evolucao_ISO**: ⚠️ Verificar
- **Prioridade**: ALTA
- **Implementação**: Semana 2

#### 3.6.3 - Layout com Drag & Drop
- **Commit**: c181749
- **O que é**: Solicitar layout com suporte drag-and-drop
- **Arquivos a modificar**:
  - `ajax/layout.php`
  - `assets/pages/proposta.js`
  - CSS para drop zones
- **Funcionalidades**:
  - Zona de drop visual
  - Feedback ao arrastar
  - Upload de múltiplos layouts
- **Status em Evolucao_ISO**: ⚠️ Verificar
- **Prioridade**: MÉDIA
- **Implementação**: Semana 3

---

### FASE 3.7: PEDIDOS DE VENDA (Prioridade: ALTA)

#### 3.7.1 - Sistema de Cancelamento de Pedidos
- **Commit**: 1f51d0d
- **O que é**: Permitir cancelamento de pedidos com auditoria
- **Arquivos a modificar**:
  - `ajax/pedidos-venda.php` (adicionar função cancelarPedidoVenda)
  - `pedidos-venda.php` (interface de cancelamento)
- **Funcionalidades**:
  - Botão cancelar visível quando apropriado
  - Motivo obrigatório
  - UPDATE estado='cancelado'
  - Auditoria do cancelamento
- **Status em Evolucao_ISO**: ⚠️ Verificar
- **Prioridade**: ALTA
- **Implementação**: Semana 2

#### 3.7.2 - Sistema de Endereços (Entrega + Faturamento)
- **Commit**: 3f52c85
- **O que é**: Múltiplos endereços por cliente
- **Arquivos a modificar**:
  - `_clientes/cliente.php`
  - `_clientes/novo-cliente.php`
  - `ajax/pedidos-venda.php`
- **Funcionalidades**:
  - Campos cliente_endereco_entrega
  - Campos cliente_endereco_faturamento
  - Seleção no novo pedido
  - Validação de preenchimento
- **Status em Evolucao_ISO**: ⚠️ Verificar
- **Prioridade**: ALTA
- **Implementação**: Semana 1

#### 3.7.3 - Fretes Manuais e Campo Transportadora
- **Commit**: 97e6ecd
- **O que é**: Permitir frete manual sem depender de Correios/ViPP
- **Arquivos a modificar**:
  - `ajax/frete.php`
  - `_propostas/novo-orcamento.php`
  - `assets/js/novo-orcamento.js`
- **Funcionalidades**:
  - Input manual de frete
  - Campo transportadora (texto)
  - Cálculo alternativo de entrega
- **Status em Evolucao_ISO**: ⚠️ Verificar
- **Prioridade**: ALTA
- **Implementação**: Semana 2

---

### FASE 3.8: CONTROLE FINANCEIRO (Prioridade: ALTA)

#### 3.8.1 - Validação Contato Financeiro (Bloqueio PV)
- **Commit**: 2974f01
- **O que é**: Impedir emissão de PV se cliente sem contato financeiro
- **Arquivos a modificar**:
  - `_propostas/proposta.php`
  - `ajax/propostas.php`
- **Funcionalidades**:
  - Validação antes de gerar PV
  - Mensagem Lobibox.notify()
  - Bloqueio visual do botão
- **Status em Evolucao_ISO**: ⚠️ Verificar
- **Prioridade**: ALTA
- **Implementação**: Semana 1

#### 3.8.2 - Alertas Boletos: Vencidos vs A Vencer
- **Commit**: bb6f064
- **O que é**: Mostrar boletos vencidos e próximos a vencer separadamente
- **Arquivos a modificar**:
  - `ajax/novo-orcamento.php`
  - `assets/js/novo-orcamento.js`
- **Funcionalidades**:
  - Seção "Boletos Vencidos"
  - Seção "Boletos A Vencer"
  - Cores diferenciadas
  - Alertas automáticos
- **Status em Evolucao_ISO**: ⚠️ Verificar
- **Prioridade**: ALTA
- **Implementação**: Semana 2

#### 3.8.3 - Controle de Acesso a Informações Financeiras
- **Commit**: 87515a3
- **O que é**: Restringir visualização de dados financeiros por nível de acesso
- **Arquivos a modificar**:
  - `ajax/propostas.php`
  - `assets/js/novo-orcamento.js`
  - Múltiplos arquivos com lógica de acesso
- **Funcionalidades**:
  - Verificação de nível de usuário
  - Ocultação de campos financeiros
  - Logs de tentativas de acesso
- **Status em Evolucao_ISO**: ⚠️ Verificar
- **Prioridade**: ALTA
- **Implementação**: Semana 2-3

---

### FASE 3.9: INTERFACE & UX (Prioridade: MÉDIA)

#### 3.9.1 - Kanban/Grid Profissional com Drag & Drop
- **Commit**: 157605c
- **O que é**: Refatorar visualização de produção em grid
- **Arquivos a modificar**:
  - `producao.php`
  - CSS grid-template-columns
- **Funcionalidades**:
  - Layout grid CSS
  - Drag & drop entre etapas
  - Tema visual neutro
  - Responsividade
- **Status em Evolucao_ISO**: Provavelmente já tem
- **Prioridade**: BAIXA
- **Implementação**: Semana 3-4

#### 3.9.2 - Consistência Visual Desktop
- **Commit**: 2387e5a
- **O que é**: Unificar visual de tabs e textos no desktop
- **Arquivos a modificar**:
  - `desktop.php`
  - `template/desktop/desktop-style.php`
- **Funcionalidades**:
  - CSS para #desktopTabs
  - Tipografia consistente
  - Cores padrão
- **Status em Evolucao_ISO**: Provavelmente já tem
- **Prioridade**: BAIXA
- **Implementação**: Semana 4

---

### FASE 3.10: CLIENTES & CONTATOS (Prioridade: MÉDIA)

#### 3.10.1 - Clientes Temporários + API CNPJ
- **Commit**: 822af4d
- **O que é**: Criar cliente temporário sem CNPJ confirmado
- **Arquivos a modificar**:
  - `_clientes/novo-cliente.php`
  - `ajax/clientes_otk.php`
  - `classes/cnpjcpfnormalizer.php` (NOVA CLASSE)
- **Funcionalidades**:
  - Toggle "Cliente Temporário"
  - Validação CNPJ/CPF com API
  - Badge visual no cliente
  - Formulário PF/PJ dinâmico
- **Status em Evolucao_ISO**: ⚠️ Pode estar parcial
- **Prioridade**: MÉDIA
- **Implementação**: Semana 2-3

#### 3.10.2 - Modal Registros de Contatos
- **Commit**: 5cf9684
- **O que é**: Modal para gerenciar registros de contatos
- **Arquivos a modificar**:
  - `_propostas/proposta.php`
  - `ajax/clientes_otk.php`
  - `template/proposta/modals.php`
- **Funcionalidades**:
  - Listagem de registros por contato
  - Filtro por representante
  - Botão contextual nas propostas
  - Histórico de interações
- **Status em Evolucao_ISO**: ⚠️ Pode estar parcial
- **Prioridade**: MÉDIA
- **Implementação**: Semana 3

#### 3.10.3 - Contatos Cliente com Notificações
- **Commit**: 9bbd90e
- **O que é**: Melhorias em exibição de contatos e notificações
- **Arquivos a modificar**:
  - `_clientes/cliente.php`
  - `ajax/layout.php`
- **Funcionalidades**:
  - Integração de contatos do cliente
  - Notificações automáticas
  - Ajuste de permissões por contato
- **Status em Evolucao_ISO**: ⚠️ Verificar
- **Prioridade**: MÉDIA
- **Implementação**: Semana 3

---

### FASE 3.11: OUTROS AJUSTES (Prioridade: BAIXA)

#### 3.11.1 - Ajustes NF-e, Etiquetas Simples e Ordenação
- **Commit**: 924aecf
- **O que é**: Diversos ajustes em NF-e e interface
- **Arquivos a modificar**:
  - `ajax/nfe.php`
  - `etiqueta-simples.php`
  - `pedidos-venda.php`
- **Prioridade**: BAIXA
- **Implementação**: Semana 4

#### 3.11.2 - Ajustes Permissões Produção
- **Commit**: 75463db
- **O que é**: Refinar controle de acesso em produção
- **Arquivos a modificar**:
  - `ajax/producao.php`
- **Prioridade**: BAIXA
- **Implementação**: Semana 4

#### 3.11.3 - Melhorias Histórico de Produção
- **Commit**: 8c923d8
- **O que é**: Interface melhorada para histórico
- **Arquivos a modificar**:
  - `prodsis/historico.php`
- **Funcionalidades**:
  - Layout grid CSS
  - Filtro funcionários
  - Responsividade horizontal
- **Prioridade**: BAIXA
- **Implementação**: Semana 4

---

## 📈 CRONOGRAMA RECOMENDADO

```
SEMANA 1 (Imediata - Prioridade Crítica):
├─ 3.1.1 - Credenciais .env
├─ 3.1.2 - Índice proposta_estado
├─ 3.1.3 - Arquivo authentication.php
├─ 3.4.1 - Classe ViPP
├─ 3.7.2 - Endereços Entrega/Faturamento
├─ 3.8.1 - Validação Contato Financeiro
├─ 3.2.1 - Dashboard
├─ 3.2.2 - Relatório Pedidos
├─ 3.3.1 - RNC Filtros
└─ 3.5.1 - RD Station Busca Empresa

SEMANA 2 (Prioridade Alta):
├─ 3.4.2 - Bug Fix AR ViPP
├─ 3.4.3 - Prepostagem ViPP
├─ 3.6.1 - Exportação Excel Etiquetas
├─ 3.6.2 - Impressão em Lote Etiquetas
├─ 3.7.1 - Cancelamento Pedidos
├─ 3.7.3 - Fretes Manuais
├─ 3.3.2 - RNC Classificação
├─ 3.5.2 - RD Station Modal Mover
├─ 3.5.3 - RD Station Botão Criar
├─ 3.8.2 - Alertas Boletos
└─ 3.10.1 - Clientes Temporários

SEMANA 3 (Prioridade Média):
├─ 3.2.3 - Relatório Produtos
├─ 3.3.3 - Gráficos RNC 12 meses
├─ 3.6.3 - Layout Drag & Drop
├─ 3.8.3 - Controle Acesso Financeiro
├─ 3.10.2 - Modal Registros Contatos
└─ 3.10.3 - Contatos Notificações

SEMANA 4 (Prioridade Baixa):
├─ 3.9.1 - Kanban Grid UX
├─ 3.9.2 - Consistência Desktop
├─ 3.11.1 - Ajustes NF-e
├─ 3.11.2 - Permissões Produção
├─ 3.11.3 - Histórico Produção
└─ 3.4.4 - Documentação ViPP (consulta)
```

---

## 🧪 CHECKLIST DE IMPLEMENTAÇÃO POR FEATURE

Para cada feature, aplicar este checklist:

```
Feature: [Nome]
Commit: [Hash]

☐ 1. CODE REVIEW
   ☐ Ler código original em development
   ☐ Identificar dependências
   ☐ Verificar bugs conhecidos

☐ 2. ANÁLISE DE DELTA
   ☐ Comparar com Evolucao_ISO
   ☐ Identificar o que falta
   ☐ Listar conflitos potenciais

☐ 3. IMPLEMENTAÇÃO
   ☐ Copiar/adaptar código
   ☐ Aplicar migrações SQL se houver
   ☐ Atualizar configurações

☐ 4. TESTES UNITÁRIOS
   ☐ Testar funcionalidade principal
   ☐ Testar casos extremos
   ☐ Verificar compatibilidade

☐ 5. TESTES DE INTEGRAÇÃO
   ☐ Testar com outras features
   ☐ Testar fluxos completos
   ☐ Verificar sem side effects

☐ 6. AUDITORIA
   ☐ Logging de ações
   ☐ Rastreamento de mudanças
   ☐ Compliance de dados

☐ 7. TELEMETRIA
   ☐ Adicionar eventos
   ☐ Medir performance
   ☐ Alertas configurados

☐ 8. DOCUMENTAÇÃO
   ☐ Atualizar README
   ☐ Documentar mudanças
   ☐ Exemplos de uso

☐ 9. COMMIT GIT
   ☐ Mensagem clara
   ☐ Referência ao commit original
   ☐ Co-author se apropriado

Status: ☐ PRONTO ☐ EM PROGRESSO ☐ BLOQUEADO
```

---

## 🎯 MÉTRICAS DE SUCESSO

- ✅ **27/27 features** implementadas em Evolucao_ISO
- ✅ **100% de cobertura** de testes para cada feature
- ✅ **Zero regressões** em funcionalidades existentes
- ✅ **Performance** mantida ou melhorada
- ✅ **Auditoria completa** de todas as mudanças
- ✅ **Zero bugs críticos** encontrados em produção

---

## 📝 NOTAS IMPORTANTES

1. **Começar pela Infraestrutura**: Credenciais, índices e arquivo faltando são PRÉ-REQUISITOS
2. **Testar Iterativamente**: Não esperar completar tudo para testar
3. **Auditoria a Cada Passo**: Registrar o que foi mudado e por quê
4. **Comunicação Clara**: Documentar tudo para futuras referências
5. **Segurança Total**: Não "forçar" implementação, respeitar testes e validações

---

**Próximo Passo**: Você quer começar pela Semana 1? Qual feature você quer implementar primeiro?
