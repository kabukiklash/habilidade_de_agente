# 🎓 GUIA PRÁTICO VISUAL - APRENDIZADO PASSO A PASSO

## 1. ENTENDENDO A ARQUITETURA EM 5 MINUTOS

### O Ciclo Completo de um Pedido

```
┌─────────────────────────────────────────────────────────────┐
│                     FIXCONTROL - CICLO COMPLETO             │
└─────────────────────────────────────────────────────────────┘

FASE 1: CRM - PROSPECÇÃO (Semana 1)
═══════════════════════════════════════
Vendedor entra no sistema
       ↓
Busca/Cria Cliente (Classe: Cliente)
       ↓
Visualiza oportunidade (OtkWeb/RDStation)
       ↓
Inicia Proposta (Classe: Proposta)
       ↓
Adiciona Produtos (Classe: Produto)
       ↓
Calcula Custos e Frete
       ↓
Salva Proposta em BD (proposta_id = 123)


FASE 2: NEGOÇÃO - APROVAÇÃO (Semana 2)
════════════════════════════════════════
Proposta enviada ao cliente
       ↓
Cliente aprova proposta (Status = aprovada)
       ↓
Sistema cria Pedido automático (Classe: Pedido)
       ↓
Pedido inicia em estado "APROVADO"
       ↓
Notificação ao setor de produção


FASE 3: PRODUÇÃO - KANBAN (Semana 3-4)
═══════════════════════════════════════════
APROVADO → Pedido validado
       ↓
MONTAGEM → Substrato preparado
       ↓
IMPRESSÃO → Arte impressa
       ↓
PLOTTER → Corte/Aplicação
       ↓
PRODUÇÃO → Finalização manual
       ↓
EMBALAGEM → Preparo para envio
       ↓
FINALIZADO → Pronto para saída


FASE 4: LOGÍSTICA - ENTREGA (Semana 4-5)
═════════════════════════════════════════════
Calcular frete (Classe: Correios)
       ↓
Gerar etiqueta de postagem
       ↓
Enviar para Correios
       ↓
Rastrear entrega
       ↓
✅ Pedido completo!
```

---

## 2. ESTRUTURA FILE-BY-FILE EXPLICADA

### 📄 **connection.php** - A Porta de Entrada
```php
<?php
// /requires/connection.php

// Cria conexão com BD
require_once __DIR__ . "/../layout/classes/database.php";

$db = new Database();
$pdo = $db->getPDO();  // ← OBJETO PRINCIPAL

// Todos os arquivos usam $pdo:
// $cliente = new Cliente($pdo);
// $proposta = new Proposta($pdo);
```

**Por que importa:** Todo arquivo PHP que precisa acessar dados PRECISA desta conexão.

---

### 📄 **authentication.php** - Proteção de Acesso
```php
<?php
// /requires/authentication.php

// Verifica se usuário está autenticado
if (!isset($_SESSION['usuario_id'])) {
    header("Location: login.php");
    exit;
}

// Obtém dados do usuário
$user_id = $_SESSION['usuario_id'];
$level = $_SESSION['usuario_level'];

// Exemplos de níveis:
// level = 1 → Produção (vê só kanban)
// level = 2 → Vendedor (vê apenas CRM)
// level = 3 → Gerente (relatórios)
// level = 99 → Administrador (tudo)
```

---

### 📄 **Classes em /classes** - O Coração

```
/classes/
├── database.php        ← Conexão pura (em /layout/classes)
├── clientes.php        ← Gerencia tabela clientes
├── propostas.php       ← Gerencia tabela propostas
├── pedidos.php         ← Gerencia tabela pedidos
├── produtos.php        ← Gerencia tabela produtos
├── usuarios.php        ← Gerencia usuários + auth
├── montagens.php       ← Gerencia montagens
├── impressoras.php     ← Gerencia impressoras
├── historico.php       ← Log de todas alterações
├── otkweb.php          ← API integração OtkWeb
├── rdstation.php       ← API integração RDStation
├── correios.php        ← API integração Frete
└── global.php          ← Helpers como Modal
```

---

## 3. EXEMPLO PRÁTICO #1: Como um Usuário faz Login

### 🔷 Fluxo Visual

```
┌──────────────┐
│  login.php   │  ← Formulário HTML
│   Username   │
│   Password   │
│  [ENVIAR]    │
└──────────────┘
       ↓ POST
┌──────────────────────────────────┐
│  login.php (processamento)       │
│                                  │
│ 1. Recebe: email + senha         │
│ 2. Cria object: new Usuario($pdo)│
│ 3. Chama: $usuario->Login(...)   │
└──────────────────────────────────┘
       ↓
┌──────────────────────────────────┐
│  Usuario::Login() - classe       │
│                                  │
│ 1. SELECT * FROM usuarios        │
│    WHERE usuario_email = :email  │
│ 2. password_verify(senha)        │
│ 3. Retorna: array com dados      │
└──────────────────────────────────┘
       ↓
┌──────────────────────────────────┐
│  Session iniciada                │
│  $_SESSION['usuario_id'] = 5     │
│  $_SESSION['usuario_level'] = 2  │
│  Redireciona: header("Location")│
└──────────────────────────────────┘
       ↓
✅ Usuário Autenticado!
```

### 🔶 Código Real - Arquivo por Arquivo

**Arquivo: login.php (Formulário)**
```html
<form method="POST">
    <input name="email" type="email" />
    <input name="senha" type="password" />
    <button>Login</button>
</form>

<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    require_once "requires/connection.php";
    require_once "classes/usuarios.php";
    
    $usuario = new Usuario($pdo);
    $resultado = $usuario->Login($_POST['email'], $_POST['senha']);
    
    if ($resultado['sucesso']) {
        $_SESSION['usuario_id'] = $resultado['id'];
        $_SESSION['usuario_level'] = $resultado['nivel'];
        header("Location: index.php");
        exit;
    } else {
        echo "Senha incorreta!";
    }
}
?>
```

**Classe: Usuario.php**
```php
class Usuario {
    public $pdo;
    
    function __construct($pdo) {
        $this->pdo = $pdo;
    }
    
    function Login($email, $senha) {
        // 1️⃣ Busca usuário no banco
        $query = "SELECT usuario_id, usuario_senha, usuario_tipo FROM usuarios 
                  WHERE usuario_email = :email";
        $stmt = $this->pdo->prepare($query);
        $stmt->bindValue(":email", $email);
        $stmt->execute();
        
        // 2️⃣ Se encontrou
        if ($stmt->rowCount() > 0) {
            $usuario = $stmt->fetch(PDO::FETCH_ASSOC);
            
            // 3️⃣ Verifica hash de senha
            if (password_verify($senha, $usuario['usuario_senha'])) {
                return [
                    "sucesso" => true,
                    "id" => $usuario['usuario_id'],
                    "nivel" => $usuario['usuario_tipo']
                ];
            }
        }
        
        return ["sucesso" => false];
    }
}
```

---

## 4. EXEMPLO PRÁTICO #2: Criando uma Proposta

### 🔷 Fluxo Visual

```
VENDEDOR ACESSA:
/nova-proposta.php
       ↓
FORMULÁRIO com campos:
- Cliente (dropdown)
- Produtos (adicionar items)
- Quantidade cada producto
- [SALVAR]
       ↓
JavaScript:
fetch('/ajax/propostas.php', {
  method: 'POST',
  body: JSON.stringify(dados)
})
       ↓
/ajax/propostas.php:
1. Verifica autenticação
2. Valida dados
3. Cria new Proposta($pdo)
4. Chama Proposta::Insert()
       ↓
Proposta::Insert():
1. INSERT INTO propostas (...)
2. Retorna: proposta_id = 456
       ↓
AJAX retorna: {
  status: true,
  id: 456,
  message: "Proposta criada!"
}
       ↓
JavaScript atualiza página
       ↓
✅ Proposta salva em BD!
```

### 🔶 Código Real

**Arquivo: _propostas/nova-proposta.php (Frontend)**
```php
<?php
require_once __DIR__ . "/../requires/connection.php";
require_once __DIR__ . "/../requires/authentication.php";
require_once __DIR__ . "/../classes/propostas.php";
require_once __DIR__ . "/../classes/cliente.php";

$cliente = new Cliente($pdo);
$clientes_lista = $cliente->GetAll();
?>

<form id="form-nova-proposta">
    <select name="cliente_id">
        <?php foreach($clientes_lista as $c) { ?>
            <option value="<?= $c['cliente_id'] ?>">
                <?= $c['cliente_info']->nome ?>
            </option>
        <?php } ?>
    </select>
    
    <!-- Adicionar produtos dinamicamente -->
    <div id="produtos">
        <div class="produto-item">
            <input name="produto_id[]" type="number" />
            <input name="quantidade[]" type="number" />
        </div>
    </div>
    
    <button type="submit">Salvar Proposta</button>
</form>

<script>
document.getElementById('form-nova-proposta').onsubmit = async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const dados = Object.fromEntries(formData);
    
    const response = await fetch('/ajax/propostas.php?acao=criar', {
        method: 'POST',
        body: JSON.stringify(dados),
        headers: { 'Content-Type': 'application/json' }
    });
    
    const resultado = await response.json();
    
    if (resultado.status) {
        alert('Proposta criada com ID: ' + resultado.id);
        window.location.href = '/propostas/' + resultado.id;
    }
};
</script>
```

**Arquivo: ajax/propostas.php (Backend)**
```php
<?php
require_once __DIR__ . "/../requires/connection.php";
require_once __DIR__ . "/../requires/authentication.php";
require_once __DIR__ . "/../classes/propostas.php";

header('Content-Type: application/json');

$acao = $_GET['acao'] ?? '';

if ($acao === 'criar') {
    // 1️⃣ Recebe dados
    $dados = json_decode(file_get_contents('php://input'), true);
    
    // 2️⃣ Validação
    if (!isset($dados['cliente_id']) || !isset($dados['produto_id'])) {
        http_response_code(400);
        echo json_encode(['status' => false, 'erro' => 'Dados incompletos']);
        exit;
    }
    
    // 3️⃣ Instancia classe
    $proposta = new Proposta($pdo);
    
    // 4️⃣ Chama método
    $proposta_id = $proposta->Insert(
        filial: 1,
        cliente: $dados['cliente_id'],
        representante: $_SESSION['usuario_id'],
        identificador: 'PRO-' . date('YmdHis'),
        deal: '',
        frete: []
    );
    
    // 5️⃣ Adiciona produtos
    foreach ($dados['produto_id'] as $k => $produto_id) {
        $proposta->InsertProdutos(
            proposta: $proposta_id,
            produto: $produto_id,
            larg: $dados['larg'][$k],
            alt: $dados['alt'][$k],
            qtd: $dados['quantidade'][$k],
            processos: '',
            margem: 0,
            valor_und: 0,
            valor_custo: 0,
            valor_total: 0,
            resumo: ''
        );
    }
    
    // 6️⃣ Retorna sucesso
    http_response_code(200);
    echo json_encode([
        'status' => true,
        'id' => $proposta_id,
        'mensagem' => 'Proposta criada com sucesso!'
    ]);
}
?>
```

**Classe: Proposta.php (Core)**
```php
class Proposta {
    public $pdo;
    
    function __construct($pdo) {
        $this->pdo = $pdo;
    }
    
    public function Insert($filial, $cliente, $representante, $identificador, $deal, $frete) {
        // 1️⃣ Preparar query
        $query = "INSERT INTO propostas 
                 (proposta_filial, proposta_cliente, proposta_representante, 
                  proposta_identificador, proposta_deal_id, proposta_frete, proposta_criada) 
                 VALUES 
                 (:filial, :cliente, :representante, :identificador, :deal, :frete, NOW())";
        
        // 2️⃣ Prepare statement
        $stmt = $this->pdo->prepare($query);
        
        // 3️⃣ Executar com bind
        $stmt->execute([
            ':filial' => $filial,
            ':cliente' => $cliente,
            ':representante' => $representante,
            ':identificador' => $identificador,
            ':deal' => $deal,
            ':frete' => json_encode($frete)
        ]);
        
        // 4️⃣ Retornar ID da nova proposta
        return $this->pdo->lastInsertId();
    }
    
    public function InsertProdutos($proposta, $produto, $larg, $alt, $qtd, $processos, 
                                   $margem, $valor_und, $valor_custo, $valor_total, $resumo) {
        $query = "INSERT INTO proposta_produtos 
                 (proposta_produto_proposta, proposta_produto_produto, proposta_produto_larg, 
                  proposta_produto_alt, proposta_produto_qtd, proposta_processos, 
                  proposta_produto_margem, proposta_produto_und, proposta_produto_custo, 
                  proposta_produto_total, proposta_resumo) 
                 VALUES 
                 (:proposta, :produto, :larg, :alt, :qtd, :processos, :margem, 
                  :valor_und, :valor_custo, :valor_total, :resumo)";
        
        $stmt = $this->pdo->prepare($query);
        $stmt->execute([
            ':proposta' => $proposta,
            ':produto' => $produto,
            ':larg' => $larg,
            ':alt' => $alt,
            ':qtd' => $qtd,
            ':processos' => $processos,
            ':margem' => $margem,
            ':valor_und' => $valor_und,
            ':valor_custo' => $valor_custo,
            ':valor_total' => $valor_total,
            ':resumo' => $resumo
        ]);
        
        return true;
    }
}
```

---

## 5. EXEMPLO PRÁTICO #3: Movendo um Pedido no Kanban

### 🔷 Fluxo Visual

```
PRODUÇÃO vê Kanban:

┌─────────────────────────────────────┐
│         KANBAN VISUAL               │
├─────────────────────────────────────┤
│                                     │
│ APROVADO    │ MONTAGEM  │ IMPRESSÃO │ 
│ [Pedido123] │          │           │
│             │ [Pedido456]│          │
│             │           │ [Pedido789]│
│             │           │           │
│ PLOTTER     │ PRODUÇÃO  │ EMBALAGEM │
│             │ [Pedido456]│           │
│             │           │ [Pedido789]│
│             │           │           │
└─────────────────────────────────────┘

USUÁRIO ARRASTA Pedido123 para MONTAGEM
       ↓
JavaScript captura evento Drag & Drop
       ↓
Faz requisição AJAX:
fetch('/ajax/pedidos.php', {
  method: 'POST',
  body: JSON.stringify({
    acao: 'atualizar_estado',
    pedido_id: 123,
    novo_estado: 'montagem'
  })
})
       ↓
/ajax/pedidos.php processa:
1. Verifica permissão (level = 1)
2. Valida novo estado
3. Chama Pedido::UpdateEstado()
       ↓
Pedido::UpdateEstado():
UPDATE pedidos SET pedido_estado = :estado
WHERE pedido_id = :id
       ↓
Historico registrado
       ↓
✅ Retorna sucesso JSON
       ↓
Frontend atualiza visual
       ↓
✅ Pedido movido!
```

### 🔶 Código Real

**Arquivo: Kanban JavaScript**
```javascript
// Biblioteca: jQuery UI Draggable
$(document).ready(function() {
    // Fazer itens draggáveis
    $('.pedido-item').draggable({
        revert: "invalid",
        cursor: "move"
    });
    
    // Fazer containers soltem itens
    $('.kanban-coluna').droppable({
        drop: async function(event, ui) {
            const pedido_id = ui.draggable.data('pedido-id');
            const novo_estado = $(this).data('estado');
            
            // Requisição AJAX
            const response = await fetch('/ajax/pedidos.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    acao: 'atualizar_estado',
                    pedido_id: pedido_id,
                    novo_estado: novo_estado
                })
            });
            
            const resultado = await response.json();
            
            if (resultado.status) {
                // Item foi para nova coluna
                $(this).append(ui.draggable);
            } else {
                // Erro - volta para posição anterior
                ui.draggable.revert();
            }
        }
    });
});
```

**Arquivo: ajax/pedidos.php**
```php
<?php
require_once __DIR__ . "/../requires/connection.php";
require_once __DIR__ . "/../requires/authentication.php";
require_once __DIR__ . "/../classes/pedidos.php";
require_once __DIR__ . "/../classes/historico.php";

header('Content-Type: application/json');

$acao = $_GET['acao'] ?? '';

if ($acao === 'atualizar_estado') {
    $dados = json_decode(file_get_contents('php://input'), true);
    
    // 1️⃣ Validação de perfil
    if ($_SESSION['usuario_level'] != 1) {  // level 1 = produção
        http_response_code(403);
        echo json_encode(['status' => false, 'erro' => 'Sem permissão']);
        exit;
    }
    
    // 2️⃣ Estados válidos
    $estados_validos = ['aprovado', 'montagem', 'impressao', 'plotter', 'producao', 'embalagem', 'finalizado'];
    
    if (!in_array($dados['novo_estado'], $estados_validos)) {
        http_response_code(400);
        echo json_encode(['status' => false, 'erro' => 'Estado inválido']);
        exit;
    }
    
    // 3️⃣ Atualizar pedido
    $pedido = new Pedido($pdo);
    $result = $pedido->UpdateEstado($dados['pedido_id'], $dados['novo_estado']);
    
    if ($result) {
        // 4️⃣ Registrar no histórico
        $historico = new Historico($pdo);
        $historico->SalvarHistoricoProduto(
            $dados['pedido_id'],
            $_SESSION['usuario_id'],
            'mudanca_estado'
        );
        
        echo json_encode(['status' => true, 'mensagem' => 'Pedido atualizado']);
    } else {
        http_response_code(500);
        echo json_encode(['status' => false, 'erro' => 'Erro ao atualizar']);
    }
}
?>
```

**Classe: Pedido.php**
```php
class Pedido {
    public $pdo;
    
    function __construct($pdo) {
        $this->pdo = $pdo;
    }
    
    public function UpdateEstado($id, $estado) {
        // Se finalizado, registra timestamp
        if ($estado == "finalizado") {
            $query = "UPDATE pedidos SET pedido_estado = :estado, pedido_finalizado = NOW() 
                      WHERE pedido_id = :id";
        } else {
            $query = "UPDATE pedidos SET pedido_estado = :estado, pedido_finalizado = NULL 
                      WHERE pedido_id = :id";
        }
        
        $stmt = $this->pdo->prepare($query);
        
        $resultado = $stmt->execute([
            ':estado' => $estado,
            ':id' => $id
        ]);
        
        return $stmt->rowCount() > 0;
    }
}
```

---

## 6. REFERÊNCIA RÁPIDA: OPERAÇÕES COMUNS

### ✅ **Criar um Novo Record**
```php
// 1. Instanciar
$cliente = new Cliente($pdo);

// 2. Chamar Insert
$resultado = $cliente->Insert(
    rd_id: null,
    representante: 1,
    cnpj_cpf: '12.345.678/0001-90',
    nome: 'Empresa XYZ',
    detalhes: ['telefone' => '1133334444'],
    endereco: ['rua' => 'Av Principal'],
    contato: ['email' => 'contato@empresa.com']
);

// 3. Resultado
echo $resultado['last_id'];    // ID novo
echo $resultado['codigo'];     // Código clienteel
```

### ✅ **Buscar um Record**
```php
// Busca por ID
$cliente = new Cliente($pdo);
$dados = $cliente->Select(123);

// Resultado
echo $dados['cliente_nome'];
echo $dados['cliente_endereco_entrega'];
```

### ✅ **Actualizar um Record**
```php
$cliente = new Cliente($pdo);

$dados = [
    'codigo' => 123,
    'nome' => 'Novo Nome',
    'detalhes' => [...],
    'endereco' => [...],
    'contato' => [...]
];

$resultado = $cliente->Update($dados);

if ($resultado) {
    echo "Atualizado!";
}
```

### ✅ **Deletar um Record**
```php
$cliente = new Cliente($pdo);

$resultado = $cliente->Delete(123);

if ($resultado) {
    echo "Deletado!";
}
```

### ✅ **Buscar com Filtro**
```php
$cliente = new Cliente($pdo);

// Todos com ORDER BY
$todos = $cliente->GetAll("ORDER BY cliente_codigo DESC");

// Busca por texto
$resultados = $cliente->Search("Empresa");
```

---

## 7. TABELA: MÉTODOS PRINCIPAL CADA CLASSE

| Classe | Métodos Principais |
|--------|-------------------|
| **Cliente** | Insert, Update, Delete, Select, GetAll, Search |
| **Proposta** | Insert, InsertRevisao, InsertProdutos, UpdateProduto, GetAll, Select |
| **Pedido** | InsertPedido, Select, GetAll, UpdateEstado, SelectByProposta |
| **Produto** | Insert, Update, Delete, Select, GetAll |
| **Usuario** | Insert, Login, Delete, Select, GetAll, User |
| **Montagem** | Insert, Delete, Select, GetAll |
| **Impressora** | Insert, Update, Delete, Select, GetAll |
| **Historico** | SalvarHistoricoProduto, ObterHistoricoProduto |
| **OtkWeb** | DetalhesCliente, CarregarOportunidades |
| **RDStation** | CarregarContatos, CarregarOportunidades, AtualizarDeal |
| **Correios** | CalcularFrete, GerarEtiqueta, RastrearEnvio |

---

## 8. CHEAT SHEET: PADRÕES DE CÓDIGO

### 🔷 Novo AJAX Handler
```php
<?php
// /ajax/seu_modulo.php

require_once __DIR__ . "/../requires/connection.php";
require_once __DIR__ . "/../requires/authentication.php";
require_once __DIR__ . "/../classes/sua_classe.php";

header('Content-Type: application/json');

$acao = $_GET['acao'] ?? '';

if ($acao === 'acao1') {
    // código aqui
} else if ($acao === 'acao2') {
    // código aqui
} else {
    http_response_code(400);
    echo json_encode(['status' => false, 'erro' => 'Ação inválida']);
}
?>
```

### 🔷 Nova Classe DAO
```php
<?php
// /classes/sua_tabela.php

class SuaTabela {
    public $pdo;
    
    function __construct($pdo) {
        $this->pdo = $pdo;
    }
    
    public function Insert($param1, $param2) {
        $query = "INSERT INTO sua_tabela (coluna1, coluna2) VALUES (:p1, :p2)";
        $stmt = $this->pdo->prepare($query);
        $stmt->execute([':p1' => $param1, ':p2' => $param2]);
        return $this->pdo->lastInsertId();
    }
    
    public function Select($id) {
        $query = "SELECT * FROM sua_tabela WHERE id = :id";
        $stmt = $this->pdo->prepare($query);
        $stmt->bindValue(":id", $id);
        if ($stmt->execute()) {
            return $stmt->fetch(PDO::FETCH_ASSOC);
        }
    }
    
    public function Update($id, $param1, $param2) {
        $query = "UPDATE sua_tabela SET coluna1 = :p1, coluna2 = :p2 WHERE id = :id";
        $stmt = $this->pdo->prepare($query);
        $stmt->execute([':p1' => $param1, ':p2' => $param2, ':id' => $id]);
        return $stmt->rowCount() > 0;
    }
    
    public function Delete($id) {
        $query = "DELETE FROM sua_tabela WHERE id = :id";
        $stmt = $this->pdo->prepare($query);
        $stmt->bindValue(":id", $id);
        return $stmt->execute();
    }
    
    public function GetAll($filtro = '') {
        $query = "SELECT * FROM sua_tabela $filtro";
        $stmt = $this->pdo->prepare($query);
        if ($stmt->execute()) {
            return $stmt->fetchAll();
        }
    }
}
?>
```

---

## 9. PROBLEMAS COMUNS E SOLUÇÕES

### ❌ **Problema: "Call to a member function prepare() on null"**

Significa que `$pdo` não foi inicializado.

```php
// ❌ Errado
$proposta = new Proposta();  // Sem PDO!

// ✅ Correto
require_once "requires/connection.php";
$proposta = new Proposta($pdo);  // Com PDO!
```

---

### ❌ **Problema: "SQLSTATE[42S22]: Column not found"**

Nome de coluna errado na query.

```php
// ❌ Errado
$query = "SELECT cliente_nive FROM clientes";  // Coluna não existe

// ✅ Correto
$query = "SELECT cliente_codigo FROM clientes";  // Coluna correta
```

---

### ❌ **Problema: "Header already sent"**

Tentou redirecionar após enviar conteúdo.

```php
// ❌ Errado
echo "Algo";
header("Location: index.php");  // Erro!

// ✅ Correto
header("Location: index.php");  // Deve ser antes
exit;
```

---

### ❌ **Problema: AJAX retorna JSON quebrado**

Geralmente há `echo` antes do JSON.

```php
// ❌ Errado
echo "Debug: " . $var;
echo json_encode($dados);  // JSON inválido

// ✅ Correto
header('Content-Type: application/json');
echo json_encode($dados);  // JSON puro
```

---

## 10. FLUXOGRAMA: SELECIONANDO ARQUIVOS PARA ESTUDAR

```
┌─────────────────────────────┐
│  Quero aprender sobre:      │
├─────────────────────────────┤
│                             │
├─ Conexão com BD ────→ /layout/classes/database.php
│
├─ Autenticação ──────→ /requires/authentication.php + /classes/usuarios.php
│
├─ CRUD básico ───────→ /classes/cliente.php
│
├─ Fluxo CRM ─────────→ /classes/proposta.php → /classes/pedido.php
│
├─ Produção ──────────→ Kanban JS + /ajax/pedidos.php
│
├─ Integrações ───────→ /classes/otkweb.php, rdstation.php, correios.php
│
├─ Frontend ──────────→ /template/*.php
│
├─ AJAX ───────────────→ /ajax/*.php
│
└─ Tudo junto ───────→ Trace: /nova-proposta.php → /ajax/propostas.php → Proposta::Insert()
```

---

## 11. ROTEIROS DE ESTUDO RECOMENDADOS

### 🟩 **INICIANTE (Semana 1)**
- [ ] Leia `ANALISE_UML_COMPLETA.md` - Seções 1-5
- [ ] Estude `/layout/classes/database.php`
- [ ] Estude `/classes/cliente.php` completamente
- [ ] Rode um `SELECT * FROM clientes` localmente
- [ ] Faça Insert/Update/Delete manual no banco
- [ ] Revise autenticação básica

**Tempo:** 10-15 horas

---

### 🟨 **INTERMEDIÁRIO (Semana 2)**
- [ ] Estude `/classes/proposta.php` + Relacionamentos
- [ ] Estude `/classes/pedido.php` + Estados
- [ ] Trace fluxo: Proposta → Pedido
- [ ] Estude um AJAX handler completo
- [ ] Implemente um novo AJAX handler simples
- [ ] Familiarizar-se com Bootstrap templates

**Tempo:** 15-20 horas

---

### 🟥 **AVANÇADO (Semana 3-4)**
- [ ] Estude `/classes/otkweb.php` - HTTP Client
- [ ] Estude `/classes/correios.php` - API integrações
- [ ] Leia `UML_AVANCADO_HERANCA_E_PADROES.md`
- [ ] Propose refatoração (herança base)
- [ ] Implemente novo módulo completo
- [ ] Otimize queries lentas

**Tempo:** 20-30 horas

---

## 12. EXERCÍCIOS PRÁTICOS

### 🎯 **Exercício 1: Criar Cliente via Interface**
1. Entre em novo-cliente.php
2. Preencha todos os campos
3. Clique Salvar
4. Verifique no BD se Cliente foi criado
5. Edite cliente
6. Delete cliente

**Objetivo:** Entender fluxo CRUD básico

---

### 🎯 **Exercício 2: Criar Proposta com Produtos**
1. Acesse nova-proposta.php
2. Selecione cliente
3. Adicione 2-3 produtos
4. Salve proposta
5. Veja detalhes em BD
6. Edite um produto da proposta

**Objetivo:** Entender relacionamento 1:N (Proposta → Produtos)

---

### 🎯 **Exercício 3: Drag & Drop Kanban**
1. Crie um pedido (via proposta aprovada)
2. Vá para produção.php
3. Veja Kanban
4. Arraste pedido pela coluna
5. Observe mudança de estado em BD

**Objetivo:** Entender mudança de estado + AJAX

---

### 🎯 **Exercício 4: Criar Nova Classe**
1. Crie `/classes/comentarios.php` (já existe, estude)
2. Adicione método: `GetByProposta($proposta_id)`
3. Use em `/ajax/comentarios.php`
4. Crie interface para exibir comentários

**Objetivo:** Criar DAO nova + usar em AJAX

---

## 13. DICIONÁRIO DE TERMOS

| Termo | Significado |
|-------|-------------|
| **DAO** | Data Access Object - Classe que acessa dados |
| **PDO** | PHP Data Objects - Driver do MySQL |
| **Prepared Statement** | Query preparada para mais segurança |
| **Bind** | Passar valores seguros à query |
| **AJAX** | Requisição assíncrona sem recarregar página |
| **JSON** | Formato de troca de dados (JavaScript Object Notation) |
| **Kanban** | Método visual de gestão (quadro com cards) |
| **Estado** | Situação atual de um pedido (aprovado, montagem, etc) |
| **ORM** | Object-Relational Mapping - Mapear tabelas a classes |
| **API** | Interface para integração com sistemas externos |
| **Integração** | Conexão com outro sistema (OtkWeb, RDStation) |
| **Composição** | Quando classe contém outras (1:N - Proposta possui Produtos) |
| **Agregação** | Quando classe referencia outras (Pedido referencia Proposta) |
| **Herança** | Classe filha herda propriedades da classe pai |

---

**Próximo passo:** Abra VS Code, defina breakpoints no código, e execute passo a passo!

