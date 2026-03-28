# AfixControl — Mapa de Arquivos → Função

> Referência rápida: qual arquivo faz o quê.
> Última atualização: 2026-03-23

## Arquivos Root (Páginas)

| Arquivo | Rota URL | Função |
|---|---|---|
| `login.php` | `/login` | Tela de login |
| `index.php` | `/` | Redirect para `/desktop` ou `/login` |
| `desktop.php` | `/desktop` | Dashboard principal |
| `producao.php` | `/producao` | Kanban de produção (12 estados) |
| `pedidos-venda.php` | `/pedidos-venda` | Lista de PVs (4 abas) |
| `pedido-venda.php` | `/pedido-venda?id=X` | Detalhe do PV (7+2 abas) |
| `nota-fiscal.php` | `/nota-fiscal?id=X` | Detalhe da NF-e |
| `etiqueta-simples.php` | `/etiqueta-simples?id=X` | Etiqueta sem Correios |
| `prepost-etiqueta.php` | `/prepost-etiqueta?recibo=X` | Etiqueta de pré-postagem |
| `correios.php` | `/correios` | Gestão de postagens |
| `ar.php` | `/ar` | Aviso de recebimento |
| `relatorios.php` | `/relatorios` | Relatórios e insights |

## AJAX Handlers Principais

| Arquivo | Ações (GET `?acao=`) |
|---|---|
| `ajax/propostas.php` | criar, listar, atualizar, deletar propostas |
| `ajax/pedidos.php` | criar pedido, atualizar estado, listar |
| `ajax/pedidos-venda.php` | carregar-pedidos (por estado), criar PV |
| `ajax/pv.php` | abrir-pedido (converte proposta→PV), carregar-pedidos |
| `ajax/clientes.php` | CRUD clientes |
| `ajax/produtos.php` | CRUD produtos |
| `ajax/calculos-orcamento.php` | Calcular custos de proposta |
| `ajax/correios.php` | Calcular frete, gerar etiqueta |
| `ajax/comentarios.php` | Comentários em propostas/pedidos |
| `ajax/montagens.php` | Gestão de montagens |
| `ajax/usuarios.php` | CRUD usuários |

## Classes de Negócio

| Classe | Arquivo | Métodos Principais |
|---|---|---|
| `Cliente` | `classes/clientes.php` | Insert, Update, Delete, Select, Search, GetAll |
| `Proposta` | `classes/propostas.php` | Insert, InsertRevisao, InsertProdutos, UpdateProduto, Select, GetProdutos, GetAll |
| `Pedido` | `classes/pedidos.php` | InsertPedido, Select, SelectByProposta, GetAll, UpdateEstado |
| `Produto` | `classes/produtos.php` | Insert, Update, Delete, Select, GetAll |
| `Usuario` | `classes/usuarios.php` | Insert, Login, Exists, Select, SelectByCodigo, User(token), GetAll, Delete |
| `Montagem` | `classes/montagens.php` | Insert, Delete, Select, GetAll |
| `Impressora` | `classes/impressoras.php` | Insert, Update, Delete, Select, GetAll |
| `Historico` | `classes/historico.php` | SalvarHistoricoProduto, ObterHistoricoProduto |
| `OtkWeb` | `classes/otkweb.php` | DetalhesCliente, CarregarClientes (Guzzle HTTP) |
| `RDStation` | `classes/rdstation.php` | CarregarContatos, CarregarOportunidades (Guzzle HTTP) |
| `Correios` | `classes/correios.php` | calcularFrete, refreshToken (SOAP/REST) |
| `AfixControl` | `classes/afixcontrol.php` | getProposals, getProposal, getProposalProducts |

## JavaScript Frontend

| Arquivo | Responsabilidade |
|---|---|
| `assets/pages/pedidos.js` | DataTable + AJAX para pedidos de produção |
| `assets/pages/producao.js` | Kanban drag&drop |
| `assets/pages/pedidos-venda.js` | DataTable + AJAX para PVs |
| `assets/pages/propostas.js` | Gestão de propostas |
| `assets/pages/clientes.js` | Gestão de clientes |

## Módulos por Pasta

| Pasta | Páginas |
|---|---|
| `_clientes/` | novo-cliente, clientes, alterar-cliente |
| `_propostas/` | nova-proposta, propostas, proposta |
| `_pedidos/` | pedidos, pedido |
| `_configuracoes/` | configuracoes, criar_usuario |
| `_impressao/` | impressoras, layouts |
| `_predefinicoes/` | custos, substratos, processos, fatores |
