# 📊 ANÁLISE COMPLETA DO BANCO DE DADOS - Fixcontrol

**Nível:** Iniciante  
**Data da Análise:** 19/03/2026  
**Versão MySQL:** 5.7 (Docker) / 8.0.33 (Produção remota)  
**Total de Tabelas:** 40  
**Character Set:** utf8mb4 (Suporta emojis e caracteres especiais)  

---

## 📋 ÍNDICE

1. [Visão Geral](#visão-geral)
2. [Estatísticas do Banco](#estatísticas-do-banco)
3. [Tabelas Principais (15)](#tabelas-principais)
4. [Tabelas de Suporte (25)](#tabelas-de-suporte)
5. [Fluxo de Dados Principais](#fluxo-de-dados-principais)
6. [Padrões de Design](#padrões-de-design)
7. [Relacionamentos (ER Diagram)](#relacionamentos)
8. [Glossário de Termos](#glossário-de-termos)

---

## 🎯 Visão Geral

O Fixcontrol é um sistema de gestão de pedidos e propostas para uma empresa gráfica. Ele integra:

- **Gestão de Clientes** (OtkWeb + RD Station CRM)
- **Orçamentos e Propostas** com integração RD Station
- **Pedidos de Produção** com fluxo Kanban (12 estados reais na produção)
- **Catálogo de Produtos** (100+ itens)
- **Controle de Usuários** (Adminstradores, Comercial, Produção)
- **Integração com Correios** (Cálculo de frete)
- **Gestão de Recursos** (Equipamentos, Substratos, Acabamentos)
- **Faturamento e NF-e** via OTKWeb API
- **Logística e Etiquetas** via ViPP Correios API

### 🔹 Formato Denormalizado com JSON

Uma característica importante: muitos dados são armazenados em **colunas JSON** para flexibilidade:

```
cliente_info → {cpf, cnpj, email, endereco{}, contatos[], ...}
pedido_info → {cliente_nome, cnpj, natureza, ...}
proposta_frete → {cep, prazo, valor, servico, ...}
```

Isso permite armazenar estruturas complexas sem criar múltiplas tabelas de junção.

---

## 📊 Estatísticas do Banco

| Métrica | Valor |
|---------|-------|
| **Total de Tabelas** | 40 |
| **Tabelas Principais** | 15 |
| **Tabelas de Suporte** | 25 |
| **Registros de Clientes** | ~950 |
| **Registros de Usuários** | 26 |
| **Registros de Produtos** | ~100+ |
| **Registros de Propostas** | ~550+ |
| **Registros de Pedidos** | ~160+ |
| **Tamanho Estimado** | 15-20 MB |

---

## 🔴 TABELAS PRINCIPAIS (15)

### 1️⃣ `clientes` ⭐ CRÍTICA

**Descrição:** Central de clientes da empresa. Dados denormalizados importados da OtkWeb.

**Estrutura:**
```sql
CREATE TABLE `clientes` (
  cliente_id          INT PRIMARY KEY
  cliente_codigo      INT (ex: 106275)
  cliente_info        JSON (denormalized OtkWeb API response)
  cliente_endereco_entrega    JSON
  cliente_endereco_faturamento JSON
  cliente_contatos    JSON
  cliente_representante INT (FK usuarios)
  cliente_rdid        INT (RD Station CRM ID)
  cliente_data        DATETIME
)
```

**Estrutura do JSON `cliente_info`:**
```json
{
  "cpf": null,
  "cnpj": "17.047.367/0001-63",
  "site": "www.example.com",
  "ativo": true,
  "email": "contato@example.com",
  "endereco": {
    "uf": "RJ",
    "cep": "24020-105",
    "bairro": "CENTRO",
    "cidade": "Niterói",
    "numero": "94",
    "logradouro": "RUA JOSE CLEMENTE",
    "complemento": "SALA 301",
    "codigoIBGEUF": "33",
    "codigoDoMunicipio": "3303302"
  },
  "contatos": [
    {
      "nome": "João Silva",
      "email": "joao@example.com",
      "celular": "(21) 99999-8888",
      "telefone": "(21) 3333-4444",
      "departamento": "Comercial"
    }
  ],
  "razaoSocial": "EXEMPLO LTDA",
  "nomeComercial": "Exemplo",
  "dataDeCadastro": "2023-03-10T00:00:00",
  "codigoDoCliente": 106275,
  "codigoDoVendedor": null,
  "emailsFinanceiro": ["fiscal@example.com"],
  "codigoDaCategoria": 13,
  "descricaoDaCategoria": "CLIENTE - AFIX/OTK/AFIXGRAF",
  "codigoDoTipoDeCliente": 3,
  "descricaoDoTipoDeCliente": "CLIENTE PLACAS"
}
```

**Relacionamentos:**
- `cliente_representante` → `usuarios.usuario_id`
- `cliente_rdid` → Externo (RD Station CRM)

**Dados Reais (Exemplo):**
- Cliente 170: **4C DIGITAL** (Niterói/RJ)
- Cliente 49491: **INDUSTRIAS XHARA LTDA** (Limeira/SP)
- Cliente 79833: **ASAWEB SERVICOS DE MULTIMIDIA LTDA**
- ~950+ clientes totais

---

### 2️⃣ `propostas` ⭐ CRÍTICA

**Descrição:** Orçamentos/Propostas de venda. Ponto de entrada para pedidos.

**Estrutura:**
```sql
CREATE TABLE `propostas` (
  proposta_id               INT PRIMARY KEY
  proposta_deal_id          VARCHAR (RD Station deal ID)
  proposta_revisao          INT
  proposta_filial           INT (FK filiais)
  proposta_cliente          INT (FK clientes)
  proposta_nome_cliente     VARCHAR (cached)
  proposta_representante    INT (FK usuarios)
  proposta_estado           VARCHAR (em negociação/aprovado/declinada)
  proposta_temperatura      INT (50/70 default)
  proposta_identificador    VARCHAR (código único)
  proposta_pedido           INT (FK pedidos - when converted)
  proposta_frete            JSON {cep, prazo, valor, codigo, servico}
  proposta_classificacao    VARCHAR (tipo de trabalho)
  proposta_condicoes        TEXT (payment/delivery terms)
  proposta_orcamento_detalhes JSON
  proposta_contato_comprador VARCHAR
  proposta_pv               INT (PV do cliente)
  proposta_nfe              INT (NFe reference)
  proposta_pedido_venda     INT (FK pedidos_venda)
  proposta_transportadora   JSON
  proposta_data             DATETIME
)
```

**Estados:**
- `em negociação` → Aguardando resposta do cliente
- `aprovado` → Cliente aprovou, pronto para criar pedido
- `declinada` → Cliente rejeitou

**Dados Reais (Exemplos):**
```
ID: 310 → Cliente: "INDUSTRIAS XHARA LTDA"
         Estado: aprovado
         Frete: SEDEX (Correios) R$ 12,00
         Prazo: 10 dias úteis

ID: 318 → Cliente: "ASSOCIACAO FUNDO DE INCENTIVO A PESQUISA"
         Estado: aprovado
         Frete: Econômico (Mandaê) R$ 142,01
         Classificação: "Patrimonio Rígido"
```

**Relacionamentos:**
- `proposta_cliente` → `clientes.cliente_id`
- `proposta_representante` → `usuarios.usuario_id`
- `proposta_filial` → `filiais.filial_id`
- `proposta_pedido` → `pedidos.pedido_id` (quando convertida em pedido)

**Estados Possíveis:**
```
em negociação → Enviada al cliente, aguardando decisão
         ↓
    aprovado → Pode gerar pedido (proposta_pedido)
         ↓
    declinada → Cliente rejeitou
```

---

### 3️⃣ `pedidos` ⭐ CRÍTICA

**Descrição:** Ordens de produção (Pedidos De Serviço). Gerados a partir de Propostas aprovadas.

**Estrutura:**
```sql
CREATE TABLE `pedidos` (
  pedido_id           INT PRIMARY KEY
  pedido_proposta     INT (FK propostas - source)
  pedido_cliente      INT (FK clientes)
  pedido_representante INT (FK usuarios)
  pedido_estado       VARCHAR (aprovado/montagem/impressao/plotter/producao/embalagem/finalizado)
  pedido_arquivos     JSON (array de URLs SharePoint)
  pedido_obs          TEXT (notas internas)
  pedido_data         DATETIME
  pedido_prazo        DATE (data limite de entrega)
  pedido_urgente      INT (boolean: 0/1)
  pedido_amostra      INT (boolean: 0/1)
  pedido_retirada     INT (quantidade de retiradas)
  pedido_info         JSON (dados snapshot do cliente)
  pedido_finalizado   DATETIME (when completed)
)
```

**Estados do Pedido (Kanban - 7 estados):**
```
   APROVADO
       ↓
   MONTAGEM (preparação/design)
       ↓
   IMPRESSÃO (impressoras digitais)
       ↓
   PLOTTER (cortes especiais)
       ↓
   PRODUÇÃO (montagem/acabamento)
       ↓
   EMBALAGEM (packing/shipping prep)
       ↓
   FINALIZADO (entregue/concluído)
```

**Dados Reais (Exemplos):**
```
ID: 67 → Proposta: 310
        Cliente: INDUSTRIAS XHARA LTDA
        Estado: finalizado (completado em 2025-06-10)
        Urgente: NÃO
        Amostra: NÃO

ID: 158 → Proposta: 530
         Cliente: IONTECH INDUSTRIA E COMERCIO LTDA
         Estado: montagem (EM ANDAMENTO)
         Urgente: NÃO
         Prazo: 2026-03-16
         Retirada: 1x

ID: 159 → Proposta: 545
         Cliente: QUALY PERSIANAS
         Estado: montagem (EM ANDAMENTO)
         Observação: "etiqueta resinada mesmo modelo que fizemos"
         Prazo: 2026-03-17
```

**Relacionamentos:**
- `pedido_proposta` → `propostas.proposta_id`
- `pedido_cliente` → `clientes.cliente_id`
- `pedido_representante` → `usuarios.usuario_id`

---

### 4️⃣ `produtos` ⭐ CRÍTICA

**Descrição:** Catálogo de produtos/serviços. ~100+ itens.

**Estrutura:**
```sql
CREATE TABLE `produtos` (
  produto_id          INT PRIMARY KEY
  produto_cod         VARCHAR (ex: Person-Alu-050)
  produto_nfe_cod     VARCHAR (código NFe)
  produto_nfe_desc    TEXT (descrição nota fiscal)
  produto_finalidade  INT (FK finalidades - what it's for)
  produto_substrato   INT (FK substratos - material)
  produto_fator       INT (FK fatores - production complexity)
  produto_ncm         VARCHAR (NCM tax code)
  produto_desc        TEXT (long description)
  produto_peso        DOUBLE
  produto_larg        FLOAT (width)
  produto_alt         FLOAT (height)
  produto_valor_tipo  VARCHAR (m2/und/caixa)
  produto_valor_min   DOUBLE (minimum price)
  produto_valor       DOUBLE (unit price)
  produto_imposto     FLOAT (tax %)
  produto_custos      VARCHAR (comma-separated cost IDs)
  produto_margem      INT (profit margin %)
  produto_valor_margem INT
  produto_data        DATETIME
)
```

**Categorias de Produtos (Exemplos):**

| ID | Código | Descrição | Material | Tipo | Preço |
|----|----|-----|----------|------|-------|
| 27 | Person-Alu-050 | Placa Personalizada Alumínio 0,5mm | Alumínio | m² | R$ 272,50 |
| 29 | Pat-Person-Alu030 | Placa Patrimonial Alumínio | Alumínio | m² | R$ 348,79 |
| 54 | Person-Acri-2 | Placa Acrílico 2mm | Acrílico | m² | R$ 357,00 |
| 55 | Person-Acri-4 | Placa Acrílico 4mm | Acrílico | m² | R$ 474,00 |
| 83 | Etiq-Bopp-Branco | Etiqueta BOPP Branco | BOPP | m² | R$ 138,80 |
| 90 | Etiq-Vinil-Transp-Solvente | Etiqueta Vinil Transparente | Vinil | m² | R$ 82,66 |
| 71 | Vidro | Vidro Temperado 8mm Incolor | Vidro | m² | R$ 425,00 |

**Relacionamentos:**
- `produto_finalidade` → `finalidades.finalidade_id` (for what)
- `produto_substrato` → `substratos.substrato_id` (material)
- `produto_fator` → `fatores.fator_id` (complexity)

---

### 5️⃣ `usuarios` ⭐ CRÍTICA

**Descrição:** Sistema de autenticação e controle de acesso.

**Estrutura:**
```sql
CREATE TABLE `usuarios` (
  usuario_id          INT PRIMARY KEY
  usuario_nome        VARCHAR (60)
  usuario_email       VARCHAR (140) - login
  usuario_senha       VARCHAR (bcrypt hash)
  usuario_avatar      VARCHAR (profile image)
  usuario_tipo        VARCHAR (administrador/comercial/produção/gerente...)
  usuario_email_phpmailer VARCHAR (para envio de emails)
  usuario_senha_phpmailer VARCHAR
  usuario_rd_id       VARCHAR (RD Station user ID)
  usuario_token_1     VARCHAR (session cache)
  usuario_token_2     VARCHAR (session cache)
  usuario_data        DATETIME
  usuario_bloqueado   INT (0=ativo, 1=bloqueado)
  usuario_vendedor    INT (0=não/1=é vendedor)
  usuario_codigo_vendedor INT (link to vendedor code)
)
```

**Usuários (Exemplos):**

| ID | Nome | Email | Tipo | Bloqueado | Vendedor |
|----|------|-------|------|-----------|----------|
| 1 | Guilherme Silva | guilherme.silva@afixgraf.com.br | administrador | Não | Não |
| 2 | Robson Silva | robson.silva@afixgraf.com.br | administrador | Não | Não |
| 8 | Joseane Mendes | joseane.santos@afixgraf.com.br | administrador | Não | **Sim** |
| 22 | Francielli Moura | francielli.moura@afixgraf.com.br | comercial | Não | **Sim** |
| 13 | Produção Afixgraf | producao@afixgraf.com.br | produção | Não | Não |

**Tipos de Usuário:**
- `administrador` → Acesso total ao sistema
- `comercial` → Vendedores criando propostas
- `produção` → Gerenciando workflow de produção
- `gerente produção` → Supervisão da produção
- `gerente comercial` → Supervisão de vendas

**Segurança:**
- Senhas usando `bcrypt` (hash de 60 caracteres)
- Exemplo: `$2y$10$UHAPlP3cnPwuRccBsc.DbOtEIoKH8...`

---

### 6️⃣ `proposta_produtos`

**Descrição:** Itens inclusos em uma proposta (tabela de junção).

**Estrutura:**
```sql
Relação: 1 Proposta → Múltiplos Produtos
Dados: quantidade, preço unitário, subtotal
```

**Dados Reais (Inferido):**
```
Proposta 310 contém:
  - 50 un. de Placa Alu 0,5mm @ R$ 52,00 = R$ 2.600,00
  - Frete SEDEX = R$ 12,00
  SUBTOTAL PROPOSTA = R$ 2.612,00
```

---

### 7️⃣ `pedidos_venda` ⭐ CRÍTICA

**Descrição:** Pedidos de venda para faturamento (NFe). Módulo completo de gestão fiscal e logística, separado do módulo de produção (`pedidos`).

**Estrutura:**
```sql
CREATE TABLE `pedidos_venda` (
  pedido_venda_id         INT PRIMARY KEY
  pedido_venda_proposta   INT (FK propostas)
  pedido_venda_cliente    INT (FK clientes)
  pedido_venda_filial     INT (FK filiais)
  pedido_venda_estado     VARCHAR (aberto/processado/emitido/cancelado)
  pedido_venda_nfe        INT (NFe number - ex: 16941)
  pedido_venda_dados      JSON (full order snapshot com dados fiscais)
  pedido_venda_data       DATETIME
  pedido_venda_processado_data DATETIME
)
```

**Estados do Pedido de Venda (4 abas no UI):**
```
ABERTO → PV criado, pendente de faturamento
    ↓
PROCESSADO → NF-e emitida via OTKWeb API, aguardando SEFAZ
    ↓
EMITIDO → NF-e autorizada pela SEFAZ, pronto para envio
    ↓
CANCELADO → PV cancelado (alternativo)
```

**Página de Detalhe (pedido-venda.php?id=X) — 7 abas + 2 sub-abas:**

| # | Aba | Conteúdo |
|---|---|---|
| 1 | **Informações e Cliente** | Filial, Tipo operação (Saída), Natureza (VENDA), Razão Social, CNPJ/CPF, IE, IM, Endereço completo |
| 2 | **Produtos** | Itens do pedido com NCM, CFOP, quantidades, valores |
| 3 | **Pagamentos** | Condições comerciais, duplicatas |
| 4 | **Frete** | Transportadora (CNPJ, IE, endereço), Modalidade, Tipo volume, Placa, Peso, Valor frete/seguro |
| 5 | **Entrega** | Endereço de entrega diferente do faturamento |
| 6 | **Complementares** | Código de rastreamento, observações adicionais |
| 7 | **Etiqueta Correios** | Integração ViPP Correios: gerar etiqueta, código rastreamento (ex: AD214064939BR), baixar PDF |
| 8 | **Etiqueta Simples** | Etiqueta sem integração Correios para retirada |

**Integração com APIs Externas:**
- **OTKWeb API** → Emite NF-e, retorna número (ex: NF-e #16941)
- **ViPP Correios** → Gera etiquetas de postagem com rastreamento

**Gatilho de Criação:**
O PV é criado quando o pedido de produção atinge o estado **"Pediu Nota"** no Kanban.

**Botões de Ação (menu Ações):**
- Processar Pedido (emitir NF-e)
- Cancelar Pedido
- Recomeçar Pedido
- Imprimir Pedido

**Botões Globais na Listagem:**
- Impressão em Lote
- Relatório (filtros por data/estado/representante)
- Atualizar Estados (sincroniza com OTKWeb)

**Relacionamentos:**
- `pedido_venda_proposta` → `propostas.proposta_id`
- `pedido_venda_cliente` → `clientes.cliente_id`
- `pedido_venda_filial` → `filiais.filial_id`

**Propósito:** Integração completa com sistema de faturamento (NFe via OTKWeb) e logística (Correios ViPP).

---

### 8️⃣ `filiais`

**Descrição:** Unidades/sedes da empresa.

**Dados Reais:**
- Filial 1: SP (Afixgraf)
- Filial 2: RJ (Afixgraf Rio)
- Filial 3: Outro Estado (maybe)

---

### 9️⃣ `finalizações` / `acabamentos` / `substratos`

**Descrição:** Catálogos de materiais e processos.

**Exemplos:**
- `substratos` → Alumínio, Acrílico, PVC, Vinil, Vidro, BOPP, Poliéster
- `acabamentos` → Verniz fosco, brilho, resinagem, etc.
- `finalidades` → Para que serve (Placa Patrimonial, Etiqueta, Sinalização, etc.)

---

### 🔟 `impressoras` / `layouts` / `montagens`

**Descrição:** Recursos produtivos.

**Impressoras:**
- Impressoras digitais UV 1440dpi
- Cortadoras a laser
- Plotters de corte

**Layouts:**
- Projetos de design armazenados

**Montagens:**
- Processos de assemblagem

---

### 1️⃣1️⃣ `afixcontrol_os`

**Descrição:** Work Orders (OS) do sistema AfixControl (integração com plataforma externa).

**Estrutura:**
```sql
  id              INT PRIMARY KEY
  os_number       INT (número da OS)
  os_image        VARCHAR (imagem/referência)
  os_data         JSON (dados completos)
  os_date         DATETIME (criação)
  os_update       DATETIME (última atualização)
```

---

### 1️⃣2️⃣ `otkweb_api`

**Descrição:** Cache de respostas da API OtkWeb.

**Propósito:** Sincronização de clientes com OtkWeb.

---

### 1️⃣3️⃣ `historico`

**Descrição:** Auditoria/log de todas as ações no sistema.

**Registra:**
- Quem fez o quê
- Quando foi feito
- Que tipo de mudança (INSERT/UPDATE/DELETE)

---

### 1️⃣4️⃣ `notificacoes`

**Descrição:** Sistema de notificações internas (push/toast messages).

---

### 1️⃣5️⃣ `comentarios`

**Descrição:** Discussões/comentários em propostas e pedidos.

---

## 📦 TABELAS DE SUPORTE (25 tabelas)

Para referência rápida:

| # | Tabela | Propósito | Registros |
|---|--------|----------|----------|
| 1 | `acabamentos` | Tipos de acabamento (verniz, etc) | ~20 |
| 2 | `afixcontrol_os` | Work Orders externas | ~450 |
| 3 | `comentarios` | Discussões em propostas | ~50 |
| 4 | `compras` | Gestão de compras de insumos | ? |
| 5 | `contatos` | Pessoas de contato por cliente | ~100 |
| 6 | `custos` | Tabela de custos operacionais | ~20 |
| 7 | `estado_pagantes` | Status de pagamento de clientes | ? |
| 8 | `estoque` | Inventário de matérias-primas | ? |
| 9 | `estoque_movimentacoes` | Log de entradas/saídas | ? |
| 10 | `estoque_produtos` | Estoque de produtos finalizados | ? |
| 11 | `fatores` | Fatores de complexidade/produtividade | ~30 |
| 12 | `finalidades` | Para que servem os produtos | ~15 |
| 13 | `fixacoes` | Métodos de fixação (adesivo, parafuso, etc) | ~10 |
| 14 | `fornecedores` | Cadastro de fornecedores | ~50 |
| 15 | `layouts` | Projetos de design | ~600+ |
| 16 | `layouts_conversas` | Chat/mensagens sobre layouts | ~200 |
| 17 | `layouts_mensagens` | Histórico de layout discussions | ~400 |
| 18 | `manutencao` | Manutenção de equipamentos | ~30 |
| 19 | `meta` | Metas de vendas/produção | ? |
| 20 | `montagens` | Processos de montagem | ~10 |
| 21 | `notificacoes` | Sistema de alertas | ~100 |
| 22 | `otkweb_api` | Cache de API | ~950 |
| 23 | `preventivas` | Manutenção preventiva | ~20 |
| 24 | `processos` | Passos de produção | ~15 |
| 25 | `reprovas` | Produtos reprovados/devolvidos | ? |
| 26 | `registros` | Log de atividades | ? |
| 27 | `substratos` | Materiais brutos (Alu, Acrílico, etc) | ~40 |

---

## 🔄 FLUXO DE DADOS PRINCIPAIS

### Fluxo 1: PROPOSTA → PEDIDO

```
┌─────────────────────────────────────────────────────┐
│ 1️⃣  CLIENTE SOLICITA ORÇAMENTO                       │
│     - Telefone, email, formulário web              │
└────────────────────┬────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│ 2️⃣  VENDEDOR CRIA PROPOSTA                           │
│     - Seleciona cliente (clientes.cliente_id)       │
│     - Adiciona produtos (proposta_produtos)         │
│     - Calcula frete (Correios API)                  │
│     - Define condições de pagamento                 │
│     - Status: "em negociação"                       │
│     - Salva em propostas table                      │
└────────────────────┬────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│ 3️⃣  INTEGRAÇÃO RD STATION (CRM)                      │
│     - Cria deal no RD Station                       │
│     - Salva proposta_deal_id                        │
│     - Vincula cliente_rdid                          │
│     - Sincroniza status de negociação               │
└────────────────────┬────────────────────────────────┘
                     ↓
        [CLIENTE ANALISA PROPOSTA]
                     ↓
        ┌───────────────────────┐
        │   Aprova?             │
        └───┬──────────────┬────┘
            │              │
           SIM            NÃO
            │              │
            ↓              ↓
      ┌─────────┐   ┌──────────────┐
      │APROVADO │   │ DECLINADA    │
      └────┬────┘   └──────────────┘
           ↓
┌─────────────────────────────────────────────────────┐
│ 4️⃣  CONVERSÃO: PROPOSTA → PEDIDO                      │
│     - Sistema cria novo PEDIDO                      │
│     - Copia: cliente, produtos, frete, prazos      │
│     - Estado inicial: "aprovado"                    │
│     - Vincula: proposta_pedido = pedido.id          │
│     - Cria histórico de transição                   │
└────────────────────┬────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│ 5️⃣  FLUXO KANBAN DE PRODUÇÃO (7 ESTADOS)             │
│                                                      │
│   APROVADO → MONTAGEM ↔ IMPRESSÃO ↔ PLOTTER         │
│     ↓         ↓          ↓          ↓                │
│     └────→ PRODUÇÃO ← EMBALAGEM → FINALIZADO        │
│                                                      │
│   Cada transição registra:                          │
│   - Quem fez (usuario_id)                           │
│   - Quando (DATETIME)                               │
│   - Notas/observações                               │
│   - Arquivo de referência (design)                  │
└────────────────────┬────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│ 6️⃣  FINALIZAÇÃO & ENTREGA                             │
│     - Produto pronto                                │
│     - Estado: "finalizado"                          │
│     - Registro: pedido_finalizado = DATETIME        │
│     - Envia notificação ao cliente                  │
│     - Prepara para faturamento (pedidos_venda)      │
└─────────────────────────────────────────────────────┘
```

---

### Fluxo 2: INTEGRAÇÃO CORREIOS (FRETE)

```
Proposta → Sistema consulta Correios API
           ↓
        [CEP Cliente]
           ↓
   - Calcula prazo
   - Calcula valor
   - Retorna opções (SEDEX, PAC, etc)
           ↓
   Aramazena em proposta_frete (JSON):
   {
     "cep": "24020-105",
     "prazo": "1",
     "valor": 12,
     "codigo": "03220",
     "servico": "SEDEX (Correios)",
     "atualizado": true
   }
```

---

### Fluxo 3: SINCRONIZAÇÃO OTKWEB

```
Sistema OtkWeb (CRM externo)
           ↓
   [API RESTful]
           ↓
   PHP guzzleHttp client faz requisição
           ↓
   Respostas JSON armazenadas em:
   - clientes (cliente_info, cliente_endereco_*)
   - otkweb_api (cache de respostas)
   - clientes_otk (backup)
           ↓
   Sincroniza ~950 clientes semestralmente
           ↓
   Mantém: CNPJ, endereços, contatos, categoria
```

---

## 🏗️ PADRÕES DE DESIGN

### 1. MVC + DAO Pattern

```
Controller (HTTP Request)
     ↓
Service Layer (Business Logic)
     ↓
DAO Class (Database Access)
     ↓
PDO Query (Prepared Statements)
     ↓
MySQL Database
```

**Exemplo - Classe Cliente:**
```php
// /classes/Cliente.php
public function Insert(array $dados) {}      // INSERT
public function Update($id, array $dados) {} // UPDATE
public function Delete($id) {}               // DELETE
public function GetById($id) {}              // SELECT by PK
public function GetAll() {}                  // SELECT *
public function Search($termo) {}            // WHERE LIKE
```

### 2. JSON Storage Pattern

Alguns dados são armazenados como JSON em colunas MySQL:

```sql
cliente_info → Estrutura complexa aninhada
proposta_frete → Dados de frete (prazo, valor, etc)
pedido_info → Snapshot do cliente no momento do pedido
proposta_transportadora → Dados da transportadora
```

**Vantagem:** Flexibilidade sem alterar schema da tabela

**Desvantagem:** Difícil fazer busca por campos JSON (precisa JSON_EXTRACT)

### 3. Audit Trail (Historico)

Toda mudança de estado é registrada:

```
INSERT INTO historico (tabela, registro_id, acao, usuario_id, dados_antes, dados_depois, data)
```

Permite:
- Saber quem fez cada ação
- Quando foi feita
- Rastreabilidade completa

### 4. Soft Delete Pattern

Alguns registros não são deletados, apenas marcados como inativos:

```
usuario_bloqueado = 1  (ao invés de DELETE)
```

### 5. External ID Pattern

Relacionamentos com sistemas externos:

```
cliente_rdid → RD Station CRM ID
usuario_rd_id → RD Station User ID
proposta_deal_id → RD Station Deal ID
```

Permite sincronização bidirecional.

---

## 🔗 RELACIONAMENTOS (ER Diagram)

### Diagrama Simplificado:

```
   ┌──────────────────────────────────────────┐
   │           CLIENTES                        │
   │  (tipo Jurídica/Física, ~950 registros)  │
   │  PK: cliente_id                           │
   │  FK: cliente_representante → usuarios     │
   │  External: cliente_rdid (RD Station)      │
   └─────────────────┬────────────────────────┘
                     │
         ┌───────────┼──────────┬────────┐
         │           │          │        │
         ↓           ↓          ↓        ↓
    ┌────────────┐  ┌────────────┐  ┌──────────────┐
    │ PROPOSTAS  │  │ PEDIDOS    │  │ CONTATOS     │
    │ (em quórum)│  │ (7 estados)│  │ (pessoas     │
    │ PK: id     │  │ PK: id     │  │  de contato) │
    │ FK: cliente│  │ FK: cliente│  │              │
    │ FK: usuario│  │ FK: usuario│  └──────────────┘
    │ FK: filial │  │ FK: proposta
    │ Ext: deal_id  │
    └────┬───────┘  └────┬────────┘
         │               │
         │               │ proposta_produtos
         │               │ pedidos_produtos
         │               │ pedidos_servicos
         │               │
         └───────┬───────┘
                 ↓
          ┌─────────────────┐
          │ PRODUTOS (~100) │
          │ PK: produto_id  │
          │ FK: finalidade  │
          │ FK: substrato   │
          │ FK: fator       │
          └─────────────────┘


   ┌──────────────────┐
   │ USUARIOS (26)    │
   │ PK: usuario_id   │
   │ Types:           │
   │ - admin          │
   │ - comercial      │
   │ - produção       │
   └──────────────────┘
         ↑
         │ FK de
         │ propostas & pedidos
         │
   ┌──────────────────┐
   │ FILIAIS (3)      │
   │ SP, RJ, MG...    │
   └──────────────────┘


   ┌─────────────────────────────────────┐
   │ RECURSOS DE PRODUÇÃO                │
   │  - impressoras (equipamentos)        │
   │  - layouts (designs/projetos)        │
   │  - montagens (processos)             │
   │  - substratos (Alu, Acrílico, etc)  │
   │  - acabamentos (verniz, etc)         │
   │  - fatores (complexidade)            │
   │  - finalidades (para quê?)           │
   └─────────────────────────────────────┘
```

### Cardinalidade (1:N Relationships):

| Tabela A | Tabela B | Relação | Descrição |
|----------|----------|---------|-----------|
| usuários | propostas | 1:N | Um vendedor faz muitas propostas |
| usuários | pedidos | 1:N | Um supervisor gerencia muitos pedidos |
| clientes | propostas | 1:N | Um cliente recebe muitas propostas |
| clientes | pedidos | 1:N | Um cliente tem muitos pedidos |
| propostas | proposta_produtos | 1:N | Uma proposta contém muitos produtos |
| pedidos | pedidos_produtos | 1:N | Um pedido contém muitos produtos |
| produtos | proposta_produtos | 1:N | Um produto aparece em muitas propostas |
| filiais | propostas | 1:N | Uma filial gerencia muitas propostas |

---

## 📚 GLOSSÁRIO DE TERMOS

| Termo | Significado | Exemplo |
|-------|-------------|---------|
| **Proposta** | Orçamento/Cotação enviado al cliente | "Placa Alumínio 0,5mm - 100 un - R$ 2.600" |
| **Pedido** | Ordem de produção após cliente aprovar proposta | ID: 158 (em montagem) |
| **Cliente** | Empresa ou pessoa jurídica/física | "4C DIGITAL" (CNPJ 17.047.367/0001-63) |
| **Produto** | Item do catálogo (material base) | "Person-Alu-050" = Placa Alu personalizada |
| **Substrato** | Material bruto para fabricação | Alumínio, Acrílico, Vinil, BOPP, Vidro |
| **Acabamento** | Tratamento superficial | Verniz fosco, brilho, resinagem, etc |
| **Fator** | Índice de complexidade/produtividade | 1-30 (maior = mais complexo) |
| **Finalidade** | Para que serve o produto | Sinalização, Patrimonial, Etiqueta, etc |
| **Filial** | Unidade/Sede da empresa | Filial 1 (SP), Filial 2 (RJ) |
| **Usuário** | Pessoa com acesso ao sistema | "Francielli Moura" (comercial) |
| **Deal ID** | ID da oportunidade no RD Station CRM | "681baa33564c3000188e4f8a" |
| **RD ID** | ID de cadastro cliente no RD Station | Número inteiro linkando ao deal |
| **NCM** | Nomenclatura Comum do Mercosul (imposto) | "76061290" (placas de alumínio) |
| **Frete** | Custo de envio/transportadora | R$ 12 - 40 (varia por CEP) |
| **Prazo** | Número de dias para entrega | "1" (SEDEX), "5" (Comum) |
| **Estado/Status** | Situação atual do pedido | Aprovado→Montagem→Impressão→...→Finalizado |
| **Layout** | Arquivo de design/projeto | "projeto_cliente_v2.pdf" |
| **OS** | Ordem de Serviço (Work Order) | Integrada com sistema AfixControl |
| **NFe** | Nota Fiscal eletrônica | Referência para faturamento |
| **Kanban** | Sistema visual de workflow | 7 colunas: aprovado, montagem... finalizado |

---

## ✅ RESUMO EXECUTIVE

### O que você acabou de aprender:

✅ **40 tabelas** organizadas em estrutura relacional  
✅ **3 principais fluxos:**
   1. Proposta → Pedido → Produção → Entrega
   2. Integração com OtkWeb API (clientes)
   3. Integração com RD Station CRM (deals)

✅ **Padrões de design:**
   - MVC + DAO para separação de responsabilidades
   - JSON storage para flexibilidade
   - Audit trail para rastreabilidade
   - External IDs para sincronização

✅ **Dados reais:**
   - ~950 clientes sincronizados
   - 26 usuários do sistema
   - 100+ produtos no catálogo
   - 160+ pedidos em histórico
   - 3 filiais da empresa

### Próximo Passo (Task 2):
Mapear cada tabela para sua correspondente classe PHP DAO na pasta `/classes/`

---

**Documento Gerado:** 19/03/2026  
**Versão:** 1.0
