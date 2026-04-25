# 🎨 DIAGRAMAS UML AVANÇADOS - HERANÇA, ABSTRAÇÃO E PADRÕES

## 1. DIAGRAMA ESTRUTURAL: HERANÇA DE CLASSES (POSSÍVEL REFATORAÇÃO)

Embora o projeto atual **NÃO utilize herança explícita**, presento a estrutura que **PODERIA** ser implementada para melhorar a arquitetura:

```mermaid
classDiagram
    class EntidadeAbstrata {
        <<abstract>>
        #pdo: PDO
        #tabela: string
        #id_field: string
        +Insert(dados)*
        +Update(id, dados)*
        +Delete(id)*
        +Select(id): array
        +GetAll(filtro): array
        #validar(dados)*: boolean
    }
    
    class Cliente {
        -pdo: PDO
        -otk: OtkWeb
        +Insert(rd_id, representante, cnpj_cpf, nome, detalhes, endereco, contato): array
        +Update(dados): boolean
        +Delete(id): boolean
        +Search(pesquisa): array
        +GetAll(increment): array
    }
    
    class Produto {
        -pdo: PDO
        +Insert(codigo, finalidade, substrato...): int
        +Update(id, codigo, finalidade...): int
        +Delete(id): int
        +Select(id): array
        +GetAll(pdo): array
    }
    
    class Usuario {
        -pdo: PDO
        -nivel: int
        -token: string
        +Insert(nome, email, senha, tipo): boolean
        +Login(email, senha): array
        +Delete(id): boolean
        +Verify(token): array
    }
    
    class Pedido {
        -pdo: PDO
        -estado: EstadoPedido
        +InsertPedido(...): array
        +UpdateEstado(id, estado): boolean
        +MoverKanban(id, novo_estado): boolean
        +GetByProposta(proposta): array
    }
    
    class Proposta {
        -pdo: PDO
        -otk: OtkWeb
        +Insert(filial, cliente, representante...): int
        +InsertRevisao(...): int
        +InsertProdutos(...): boolean
        +UpdateProduto(...): boolean
        +GetAll(increment): array
        +GetProdutos(proposta_id): array
    }
    
    class Montagem {
        -pdo: PDO
        +Insert(produtos, substrato): boolean
        +Select(id): array
        +Delete(id): boolean
        +GetAll(): array
    }
    
    class Impressora {
        -pdo: PDO
        +Insert(nome, tipo, obs): int
        +Update(id, nome, tipo, obs): int
        +Select(id): array
        +Delete(id): int
    }
    
    class Historico {
        -pdo: PDO
        +SalvarHistoricoProduto(produto_id, usuario_id, tipo): boolean
        +ObterHistoricoProduto(produto_id): array
        +ObterHistoricoCompleto(): array
    }
    
    EntidadeAbstrata <|-- Cliente
    EntidadeAbstrata <|-- Produto
    EntidadeAbstrata <|-- Usuario
    EntidadeAbstrata <|-- Pedido
    EntidadeAbstrata <|-- Proposta
    EntidadeAbstrata <|-- Montagem
    EntidadeAbstrata <|-- Impressora
    EntidadeAbstrata <|-- Historico
```

## 2. DIAGRAMA: INTEGRAÇÕES COM PADRÃO ADAPTER

```mermaid
classDiagram
    class ClienteIntegracaoExterno {
        <<interface>>
        +obterDados(id): array
        +sincronizar(dados): boolean
        +validar(dados): boolean
    }
    
    class AdapterOtkWeb {
        -guzzle: GuzzleClient
        -token: string
        -pdo: PDO
        +obterDados(id): array
        +sincronizar(dados): boolean
        +validar(dados): boolean
        -novaConexao(): void
        -renovarToken(): void
    }
    
    class AdapterRDStation {
        -token: string
        -guzzle: GuzzleClient
        +obterDados(id): array
        +sincronizar(dados): boolean
        +validar(dados): boolean
        -carregarDeals(stage, date): array
        -atualizarDeal(deal_id, dados): boolean
    }
    
    class AdapterCorreios {
        -token: string
        -senha_acesso: string
        -cartao_postagem: string
        -guzzle: GuzzleClient
        +obterDados(id): array
        +sincronizar(dados): boolean
        +validar(dados): boolean
        -calcularFrete(origem, destino): decimal
        -gerarEtiqueta(pedido_id): string
    }
    
    ClienteIntegracaoExterno <|.. AdapterOtkWeb
    ClienteIntegracaoExterno <|.. AdapterRDStation
    ClienteIntegracaoExterno <|.. AdapterCorreios
```

## 3. DIAGRAMA UML DETALHADO: CLASSE PROPOSTA

```mermaid
classDiagram
    class Proposta {
        - pdo: PDO
        
        ATRIBUTOS:
        - proposta_id: int
        - proposta_deal_id: string
        - proposta_filial: int
        - proposta_cliente: int
        - proposta_nome_cliente: string
        - proposta_representante: int
        - proposta_identificador: string
        - proposta_revisao: int
        - proposta_frete: json
        - proposta_classificacao: string
        - proposta_condicoes: string
        - proposta_criada: datetime
        
        MÉTODOS DE LEITURA:
        + GetAll(increment: string): array
        + Select(id: int): array
        + SelectByDeal(deal_id: string): array
        + GetProdutos(proposta_id: int): array
        + GetRevisoes(proposta_id: int): array
        + GetHistoricoAlteracoes(proposta_id: int): array
        
        MÉTODOS DE ESCRITA:
        + Insert(filial, cliente, representante, identificador, deal, frete): int
        + InsertRevisao(proposta, filial, cliente, representante, identificador, deal, frete): int
        + InsertProdutos(proposta, produto, larg, alt, qtd, processos, margem, valor_und, valor_custo, valor_total, resumo): boolean
        + Update(id: int, dados: array): boolean
        
        MÉTODOS DE MODIFICAÇÃO:
        + UpdateProduto(id, produto, larg, alt, qtd, processos, margem, valor_und, valor_custo, valor_total, resumo): boolean
        + DeleteProduto(id: int): boolean
        + Delete(id: int): boolean
        + FinalizarProposta(id: int): boolean
        
        MÉTODOS DE NEGÓCIO:
        + MudarStatusPara(id: int, novoStatus: string): boolean
        + CalcularTotalProposta(proposta_id: int): decimal
        + GerarPDF(): string
        + EnviarParaRDStation(proposta_id: int): boolean
        + ImportarRDStation(deal_id: string): int
        
        HELPERS:
        - validarProposta(dados): boolean
        - validarProduto(produto_dados): boolean
        - calcularMarginsProdutos(): void
    }
```

## 4. DIAGRAMA UML DETALHADO: CLASSE PEDIDO

```mermaid
classDiagram
    class Pedido {
        - pdo: PDO
        - estados_validos: array
        
        ATRIBUTOS:
        - pedido_id: int
        - pedido_proposta: int
        - pedido_cliente: int
        - pedido_representante: int
        - pedido_obs: text
        - pedido_prazo: date
        - pedido_urgente: int
        - pedido_amostra: int
        - pedido_retirada: int
        - pedido_info: json
        - pedido_estado: EstadoPedido
        - pedido_finalizado: datetime
        - pedido_criado: datetime
        
        CONSTANTES - ESTADOS:
        + ESTADO_APROVADO: string = "aprovado"
        + ESTADO_MONTAGEM: string = "montagem"
        + ESTADO_IMPRESSAO: string = "impressao"
        + ESTADO_PLOTTER: string = "plotter"
        + ESTADO_PRODUCAO: string = "producao"
        + ESTADO_EMBALAGEM: string = "embalagem"
        + ESTADO_FINALIZADO: string = "finalizado"
        
        MÉTODOS DE LEITURA:
        + Select(id: int): array
        + SelectByProposta(proposta: int): array
        + SelectByCliente(cliente: int): array
        + GetAll(increment: string): array
        + GetByEstado(estado: string): array
        + ObterEstadoAtual(pedido_id: int): string
        
        MÉTODOS DE NEGÓCIO:
        + InsertPedido(proposta, cliente, representante, obs, prazo, urgente, amostra, retirada, info): array
        + UpdateEstado(id: int, estado: string): boolean
        + MoverKanban(id: int, novoEstado: string): boolean
        + Finalizar(id: int): boolean
        + CalcularProducaoRestante(id: int): array
        + VerificarAtrasos(): array
        
        MÉTODOS AUXILIARES:
        - validarEstado(estado: string): boolean
        - verificarTransicaoValida(estadoAtual: string, novoEstado: string): boolean
        - registrarMudancaEstado(pedido_id: int, estado: string, usuario_id: int): void
    }
```

## 5. DIAGRAMA: FLUXO DE ESTADOS DO PEDIDO (STATE PATTERN)

```mermaid
stateDiagram-v2
    [*] --> Aprovado
    
    Aprovado --> Montagem: moverParaMontagem()
    
    Montagem --> Impressao: moverParaImpressao()
    
    Impressao --> Plotter: moverParaPlotter()
    
    Plotter --> Producao: moverParaProducao()
    
    Producao --> Embalagem: moverParaEmbalagem()
    
    Embalagem --> Finalizado: finalizarPedido()
    
    Finalizado --> [*]
    
    Aprovado --> Aprovado: Permanece aguardando
    Montagem --> Montagem: Processamento subsequente
    Impressao --> Impressao: Reprocessamento possível
    
    note right of Aprovado
        - Pedido criado
        - Pronto para produção
        - Validação final
    end
    
    note right of Montagem
        - Substrato preparado
        - Serviços básicos
        - Classe: Montagem
    end
    
    note right of Impressao
        - Arte impressa
        - Validação visual
        - Classe: Impressora
    end
    
    note right of Finalizado
        - Produto completo
        - Pronto para entrega
        - Gerar etiqueta Correios
    end
```

## 6. DIAGRAMA DE COMPOSIÇÃO: PROPOSTA CONTÉM PRODUTOS

```mermaid
classDiagram
    class Proposta {
        - proposta_id: int
        - cliente_id: int
        - proposta_criada: datetime
        + Insert(): int
        + GetProdutos(): array
    }
    
    class ProdutoProposta {
        - proposta_produto_id: int
        - proposta_id: int (FK)
        - produto_id: int (FK)
        - quantidade: int
        - valor_unitario: decimal
        - valor_total: decimal
        + Insert(): boolean
        + Update(): boolean
        + Delete(): boolean
    }
    
    class Produto {
        - produto_id: int
        - codigo: string
        - finalidade: string
        - substrato: string
        - valor_base: decimal
        + Insert(): int
        + GetDados(): array
    }
    
    class Processamento {
        - processo_id: int
        - nome: string
        - custo: decimal
        + GetTodos(): array
    }
    
    Proposta "1" *-- "1..*" ProdutoProposta : contém
    ProdutoProposta "1" o-- "1" Produto : referencia
    ProdutoProposta "1" o-- "0..*" Processamento : utiliza
    
    note right of Proposta
        Uma proposta pode ter
        múltiplos produtos
        (composição)
    end
```

## 7. DIAGRAMA DE AGREGAÇÃO: PEDIDO REFERENCIA PROPOSTA

```mermaid
classDiagram
    class Pedido {
        - pedido_id: int
        - proposta_id: int (FK)
        - cliente_id: int
        - estado: string
    }
    
    class Proposta {
        - proposta_id: int
        - cliente_id: int
    }
    
    class Cliente {
        - cliente_id: int
        - nome: string
    }
    
    class ProdutoProposta {
        - produto_id: int
    }
    
    Pedido "1" --> "1" Proposta : referencia via agregação
    Proposta "1" --> "1" Cliente : associado a
    Proposta "1" --> "1..*" ProdutoProposta : contém
    
    note right of Pedido
        Pedido usa dados de Proposta
        (agregação, não composição)
        Proposta pode existir sem Pedido
    end
```

## 8. DIAGRAMA: CLASSES DE INTEGRAÇÃO - CLIENTE HTTP COMUM

```mermaid
classDiagram
    class GuzzleHttpClient {
        <<library>>
        + post(url, options): Response
        + get(url, options): Response
        + put(url, options): Response
        + delete(url, options): Response
    }
    
    class OtkWeb {
        - guzzle: GuzzleHttpClient
        - token: string
        - pdo: PDO
        + __construct(pdo)
        + DetalhesCliente(cliente_id): array
        + ObterOportunidades(empresa): array
        - novaConexao(): void
    }
    
    class RDStation {
        - token: string
        + CarregarContatos(stage, date, page): array
        + CarregarOportunidades(empresa): array
        + AtualizarDeal(deal_id, dados): boolean
        + CriarDeal(dados): int
    }
    
    class Correios {
        - token: string
        - cartao_postagem: string
        - client: GuzzleHttpClient
        + CalcularFrete(origem, destino, peso): decimal
        + GerarEtiqueta(pedido_id): string
        + RastrearEnvio(codigo): array
        - refreshToken(): void
    }
    
    OtkWeb --> GuzzleHttpClient : usa
    RDStation --> GuzzleHttpClient : usa
    Correios --> GuzzleHttpClient : usa
    
    note right of GuzzleHttpClient
        Biblioteca HTTP compartilhada
        Todas as classes de integração
        utilizam para requisições
    end
```

## 9. DIAGRAMA: CAMADA DE AUTENTICAÇÃO

```mermaid
classDiagram
    class Usuario {
        - usuario_id: int
        - usuario_email: string
        - usuario_senha: string (hash)
        - usuario_tipo: int
        - usuario_token_1: string
        - usuario_token_2: string
        + Login(email, senha): array
        + ValidarToken(token): boolean
        + Delete(id): boolean
    }
    
    class Session {
        <<utility>>
        + Iniciar(): void
        + Destruir(): void
        + ObterValor(chave): mixed
        + DefinirValor(chave, valor): void
    }
    
    class Authentication {
        <<utility>>
        - usuario_atual: Usuario
        + VerificarAutenticacao(): boolean
        + VerificarAutorizacao(nivel): boolean
        + ObterUsuarioAtual(): Usuario
    }
    
    class Autorizacao {
        <<utility>>
        + VerificarNivel(nivel_minimo): boolean
        + VerificarPermissao(acao): boolean
        + ObterNivelAtual(): int
    }
    
    Usuario "1" --> "1" Session : cria
    Session "1" --> "1" Authentication : suporta
    Authentication "1" --> "1" Autorizacao : coordena
```

## 10. DIAGRAMA: FLUXO DE DADOS EM AJAX REQUEST

```mermaid
graph TD
    A["Frontend<br/>form.submit()"] --> B["JavaScript<br/>fetch() ou AJAX"]
    
    B --> C["HTTP POST<br/>/ajax/propostas.php"]
    
    C --> D["Server-side<br/>index.php AJAX Handler"]
    
    D --> E{"1. Verificar<br/>Autenticação"}
    
    E -->|Não autenticado| F["❌ Retornar 401<br/>JSON: error"]
    
    E -->|Sim| G{"2. Verificar<br/>Autorização"}
    
    G -->|Sem permissão| H["❌ Retornar 403<br/>JSON: error"]
    
    G -->|Sim| I["3. Validar<br/>Dados de Entrada"]
    
    I -->|Inválido| J["❌ Retornar 400<br/>JSON: errors"]
    
    I -->|Válido| K["4. Instanciar Classe"]
    
    K --> L["$proposta = new Proposta($pdo)"]
    
    L --> M["5. Executar CRUD"]
    
    M --> N["$proposta->Insert()"]
    
    N --> O["6. Operação DB<br/>PDO Query"]
    
    O -->|Sucesso| P["✅ Retornar 200<br/>JSON: success"]
    
    O -->|Erro| Q["❌ Retornar 500<br/>JSON: error DB"]
    
    P --> R["Frontend<br/>Atualizar UI"]
    
    style A fill:#e3f2fd
    style C fill:#fff3e0
    style E fill:#f3e5f5
    style O fill:#e8f5e9
    style P fill:#c8e6c9
```

## 11. DIAGRAMA: PADRÃO FACTORY PARA CRIAR ENTIDADES

```mermaid
classDiagram
    class EntidadeFactory {
        <<static>>
        - pdo: PDO
        + criarCliente(pdo): Cliente
        + criarProposta(pdo): Proposta
        + criarPedido(pdo): Pedido
        + criarUsuario(pdo): Usuario
        + criarProduto(pdo): Produto
    }
    
    class Cliente {
        - pdo: PDO
    }
    
    class Proposta {
        - pdo: PDO
    }
    
    class Pedido {
        - pdo: PDO
    }
    
    class Usuario {
        - pdo: PDO
    }
    
    class Produto {
        - pdo: PDO
    }
    
    EntidadeFactory ..> Cliente : cria
    EntidadeFactory ..> Proposta : cria
    EntidadeFactory ..> Pedido : cria
    EntidadeFactory ..> Usuario : cria
    EntidadeFactory ..> Produto : cria
    
    note right of EntidadeFactory
        Factory Pattern para
        centralizar criação de objetos
        Simplifica injeção de PDO
    end
```

### Implementação do Factory:
```php
class EntidadeFactory {
    public static function criar($tipo, $pdo) {
        switch($tipo) {
            case 'cliente':
                return new Cliente($pdo);
            case 'proposta':
                return new Proposta($pdo);
            case 'pedido':
                return new Pedido($pdo);
            default:
                throw new Exception("Tipo inválido");
        }
    }
}

// Uso:
$cliente = EntidadeFactory::criar('cliente', $pdo);
$proposta = EntidadeFactory::criar('proposta', $pdo);
```

## 12. DIAGRAMA: OBSERVADOR (OBSERVER PATTERN) PARA HISTÓRICO

```mermaid
classDiagram
    class Observable {
        <<interface>>
        +attach(observer): void
        +detach(observer): void
        +notify(): void
    }
    
    class Pedido {
        - observers: Observer[]
        - estado_atual: string
        +setState(novoEstado): void
        +attach(observer): void
        +notify(): void
    }
    
    class Observer {
        <<interface>>
        +update(pedido): void
    }
    
    class LoggerHistorico {
        +update(pedido): void
    }
    
    class NotificadorEmail {
        +update(pedido): void
    }
    
    class AtualizadorDashboard {
        +update(pedido): void
    }
    
    Observable <|.. Pedido
    Observer <|.. LoggerHistorico
    Observer <|.. NotificadorEmail
    Observer <|.. AtualizadorDashboard
    
    Pedido --> Observer : notifica
    
    note right of Pedido
        Quando estado muda,
        todos os observers
        são notificados
    end
```

## 13. TABELA: COMPARAÇÃO DE PADRÕES NO PROJETO

| Padrão | Implementação Atual | Implementação Ideal | Benefício |
|--------|-------------------|-------------------|-----------|
| **DAO** | ✅ Sim, em todas classes | ✅ Já existe | Segurança, Reutilização |
| **Injeção Dependência** | ✅ Sim, via constructor | ✅ Já existe | Testabilidade, Desacoplamento |
| **Prepared Statements** | ✅ Sim, em todas queries | ✅ Já existe | Previne SQL Injection |
| **MVC** | ✅ Partial | ⚠️ Melhorar | Organização, Manutenibilidade |
| **Herança (Base)** | ❌ Não | ⚠️ Considerar | Código DRY, Reutilização |
| **Interface** | ❌ Não | ✅ Recomendado | Contrato de classes |
| **Factory** | ❌ Não | ✅ Recomendado | Centralizar criação |
| **Observer** | ❌ Não | ✅ Para histórico | Auditoria, Notificações |
| **Adapter** | ✅ Implicit | ✅ Melhorar | Integração externa |
| **Singleton DB** | ❌ Não | ⚠️ Considerar | Uma conexão central |

## 14. DIAGRAMA: PROPOSTA PARA CLASSE BASE (REFATORAÇÃO)

```php
<?php
// Proposta Atual
class Proposta {
    public $pdo;
    
    function __construct($pdo) {
        $this->pdo = $pdo;
    }
    
    public function Insert(...) { }
    public function Update(...) { }
    public function Delete(...) { }
    public function Select($id) { }
}

// ⬇️ REFATORAÇÃO SUGERIDA ⬇️

// 1️⃣ Criar Classe Base Abstrata
abstract class EntidadeBase {
    protected $pdo;
    protected $tabela;
    
    public function __construct($pdo) {
        $this->pdo = $pdo;
    }
    
    abstract public function Insert($dados);
    abstract public function Update($id, $dados);
    abstract public function Delete($id);
    
    public function Select($id) {
        $query = "SELECT * FROM {$this->tabela} WHERE id = :id";
        $stmt = $this->pdo->prepare($query);
        $stmt->bindValue(":id", $id);
        $stmt->execute();
        return $stmt->fetch(PDO::FETCH_ASSOC);
    }
}

// 2️⃣ Proposta herda de EntidadeBase
class Proposta extends EntidadeBase {
    protected $tabela = 'propostas';
    
    public function Insert($filial, $cliente, $representante, ...) {
        // Implementação específica
        $query = "INSERT INTO {$this->tabela} VALUES (...)";
        // ...
    }
    
    public function Update($id, $dados) {
        // Implementação específica
    }
    
    public function Delete($id) {
        // Implementação específica
    }
}
```

## 15. DIAGRAMA COMPLETO: REPOSITÓRIO (REPOSITORY PATTERN)

```mermaid
classDiagram
    class Repositorio {
        <<interface>>
        +buscar(id): Entidade
        +buscarTodos(): array
        +salvar(entidade): void
        +deletar(id): void
    }
    
    class RepositorioCliente {
        - pdo: PDO
        +buscar(id): Cliente
        +buscarTodos(): array
        +buscarPorCNPJ(cnpj): Cliente
        +salvar(cliente): void
        +deletar(id): void
    }
    
    class RepositorioProposta {
        - pdo: PDO
        +buscar(id): Proposta
        +buscarTodos(): array
        +buscarPorCliente(cliente_id): array
        +salvar(proposta): void
        +deletar(id): void
    }
    
    class ServicoCliente {
        - repositorio: RepositorioCliente
        +criar(dados): Cliente
        +buscar(id): Cliente
        +atualizar(id, dados): void
    }
    
    class ServicoProposta {
        - repositorio: RepositorioProposta
        +criar(dados): Proposta
        +buscar(id): Proposta
        +enviarParaRDStation(proposta_id): void
    }
    
    Repositorio <|.. RepositorioCliente
    Repositorio <|.. RepositorioProposta
    
    ServicoCliente --> RepositorioCliente
    ServicoProposta --> RepositorioProposta
```

## 16. DOCUMENTAÇÃO: COMO ESTENDER O SISTEMA

### Adicionar uma Nova Entidade (exemplo: Contrato)

```php
<?php
// 1. Criar classe seguindo o padrão DAO
// /classes/contratos.php

class Contrato extends EntidadeBase {
    protected $tabela = 'contratos';
    
    public function Insert($proposta_id, $cliente_id, $termos) {
        $query = "INSERT INTO contratos (contrato_proposta, contrato_cliente, contrato_termos, contrato_ativo) 
                 VALUES (:proposta, :cliente, :termos, 1)";
        $stmt = $this->pdo->prepare($query);
        $stmt->execute([
            ':proposta' => $proposta_id,
            ':cliente' => $cliente_id,
            ':termos' => $termos
        ]);
        
        return $this->pdo->lastInsertId();
    }
    
    public function Update($id, $dados) {
        // Implementação....
    }
    
    public function Delete($id) {
        // Implementação...
    }
}

// 2. Criar AJAX handler
// /ajax/contratos.php

<?php
require_once __DIR__ . "/../requires/connection.php";
require_once __DIR__ . "/../requires/authentication.php";
require_once __DIR__ . "/../classes/contratos.php";

header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $acao = $_POST['acao'] ?? '';
    
    $contrato = new Contrato($pdo);
    
    if ($acao === 'criar') {
        $id = $contrato->Insert($_POST['proposta'], $_POST['cliente'], $_POST['termos']);
        echo json_encode(['status' => true, 'id' => $id]);
    }
}
?>

// 3. Usar em uma página
// /_contratos/novo-contrato.php

<?php
require_once __DIR__ . "/../classes/contratos.php";

$contrato = new Contrato($pdo);
// Usar o objeto...
?>
```

## 17. DOCUMENTAÇÃO: ADICIONAR NOVO ATRIBUTO

### Adicionar campo em Proposta (exemplo: desconto_total)

```sql
-- 1. Alterar tabela
ALTER TABLE propostas ADD COLUMN proposta_desconto_total DECIMAL(10, 2) DEFAULT 0;

-- 2. Criar migração (backup automático)
-- Já existe em: /backup_database.php
```

```php
// 3. Atualizar classe Proposta
class Proposta {
    public function Insert($filial, $cliente, $representante, $identificador, $deal, $frete, $desconto_total) {
        $query = "INSERT INTO propostas 
                 (proposta_filial, proposta_cliente, ..., proposta_desconto_total) 
                 VALUES (:filial, :cliente, ..., :desconto_total)";
        
        $stmt = $this->pdo->prepare($query);
        $stmt->execute([
            // ... outros parametros
            ':desconto_total' => $desconto_total
        ]);
        
        return $this->pdo->lastInsertId();
    }
}

// 4. Usar no AJAX
// /ajax/propostas.php
$desconto = $_POST['desconto_total'] ?? 0;
$id_proposta = $proposta->Insert(..., $desconto);
```

---

## 18. CHECKLIST: BOAS PRÁTICAS IMPLEMENTADAS

- ✅ Prepared Statements em todas as queries
- ✅ PDO Exceptions
- ✅ Validação de entrada
- ✅ Base de dados normalizada
- ✅ Autenticação por token
- ✅ Logs de auditoria (Historico)
- ⚠️ Separação MVC (parcial - melhorar)
- ⚠️ Tratamento de erros (melhorar)
- ❌ Testes unitários
- ❌ Versionamento de API
- ❌ Documentação de API (swagger)
- ❌ Rate limiting

---

## 19. GUIA: LEITURA DE CÓDIGO - POR TIPO

### 🔷 Para Iniciantes
1. Leia `/layout/classes/database.php` - Entender conexão
2. Leia `/classes/cliente.php` - Entender DAO simples
3. Explore `/includes/global.php` - Entender helpers

### 🔶 Para Intermediários
1. Leia `/classes/proposta.php` - Relacionamentos
2. Leia `/classes/pedido.php` - Estados
3. Explore `/ajax/propostas.php` - Fluxo AJAX

### 🔴 Para Avançados
1. Leia `/classes/otkweb.php` - Integração complexa
2. Leia `/classes/RDStation.php` - HTTP Client
3. Analise fluxo completo: Proposta → Pedido → Produção

---

## 20. DIAGRAMA FINAL: VISÃO 360° DO SISTEMA

```mermaid
graph TB
    subgraph "Entrada de Dados"
        CRM["CRM / RDStation<br/>Oportunidades"]
        CLIENTE["Cliente<br/>Cadastro"]
        VENDEDOR["Vendedor<br/>Interface Web"]
    end
    
    subgraph "Processamento - CRM"
        PROP["Proposta<br/>Criação/Cálculo"]
        COTACAO["Orçamento<br/>Custos + Frete"]
        APROVACAO["Aprovação<br/>Client Aceita"]
    end
    
    subgraph "Persistência"
        BD["MySQL<br/>Propostas<br/>Pedidos<br/>Histórico"]
    end
    
    subgraph "Processamento - Produção"
        KANBAN["Kanban Visual<br/>Estados"]
        ETAPAS["Etapas Produção<br/>7 Estados"]
        ENDERECO["Logística<br/>Frete + Etiqueta"]
    end
    
    subgraph "Saída de Dados"
        RELATORIO["Relatórios<br/>Dashboard"]
        EXPORTACAO["Exportação<br/>PDF/CSV"]
        ENTREGA["Entrega<br/>Rastreamento"]
    end
    
    CRM --> CLIENTE
    CLIENTE --> VENDEDOR
    VENDEDOR --> PROP
    PROP --> COTACAO
    COTACAO --> APROVACAO
    APROVACAO --> BD
    
    BD --> KANBAN
    KANBAN --> ETAPAS
    ETAPAS --> ENDERECO
    ENDERECO --> BD
    
    BD --> RELATORIO
    BD --> EXPORTACAO
    ENDERECO --> ENTREGA
    
    style CRM fill:#e3f2fd
    style PROP fill:#fff3e0
    style KANBAN fill:#e8f5e9
    style ENTREGA fill:#fce4ec
```

---

**Resumo Executivo:**
- **12 Classes principais** com padrão DAO
- **7 Integrações externas** via HTTP
- **3 Camadas** (Apresentação, Negócio, Dados)
- **Arquitetura MVC** parcialmente implementada
- **Oportunidades** para refatoração com herança base e padrões avançados

