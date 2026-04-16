# 🚀 PLANO DE SINCRONIZAÇÃO GRADUAL - Evolucao_ISO ← development
**Estratégia**: Implementação em 5 Fases Seguras
**Branch Atual**: Evolucao_ISO
**Direção**: Trazer 13 commits de development para Evolucao_ISO
**Data Início**: 2026-04-01
**Tempo Total Estimado**: 40-50 horas

---

## 📋 ESTRUTURA DAS 5 FASES

```
FASE 1 (4-6h):   Bug Fixes Essenciais
       ↓
FASE 2 (6-8h):   Cálculos Críticos
       ↓
FASE 3 (8-10h):  Integração com APIs
       ↓
FASE 4 (12-16h): UI/UX e Refactoring
       ↓
FASE 5 (4-6h):   Relatórios e Limpeza
       ↓
✅ EVOLUCAO_ISO SINCRONIZADA COM DEVELOPMENT
```

---

## 🔴 FASE 1: BUG FIXES ESSENCIAIS (4-6h)

**Objetivo**: Corrigir issues críticas antes de implementar features

### Commits a Trazer:
1. **fa561e6** - Sincronização RD Station (representante)
2. **c5d8bb6** - Fluxo OTK no cadastro de cliente
3. **822af4d** - CNPJ/CPF e clientes temporários

### Arquivos Afetados:
```
classes/propostas.php
classes/otkweb.php
classes/CnpjCpfNormalizer.php
ajax/propostas.php
ajax/nova-proposta.php
```

### Metodologia de Implementação:

#### PASSO 1.1: Criar branch de work
```bash
git checkout Evolucao_ISO
git pull origin Evolucao_ISO
git checkout -b phase-1-bugfixes
```

#### PASSO 1.2: Cherry-pick commits de bug fix
```bash
git cherry-pick fa561e6
git cherry-pick c5d8bb6
git cherry-pick 822af4d
```

#### PASSO 1.3: Resolver Conflitos (se houver)
- Revisar diferenças em `propostas.php`
- Revisar diferenças em `otkweb.php`
- Revisar diferenças em `CnpjCpfNormalizer.php`

#### PASSO 1.4: Testes
```
☐ Verificar RD Station sync (proposta → RD)
☐ Testar fluxo OTK (novo cliente → OTK)
☐ Validar CNPJ/CPF (com dados reais)
☐ Confirmar clientes temporários funcionam
```

#### PASSO 1.5: Commit em Evolucao_ISO
```bash
git checkout Evolucao_ISO
git merge phase-1-bugfixes
git commit -m "Fase 1: Bug fixes essenciais (3 commits)"
git push origin Evolucao_ISO
```

### ✅ Critério de Sucesso FASE 1:
- [ ] RD Station sincroniza representante corretamente
- [ ] Clientes OTK são criados sem erro
- [ ] CNPJ/CPF são validados corretamente
- [ ] Nenhuma regressão em módulos existentes

---

## 🟡 FASE 2: CÁLCULOS CRÍTICOS (6-8h)

**Objetivo**: Implementar lógica de precificação correta

### Commits a Trazer:
1. **e1a96ba** - Precificação com margem composta
2. **c097032** - Orçamento: markup, custo ajustado, margem contribuição

### Arquivos Afetados:
```
classes/calculadora-core.php
ajax/calculos.php
ajax/novo-orcamento.php
assets/js/novo-orcamento.js
_propostas/proposta.php
```

### Metodologia:

#### PASSO 2.1: Preparar fase 2
```bash
git checkout Evolucao_ISO
git pull origin Evolucao_ISO
git checkout -b phase-2-calculos
```

#### PASSO 2.2: Cherry-pick commits
```bash
git cherry-pick e1a96ba
git cherry-pick c097032
```

#### PASSO 2.3: Revisar Lógica de Cálculos
- Validar implementação de margem composta
- Verificar fórmulas de markup
- Confirmar repasse proporcional

#### PASSO 2.4: Testes Rigorosos
```
☐ Teste de caso 1: Proposta com 1 produto
  Input: Custo=100, Margem=30%
  Esperado: Valor=130 (ou conforme fórmula)

☐ Teste de caso 2: Proposta com múltiplos produtos
  Input: Produtos variados com diferentes margens
  Esperado: Margem composta correta

☐ Teste de caso 3: Proposta com desconto manual
  Input: Desconto=10%
  Esperado: Margem recalculada corretamente

☐ Teste de caso 4: Orçamento com substrato
  Input: Produto + Substrato com custos diferentes
  Esperado: Cálculo com repasse proporcional
```

#### PASSO 2.5: Validar com Dados Reais
```bash
# Comparar com propostas existentes em Evolucao_ISO
# Verificar se valores calculados fazem sentido
# Confirmar que relatórios mostram mesmos valores
```

#### PASSO 2.6: Commit
```bash
git checkout Evolucao_ISO
git merge phase-2-calculos
git commit -m "Fase 2: Cálculos críticos (margem composta, orçamento)"
git push origin Evolucao_ISO
```

### ✅ Critério de Sucesso FASE 2:
- [ ] Margem composta calculada corretamente
- [ ] Markup aplicado corretamente
- [ ] Desconto manual não quebra margem
- [ ] Substrato com repasse proporcional funciona
- [ ] Valores batem com cálculos manuais

---

## 🔵 FASE 3: INTEGRAÇÃO COM APIs (8-10h)

**Objetivo**: Conectar com OTK, RD Station, CNPJ APIs corretamente

### Commits a Trazer:
1. **6275220** - NF-e: rastreio OTK, pré-postagem e pedido local

### Arquivos Afetados:
```
ajax/nfe.php
classes/otkweb.php
pedido-venda.php
migrations/add_pedido_retrabalho.sql (já temos de FASE 1)
```

### Metodologia:

#### PASSO 3.1: Preparar fase 3
```bash
git checkout Evolucao_ISO
git pull origin Evolucao_ISO
git checkout -b phase-3-integracao
```

#### PASSO 3.2: Cherry-pick
```bash
git cherry-pick 6275220
```

#### PASSO 3.3: Validar Integração OTK
```
☐ Testar criação de NF-e simples
☐ Verificar rastreio OTK (PUT /processar)
☐ Validar pré-postagem gerada
☐ Confirmar pedido local sincronizado
```

#### PASSO 3.4: Testes com Sandbox
```bash
# Usar sandbox OTK para testes
# NÃO usar produção ainda
# Validar respostas da API
```

#### PASSO 3.5: Commit
```bash
git checkout Evolucao_ISO
git merge phase-3-integracao
git commit -m "Fase 3: Integração NF-e com OTK e rastreamento"
git push origin Evolucao_ISO
```

### ✅ Critério de Sucesso FASE 3:
- [ ] NF-e gerada sem erro
- [ ] Rastreio OTK funciona em sandbox
- [ ] Pré-postagem criada corretamente
- [ ] Pedido local sincronizado

---

## 🟢 FASE 4: UI/UX E REFACTORING (12-16h)

**Objetivo**: Melhorar interface e experiência do usuário

### Commits a Trazer:
1. **2aa1a2a** - Proposta: exibição de produtos, contato, substrato
2. **09d638b** - PDF e catálogo de motivos declínio
3. **4fbdab4** - Refatoração de listagens com filtros
4. **bcda533** - Flag Retrabalho, cores nas filas, prazo editável
5. **5cf9684** - Modal de contatos com filtro

### Arquivos Afetados:
```
_propostas/proposta.php
_propostas/propostas.php
_propostas/todas-propostas.php
_pedidos/pedido.php
_produtos/produtos.php
template/proposta/modals.php
assets/js/novo-orcamento.js
assets/js/app.js
assets/css/style.css
assets/pages/proposta-*.js
migrations/add_proposta_motivo_declinio.sql
```

### Metodologia:

#### PASSO 4.1: Preparar fase 4
```bash
git checkout Evolucao_ISO
git pull origin Evolucao_ISO
git checkout -b phase-4-ui-ux
```

#### PASSO 4.2: Cherry-pick commits (1 por 1, resolvendo conflitos)
```bash
git cherry-pick 2aa1a2a  # Modal de produtos
git cherry-pick 09d638b  # PDF e declínio
git cherry-pick 4fbdab4  # Listagens refatoradas
git cherry-pick bcda533  # Retrabalho e filas
git cherry-pick 5cf9684  # Modal de contatos
```

#### PASSO 4.3: Resolver Conflitos CSS/JS
- Manter estilos consistes
- Não sobrescrever customizações locais
- Integrar novo layout com existente

#### PASSO 4.4: Testes de Interface
```
☐ Modal de proposta funciona
☐ Exibição de produtos está correta
☐ Contatos aparecem corretamente
☐ Substrato é exibido
☐ PDF gera sem erro
☐ Catálogo de motivos de declínio funciona
☐ Listagens filtram por mês e estado
☐ Toolbar unificada aparece
☐ Flag de retrabalho funciona
☐ Cores nas filas são visíveis
☐ Prazo é editável
☐ Modal de contatos filtra por representante
```

#### PASSO 4.5: QA Visual
```
☐ Layout responsivo (desktop, tablet, mobile)
☐ Cores e fontes consistentes
☐ Ícones carregam corretamente
☐ Animações funcionam
☐ Botões estão acessíveis
```

#### PASSO 4.6: Commit
```bash
git checkout Evolucao_ISO
git merge phase-4-ui-ux
git commit -m "Fase 4: UI/UX e refactoring (5 commits)"
git push origin Evolucao_ISO
```

### ✅ Critério de Sucesso FASE 4:
- [ ] Todos os modais funcionam sem erro
- [ ] Listagens mostram dados corretos
- [ ] Toolbar unificada funciona
- [ ] Nenhuma quebra visual
- [ ] PDF gera corretamente
- [ ] Filtros funcionam

---

## 💜 FASE 5: RELATÓRIOS E LIMPEZA (4-6h)

**Objetivo**: Finalizar com relatórios e sincronização completa

### Commits a Trazer:
1. **9052eeb** - Relatório de pedidos por filial

### Arquivos Afetados:
```
includes/pedidos_venda_relatorio.php
pedidos-venda.php
```

### Metodologia:

#### PASSO 5.1: Preparar fase 5
```bash
git checkout Evolucao_ISO
git pull origin Evolucao_ISO
git checkout -b phase-5-relatorios
```

#### PASSO 5.2: Cherry-pick
```bash
git cherry-pick 9052eeb
```

#### PASSO 5.3: Testes de Relatório
```
☐ Relatório agrupa por filial
☐ Subtotais por filial calculados
☐ Total geral correto
☐ Exportação para Excel funciona
☐ Dados históricos preservados
```

#### PASSO 5.4: Validação Final
```
☐ Nenhum arquivo temp deixado (tmp_*.php)
☐ Banco de dados sincronizado
☐ Logs limpos
☐ Sem erros de PHP
```

#### PASSO 5.5: Commit Final
```bash
git checkout Evolucao_ISO
git merge phase-5-relatorios
git commit -m "Fase 5: Relatórios finais e sincronização completa"
git push origin Evolucao_ISO
```

#### PASSO 5.6: Limpeza
```bash
# Remover branches temporários
git branch -d phase-1-bugfixes
git branch -d phase-2-calculos
git branch -d phase-3-integracao
git branch -d phase-4-ui-ux
git branch -d phase-5-relatorios

# Remover arquivos temporários não rastreados
rm tmp_*.php 2>/dev/null
git status
```

### ✅ Critério de Sucesso FASE 5:
- [ ] Relatório funciona corretamente
- [ ] Nenhum arquivo temporário
- [ ] Evolucao_ISO está sincronizada com todos 13 commits
- [ ] Pronto para substituir main

---

## 📊 RESUMO DE PROGRESSO

| Fase | Commits | Tempo | Status | Checkmark |
|------|---------|-------|--------|-----------|
| 1: Bug Fixes | 3 | 4-6h | ⏳ Pendente | ☐ |
| 2: Cálculos | 2 | 6-8h | ⏳ Pendente | ☐ |
| 3: APIs | 1 | 8-10h | ⏳ Pendente | ☐ |
| 4: UI/UX | 5 | 12-16h | ⏳ Pendente | ☐ |
| 5: Relatórios | 1 | 4-6h | ⏳ Pendente | ☐ |
| **TOTAL** | **13** | **40-50h** | **✅ PRONTO** | **☐** |

---

## 🎯 COMANDOS RÁPIDOS

### Iniciar Fase 1:
```bash
cd C:\Users\RobsonSilva-AfixGraf\Habilidade_de_agente\WORKSPACE\PROJETOS\AfixcontrolAfixgraf
git checkout Evolucao_ISO
git pull origin Evolucao_ISO
git checkout -b phase-1-bugfixes
git cherry-pick fa561e6 c5d8bb6 822af4d
```

### Após cada fase - Merge para Evolucao_ISO:
```bash
git checkout Evolucao_ISO
git merge phase-X-nome
git push origin Evolucao_ISO
```

### Ver progresso:
```bash
git log Evolucao_ISO..development --oneline
# Deve diminuir de 13 para 0 ao final
```

---

## ⚠️ PONTOS CRÍTICOS

1. **Não fazer push para main** - Apenas para Evolucao_ISO
2. **Testar cada fase completamente** - Não pular testes
3. **Documentar conflitos** - Se houver, registrar solução
4. **Backup do database** - Antes de testes críticos
5. **Validar com dados reais** - Não usar dados fake para FASE 2 (cálculos)

---

## ✅ PRÓXIMO PASSO

**INICIAR FASE 1 AGORA?**

Você quer que eu:
- [ ] A) Inicie FASE 1 automaticamente (cherry-pick dos 3 commits)
- [ ] B) Você faz manualmente e me mostra o resultado
- [ ] C) Aguarde sua confirmação para cada passo

**Qual?**

