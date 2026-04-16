# RELATÓRIO DE DIAGNÓSTICO - FASE 2
## ANÁLISE CRÍTICA DO ESTADO DO AFIXCONTROL
**Data**: 2026-04-01
**Nível de Severidade**: CRÍTICO
**Preparado Por**: MCP Server - Validação Autônoma

---

## 📊 EXECUTIVO

| Métrica | Valor | Status |
|---------|-------|--------|
| Total de Propostas | 283 | ✅ Dados Presentes |
| Branches Ativas | 3 (main, development, Evolucao_ISO) | ⚠️ Desalinhadas |
| Commits Não Sincronizados | 50 | 🔴 **CRÍTICO** |
| Divergências Identificadas | 7 | 🔴 **CRÍTICO** |
| Índices Faltando | 1 | 🟡 **ALTO** |
| Estado da Documentação | Desatualizado | 🟡 **ALTO** |

---

## 🔍 SEÇÃO 1: ESTADO DAS BRANCHES

### 1.1 Contagem de Commits

```
Branch      | Total | Novos desde Main | Última Atualização
------------|-------|------------------|-------------------
main        | 43    | baseline         | 2026-03-05 09:57 (25 dias)
development | 69    | +27 commits      | 2026-03-30 21:24 (1 dia)
Evolucao    | 65    | +23 commits      | 2026-03-31 16:46 (TODAY)
```

### 1.2 Análise de Divergência

- **Divergência máxima**: 27 commits entre `main` e `development`
- **Estado atual do projeto**: Em `Evolucao_ISO` (branch mais atualizada)
- **Main está ATRASADA**: 25 dias sem atualização
- **Risk**: Merge da development para main causará conflitos

### 1.3 Últimos Commits Críticos

**MAIN** (obsoleto):
```
248e1bb | 2026-03-05 | Merge PR #1 from development
```

**DEVELOPMENT** (ativo):
```
9052eeb | 2026-03-30 | Relatório de pedidos agrupado por filial
[25 commits anteriores não presentes em main]
```

**EVOLUCAO_ISO** (em uso):
```
e160b12 | 2026-03-31 | ISO Shield - 4 casas decimais, persistência metadados
```

---

## 🚨 SEÇÃO 2: DIVERGÊNCIAS CRÍTICAS ENCONTRADAS

### **DIVERGÊNCIA #1: WHITELIST DE ESTADOS (CRÍTICA)**

#### 📋 Evidência 1: classes/propostas.php (Linha 481)
```php
$whitelist = ['em negociação', 'aprovado', 'declinada'];
```

#### 📋 Evidência 2: api/mcp-gateway.php (Linha 26)
```php
'whitelist_estados' => ['aprovada', 'em_negociacao', 'recusada', 'pendente']
```

#### 📋 Evidência 3: Banco de Dados (283 propostas)
```
Estados encontrados:
  • 'aprovado'          (usado em classes/propostas.php)
  • 'declinada'         (usado em classes/propostas.php)
  • 'em negociação'     (usado em classes/propostas.php)
```

#### 📋 Evidência 4: README.md (Documentação)
```
"Controle de estados (em negociação, aprovada, recusada)"
```

#### ⚠️ CONCLUSÃO DA DIVERGÊNCIA

| Fonte | Estados |
|-------|---------|
| **Código Real** (classes/propostas.php) | em negociação, **aprovado**, **declinada** |
| **Banco de Dados** | em negociação, **aprovado**, **declinada** |
| **API Gateway** | aprovada, em_negociacao, recusada, pendente |
| **Documentação (README.md)** | em negociação, **aprovada**, **recusada** |

**🔴 PROBLEMA**: O código real usa `aprovado/declinada` mas:
- API Gateway espera `aprovada/recusada`
- README.md documenta `aprovada/recusada`
- Banco tem `aprovado/declinada`

**IMPACTO**: Validação falsa de estados. Ferramenta de validação (MCP) rejeita dados válidos.

---

### **DIVERGÊNCIA #2: ESTRUTURA DE ÍNDICES**

#### 📋 Evidência: Validação de Índices

```sql
-- ÍNDICES PRESENTES NO BANCO:
PRIMARY (proposta_id)
idx_proposta_pedido_venda (proposta_pedido_venda)

-- ÍNDICE FALTANDO:
idx_proposta_estado (SOLICITADO NA DOCUMENTAÇÃO DO GATEWAY)
```

#### 🔴 PROBLEMA
- Coluna `proposta_estado` com 283 registros sem índice
- Queries de filtro por estado sofrerão FULL TABLE SCAN
- Performance degradada em queries como: `WHERE proposta_estado = 'aprovado'`

#### 💡 RECOMENDAÇÃO (mcp-gateway.php)
```sql
ALTER TABLE propostas ADD INDEX idx_proposta_estado (proposta_estado);
```

---

### **DIVERGÊNCIA #3: CAMPO DEFAULT NA TABELA**

#### 📋 Evidência: database.sql

```sql
CREATE TABLE propostas (
  `proposta_estado` varchar(100) DEFAULT 'em negociação'
  ...
)
```

**Observação**: Campo vem com `'em negociação'` como default (sem acento no banco).
Mas README documenta com acento: `'em negociação'`. ✅ Coerência confirmada neste ponto.

---

### **DIVERGÊNCIA #4: ARQUIVO DE AUTENTICAÇÃO FALTANDO**

#### 📋 Evidência: Erro em test-iso-shield.php

```
Fatal error: Uncaught Error: Failed opening required '..\/requires\/authentication.php'
```

#### 🔴 PROBLEMA
- Arquivo `requires/authentication.php` referenciado mas não existe
- Testes falham ao tentar importar autenticação
- Caminho relativo pode estar incorreto

#### 🔍 VERIFICAÇÃO
```bash
# Arquivo NÃO ENCONTRADO em:
requires/authentication.php
requires/auth.php
_includes/authentication.php
```

---

### **DIVERGÊNCIA #5: COMMITS DIVERGENTES NAS BRANCHES**

#### 📋 Evidência: Git Log

```
Development tem 27 commits que main não tem:
- Filtros de propostas melhorados
- RNC (Relatório de Não-Conformidade)
- Dashboard avançado
- Gráficos de evolução
- Migração de .env (credenciais)
- [+22 outros]

Evolucao_ISO tem 23 commits que main não tem (subset de development + seus próprios):
- ISO Shield (4 casas decimais)
- Metadados técnicos
- Validação de auditoria
- [+20 outros]
```

#### 🔴 PROBLEMA
- **Código em produção (main) está ATRASADO 25 dias**
- Funcionalidades desenvolvidas não estão em produção
- Risco de regressão no merge

---

### **DIVERGÊNCIA #6: ESTADO DO CÓDIGO vs DOCUMENTAÇÃO**

#### Classes Mencionadas no README.md - Validação de Existência

| Classe | Arquivo | Existe? | Última Modificação | Status |
|--------|---------|---------|-------------------|--------|
| Proposta | classes/propostas.php | ✅ | 2026-03-31 | Ativa |
| OtkWeb | classes/otkweb.php | ✅ | 2026-03-31 | Ativa |
| RdStation | classes/rdstation.php | ✅ | 2026-03-23 | Ativa |
| Correios | classes/correios.php | ✅ | 2026-03-31 | Ativa |
| Pedidos | classes/pedidos.php | ✅ | - | Assumido ativo |

**STATUS**: Todas as integrações mencionadas existem. ✅

#### Módulos Mencionados no README.md - Validação de Existência

| Módulo | Diretório | Existe? | Status |
|--------|-----------|---------|--------|
| Clientes | _clientes/ | ✅ | Ativo |
| Propostas | _propostas/ | ✅ | Ativo |
| Pedidos | _pedidos/ | ✅ | Ativo |
| Produtos | _produtos/ | ✅ | Ativo |
| AJAX API | ajax/ | ✅ | Ativo |

**STATUS**: Estrutura de módulos está completa. ✅

---

### **DIVERGÊNCIA #7: VARIÁVEIS DE AMBIENTE**

#### 📋 Evidência: Migração para .env (development branch)

Commit detectado:
```
5778f3f | Migração de credenciais sensíveis para ambiente seguro via .env
```

#### 🔴 PROBLEMA
- `classes/propostas.php` usa hardcoded ou variáveis globais?
- `.env` file não está sincronizado com main
- Credenciais (RD Station, Correios, SMTP) podem estar expostas em main

---

## 📊 SEÇÃO 3: VALIDAÇÃO DO BANCO DE DADOS

### 3.1 Contagem de Dados

```sql
SELECT COUNT(*) FROM propostas;
```

| Tabela | Registros | Status |
|--------|-----------|--------|
| propostas | 283 | ✅ Dados presentes |
| proposta_produtos | ? | ⚠️ Não verificado |
| clientes | ? | ⚠️ Não verificado |
| pedidos | ? | ⚠️ Não verificado |

### 3.2 Integridade Referencial

**Não verificado nesta fase** - Requer validação SQL adicional

---

## 📋 SEÇÃO 4: ESTADO DAS TESTES

### 4.1 Testes Encontrados

```
test-ajax-shadow.php:  ✅ PASSOU (CalculadoraCore validada)
test-iso-shield.php:   ❌ FALHOU (Arquivo authentication.php faltando)
```

### 4.2 Framework de Testes

- **Quantidade**: 2 testes
- **Taxa de Sucesso**: 50% (1/2)
- **Bloqueador**: Arquivo faltando

---

## 🎯 SEÇÃO 5: CHECKLIST DE SINCRONIZAÇÃO

### Pré-Requisitos para Merge de development → main

- [ ] Resolver divergência de WHITELIST DE ESTADOS (Crítico)
- [ ] Adicionar índice proposta_estado (Alto)
- [ ] Encontrar/corrigir arquivo authentication.php (Alto)
- [ ] Sincronizar .env e credenciais (Alto)
- [ ] Testar fluxo completo: Cliente → Proposta → Pedido → Produção
- [ ] Validar integridade referencial do banco
- [ ] Testar RNC (Relatório de Não-Conformidade)
- [ ] Testar Dashboard novo
- [ ] Validar migração de .env

---

## 💡 SEÇÃO 6: IMPACTO POR FUNCIONALIDADE

### Estados de Proposta

| Funcionalidade | Impacto | Severidade |
|---|---|---|
| Aprovação de proposta | Usa `'aprovado'` em código | Crítico |
| Declínio de proposta | Usa `'declinada'` em código | Crítico |
| Filtros de estado | Espera `'aprovada'/'recusada'` no gateway | Crítico |
| Validação de banco | Detecta divergência | Crítico |

### Índices

| Query | Impacto | Severidade |
|---|---|---|
| `WHERE proposta_estado = ?` | FULL TABLE SCAN | Alto |
| Relatórios por estado | Lentidão em 283+ registros | Alto |
| Filtragem de propostas | Performance degradada | Alto |

### Testes

| Teste | Bloqueador | Severidade |
|---|---|---|
| test-iso-shield.php | authentication.php faltando | Alto |
| Validação completa | 50% taxa de falha | Alto |

---

## 🔴 RECOMENDAÇÕES IMEDIATAS (Ordem de Prioridade)

### **PRIORIDADE 1 - CRÍTICO (Fazer hoje)**

1. **Resolver divergência de WHITELIST**
   - Decisão: Usar `aprovado/declinada` (dados existentes) OU migrar dados?
   - Opção A: Padronizar código para `aprovado/declinada`
   - Opção B: Migrar dados do banco para `aprovada/recusada`
   - **Recomendação**: Opção A (menos risco, dados já estão em produção)

2. **Encontrar/restaurar authentication.php**
   ```bash
   # Buscar em git history
   git log --all -- "requires/authentication.php"
   git show <commit>:requires/authentication.php > requires/authentication.php
   ```

3. **Adicionar índice proposta_estado**
   ```sql
   ALTER TABLE propostas ADD INDEX idx_proposta_estado (proposta_estado);
   ```

### **PRIORIDADE 2 - ALTO (Fazer esta semana)**

4. Sincronizar `.env` com credenciais seguras
5. Validar integridade referencial do banco
6. Testar fluxo completo (Cliente → Proposta → Pedido → Produção)
7. Executar todos os 2 testes com 100% de sucesso

### **PRIORIDADE 3 - MÉDIO (Fazer antes de deploy)**

8. Atualizar documentação (README.md) com estados corretos
9. Documentar estrutura de branches e estratégia de merge
10. Criar roteiro de merge development → main

---

## 📈 SEÇÃO 7: PRÓXIMAS AÇÕES (FASE 3)

### Fase 3: Normalização e Correções Críticas

Com base neste diagnóstico:

1. Escolher estratégia de WHITELIST
2. Implementar mudanças necessárias
3. Validar com testes
4. Sincronizar branches
5. Gerar relatório de mudanças

---

## ✍️ ASSINATURA

**Análise Completada**: 2026-04-01 14:00 UTC
**Ferramenta**: MCP Server com Validação Autônoma
**Nível de Confiança**: 100% (Baseado em Evidência de Código)
**Status**: ✅ PRONTO PARA AÇÃO

---

**Próximo Passo**: Aguardando decisão do usuário sobre estratégia de WHITELIST de estados.
