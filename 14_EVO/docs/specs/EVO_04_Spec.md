# Especificação Funcional: [EVO-04] O Livro-Caixa do Raciocínio (Tabela ai_reasoning_audits)

## 1. Objetivo da Evolução
Criar uma estrutura de dados definitiva e focada em auditoria cognitiva. Esta tabela não guardará linhas de código, mas sim o *raciocínio, contexto e decisão* que a Inteligência Artificial tomou em um determinado momento, bem como a tradução humana dessa decisão. O objetivo primário é fornecer rastreabilidade científica para o Arquiteto-Chefe sobre como as Invariantes estão moldando o comportamento da IA remota ou local.

## 2. Princípio Arquitetural Aplicado
**Data Immutability (Ledger-style) e Evidence-Based Logging.** O banco de dados do CMS opera como um Blockchain cognitivo privado. Uma vez que o raciocínio é depositado pelo Agente ACE, ele nunca pode ser alterado (`UPDATE`) ou deletado (`DELETE`), apenas anexado (`APPEND`). Isso garante uma prova matemática e temporal do comportamento da IA em toda a plataforma GenesisCore.

---

## 3. Topologia e Arquivos Afetados

A implementação ocorrerá puramente na Camada de Dados (SQLite inicial, escalável para Postgres) e no motor de persistência do FastAPI.

### 3.1. Arquivos Core (A Serem Modificados)

#### `cognitive-memory-service/sql/001_init.sql`
**Alterações Técnicas Previstas:**
1.  **Criação do Esquema (Schema):** Adicionaremos a tabela `ai_reasoning_audits` com a seguinte estrutura física de colunas:
    *   `id` (UUID - Chave Primária Automática)
    *   `timestamp` (TIMESTAMP - Data/hora exata do evento)
    *   `source_node` (VARCHAR - Identificador de qual máquina originou a requisição, ex: "PC_CASA", "NOTEBOOK_AFIXGRAF")
    *   `event_context` (TEXT - O que estava sendo feito? ex: "Refatoração de rota login.js")
    *   `raw_ai_learning` (TEXT - O conteúdo original extraído do arquivo `.cursor/aprendizados_brutos.md`)
    *   `saved_tokens` (INTEGER - Custo computacional evitado)
    *   `semantic_translation` (TEXT - A tradução humanizada gerada pelo CMS na hora da inserção, ex: "A IA percebeu o erro X e...". Inicialmente pode ser nula até a EVO-05).
2.  **Gatilhos de Proteção (Triggers):** Reutilizaremos ou criaremos triggers no banco relacional para bloquear `UPDATE` e `DELETE` especificamente nesta nova tabela.

#### `cognitive-memory-service/app/db.py` ou Modelação ORM
**Alterações Técnicas Previstas:**
1.  **Proteção Anti-Deadlock:** Na inicialização da conexão SQLite (função `init_db` ou equivalente), deverá ser injetado compulsoriamente o comando `PRAGMA journal_mode=WAL;`. Esta manobra garante leitura e escrita assíncrona simultânea, evitando que disparos WebSocket congelem o banco (`database is locked`) sob picos de transações simultâneas de vários *ACE Clients*.
2.  Refletiremos a tabela criada em SQL para modelos Pydantic/SQLAlchemy caso a arquitetura local utilize ORMs para as consultas REST do dashboard.

#### `cognitive-memory-service/app/routes/concepts.py` (ou onde couber o Endpoint de Extração)
**Alterações Técnicas Previstas:**
1.  Atualizaremos a rota existente (`/tables/concepts/append` ou nova rota específica `/api/audits/append`) para que, ao receber a "sabedoria bruta" do script `MemoryExtractor` do ACE, os dados sejam direcionados formalmente para a nova tabela `ai_reasoning_audits` com todas as flags de auditoria (timestamp e nódulo de origem preenchidos).

---

## 4. Comportamento e Retornos (Data Lifecycle)

| Ação Analítica | Acontecimento no Banco |
| :--- | :--- |
| **ACE (Nômade)** envia um novo aprendizado bruto ao Extrair Sabedoria. | O CMS aceita o payload. Salva uma nova linha na tabela `ai_reasoning_audits`. Retorna `201 Created` para o ACE. O timestamp gerado é sempre o do Servidor CMS (para evitar falsificação de data na origem). |
| **Administrador** tenta apagar o log via CLI do SQLite porque cometeu um erro. | Banco de Dados rejeita a operação com erro de Trigger: "Immutable Ledger Violation". |

## 5. Próximo Passo Cingulado (Pontos de Atenção)
Com a EVO-04 implantada, passamos a ter um cemitério formidável de "Pós-Mortems" de código que a IA gerou e consertou. No entanto, o texto que o ACE mandará lá da ponta é "frio" e técnico (ex: "erro linha 402 db_conn fail"). 

Para que isso vire a tela principal do nosso **Glass Brain Dashboard (Cérebro de Vidro)**, precisamos de um tradutor simultâneo — um cérebro inteligente rodando no próprio CMS que leia essa inserção técnica e crie o parágrafo humanizado. Essa "Alquimia de Logs" é o motor e a alma da **[EVO-05] O Tradutor Semântico de Ações**.

---
> Aguardando Revisão do Arquiteto. 
> Se a estrutura de banco de dados imutável estiver aprovada no seu padrão de qualidade, por favor ordene: **"Aprovado. Descreva a EVO-05"**.
