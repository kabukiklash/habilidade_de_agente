# 📋 TABELAS DE REFERÊNCIA RÁPIDA

## 1. TABELA: CLASSES E SEUS MÉTODOS

```
┌──────────────────┬──────────────────────────────────────────────┐
│ Classe: CLIENTE  │ Arquivo: /classes/clientes.php               │
├──────────────────┼──────────────────────────────────────────────┤
│ Construtor       │ __construct($pdo)                            │
│ Criar            │ Insert(representante, cnpj_cpf, nome, ...)  │
│ Ler              │ Select(id) / SelectByCode(codigo)            │
│ Atualizar        │ Update(dados)                                │
│ Deletar          │ Delete(id)                                   │
│ Listar           │ GetAll(increment)                            │
│ Buscar           │ Search(pesquisa)                             │
│ Retorna          │ Array com dados do cliente                   │
└──────────────────┴──────────────────────────────────────────────┘

┌──────────────────┬──────────────────────────────────────────────┐
│ Classe: PROPOSTA │ Arquivo: /classes/propostas.php              │
├──────────────────┼──────────────────────────────────────────────┤
│ Construtor       │ __construct($pdo)                            │
│ Criar            │ Insert(filial, cliente, representante, ...) │
│ Rev. Proposta    │ InsertRevisao(...)                           │
│ Add Produto      │ InsertProdutos(proposta, produto, ...)      │
│ Edit Produto     │ UpdateProduto(id, produto, ...)             │
│ Ler              │ Select(id)                                   │
│ Ler Produtos     │ GetProdutos(proposta_id)                     │
│ Listar           │ GetAll(increment)                            │
│ Retorna          │ Array com dados da proposta                  │
└──────────────────┴──────────────────────────────────────────────┘

┌──────────────────┬──────────────────────────────────────────────┐
│ Classe: PEDIDO   │ Arquivo: /classes/pedidos.php                │
├──────────────────┼──────────────────────────────────────────────┤
│ Construtor       │ __construct($pdo)                            │
│ Criar            │ InsertPedido(proposta, cliente, ...)        │
│ Ler              │ Select(id) / SelectByProposta(proposta)      │
│ Listar           │ GetAll(increment)                            │
│ Atualizar Estado │ UpdateEstado(id, estado)                    │
│ Estados Válidos  │ aprovado, montagem, impressao, plotter, ... │
│ Retorna          │ Array com dados do pedido                    │
└──────────────────┴──────────────────────────────────────────────┘

┌──────────────────┬──────────────────────────────────────────────┐
│ Classe: USUARIO  │ Arquivo: /classes/usuarios.php               │
├──────────────────┼──────────────────────────────────────────────┤
│ Construtor       │ __construct($pdo)                            │
│ Criar            │ Insert(nome, email, senha, tipo)            │
│ Login            │ Login(email, senha)                          │
│ Verificar Existe │ Exists(email)                                │
│ Ler              │ Select(id) / SelectByCodigo(codigo)          │
│ Por Token        │ User(token)                                  │
│ Listar           │ GetAll(increment)                            │
│ Deletar          │ Delete(id)                                   │
│ Retorna          │ Array com usuario ou boolean                 │
└──────────────────┴──────────────────────────────────────────────┘

┌──────────────────┬──────────────────────────────────────────────┐
│ Classe: PRODUTO  │ Arquivo: /classes/produtos.php               │
├──────────────────┼──────────────────────────────────────────────┤
│ Construtor       │ __construct($pdo)                            │
│ Criar            │ Insert(codigo, finalidade, substrato, ...)  │
│ Atualizar        │ Update(id, codigo, finalidade, ...)         │
│ Deletar          │ Delete(id)                                   │
│ Ler              │ Select(id)                                   │
│ Listar           │ GetAll(pdo, increment)                       │
│ Retorna          │ Array com dados do produto                   │
└──────────────────┴──────────────────────────────────────────────┘

```

---

## 2. TABELA: ESTADOS DO PEDIDO / KANBAN (12 Estados Reais na Produção)

```
┌───────────────────────────────────────────────────────────────┐
│ ESTADO                │ DESCRIÇÃO              │ PRÓXIMO ESTADO      │
├───────────────────────────────────────────────────────────────┤
│ APROVADOS             │ Proposta aprovada     │ FILA MONTAGEM       │
│                       │ Pronto para produção  │                     │
├───────────────────────────────────────────────────────────────┤
│ FILA DE MONTAGEM      │ Aguardando início     │ MONTANDO            │
│                       │ Na fila de produção   │                     │
├───────────────────────────────────────────────────────────────┤
│ MONTANDO              │ Substrato preparado   │ FILA IMPRESSÃO      │
│                       │ Materiais selecionados│                     │
├───────────────────────────────────────────────────────────────┤
│ FILA DE IMPRESSÃO     │ Aguardando impressora │ IMPRIMINDO          │
│                       │ Máquina ocupada       │                     │
├───────────────────────────────────────────────────────────────┤
│ IMPRIMINDO            │ Arte sendo impressa   │ IMPRESSOS           │
│                       │ Validação visual      │                     │
├───────────────────────────────────────────────────────────────┤
│ IMPRESSOS             │ Impressão concluída   │ LASER/CORROSÃO      │
│                       │ Aguardando corte      │                     │
├───────────────────────────────────────────────────────────────┤
│ LASER/CORROSÃO        │ Corte especial        │ PLOTTER             │
│                       │ Gravação laser        │                     │
├───────────────────────────────────────────────────────────────┤
│ PLOTTER               │ Corte/Aplicação       │ PRODUÇÃO            │
│                       │ Vinil/Adesivo         │                     │
├───────────────────────────────────────────────────────────────┤
│ PRODUÇÃO              │ Finalização manual    │ PEDIU NOTA          │
│                       │ QA checks             │                     │
├───────────────────────────────────────────────────────────────┤
│ PEDIU NOTA ⭐         │ NF-e solicitada       │ DISP. RETIRADA      │
│                       │ Cria PV (Pedido Venda)│                     │
│                       │ Emite NF-e (OTKWeb)   │                     │
├───────────────────────────────────────────────────────────────┤
│ DISP. P/ RETIRADA     │ NF-e emitida          │ FINALIZADOS         │
│                       │ Etiqueta gerada (ViPP)│                     │
├───────────────────────────────────────────────────────────────┤
│ FINALIZADOS           │ Entregue/Retirado     │ [CICLO COMPLETO]    │
│                       │ Pedido concluído      │                     │
└───────────────────────────────────────────────────────────────┘

🔄 TRANSIÇÕES NÃO PERMITIDAS:
- Voltar para estado anterior
- Pular estados (ex: APROVADO → PLOTTER)
- Mudança sem validação

📝 REGRAS:
- Cada mudança registra timestamp
- Historico registra usuario + mudança
- Pedido finalizado = não pode voltar
- "Pediu Nota" = gatilho para criar Pedido de Venda

🔗 PONTE PRODUÇÃO → FATURAMENTO:
- Estado "Pediu Nota" → Cria registro em pedidos_venda
- OTKWeb API emite NF-e → Estado PV: processado → emitido
- ViPP Correios gera etiqueta → Código rastreamento vinculado
```

---

## 3. TABELA: NÍVEIS DE USUÁRIO (RBAC)

```
┌──────────┬─────────────────┬────────────────────────────────┐
│ LEVEL    │ TIPO             │ ACESSO                         │
├──────────┼─────────────────┼────────────────────────────────┤
│ 1        │ PRODUÇÃO        │ ✓ Kanban                       │
│          │                 │ ✓ Alterar estado pedido        │
│          │                 │ ✗ CRM                          │
│          │                 │ ✗ Relatórios                   │
├──────────┼─────────────────┼────────────────────────────────┤
│ 2        │ VENDEDOR        │ ✓ CRM Completo                 │
│          │                 │ ✓ Criar Propostas             │
│          │                 │ ✓ Ver Clientes                 │
│          │                 │ ✓ Calcular Orçamentos         │
│          │                 │ ✗ Deletar Propostas           │
│          │                 │ ✗ Admin                        │
├──────────┼─────────────────┼────────────────────────────────┤
│ 3        │ GERENTE         │ ✓ Tudo de Vendedor            │
│          │                 │ ✓ Relatórios                   │
│          │                 │ ✓ Dashboard                    │
│          │                 │ ✓ Ver Desempenho              │
│          │                 │ ✗ Deletar Registros           │
│          │                 │ ✗ Admin                        │
├──────────┼─────────────────┼────────────────────────────────┤
│ 99       │ ADMINISTRADOR   │ ✓ TUDO                         │
│          │                 │ ✓ Criar Usuários              │
│          │                 │ ✓ Deletar Registros           │
│          │                 │ ✓ Configurações               │
│          │                 │ ✓ Backup                      │
└──────────┴─────────────────┴────────────────────────────────┘
```

---

## 4. TABELA: ESTRUTURA DE DIRETÓRIOS (MAPEADO)

```
┌──────────────────────────────────────────────────────────────┐
│ ESTRUTURA DO PROJETO                                         │
├──────────────────────────────────────────────────────────────┤
│ Raiz/                                                        │
│ ├── /classes/                    [MODELOS - DAO]            │
│ │   ├── afixcontrol.php          Orquestração geral        │
│ │   ├── clientes.php             Gestão clientes           │
│ │   ├── propostas.php            Gestão propostas          │
│ │   ├── pedidos.php              Gestão pedidos            │
│ │   ├── produtos.php             Catálogo produtos         │
│ │   ├── usuarios.php             Auth + usuarios           │
│ │   ├── montagens.php            Substrato + serviços      │
│ │   ├── impressoras.php          Equipamentos              │
│ │   ├── comentarios.php          Comentários               │
│ │   ├── historico.php            Auditoria                 │
│ │   ├── otkweb.php               Integração OtkWeb        │
│ │   ├── rdstation.php            Integração RDStation     │
│ │   ├── correios.php             Integração Frete         │
│ │   └── global.php               Helpers (ex: Modal)       │
│ │                                                           │
│ ├── /layout/classes/                                         │
│ │   └── database.php             PDO Connection            │
│ │                                                           │
│ ├── /requires/                   [CONFIGURAÇÃO]            │
│ │   ├── connection.php           Inicializa $pdo          │
│ │   └── authentication.php       Verifica autenticação    │
│ │                                                           │
│ ├── /includes/                   [UTILITÁRIOS]             │
│ │   └── (helpers diversos)                                 │
│ │                                                           │
│ ├── /ajax/                       [HANDLERS AJAX]           │
│ │   ├── propostas.php            CRUD Propostas           │
│ │   ├── pedidos.php              CRUD Pedidos             │
│ │   ├── clientes.php             CRUD Clientes            │
│ │   ├── calculos-orcamento.php   Cálculos                 │
│ │   ├── correios.php             Frete                    │
│ │   └── (30+ handlers mais)                               │
│ │                                                           │
│ ├── /api/                        [REST API]                │
│ │   ├── propostas.php            API Propostas            │
│ │   ├── pedidos.php              API Pedidos              │
│ │   └── (endpoints mais)                                  │
│ │                                                           │
│ ├── /template/                   [VIEWS HTML]              │
│ │   ├── header.php               Head + CSS                │
│ │   ├── sidebar.php              Menu lateral              │
│ │   ├── top_header.php           Header topo              │
│ │   └── (views diversas)                                  │
│ │                                                           │
│ ├── /_clientes/                  [MÓDULO CLIENTES]         │
│ │   ├── novo-cliente.php         Nova cliente             │
│ │   ├── clientes.php             Listar clientes          │
│ │   └── alterar-cliente.php      Editar cliente           │
│ │                                                           │
│ ├── /_propostas/                 [MÓDULO PROPOSTAS]        │
│ │   ├── nova-proposta.php        Nova proposta            │
│ │   ├── propostas.php            Listar propostas         │
│ │   └── proposta.php             Ver detalhe              │
│ │                                                           │
│ ├── /_pedidos/                   [MÓDULO PEDIDOS]          │
│ │   └── pedidos.php              Gestão pedidos           │
│ │                                                           │
│ ├── /_configuracoes/             [CONFIGURAÇÕES]           │
│ │   ├── configuracoes.php        Sistema                  │
│ │   └── criar_usuario.php        Novo usuario             │
│ │                                                           │
│ ├── /_impressao/                 [MÓDULO IMPRESSÃO]        │
│ │   ├── impressoras.php          Equipamentos             │
│ │   └── layouts.php              Arquivos                 │
│ │                                                           │
│ ├── /_predefinicoes/             [DADOS CENTRAIS]          │
│ │   ├── custos.php               Gestão custos            │
│ │   ├── substratos.php           Materiais                │
│ │   ├── processos.php            Processos                │
│ │   └── fatores.php              Cálculo                  │
│ │                                                           │
│ ├── index.php                    PÁGINA INICIAL             │
│ ├── login.php                    LOGIN                      │
│ ├── producao.php                 KANBAN PRODUÇÃO           │
│ ├── desktop.php                  DASHBOARD                 │
│ │                                                           │
│ ├── /database/                   DUMPS DB                  │
│ ├── /backups/                    BACKUP AUTOMÁTICO         │
│ ├── /uploads/                    ARQUIVOS ENVIADOS         │
│ └── /lib/                        BIBLIOTECAS (Guzzle)     │
└──────────────────────────────────────────────────────────────┘
```

---

## 5. TABELA: FLUXO REQUISIÇÃO HTTP

```
┌──────────────────────────────────────────────────────────────┐
│ REQUISIÇÃO HTTP - FLUXO COMPLETO                            │
├──────────────────────────────────────────────────────────────┤
│ 1. CLIENTE                                                   │
│    └─ XMLHttpRequest / fetch()                              │
│       POST /ajax/propostas.php?acao=criar                  │
│       Body: { cliente_id: 5, produtos: [...] }            │
│                                                              │
│ 2. SERVIDOR - Validação                                     │
│    ├─ Verifica autenticação ($_SESSION existe?)            │
│    ├─ Verifica autorização (level >= 2?)                   │
│    ├─ Valida dados enviados                                │
│    └─ Se erro → return 400/401/403 + JSON                 │
│                                                              │
│ 3. LÓGICA DE NEGÓCIO                                        │
│    ├─ require classes/ correspondentes                      │
│    ├─ Instancia: $proposta = new Proposta($pdo)           │
│    ├─ Executa: $id = $proposta->Insert(...)               │
│    ├─ Prepara statement PDO                                │
│    ├─ Executa query                                        │
│    └─ Obtém resultado (ID ou erro)                         │
│                                                              │
│ 4. PERSISTÊNCIA                                             │
│    ├─ INSERT INTO propostas VALUES (...)                   │
│    ├─ lastInsertId() retorna ID gerado                     │
│    └─ rowCount() verifica sucesso                          │
│                                                              │
│ 5. RESPOSTA JSON                                            │
│    └─ header('Content-Type: application/json')             │
│       echo json_encode([                                    │
│           'status' => true,                                │
│           'id' => 789,                                      │
│           'mensagem' => 'Proposta criada!'                 │
│       ])                                                    │
│                                                              │
│ 6. CLIENTE (JavaScript)                                     │
│    ├─ response.json()                                       │
│    ├─ Checa resultado.status                               │
│    ├─ Se true → Atualiza UI                                │
│    └─ Se false → Mostra erro                               │
└──────────────────────────────────────────────────────────────┘
```

---

## 6. TABELA: PADRÕES DE QUERY

```
┌──────────────────────────────────────────────────────────────┐
│ PADRÃO 1: SELECT COM BIND                                    │
├──────────────────────────────────────────────────────────────┤
│ $query = "SELECT * FROM clientes WHERE cliente_id = :id";  │
│ $stmt = $pdo->prepare($query);                             │
│ $stmt->bindValue(":id", $id);                              │
│ $stmt->execute();                                          │
│ $resultado = $stmt->fetch(PDO::FETCH_ASSOC);              │
│                                                              │
│ PADRÃO 2: INSERT COM EXECUTE                                │
├──────────────────────────────────────────────────────────────┤
│ $query = "INSERT INTO clientes (...) VALUES (...) ";       │
│ $stmt = $pdo->prepare($query);                             │
│ $stmt->execute([                                           │
│     ':campo1' => $valor1,                                  │
│     ':campo2' => $valor2                                   │
│ ]);                                                        │
│ $novo_id = $pdo->lastInsertId();                          │
│                                                              │
│ PADRÃO 3: UPDATE COM ARRAY                                  │
├──────────────────────────────────────────────────────────────┤
│ $query = "UPDATE clientes SET campo1 = :v1 WHERE id = :id"│
│ $stmt = $pdo->prepare($query);                             │
│ $stmt->execute([':v1' => $val1, ':id' => $id]);           │
│ $linhas_afetadas = $stmt->rowCount();                      │
│                                                              │
│ PADRÃO 4: DELETE                                            │
├──────────────────────────────────────────────────────────────┤
│ $query = "DELETE FROM clientes WHERE cliente_id = :id";   │
│ $stmt = $pdo->prepare($query);                             │
│ $stmt->bindValue(":id", $id);                              │
│ $stmt->execute();                                          │
│ $deletado = $stmt->rowCount() > 0;                         │
│                                                              │
│ PADRÃO 5: FETCHALL (Múltiplos)                             │
├──────────────────────────────────────────────────────────────┤
│ $query = "SELECT * FROM clientes ORDER BY cliente_id DESC";│
│ $stmt = $pdo->prepare($query);                             │
│ $stmt->execute();                                          │
│ $resultados = $stmt->fetchAll(PDO::FETCH_ASSOC);          │
│                                                              │
│ PADRÃO 6: COUNT                                             │
├──────────────────────────────────────────────────────────────┤
│ $query = "SELECT COUNT(*) as total FROM clientes";        │
│ $stmt = $pdo->prepare($query);                             │
│ $stmt->execute();                                          │
│ $total = $stmt->fetch()['total'];                         │
└──────────────────────────────────────────────────────────────┘
```

---

## 7. TABELA: CAMPOS PRINCIPAIS DE CADA TABELA

```
TABELA: clientes
┌──────────────────────┬──────────┬──────────────┐
│ Campo                │ Tipo     │ Descrição    │
├──────────────────────┼──────────┼──────────────┤
│ cliente_id           │ INT (PK) │ ID único     │
│ cliente_codigo       │ INT (UK) │ Código seq.  │
│ cliente_info         │ JSON     │ Dados gerais │
│ cliente_endereco_entrega │ JSON │ Endereço     │
│ cliente_contatos     │ JSON     │ Telefone email│
│ cliente_representante│ INT (FK) │ Usuário      │
│ cliente_rdid         │ STRING   │ ID RDStation │
└──────────────────────┴──────────┴──────────────┘

TABELA: propostas
┌──────────────────────┬──────────┬──────────────┐
│ Campo                │ Tipo     │ Descrição    │
├──────────────────────┼──────────┼──────────────┤
│ proposta_id          │ INT (PK) │ ID único     │
│ proposta_cliente     │ INT (FK) │ Cliente id   │
│ proposta_deal_id     │ STRING   │ ID RDStation │
│ proposta_frete       │ JSON     │ Dados frete  │
│ proposta_criada      │ DATETIME │ Data criação │
│ proposta_revisao     │ INT (FK) │ Rev.anterior │
└──────────────────────┴──────────┴──────────────┘

TABELA: pedidos
┌──────────────────────┬──────────┬──────────────┐
│ Campo                │ Tipo     │ Descrição    │
├──────────────────────┼──────────┼──────────────┤
│ pedido_id            │ INT (PK) │ ID único     │
│ pedido_proposta      │ INT (FK) │ Proposta id  │
│ pedido_estado        │ ENUM     │ Estado atual │
│ pedido_urgente       │ INT      │ 0/1 urgente  │
│ pedido_retirada      │ INT      │ 0/1 retirar  │
│ pedido_finalizado    │ DATETIME │ Data fim     │
│ pedido_criado        │ DATETIME │ Data criação │
└──────────────────────┴──────────┴──────────────┘

TABELA: usuarios
┌──────────────────────┬──────────┬──────────────┐
│ Campo                │ Tipo     │ Descrição    │
├──────────────────────┼──────────┼──────────────┤
│ usuario_id           │ INT (PK) │ ID único     │
│ usuario_email        │ STRING   │ Email (UK)   │
│ usuario_senha        │ STRING   │ Hash bcrypt  │
│ usuario_tipo         │ INT      │ 1/2/3/99     │
│ usuario_token_1      │ STRING   │ Token API    │
│ usuario_criado       │ DATETIME │ Data criação │
└──────────────────────┴──────────┴──────────────┘

TABELA: produtos
┌──────────────────────┬──────────┬──────────────┐
│ Campo                │ Tipo     │ Descrição    │
├──────────────────────┼──────────┼──────────────┤
│ produto_id           │ INT (PK) │ ID único     │
│ produto_cod          │ STRING   │ Código (UK)  │
│ produto_finalidade   │ STRING   │ Ex: Adesivo  │
│ produto_substrato    │ STRING   │ Material     │
│ produto_valor        │ DECIMAL  │ Preço unitário│
│ produto_custos       │ DECIMAL  │ Custo base   │
│ produto_margem       │ DECIMAL  │ % Margem     │
└──────────────────────┴──────────┴──────────────┘

TABELA: proposta_produtos
┌──────────────────────┬──────────┬──────────────┐
│ Campo                │ Tipo     │ Descrição    │
├──────────────────────┼──────────┼──────────────┤
│ proposta_produto_id  │ INT (PK) │ ID item      │
│ proposta_produto_proposta │ INT (FK) │ Proposta │
│ proposta_produto_produto │ INT (FK) │ Produto │
│ proposta_produto_larg│ FLOAT    │ Largura      │
│ proposta_produto_alt │ FLOAT    │ Altura       │
│ proposta_produto_qtd │ INT      │ Quantidade   │
│ proposta_produto_und │ DECIMAL  │ Valor unit.  │
│ proposta_produto_total │ DECIMAL │ Valor total │
└──────────────────────┴──────────┴──────────────┘
```

---

## 8. CÓDIGO: TEMPLATE CLASSE DAO

```php
<?php
// /classes/sua_tabela.php

class SuaTabela {
    public $pdo;
    
    // 📌 CONSTRUTOR: Injetar PDO
    function __construct($pdo) {
        $this->pdo = $pdo;
    }
    
    // ✅ CREATE
    public function Insert($param1, $param2) {
        $query = "INSERT INTO sua_tabela (coluna1, coluna2) VALUES (:p1, :p2)";
        $stmt = $this->pdo->prepare($query);
        $stmt->execute([
            ':p1' => $param1,
            ':p2' => $param2
        ]);
        return $this->pdo->lastInsertId();
    }
    
    // ✅ READ
    public function Select($id) {
        $query = "SELECT * FROM sua_tabela WHERE id = :id";
        $stmt = $this->pdo->prepare($query);
        $stmt->bindValue(":id", $id);
        if ($stmt->execute()) {
            return $stmt->fetch(PDO::FETCH_ASSOC);
        }
        return false;
    }
    
    // ✅ READ ALL
    public function GetAll($filtro = '') {
        $query = "SELECT * FROM sua_tabela $filtro";
        $stmt = $this->pdo->prepare($query);
        if ($stmt->execute()) {
            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        }
        return false;
    }
    
    // ✅ UPDATE
    public function Update($id, $param1, $param2) {
        $query = "UPDATE sua_tabela SET coluna1 = :p1, coluna2 = :p2 WHERE id = :id";
        $stmt = $this->pdo->prepare($query);
        $stmt->execute([
            ':p1' => $param1,
            ':p2' => $param2,
            ':id' => $id
        ]);
        return $stmt->rowCount() > 0;
    }
    
    // ✅ DELETE
    public function Delete($id) {
        $query = "DELETE FROM sua_tabela WHERE id = :id";
        $stmt = $this->pdo->prepare($query);
        $stmt->bindValue(":id", $id);
        if ($stmt->execute()) {
            return true;
        }
        return false;
    }
}
?>
```

---

## 9. CÓDIGO: TEMPLATE AJAX HANDLER

```php
<?php
// /ajax/sua_tabela.php

require_once __DIR__ . "/../requires/connection.php";
require_once __DIR__ . "/../requires/authentication.php";
require_once __DIR__ . "/../classes/sua_tabela.php";

header('Content-Type: application/json');

$acao = $_GET['acao'] ?? '';

try {
    
    $tabela = new SuaTabela($pdo);
    
    if ($acao === 'criar') {
        // Receber dados
        $dados = $_POST['dados'] ?? json_decode(file_get_contents('php://input'), true);
        
        // Validar
        if (!isset($dados['param1']) || !isset($dados['param2'])) {
            http_response_code(400);
            echo json_encode(['status' => false, 'erro' => 'Parâmetros inválidos']);
            exit;
        }
        
        // Executar
        $id = $tabela->Insert($dados['param1'], $dados['param2']);
        
        // Retornar
        http_response_code(200);
        echo json_encode(['status' => true, 'id' => $id, 'mensagem' => 'Criado!']);
        
    } else if ($acao === 'ler') {
        $id = $_GET['id'] ?? null;
        if (!$id) {
            http_response_code(400);
            echo json_encode(['status' => false, 'erro' => 'ID não informado']);
            exit;
        }
        
        $resultado = $tabela->Select($id);
        
        if ($resultado) {
            echo json_encode(['status' => true, 'data' => $resultado]);
        } else {
            http_response_code(404);
            echo json_encode(['status' => false, 'erro' => 'Não encontrado']);
        }
        
    } else if ($acao === 'listar') {
        $resultados = $tabela->GetAll();
        echo json_encode(['status' => true, 'data' => $resultados]);
        
    } else if ($acao === 'atualizar') {
        $dados = json_decode(file_get_contents('php://input'), true);
        $resultado = $tabela->Update($dados['id'], $dados['param1'], $dados['param2']);
        
        if ($resultado) {
            echo json_encode(['status' => true, 'mensagem' => 'Atualizado!']);
        } else {
            http_response_code(500);
            echo json_encode(['status' => false, 'erro' => 'Erro ao atualizar']);
        }
        
    } else if ($acao === 'deletar') {
        $id = $_POST['id'] ?? null;
        if (!$id) {
            http_response_code(400);
            echo json_encode(['status' => false, 'erro' => 'ID não informado']);
            exit;
        }
        
        $resultado = $tabela->Delete($id);
        
        if ($resultado) {
            echo json_encode(['status' => true, 'mensagem' => 'Deletado!']);
        } else {
            http_response_code(500);
            echo json_encode(['status' => false, 'erro' => 'Erro ao deletar']);
        }
        
    } else {
        http_response_code(400);
        echo json_encode(['status' => false, 'erro' => 'Ação não reconhecida']);
    }
    
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['status' => false, 'erro' => $e->getMessage()]);
}
?>
```

---

## 10. CHECKLIST: ANTES DE DEPLOYAR CÓDIGO

```
SEGURANÇA
☐ Todas queries usam Prepared Statements?
☐ PDO com parâmetros bind?
☐ Sem concatenação de strings em SQL?
☐ Senhas com password_hash()?
☐ Token/Session em todas as páginas protegidas?
☐ Validação de input do usuário?
☐ Rate limiting (opcional)?

FUNCIONALIDADE
☐ Testou INSERT/UPDATE/DELETE localmente?
☐ Testou fluxo completo (A→B→C)?
☐ Tratamento de erros implementado?
☐ Edge cases considerados?
☐ Mensagens de erro amigáveis?

PERFORMANCE
☐ Queries otimizadas (índices)?
☐ N+1 queries evitado?
☐ Paginação se muitos registros?
☐ Cache se necessário?

CÓDIGO
☐ Segue padrão DAO?
☐ PDO injetado via constructor?
☐ Método names descritivos?
☐ Comentários quando necessário?
☐ Sem código morto/comentado?

DATABASE
☐ Backup feito?
☐ Constraints definidas?
☐ Foreign keys criadas?
☐ Índices adicionados?

DOCUMENTAÇÃO
☐ Método documentado (comentários)?
☐ Novo AJAX handler documentado?
☐ README atualizado?
☐ Tabelas no BD documentadas?

TESTES
☐ Teste no browser?
☐ Console sem erros?
☐ BD sem erros?
☐ Responsivo (mobile)?

DEPLOY
☐ Todos os arquivos enviados?
☐ Permissões de arquivo corretas?
☐ .env atualizado?
☐ Backup antes de deploy?
```

---

**Fim das tabelas de referência**

Você tem agora um **repositório completo de conhecimento** sobre o Sistema Fixcontrol!

