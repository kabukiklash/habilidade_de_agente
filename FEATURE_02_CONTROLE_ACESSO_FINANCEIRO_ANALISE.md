# 🔐 FEATURE #2: CONTROLE DE ACESSO A INFORMAÇÕES FINANCEIRAS
## Análise Completa + Plano de Implementação Segura

**Commit**: 87515a3
**Data Original**: TBD (estimado 2026-03)
**Repositório**: AfixControl
**Duração Estimada**: 5 horas
**Risco**: **CRÍTICO** (segurança + compliance)
**Prioridade**: **CRÍTICA**
**Tipo**: Feature NOVO (não é bugfix)

---

## 📋 FASE 1: MAPEAMENTO COMPLETO

### O QUE É A FEATURE?

**Problema Identificado**:
- Usuários COM acesso restrito conseguem visualizar dados financeiros (valores, custos, margens)
- Não há validação no frontend E backend para restringir visualização por nível de acesso
- Risco de exposição de informação sensível a usuários não autorizados

**Escopo da Feature**:
1. Validação de nível de acesso do usuário (usuário logado)
2. Mascarar/ocultar campos financeiros para usuários restritos
3. Impedir acesso a dados financeiros via API/AJAX (validation backend)
4. Logs de tentativas de acesso a dados financeiros
5. Validação em:
   - Propostas (valores, custos, margens)
   - Pedidos de venda (frete, serviços adicionais, totais)
   - Dashboard (gráficos de faturamento)
   - Relatórios (valores vendidos, custos, lucros)

---

## 🎯 FASE 2: ARQUIVOS AFETADOS E MODIFICAÇÕES

### ARQUIVO 1: classes/usuario.php (MODIFICAR/CRIAR)

**Cenário**: Classe Usuario precisa ter método para verificar permissões

**Modificações necessárias**:
```php
class Usuario {
    // Propriedade nova
    private $nivelAcesso;  // 'admin', 'gerente', 'operador', 'visualizacao'

    // Método novo
    public function temAcessoFinanceiro() {
        // Retorna true apenas para admin/gerente
        return in_array($this->nivelAcesso, ['admin', 'gerente']);
    }

    public function getNivelAcesso() {
        return $this->nivelAcesso;
    }
}
```

**Linha estimada**: ~50 linhas novas

---

### ARQUIVO 2: ajax/propostas.php (MODIFICAR)

**Modificações necessárias**:

#### PARTE A: Listar propostas (linha ~50)
```php
// ANTES (INSEGURO - mostra valores para todos):
if ($action == 'listar-propostas') {
    $sql = "SELECT proposta_id, proposta_numero, proposta_valor, proposta_custo FROM propostas";
    // ... loop de dados
    echo json_encode($dados);
}

// DEPOIS (SEGURO - filtra por acesso):
if ($action == 'listar-propostas') {
    $usuario = new Usuario();  // Já logado

    // Sempre trazer dados
    $sql = "SELECT proposta_id, proposta_numero, proposta_valor, proposta_custo FROM propostas";

    // MAS ao montar resposta:
    foreach ($propostas as $prop) {
        $item = [
            'proposta_id' => $prop['proposta_id'],
            'proposta_numero' => $prop['proposta_numero'],
        ];

        // APENAS se tem acesso financeiro
        if ($usuario->temAcessoFinanceiro()) {
            $item['proposta_valor'] = $prop['proposta_valor'];
            $item['proposta_custo'] = $prop['proposta_custo'];
            $item['margem'] = ($prop['proposta_valor'] - $prop['proposta_custo']) / $prop['proposta_valor'] * 100;
        } else {
            // Ocultar com placeholder
            $item['proposta_valor'] = '***';
            $item['proposta_custo'] = null;  // Não enviar mesmo
            $item['margem'] = null;
        }

        $dados[] = $item;
    }

    error_log("SEGURANÇA - Acesso a propostas pelo usuário: " . $_SESSION['usuario_id'] .
              ", acesso financeiro: " . ($usuario->temAcessoFinanceiro() ? 'SIM' : 'NÃO'));
}
```

**Linha estimada**: ~30 linhas modificadas

---

#### PARTE B: Obter detalhes de proposta (linha ~200)
```php
if ($action == 'obter-proposta') {
    $proposta_id = $_POST['proposta_id'];
    $usuario = new Usuario();

    $sql = "SELECT * FROM propostas WHERE proposta_id = :proposta_id";
    $stmt = $pdo->prepare($sql);
    $stmt->execute([':proposta_id' => $proposta_id]);
    $proposta = $stmt->fetch();

    // SEMPRE validar acesso
    if (!$usuario->temAcessoFinanceiro()) {
        // Log de tentativa de acesso
        error_log("SEGURANÇA - Tentativa de acesso a dados financeiros por: " . $_SESSION['usuario_id']);

        // Opção 1: Rejeitar completamente (RECOMENDADO)
        exit(json_encode([
            'success' => false,
            'error' => 'Você não tem permissão para acessar informações financeiras'
        ]));

        // Opção 2: Enviar dados sem valores (alternativa menos segura)
        // unset($proposta['proposta_valor']);
        // unset($proposta['proposta_custo']);
    }

    exit(json_encode($proposta));
}
```

**Linha estimada**: ~25 linhas novas/modificadas

---

### ARQUIVO 3: assets/js/novo-orcamento.js (MODIFICAR)

**Modificações necessárias**:

```javascript
// Adição ao início do arquivo
const usuarioTemAcessoFinanceiro = window.acessoFinanceiroPermitido ?? false;

// Em cada função que exibe valores:
function exibirValoresProposta(dados) {
    if (!usuarioTemAcessoFinanceiro) {
        // Ocultar campos de valor
        document.getElementById('proposta-valor-total').style.display = 'none';
        document.getElementById('proposta-margem').style.display = 'none';
        document.getElementById('proposta-custo').style.display = 'none';

        // Ou substituir por placeholder
        document.getElementById('proposta-valor-total').innerText = '***';

        console.warn('Acesso a informações financeiras negado');
        return;
    }

    // Caso contrário, exibir normalmente
    document.getElementById('proposta-valor-total').innerText = dados.proposta_valor;
    document.getElementById('proposta-margem').innerText = dados.margem + '%';
}
```

**Linha estimada**: ~20 linhas novas

---

### ARQUIVO 4: _propostas/proposta.php (TEMPLATE - MODIFICAR)

**Modificações necessárias**:

```php
<?php
// No início do arquivo
$usuario = new Usuario();
$temAcesso = $usuario->temAcessoFinanceiro();
?>

<!-- Em vez de: -->
<!-- <div class="valor">R$ <?php echo number_format($proposta['proposta_valor'], 2, ',', '.'); ?></div> -->

<!-- Fazer: -->
<div class="valor">
    <?php
        if ($temAcesso) {
            echo 'R$ ' . number_format($proposta['proposta_valor'], 2, ',', '.');
        } else {
            echo '<span class="text-muted">***</span>';
        }
    ?>
</div>
```

**Linha estimada**: ~15 linhas modificadas

---

## 🚨 FASE 3: ANÁLISE DE RISCO DE CRASH

### RISCO #1: Objeto Usuario Pode Não Estar Inicializado (ALTO)

**Cenário**: `new Usuario()` falha se a classe não existe ou session não está set

**Onde pode quebrar**:
- Arquivos AJAX que não têm $_SESSION inicializada
- Instância de Usuario que depende de dados não carregados
- Erros silenciosos se Usuario::temAcessoFinanceiro() não existe

**Mitigação**:
```php
// Sempre verificar antes
if (!isset($_SESSION['usuario_id'])) {
    exit(json_encode(['error' => 'Não autenticado']));
}

// Depois criar usuario
if (!class_exists('Usuario')) {
    require_once __DIR__ . '/../classes/usuario.php';
}
$usuario = new Usuario($_SESSION['usuario_id']);
```

---

### RISCO #2: Quebra de Integração RD Station (MÉDIO)

**Cenário**: RD Station API espera campos `proposta_valor` sempre presentes

**Onde pode quebrar**:
- Sincronização com RD Station que tenta acessar valor
- Relatórios que dependem de `proposta_valor` não ser null

**Mitigação**:
- Manter `proposta_valor` no array, apenas omitir da exibição frontend
- RD Station acessa direto do banco, não do JSON retornado
- Testar sincronização RD Station após mudanças

---

### RISCO #3: Regressão em Testes Existentes (MÉDIO)

**Cenário**: Testes que simulam usuários e esperam `proposta_valor` sempre presente

**Onde pode quebrar**:
- `test-propostas.php` ou testes de AJAX
- Queries de relatório que filtram por valor

**Mitigação**:
- Verificar testes que usam propostas
- Atualizar mocks para passar nível de acesso
- Testar com usuário "admin" e usuário "operador"

---

### RISCO #4: Performance - N+1 Queries (BAIXO)

**Cenário**: Verificar `temAcessoFinanceiro()` para cada linha de resposta

**Onde pode quebrar**:
- Listar 100 propostas = 100 verificações de acesso
- Lentidão em relatórios grandes

**Mitigação**:
- Cache permissão do usuário em variável antes do loop
- Não fazer queries adicionais em `temAcessoFinanceiro()` (apenas propriedade)

---

### MATRIZ DE RISCO

| Risco | Severidade | Probabilidade | Impacto | Score | Mitigação |
|-------|-----------|---------------|--------|-------|-----------|
| #1 - Usuario não init | ALTO | MÉDIO | CRÍTICO | 🔴 ALTO | Validar $_SESSION sempre |
| #2 - RD Station quebra | MÉDIO | BAIXO | MÉDIO | 🟡 MÉDIO | Manter BD intocado, filtrar output |
| #3 - Regressão testes | MÉDIO | MÉDIO | MÉDIO | 🟡 MÉDIO | Testar com múltiplos níveis |
| #4 - Performance N+1 | BAIXO | MÉDIO | MÉDIO | 🟡 BAIXO | Cache permissão em variável |

---

## 🛡️ FASE 4: MITIGAÇÃO DETALHADA

### MITIGAÇÃO #1: Padronizar Inicialização de Usuario

Em TODOS os arquivos AJAX que manipulam dados financeiros:

```php
<?php
// Top do arquivo
if (!isset($_SESSION['usuario_id'])) {
    exit(json_encode(['error' => 'Não autenticado']));
}

require_once __DIR__ . '/../classes/usuario.php';
$usuario = new Usuario($_SESSION['usuario_id']);
?>
```

**Arquivos a atualizar**:
- `ajax/propostas.php`
- `ajax/novo-orcamento.php`
- `ajax/pedidos-venda.php` (onde manipula valores)
- `ajax/nfe.php` (onde calcula totais)
- `ajax/relatorios.php` (se existir)

---

### MITIGAÇÃO #2: Testar com Múltiplos Níveis

Criar fixture de usuários para testes:

```php
// test-acesso-financeiro.php
class TestAcessoFinanceiro {

    public function testAdminVeValores() {
        $_SESSION['usuario_id'] = 1;  // admin
        $_SESSION['usuario_nivel'] = 'admin';

        $usuario = new Usuario(1);
        $this->assertTrue($usuario->temAcessoFinanceiro());
    }

    public function testOperadorNaoVeValores() {
        $_SESSION['usuario_id'] = 2;  // operador
        $_SESSION['usuario_nivel'] = 'operador';

        $usuario = new Usuario(2);
        $this->assertFalse($usuario->temAcessoFinanceiro());
    }

    public function testAjaxPropostasFiltra() {
        // Simulate AJAX call with operador
        $_SESSION['usuario_id'] = 2;
        $_POST['action'] = 'listar-propostas';

        ob_start();
        include 'ajax/propostas.php';
        $response = json_decode(ob_get_clean(), true);

        // Verificar que proposta_valor é nulo ou '***'
        $this->assertTrue(is_null($response[0]['proposta_valor']) ||
                          $response[0]['proposta_valor'] === '***');
    }
}
```

---

### MITIGAÇÃO #3: Logs de Segurança

Adicionar ao padrão de todas as operações financeiras:

```php
$acessoPermitido = $usuario->temAcessoFinanceiro();
$acao = $_POST['action'] ?? 'desconhecida';

error_log(json_encode([
    'tipo' => 'ACESSO_FINANCEIRO',
    'usuario_id' => $_SESSION['usuario_id'],
    'acao' => $acao,
    'acesso_permitido' => $acessoPermitido,
    'timestamp' => date('Y-m-d H:i:s'),
    'ip' => $_SERVER['REMOTE_ADDR']
]), 3, __DIR__ . '/../logs/seguranca.log');
```

---

## 🧪 FASE 5: PLANO DE TESTES DETALHADO

### PRÉ-IMPLEMENTAÇÃO
- [ ] Backup do banco de dados
- [ ] Identificar TODOS os arquivos que acessam dados financeiros
- [ ] Mapear quais campos são "financeiros" (valor, custo, margem, frete, etc)
- [ ] Revisar logs de produção (há acessos negados já?)

### TESTES UNITÁRIOS

**Teste 1: Usuario::temAcessoFinanceiro()**
```
Setup: Usuario com nivel = 'admin'
Esperado: Retorna true
Setup: Usuario com nivel = 'operador'
Esperado: Retorna false
```

**Teste 2: AJAX Propostas - Admin vs Operador**
```
Setup: $_SESSION['usuario_nivel'] = 'admin'
Action: listar-propostas
Esperado: JSON contém 'proposta_valor' com valores reais

Setup: $_SESSION['usuario_nivel'] = 'operador'
Action: listar-propostas
Esperado: JSON NÃO contém 'proposta_valor' ou contém null/'***'
```

**Teste 3: AJAX Propostas - Tentativa de Acesso**
```
Setup: $_SESSION['usuario_nivel'] = 'operador'
Action: obter-proposta (com proposal_id=123)
Esperado: erro HTTP 403 ou JSON['error']
Não esperado: dados financeiros no response
```

### TESTES DE INTEGRAÇÃO

- [ ] Login como operador → Listar propostas → Verificar campos ocultados
- [ ] Login como admin → Listar propostas → Verificar todos os campos presentes
- [ ] Operador tenta acessar AJAX diretamente (curl) → Deve ser rejeitado
- [ ] Verificar logs de segurança para cada tentativa de acesso

### TESTES DE REGRESSÃO

- [ ] RD Station consegue sincronizar propostas (acessa banco direto, não JSON)
- [ ] Relatórios de admin funcionam normalmente
- [ ] Dashboard de admin mostra valores corretos
- [ ] UI de proposta não quebra para operador (sem elementos de valor)

---

## 📝 FASE 6: CHECKLIST DE IMPLEMENTAÇÃO

```
PRE-IMPLEMENTAÇÃO:
☐ Backup do banco completo
☐ Verificar documento de usuários e níveis
☐ Listar TODOS os arquivos que acessam dados financeiros
☐ Revisar logs de segurança existentes

IMPLEMENTAÇÃO:
☐ Criar/modificar classes/usuario.php com temAcessoFinanceiro()
☐ Modificar ajax/propostas.php (listar + obter)
☐ Modificar ajax/novo-orcamento.php se necessário
☐ Modificar template _propostas/proposta.php
☐ Adicionar validações no frontend (assets/js/novo-orcamento.js)
☐ Adicionar logs de segurança em todos os AJAX financeiros
☐ Revisar e testar classes/rdstation.php (não quebrar integração)

POS-IMPLEMENTAÇÃO:
☐ Testes unitários passando (all 3)
☐ Testes integração passando (all 4)
☐ Testes regressão passando (all 4)
☐ Logs de segurança sendo registrados corretamente
☐ Verificação final: admin vs operador tem acesso diferente
☐ Documentação atualizada (permissões, níveis)
☐ Commit com mensagem de segurança clara
```

---

## ⚠️ FASE 7: DECISÕES COM CONCILIUM (SE NECESSÁRIO)

**Usar Concilium se**:
- Não conseguir identificar todos os arquivos financeiros
- Encontrar conflito entre acesso financeiro e outro módulo (ex: RD Station)
- Testes falharem de forma inesperada
- Dúvida sobre como tratar "operador" vs "visualizacao"

**Concilium Decision Points**:
1. "Qual é exatamente a hierarquia de acesso? admin > gerente > operador > visualizacao?"
2. "RD Station precisa de acesso aos valores ou apenas de IDs/status?"
3. "Rejeitar (403) ou mascarar (***) para usuários sem acesso?"
4. "Diferentes níveis devem ter diferentes views de dados ou mesma view com valores ocultos?"

---

## 📊 RESUMO EXECUTIVO

| Aspecto | Valor |
|---------|-------|
| **Mapeamento** | ✅ COMPLETO |
| **Arquivos Afetados** | 4-5 (usuario.php, propostas.php, novo-orcamento.js, proposta.php, potencial relatorios) |
| **Linhas Modificadas** | ~90 linhas |
| **Risco Máximo** | **CRÍTICO** (mas mitigável) |
| **Testes Necessários** | 11 (3 unit + 4 integration + 4 regression) |
| **Complexidade** | MÉDIA (múltiplos arquivos, lógica clara) |
| **Pronto para Implementar?** | ⚠️ APÓS APROVAÇÃO DO DESIGN |
| **Necessita Concilium?** | ⚠️ **SIM - ANTES DE IMPLEMENTAR** |

---

## 🎯 PRÓXIMOS PASSOS

**ANTES de implementar:**

1. **APROVAR DESIGN**: Qual é a hierarquia exata de níveis de acesso?
   - [ ] A) 2 níveis: admin (vê tudo) vs operator (não vê financeiro)
   - [ ] B) 4 níveis: admin > gerente > operador > visualizacao
   - [ ] C) 3 níveis: admin > gerente > operador

2. **APROVAR ESTRATÉGIA**: Como tratar usuários sem acesso?
   - [ ] A) Rejeitar com erro (403 Forbidden)
   - [ ] B) Mascarar com "***" mas continuar processamento
   - [ ] C) Omitir campos do JSON (null)

3. **APROVAT ESCOPO**: Quais módulos devem ter validação?
   - [ ] A) Apenas Propostas
   - [ ] B) Propostas + Pedidos
   - [ ] C) Propostas + Pedidos + Dashboard + Relatórios

4. **INTEGRAÇÃO RD STATION**: RD Station precisa dos valores reais?
   - [ ] A) Não, RD Station acessa banco direto (seguro omitir do JSON)
   - [ ] B) Sim, precisa sincronizar valores (manter acesso interno)

**Após aprovação acima, proceder com IMPLEMENTAÇÃO COMPLETA.**

---

**Status**: ✅ ANÁLISE COMPLETA - AGUARDANDO DECISÕES

