# 📊 ANÁLISE DELTA CORRIGIDA: Evolucao_ISO vs Development
**Data**: 2026-04-01
**Local**: `/WORKSPACE/PROJETOS/AfixcontrolAfixgraf`
**Branch Comparação**: `Evolucao_ISO` ←→ `development`

---

## 🔴 RESULTADO REAL

**Evolucao_ISO está ATRÁS de development por:**
- **13 commits** novos em development que faltam em Evolucao_ISO
- **Múltiplos módulos** afetados (Propostas, Pedidos, Cálculos, NF-e, Producção, etc)
- **Infraestrutura Antigravity** adicionada (SENTRY telemetry)

---

## 📋 OS 13 COMMITS FALTANDO EM EVOLUCAO_ISO

### 1️⃣ **fa561e6** - Sincronização RD Station com Representante
```
fix: reivindicação de cliente sincroniza representante em propostas e pedidos locais
```
**Arquivos**: `classes/propostas.php`, `ajax/propostas.php`
**Tipo**: Bug Fix
**Impacto**: MÉDIO - Sincronização de dados entre RD Station e sistema local

---

### 2️⃣ **c5d8bb6** - Fluxo OTK e UX
```
fix: fluxo OTK no cadastro de cliente, UX ao salvar e listagem sem duplicatas
```
**Arquivos**: `ajax/nova-proposta.php`, `classes/otkweb.php`
**Tipo**: Bug Fix
**Impacto**: MÉDIO - Integração OTK e interface de usuário

---

### 3️⃣ **e1a96ba** - Precificação e Margem Composta
```
Ajusta precificação: margem composta, repasse proporcional no substrato e documentação
```
**Arquivos**: `classes/calculadora-core.php`, `ajax/calculos.php`
**Tipo**: Feature NOVA
**Impacto**: ALTO - Cálculos críticos de margem e preço

---

### 4️⃣ **a6ec549** - Auto-atualizar Valor e Preview em Lote
```
feat(produtos/substratos/custos): auto-atualizar valor, preview e aplicar em lote
```
**Arquivos**: `_produtos/produtos.php`, `ajax/novo-orcamento.js`, `classes/produtos.php`
**Tipo**: Feature NOVA
**Impacto**: MÉDIO - Produtividade em produtos/substratos

---

### 5️⃣ **c097032** - Orçamento: Markup, Custo Ajustado, Margem Contribuição
```
Orçamento: markup sobre custo, custo ajustado, margem de contribuição e UI alinhada
```
**Arquivos**: `ajax/novo-orcamento.php`, `assets/js/novo-orcamento.js`, `_propostas/proposta.php`
**Tipo**: Feature NOVA
**Impacto**: ALTO - Cálculos de orçamento completos

---

### 6️⃣ **6275220** - NF-e: Rastreio OTK, Pré-postagem e Pedido Local
```
NF-e: rastreio OTK (PUT/processar), pré-postagem e pedido local
```
**Arquivos**: `ajax/nfe.php`, `classes/otkweb.php`, `pedido-venda.php`
**Tipo**: Feature NOVA
**Impacto**: ALTO - Emissão de nota fiscal com rastreamento

---

### 7️⃣ **2aa1a2a** - Proposta Modal: Exibição de Produtos, Contato, Substrato
```
Proposta (modal e orçamento): exibição de produtos, contato e substrato
```
**Arquivos**: `_propostas/proposta.php`, `template/proposta/modals.php`, `ajax/propostas.php`
**Tipo**: Feature NOVA / UI
**Impacto**: MÉDIO - Interface de proposta melhorada

---

### 8️⃣ **09d638b** - PDF da Modal Otimizado e Catálogo de Motivos Declínio
```
feat: propostas — PDF da modal otimizado e declinação com catálogo de motivos no banco
```
**Arquivos**: `_propostas/proposta.php`, `migrations/add_proposta_motivo_declinio.sql`, `ajax/propostas.php`
**Tipo**: Feature NOVA
**Impacto**: MÉDIO - Geração de PDF e gestão de declínios

---

### 9️⃣ **4fbdab4** - Refatoração de Listagens com Filtros e Toolbar Uniforme
```
change: refatorar listagens de propostas com filtros por mês e estado, tabela única e toolbar uniforme
```
**Arquivos**: `_propostas/propostas.php`, `_propostas/todas-propostas.php`, `assets/css/style.css`, `assets/js/app.js`
**Tipo**: Refactoring / UI
**Impacto**: MÉDIO - Interface consistente

---

### 🔟 **bcda533** - Flag Retrabalho, Cores nas Filas, Prazo Editável
```
fix: proposta, produção e pedido — flag Retrabalho, cores nas filas e prazo editável
```
**Arquivos**: `ajax/producao.php`, `ajax/propostas.php`, `_pedidos/pedido.php`, `migrations/add_pedido_retrabalho.sql`
**Tipo**: Bug Fix / Feature
**Impacto**: MÉDIO - Gestão de produção

---

### 1️⃣1️⃣ **822af4d** - Clientes Temporários, Badges, Formulários PF/PJ, API CNPJ/OTK
```
fix: clientes temporários, badge nas telas, formulários PF/PJ e API CNPJ/OTK
```
**Arquivos**: `classes/CnpjCpfNormalizer.php`, `ajax/nova-proposta.php`, `classes/otkweb.php`
**Tipo**: Bug Fix / Feature
**Impacto**: ALTO - Cadastro e validação de clientes

---

### 1️⃣2️⃣ **5cf9684** - Modal de Registros de Contatos com Filtro e Botão Contextual
```
feat: modal de registros de contatos, filtro por representante e botão contextual nas propostas
```
**Arquivos**: `_propostas/proposta.php`, `assets/pages/proposta-registros-contatos-lista.js`, `ajax/propostas.php`
**Tipo**: Feature NOVA
**Impacto**: MÉDIO - Gestão de contatos

---

### 1️⃣3️⃣ **9052eeb** - Relatório de Pedidos por Filial com Subtotais
```
changes: relatório de pedidos de venda agrupado por filial, com subtotais por filial e total geral ao final
```
**Arquivos**: `includes/pedidos_venda_relatorio.php`, `pedidos-venda.php`
**Tipo**: Feature NOVA
**Impacto**: MÉDIO - Relatórios de vendas

---

## 📊 RESUMO POR CATEGORIA

| Categoria | Commits | Exemplos |
|-----------|---------|----------|
| **Feature NOVA** | 8 | Margem composta, Auto-update, NF-e, Contatos, Relatórios |
| **Bug Fix** | 4 | OTK flow, RD sync, Retrabalho, CNPJ validation |
| **Refactoring/UI** | 1 | Listagens unificadas |

---

## 🎯 ARQUIVOS PRINCIPAIS MODIFICADOS

### Backend (PHP):
- ✅ `ajax/propostas.php` - Listagens, modais, contatos
- ✅ `ajax/novo-orcamento.php` - Cálculos de orçamento
- ✅ `ajax/nfe.php` - Emissão de nota fiscal
- ✅ `ajax/producao.php` - Gestão de produção
- ✅ `classes/calculadora-core.php` - Cálculos críticos
- ✅ `classes/propostas.php` - Lógica de propostas
- ✅ `classes/otkweb.php` - Integração OTK
- ✅ `classes/CnpjCpfNormalizer.php` - Validação CNPJ/CPF

### Frontend (JavaScript/CSS):
- ✅ `assets/js/novo-orcamento.js` - UI de orçamento
- ✅ `assets/js/app.js` - Aplicação principal
- ✅ `assets/css/style.css` - Estilos unificados
- ✅ `assets/pages/proposta-*.js` - Páginas de proposta

### Templates (HTML/PHP):
- ✅ `_propostas/proposta.php` - Modal de proposta
- ✅ `_propostas/propostas.php` - Listagem de propostas
- ✅ `_pedidos/pedido.php` - Detalhes de pedido
- ✅ `template/proposta/modals.php` - Modais reutilizáveis

### Database:
- ✅ `migrations/add_proposta_motivo_declinio.sql` - Catálogo de declínios
- ✅ `migrations/add_pedido_retrabalho.sql` - Flag de retrabalho

### Infraestrutura:
- ✅ `13_ANTIGRAVITY_TELEMETRY/` - Sistema de monitoramento Antigravity
  - SENTRY monitoring
  - Snapshots de auditoria
  - Colector de telemetria

---

## ⚠️ ANÁLISE DE RISCO DOS 13 COMMITS

### RISCO CRÍTICO 🔴
**Commits**: `e1a96ba`, `c097032`, `6275220`, `822af4d`

**Por quê**:
- Modificam lógica crítica de cálculos (`calculadora-core.php`)
- Afetam emissão de NF-e (requer validação fiscal)
- Modificam fluxo de integração com APIs externas (OTK, RD Station, CNPJ)
- Impactam validação de dados críticos

**Mitigação**:
- [ ] Testar cálculos com casos de teste conhecidos
- [ ] Validar emissão de NF-e em sandbox
- [ ] Verificar APIs externas (OTK, RD Station)
- [ ] Validações de CNPJ/CPF com dados reais

---

### RISCO MÉDIO 🟡
**Commits**: `fa561e6`, `c5d8bb6`, `a6ec549`, `2aa1a2a`, `09d638b`, `4fbdab4`, `bcda533`, `5cf9684`, `9052eeb`

**Por quê**:
- Modificam UI e fluxos de usuário
- Afetam históricos e relatórios
- Integram novos módulos (contatos, retrabalho)

**Mitigação**:
- [ ] Testes de integração em cada módulo
- [ ] QA em cada interface modificada
- [ ] Validação de dados históricos

---

## 🛠️ PRÓXIMOS PASSOS - OPÇÕES

### OPÇÃO A: Implementação Gradual
1. Trazer commits de bug fix first (`fa561e6`, `c5d8bb6`, `822af4d`)
2. Depois features de cálculo (`e1a96ba`, `c097032`)
3. Depois integração (`6275220`, `09d638b`)
4. Depois UI/UX (`4fbdab4`, `5cf9684`, `2aa1a2a`)
5. Depois relatórios (`9052eeb`)

**Tempo**: ~40-50h (distribuído em sprints)

---

### OPÇÃO B: Merge Completo + Testes
1. Fazer merge de todos os 13 commits
2. Executar suite de testes completa
3. Corrigir issues encontrados

**Tempo**: ~30h (concentrado, mas alto risco)

---

### OPÇÃO C: Cherry-pick Seletivo
1. Pegar apenas commits críticos primeiro
2. Validar em staging
3. Depois pegar os demais

**Tempo**: ~60h (mais seguro mas mais lento)

---

## 📋 DECISÃO NECESSÁRIA

**O que você quer fazer?**

- [ ] A) Implementar gradualmente (feature por feature)
- [ ] B) Merge completo de todos os 13 commits
- [ ] C) Cherry-pick dos commits críticos primeiro
- [ ] D) Análise de conflitos específicos antes de decidir

**Qual é sua preferência?**

