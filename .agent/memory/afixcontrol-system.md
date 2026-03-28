# AfixControl — Sistema Principal (Prioridade Máxima)

> **Projeto:** AfixControl (Fixcontrol)
> **Dono:** Robson Silva (robson.silva@afixgraf.com.br)
> **Empresa:** Afixgraf — Sinalização Visual e Gráfica
> **Tipo:** CRM + Controle de Produção + Faturamento + Logística
> **Prioridade:** 🔴 MÁXIMA — Sistema core do negócio
> **Última atualização:** 2026-03-23

---

## Stack Tecnológica

| Camada | Tecnologia |
|---|---|
| **Backend** | PHP 7.4 |
| **Database** | MySQL 5.7 (Docker local) — charset `utf8mb4` obrigatório |
| **Frontend** | HTML5 + CSS3 + JavaScript + Bootstrap 5 + jQuery + DataTables |
| **HTTP Client** | GuzzleHttp (APIs externas) |
| **Container** | Docker (PHP 7.4 Apache + MySQL 5.7) |
| **Porta local** | `localhost:8050` |
| **Produção** | `afixcontrol.afixgraf.com.br` |
| **Auth** | Bcrypt + Session/Cookie (`afx_session`) + Tokens |

---

## Localização do Projeto

```
C:\Users\RobsonSilva-AfixGraf\Habilidade_de_agente\WORKSPACE\PROJETOS\AfixcontrolAfixgraf\
```

**Documentação completa:** `uml_e_docs/` (6 arquivos Markdown com diagramas Mermaid)

---

## Arquitetura MVC + DAO

```
/classes/           → Models (DAO Pattern): Cliente, Proposta, Pedido, Produto, Usuario,
                      Montagem, Impressora, Historico, OtkWeb, RDStation, Correios, AfixControl
/ajax/              → Controllers AJAX (40+ handlers, retornam JSON)
/api/               → REST API endpoints
/template/          → Views HTML (header, sidebar, top_header)
/requires/          → connection.php ($pdo) + authentication.php (session check)
/layout/classes/    → database.php (PDO factory)
/includes/          → Helpers (Global.php, Modal.php)
/_clientes/         → Módulo Clientes
/_propostas/        → Módulo Propostas
/_pedidos/          → Módulo Pedidos de Produção
/_configuracoes/    → Módulo Admin
/_impressao/        → Módulo Impressoras
/_predefinicoes/    → Dados centralizados (custos, substratos, processos)
```

**Arquivos Root-Level (35+):** Resolvidos via `.htaccess` regra dinâmica (RewriteRule)

---

## Banco de Dados (40 tabelas)

### Tabelas Críticas

| Tabela | Registros | Propósito |
|---|---|---|
| `clientes` | ~950 | Clientes (dados JSON denormalizados da OTKWeb) |
| `propostas` | ~550+ | Orçamentos com produtos, frete, condições |
| `pedidos` | ~160+ | Ordens de produção (Kanban 12 estados) |
| `pedidos_venda` | ~60+ | Faturamento (NF-e via OTKWeb, 4 estados) |
| `usuarios` | 26 | Auth com 5 níveis RBAC |
| `produtos` | ~100+ | Catálogo com preços, substratos, NCM |
| `proposta_produtos` | N:N | Itens de cada proposta |

### Padrão JSON Storage
Campos como `cliente_info`, `pedido_info`, `proposta_frete`, `pedido_venda_dados` armazenam estruturas complexas em JSON.

---

## Fluxo Completo do Negócio

```
1. CLIENTE (OTKWeb sync) → 2. PROPOSTA (vendedor cria)
        ↓
3. APROVAÇÃO (cliente aprova) → 4. PEDIDO DE PRODUÇÃO
        ↓
5. KANBAN (12 estados):
   Aprovados → Fila Montagem → Montando → Fila Impressão →
   Imprimindo → Impressos → Laser/Corrosão → Plotter →
   Produção → PEDIU NOTA ⭐ → Disp. Retirada → Finalizados
        ↓
6. PEDIDO DE VENDA (PV) — Gatilho: "Pediu Nota"
   - 4 estados: Aberto → Processado → Emitido → (ou Cancelado)
   - 7 abas + 2 sub-abas no detalhe
   - NF-e emitida via OTKWeb API
        ↓
7. LOGÍSTICA
   - Etiqueta Correios via ViPP API (ex: AD214064939BR)
   - Cálculo de frete via SIGEP/Correios
        ↓
8. FINALIZADO — Entregue ao cliente
```

---

## Integrações API

| API | Classe PHP | Propósito |
|---|---|---|
| **OTKWeb** | `classes/otkweb.php` | Clientes + Faturamento + NF-e |
| **RD Station** | `classes/rdstation.php` | CRM (Deals, Contatos) |
| **Correios SIGEP** | `classes/correios.php` | Cálculo de frete |
| **ViPP Correios** | `classes/vipp.php` | Etiquetas + Rastreamento |

---

## Níveis de Usuário (RBAC)

| Nível | Tipo | Acesso |
|---|---|---|
| 1 | Produção | Kanban apenas |
| 2 | Gerente Produção | Kanban + supervisão |
| 3 | Comercial | CRM + Propostas |
| 4 | Gerente Comercial | CRM + Relatórios |
| 5 | Administrador | Acesso total |

---

## Pedido de Venda — Detalhamento Completo

**Rota:** `/pedido-venda?id=X` → `pedido-venda.php`

### 7 Abas + 2 Sub-abas:
1. **Informações e Cliente** — Filial, Tipo operação, Natureza, CNPJ/CPF, IE, Endereço
2. **Produtos** — Itens com NCM, CFOP, quantidades, valores
3. **Pagamentos** — Condições comerciais, duplicatas
4. **Frete** — Transportadora completa (CNPJ, IE, endereço, placa, peso)
5. **Entrega** — Endereço alternativo de entrega
6. **Complementares** — Código rastreamento, observações
7. **Etiqueta Correios** — Integração ViPP (gerar/baixar etiqueta, rastreio)
8. **Etiqueta Simples** — Para retirada sem Correios

### Menu Ações:
- Processar Pedido (emitir NF-e)
- Cancelar / Recomeçar / Imprimir

---

## Routing (.htaccess)

```apache
# Regra dinâmica (linhas 3-7) resolve automaticamente qualquer .php na raiz
RewriteCond %{REQUEST_FILENAME}.php -f
RewriteRule ^([a-zA-Z0-9_-]+)$ $1.php [L,QSA]
```

Todos os 35+ arquivos root-level são resolvidos automaticamente sem rota hard-coded.

---

## Problemas Conhecidos e Resolvidos

| Problema | Causa Raiz | Correção | Data |
|---|---|---|---|
| JSON encoding failure | PDO sem `charset=utf8mb4` | `connection.php` DSN + SET NAMES | 2026-03-23 |
| BOM em arquivos PHP | UTF-8 BOM invisível | `sed` recursivo em `ajax/` e `classes/` | 2026-03-23 |
| "Headers already sent" | `header()` sem `exit()` | `exit()` após redirect em `index.php` | 2026-03-23 |
| MySQL collation error | `utf8mb4_0900_ai_ci` no MySQL 5.7 | Patch no SQL dump | 2026-03-23 |
| Login não funciona | Schema vazio importado | Reimportado `afixcontrol.sql` (22MB) | 2026-03-23 |
| Porta 8000 ocupada | Conflito com outro serviço | Mudou para 8050 no docker-compose | 2026-03-23 |

---

## Regras de Ouro para Modificar o AfixControl

1. **SEMPRE** usar `charset=utf8mb4` na conexão PDO
2. **NUNCA** salvar arquivos PHP com BOM (usar UTF-8 sem BOM)
3. **SEMPRE** usar Prepared Statements (PDO::prepare + bindValue)
4. **SEMPRE** testar AJAX no browser após mudanças (verificar JSON válido)
5. **authentication.php** redireciona para login em HTML — AJAX requests devem tratar isso
6. **Docker:** `docker-compose up -d` na pasta do projeto, porta 8050
7. **Senha padrão dev:** `afix123` (Bcrypt hash no BD)
