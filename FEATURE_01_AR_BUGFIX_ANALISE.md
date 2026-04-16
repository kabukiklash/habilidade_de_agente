# 🔧 FEATURE #1: BUG FIX AR ViPP
## Análise Completa + Plano de Implementação Segura

**Commit**: 83368a1
**Data Original**: 2026-02-20
**Autor Original**: guisilvaafix
**Duração Estimada**: 2 horas
**Risco**: MÉDIO (mas bem documentado)
**Prioridade**: CRÍTICA

---

## 📋 FASE 1: MAPEAMENTO COMPLETO

### O QUE É O BUG?

**Problema**: Serviço AR (Aviso de Recebimento) era ativado por padrão mesmo quando não solicitado

**Cenário do Bug**:
1. Usuário cria etiqueta Correios SEM solicitar AR
2. Payload enviado para ViPP tem campo `AdicionaisVolume` vazio
3. ViPP interpreta campo vazio como "usar configuração padrão"
4. Perfil ViPP padrão tem AR ativado
5. **Resultado**: AR adicionado sem custo apropriado, cliente não cobrado

**Impacto**: Perda financeira, inconsistência de custos, falha na cobrança

---

### MUDANÇAS EXATAS DO COMMIT

#### **Arquivo 1: ajax/pedidos-venda.php**

**Antes (BUGADO):**
```php
'Volumes' => [
    [
        'ValorDeclarado' => '',
        'AdicionaisVolume' => '',  // ← CAMPO SEMPRE PRESENTE (mesmo vazio!)
        'VlrACobrar' => '',
        'Etiqueta' => ''
    ]
]
```

**Depois (CORRIGIDO):**
```php
'Volumes' => [
    [
        'Etiqueta' => ''  // ← Só campos essenciais
    ]
]

// Adicionar serviços APENAS se solicitados
if (!empty($adicionais)) {
    $dados_vipp['Volumes'][0]['AdicionaisVolume'] = implode(',', $adicionais);
} else {
    // CRÍTICO: Remover campo se vazio
    unset($dados_vipp['Volumes'][0]['AdicionaisVolume']);  // ← FIX PRINCIPAL
}
```

**Mudanças de Formatação:**
```php
// ANTES: Usar vírgula como decimal
'ValorDeclarado' => number_format($valor_total, 2, ',', '');

// DEPOIS: Usar ponto como decimal (padrão internacional)
'ValorDeclarado' => number_format($valor_total, 2, '.', '');
```

**Logs Adicionados:**
```php
error_log("ViPP - Serviço AR solicitado");
error_log("ViPP - Valor Declarado solicitado: " . $valor_total);
error_log("ViPP - Gerando etiqueta ... AR: " . ($servico_ar ? 'SIM' : 'NÃO'));
```

---

#### **Arquivo 2: ajax/prepostagem.php**

**Antes (BUGADO):**
```php
if (!empty($resumo['listaServicoAdicional'][0])) {
    if ($resumo['listaServicoAdicional'][0]['siglaServicoAdicional'] == "AR") {
        $ar = '<a ...>AR</a>';
    }
} else {
    $ar = "";
}
// ↑ PROBLEMA: Não verifica ViPP AdicionaisVolume
```

**Depois (CORRIGIDO):**
```php
$ar = "";
$has_ar = false;

// Suportar AMBOS: Correios CWS (antiga) + ViPP (nova)
if (!empty($resumo['listaServicoAdicional'])) {
    // CWS
    foreach ($resumo['listaServicoAdicional'] as $servico_adicional) {
        if (($servico_adicional['siglaServicoAdicional'] ?? '') == "AR") {
            $has_ar = true;
            break;
        }
    }
} elseif (!empty($resumo['Volumes'][0]['AdicionaisVolume'])) {
    // ViPP
    if (strpos($resumo['Volumes'][0]['AdicionaisVolume'], 'AR') !== false) {
        $has_ar = true;
    }
}

if ($has_ar) {
    $id_link = !empty($prepostagem['prepostagem_codigo_objeto'])
        ? $prepostagem['prepostagem_codigo_objeto']
        : $id;
    $ar = '<a href="ar?ids=' . $id_link . '">AR</a>';
}
```

---

## 🚨 FASE 2: ANÁLISE DE RISCO DE CRASH

### RISCOS IDENTIFICADOS

#### **RISCO #1: Incompatibilidade com Payloads Antigos (MÉDIO)**

**Cenário**: Evolucao_ISO pode ter código que ESPERA `AdicionaisVolume` sempre presente

**Onde pode quebrar**:
- Logs que tentam acessar `$dados_vipp['Volumes'][0]['AdicionaisVolume']` sem verificar existência
- Frontend que tenta exibir campo vazio
- API ViPP que recebe payload sem o campo

**Evidência**: Linha que faz `unset()` é NOVA - pode quebrar código legado

---

#### **RISCO #2: Mudança de Formatação de Valor (MÉDIO)**

**Antes**: `number_format($valor_total, 2, ',', '')` → "123,45"
**Depois**: `number_format($valor_total, 2, '.', '')` → "123.45"

**Cenário**: ViPP espera ponto, mas código legado envia vírgula?

**Onde pode quebrar**:
- Se código em Evolucao_ISO usa vírgula em lugar errado
- Se ViPP rejeita vírgula

---

#### **RISCO #3: Lógica de Detecção de AR em prepostagem.php (BAIXO)**

**Novo código**:
```php
if (!empty($resumo['listaServicoAdicional'])) {
    // CWS
} elseif (!empty($resumo['Volumes'][0]['AdicionaisVolume'])) {
    // ViPP
}
```

**Cenário**: E se ambas as estruturas existem?
- **Probabilidade**: BAIXA (nunca devem estar juntas)
- **Impacto**: Mostraria AR apenas se CWS presente, ignoraria ViPP

---

#### **RISCO #4: Código Morto / Regressão (BAIXO)**

**O que foi removido**:
```php
'ValorDeclarado' => '',  // Removido
'VlrACobrar' => '',      // Removido
```

**Cenário**: Código legado que depende desses campos vazios?

**Probabilidade**: BAIXA (campos estavam sempre vazios)

---

### MATRIZ DE RISCO

| Risco | Severidade | Probabilidade | Impacto | Score | Mitigação |
|-------|-----------|---------------|--------|-------|-----------|
| #1 - Payload Antigo | MÉDIO | MÉDIO | ALTO | 🔴 MÉDIO | Grep busca |
| #2 - Formatação Valor | MÉDIO | BAIXO | MÉDIO | 🟡 BAIXO | Teste ViPP |
| #3 - Lógica AR Dupla | BAIXO | BAIXA | MÉDIO | 🟢 BAIXO | Teste UI |
| #4 - Código Morto | BAIXO | MUITO BAIXA | BAIXO | 🟢 MUITO BAIXO | Grep busca |

---

## 🛡️ FASE 3: MITIGAÇÃO DE RISCOS

### MITIGAÇÃO #1: Verificar Código Legado

```bash
# Procurar por acessos a AdicionaisVolume
grep -rn "AdicionaisVolume" --include="*.php" --include="*.js"

# Procurar por acessos a ValorDeclarado/VlrACobrar
grep -rn "ValorDeclarado\|VlrACobrar" --include="*.php" --include="*.js"
```

**Ação**: Se encontrar, adaptar código para verificar existência do campo

---

### MITIGAÇÃO #2: Testar com ViPP Real

- Gerar etiqueta **SEM** solicitar AR
- Verificar payload enviado a ViPP (checar logs)
- Confirmar que `AdicionaisVolume` NÃO aparece no JSON
- Gerar etiqueta **COM** solicitar AR
- Confirmar que `AdicionaisVolume` contém "AR"

---

### MITIGAÇÃO #3: Testar Formatação de Valor

- Valor com casas decimais: "123.45"
- Valor redondo: "100.00"
- Valor zero: "0.00"
- Verificar se ViPP aceita

---

### MITIGAÇÃO #4: Testar Lógica de Detecção AR

- Prepostagem CWS com AR → Deve mostrar botão AR
- Prepostagem ViPP com AR → Deve mostrar botão AR
- Prepostagem SEM AR → Não deve mostrar botão

---

## 🧪 FASE 4: PLANO DE TESTES

### PRÉ-IMPLEMENTAÇÃO

- [ ] Backup de Evolucao_ISO feito
- [ ] Grep para detectar incompatibilidades
- [ ] Revisar logs de produção (há erros relacionados a AR?)

### TESTES UNITÁRIOS

- [ ] **Teste 1**: Payload SEM AR
  ```
  Esperado: Array ['Volumes'][0] NÃO contém 'AdicionaisVolume'
  ```

- [ ] **Teste 2**: Payload COM AR
  ```
  Esperado: Array ['Volumes'][0]['AdicionaisVolume'] = 'AR'
  ```

- [ ] **Teste 3**: Formatação de Valor
  ```
  Esperado: "123.45" com ponto (não "123,45" com vírgula)
  ```

### TESTES DE INTEGRAÇÃO

- [ ] Gerar etiqueta pelo UI
- [ ] Verificar payload em logs/network inspector
- [ ] Prepostagem lista AR corretamente
- [ ] Clicar em botão AR leva a página correta

### TESTES DE REGRESSÃO

- [ ] Etiquetas antigas ainda funcionam
- [ ] Relatórios de AR não quebram
- [ ] UI de prepostagem não tem erros

---

## 📝 FASE 5: CHECKLIST DE IMPLEMENTAÇÃO

```
PRE-IMPLEMENTAÇÃO:
☐ Backup de Evolucao_ISO criado
☐ Clonar código de development exatamente
☐ Grep para verificar incompatibilidades
☐ Revisar logs de produção

IMPLEMENTAÇÃO:
☐ Modificar ajax/pedidos-venda.php (Linhas do fix)
☐ Modificar ajax/prepostagem.php (Linhas do fix)
☐ Adicionar logs conforme commit
☐ Testar localmente

POS-IMPLEMENTAÇÃO:
☐ Testes unitários passando
☐ Testes integração passando
☐ Regressão verificada
☐ Documentação atualizada
☐ Commit criado com Co-Author
```

---

## ⚠️ FASE 6: DECISÃO COM CONCILIUM (SE NECESSÁRIO)

**Usar Concilium se**:
- Grep encontrar incompatibilidades críticas
- Testes falharem de forma inesperada
- Análise mostrar que mudar formato de valor afeta muitos lugares

**Concilium Decision Points**:
1. "Devemos migrar TODOS os valores para usar '.' em vez de ','?"
2. "Se código legado quebrar, revert ou fix forward?"
3. "Sincronizar prepostagem.php em 100% ou manter compatibilidade?"

---

## 📊 RESUMO EXECUTIVO

| Aspecto | Status |
|---------|--------|
| **Mapeamento** | ✅ COMPLETO |
| **Arquivos Afetados** | 2 (pedidos-venda.php, prepostagem.php) |
| **Linhas Modificadas** | ~35 linhas |
| **Risco Máximo** | MÉDIO (mitigável) |
| **Testes Necessários** | 7 (unit + integration) |
| **Pronto para Implementar?** | ✅ SIM |
| **Necessita Concilium?** | ⚠️ TALVEZ (após grep) |

---

## 🎯 PRÓXIMO PASSO

**Confirmar antes de implementar**:

- [ ] A) Rodar Grep para verificar incompatibilidades (recomendado)
- [ ] B) Partir direto para implementação
- [ ] C) Cancelar e passar para Feature #2

**Qual você quer?**
