# AfixControl: Mapeamento Genético do Banco de Dados (Ultimate Schema)

Este documento detalha 100% da inteligência de dados do sistema AfixControl, mapeando a função técnica e o impacto comercial de cada tabela identificada no escrutínio de 2026.

---

## 1. Núcleo Comercial e de Negociação (The Sales Heart)

### Tabela: `propostas`
- **Função:** Centraliza toda a negociação.
- **Campos Críticos:** 
  - `proposta_revisao`: Controle de versão ISO.
  - `proposta_frete` (JSON): Armazena o objeto de logística (VIPP/Manual).
  - `proposta_orcamento_detalhes` (JSON): Condições de pagamento dinâmicas.
- **Relacionamentos:** Cabeçalho para `proposta_produtos`.

### Tabela: `proposta_produtos`
- **Função:** Detalhamento atômico de cada item vendido.
- **Campos Críticos:**
  - `proposta_resumo` (JSON): Snapshot das regras de cálculo (Substrato + Custos + Adicionais).
  - `proposta_produto_os`: Vínculo com a Ordem de Serviço da Produção.

### Tabela: `proposta_produtos_historico`
- **Função:** Log de auditoria para cada alteração em itens de proposta. Garante a rastreabilidade total exigida pelo usuário.

---

## 2. Núcleo Técnico e de Insumos (The Brain)

### Tabela: `substratos`
- **Função:** Matriz de custos de materiais.
- **Campos Críticos:** `substrato_custo_m2`, `substrato_data_atualizacao`.

### Tabela: `custos` / `processos`
- **Função:** Mão de obra e processos produtivos.
- **Diferença Técnica:** `custos` foca no H/H (Homem/Hora), enquanto `processos` foca na execução técnica repetitiva.

### Tabela: `fatores`
- **Função:** Inteligência de margem. Armazena escalonamentos de desconto baseados em volume e complexidade.

---

## 3. Núcleo de Design e Colaboração (The Art)

### Tabela: `layouts`
- **Função:** Gestão da fila de arte-final.
- **Campos Críticos:** `layout_estado` (0:Fila, 1:Aguardando, 2:Finalizado), `layout_arquivo` (Path do vetor).

### Tabela: `layouts_mensagens`
- **Função:** Chat de briefing entre comercial e arte. Armazena o histórico de conversas para evitar erros de interpretação no layout.

---

## 4. Núcleo Operacional e Industrial (The Shop Floor)

### Tabela: `pedidos` / `pedidos_venda`
- **Função:** Transformação do dado comercial em dado faturável.
- **Campos Críticos:** `valor_frete`, `data_faturamento`, `status_producao`.

### Tabela: `notificacoes`
- **Função:** Sistema de mensageria interna (Taskbar Tray). Alerta usuários sobre aprovações, novos layouts ou mudanças na produção.

### Tabela: `registros`
- **Função:** Log de auditoria global (Quem, Quando, Onde e O Que). Onde cada ação do sistema é carimbada.

---

## 5. Módulos Auxiliares e Específicos

- **`manutencao` / `preventivas`**: Controle de máquinas do chão de fábrica.
- **`meta`**: KPIs de vendas por representante.
- **`montagens`**: Lógica de agrupamento de produtos para produção em lote.
- **`prepostagens`**: Integração direta com a logística reversa e VIPP.

---
**Documento Gerado por Antigravity Sentry v3 - Escrutínio Genético de Dados.**
